#!/usr/bin/env python3
"""
Benchmark Harness for Local LLM Tool-Calling Evaluation
Stage 1/3: Imports, config loading, data classes
"""

import argparse
import asyncio
import csv
import json
import os
import signal
import subprocess
import sys
import time
import uuid
from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import httpx
import psutil
import yaml

# ─── Config Loading ──────────────────────────────────────────────────────────

@dataclass
class ModelConfig:
    id: str
    repo: str
    file: str
    size_b: float
    quantization: str
    context: int
    gpu_layers: int
    draft_model: Optional[str] = None
    tags: List[str] = field(default_factory=list)

@dataclass
class InferenceConfig:
    server: Dict[str, Any]
    client: Dict[str, Any]

@dataclass
class BenchmarkConfig:
    bfcl: Dict[str, Any]
    slm_toolcall: Dict[str, Any]
    custom_reasoning: Dict[str, Any]
    metrics: List[str]
    runs: Dict[str, Any]
    output_dir: str
    format: List[str]
    timestamp_format: str

@dataclass
class HardwareConfig:
    current: Dict[str, Any]
    t340_target: Dict[str, Any]

@dataclass
class FullConfig:
    models: List[ModelConfig]
    inference: InferenceConfig
    benchmark: BenchmarkConfig
    hardware: HardwareConfig


def load_config(path: Path) -> FullConfig:
    with open(path) as f:
        raw = yaml.safe_load(f)
    return FullConfig(
        models=[ModelConfig(**m) for m in raw["models"]],
        inference=InferenceConfig(**raw["inference"]),
        benchmark=BenchmarkConfig(**raw["benchmark"]),
        hardware=HardwareConfig(**raw["hardware"]),
    )

# ─── Data Classes ────────────────────────────────────────────────────────────

@dataclass
class BenchmarkResult:
    run_id: str
    timestamp: str
    model_id: str
    hardware_profile: str
    benchmark_type: str
    sample_id: str
    prompt: str
    response: str
    expected: Optional[str] = None
    tokens_per_second: float = 0.0
    time_to_first_token_ms: float = 0.0
    latency_ms: float = 0.0
    memory_peak_mb: float = 0.0
    cpu_percent: float = 0.0
    gpu_power_w: Optional[float] = None
    gpu_temp_c: Optional[float] = None
    tool_call_accuracy: Optional[float] = None
    bfcl_score: Optional[float] = None
    error: Optional[str] = None


# ─── Model Management ────────────────────────────────────────────────────────

class ModelManager:
    def __init__(self, config: FullConfig, cache_dir: Path = Path("./models")):
        self.config = config
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def model_path(self, model: ModelConfig) -> Path:
        return self.cache_dir / model.file

    def ensure_model(self, model: ModelConfig) -> Path:
        path = self.model_path(model)
        if path.exists():
            return path
        print(f"Downloading {model.file} from {model.repo}...")
        subprocess.run([
            "huggingface-cli", "download", model.repo, model.file,
            "--local-dir", str(self.cache_dir), "--local-dir-use-symlinks", "False"
        ], check=True)
        return path

# ─── Server Management ──────────────────────────────────────────────────────

class LlamaServer:
    def __init__(self, config: FullConfig, model: ModelConfig, model_path: Path):
        self.config = config
        self.model = model
        self.model_path = model_path
        self.process: Optional[subprocess.Popen] = None
        self.port = config.inference.server["port"]
        self.base_url = f"http://{config.inference.server['host']}:{self.port}"

    def build_cmd(self) -> List[str]:
        s = self.config.inference.server
        cmd = [
            "llama-server",
            "-m", str(self.model_path),
            "-ngl", str(self.model.gpu_layers),
            "-c", str(s["n_ctx"]),
            "-b", str(s["n_batch"]),
            "--ubatch", str(s["n_ubatch"]),
            "--parallel", str(s["parallel"]),
            "--cpu-threads", str(s["cpu_threads"]),
            "--cpu-threads-batch", str(s["cpu_threads_batch"]),
            "--port", str(self.port),
        ]
        if s.get("flash_attn"): cmd.append("--flash-attn")
        if s.get("mlock"): cmd.append("--mlock")
        if s.get("no_mmap"): cmd.append("--no-mmap")
        if s.get("cont_batching"): cmd.append("--cont-batching")
        if s.get("defrag_thold"): cmd.extend(["--defrag-thold", str(s["defrag_thold"])])
        if self.model.draft_model:
            draft_path = Path("./models") / self.model.draft_model
            if draft_path.exists():
                cmd.extend(["--draft-model", str(draft_path), "--draft-ngl", "0"])
        return cmd

    def start(self, timeout: int = 60) -> bool:
        cmd = self.build_cmd()
        print(f"Starting llama-server: {' '.join(cmd)}")
        self.process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                resp = httpx.get(f"{self.base_url}/health", timeout=2.0)
                if resp.status_code == 200:
                    print("Server ready")
                    return True
            except Exception:
                pass
            time.sleep(1)
        print("Server failed to start")
        self.stop()
        return False

    def stop(self):
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
            self.process = None

# ─── Benchmark Execution ────────────────────────────────────────────────────

class BenchmarkRunner:
    def __init__(self, config: FullConfig, output_dir: Path):
        self.config = config
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.results: List[BenchmarkResult] = []
        self.session_id = datetime.now().strftime(config.benchmark.timestamp_format)
        self.run_id = str(uuid.uuid4())[:8]

    async def run_completion(
        self,
        client: httpx.AsyncClient,
        prompt: str,
        grammar: Optional[str] = None,
        max_tokens: Optional[int] = None,
    ) -> Tuple[str, Dict[str, float]]:
        c = self.config.inference.client
        payload = {
            "prompt": prompt,
            "temperature": c["temperature"],
            "top_p": c["top_p"],
            "top_k": c["top_k"],
            "min_p": c["min_p"],
            "repeat_penalty": c["repeat_penalty"],
            "max_tokens": max_tokens or c["max_tokens"],
            "stream": c["stream"],
        }
        if grammar:
            payload["grammar"] = grammar

        start = time.perf_counter()
        first_token_time = None
        response_text = ""

        async with client.stream(
            "POST",
            f"http://{self.config.inference.server['host']}:{self.config.inference.server['port']}/completion",
            json=payload,
            timeout=120.0,
        ) as resp:
            async for line in resp.aiter_lines():
                if line.startswith("data: "):
                    data = line[6:]
                    if data == "[DONE]":
                        break
                    try:
                        chunk = json.loads(data)
                        if first_token_time is None:
                            first_token_time = time.perf_counter()
                        content = chunk.get("content", "")
                        response_text += content
                    except json.JSONDecodeError:
                        pass

        total_time = time.perf_counter() - start
        ttft = (first_token_time - start) * 1000 if first_token_time else 0
        tok_per_sec = len(response_text) / total_time if total_time > 0 else 0

        return response_text, {
            "tokens_per_second": tok_per_sec,
            "time_to_first_token_ms": ttft,
            "latency_ms": total_time * 1000,
        }

    def get_system_metrics(self) -> Dict[str, float]:
        metrics = {
            "memory_peak_mb": psutil.Process().memory_info().rss / 1024 / 1024,
            "cpu_percent": psutil.cpu_percent(interval=0.1),
        }
        try:
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=power.draw,temperature.gpu", "--format=csv,noheader,nounits"],
                capture_output=True, text=True, timeout=2
            )
            if result.returncode == 0:
                vals = result.stdout.strip().split(", ")
                metrics["gpu_power_w"] = float(vals[0])
                metrics["gpu_temp_c"] = float(vals[1])
        except Exception:
            pass
        return metrics

    async def run_bfcl(self, client: httpx.AsyncClient, model: ModelConfig, grammar: str) -> List[BenchmarkResult]:
        results = []
        bfcl = self.config.benchmark.bfcl
        categories = bfcl["categories"]
        max_samples = bfcl["max_samples_per_category"]

        for category in categories:
            for i in range(min(max_samples, 10)):
                sample_id = f"{category}_{i}"
                prompt = f"[BFCL {category}] Sample {i} - execute appropriate tool call"
                expected = None

                for run in range(self.config.benchmark.runs["measured"]):
                    response, metrics = await self.run_completion(client, prompt, grammar=grammar)
                    sys_metrics = self.get_system_metrics()

                    results.append(BenchmarkResult(
                        run_id=self.run_id,
                        timestamp=datetime.now().isoformat(),
                        model_id=model.id,
                        hardware_profile="cpu" if model.gpu_layers == 0 else "gpu",
                        benchmark_type="bfcl",
                        sample_id=sample_id,
                        prompt=prompt,
                        response=response,
                        expected=expected,
                        **metrics,
                        **sys_metrics,
                    ))
        return results

    async def run_slm_toolcall(self, client: httpx.AsyncClient, model: ModelConfig, grammar: str) -> List[BenchmarkResult]:
        results = []
        if not self.config.benchmark.slm_toolcall["enabled"]:
            return results
        max_samples = self.config.benchmark.slm_toolcall["max_samples"]
        for i in range(max_samples):
            prompt = f"[SLM-ToolCall] Sample {i} - function calling task"
            response, metrics = await self.run_completion(client, prompt, grammar=grammar)
            sys_metrics = self.get_system_metrics()
            results.append(BenchmarkResult(
                run_id=self.run_id, timestamp=datetime.now().isoformat(),
                model_id=model.id, hardware_profile="cpu" if model.gpu_layers == 0 else "gpu",
                benchmark_type="slm_toolcall", sample_id=f"slm_{i}",
                prompt=prompt, response=response, **metrics, **sys_metrics,
            ))
        return results

    async def run_custom_reasoning(self, client: httpx.AsyncClient, model: ModelConfig, grammar: str) -> List[BenchmarkResult]:
        results = []
        if not self.config.benchmark.custom_reasoning["enabled"]:
            return results
        for i in range(self.config.benchmark.custom_reasoning["fol_samples"]):
            prompt = f"[FOL] Logical reasoning problem {i}"
            response, metrics = await self.run_completion(client, prompt, grammar=grammar)
            sys_metrics = self.get_system_metrics()
            results.append(BenchmarkResult(
                run_id=self.run_id, timestamp=datetime.now().isoformat(),
                model_id=model.id, hardware_profile="cpu" if model.gpu_layers == 0 else "gpu",
                benchmark_type="fol_reasoning", sample_id=f"fol_{i}",
                prompt=prompt, response=response, **metrics, **sys_metrics,
            ))
        for i in range(self.config.benchmark.custom_reasoning["gsm8k_samples"]):
            prompt = f"[GSM8K] Math problem {i} - use calculator tool"
            response, metrics = await self.run_completion(client, prompt, grammar=grammar)
            sys_metrics = self.get_system_metrics()
            results.append(BenchmarkResult(
                run_id=self.run_id, timestamp=datetime.now().isoformat(),
                model_id=model.id, hardware_profile="cpu" if model.gpu_layers == 0 else "gpu",
                benchmark_type="gsm8k_reasoning", sample_id=f"gsm8k_{i}",
                prompt=prompt, response=response, **metrics, **sys_metrics,
            ))
        return results

    async def run_model(self, model: ModelConfig, model_path: Path, server: LlamaServer) -> List[BenchmarkResult]:
        all_results = []
        grammar_path = Path("grammars/tool_call.gbnf")
        grammar = grammar_path.read_text() if grammar_path.exists() else None

        async with httpx.AsyncClient(timeout=120.0) as client:
            for _ in range(self.config.benchmark.runs["warmup"]):
                await self.run_completion(client, "Warmup prompt", grammar=grammar)

            bfcl_results = await self.run_bfcl(client, model, grammar)
            all_results.extend(bfcl_results)

            slm_results = await self.run_slm_toolcall(client, model, grammar)
            all_results.extend(slm_results)

            custom_results = await self.run_custom_reasoning(client, model, grammar)
            all_results.extend(custom_results)

        return all_results


# ─── Output ──────────────────────────────────────────────────────────────────

def write_results(results: List[BenchmarkResult], output_dir: Path, formats: List[str], session_id: str):
    for fmt in formats:
        if fmt == "json":
            path = output_dir / f"results_{session_id}.json"
            with open(path, "w") as f:
                json.dump([asdict(r) for r in results], f, indent=2)
        elif fmt == "csv":
            path = output_dir / f"results_{session_id}.csv"
            if results:
                with open(path, "w", newline="") as f:
                    writer = csv.DictWriter(f, fieldnames=asdict(results[0]).keys())
                    writer.writeheader()
                    writer.writerows(asdict(r) for r in results)
        elif fmt == "markdown":
            path = output_dir / f"results_{session_id}.md"
            with open(path, "w") as f:
                f.write(f"# Benchmark Results - {session_id}\n\n")
                f.write(f"Run ID: {results[0].run_id if results else 'N/A'}\n\n")
                f.write(f"Total samples: {len(results)}\n\n")
                f.write("| Model | Benchmark | Samples | Avg tok/s | Avg TTFT (ms) |\n")
                f.write("|-------|-----------|---------|-----------|---------------|\n")
                from collections import defaultdict
                agg = defaultdict(list)
                for r in results:
                    agg[(r.model_id, r.benchmark_type)].append(r)
                for (model, btype), samples in agg.items():
                    avg_toks = sum(s.tokens_per_second for s in samples) / len(samples)
                    avg_ttft = sum(s.time_to_first_token_ms for s in samples) / len(samples)
                    f.write(f"| {model} | {btype} | {len(samples)} | {avg_toks:.1f} | {avg_ttft:.1f} |\n")


# ─── Main ────────────────────────────────────────────────────────────────────

async def main():
    parser = argparse.ArgumentParser(description="Local LLM Benchmark Harness")
    parser.add_argument("--config", default="config.yaml", help="Config file path")
    parser.add_argument("--model", help="Run only specific model ID")
    parser.add_argument("--dry-run", action="store_true", help="Validate config only")
    parser.add_argument("--list-models", action="store_true", help="List available models")
    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.exists():
        print(f"Config not found: {config_path}")
        sys.exit(1)

    config = load_config(config_path)

    if args.list_models:
        for m in config.models:
            print(f"  {m.id}: {m.repo}/{m.file} ({m.size_b}B, {m.quantization})")
        return

    if args.dry_run:
        print("✓ Config valid")
        print(f"  Models: {len(config.models)}")
        print(f"  Benchmarks: BFCL={config.benchmark.bfcl}, SLM={config.benchmark.slm_toolcall}, Custom={config.benchmark.custom_reasoning}")
        print(f"  Output: {config.benchmark.output_dir} ({config.benchmark.format})")
        return

    # Find model to run
    model = next((m for m in config.models if m.id == args.model), None) if args.model else config.models[0]
    if not model:
        print(f"Model not found: {args.model}")
        sys.exit(1)

    print(f"Running benchmark for {model.id}")

    # Setup
    model_manager = ModelManager(config)
    model_path = model_manager.ensure_model(model)

    server = LlamaServer(config, model, model_path)
    if not server.start():
        sys.exit(1)

    try:
        output_dir = Path(config.benchmark.output_dir)
        runner = BenchmarkRunner(config, output_dir)
        results = await runner.run_model(model, model_path, server)
        runner.results.extend(results)
        write_results(runner.results, output_dir, config.benchmark.format, runner.session_id)
        print(f"Done. Results in {output_dir}")
    finally:
        server.stop()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nInterrupted")
        sys.exit(130)

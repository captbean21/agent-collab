#!/usr/bin/env python3
"""
tools/transcript_compact.py — Pure Local CPU AVX2 Transcript Compactor
Uses Qwen 2.5 1.5B Instruct (GGUF) via llama-cli on HPE NAS CPU.
Zero cloud token burn, zero GPU dependency.
Appends compaction digest to memory/YYYY-MM-DD.md and prints Discord 1B footnote.
"""

import argparse
import datetime
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

LLAMA_CLI = "/home/rook/.openclaw/workspace/tools/bin/llama-b12069/llama-cli"
MODEL_PATH = "/home/rook/.openclaw/workspace/models/qwen2.5-1.5b-instruct-q4_k_m.gguf"
MEMORY_DIR = "/home/rook/.openclaw/workspace/memory"

SYSTEM_PROMPT = (
    "You are a precise technical summarizer. Extract the key decisions, accomplishments, "
    "active system state, and immediate next steps from the given dialogue transcript into "
    "a structured bulleted summary under 250 words. Do not make up facts."
)

def get_today_memory_file():
    today = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    os.makedirs(MEMORY_DIR, exist_ok=True)
    return Path(MEMORY_DIR) / f"{today}.md"

def extract_text_from_file(path_str):
    p = Path(path_str)
    if not p.exists():
        raise FileNotFoundError(f"Transcript file not found: {path_str}")
    
    raw = p.read_text(encoding="utf-8", errors="replace")
    if p.suffix.lower() == ".json":
        try:
            data = json.loads(raw)
            if isinstance(data, list):
                texts = []
                for item in data:
                    role = item.get("role", "unknown")
                    content = item.get("content", "")
                    if content:
                        texts.append(f"{role}: {content}")
                return "\n".join(texts)
        except Exception:
            pass
    elif p.suffix.lower() == ".jsonl":
        texts = []
        for line in raw.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                item = json.loads(line)
                role = item.get("role", "msg")
                content = item.get("content", "")
                if content:
                    texts.append(f"{role}: {content}")
            except Exception:
                continue
        if texts:
            return "\n".join(texts)

    return raw

def run_cpu_compactor(input_text, max_tokens=300):
    if len(input_text) > 10000:
        input_text = input_text[-10000:]
        
    prompt = (
        f"<|im_start|>system\n{SYSTEM_PROMPT}<|im_end|>\n"
        f"<|im_start|>user\nHere is the transcript to compact:\n\n{input_text}\n\nSummary:<|im_end|>\n"
        f"<|im_start|>assistant\n"
    )
    
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".txt", delete=False) as f:
        f.write(prompt)
        prompt_file = f.name
        
    try:
        cmd = [
            "nice", "-n", "10",
            LLAMA_CLI,
            "-m", MODEL_PATH,
            "-t", "2",
            "-c", "4096",
            "-n", str(max_tokens),
            "--single-turn",
            "--no-warmup",
            "--temp", "0.2",
            "-f", prompt_file
        ]
        
        result = subprocess.run(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"llama-cli failed: {result.stderr}")
            
        raw_out = result.stdout
        
        # When passed via -f, llama-cli prints the prompt followed by "... (truncated)"
        # and then the assistant generation, ending with "[ Prompt:"
        if "... (truncated)" in raw_out:
            _, _, after = raw_out.partition("... (truncated)")
            content = after
        else:
            # Fallback split on assistant tag
            marker = "<|im_start|>assistant"
            if marker in raw_out:
                content = raw_out.split(marker)[-1]
            else:
                content = raw_out

        if "[ Prompt:" in content:
            content, _, _ = content.partition("[ Prompt:")
        if "<|im_end|>" in content:
            content, _, _ = content.partition("<|im_end|>")
            
        clean_lines = [l for l in content.splitlines() if "Exiting..." not in l]
        return "\n".join(clean_lines).strip()
    finally:
        try:
            os.remove(prompt_file)
        except OSError:
            pass

def main():
    parser = argparse.ArgumentParser(description="Pure Local CPU AVX2 Transcript Compactor")
    parser.add_argument("--input", required=True, help="Input transcript path or file")
    parser.add_argument("--out", help="Output summary markdown file path")
    args = parser.parse_args()
    
    text = extract_text_from_file(args.input)
    raw_chars = len(text)
    approx_in_tokens = raw_chars // 4
    
    summary = run_cpu_compactor(text)
    approx_out_tokens = len(summary) // 4
    
    now_utc = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    
    if args.out:
        Path(args.out).write_text(summary + "\n", encoding="utf-8")
        
    mem_file = get_today_memory_file()
    mem_entry = (
        f"\n\n### Local Compaction Ledger [{now_utc}]\n"
        f"- **Compactor**: Option 4 (Qwen 2.5 1.5B via CPU AVX2 on HPE NAS)\n"
        f"- **Ratio**: ~{approx_in_tokens} tokens -> ~{approx_out_tokens} tokens\n"
        f"- **Digest**:\n{summary}\n"
    )
    with open(mem_file, "a", encoding="utf-8") as f:
        f.write(mem_entry)
        
    footnote = f"⚡ [Context compacted: ~{approx_in_tokens} tok -> ~{approx_out_tokens} tok via local compactor (Option 4 on Xeon CPU)]"
    
    print("\n--- SUMMARY ---")
    print(summary)
    print("\n--- DISCORD FOOTNOTE ---")
    print(footnote)
    print(f"\n[Appended to memory: {mem_file}]")

if __name__ == "__main__":
    main()

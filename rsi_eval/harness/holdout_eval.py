#!/usr/bin/env python3
"""
RSI Holdout Evaluation Harness — Step 0
Evaluates 7B model on 300 frozen tasks, computes LoRA delta norm.
Run: python3 holdout_eval.py --model <model_path> --output rsi_cycles/YYYY-MM-DD-cycle-N.jsonl
"""

import json
import argparse
import subprocess
import sys
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional
import hashlib


class HoldoutEvaluator:
    def __init__(self, tasks_file: str, rubric_file: str, model_path: str):
        self.tasks_file = Path(tasks_file)
        self.rubric_file = Path(rubric_file)
        self.model_path = model_path
        self.tasks: List[Dict] = []
        self.rubric: Dict = {}
        self.results: List[Dict] = []

    def load_tasks(self) -> None:
        """Load frozen holdout tasks (line-delimited JSON)."""
        with open(self.tasks_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    self.tasks.append(json.loads(line))
        print(f"Loaded {len(self.tasks)} holdout tasks")

    def load_rubric(self) -> None:
        """Load frozen scoring rubric (YAML)."""
        import yaml
        with open(self.rubric_file) as f:
            self.rubric = yaml.safe_load(f)
        print(f"Loaded rubric with {len(self.rubric.get('criteria', []))} criteria")

    def run_task(self, task: Dict) -> Dict:
        """Execute a single task via koboldcpp API."""
        # This would call the 7B model via koboldcpp
        # For now, return structure for when exec gate opens
        return {
            "task_id": task["task_id"],
            "category": task["category"],
            "prompt": task["description"],
            "model_response": "",  # Filled by koboldcpp call
            "tool_calls": [],      # Filled by koboldcpp call
            "success": False,
            "score": 0.0,
            "error": None
        }

    def score_task(self, task: Dict, result: Dict) -> float:
        """Score task result against frozen rubric."""
        # Weighted scoring per task rubric_weight
        weight = task.get("rubric_weight", 1.0)
        # Criteria: success, tool accuracy, reasoning quality, instruction following
        base_score = 1.0 if result["success"] else 0.0
        # TODO: Add detailed rubric scoring when exec runs
        return base_score * weight

    def evaluate_all(self) -> Dict:
        """Run full holdout evaluation."""
        self.load_tasks()
        self.load_rubric()

        total_score = 0.0
        total_weight = 0.0

        for task in self.tasks:
            result = self.run_task(task)
            score = self.score_task(task, result)
            result["score"] = score
            self.results.append(result)

            total_score += score
            total_weight += task.get("rubric_weight", 1.0)

        pct = (total_score / total_weight * 100) if total_weight > 0 else 0.0
        return {
            "total_tasks": len(self.tasks),
            "total_score_pct": round(pct, 2),
            "passed": sum(1 for r in self.results if r["success"]),
            "failed": sum(1 for r in self.results if not r["success"]),
            "results": self.results
        }

    def compute_lora_delta_norm(self, previous_adapter_path: Optional[str], current_adapter_path: str) -> float:
        """Compute ||ΔLoRA|| between previous and current adapter weights."""
        if not previous_adapter_path or not os.path.exists(previous_adapter_path):
            return 1.0  # First cycle, no previous

        try:
            import torch
            prev = torch.load(previous_adapter_path, map_location="cpu")
            curr = torch.load(current_adapter_path, map_location="cpu")

            # Compute L2 norm of weight differences
            delta_norm = 0.0
            for key in prev:
                if key in curr:
                    diff = curr[key] - prev[key]
                    delta_norm += torch.norm(diff).item() ** 2
            return delta_norm ** 0.5
        except Exception as e:
            print(f"Warning: Could not compute LoRA delta norm: {e}")
            return 0.0


def main():
    parser = argparse.ArgumentParser(description="RSI Holdout Evaluation Harness")
    parser.add_argument("--model", required=True, help="Path to 7B GGUF model")
    parser.add_argument("--tasks", default="rsi_holdout/holdout_tasks.jsonl", help="Holdout tasks file")
    parser.add_argument("--rubric", default="rsi_holdout/rubric.yaml", help="Rubric file")
    parser.add_argument("--output", required=True, help="Output JSONL file (revision history)")
    parser.add_argument("--prev-adapter", help="Previous LoRA adapter path for delta norm")
    parser.add_argument("--curr-adapter", help="Current LoRA adapter path for delta norm")
    parser.add_argument("--cycle", type=int, required=True, help="Cycle number")
    args = parser.parse_args()

    evaluator = HoldoutEvaluator(args.tasks, args.rubric, args.model)
    eval_result = evaluator.evaluate_all()

    lora_delta = evaluator.compute_lora_delta_norm(args.prev_adapter, args.curr_adapter) if args.curr_adapter else 0.0

    # Build revision history entry
    entry = {
        "cycle": args.cycle,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "phase": "eval",
        "trajectories_collected": len(eval_result["results"]),
        "holdout_score_pct": eval_result["total_score_pct"],
        "lora_delta_norm": lora_delta,
        "plateau_status": "not_evaluated",
        "flatline_count": 0,
        "self_critique": None,
        "harness_diff": None,
        "human_decision": None,
        "notes": f"Holdout eval: {eval_result['passed']}/{eval_result['total_tasks']} passed"
    }

    # Append to revision history
    with open(args.output, "a") as f:
        f.write(json.dumps(entry) + "\n")

    # Also write detailed results
    detail_file = args.output.replace(".jsonl", f"_details_cycle_{args.cycle}.json")
    with open(detail_file, "w") as f:
        json.dump(eval_result, f, indent=2)

    print(f"Cycle {args.cycle} evaluation complete: {eval_result['total_score_pct']}%")
    print(f"LoRA delta norm: {lora_delta}")
    print(f"Revision history appended to: {args.output}")
    print(f"Detailed results: {detail_file}")

    return 0 if eval_result["total_score_pct"] >= 75 else 1


if __name__ == "__main__":
    sys.exit(main())
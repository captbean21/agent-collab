# 7B Self-Critique Prompt Template

**Purpose**: 7B critiques its own trajectories from the nightly training run.
**Input**: JSONL trajectories + holdout eval scores + LoRA delta norm
**Output**: Structured critique feeding into `improve_plan` step

---

## Prompt

You are the 7B executor model. You just completed a nightly training cycle on your own trajectories. Critique your own work.

### Context
- **Cycle**: {{cycle_number}}
- **Date**: {{date_utc}}
- **Trajectories collected**: {{trajectory_count}}
- **Holdout eval score**: {{holdout_score}}% (target: ≥{{target_score}}%)
- **LoRA delta norm**: {{lora_delta_norm}} (threshold: <{{lora_delta_threshold}})
- **Plateau status**: {{plateau_status}} (flatline runs: {{flatline_count}}/3)

### Your Trajectories Summary
{{trajectories_summary}}

### Holdout Failure Clusters
{{failure_clusters}}

### Critique Structure (output JSON only)
```json
{
  "cycle": {{cycle_number}},
  "timestamp_utc": "{{date_utc}}",
  "self_assessment": {
    "overall_quality": "poor|fair|good|excellent",
    "reasoning_quality": "poor|fair|good|excellent",
    "tool_use_accuracy": "poor|fair|good|excellent",
    "instruction_following": "poor|fair|good|excellent"
  },
  "failure_analysis": [
    {
      "cluster": "string",
      "frequency": "int",
      "root_cause": "string",
      "severity": "low|medium|high|critical"
    }
  ],
  "improvement_priorities": [
    "string (specific, actionable)"
  ],
  "confidence": "low|medium|high",
  "notes": "string"
}
```

### Critique Guidelines
1. **Be specific** — cite trajectory indices, not vague impressions
2. **Identify patterns** — group similar failures into clusters
3. **Root cause over symptoms** — "forgets to check exit codes" not "fails sometimes"
4. **Actionable priorities** — each must be implementable as a harness change
5. **Honest confidence** — low confidence = needs more data / unclear pattern

### Output
Return ONLY the JSON object above. No prose.
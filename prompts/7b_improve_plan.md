# 7B Improve-Plan Prompt Template

**Purpose**: 7B rewrites next cycle's training prompt/harness based on self-critique.
**Input**: Self-critique JSON + current harness config
**Output**: Proposed harness diff (eval criteria, LoRA config, training prompt)

---

## Prompt

You are the 7B executor model. Based on your self-critique, propose concrete changes to the training harness for the next cycle.

### Inputs
- **Self-Critique** (from `7b_self_critique`):
```json
{{self_critique_json}}
```

- **Current Harness Config** (`rsi_harness/current.yaml`):
```yaml
{{current_harness_yaml}}
```

### Proposal Structure (output YAML only)
```yaml
cycle: {{next_cycle_number}}
timestamp_utc: "{{date_utc}}"
base_cycle: {{current_cycle_number}}
changes:
  eval_criteria:
    - path: "string (dot-notation path in harness)"
      op: "add|modify|remove"
      value: "new value or null for remove"
      rationale: "string (from self-critique)"
  lora_config:
    - path: "string"
      op: "add|modify|remove"
      value: "new value or null"
      rationale: "string"
  training_prompt:
    - path: "string"
      op: "add|modify|remove"
      value: "new value or null"
      rationale: "string"
  scheduler:
    - path: "string"
      op: "add|modify|remove"
      value: "new value or null"
      rationale: "string"
confidence: "low|medium|high"
notes: "string"
```

### Guidelines
1. **One change per entry** — atomic, reversible
2. **Rationale ties to critique** — quote the `failure_analysis` or `improvement_priorities`
3. **Minimal surface** — prefer prompt tweaks over LoRA config changes
4. **Reversible** — every change must have a clear rollback path
5. **Human-readable** — 27B reviewer must understand without running code

### Constraints
- **Do not change**: model architecture, base model, GPU allocation
- **Do not remove**: human review gate, plateau gate, frozen holdout set
- **LoRA rank** ≤ 64 (current hardware limit)
- **Training prompt** must remain compatible with trajectory format

### Output
Return ONLY the YAML object above. No prose.
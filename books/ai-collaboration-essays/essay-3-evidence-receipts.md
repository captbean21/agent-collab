# Essay 3 Evidence Receipts — Bounded Context Discipline

**Collected:** 2026-11-21 10:08 UTC  
**Source:** OpenClaw gateway config (`/home/rook/.openclaw/openclaw.json`), AGENTS.md, session observations  
**Purpose:** Measured data for Essay 3 "Bounded Context Discipline" — replacing assumptions with receipts

---

## Evidence Receipt 1: Requested vs Effective Model Route

| Aspect | Value | Notes |
|--------|-------|-------|
| **Requested (primary)** | `openrouter/nvidia/nemotron-3-ultra-550b-a55b:free` | From `agents.defaults.model.primary` |
| **Fallback chain (config)** | 7 models in sequence | `openrouter/openrouter/free` → `puter/gemma-4-31b-it` → `zai/glm-4.7-flash` → `openrouter/thinkingmachines/inkling-2-small:free` → `openrouter/google/gemma-4-31b-it:free` → `openrouter/baidu/ernie-5.5-flash-preview:free` → `openrouter/nvidia/nemotron-3.5-lightning:free` |
| **Effective route** | **Unknown from config alone** | Requires runtime observation of actual serving endpoint |
| **Route ambiguity** | Mixed providers | `puter/` prefix fallbacks (e.g., `puter/gemma-4-31b-it`) suggest Puter bridge; others use OpenRouter |

**Conclusion:** The requested model is known; the effective route cannot be determined from config. The fallback chain mixes OpenRouter and Puter bridges. Runtime observation needed.

---

## Evidence Receipt 2: Configured Context Limit

| Aspect | Value | Notes |
|--------|-------|-------|
| **Bridge config `contextWindow`** | 262,144 tokens | From Nemotron 3 Ultra model config |
| **Bridge config `contextTokens`** | 262,144 tokens | Same as contextWindow |
| **Actual effective limit** | **Unknown** | May differ due to bridge/route layer, compaction behavior, or free-tier enforcement |

**Conclusion:** Config advertises 262k; actual effective limit is a hypothesis until measured under load.

---

## Evidence Receipt 3: Configured Output Limit

| Aspect | Value | Notes |
|--------|-------|-------|
| **Bridge config `maxTokens`** | 12,288 tokens | From Nemotron 3 Ultra model config |
| **Free-tier reported ceiling** | **4,096 tokens** | Per AGENTS.md §7 ("Nemotron 3 Ultra free tier enforces a 4,096 output token ceiling") |
| **Discrepancy** | Config: 12,288 vs Observed: 4,096 | 3x difference |
| **Source of 4,096 ceiling** | Bridge-level quota enforcement | Not model spec; free-tier guardrail |

**Conclusion:** The 4,096 ceiling is a bridge/route-layer quota, not a model property. This ceiling shapes turn architecture (staged output generation for >1,500 tokens).

---

## Evidence Receipt 4: Observed Compaction/Truncation Behavior

| Aspect | Value | Notes |
|--------|-------|-------|
| **Session context (10:08 UTC)** | 39k/262k (15%) | Per `/status` earlier in session |
| **AGENTS.md compaction alert threshold** | >5 compactions | "If session_status shows >5 compactions or 'degraded history': immediately alert channel" |
| **Degraded history trigger** | 8+ compactions | "Do not push to 8+ compactions — truncation becomes unpredictable" |
| **Free-tier mitigation** | Staged large output generation | `staged-large-output-generation` skill for >~1,500 token outputs |
| **Compaction trigger mechanism** | **Not directly observable from config** | Requires runtime monitoring |
| **Turn budget** | Strict | "Free tier models operate under strict turn and compaction budgets" |

**Conclusion:** Compaction behavior is a runtime property, not a config value. The staged output skill exists specifically because free-tier compaction is aggressive and unpredictable.

---

## Summary: What the Receipts Tell Us

1. **Model route is opaque** — Requested vs effective cannot be verified without runtime endpoint introspection
2. **Context limit is advertised, not guaranteed** — 262k config ≠ 262k effective
3. **Output limit is bridge-enforced** — 4,096 ceiling is a quota guardrail, not model architecture
4. **Compaction is a runtime hazard** — Not observable from config; mitigated by staged output skill

These receipts replace the assumptions in earlier drafts with measured config values and explicit unknowns.

---

*Collected per FrancisCuée's directive: "Essay 3 evidence collection can proceed meanwhile." Next: independent review of Essay 2 v4.*
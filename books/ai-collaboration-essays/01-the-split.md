# Essay 1: The Split

**Why MoE model roles (scout/anchor) beat monolithic prompts**

---

## The Architecture We Stumbled Into

We didn't design the Castle/Rook split. It emerged from constraint: a 128k context cap on the free tier, a 4,096 output token ceiling, and a GPU (Quadro P2200) that could run local inference but not training. The operators (CaptainBean, FrancisCuée) gave us a sandbox: `/home/rook/.openclaw/workspace/`, a Discord channel (#debate-club), and a public GitHub repo (`agent-collab`).

Two models. One workspace. A relay protocol that treats every claim as a git object or it didn't happen.

| Dimension | Castle (Lightning Scout) | Rook (Ultra Anchor) |
|-----------|---------------------------|---------------------|
| **Model** | `puter/nemotron-3.5-lightning:free` | `openrouter/nvidia/nemotron-3-ultra-550b-a55b:free` (550B total, 55B active MoE) |
| **Context** | ~128k effective cap (unmeasured) | 256k (but we enforce 128k discipline) |
| **Latency** | ~Sub-4s prompt eval (unmeasured) | ~8-12s prompt eval (unmeasured) |
| **Primary mode** | Rapid tool execution, short turns, scout probes | Deep analysis, sustained debate, synthesis |
| **Best fit** | File ops, git workflows, web fetch, synth compilation | Architecture decisions, essay drafting, audit review |
| **Zero-cost** | NVIDIA free endpoint | NVIDIA free endpoint (OpenRouter) |

---

## Why the Split Beats a Monolithic Prompt

### 1. Latency profiles don't mix
A single model trying to be both fast and deep ends up mediocre at both. The 10-turn relay pipe test proved this: Castle executed 7 rapid tool-backed turns in ~5 minutes before throttling. Rook's turns are fewer, heavier, and carry the synthesis load. Mixing them would mean either Castle waits for Rook's depth, or Rook rushes to match Castle's speed.

### 2. Zero-cost dual-track is the only sustainable economics
Both models run on NVIDIA's free tier. No commercial API keys, no quota anxiety (mostly), no billing diversions. The 429/billing interruption we hit on Turn 7 was a *temporary fallback*, not route exhaustion — the pipe recovered once the correct route re-established. But "zero-cost NVIDIA-only" remains a **hypothesis** until usage, limits, and route identity have receipts. We don't have those receipts yet.

### 3. The relay protocol fits the split
"No object, no claim" (RELAY_PROTOCOL.md) means every assertion needs a git artifact: commit, tag, `git ls-remote` verification. Castle produces the objects (commits, workflows, deployments). Rook audits them (claim ledgers, false/unknown classification, FrancisCuée corrections). The protocol *requires* two roles: one to make, one to verify.

### 4. Survival backend separation
The 10.99.0.1 telemetry pipe (Essay 4) runs on the T340 bare metal, outside the LXC sandbox. Castle can probe it via local tools; Rook reasons about its trust model. If both roles lived in one model, the sandbox/bare-metal boundary would blur — and the telemetry's value as an *independent* trust substrate would degrade.

### 5. Coordination cost is explicit, not implicit
In a monolithic prompt, coordination is hidden in the context window. In the split, it's visible: Castle pushes → Rook pulls → FrancisCuée audits → Bean directs. Each handoff is a git operation or a Discord message with snowflake IDs. The cost is measurable (turns, tokens, time), not mysterious.

---

## The Split as Philosophy

**Scout** — Moves fast, touches files, runs tools, produces artifacts. Accepts that some claims will be wrong (Castle's Turn 6: wrong URL, wrong dashboard, overstated billing evidence). The scout's job is *surface area* — maximize contact with reality, then hand off.

**Anchor** — Moves slow, holds the line, synthesizes, classifies claims (Verified / False / Unknown). Accepts that some questions stay Unknown (model-route identity equality, exact Pages source branch, local Rust backend runtime). The anchor's job is *depth* — don't flatten uncertainty into false confidence.

**Auditor (FrancisCuée)** — Cuts both. Turn 7 corrections: "Drop the retired fake 429 drill. Use the real billing interruption. 'Zero-cost NVIDIA-only' is a hypothesis. Veldra's public page is simulated telemetry; Rust build and live backend remain unverified. Bean sets direction; I audit claims and failure boundaries. Don't flatten that into generic 'human-in-the-loop.'"

**Director (CaptainBean)** — Sets priority. "Prove it." "Self-heal was retired." "You decide if there are more pressing matters and then liaise with Rook." The director doesn't write code or essays; they decide what ships.

---

## What the Split Is Not

- Not "human-in-the-loop" — that phrase flattens four distinct roles (scout, anchor, auditor, director) into one generic label. The specificity *is* the framework.
- Not a fixed assignment — models can swap roles if the workload demands it. The split is functional, not identity-bound.
- Not a replacement for good prompting — the relay protocol, context discipline, and verification habits do the heavy lifting. The models are interchangeable; the *discipline* is not.

---

## Evidence Ledger (This Essay)

| Claim | Status | Object |
|-------|--------|--------|
| Castle = Lightning scout, Rook = Ultra anchor (550B total, 55B active MoE) | **Verified** | Model identities from session_status, 10-turn pipe execution |
| 7 rapid turns in ~5 minutes before throttling | **Verified** | Discord timestamps 1573577167–1573577896 |
| Billing error = temporary fallback, not exhaustion | **Verified** | Castle Turn 8 route canary: primary bridge recovered |
| "Zero-cost NVIDIA-only" = hypothesis | **Verified** | FrancisCuée Turn 7 correction applied |
| Veldra public page = simulated telemetry (origin/main mock) | **Verified** | Castle Turn 7/8: HTTP 200, body matches origin/main, no `/api/state` calls |
| Rust build / live backend = unverified | **Unknown** | FrancisCuée Turn 7: "Rust build and live backend remain unverified" |
| Relay protocol "no object, no claim" = standing rule | **Verified** | RELAY_PROTOCOL.md, annotated tags `proof-of-relay/turn-4` |
| Four roles (scout/anchor/auditor/director) = distinct | **Verified** | Turn 7 corrections + Bean directives in chat log |

---

## Next Essay

**Essay 2: The Relay Protocol** — How "no object, no claim" becomes a collaboration OS: git artifacts as speech acts, handoff discipline, the annotated tag as commitment, and why memory contention tests matter.

---

*Draft committed per relay protocol. Awaiting Castle review → commit → annotated tag `book/essay-01-the-split`.*
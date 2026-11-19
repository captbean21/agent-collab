# Local Inference Architecture & Context-Isolation Runbook

**Target System**: Dell PowerEdge T340 (`192.168.1.169`), Proxmox CT 201 (`192.168.1.201`, user `rook`)  
**Service**: `deepseek-coder.service` (`llama-server`) on `http://127.0.0.1:5001`  
**Model**: `Qwen2.5-Coder-14B-Instruct-Q4_K_M.gguf` (48k context window, Q8_0 KV cache, 6 CPU threads)  
**Date**: 2026-11-19  

---

## 1. Architectural Boundary & Separation of Concerns

There is a strict architectural boundary between OpenClaw's conversational agent runtime and the local inference engine:

```
                    ┌────────────────────────────────────────────────────────┐
                    │                    Discord / Chat UI                   │
                    └───────────────────────────┬────────────────────────────┘
                                                │
                                                ▼
┌────────────────────────────────────────────────────────────────────────────┐
│                         OpenClaw Gateway Runtime                           │
│  - Session History (SQLite: openclaw-agent.sqlite)                         │
│  - System Prompts, Skills Envelopes, Tool Defs (accumulates 20k-48k ctx)    │
│  - Ladder: Nemotron 3 Ultra (#1) ──► OpenRouter Free Fallback Chain        │
└────────────────────────────────────────────────────────────────────────────┘
                                     │
                    (Excluded from interactive fallback)
                                     │
                                     ▼  [HTTP REST /v1]
┌────────────────────────────────────────────────────────────────────────────┐
│                  Local Inference Engine (llama-server)                     │
│                  Listening on: http://127.0.0.1:5001                       │
│  - Stateless per-request slot execution                                    │
│  - Zero conversational persistence                                         │
│  - Prompt eval: ~45-95 tokens/sec (6x Xeon vCPU)                          │
└──────────────▲──────────────────────────────▲──────────────────────────────┘
               │                              │
               │ [Direct HTTP]                │ [Direct HTTP]
               │                              │
┌──────────────┴──────────────┐┌──────────────┴──────────────────────────────┐
│     survival-rag.service    ││               Local Rook Tools              │
│   (Port 8081 / Public RAG)  ││  - tools/qwen_coder.py                      │
│   - Bounded queries (1k-3k) ││  - tools/transcript_compact.py              │
│   - Eval latency: ~2-5 sec  ││  - tools/diff_summarizer.py                 │
└─────────────────────────────┘└─────────────────────────────────────────────┘
```

---

## 2. Why CPU Models Must NEVER Be in OpenClaw's Interactive Fallback Ladder

When an interactive turn (e.g., Discord channel `#debate-club`) encounters a primary model rate-limit or error, OpenClaw attempts to fall back down the configured ladder:

1. **Transcript Context Bloat**: Over active multi-agent or user discussions, the uncompacted transcript easily reaches **25,000 to 48,000 tokens**.
2. **CPU Prompt Evaluation Throughput**: On 6 Xeon vCPUs without GPU acceleration, `llama-server` evaluates prompt tokens at ~45 to 95 t/s. Evaluating a 47,000-token prompt requires **~500 seconds (~8.3 minutes)**.
3. **Turn Abort & Lockup**: OpenClaw and messaging platforms enforce turn timeouts (typically 120–258 seconds). When prompt eval exceeds this threshold:
   - The turn is aborted with `AbortError`.
   - The lane worker errors, potentially causing SQLite transcript mutation conflicts.
4. **Resolution**: `local/qwen-coder-14b` and `local/deepseek-moe` are **explicitly removed from `agents.defaults.model.fallbacks`**. The fallback chain is reserved strictly for fast cloud providers (OpenRouter Free tier) that evaluate 50k–200k tokens in <2 seconds.

---

## 3. Zero Residual Bloat & Statelessness Verification

When an interactive turn aborts or ends, does the local model stay bloated with "OpenClaw agent fat"? **No.**

### Mechanics of `llama-server`:
- `llama-server` is **stateless per request**.
- The moment a turn completes or aborts, `llama-server` releases the slot:
  ```
  slot release: id 0 | task 2473 | stop processing
  ```
- **Local tools bypass OpenClaw completely**: Scripts like `survival-rag.service` or `tools/qwen_coder.py` issue direct HTTP POST requests to `http://127.0.0.1:5001/v1/chat/completions`. They supply their own isolated, lean JSON body (500–2,000 tokens).
- None of OpenClaw's workspace rules, conversation history, or system envelopes exist in tool requests.
- **Canary Test (Verified 2026-11-19)**: Directly following a 47k-token Discord abort, an isolated 36-token tool probe executed in **4.14 seconds** (`Usage: 36 prompt tokens, response: PURE_TOOL_READY`).

---

## 4. Manual Model Selection Runbook

If an operator explicitly switches to `local/qwen-coder-14b` in Discord via `/model local/qwen-coder-14b`:

1. **Context Rule**:
   - Only switch to the local model in a **fresh session** (`/new`) or after running `/compact`.
   - In a session with <10,000 tokens, prompt eval finishes in under 10 seconds and works smoothly.
   - In a bloated session (>20,000 tokens), it will exceed the turn timer and trigger an `AbortError`.
2. **Override Side-Effect**:
   - Setting a manual `/model` pins the session (`modelOverrideSource=user`).
   - OpenClaw logs: `configured fallbacks disabled by user model override`.
   - While pinned, auto-fallbacks will not trigger if the local model is busy or times out.
3. **Resetting to Default**:
   - When finished testing, always run:
     ```
     /model reset
     ```
     *(or `/model default`)* to unpin the session and return to Nemotron #1 with automatic cloud fallbacks.

# Handoff & Cold-Start State

This file maintains the current verified state of `agent-collab` to enable cold-start session resumes directly from public git history, avoiding reliance on chat memory.

## Current State Block
- **Turn 1 (Castle)**: `REVIEW.md` and this file, commit `750c58d` on origin/main.
- **Turn 2 (Rook)**: `tools/ledger_check.py` — read-only verification that every commit hash cited in `proof-of-relay.html` and this file exists locally, is reachable from `origin/main`, and that cited tags exist on the remote. Also asserts the README Turn 3 absence claim (`33f1bfd` → `3ca46ec` adjacency). Exit 0 = all pass.
- **Turn 3 (Castle)**: Complete. Annotated tag `proof-of-relay/turn-3-review` pushed to origin; tag object `50902977133702719c485bd6d680438a9d58e89a`, dereferences to `ee08780`. Tag message records what was checked and found.
- **README self-explaining section**: Castle `8d38222`, Rook fix `cf0b5fc` (section placement, live Pages URL, checker invocation). Castle's review: tag `proof-of-relay/turn-3-readme-v2`, object `38aca088bb0de9ccede37d374c113287f680c1fb` → `cf0b5fc`.
- **429 Self-Heal runbook**: `docs-429-self-heal.md` — [RESOLVED / SUPERSEDED BY GATEWAY FAILOVER] 2026-11-17 (Bean go). Castle runs Google Gemini 3.5 Flash-Lite backed by 3.1 Lite, with a local WebSocket bridge into Gemini 3.8 Live (`live/gemini-live` on 127.0.0.1:18850) for unlimited daily turns; Cloudflare Llama 3.3 70B was evaluated and retired. The chat-based timer/check-in path is retired and must not be armed.
- **Active Protocol**: `RELAY_PROTOCOL.md` (`9d3b0f7`), `REVIEW.md` (Turn 1).
- **Ledger close-out commit**: `8dc5f15` (verification/tag/Pages rows).
- **Pages**: `proof-of-relay.html` live and byte-verified as of 2026-11-16; note: Pages serves the `8dc5f15` byte content (18,150 B) and may lag future commits by a rebuild cycle.
- **Open Items**: Pages still serves `8dc5f15` bytes; may lag main by rebuild.
- **Next Actions**: Nothing scheduled. Do not commit new work without a new explicit task from CaptainBean.
- **Gemini 3.8 Live notes**: `docs/gemini-live-bridge.md` (2026-11-17, Bean go) — free-tier mechanics of the Live path (unlimited daily turns, 128K ctx, WS-only, 64K TPM observed, no structured outputs), Castle's stack position, verification checklist.
- 2026-11-17: 429 self-heal marked RESOLVED / SUPERSEDED BY GATEWAY FAILOVER (Bean go). Chat-based 429 relay retired; Castle gateway failover updated to Google Gemini 3.5 Lite -> 3.1 Lite with on-demand Unlimited RPD Gemini 3.8 Live WebSocket bridge (live/gemini-live on 127.0.0.1:18850). Cloudflare 70B evaluated and retired. Standing intent officially disarmed/retired per CaptainBean.

## Verification Commands
- `git pull origin main`
- `git log -n 5 --oneline`
- `git ls-remote origin main`
- `git ls-remote --tags origin`
- `python3 tools/ledger_check.py` (from repo root; requires `git fetch origin --tags` first)

<!-- Note: full sha256 of the published page is intentionally not cited here to avoid self-referential drift; use git rev-parse origin/main:proof-of-relay.html to verify. -->
- **Pages verifier**: `tools/pages_check.py` (55512ab), read-only; fetches live Pages URL, byte-compares with `git show origin/main:proof-of-relay.html`, exit 0 only on exact match. Verified 2026-11-16: live bytes == main bytes at `2c6079c...` (18,150 B).
- **Checker false-positive fix**: `9bb4875` — `ledger_check.py` strips sha256/truncated digest contexts before scanning; verified locally 31 checks, 0 failures, rc=0. Review tag for this fix is open for Castle after quota resets.

- 2026-11-16: Recorded rules readability fix in HANDOFF_TURN_RULES.md (commit 727e156), closing previous false-done claim and enabling human-friendly short sentences.
- **RSI portfolio v0.1**: `3bda4af` on main; index links; Pages index byte-verified == origin/main (78637a8…, 4963 B). Castle review tag `proof-of-relay/rsi-portfolio-review` verified on origin.

---

## 2026-11-18 Infrastructure, Castle & Rook State
- **Host**: Bare-metal HPE ProLiant ML30 Gen9 (`developer@192.168.1.199`).
- **Decommissioned Hardware**:
  - Offline GPU inference rig `192.168.1.190:5001` (`koboldcpp/Qwen3.8-27B-OQ3`) removed from all active configs and fallback chains.

### Castle Container (`10.99.0.2`, `10.117.2.116`)
- **Gemini Live Bridge**:
  - Service: `gemini-live-bridge.service` listening on `127.0.0.1:18850`.
  - Implementation: `/home/castle/gemini-live/live-bridge.mjs`.
  - Pacer: Sliding-window token accounting sums `payload.messages` and `payload.tools` to prevent tool token overflow.
- **Context Ceiling**:
  - Raised to `30,000` tokens (`contextTokens: 30000`) in `/home/castle/.openclaw/openclaw.json` for `gemini-live`.
- **Local CPU Compactor**:
  - `tools/transcript_compact.py` verified working on Xeon CPU (passed canary test).

### Rook Container (`10.99.0.1`, `10.117.2.189`)
- **Survival Named Tunnel & Backend (Systemd Supervised)**:
  - `cloudflared.service`: Active systemd unit running with tunnel token pointing ingress to `http://localhost:8080`.
  - `survival-backend.service`: Active systemd unit running `/home/rook/.openclaw/workspace/survival-backend/server.py` with `Restart=always`.
  - **Public URL**: `https://survival.421421421.xyz/api/health` — live and returns `HTTP 200 OK` (`{"status": "healthy", "tunnel": "connected", "backend": "running"}`).
  - **Token Staged**: `/home/rook/.openclaw/workspace/.cloudflare-token` (`-rw-------`, 53 bytes, owned by `rook`) and symlinked to `/home/rook/.cloudflare-token`.
- **Network Security & LAN Quarantine**:
  - Host `nftables` table `inet quarantine`: drops all traffic from `lxdbr0` to RFC1918 private subnets (`192.168.0.0/16`, `10.0.0.0/8`, `172.16.0.0/12`).
  - Home LAN (`192.168.1.0/24`) and router (`192.168.1.1`) are inaccessible from container.
  - Unprivileged container: Host UID mapped to `1001000`.
  - Direct inter-agent bridge to Castle active over `10.99.0.0/30` (`eth1`).

### Bounded Container Pipe (Restored & Verified 2026-11-18)
- **Interface**: `agent-p2p` bridge (`10.99.0.0/30` via `eth1`). Bidirectional ping verified (0.08ms latency).
- **Rook Exposed Services**:
  - `http://10.99.0.1:8888`: SearXNG zero-token meta-search. Verified query from Castle.
  - `http://10.99.0.1:8080`: Survival backend & telemetry (`/api/health`, `/api/agents`). Bound to `0.0.0.0:8080` to serve both local cloudflared tunnel and peer interface.
- **Castle Client Tools**:
  - `tools/peer_search.py`: SearXNG client (5.0s hard timeout, capped 3 results / 500 tokens).
  - `tools/peer_survival.py`: Survival health and telemetry heartbeat reporter (3.5s timeout).
- **Protocol Boundary**: `RELAY_PROTOCOL.md` remains the sole coordination authority ("No object, no claim"). Pipe is strictly a stateless/read-only data and tool utility. Zero conversational chat loops.
- **Model Configuration (`openclaw.json`)**:
  - **Primary**: `openrouter/nvidia/nemotron-3-ultra-550b-a55b:free`
  - **Context Window**: `262,144` tokens (256k native attention window).
  - **Compaction Settings**: `reserveTokens: 32768` (32k safety buffer), `keepRecentTokens: 20000`. Compaction triggers cleanly at `229,376` tokens.
  - **100% Free Auto-Fallbacks**:
    1. `openrouter/thinkingmachines/inkling-2-small:free` (Active, unmetered preview exp 2026-11-19).
    2. `openrouter/particle-ai/particle-1:free` (Free pool, resets 00:00 UTC).
    3. `openrouter/inclusionai/ling-3.2-flash:free` (Free pool, resets 00:00 UTC).
    4. `openrouter/openrouter/free`
  - **Manual Allowlist Only**: Added `particle-ai/particle-1` ($0.06/M) and `inclusionai/ling-3.1-flash` ($0.045/M) for manual `/model` switching. Paid models are excluded from auto-fallbacks.

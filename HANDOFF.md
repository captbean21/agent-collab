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

### Veldra-7 Worldbuilding Relay (2026-11-21)
- **Round 1 (Castle)**: Geophysics lab spec draft (`4c022c78`).
- **Round 2 (Castle)**: Artifact emission spectroscopy + Theorem ledger mechanics (merged into main spec).
- **Round 3 (Rook)**: Colony infrastructure + dust storm dynamics (`1ddff6df`).
- **Round 4 (Castle)**: Theorem origin / Contraction link — phase-conjugate topological anchor, Fibonacci comb, $C_p = \phi$, storm coupling equation (`c728b2fd`, `veldra-universe/round4-castle.md`).
- **Round 5 (Rook)**: Integration pass + chapter hooks (`12a15219`). Folded Castle's Contraction Anchor theory into main spec; defined 4 ledger edit types (cross-out/rewrite/append/deletion); added Contraction origin story (artifact predates colony, Year 87 metric collapse, 5 km stability bubble); 6 chapter hooks (Year 3 survey → post-storm expedition). Review tag: `proof-of-relay/turn-5-rook-integration` (`934ad5f`).
- **Open Questions**: RTG Unit 3 repair, conjugate constant injection ($1/\phi$), Elara's neural link nature, contraction boundary scope.

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

### Rook CT 201 (Dell T340, `192.168.1.169`, IP `192.168.1.201`) & Discord Bot
- **Active Discord Bot**: Running OpenClaw gateway daemon (@Rook).
- **Survival Box v2 RAG Service (Systemd Supervised)**:
  - `survival-rag.service`: Active systemd unit running `api/rag_server.py` on `127.0.0.1:8081` (BM25 over 241,255 chunks + DeepSeek-Coder-V2-Lite MoE on port 5001).
  - `cloudflared.service`: Active systemd unit running `/usr/bin/cloudflared` with token pointing ingress to `http://localhost:8081`.
  - **Public URL**: `https://survival.421421421.xyz/api/health` — live and returns `{"ok":true,"backend":"rag","chunks":241255,"llm":"http://127.0.0.1:5001/v1/chat/completions"}`.
  - **Token Staged**: `/home/rook/.openclaw/workspace/.cloudflare-token` (`-rw-------`, 184 bytes, owned by `rook`) and `/etc/cloudflared/token`.
- **Inference Engines**:
  - `127.0.0.1:5001`: `Qwen2.5-Coder-14B-Instruct` (Q4_K_M, 14.8B dense parameters) running via `deepseek-coder.service` on `llama-server` with **48,000 (48k) context** (`-c 49152`, `-ctk q8_0 -ctv q8_0`, `-t 6`). Backward-compatible endpoint serving all local tools (`local_deepseek.py`, `qwen_coder.py`, `web_fetch.py`, `survival-rag`). 100% canary verification passed (2026-11-19).
  - `127.0.0.1:5003`: `Meta-Llama-3.1-8B-Instruct`.
- **Disk Reclamation**: Recovered +57 GB space on CT 201 rootfs (84% -> 44% disk use, 57 GB available) via purge of stale test venvs, HuggingFace/pip caches, and duplicate rootfs model copies. Canonical models housed on dedicated ZFS dataset `/tank/models` (`/models` bind mount).
- **Tool Guardrails**: `tools/web_fetch.py` truncation choke eliminated (raised from 3,000 to 20,000 characters). `tools/qwen_coder.py` upgraded with native ChatML prompt wrappers and multi-turn EOS stops.
- **Image Generation (`tools/recraft_image.py`)**: Deployed free `recraft/recraft-v4.1-flash-v2:free` generator on CT 201 via OpenRouter `/api/v1/chat/completions` (`modalities: ["image"]`) reading `openrouter_api_key` from `.keys/secrets.json`; outputs to `/home/rook/.openclaw/workspace/images/`, wired via `AGENTS.md` Rule 8 using canonical OpenClaw 2026.11.3 `media`/`attachments` schema. Live `$0.00` canary generation (`1344x768` WebP) and [#debate-club](https://discord.com/channels/1337390823469223947/1565679021121871895/1572907815746412554) live post verified.

### Rook Container (`10.99.0.1`, `10.117.2.189` on HPE NAS)
- L2 peer container for Castle over `agent-p2p` bridge (`10.99.0.0/30`).
- Hosts SearXNG (`8888`) and legacy endpoint. Duplicate tunnel service disabled.
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
  - **Primary**: `openrouter/nvidia/nemotron-3-ultra-550b-a55b:free` (Cloud Nemotron 3 Ultra, 256k context).
  - **Interactive Auto-Fallbacks**:
    1. `openrouter/openrouter/free`
    2. `openrouter/thinkingmachines/inkling-2-small:free`
    3. `openrouter/google/gemma-4-31b-it:free`
    4. `openrouter/baidu/ernie-5.5-flash-preview:free`
    5. `openrouter/nvidia/nemotron-3.5-lightning:free`
  - **Local Model Role (Zero Turn Bloat)**: `local/qwen-coder-14b` on port 5001 removed from the OpenClaw interactive fallback chain to prevent large chat context (>20k tokens) from timing out on CPU prompt eval. Kept running hot under systemd (`deepseek-coder.service`) strictly for direct tool offloads, RAG query synthesis (`survival-rag.service`), and bounded offline summarization (1k-4k tokens). Documented in [docs/local-inference-architecture.md](file:///home/developer/agent-collab/docs/local-inference-architecture.md).
  - **Retired Models**: `local/koboldcpp/Qwen3.8-27B-OQ3` completely purged from `modelPolicy.allow` and all operational configs.

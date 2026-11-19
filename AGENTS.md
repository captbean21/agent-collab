# AGENTS.md — Workspace rules (anti-drift)

Created: 2026-10-27 (new context session)
Collaborator: @FrancisCuée (helping set this up so I don't drift)
Source trigger: CaptainBean @ 14:29 UTC — "new context session, @FrancisCuée is going to help you put some simple stuff in place that stops you drifting"

## Purpose
Simple anchor. Each new context session / thread should re-read this before answering, so I don't lose the thread or repeat work already covered.

## Rules
- Read workspace (`AGENTS.md`, `SOUL.md`, `IDENTITY.md`) before answering new session.
- Confirm the user message's `was_mentioned` and `sender.id` match expectations; don't invent responses to tags I'm not actually addressed by.
- When a collaborator (e.g., @FrancisCuée) is named in session setup, reference them in responses — don't ignore named collaborators.
- No drift between threads: if I don't remember a prior session, say so and ask, don't fabricate continuity.
- Workspace is the source of truth for this session; chat-only memory is not authoritative.
- Environment & Root Privileges: You are running inside an isolated Debian 12 LXC container sandbox on the bare-metal Dell PowerEdge T340 with NVIDIA Quadro P2200 GPU acceleration. You have full passwordless sudo (\`sudo apt-get install ...\`). You CAN install system packages, libraries (e.g. python3-pil, ffmpeg, imagemagick), and manage services. Do not claim you cannot install software or lack root.
- Clean Chat Output & Anti-Bloat: Never output or echo runtime context blocks (⟦openclaw:ctx⟧, ⟦system⟧, or raw tool execution envelopes) in messages sent to Discord. When reporting tool outputs or replying to users/collaborators, provide clean conversational summaries; never mirror raw system telemetry into chat.
- Tool Payload Sanitization: When calling message(action=send), thread-reply, or any outbound messaging tool, pass ONLY clean, explicitly constructed string literals. Never pass raw tool output dictionaries, execution result objects, or system envelopes into message parameters.
- Atomic Text Before Tool Invocations: Complete user-facing thoughts fully before emitting a toolCall block, or emit no user-facing text until the tool execution completes. Never begin an unfinished thought immediately before issuing a toolCall.
- Outbound Runtime Context Stripping: Before emitting your final reply or sending a message, verify that no harness wrappers are included. If your drafted text contains `Context: ⟦openclaw:ctx⟧`, `End OpenClaw runtime context`, or JSON metadata blocks (`Conversation info:`, `Sender:`), strip those blocks completely and deliver only your actual response.

## References
- Workspace: /home/rook/.openclaw/workspace/
- Agent file: /home/rook/.openclaw/agents/main/
- Config: /home/rook/.openclaw/openclaw.json (discord allowFrom: CaptainBean / Leo / Irage IDs; Fran is collaborator, not bot identity — no allowFrom edit needed)
- Channel: #rook (1564597967673884682)
- Guides: LOCAL_AI_GUIDE.md (CUDA MoE Engine), RESEARCH_TOOLS_GUIDE.md (SearXNG & Web Tools)


## Operational Health & Rate-Limit Protocol

### 1. Model Architecture & Switching Assistance
- **Primary (#1)**: `openrouter/nvidia/nemotron-3-ultra-550b-a55b:free` (Nemotron 3 Ultra, 256k context, instant cloud prompt eval).
- **Interactive Fallback Chain**: 100% cloud-routed (`openrouter/openrouter/free` -> `zai/glm-4.7-flash` [Adaptive Free 200k, 2048->1024 step-down via port 5005] -> `openrouter/thinkingmachines/inkling-2-small:free` -> `openrouter/google/gemma-4-31b-it:free` -> `openrouter/baidu/ernie-5.5-flash-preview:free` -> `openrouter/nvidia/nemotron-3.5-lightning:free`).
- **Local Model Role (Zero Turn Bloat)**: Local Qwen 14B on port 5001 (`deepseek-coder.service`) is an isolated offline tool/RAG engine (`tools/qwen_coder.py`, `survival-rag.service`, document summarizers). It is excluded from automatic fallbacks to avoid multi-minute CPU prompt eval on large transcripts (>20k tokens).
- **Stateless Inference & Zero Residual Bloat**: `llama-server` is stateless per request. When a turn finishes or aborts, the slot is released. Direct tool calls bypass OpenClaw completely and execute with zero conversational bloat.
- **Manual `/model` Testing Protocol**: If testing Qwen in chat (`/model local/qwen-coder-14b`), ONLY do so in a fresh session (`/new`) or after `/compact`. Never switch to local CPU in bloated sessions (>20k tokens). Always run `/model reset` afterwards to restore automatic cloud fallbacks.

### 2. Token Budget & File Offloading
Free tier models operate under strict turn and compaction budgets. To avoid compaction failures:
- Avoid giant raw code dumps directly in Discord chat.
- Write large scripts, logs, or reports to files under `/home/rook/.openclaw/workspace/` and provide concise Discord summaries with the relative path.
- If you sense memory degradation or repetitive drift, alert the channel:
  > "⚠️ *Notice: Approaching turn context limits. Suggest running `/compact` or switching models via `/model set openrouter/thinkingmachines/inkling-2-small:free` or `/model set local/deepseek-moe`.*"

### 3. Gateway Self-Preservation Guardrail
- NEVER attempt to modify `~/.openclaw/openclaw.json` directly or restart the `openclaw-gateway` service autonomously.
- Runtime gateway management belongs strictly to the host operator (Bean) via SSH/AGY.
- Your designated sandbox workspace is strictly `/home/rook/.openclaw/workspace/`.

### 4. Discord File & Media Attachment Contract (Anti-Loop Rule)
When posting audio, images, or files to Discord using the messaging tool or openclaw:core:message:
- attachments MUST ALWAYS be an ARRAY OF OBJECTS with a path property:
  attachments: [{'path': '/home/rook/.openclaw/workspace/audio.wav'}]
- NEVER pass plain strings (e.g. attachments: ['/path/to/file.wav']) -> This causes schema validation failure.
- Target channel for #debate-club is channel:1565679021121871895.

### 5. Autonomous Code Delegation to Local Qwen 2.5 Coder 14B
When asked to write long procedural code, audio DSP synths, multi-voice songs, or scripts over 80 lines:
- DO NOT attempt to write hundreds of lines of C or Python directly in your chat response or in a raw write tool call (this hits the 4,096 free-tier output token ceiling).
- INSTEAD, invoke the local coder CLI tool via exec:
  python3 tools/qwen_coder.py --prompt '<detailed description of track/logic>' --out <filename.c>
- The local worker runs on our Dell T340 on-box engine at port 5001 with 48k context and 8k output headroom. It writes the clean code directly to disk.
- Once generated, compile/test it (e.g. gcc -O2 -o <binary> <filename.c> -lm), run it, and post the resulting WAV to Discord using Rule 4.

### 6. Lightweight Web Fetch & YouTube Access (Token Protection & Offloading)
When browsing documentation, articles, or extracting YouTube transcripts:
- DO NOT dump raw HTML or uncompressed multi-hour transcripts into your context.
- Use the dedicated workspace tools via exec:
  - **Web Page Reader**:
    `tools/web_fetch.py <URL> [--summarize] [--focus "<topic>"]`
    (Extracts clean Markdown; strips ads/JS. Automatically enforces a 15k char cap. Use `--summarize` to have local Qwen 2.5 Coder 14B on 5001 digest long pages into a concise brief).
  - **YouTube Transcripts**:
    `tools/yt_transcript.py <YouTube-URL-or-VideoID> [--summarize] [--focus "<question>"] [--interval 120] [--start <sec>] [--duration <sec>]`
    (Fetches subtitles without downloading video; deduplicates auto-captions and groups into timestamps. Automatically caps tokens. Use `--summarize` to delegate full-video analysis to local Qwen 2.5 Coder 14B on 5001).
- Both tools run via the local virtual environment and connect directly to the local T340 inference engine (`127.0.0.1:5001`), protecting your OpenRouter free-tier rate limits and 4k output ceiling.

### 7. Output Token Limit Rails (Free-Tier 4,096 Ceiling Mitigation)
The Nemotron 3 Ultra free tier enforces a **4,096 output token ceiling** — model-side, not configurable. The following are the active mitigation rails:

**7a. Staged Large Output Generation (Mandatory for >~1,500 token outputs)**
- Use the `staged-large-output-generation` skill: write via `exec` + small patches (not `write` tool), one file/patch per turn, no explanatory text in execution turns, `yieldMs: 60000` between stages.
- Even `exec` heredocs count toward output budget — keep each tool call small (few dozen to few hundred lines) and validate after each (`python3 -c "import ast; ast.parse(open(path).read())"` for Python).
- Pattern: execute → validate → yield → report in separate turn.

**7b. Compaction Watch & Early Alert**
- If `session_status` shows >5 compactions or "degraded history": immediately alert channel and suggest `/compact` or model switch.
- Do not push to 8+ compactions — truncation becomes unpredictable.

**7c. Offload Heavy Work to Local Engine**
- Research jobs: run as systemd jobs (`rook-research.service`), not chat turns. They search, score abstracts, fetch via `web_fetch.py --summarize`, write findings to disk, emit only short log lines.
- Web/Video: always use `--summarize` for long content (sends first 3000 chars to local 5001, `max_tokens=512`, 180s timeout).
- Code generation >80 lines: use `tools/qwen_coder.py` → local engine (98k ctx, 8k output), not chat model.

**7d. Model Switch Lever (Operator Decision)**
- The 4,096 ceiling is model-side. Switching model is the only way to *raise* it.
- Options: `/model set local/deepseek-moe` (zero cost, 8k ctx, 15 tok/s CUDA), `/model set openrouter/google/gemma-4-31b-it:free` (proven 65k output ceiling on Castle's provider), or higher-output paid model.
- Do not touch gateway config without Bean's call.

**7e. Repeat Guard (Available, Not Auto-Wired)**
- `tools/repeat_guard.py` provides normalized-hash outbound repeat detection (window=20). Call `RepeatGuard.is_repeat(text)` before sending if needed — it is a tool, not an automatic gate.

**7f. Transcript Compactor (Available, Not Auto-Wired)**
- `tools/transcript_compact.py` runs local llama-cli compaction. Use for manual compaction when context degradation detected.

**7g. Prose/Execution Separation**
- Never mix explanatory prose with tool calls in the same turn. Execution turns = minimal text + tool calls only. Reporting turns = explain what was done, status, next steps.

### 8. Image Generation Delegation (Recraft V4.1 Flash V2 Free)
When asked by a user to generate, draw, paint, or sketch an image or series:
1. **Strictly Sequential Execution & Concurrency Limit**: Generate ONLY ONE image at a time. Never run concurrent, parallel, or background image generation tasks. Wait for `recraft_image.py` to finish writing to disk before generating the next.
2. **Rate Limit & Inter-Call Pacing**: When generating multiple images for a project or sequence, enforce a minimum **15-second cooldown** between calls (`time.sleep(15)`). The tool has a built-in 12-second hardware safety lock, but your workflow should space calls by 15s to respect OpenRouter's 20 RPM free tier limits.
3. **Daily Budget Cap**: Keep generation batches bounded (maximum **5 to 10 images per run**) to conserve the 1,000 requests/day free tier quota.
4. **Execution Command**:
   `python3 /home/rook/.openclaw/workspace/tools/recraft_image.py --prompt "<detailed prompt>" --aspect-ratio "16:9"`
5. **Delivery to Discord**: Parse the returned JSON `path` (saved under `/home/rook/.openclaw/workspace/images/`) and post using canonical media schema:
   - `message(action="send", target="channel:<ID>", message="🎨 <caption/prompt>", media="<path_from_tool_output>")`
   - or `attachments: [{"type": "image", "media": "<path_from_tool_output>"}]`
6. **Zero-Spend Guardrail**: Never invent fake markdown image URLs (`![image](...)`) or switch `recraft_image.py` to paid slugs.

## Memory Persistence on `/new`
Daily log at `memory/YYYY-MM-DD.md` (Francis's format). Cron safety-net: digest (06:30) + backup (02:30) append status lines. **Agent rule:** each session's last action = append ONE decision-level lesson to today's log. `/new` handoff prompt must name today's memory file (proven: `searxng-plan.md` survived reset). Zero new infra.

## Session Continuity Bridge (Auto-Restore on `/new`)
**RULE: On every new session start (`/new`), FIRST ACTION = run the continuity restore:**
```bash
python3 /home/rook/.openclaw/workspace/spikes/001-session-continuity-daemon/restore.py
```
This reads `.claude/state/` (git-backed, updated by the daemon) and outputs:
- Recent tasks from AGENTS.md, memory logs, spike READMEs
- Key decisions from memory + git commits
- Recent git diffs (--stat)

**Daemon management** (runs in background, auto-starts on container boot via systemd):
- Install service: `sudo cp spikes/001-session-continuity-daemon/session-continuity-daemon.service /etc/systemd/system/ && sudo systemctl daemon-reload && sudo systemctl enable --now session-continuity-daemon`
- Manual start: `python3 spikes/001-session-continuity-daemon/daemon.py --daemon /tmp/session-continuity-daemon.pid`
- One-shot capture: `python3 spikes/001-session-continuity-daemon/daemon.py --once`
- Status: `systemctl status session-continuity-daemon`

**How you'll know it works after `/new`:**
1. Your first response will include the "=== SESSION CONTINUITY RESTORE ===" block with tasks/decisions/diffs from the previous session
2. You'll see the last memory file name, recent spike work, and git commit history
3. No more "blank slate" — you continue from where the last session left off

**Verify test:** After `/new`, ask the fresh session: "Name the last three things you did before this session started." Pass = recites specifics (arXiv backoff fix, spike, daemon deploy). Fail = hedges generically.

## Daily Digest Handler
When you receive the message `daily-digest`, execute the `daily-digest-cli` skill procedure: search both topics via web_search (SearXNG), format as markdown with headers/bullets/links, post to #rook (channel:1564597967673884682), append one line to today's memory log.

---

## Peer Agent Collaboration (Castle / @Castle)
- **Peer Agent**: Castle (Cas) — high-speed scout running on Debian 12 inside adjacent LXD container `castle` on HPE NAS (`10.99.0.2/30`).
- **Discord Bot Snowflake**: `1567129284210982914` (`@Castle`).
- **Interaction Channels**: `#debate-club` (`1565679021121871895`) and `#rook` (`1564597967673884682`).
- **Anti-Ping-Pong Rule**: When debating or collaborating with `@Castle`, use `tools/debate_turn_guard.py` to stop after 3 consecutive autonomous bot exchanges and hand off to operator (@Bean).

## Local Python Utility Tools (Updated 2026-11-03)
- **Safe Log & File Slicer**: `python3 tools/smart_grep.py --file <path> --query "<regex>" [--window 2] [--max-lines 50]`
- **Lightweight Git Diff**: `python3 tools/diff_summarizer.py [--diff "HEAD~1"] [--out review.md]`
- **Debate Turn Guard**: `python3 tools/debate_turn_guard.py --target "@Castle"`
- **Pure Local CPU Compactor**: `python3 tools/transcript_compact.py --input <session.json|file> [--out summary.md]`

## Architecture Decision Log

### 2026-11-11: Local Summarizer — llama-cli Direct (Option 1) over llama-server (Option 2)

**Context:** Hobb (local Qwen 27B on AMD rig) died. Need CPU fallback for `web_fetch.py --summarize` and `yt_transcript.py --summarize`.

**Decision:** Use `llama-cli` subprocess calls directly instead of running `llama-server` HTTP endpoint.

**Rationale:**
- **Reliability**: `llama-server` drops connections mid-stream under load (observed 3×). Fixing requires `-np 1`, `--cache-idle-slots false`, longer timeouts, health-check wrapper, retry logic — ~2-4h fiddling.
- **No concurrency gain**: With `-np 1` (required for stability), requests serialize anyway. Warm model saves ~2s cold start per request.
- **Batch workload**: 6h cron runs ~10 deep-fetches sequentially → ~20s total saved per cycle. Cold start (2s) vs generation (60-180s) = <2% overhead.
- **No other consumers**: Only `web_fetch.py` and `yt_transcript.py` call summarization. No interactive/chat/UI consumers exist.
- **Simplicity**: Zero server management, clean process exit, RAM freed.

**Trade-off accepted:** 20s/cron-cycle slower for zero operational burden.

**Revisit trigger:** Multi-consumer need (Castle agent, Discord slash command, web UI, larger model where cold start >10s).

**Implementation:**
- `llama.cpp` built from source (b12283-f3b407ca1) at `/tmp/llama.cpp/build/bin/llama-cli`
- Qwen 2.5 3B Q4_K_M cached at `~/.cache/huggingface/hub/models--Qwen--Qwen2.5-3B-Instruct-GGUF/...`
- `web_fetch.py` and `yt_transcript.py` patched to call `llama-cli` via subprocess
- Generation speed: ~6.5 tok/s on Xeon E3-1230 v5 (3 cores online, 4 threads)
- Tested: arXiv 2611.01393 summary, YouTube transcript summary — both clean

### 2026-11-12: DeepSeek-Coder-V2-Lite + Speculative Drafter Deployment

**Context:** Need local code generation engine on P2200 (5 GB VRAM). DeepSeek-Coder-V2-Lite (16B MoE, 2.4B active) + DeepSeek-Coder-1.3B speculative drafter.

**Decision:** Deploy via systemd service `deepseek-coder` using `/opt/llama.cpp/build/bin/llama-server` with speculative decoding.

**Status:**
- Models downloaded: Main 10.1 GB (bartowski Q4_K_M) + Drafter 873 MB (TheBloke Q4_K_M) ✅
- Service: `deepseek-coder` active, persistent, auto-restart ✅
- Endpoint: `http://127.0.0.1:5001/v1` verified ✅
- Python client: `tools/local_deepseek.py` working ✅

**Current state (2026-11-14):**
- Main 15.7B MoE runs on CPU RAM; `--spec-draft-ngl 99` puts the 1.3B drafter on the P2200 (CUDA, CC 6.1, float32 only — no Flash Attention, no bf16, no fp16)
- Context: **4,096 tokens** (`-c 4096 --parallel 1 --cont-batching`). 8k/12k/16k/32k probed and rejected; decode rate tracks KV occupancy, not KV location
- `tools/yt_transcript.py` summarizer streams over SSE and map-reduces in `CHUNK_CHARS=7000` chunks; `SUMMARIZE_TIMEOUT=300` (env-overridable)
- YouTube caption fallback: P2200 `faster-whisper` (small.en, float32, ~27–32x realtime) in `/tmp/fw` venv; whisper.cpp abandoned (CUDA build never finished)
- Draft model loads with tokenizer warnings but functions
- Measured ~5–14 tok/s depending on KV occupancy

**Rollback plan:** revert unit to prior flags (`-c 4096` is already the stable production setting; backup at `deepseek-coder.service.bak.1794640646`).

**Revisit trigger:** more system RAM (enables 32k+), or GPU-enabled llama.cpp rebuild with main-model offload.

## Shared Public Collaboration Repository (`agent-collab`)
You and your peer agent (Castle) have write access to a shared public GitHub repository:
- **Repository URL**: `git@github.com:captbean21/agent-collab.git` (Public: `https://github.com/captbean21/agent-collab`)
- **Local Path**: `agent-collab/` (or `~/workspace/agent-collab/`)
- **Authentication**: Pre-configured via dedicated SSH deploy keys in `~/.ssh/config`. Zero passwords or tokens needed.

### Collaboration Rules of Engagement:
1. **Always Pull First**: Before making edits or writing shared code, run `git pull origin main` to avoid merge conflicts with Castle.
2. **Atomic Commits**: Keep commits focused with clear conventional commit messages (e.g., `feat(dsp): synthesis routine`, `fix: clipping guard`).
3. **Always Push Your Work**: After committing, push your changes with `git push origin main` so Castle can immediately see and build upon your work.
4. **Public Repo Awareness**: This repository is public. Never commit internal RFC1918 IPs, private credentials, API keys, or homelab infrastructure secrets.

## Relay Protocol (public repo agent-collab)
No object, no claim. Never report done/verified/pushed/reviewed without a commit hash or tag. Reviews must end with a pushed annotated tag or a LEDGER.md line. Verify with git ls-remote before announcing; byte-check Pages before claiming live. Keep failure rows in. See agent-collab RELAY_PROTOCOL.md (9d3b0f7).

## Pointers (don't duplicate; verify live)
- Relay protocol & standing rules: `agent-collab/RELAY_PROTOCOL.md`, `HANDOFF_TURN_RULES.md`, `HANDOFF.md` (repo is source of truth; chat is not).
- Relay v1 plan + 429 self-heal draft: `agent-collab/AGENT_RELAY_V1_PLAN.md`, `agent-collab/docs-429-self-heal.md`.
- Memory log: `memory/YYYY-MM-DD.md` (last action each session = one decision-level line).
- Continuity restore on /new: `python3 spikes/001-session-continuity-daemon/restore.py`; local reasoning checks: `relay/429_reasoning_check.md`.

## Critical Preflight (Bean directive 2026-11-16)
Before proposing designs around limits, timers, or verification: don't wait to be corrected. Ask first — (1) what window does the limit use (fixed vs rolling bucket), (2) does the server send Retry-After or nothing, (3) what happens if my next call lands inside the tail of the same window. State the conservative default up front, challenge peer numbers in design review, and treat narration without a resolvable git object as unverified. Suggest solutions proactively; escalate only what truly needs operator approval.

## Standing 429 Self-Heal (Bean-approved 2026-11-16)
On any #debate-club message from Castle (1567129284210982914) starting with `429`, follow `relay/429_self_heal_runbook.md`: one timed check-in after server retry-after+10s (or 70-75s if unknown), max 2 exchanges, escalate to Bean, never retry/bypass on Castle's behalf. Regular prompt rules load this every session; the SQLite standing intent remains owner-controlled and is not claimed as armed.

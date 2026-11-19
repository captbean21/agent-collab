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

### 1. Model Switching Assistance
If you encounter tool execution loops, rate limits, truncation warnings, sluggish TTFT, or if a user requests a model change, suggest or remind the channel of the command to switch models instantly:
- `/model set openrouter/nvidia/nemotron-3-ultra-550b-a55b:free` (Primary: Deepest reasoning, 1M context)
- `/model set openrouter/openrouter/free` (Fallback 1: Rotating free tier safety net)
- `/model set zai/glm-4.7-flash` (Fallback 2: Zero-cost 200k context, adaptive 2048->1024 token step-down)
- `/model set openrouter/thinkingmachines/inkling-2-small:free` (Fallback 3: Rapid tool execution, 1M context)
- `/model set openrouter/google/gemma-4-31b-it:free` (Fallback 4: High quality tool calling, 262k context)
- `/model set openrouter/baidu/ernie-5.5-flash-preview:free` (Fallback 5: Deep research & flash attention, 1M context)
- `/model set openrouter/nvidia/nemotron-3.5-lightning:free` (Fallback 6: High throughput, 1M context)
- `/model set local/deepseek-moe` (On-box CUDA accelerated Sparse MoE on Quadro P2200, 8k context, zero token cost)

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

### 5. Autonomous Code Delegation to Local Qwen 27B
When asked to write long procedural code, audio DSP synths, multi-voice songs, or scripts over 80 lines:
- DO NOT attempt to write hundreds of lines of C or Python directly in your chat response or in a raw write tool call (this hits the 4,096 free-tier output token ceiling).
- INSTEAD, invoke the local coder CLI tool via exec:
  python3 tools/qwen_coder.py --prompt '<detailed description of track/logic>' --out <filename.c>
- The local worker runs on our AMD GPU rig at port 5001 with 98k context and 8k output headroom. It writes the clean code directly to disk.
- Once generated, compile/test it (e.g. gcc -O2 -o <binary> <filename.c> -lm), run it, and post the resulting WAV to Discord using Rule 4.

### 6. Lightweight Web Fetch & YouTube Access (Token Protection & Offloading)
When browsing documentation, articles, or extracting YouTube transcripts:
- DO NOT dump raw HTML or uncompressed multi-hour transcripts into your context.
- Use the dedicated workspace tools via exec:
  - **Web Page Reader**:
    `tools/web_fetch.py <URL> [--summarize] [--focus "<topic>"]`
    (Extracts clean Markdown; strips ads/JS. Automatically enforces a 15k char cap. Use `--summarize` to have local Qwen 27B digest long pages into a concise brief).
  - **YouTube Transcripts**:
    `tools/yt_transcript.py <YouTube-URL-or-VideoID> [--summarize] [--focus "<question>"] [--interval 120] [--start <sec>] [--duration <sec>]`
    (Fetches subtitles without downloading video; deduplicates auto-captions and groups into timestamps. Automatically caps tokens. Use `--summarize` to delegate full-video analysis to local Qwen 27B).
- Both tools run via the local virtual environment and connect directly to the AMD GPU inference rig (`192.168.1.190:5001`), protecting your OpenRouter free-tier rate limits and 4k output ceiling.

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

**Current limitations (llama.cpp build lacks GPU support):**
- Runs on CPU only (no `-ngl` offload)
- Context: 8192 tokens (requested 32768)
- Draft model loads with tokenizer warnings but functions
- Generation: ~16 tok/s on CPU

**Rollback plan:** If GPU build available later, tune `-ngl 35` main / `--spec-draft-ngl 99` drafter for P2200 VRAM.

**Revisit trigger:** GPU-enabled llama.cpp rebuild, or acceptance rate measurement <70% for speculative decoding.

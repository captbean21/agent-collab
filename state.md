---
project_id: 201
name: rook
status: ACTIVE
last_updated: 2026-11-20 22:20:00 UTC
local_path: /home/rook
architecture_version: 3.5.0
state_version: 3.5.0
---

# Rook Autonomous Sandbox Agent (State 201)

## Project Overview
Rook is an isolated, autonomous sandbox AI agent running OpenClaw inside a dedicated LXC container (`CT 201`) on the bare-metal Dell PowerEdge T340 (`192.168.1.169`). Migrated from the HPE NAS to unlock high-capacity local compute, Rook operates with full internal execution permissions while strictly quarantined from the local home network (RFC1918 egress blocked). He is equipped with an on-box AVX2-accelerated Sparse Mixture-of-Experts (MoE) inference engine (`DeepSeek-Coder-V2-Lite-Instruct`, 15.7B sparse MoE / 2.4B active) running at ~15 tokens/sec, backed by 24 GiB elastic RAM and a 100 GiB rootfs on enterprise SSD storage.

## Local Repository Structure
```text
/
├── home/rook/
│   ├── .openclaw/
│   │   ├── openclaw.json          # Agent & Discord configuration (local MoE + OpenRouter fallback)
│   │   ├── services/
│   │   │   ├── zai-proxy/         # Adaptive resilient reverse proxy for Z.ai GLM-4.7-Flash
│   │   │   │   └── adaptive_proxy.py
│   │   │   └── puter-bridge/      # Puter.js loopback bridge for Gemma 4 & GLM-5.2
│   │   │       └── puter_bridge.py
│   │   └── workspace/             # Unrestricted sandbox workspace for tools/tasks
│   │       ├── LOCAL_AI_GUIDE.md  # Instructions for Rook on calling local MoE engine
│   │       └── tools/             # Local DSP coder, web fetch, transcript tools
│   └── .config/systemd/user/
│       └── openclaw-gateway.service # Managed user daemon
├── models/                        # Bind mount of /tank/models (read-only)
│   └── DeepSeek-Coder-V2-Lite-Instruct-Q4_K_M.gguf (9.7 GiB)
└── /etc/systemd/system/
    ├── llama-local.service        # Managed systemd unit for local inference server (port 5001)
    ├── zai-adaptive-proxy.service # Systemd unit for Z.ai adaptive step-down proxy (port 5005)
    └── puter-bridge.service       # Systemd unit for Puter.js loopback bridge (port 5006)
```

## Architecture
- **Host Node**: Bare-Metal Dell PowerEdge T340 (`192.168.1.169`, CT 201).
- **Container Runtime**: Proxmox VE 9.2 LXC container provisioned on `tank-zfs` storage.
- **Storage Subsystem**: 100 GiB rootfs on Seagate Enterprise SSD (`tank-zfs:subvol-201-disk-0`).
- **Memory & Compute**: 4 vCPUs (Intel Xeon E-2126G up to 4.5 GHz, AVX2), 24 GiB elastic RAM (sips ~1.5 GB idle, expands to ~14 GB under full 32k context inference), 4 GiB swap.
- **Network Boundaries & Isolation**:
  - Outbound WAN: Full internet access (Discord API, OpenRouter endpoint, GitHub, web fetching).
  - LAN Quarantine: Egress traffic to RFC1918 private subnets (`192.168.0.0/16`, `10.0.0.0/8`, `172.16.0.0/12`) is strictly dropped by the Proxmox firewall (`/etc/pve/firewall/201.fw`). Zero access to Immich, family photo pools, TrueNAS backups, or router administration.
  - DNS Pinhole: Explicit UDP/TCP port 53 permitted to router `192.168.1.1` to enable public domain name resolution.
  - Ingress Access: Port 22 SSH allowed exclusively from AGY agent container (`192.168.1.178`).
- **GPU & Hardware Acceleration**:
  - GPU: Dedicated NVIDIA Quadro P2200 (Pascal GP106GL, 5 GiB GDDR5, Compute Capability 6.1, 75W TDP).
  - Driver & Kernel Subsystem: Proprietary driver `550.163.01` compiled and running against Proxmox VE 9.2 (Linux `7.0.2-6-pve`) using custom 3-point patches (`in_hardirq`, inline `vm_flags_set`/`vm_flags_clear`, `NV_CAN_CALL_VMA_START_WRITE 1`, headless exclude `nvidia-drm`).
  - Container Passthrough: Full device nodes (`/dev/nvidia0`, `/dev/nvidiactl`, `/dev/nvidia-modeset`, `/dev/nvidia-uvm`, `/dev/nvidia-uvm-tools`) mapped with permissions 0666 and cgroup permissions (majors 195, 509, 510, 511).
  - Persistence Service: `nvidia-persistence-init.service` enabled on host (persistence mode ON, 4W idle / 22W compute).
- **Application Stack**:
  - OpenClaw 2026.11.3 gateway daemon running under non-root user `rook` with systemd linger enabled.
  - Local Inference Server: `llama-server` compiled with native CUDA support (`-DGGML_CUDA=ON -DCMAKE_CUDA_ARCHITECTURES=61`) running as `deepseek-coder.service` on `127.0.0.1:5001`.
  - Speculative Drafting & VRAM Allocation: Speculative draft model (`deepseek-coder-1.3b-instruct.Q4_K_M.gguf`, 834 MB) fully offloaded to VRAM (`--spec-draft-ngl 99`), with DeepSeek-Coder-V2-Lite transformer layers dynamically fitted (`--fit on`), allocating ~1.66 GB VRAM.
  - Local Search Engine: Native SearXNG (`uwsgi-app@searxng.service`) backed by `redis-server.service` on `127.0.0.1:8888`.
  - Tool execution mode: `unrestricted` inside container jail.
  - Discord bot integration with developer team permissions and in-chat model switching.
  - Working Context Buffer: 8,192 tokens local context window; up to 1,048,576 tokens via OpenRouter fallbacks; 200,000 tokens zero-cost via Z.ai GLM-4.7-Flash.
  - Adaptive Token Proxy: Lightweight systemd service `zai-adaptive-proxy.service` running on `127.0.0.1:5005` that handles session affinity (Alibaba Cloud WAF `acw_tc` cookie), disables thinking tokens, and implements a resilient 1-shot (2048) + 1 step-down (1024) backoff before cascading down the ladder.
- **Inference Model Ladder & Fallback Policy**:
  1. **Primary Cloud / Chat**: `openrouter/nvidia/nemotron-3-ultra-550b-a55b:free` (1M ctx, flagship reasoning)
  2. **Cloud Fallback 1**: `openrouter/openrouter/free` (131k ctx, automatic free provider router)
  3. **Cloud Fallback 2 (Zero-Cost Puter Bridge)**: `puter/gemma-4-31b-it` via `http://127.0.0.1:5006/v1` (262k ctx, verified agentic tool loop, $0.00 spend, 0 credit burn)
  4. **Cloud Fallback 3 (Zero-Cost Adaptive)**: `zai/glm-4.7-flash` via `http://127.0.0.1:5005/v1` (200k ctx, adaptive 2048 -> 1024 step-down, thinking disabled, $0.00 spend)
  5. **Cloud Fallback 4**: `openrouter/thinkingmachines/inkling-2-small:free` (1M ctx, rapid tool execution)
  6. **Cloud Fallback 5**: `openrouter/google/gemma-4-31b-it:free` (262k ctx, high quality tool calling)
  7. **Cloud Fallback 6**: `openrouter/baidu/ernie-5.5-flash-preview:free` (1M ctx, deep research & flash attention)
  8. **Cloud Fallback 7**: `openrouter/nvidia/nemotron-3.5-lightning:free` (1M ctx, high throughput)
  9. **On-Box Engine / Tool Offload**: `local/deepseek-moe` on `http://127.0.0.1:5001/v1` (15.7B Sparse MoE + 1.3B drafter, 8k context, 16.5 tok/s, zero token costs, dedicated DSP/C synthesis)
  - **Manual On-Demand Models**: `puter/glm-5.2` (1M context flagship reasoning), `puter/gemma-4-31b-it` accessible via in-chat `/model` command.

## Autonomous Worker Tools & Guardrails
- **Tool-Loop Guard & Rolling History**:
  - `tools.loopDetection.enabled: true` in `~/.openclaw/openclaw.json` monitors rolling tool calls and halts repetitive loop signatures immediately.
- **Turn Timeout Ceiling**:
  - `agents.defaults.timeoutSeconds: 900` (15-minute hard limit per turn) ensures long-running local MoE code and audio synthesis complete safely while capping runaway executions.
- **Subagent Spawning Bounds**:
  - `agents.defaults.subagents`: `maxSpawnDepth: 1`, `maxChildrenPerAgent: 2`, `runTimeoutSeconds: 900` prevents recursive fork-bombs.
- **Local Coder Tool**: `/home/rook/.openclaw/workspace/tools/qwen_coder.py`
  - Routes directly to local MoE engine (`http://127.0.0.1:5001/v1/completions` and `/v1/chat/completions`).
  - Generates clean DSP/C code with strict audio safety rails (phase wrapping, hard clipping, modulo ring buffers).
- **Lightweight Web Fetch & YouTube Transcript Tools**:
  - Summarization pipeline routed to local engine without consuming external tokens.
- **Discord Media Attachment Contract**:
  - Pinned in `AGENTS.md`: `attachments` MUST be an array of objects `[{"path": "/path/to/file.wav"}]` or canonical `message(media=...)`.
- **Zero-Cost Image Generation & Rate Guardrail**:
  - Tool: `/home/rook/.openclaw/workspace/tools/recraft_image.py` (uses OpenRouter `recraft/recraft-v4.1-flash-v2:free` at $0.00 spend).
  - Hardware Cooldown Lock: Built-in 12-second inter-call throttle via `/tmp/recraft_last_run.ts` to strictly prevent 429 burst rate limits on OpenRouter free tier (20 RPM).
  - Rule 8 in `AGENTS.md`: Strictly sequential execution (1 image at a time, 15s inter-call pacing, max batch size 5-10 images per run).

## Operator Runbook (Manual Controls)

### Quick Health & Service Checks
```bash
# Check CT 201 status from Dell T340 host
ssh root@192.168.1.169 "pct status 201"

# Check local inference server inside CT 201
ssh root@192.168.1.169 "pct exec 201 -- systemctl status deepseek-coder"
ssh root@192.168.1.169 "pct exec 201 -- curl -s http://127.0.0.1:5001/v1/models"

# Check Z.ai adaptive proxy inside CT 201
ssh root@192.168.1.169 "pct exec 201 -- systemctl status zai-adaptive-proxy"
ssh root@192.168.1.169 "pct exec 201 -- curl -s http://127.0.0.1:5005/v1/models"

# Check OpenClaw gateway status inside CT 201
ssh root@192.168.1.169 "pct exec 201 -- runuser -u rook -- env XDG_RUNTIME_DIR=/run/user/1000 systemctl --user status openclaw-gateway"

# Test local C code generation
ssh root@192.168.1.169 "pct exec 201 -- runuser -u rook -- /home/rook/.local/share/tool-env/bin/python3 /home/rook/.openclaw/workspace/tools/qwen_coder.py --prompt 'Write a highpass filter' --out /tmp/hp.c"
```

### Discord Bot Model Switching
```text
/model set openrouter/nvidia/nemotron-3-ultra-550b-a55b:free
/model set zai/glm-4.7-flash
/model set local/deepseek-moe
/model set openrouter/google/gemma-4-31b-it:free
```

## Latest Accepted Phases
- **Phase**: ROOK-P6 — Research Stack Stabilization, GPU Extraction Pipeline & Automation Timer
  - **Result**: PASS on 2026-11-12
  - **Summary**:
    - Purged duplicate `uwsgi-app@searxng.service` conflict; confirmed SearXNG stable on `uwsgi.service` (port 8888).
    - Rewrote `tools/web_fetch.py` and `tools/yt_transcript.py` summarization pipelines to call warm local GPU MoE engine on `http://127.0.0.1:5001/v1`. Verified real-time extraction + summary on P2200 (~5s execution).
    - Provisioned `rook-research.timer` and `rook-research.service` (every 6 hours: 00:04, 06:04, 12:04, 18:04 UTC) with logging to `logs/research-runner.log`.
    - Deployed `RESEARCH_TOOLS_GUIDE.md` in workspace and updated `AGENTS.md`.
- **Phase**: ROOK-P5 — NVIDIA Quadro P2200 GPU Passthrough & CUDA Accelerated Inference
  - **Result**: PASS on 2026-11-12
  - **Summary**:
    - Compiled and loaded proprietary NVIDIA 550.163.01 driver on Dell PowerEdge T340 host running Proxmox VE 9.2 (Linux 7.0.2-6-pve) via custom 3-point ABI patches (`in_hardirq`, `NV_CAN_CALL_VMA_START_WRITE 1`, `nv_dma_use_map_resource`, headless exclude `nvidia-drm`).
    - Configured persistence mode and enabled `nvidia-persistence-init.service` on host (4W idle / 22W compute, locked at 75W VBIOS limit).
    - Configured full `/dev/nvidia*` character node passthrough (0666) and cgroups (majors 195, 509, 510, 511) in `/etc/pve/lxc/201.conf`.
    - Installed matched user-space libraries (`libcuda1=550.163.01-1`, `libnvidia-ml1`, `nvidia-smi`) and validated smoke test kernel via `nvcc -arch=sm_61`.
    - Rebuilt `/opt/llama.cpp` inside CT 201 with `-DGGML_CUDA=ON -DCMAKE_CUDA_ARCHITECTURES=61`.
    - Configured `deepseek-coder.service` with `--fit on --spec-draft-ngl 99 -c 8192 --parallel 2`, offloading the 1.3B draft model 100% to VRAM and fitting 22 main transformer layers to GPU (~1.66 GB VRAM).
    - Verified local inference `/v1/chat/completions` executing active Compute kernels on CUDA0.
    - Updated Rook's workspace documentation (`LOCAL_AI_GUIDE.md`, `AGENTS.md`, `memory/2026-11-12.md`, and `state.md`).
- **Phase**: ROOK-P4 — OpenRouter Free Tier Fallback Resiliency & Loop Gate Hardening
  - **Result**: PASS on 2026-11-12
  - **Summary**:
    - Discovered root cause of 429 quota exhaustion (`free-models-per-day-high-balance`) from an autonomous loop in `#rook-cage` (5,478 audit events, 111k context).
    - Purged delisted 404 models (`inkling:free`, `xing4.0-29b-a4b:free`) from `openclaw.json`.
    - Added high-context active OpenRouter free models (`gemma-4-31b-it:free`, `inkling-2-small:free`, `nemotron-3.5-lightning:free`, `openrouter/free`).
    - Configured `tools.loopDetection.enabled: true` to prevent unthrottled repetitive tool looping.
    - Validated configuration, restarted user gateway daemon, and verified clean Discord reconnection.
- **Phase**: ROOK-P3 — Migration to Dell T340 CT 201 & Local MoE Deployment
  - **Result**: PASS on 2026-11-12
  - **Summary**:
    - Provisioned CT 201 on T340 `tank-zfs` with 100GB SSD rootfs and 24GB elastic RAM.
    - Migrated 28GB user environment from HPE NAS and upgraded OpenClaw to 2026.11.3.
    - Built AVX2-accelerated llama-server and deployed DeepSeek-Coder-V2-Lite-Instruct MoE (15 tok/s).
    - Enforced strict RFC1918 Proxmox firewall with explicit DNS pinhole.
    - Re-routed local tools (`qwen_coder.py`) to loopback engine; verified C generation canary.
    - Quiesced and disabled old container on HPE NAS.
- **State Commit**: Resolve with `git log -1 -- rook.md`

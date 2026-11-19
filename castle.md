---
project_id: 202
name: castle
aliases: ["cas"]
status: ACTIVE
last_updated: 2026-11-19 12:45:00 UTC
local_path: /home/castle
architecture_version: 1.4.0
state_version: 1.4.0
peer_project_id: 201 # Rook
---

# Castle ("Cas") Autonomous Peer Sandbox Agent (State 202)

## 1. Project Overview & Role
**Castle** (or **"Cas"**) is an isolated, autonomous sandbox AI agent running OpenClaw inside a dedicated LXD container on the HPE NAS (`192.168.1.199`). It operates with full local execution permissions inside its container while strictly quarantined from the local private network (LAN isolation).

Castle serves as the high-speed scout, broad-context ingestor, and rapid tool executor backed by Google AI Studio's Gemini 3.5 Flash Lite architecture with an expansive context ceiling, collaborating directly with **Rook** (State 201) over an isolated point-to-point interface.

## 2. Infrastructure & Compute Specs
- **Host Node**: Bare-Metal HPE ProLiant ML30 Gen9 (`192.168.1.199`).
- **Container Runtime**: Linux Containers (LXD) unprivileged container (`castle`) on Debian 12 bookworm.
- **Compute Allocations**:
  - vCPUs: 3 pinned cores.
  - RAM: 12 GiB memory ceiling.
  - Disk: Dedicated sub-allocation on secondary SSD partition (`/dev/sdb1`, pool `sdb-pool`), preserving isolation from primary ZFS pool `tank`.
- **Runtime User**: Dedicated non-root user `castle` (`/home/castle`).
- **Daemon Stack**: OpenClaw gateway service managed via systemd user unit (`openclaw-gateway.service`) running on loopback port `18789`.
- **Discord Ack Reaction**: `🏰` (`\ud83c\udff0` European Castle) upon receiving mention.

## 3. Network Architecture & Strict Zero-Leak Isolation (Option B)

### Host Quarantine & P2P Interconnect
```
                           +----------------------------+
                           |        WAN / Internet      |
                           |   (Google AI Studio /      |
                           |     Discord Gateways)      |
                           +--------------+-------------+
                                          ^
                            Outbound WAN  |  Outbound WAN
                            (nftables ok) |  (nftables ok)
                                          |
                      +-------------------+-------------------+
                      |                                       |
       +--------------+--------------+         +--------------+--------------+
       |         Rook LXC            |         |        Castle LXD           |
       |          ("rook")           |         |         ("castle")          |
       |                             |         |                             |
       |  eth0: Outbound WAN + Kobold|         |  eth0: Outbound WAN + Kobold|
       |  RFC1918 egress DROPPED     |         |  RFC1918 egress DROPPED     |
       |                             |         |                             |
       |  eth1: 10.99.0.1/30         |<=======>|  eth1: 10.99.0.2/30         |
       +--------------+--------------+   P2P   +--------------+--------------+
                      |                 LINK                  |
                      v (Port 5001)                           v (Port 5001)
            +---------+---------------------------------------+---------+
            |  Local KoboldCPP AMD Inference Rig (192.168.1.190:5001)   |
            +-----------------------------------------------------------+
                                        |
                             [RFC 1918 LAN QUARANTINE]
                  (All other 192.168.1.x & Hypervisors BLOCKED)
```

- **WAN Interface (`eth0`)**: Inherits host-level `inet quarantine` nftables drop for all RFC1918 subnets (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`) while permitting KoboldCPP inference on `192.168.1.190:5001`.
- **Peer Interface (`eth1`, Option B P2P)**: Connected via unmanaged bridge `agent-p2p` with no gateway:
  - Rook: `10.99.0.1/30`
  - Castle: `10.99.0.2/30`
  - Zero routing capability outside the two containers.

## 4. Inference Model Ladder & Provider Architecture
Castle utilizes a multi-provider fallback ladder to ensure zero-cost operation and immunity from single-provider rate limits:

1. **Primary**: `google/gemini-3.5-flash-lite` (Google AI Studio direct, 500 RPD, 15 RPM)
2. **Fallback #1**: `google/gemini-3.1-flash-lite` (Google AI Studio direct)
3. **Fallback #2**: `openrouter/nvidia/nemotron-3-ultra-550b-a55b:free` (Cross-Provider Safety Net, OpenRouter Free)
4. **Fallback #3**: `openrouter/openrouter/free` (Cross-Provider Secondary Safety Net)
5. **Fallback #4**: `live/gemini-live` (`http://127.0.0.1:18850/v1` via local `live-bridge.mjs`)

## 5. Live Verification Ledger (2026-11-03)
* [x] **Container Launched & Pinned**: 3 cores, 12GB RAM, `sdb-pool`.
* [x] **P2P Network Active**: Bidirectional ping verified between Rook (`10.99.0.1`) and Castle (`10.99.0.2`).
* [x] **Firewall Isolation Active**: WAN ping 1.1.1.1 PASS; RFC1918 ping 192.168.1.177 100% DROP.
* [x] **KoboldCPP Offload Pinhole Active**: `/v1/models` reachable on `192.168.1.190:5001`.
* [x] **Local Coder Tool**: `qwen_coder.py` operational with isolated Python 3.11 venv.
* [x] **Local Scraper & Media Tools**: `web_fetch.py` and `yt_transcript.py` synced from Rook with dependencies.
* [x] **Local Meta-Search Engine MCP**: `searxng` MCP server active on `http://10.117.2.189:8889/mcp`.
* [x] **Request Pacing Throttling**: `humanDelay` custom mode active (6000ms–9000ms) to throttle Discord output pacing.
* [x] **Tool Surface Pruning**: Disabled 12 redundant bundled plugins (browser, canvas, alibaba, xai, anthropic, etc.).
* [x] **Agent Identity & Operational Anchor**: Deployed `/home/castle/.openclaw/workspace/AGENTS.md` giving Castle explicit awareness of local shortcuts and quota limits.
* [x] **Daily Memory Subsystem Online**:
  - Memory directory active at `/home/castle/.openclaw/workspace/memory/`.
  - Today's memory log bootstrapped at `memory/2026-11-03.md`.
  - Trigger words configured: *"remember this: ..."*, *"note this down: ..."*, *"save to memory: ..."*.
  - Compaction hook linked to record 1B Discord footnote + daily memory ledger.
* [x] **Secrets Vault**: Configured in `/home/castle/.openclaw/.keys/secrets.json` (mode 0600).
* [x] **OpenClaw Gateway Service**: Active and healthy on loopback `18789`.
* [x] **Discord Bot Online**: Connected as **@Castle** on live Discord gateway.
* [x] **Mutual Bot Peering**:
  - Rook (`1564591509192441908`) allowlisted in Castle.
  - Castle (`1567129284210982914`) allowlisted in Rook.
  - Peer interactions active in `#debate-club` (`1565679021121871895`).

## 6. Architectural Guardrails
1. **No Cron Schema in Config (Fatal Exit 78)**:
   - OpenClaw does not support `"cron": { "jobs": ... }` blocks in `openclaw.json`. All periodic agent tasks must use user systemd timers (`~/.config/systemd/user/*.timer`).
2. **Storage Snapshot Safety (ext4 `dir` Driver)**:
   - `sdb-pool` uses the `dir` driver. Never execute blocking synchronous `lxc snapshot castle <name>` over interactive SSH. Use targeted tarballs for configs or `--no-wait` when taking container snapshots.
3. **Turn Limits & Ping-Pong Loop Breaker**:
   - P2P communication between Rook and Castle must enforce `maxSteps: 10` per task and a hard conversational turn cap (max 5 peer replies) to prevent infinite recursive quota drain.
4. **Discord Media Contract**:
   - Attachments must follow `[{"path": "/path/to/file"}]` format. Never pass plain strings or raw objects.

## 7. Bounded Container Pipe Restoration (2026-11-18)
- **Status**: ACTIVE & OPERATIONAL
- **Interconnect**: `agent-p2p` bridge (`10.99.0.0/30` over `eth1`)
  - Castle: `10.99.0.2`
  - Rook: `10.99.0.1`
- **Exposed Peer Services on Rook**:
  - SearXNG Search Engine: `http://10.99.0.1:8888/search`
  - Survival Backend & Telemetry: `http://10.99.0.1:8080/api/health` and `/api/agents`
- **Castle Client Tools**:
  - `/home/castle/.openclaw/workspace/tools/peer_search.py` (SearXNG client, 5.0s timeout, capped 3 results)
  - `/home/castle/.openclaw/workspace/tools/peer_survival.py` (Survival health, telemetry and heartbeat, 3.5s timeout)
- **Protocol**: `RELAY_PROTOCOL.md` remains the sole coordination authority for code and projects ("No object, no claim"). The container pipe is strictly a stateless/read-only data bus.

## 8. Google 15 RPM Rate-Limit Incident & Safeguards Rollout (2026-11-19)
- **Incident Diagnosis**:
  - Castle encountered `429: You exceeded your current quota... [code=RESOURCE_EXHAUSTED]` at 12:32:31 UTC in `#debate-club`.
  - Root cause: Castle fired 8 autonomous `exec` tool calls within 21 seconds hunting for tea art files (~23 RPM burst), breaching Google AI Studio Free Tier's hard 15 RPM ceiling.
  - Failover failure: Fallback #1 (`gemini-3.1-flash-lite`) and Fallback #2 (`gemini-live`) both shared the same Google API key, resulting in project-wide rejection across all configured models.
- **Deployed Safeguards**:
  1. **Cross-Provider Safety Net**:
     - Injected `openrouter_api_key` into `/home/castle/.openclaw/.keys/secrets.json`.
     - Added `openrouter/nvidia/nemotron-3-ultra-550b-a55b:free` (Fallback #2) and `openrouter/openrouter/free` (Fallback #3) into Castle's `openclaw.json`.
     - Guarantees seamless failover to an independent provider if Google's 15 RPM window is temporarily saturated.
  2. **Multi-Step Tool Burst Brake in `AGENTS.md`**:
     - Hard limit of max 3 consecutive autonomous tool calls in a single response turn before pausing to report progress.
     - Pacing instruction (`sleep 3`) for chained repetitive bash/search operations to keep throughput $\le 12$ RPM.
     - 2-miss cutoff rule: If files or commits are not located after 2 attempts, Castle must stop and ask for guidance rather than burning quota on blind iterative variations.
  3. **Discord Command ACL Sync**:
     - Added all Discord allowlist IDs to `commands.allowFrom.discord` in `openclaw.json` so operators can run `/model` without permission rejections.
- **Status**: Live and verified. Verified via `openclaw models list`, service restart, and active Discord gateway connection.

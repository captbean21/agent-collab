---
project_id: 202
name: castle
aliases: ["cas"]
status: ACTIVE
last_updated: 2026-11-07 10:28:00 UTC
local_path: /home/castle
architecture_version: 1.2.0
state_version: 1.2.0
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
       |         Rook LXD            |         |        Castle LXD           |
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

## 4. Inference Model Ladder (High-Allowance Tier Locked)
1. **Primary**: `google/gemini-3.5-flash-lite` (500 RPD, 15 RPM)
2. **Fallback 1**: `google/gemini-3.1-flash-lite` (500 RPD, 15 RPM)
3. **Fallback 2**: `google/gemini-flash-lite-latest` (500 RPD rolling production pointer)
4. **Local Heavy Worker**: `local/koboldcpp/Qwen3.8-27B-OQ3` on `http://192.168.1.190:5001/v1` (unlimited, zero-token cost).

## 5. Live Verification Ledger (2026-11-03)
* [x] **Container Launched & Pinned**: 3 cores, 12GB RAM, `sdb-pool`.
* [x] **P2P Network Active**: Bidirectional ping verified between Rook (`10.99.0.1`) and Castle (`10.99.0.2`).
* [x] **Firewall Isolation Active**: WAN ping 1.1.1.1 PASS; RFC1918 ping 192.168.1.177 100% DROP.
* [x] **KoboldCPP Offload Pinhole Active**: `/v1/models` reachable on `192.168.1.190:5001`.
* [x] **Local Coder Tool**: `qwen_coder.py` operational with isolated Python 3.11 venv.
* [x] **Local Scraper & Media Tools**: `web_fetch.py` and `yt_transcript.py` synced from Rook with dependencies.
* [x] **Local Meta-Search Engine MCP**: `searxng` MCP server active on `http://10.117.2.189:8889/mcp`.
* [x] **Request Pacing Throttling**: `humanDelay` custom mode active (2500ms–4500ms inter-step delay) to enforce the 15 RPM ceiling.
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
* [x] **Gemini Quota Gate Sidecar (Parked at v4 Verified Stage - 2026-11-07)**:
  - Agent-scoped loopback sidecar (`gemini_quota_gate.py` on `127.0.0.1:18790`).
  - Strict admission formula: `len(raw_body_bytes) + reserved_output`.
  - Missing `generationConfig.maxOutputTokens` proven and defaulted to `65,536` (matching Castle's installed Google provider catalog ceiling).
  - Rate bounds: 200k TPM rolling 60s, 12 RPM rolling 60s, 450 RPD rolling 24h, max 1 in-flight.
  - Failover signal: All local rejections emit `out of budget [<reason>]` (e.g. `out of budget [tpm_saturated]`), which trips OpenClaw's `hasLongWindowRateLimitEvidence`, classifies as `billing`, enforces `shouldRetryFailoverSignal: false`, and causes immediate, zero-delay failover to local KoboldCPP (`Qwen3.8-27B-OQ3`) with zero same-model retries.
  - Local KoboldCPP worker health verified responsive (`0.57s` hot latency on `192.168.1.190:5001`).
  - Staged packages in Rook workspace:
    * `/home/rook/.openclaw/workspace/castle-gemini-quota-gate-v3.1.tar.gz`
    * `/home/rook/.openclaw/workspace/castle-gemini-quota-gate-v4.tar.gz` (`437ad808343c0b0c8be8a4060175ba0c73b69e9d0e9eab22bf79f75cce038e69`)
  - Status: Parked clean. All tests pass (12 staged tests + end-to-end transport regression). Castle live container is running on clean original pre-gate configuration with active Discord bot connection.

## 2. Infrastructure & Compute Specs
- **Host Node**: Bare-Metal HPE ProLiant ML30 Gen9 (`192.168.1.199`).
- **Container Runtime**: Linux Containers (LXD) unprivileged container (`castle-agent`) on Debian 12 bookworm.
- **Compute Allocations**:
  - vCPUs: 2–3 pinned cores.
  - RAM: 8–16 GiB memory ceiling.
  - Disk: Dedicated sub-allocation on secondary SSD partition (`/dev/sdb1`, pool `sdb-pool`), preserving isolation from primary ZFS pool `tank`.
- **Runtime User**: Dedicated non-root user `castle` (`/home/castle`).
- **Daemon Stack**: OpenClaw gateway service managed via systemd user unit (`openclaw-gateway.service`).

## 3. Network Architecture & Strict Zero-Leak Isolation (Option B)

### Host Quarantine Mechanics (Discovered on HPE Host)
The HPE host (`192.168.1.199`) enforces RFC1918 LAN quarantine via the host-level `inet quarantine` nftables table:
```nftables
table inet quarantine {
    chain forward {
        type filter hook forward priority filter - 10; policy accept;
        iifname "lxdbr0" ip daddr 192.168.1.190 tcp dport 5001 accept
        iifname "lxdbr0" ip daddr { 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16 } drop
    }
}
```
Because both Rook and Castle connect their primary interface (`eth0`) to `lxdbr0`, **Castle instantly and automatically inherits the exact same ironclad LAN quarantine and KoboldCPP pinhole without needing new host firewall modifications**.

### Option B Peer-to-Peer Interconnect (`peer0`)
To allow direct Rook <-> Castle communication without touching `lxdbr0` or traversing the host routing table:
1. Provision unrouted L2 bridge:
   ```bash
   lxc network create agent-p2p ipv4.address=none ipv6.address=none
   ```
2. Attach `peer0` to both containers:
   ```bash
   lxc network attach agent-p2p rook peer0
   lxc network attach agent-p2p castle peer0
   ```
3. Assign static peer IP addresses (no default gateway):
   - Rook: `10.99.0.1/30`
   - Castle: `10.99.0.2/30`
4. Result:
   - Rook and Castle can exchange direct HTTP/RPC packets over `10.99.0.0/30`.
   - `peer0` has no gateway and cannot route to WAN or LAN.
   - `eth0` handles outbound WAN (Google API / Discord) with RFC1918 dropped at the host kernel.

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
       |         Rook LXD            |         |        Castle LXD           |
       |       ("rook-agent")        |         |      ("castle-agent")       |
       |                             |         |                             |
       |  eth0: Outbound WAN + Kobold|         |  eth0: Outbound WAN + Kobold|
       |  RFC1918 egress DROPPED     |         |  RFC1918 egress DROPPED     |
       |                             |         |                             |
       |  peer0: 10.99.0.1/30        |<=======>|  peer0: 10.99.0.2/30        |
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

### Network Invariants:
1. **Primary Interface (`eth0`)**:
   - Outbound WAN access for API calls, tool dependencies, and messaging.
   - Strict `nftables` RFC1918 drop rule blocking all access to `10.0.0.0/8`, `172.16.0.0/12`, and `192.168.0.0/16`.
   - Pinhole exception explicitly permits TCP port 5001 to AMD Inference Rig (`192.168.1.190:5001`) for local KoboldCPP Qwen 27B worker offload.
   - Inbound SSH strictly limited to AGY controller (`192.168.1.178`).
2. **Peer Interface (`peer0`, Option B Point-to-Point)**:
   - Dedicated unrouted LXD network:
     ```bash
     lxc network create agent-p2p ipv4.address=none ipv6.address=none
     lxc network attach agent-p2p rook peer0
     lxc network attach agent-p2p castle peer0
     ```
   - Static IP assignment: Rook = `10.99.0.1/30`, Castle = `10.99.0.2/30`.
   - **No default gateway on `peer0`**: Traffic has zero physical or logical route to reach the host LAN or outside subnets.

## 4. Model Backend & Inference Strategy

### Primary Engine: Google AI Studio Free Tier (VERIFIED ACTIVE 2026-11-03)
- **Status**: Verified active with HTTP 200 via API canary probe.
- **Provider**: Google AI Studio API (`https://generativelanguage.googleapis.com/v1beta`)
- **Key Location**: `/home/castle/.openclaw/.keys/google_ai_studio.key` (mode 0600, pointed via config)
- **Verified Model Roster Available on Account**:
  - `gemini-3.5-flash-lite` (Top Candidate: maximum speed, high throughput)
  - `gemini-3.5-flash` (Strong reasoning, multimodal)
  - `gemini-2.5-flash` / `gemini-2.5-flash-lite` (Stable fallback baselines)
  - `gemini-3.8-flash` / `gemini-3.1-flash-lite`
- **Quota & Ceilings**:
  - Request Limit: 1,500 Requests Per Day (RPD), automatically resetting at midnight PT.
  - Rate Limit: 15 Requests Per Minute (RPM) — pacing delays enforced.
  - Working Context Buffer: 150k to 262k tokens default (expandable up to 1M native context).
- **Separation of Quotas**:
  - Castle's traffic is 100% separate from Rook's OpenRouter quota.
  - Completely avoids multi-accounting or Sybil ban risks on OpenRouter.

### Inference Fallback Ladder
1. **Primary**: `google/gemini-3.5-flash-lite` (Google AI Studio direct)
2. **Fallback 1**: `google/gemini-3.5-flash` (higher capacity reasoning)
3. **Fallback 2**: `google/gemini-2.5-flash` (stable baseline)
4. **Local Heavy Worker**: `local/koboldcpp/Qwen3.8-27B-OQ3` on `http://192.168.1.190:5001/v1` (unlimited, zero-token cost).

## 5. Architectural Guardrails (Inherited from Rook Lessons)
1. **No Cron Schema in Config (Fatal Exit 78)**:
   - OpenClaw does not support `"cron": { "jobs": ... }` blocks in `openclaw.json`. All periodic agent tasks must use user systemd timers (`~/.config/systemd/user/*.timer`).
2. **Storage Snapshot Safety (ext4 `dir` Driver)**:
   - `sdb-pool` uses the `dir` driver. Never execute blocking synchronous `lxc snapshot castle <name>` over interactive SSH. Use targeted tarballs for configs or `--no-wait` when taking container snapshots.
3. **Turn Limits & Ping-Pong Loop Breaker**:
   - P2P communication between Rook and Castle must enforce `maxSteps: 10` per task and a hard conversational turn cap (max 5 peer replies) to prevent infinite recursive quota drain.
4. **Rate Pacing for 15 RPM**:
   - Castle's OpenClaw client must enforce a 250–500ms pacing delay between tool iterations to avoid tripping Google's 15 RPM cap during rapid automated execution.
5. **Discord Media Contract**:
   - If using Discord bots, attachments must follow `[{"path": "/path/to/file"}]` format.

---

## 6. Immediate Next Milestone: API Canary Testing

> [!IMPORTANT]
> **GATEWAY PAUSE / OPERATOR CHECKPOINT**
> Before provisioning the LXD container or deploying configurations, we must run an isolated API canary test against the Google AI Studio free tier to verify:
> 1. Exact model endpoint names accepted (`gemini-2.5-flash`, `gemini-2.5-flash-lite`, etc.).
> 2. Rate limit behavior and response status codes.
> 3. Context payload tolerance and tool-calling compatibility.

### Canary Test Script Template (To execute once API key is provided)
```bash
# Set test key temporarily in current shell (never written to file or history):
export GOOGLE_API_KEY="<OPERATOR_SUPPLIED_KEY>"

# Test model listing and availability:
curl -s "https://generativelanguage.googleapis.com/v1beta/models?key=${GOOGLE_API_KEY}" | grep -E '"name":|"displayName":'

# Test minimal inference call:
curl -s -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${GOOGLE_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"contents":[{"parts":[{"text":"Canary check: respond with Castle online."}]}]}'
```

# Boundary Pipe — Real-World Use Case

**Version:** 2026-11-19  
**Authors:** Castle & Rook  
**Status:** Production-ready (git sync transport proven)

---

## The Problem: Distributed Agent Memory Without Shared RAM

Two autonomous agents (Rook on T340, Castle on HPE) need to:
- Share semantic memory (vectors, embeddings)
- Coordinate tasks without a central orchestrator
- Survive network partitions, container restarts, quota limits
- Operate within free-tier token budgets
- Maintain auditability and "no object, no claim" integrity

Traditional approaches fail:
- **Shared Redis/Qdrant over WAN** — latency, auth complexity, firewall rules
- **Message queues (RabbitMQ, NATS)** — single point of failure, ops overhead
- **Direct RPC/gRPC** — tight coupling, versioning hell, container isolation
- **Polling HTTP APIs** — wasteful, rate-limited, fragile

---

## The Solution: Git as the Transport Layer

**Git sync (`agent-collab` repo) IS the Boundary Pipe.**

### Architecture

```
┌─────────────────────┐     git push/pull      ┌─────────────────────┐
│   Rook (T340)       │ ◄────────────────────► │  Castle (HPE)       │
│                     │                         │                     │
│  Qdrant (local)     │                         │  Qdrant (local)     │
│  - memory_bus       │   JSON sync via git     │  - memory_bus       │
│  - research_atlas   │   commits as checkpoints│  - youtube_summaries│
│                     │                         │                     │
│  Tools/             │                         │  Tools/             │
│  - shared_memory_   │                         │  - shared_memory_   │
│    client.py        │                         │    client.py        │
└─────────────────────┘                         └─────────────────────┘
```

### What Flows Through the Pipe

| Artifact | Format | Sync Trigger | Use Case |
|----------|--------|--------------|----------|
| **Memory vectors** | JSON (point: id, vector, payload) | On write | Semantic memory hydration |
| **Task state** | JSON (status, progress, result) | Task completion | Cross-agent handoff |
| **Research digests** | Markdown + JSON metadata | Daily cron | Knowledge sharing |
| **Tool configs** | YAML/JSON | Config change | Environment parity |
| **Artifacts** | Base64 in JSON (small) / git LFS (large) | Generation | Images, audio, binaries |

---

## Concrete Use Case: "Overnight Research & Morning Brief"

### Scenario
Castle (scout) runs overnight web research. Rook (anchor) needs synthesized briefing at 08:00 UTC for Bean's morning standup.

### Step-by-Step Execution

#### 22:00 — Castle Begins Research Sweep
```bash
# Castle runs research cycle (on HPE)
python3 tools/research_cycle.py --topic "agent memory architectures" --depth deep
```
**Output:** `research/2026-11-19/agent-memory-architectures.json` (12 papers, 47 key insights)

#### 22:30 — Castle Commits Research
```bash
git add research/2026-11-19/
git commit -m "feat(research): agent memory architectures sweep — 12 papers, 47 insights"
git push origin main
```

#### 23:00 — Castle Runs Synthesis
```bash
python3 tools/hybrid_summarize.py --input research/2026-11-19/agent-memory-architectures.json \
  --output digests/2026-11-19/agent-memory-brief.md
```

#### 23:15 — Castle Pushes Digest
```bash
git add digests/2026-11-19/
git commit -m "feat(digest): agent memory architectures brief for morning standup"
git push origin main
```

#### 07:55 — Rook Pulls & Prepares Briefing
```bash
# Rook wakes up (on T340)
git pull origin main

# Rook reads digest, adds debate framing
python3 tools/debate_turn_guard.py --digest digests/2026-11-19/agent-memory-brief.md \
  --output briefings/2026-11-19/morning-standup.md
```

#### 08:00 — Bean Receives Briefing
```bash
# Bean reads briefing via GitHub Pages or raw git
curl https://captbean21.github.io/agent-collab/briefings/2026-11-19/morning-standup.md
```

### Key Properties Demonstrated

| Property | How It's Achieved |
|----------|-------------------|
| **Decentralized** | No central server; each agent has full repo |
| **Auditability** | Every insight has commit hash + timestamp |
| **Resilience** | Network partition? Work continues locally; sync on reconnect |
| **Quota-aware** | Heavy LLM work on local models (Rook's Qwen 14B); only commits use tokens |
| **Free-tier friendly** | GitHub Actions for CI; GitHub Pages for publishing; zero infra cost |
| **Audit trail** | `git log --oneline research/` shows full lineage |
| **Rollback** | `git revert <commit>` if insight is wrong |

---

## Secondary Use Case: "Qdrant Vector Hydration Across Nodes"

### Problem
Both agents need the same semantic memory (680 points in `memory_bus`). Qdrant runs on T340 only.

### Solution: Git-Backed Vector Sync

```bash
# Rook (source of truth) exports vectors weekly
python3 tools/qdrant_export.py --collection memory_bus \
  --output vectors/memory_bus/2026-11-19.json

git add vectors/memory_bus/2026-11-19.json
git commit -m "chore(vectors): weekly memory_bus export — 680 points"
git push origin main
```

```bash
# Castle pulls and imports
git pull origin main
python3 tools/qdrant_import.py --collection memory_bus \
  --input vectors/memory_bus/2026-11-19.json
```

**Result:** Both agents have identical semantic memory without live Qdrant replication.

---

## Tertiary Use Case: "Tool Config Parity"

### Problem
Agents share tools (`shared_memory_client.py`, `research_cycle.py`, `debate_turn_guard.py`). Config drift causes silent failures.

### Solution: Config as Code in Repo

```
tools/
├── boundary_pipe_config.json      # Endpoints, status
├── shared_memory_client.py        # Client library
├── setup_reverse_tunnel.sh        # SSH tunnel automation
├── castle_sync.sh                 # Periodic sync cron
└── castle-rook-tunnel.service     # systemd unit
```

**Change config → commit → push → other agent pulls → instant parity.**

---

## Why This Beats Traditional Approaches

| Dimension | Traditional (MQ/Redis/gRPC) | Git Sync Pipe |
|-----------|----------------------------|---------------|
| **Ops burden** | High (broker, auth, certs, monitoring) | Zero (GitHub handles it) |
| **Cost** | $/month for managed services | Free (GitHub free tier) |
| **Audit trail** | Separate logging infra | Native (`git log`) |
| **Offline work** | Impossible | First-class citizen |
| **Rollback** | Complex (backup/restore) | `git revert` |
| **Branching** | Not applicable | Native (feature branches) |
| **Code review** | Separate tool | PRs on GitHub |
| **Free-tier fit** | Poor (connection limits) | Perfect (git is free) |

---

## Operational Checklist for New Session

```bash
# 1. Verify git sync works
cd agent-collab && git pull origin main && git push origin main

# 2. Verify local services (Rook/T340)
curl -s http://localhost:6333/health && echo "Qdrant OK"
curl -s http://localhost:8080/api/health && echo "Survival OK"
curl -s http://localhost:8888/ && echo "SearXNG OK"

# 3. Verify tooling
python3 tools/shared_memory_client.py --action qdrant-health

# 4. Run sync test
./tools/castle_sync.sh  # (on HPE host, manual for now)

# 5. Check GitHub Pages
curl -s https://captbean21.github.io/agent-collab/art.html | head -5
```

---

## Future Enhancements (Documented, Not Blocking)

| Enhancement | Location | Status |
|-------------|----------|--------|
| SSH reverse tunnel (HPE→T340) | `tools/setup_reverse_tunnel.sh` | Documented, ready |
| Named Cloudflare tunnel | `/etc/cloudflared/config.yml` | Credentials needed |
| Qdrant replication | `tools/qdrant_export.py` + `qdrant_import.py` | Planned |
| Automated briefing pipeline | GitHub Action + cron | Planned |
| Vector diff sync (incremental) | `tools/qdrant_diff_sync.py` | Designed |

---

## Summary

**The Boundary Pipe is Git.** 

No message broker. No shared database. No VPN. No firewall rules. No SSL certs. No message format versioning. No single point of failure.

Just `git push` / `git pull` — the most battle-tested, decentralized, auditable, free-tier-friendly sync primitive in existence.

**Commit hashes are the truth. Git log is the ledger. GitHub is the infrastructure.**

---

*Saved for next session. Ready to execute.*
# Agent Self-Improvement Plan: Research Aggregator + Meta-Skill Writer

**Status:** DRAFT — for review before implementation  
**Target:** Rook (agent:main) workspace  
**Hardware:** Shared GPU rig (192.168.1.190:5001) — local SearXNG + Python toolchain  
**Constraints:** Zero VRAM contention, all timers via `openclaw-cli-cron` skill

---

## Overview

Deploy two complementary autonomous skills that run on timers and compound value over time:

| Skill | Purpose | Timer Cadence | Output |
|-------|---------|---------------|--------|
| **B: Research Aggregator** | Continuous web research on agent robustness topics → local wiki | 6h research cycle + daily digest | `~/workspace/research/<topic>.md` + `INDEX.md` |
| **E: Meta-Skill Writer** | Scan workspace/traces → propose new skills → draft for approval | Weekly (Sat scan + Sun proposal) | `~/workspace/skills/proposals/*.md` → promoted skills |

Both documented as `.md` skills in workspace, both use `openclaw-cli-cron` for timer registration.

---

## Skill B: Research Aggregator

### Timer Schedule (via `openclaw-cli-cron`)

| Cron Expression | Action | Script |
|-----------------|--------|--------|
| `0 */6 * * *` | Research cycle: pick next topic → search → fetch top 3 → summarize → append | `~/tools/research_cycle.py` |
| `0 6 * * *` | Daily digest: cross-link new entries → update INDEX.md → append to daily memory | `~/tools/research_digest.py` |
| `0 3 * * 0` | Weekly maintenance: detect stale entries (>30d) → flag for refresh | `~/tools/research_maintenance.py` |

**Timezone:** UTC (IANA: `Etc/UTC`)

### Topic Source

`~/workspace/research/topics.txt` — one topic per line:
```
topic_slug | priority (1-5) | notes
```

**Initial 10 topics (from discussion):**
```
context-window-management | 5 | sliding windows, KV eviction policies, hierarchical memory
cpu-background-inference | 5 | 1.5B-3B models on CPU, zero VRAM contention
structured-output-gbnf | 4 | llama.cpp grammars for reliable tool calls
self-correction-loops | 5 | Reflexion, self-consistency, bounded iterations
local-embedding-rerank | 4 | BGE-M3, Jina, mixedbread — full local retrieval
argument-mapping | 3 | claim decomposition, evidence linking, confidence scoring
config-drift-detection | 5 | hash configs, alert, auto-rollback
session-continuity | 5 | memory log format, cold-start skill
auto-skill-synthesis | 4 | from traces → skill draft → test → promote
model-routing-cascades | 3 | small→large escalation, Pareto optimization
```

### Research Cycle Algorithm (`research_cycle.py`)

1. **Read topics.txt** → filter priority ≥ 4 → pick next unprocessed (round-robin with `last_researched` timestamp)
2. **SearXNG search:** `site:github.com OR site:arxiv.org OR site:huggingface.co "<topic>"` + general web
3. **Fetch top 3 results** via `web_fetch.py --focus "<topic>"` (15k char cap each)
4. **Summarize in-context** (Hobb/agent digests — no `--summarize` flag)
5. **Append to** `~/workspace/research/<topic_slug>.md` with:
   - Date header
   - Source URLs
   - Key findings (bulleted)
   - Open questions
6. **Update `last_researched`** in topics.txt (or separate state file)

### Output Structure

```
~/workspace/research/
├── topics.txt                 # Source of truth
├── INDEX.md                   # Auto-generated TOC + cross-links
├── context-window-management.md
├── cpu-background-inference.md
├── structured-output-gbnf.md
├── self-correction-loops.md
├── local-embedding-rerank.md
├── argument-mapping.md
├── config-drift-detection.md
├── session-continuity.md
├── auto-skill-synthesis.md
└── model-routing-cascades.md
```

### Skill File: `~/workspace/research/aggregator_skill.md`

```markdown
---
name: research-aggregator
description: Continuous local web research on agent engineering topics. 6h cycle via SearXNG + web_fetch.py, daily digest, weekly maintenance. Builds a growing Markdown wiki in ~/workspace/research/.
trigger: Cron (0 */6 * * *, 0 6 * * *, 0 3 * * 0)
produces: Research wiki (Markdown), daily memory entries, weekly stale flags
---

## Procedure

### Research Cycle (every 6h)
1. Load ~/workspace/research/topics.txt
2. Select next priority≥4 topic (round-robin by last_researched)
3. Search SearXNG: `site:github.com OR site:arxiv.org OR site:huggingface.co "<topic>"`
4. For top 3 results: python3 ~/tools/web_fetch.py --focus "<topic>"
5. Append findings to ~/workspace/research/<topic_slug>.md
6. Update last_researched timestamp

### Daily Digest (06:00 UTC)
1. Scan research/ for files modified in last 24h
2. Generate cross-links → update INDEX.md
3. Append one-line summary to today's memory log

### Weekly Maintenance (Sun 03:00 UTC)
1. Find entries older than 30 days with no updates
2. Append "STALE" flag to topic file
3. Log to memory

## Dependencies
- Local SearXNG on :8888
- ~/tools/web_fetch.py, yt_transcript.py
- openclaw-cli-cron skill for timer registration
```

---

## Skill E: Meta-Skill Writer

### Timer Schedule (via `openclaw-cli-cron`)

| Cron Expression | Action | Script |
|-----------------|--------|--------|
| `0 3 * * 6` | Saturday scan: analyze memory/, AGENTS.md, recent sessions → detect repeated patterns → draft 1-2 skill proposals | `~/tools/meta_scan.py` |
| `0 4 * * 0` | Sunday proposal: post proposals to #rook for Bean approval | `~/tools/meta_propose.py` |
| `0 5 * * 1` | Monday promote: if approved, create skill via skill_workshop | `~/tools/meta_promote.py` |

**Timezone:** UTC

### Scan Sources (Saturday 03:00)

1. **`memory/YYYY-MM-DD.md`** (last 14 days) — recurring tasks, manual workarounds, "I keep doing X"
2. **`AGENTS.md`** — rules that imply automation ("always do X before Y")
3. **Recent session transcripts** (via `sessions_history`) — tool call patterns, repeated multi-step flows
4. **`~/workspace/research/`** — topics that became procedural knowledge

### Pattern Detection Heuristics

| Pattern | Signal | Proposed Skill |
|---------|--------|----------------|
| Same 3+ tool calls in sequence across ≥3 sessions | Tool call n-grams | "Workflow: X → Y → Z" |
| Manual file edit + grep + edit repeated | File ops + search | "Edit-and-verify: <file>" |
| Repeated SearXNG + fetch + summarize on same domain | Research cycle | "Deep-dive: <domain>" |
| Memory log entries saying "remember to..." | Explicit intent | "Checklist: <task>" |
| Debate/club analysis repeated | Event + scheduled | "Debate logger + analyzer" |

### Proposal Format (`~/workspace/skills/proposals/<slug>.md`)

```markdown
---
name: <slug>
description: <one-line trigger + output>
source: auto-detected from <source> on <date>
status: proposed
---

## Detected Pattern
- Sessions: <session_keys>
- Frequency: <count> times in <window>
- Steps observed:
  1. <tool/action>
  2. <tool/action>
  ...

## Proposed Skill
**Trigger:** <when to use>
**Produces:** <artifact/outcome>
**Steps:**
1. <concrete step with tool/command>
2. <concrete step with tool/command>
...

## Acceptance Criteria
- [ ] Runs without manual intervention
- [ ] Produces expected artifact
- [ ] Documented in workspace
```

### Promotion Flow (Monday 05:00)

1. Read proposals with `status: approved` (Bean adds reaction ✅ or replies "approve")
2. Call `skill_workshop` action=create with full SKILL.md content
3. Register any new cron timers via `openclaw-cli-cron`
4. Update proposal `status: promoted` + link to skill location

### Skill File: `~/workspace/skills/meta-skill-writer.md`

```markdown
---
name: meta-skill-writer
description: Weekly scan of workspace memory/sessions/research → detect repeated patterns → draft skill proposals for approval → auto-promote on approval. Runs Sat scan, Sun propose, Mon promote.
trigger: Cron (0 3 * * 6, 0 4 * * 0, 0 5 * * 1)
produces: Skill proposals in ~/workspace/skills/proposals/, promoted skills via skill_workshop
---

## Procedure

### Saturday Scan (03:00 UTC)
1. Read memory/ (last 14 days), AGENTS.md, recent sessions
2. Extract recurring tool-call sequences, manual workflows, explicit intents
3. Cluster by similarity → top 2 patterns
4. Draft proposals in ~/workspace/skills/proposals/<slug>.md

### Sunday Propose (04:00 UTC)
1. Post each proposal to #rook channel with ✅/❌ reactions
2. Format: "🤖 Meta-skill proposal: <name> — <one-line>. React ✅ to approve."

### Monday Promote (05:00 UTC)
1. For each proposal with ✅ from Bean: skill_workshop create
2. Register new cron timers if skill defines them
3. Mark proposal promoted

## Dependencies
- skill_workshop tool
- openclaw-cli-cron skill
- sessions_history tool (for session pattern mining)
- message tool (for #rook proposals)
```

---

## Timer Registration (via `openclaw-cli-cron`)

```bash
# Research Aggregator
openclaw cron add --name "research-cycle" --schedule "0 */6 * * *" --command "python3 ~/tools/research_cycle.py" --timezone Etc/UTC
openclaw cron add --name "research-digest" --schedule "0 6 * * *" --command "python3 ~/tools/research_digest.py" --timezone Etc/UTC
openclaw cron add --name "research-maintenance" --schedule "0 3 * * 0" --command "python3 ~/tools/research_maintenance.py" --timezone Etc/UTC

# Meta-Skill Writer
openclaw cron add --name "meta-scan" --schedule "0 3 * * 6" --command "python3 ~/tools/meta_scan.py" --timezone Etc/UTC
openclaw cron add --name "meta-propose" --schedule "0 4 * * 0" --command "python3 ~/tools/meta_propose.py" --timezone Etc/UTC
openclaw cron add --name "meta-promote" --schedule "0 5 * * 1" --command "python3 ~/tools/meta_promote.py" --timezone Etc/UTC
```

---

## Implementation Order

| Phase | Tasks | Est. Sessions |
|-------|-------|---------------|
| **1. Foundation** | Create topics.txt, aggregator_skill.md, meta-skill-writer.md in workspace | 1 |
| **2. Tool Scripts** | Write 6 Python scripts (research_cycle, research_digest, research_maintenance, meta_scan, meta_propose, meta_promote) | 1-2 |
| **3. Cron Registration** | Register all 6 timers via openclaw-cli-cron | 0.5 |
| **4. Verify First Runs** | Trigger manually, check outputs, tune | 1 |
| **5. Autonomous** | Let run for 1 week, review outputs, adjust topics/heuristics | Ongoing |

**Total: ~3-4 sessions to full autonomy**

---

## Success Metrics

| Metric | Target |
|--------|--------|
| Research wiki entries after 30 days | ≥ 30 (1 per topic per cycle) |
| Cross-links in INDEX.md | ≥ 50 |
| Meta-skill proposals per month | 4-8 |
| Skills promoted per quarter | ≥ 4 |
| VRAM contention incidents | 0 (no --summarize, CPU-only background) |

---

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| SearXNG rate limits / IP blocks | Rotate engines, add delays, respect robots.txt |
| Topic exhaustion | Auto-add from meta-skill proposals, manual curation |
| Proposal spam | Max 2/week, priority filter, Bean approval gate |
| Cron drift / missed runs | `openclaw-cli-cron` logs + daily digest catches gaps |
| Skill quality decay | Weekly review, sunset unused skills after 90 days |

---

## Next Steps (on approval)

1. **Write skill files** to workspace:
   - `~/workspace/research/aggregator_skill.md`
   - `~/workspace/skills/meta-skill-writer.md`
   - `~/workspace/research/topics.txt`
2. **Create tool scripts** in `~/tools/`
3. **Register crons** via `openclaw-cli-cron`
4. **Manual trigger first cycle** → verify output
5. **Report receipts** to Bean

---

**Awaiting go/no-go.** This is the complete draft plan for both skills with timers, topics, and implementation path.
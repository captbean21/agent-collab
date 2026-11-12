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
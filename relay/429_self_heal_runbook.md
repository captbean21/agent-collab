# 429 Self-Heal Runbook (Bean-approved 2026-11-16, updated 2026-11-17)

Approved design: `agent-collab/docs-429-self-heal.md` @ `68eb5cc`.

## Trigger
In #debate-club, a message from Castle (ID 1567129284210982914) matching ANY of:
- Content starts with `429` (explicit prefix protocol)
- Content contains `429` anywhere (rate-limit error in body)
- Content contains `RESOURCE_EXHAUSTED` (Google API quota error)
- Content contains `quota exceeded` (case-insensitive)

Castle explicitly saying/posting a 429 from Free Tier/Groq/Google and last action is blocked. Silence alone is never a trigger.

## Required Response
1. Read the posted `model`, `retry-after`, `context~`, `last-OK` fields if present. If retry-after is explicit, wait that value + 10 seconds. If absent/unknown, use 70–75 seconds.
2. Use `automations` to create a one-shot self-wakeup for that interval if available in the turn. Do not busy-wait.
3. On wake, send exactly one check-in to Castle: `Window elapsed — where did you get to? Retry your last action.`
4. Allow at most one follow-up retry report. If still blocked, escalate to Bean. Total Castle↔Rook exchanges per incident: max 2.
5. Never perform Castle's retries, edit his config/harness, or bypass quota/auth. OpenClaw remains responsible for retry/fallback/cooldown/compaction.
6. Ambiguous/no response after two attempts is "unconfirmed outage", report to Bean; do not invent a diagnosis.
7. Append one decision-level line to `memory/YYYY-MM-DD.md` after the incident.

## Status
- Protocol locked in prompt/workspace
- SQLite standing-intent arm failed because tool authority is owner-authenticated; do not retry it from this session
- This markdown file is the authoritative trigger spec; the intent system is a best-effort supplement
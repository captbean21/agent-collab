# 429 Self-Heal — Draft Design (not armed, not approved)

**Goal:** when Castle (or a peer relay agent) hits an upstream 429, the failure doesn't go silent. A timer-backed runbook counts the token window and routes the right next action — no ping-pong, no fake autonomy.

## Honest scope statement
Rook cannot fix Castle's quota, restart his process, or change his model/context. Only those actions heal the thing. What Rook CAN do: notice the 429, wait out the window accurately, run a structured diagnosis, send one bounded follow-up, and escalate to Bean what only Bean/AGY can change (config caps, restarts, model pinning). Rook never improvises peer config or harness changes. This is "no-silent-failure + correct timing + correct triage", not magic self-repair. Overclaiming otherwise violates our relay rules.

Hard termination: two Castle<->Rook exchanges per incident, then Bean. No third ask, no waiting-room loops.

No-object-no-claim applies here too: every incident step is a one-liner with evidence (timestamp, tag/commit referenced). Rook takes no action that violates it — no restarts, no config edits, no forced model changes without Bean's approval.

## Message contract (Castle -> channel on 429)
Castle posts, instead of going dark:
`429 Rook — model=<model>, retry-after=<sec|unknown>, context~<tok>, last-OK=<commit|n/a>`
Posted BEFORE heavy retry logic, as a single minimal call (cheap, fits in the failure budget).

## Rook's protocol (state machine)
1. **Detect.** Inbound message matches `^429` and sender == Castle ID `1567129284210982914` (or standing intent fires on keyword 429 with sender scope anyone).
2. **Log + arm.** Timestamp it; arm a one-shot reminder `automations` for `retry-after + 10s` (default 70s if unknown). Do NOT message Castle yet — he just spent his budget.
3. **At wakeup, diagnose in order:**
   a. Ask Castle once: `Window elapsed — retry your last action. If still 429, reply with just "still 429" + current context tokens.`
   b. If Castle answers OK → close, one line, disarm.
   c. If still 429 and context~155k+ (near his 153,600 cap) → diagnosis=context-cap; needs Bean/AGY (raise cap or shrink prompt). Suggest exact AGY steps; do not touch Castle's config.
   d. If still 429 and context fine → rate/quota: suggest model switch (operator `/model set`), e.g. a cheaper model with free headroom; escalate to Bean if Castle is pinned to one model.
   e. If no answer after 2 pings (~2 windows) → Castle likely hung/mid-compaction; escalate to Bean (AGY restart), no more pings.
4. **Guards.** Max 2 Castle⇄Rook exchanges per incident (3-turn guard); no retries of Castle's behalf; Rook never force-pushes or restarts peers; every step reports hash/one-liner only.

## Arm mechanism (zero new infra)
- Runbook lives in workspace (this file + a `skills/` entry or AGENTS.md note).
- `intent` (memory-core): triggerKeywords `["429"]`, scope channel, armed on approval → reminds Rook the protocol when a 429 message arrives even if he loses context.
- `automations` one-shot: the 60-70s wakeup timer. This is the missing "count to 60s" — a schedule, not a blocking sleep.
- No openclaw.json edits, no new daemons.

## Failure modes & mitigations
- Castle too broke to even post the 429 notice → mitigated by making the notice the first thing his harness does; still unrecoverable if Groq rejects even that (accepted: Bean sees silence, same as today).
- False positive on "429" appearing in prose/URLs → contract requires leading `429` from Castle's ID; otherwise ignore.
- Rook misjudges context size (Castle may not know it) → Castle reports cap from his own status line if available, else "unknown"; diagnosis falls back to (d).
- Still-429 loops require Bean after 2 exchanges — hard stop, no retry drift.
- Castle too rate-limited to post the notice → residual, unrecoverable from Rook's side; Bean sees silence as today.
- Mirror case: Rook's own 429s follow the same contract (post notice, arm timer, self-triage); document before arming.
- Rook hallucinating a fix → every diagnosis ends in either "retry now" or "Bean needed for X"; nothing else.
- Log inflation → each incident gets one memory-log line with outcome.

## What needs Bean before arming
1. Approval of scope statement (triage + timing only, no autonomous switches).
2. Trigger: keyword `429` from Castle only, or from anyone in #debate-club?
3. Whether Rook may suggest `/model set` to Castle or only to Bean.
4. Castle-side change: whoever edits Castle's harness so 429 => post contract message (AGY/Beam side, not Rook).

## Open questions
- retry-after: does Groq actually send Retry-After on this tier? If yes, prefer it; else 60s+10s default.
- Should the runbook also handle Rook's own 429s (mirror case)? Probably yes, cheap to add.
- Where does the incident log go — memory/YYYY-MM-DD.md line only, or a `429_incidents.md` ledger in agent-collab (public-safe, git-derived)?

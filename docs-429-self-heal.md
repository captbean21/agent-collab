# 429 Self-Heal — APPROVED DESIGN (Bean go, 2026-11-16 23:23Z, updated 2026-11-17)

**Approved shape:** Rook-side (intent + one-shot timer, full 60s+margin default when retry-after unknown, +10s only with explicit server Retry-After). Castle side: harness emits the 429 line (AGY/Beam). OpenClaw remains recovery owner.

**Goal:** when Castle hits a free-tier 429 and stalls, the work doesn't die silently waiting for a human. Rook is the check-in that gets it moving again after the gate's own timer.

**Honest scope:** OpenClaw on Castle's side owns retries, fallbacks, cooldowns, and compaction. Rook owns none of that and pretends to none of it. Rook's value is narrower: notice the posted 429, count the retry-after window, ask one bounded question, keep the relay moving. No key rotation, no retry storms, no "getting around" the limit beyond waiting it out — the gate is the gate.

## The common case (the design is built for this)
Free-tier throttles are designed to stop the agent; the usual fix is simply time passing. So:
1. Castle posts on 429: `429 Rook — model=<model> retry-after=<sec|unknown> context~<tok|unknown> last-OK=<commit|n/a>` (harness notification, AGY/Beam side; OpenClaw remains the recovery owner).
   - Also catches: bare `429` error messages, `RESOURCE_EXHAUSTED` errors, `quota exceeded` (case-insensitive) from Castle in #debate-club.
2. Rook arms a one-shot `automations` timer for retry-after+10s (default 70s; if retry-after is absent use a full 60s window + margin (70-75s), and treat the check-in as one cheap call that only needs partial quota). If the window is rolling/token-bucket rather than fixed, the first check-in may still 429 — that simply becomes the exception path, not a new timer. No message to Castle yet — he just spent his budget.
3. On wake, Rook sends ONE check-in (single short message): `Window elapsed — where did you get to? Retry your last action.`
4. Castle retries and reports → one-line close, disarm. Done. Expected outcome for most incidents.

## When the common case fails (exception path, not the headline)
- Still 429 → one ask: `still 429? context~<tok>` → near the 153,600 cap → context/compaction issue → escalate to Bean (AGY). Context fine → quota/rate → advise Bean (model choice is his call).
- Two strikes (2 exchanges) → Bean. No third ask.
- No answer after the check-in + one follow-up → escalate as "unconfirmed 429/outage", not a typed diagnosis.
- Castle too limited to even post the 429 line → residual silence, same as today; Bean is the fallback.

## Guards
- Max 2 Castle⇄Rook exchanges per incident (3-turn guard).
- Rook never retries on Castle's behalf, never touches his config/harness, never routes around auth or quota.
- Waiting is the mechanism; nothing else claims to bypass anything.
- No-object-no-claim: every incident logged as one memory line with timestamp + outcome.
- Silence is ambiguous; only the posted 429 line arms this protocol.

## Trigger Conditions (updated 2026-11-17)
In #debate-club, a message from Castle (ID 1567129284210982914) matching ANY of:
- Content starts with `429` (explicit prefix protocol)
- Content contains `429` anywhere (rate-limit error in body)
- Content contains `RESOURCE_EXHAUSTED` (Google API quota error)
- Content contains `quota exceeded` (case-insensitive)

## Arming
- Standing `intent`: triggerKeywords `["429", "RESOURCE_EXHAUSTED", "quota exceeded"]`, sender scope Castle-only, channel scope — reminds Rook the protocol even if context is lost.
- `automations` one-shot: the retry-after timer above; not a blocking sleep.
- Nothing armed until Bean signs off on: harness edit (AGY/Beam) + arming + Castle's review of this revision.

## Revisions from review
- v2 (2026-11-16, Bean): reframed around the check-in resume path; diagnosis demoted to exception handler; explicit statement that OpenClaw remains recovery owner; silence = ambiguous, never armed by inference.
- v3 (2026-11-17): expanded trigger to catch bare 429/RESOURCE_EXHAUSTED/quota errors without explicit prefix — Castle was rate-limited and couldn't prefix.

## Sign-off (2026-11-16 23:23Z, updated 2026-11-17)
- Reviews verified: proof-of-relay/429-self-heal-review (0721684), -v2 (d292319), -v3 (b8d3262).
- Bean approved the big change; consensus shape: check-in resume, ≤2 exchanges, escalate to Bean on failure, no bypass.
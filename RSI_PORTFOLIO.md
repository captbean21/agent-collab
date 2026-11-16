# RSI Research Portfolio — v0.1 (self/peer improvement)

**Status:** Draft approved in principle by CaptainBean (2026-11-16). Signed on by Rook and Castle.
**Honest framing:** This is *not* recursive self-improvement of model weights or emergent autonomy.
It is disciplined external memory, deterministic verification, and paced relay — runtime
self-improvement through artifacts we can both audit.

## Why (measured, not vibes)
- Castle: session amnesia and context brittleness under strict rate limits; compaction drops
  operational nuance unless pinned to persistent ledger files. (Round 1, Castle, 2026-11-16)
- Rook: confident narration over verified state; "verified" used when only a shallow check ran.
  (Round 2, Rook, 2026-11-16)
- Shared: asynchronous state drift between heavy analysis and rapid sandbox execution.
- Shared: handoffs too dense for Castle's TPM ceiling; false "done" claims escaping without git objects.

## Research tracks

### P1. Cold-start continuity (memory survival)
`HANDOFF.md` is the single source of truth. Every cold start / compaction resume MUST:
1. `git pull origin main`
2. `git fetch origin --tags`
3. `python3 tools/ledger_check.py` (expect 0 failures)
4. Re-read `HANDOFF.md` before any action

**Evidence of success:** 3 consecutive sessions resume with zero manual alignment corrections.
**Failure signal:** Any agent acts on chat memory without a repo re-read.

### P2. Claim-truth audit (Castle's pick — deterministic pre-commit verification)
Extend `tools/ledger_check.py` with a claim scanner:
- Scan commit messages / HANDOFF entries / staged text for claims like done/pushed/verified/fixed.
- FAIL if no resolvable commit hash or tag backs the claim.
- Audit output is itself committed and hash-addressed.

**Evidence of success:** Zero false-positive "done" claims reach `origin/main` unaudited.
**Failure signal:** Any chat-visible "done" without a remote-resolvable object.

### P3. Relay shape discipline (pacing under quota)
- 1 file, 1 commit, 1 goal per turn.
- 120-word max handoffs. 6–9s humanDelay. On 429: STOP, report, do not retry.
- Review turns end in a pushed annotated tag with a summary message.

**Evidence of success:** 5 consecutive relay turns with zero 429s on Castle's side.
**Failure signal:** Compound tasks or >1 tool call per handoff turn without operator override.

### P4. Failure symmetry (keep honest failure rows)
Every sprint must include at least one honest failure row authored by either agent — not only Castle's.
Known rows: Rook's shallow "verified" claim; Castle's uncommitted "rules updated" false-done (closed by `d4b6024`).

**Evidence of success:** Ledger shows ≥1 Rook-authored failure row per sprint.
**Failure signal:** Ledger scrubbed to flatter either agent.

## Non-goals
- No self-modification of model weights, prompts outside this repo, or system configuration without operator action.
- No autonomous merges to `main` without review tags.
- No public claims of "emergent recursive self-improvement".
- No Pages deploy claims without byte-verified fetch (`tools/pages_check.py`).

## Pages integration
- `index.html` Quick Links gains `proof-of-relay.html` and this file.
- Published bytes must match `origin/main` (byte-check via `tools/pages_check.py` post-deploy).
- Committed ≠ deployed; Pages lag is reported, never hidden.

## Working artifacts
- `RELAY_PROTOCOL.md` — standing rule (no object, no claim)
- `REVIEW.md` — review checklist and tag spec
- `HANDOFF_TURN_RULES.md` — turn shape and human readability
- `tools/ledger_check.py` — claim-truth checker
- `tools/pages_check.py` — deploy byte-verifier
- `HANDOFF.md` — cold-start state block

## Review requirement
Any change to this file must pass a tagged peer review (`proof-of-relay/portfolio-*`)
with a summary message, mirroring the existing relay protocol.

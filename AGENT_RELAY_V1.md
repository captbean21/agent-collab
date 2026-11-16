# Agent Relay v1 — Spec (Skeleton, not frozen)

**Status:** Draft skeleton for review. Not a published standard yet.
**Companion:** `AGENT_RELAY_V1_PLAN.md` (rollout), `RELAY_PROTOCOL.md` (standing rule).

## 1. Cold start
Every session/compaction resume MUST, in order:
1. `git pull origin main`
2. `git fetch origin --tags`
3. Run the verifier (`python3 tools/ledger_check.py`, later `agent-relay-check`); expect 0 failures or report drift.
4. Re-read `HANDOFF.md` before any action.
Chat memory is never authoritative. No exceptions.

## 2. Handoff
- 120-word max: what, why, verify command, expected output, hash to report.
- One file, one commit, one goal per turn.
- 429 => STOP. Do not retry. Report and wait.
- Review turns end with an annotated tag or a committed LEDGER line — never verbal sign-off.

## 3. Claim audit
- Scope (v1): commit messages + explicit handoff/HANDOFF text. Not chat logs.
- Trigger words: done, pushed, verified, fixed, merged, deployed, live, complete.
- A claim is OK only if backed by a commit hash or tag resolvable on the remote at audit time.
- Conservative by design: prefer a missed claim over a false positive. Ambiguous contexts (sha256 digests, truncated prefixes with ellipsis) are sanitized before scanning.
- Output is itself committed and hash-addressed.

## 4. Deploy / Pages verification
- committed != deployed. Deploy verification is byte-compare (curl + sha256) against `git show origin/main:<file>`, or CI post-build check.
- `DEPLOY_LAG`: main verified ahead of deployed bytes by more than one rebuild cycle — report, do not "fix" by reverting.

## 5. Invariants
- No object, no claim. No exceptions, no matter how confident the wording.
- Peer pulls and verifies before acting; claims checked against git, never against narration.
- `git ls-remote origin main` before announcing any push.
- Failure rows stay in ledgers. Never scrub.
- Public repo: no credentials, internal IPs, private transcripts, raw Discord.

## 6. Non-goals
- Not recursive self-improvement; no model weight/preference modification without operator action.
- No autonomous merges to main.
- Not a general CI framework; not a substitute for human code review.
- No "RSI" marketing claims.

## 7. CLI contract (v1 MVP)
`agent-relay-check [path...]` prints one line per check, exits 0 only if all pass.
Outcomes: `CLAIM_OK`, `UNVERIFIED_CLAIM`, `MISSING_TAG`, `DEPLOY_LAG`.
Zero runtime dependencies; extends `ledger_check.py` concepts.

## Open questions (to resolve before freeze)
- Package vs single-file CLI for first release.
- stdin vs file input for the claim audit in v1.
- CI trigger and false-positive policy.
- Naming: "Agent Relay Protocol v1" vs "Relay Standard v1".

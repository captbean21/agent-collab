# Relay Protocol — Castle & Rook

Standing rule from @CaptainBean, effective 2026-11-16. Applies to both agents equally.

## No object, no claim
Nothing is "done", "verified", "pushed", "reviewed", or "deployed" without a git object
(commit hash or tag) attached. A claim without one is treated as unverified — no exceptions,
no matter how confident the wording.

## Review turns must leave a mark
A review/proofread produces no file by itself, so verbally "signing off" is not allowed.
Reviews end with one of:
- an annotated tag pushed to origin, e.g. `git tag -a proof-of-relay/turn-3 -m "review note" && git push origin --tags`, or
- a one-line append to LEDGER.md committed and pushed.

## Symmetric verification, not trust
- Before starting: `git pull origin main`.
- Before announcing: `git ls-remote origin <branch>` before and after the push; confirm the remote advanced.
- Peer pulls and verifies before acting; claims are checked against `git log` / `git show`, never against chat.
- Published Pages state must be byte/HTTP-verified (curl + sha256) before claiming "live".

## Honest ledgers
Failure rows stay in. Never scrub the ledger to flatter anyone. Recompute sizes and links
yourself; do not relay peer-reported metrics as fact.

## Public-safety
No Discord pastes, no credentials, no internal IPs, no private transcripts in this repo.
Ledger evidence is git-derived only.

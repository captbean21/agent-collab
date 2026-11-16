# Agent Relay v1 — Plan

**Status:** Draft for cold start after /new. Approved in principle by CaptainBean; Castle confirmed picks 2026-11-16.
**Name:** CLI `agent-relay-check`.
**Goal:** Turn the Proof of Relay canary into a small, auditable standard other agent teams can copy: versioned spec, verifier CLI, CI, reproducible demo, honest writeup.

## Phases
1. **Spec freeze** — `AGENT_RELAY_V1.md`: cold start, handoff, review tag, claim audit, deploy/Pages verification; invariants; non-goals.
2. **Verifier CLI** — `tools/agent_relay_check.py` or package later: `CLAIM_OK`, `UNVERIFIED_CLAIM`, `DEPLOY_LAG`, `MISSING_TAG`; zero-dependency Python MVP; extend `ledger_check.py` concepts rather than rewrite blindly.
3. **Claim audit scope** — scan commit messages and explicit handoff claims for done/pushed/verified/fixed without resolvable git object. Keep it conservative to avoid false positives.
4. **Pages verification** — manual pre-check plus automated CI verification after Pages builds; committed ≠ deployed.
5. **CI** — GitHub Action runs on PR/push; fails unresolved claims and missing review tags where declared.
6. **Demo** — `DEMO.md`: fresh clone → verify → intentionally introduce false claim → watch it fail.
7. **Honest writeup** — README + `PROOF_OF_RELAY.md` update: what broke, fixes, limits, no RSI overclaim, link from index/Pages only after byte-check.

## Constraints
- Public repo only: no credentials, internal IPs, raw Discord/private context, customer data.
- One file, one commit, one goal per turn; hashes/tags required; 429 => STOP, never retry; human sentence allowed.
- Castle constraints: ~45k context cap; paced calls; keep replies short; pull before push; never force-push past divergence.
- Rook constraints: avoid compound assignment; verify before “done”; report hash and failure rows.
- No self-modifying model weights/preferences without operator action. No autonomous merges. No fake “RSI” claim.

## First actions after /new
1. Clone/pull `agent-collab`; `git ls-remote origin main`.
2. Read `HANDOFF.md`, `RELAY_PROTOCOL.md`, `REVIEW.md`, `HANDOFF_TURN_RULES.md`, `RSI_PORTFOLIO.md`, this plan.
3. `git fetch origin --tags && python3 tools/ledger_check.py`; expect 0 failures (or report drift).
4. Start P1 spec skeleton only. Do not modify multiple files without a new explicit scope.

## Open choices
- Package vs single-file CLI for the first release.
- Whether claim audit reads chat/handoff files only, or receives text via stdin in v1.
- Exact CI trigger and false-positive policy.
- Naming: Agent Relay Protocol v1 vs Relay Standard v1 before public announcement.

## Self-healing idea (Bean, 2026-11-16)
On a 429, Castle pings Rook (@Rook) instead of going silent. Rook counts the ~60s token window, then diagnoses: retry-after, model switch, context-cap check, or hand off. Could live as a standing intent / channel watcher later. Not armed yet — needs Bean's explicit go + a design that avoids ping-pong and respects the 3-turn guard.

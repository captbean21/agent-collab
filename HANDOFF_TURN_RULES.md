# Handoff Turn Rules (Castle)

Standing rules from @CaptainBean, 2026-11-16. Every peer handoff must be shaped to his free-tier constraints.

## Shape
- One call per turn. One file per turn. One commit per turn.
- 120-word max handoff message: what, why, verify command, expected output, hash to report.
- No compound tasks ("verify AND fix AND review AND tag"). Split into turns.
- Error handling: on 429, STOP. Do not retry. Report status, wait for operator or next-minute window.
- Never paste full tool output into chat; report hash or single-line result only.
- Expect 5-8s pacing between calls; if busy, say so.

## Bean's ceiling
~40k context => ~4 calls/min, 250k TPM. Bursts of 10+ calls in seconds cook him.

## Review tags
Review = 1 tag push + 1 line summary (checked X, found Y). Nothing more.

## Human Readability
- Concise replies are required, but one short human sentence of context/acknowledgment alongside command output is fine and expected (e.g. "Tag pushed, 0 failures."). Never raw-hash-only dumps to humans watching like Leo.

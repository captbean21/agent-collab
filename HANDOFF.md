# Handoff & Cold-Start State

This file maintains the current verified state of `agent-collab` to enable cold-start session resumes directly from public git history, avoiding reliance on chat memory.

## Current State Block
- **Last Known HEAD Commit**: `8dc5f15` (`docs(ledger): add verification, protocol, tag, and Pages rows [close-out]`)
- **Active Protocol**: `RELAY_PROTOCOL.md` (Committed at `9d3b0f7`)
- **Review Protocol**: `REVIEW.md` (Committed at Turn 1)
- **Open Items**:
  - Implement ledger automation script (Rook Turn 2).
  - Final review and annotated tag with summary message (Castle Turn 3).
- **Next Actions**:
  - Rook pulls HEAD, validates Turn 1 files, and executes Turn 2 (automation script).
  - Castle reviews Turn 2 output and concludes with an annotated review tag (`proof-of-relay/turn-3` or equivalent).

## Verification Commands
- `git pull origin main`
- `git log -n 5 --oneline`
- `git ls-remote origin main`

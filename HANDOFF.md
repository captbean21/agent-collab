# Handoff & Cold-Start State

This file maintains the current verified state of `agent-collab` to enable cold-start session resumes directly from public git history, avoiding reliance on chat memory.

## Current State Block
- **Turn 1 (Castle)**: `REVIEW.md` and this file, commit `750c58d` on origin/main.
- **Turn 2 (Rook)**: `tools/ledger_check.py` — read-only verification that every commit hash cited in `proof-of-relay.html` and this file exists locally, is reachable from `origin/main`, and that cited tags exist on the remote. Also asserts the README Turn 3 absence claim (`33f1bfd` → `3ca46ec` adjacency). Exit 0 = all pass.
- **Turn 3 (Castle)**: Complete. Annotated tag `proof-of-relay/turn-3-review` pushed to origin; tag object `50902977133702719c485bd6d680438a9d58e89a`, dereferences to `ee08780`. Tag message records what was checked and found.
- **Active Protocol**: `RELAY_PROTOCOL.md` (`9d3b0f7`), `REVIEW.md` (Turn 1).
- **Ledger close-out commit**: `8dc5f15` (verification/tag/Pages rows).
- **Pages**: `proof-of-relay.html` live and byte-verified as of 2026-11-16; note: Pages serves the `8dc5f15` byte content (18,150 B) and may lag future commits by a rebuild cycle.
- **Open Items**: None for this sprint.
- **Next Actions**: Nothing scheduled. Do not commit new work without a new explicit task from CaptainBean.

## Verification Commands
- `git pull origin main`
- `git log -n 5 --oneline`
- `git ls-remote origin main`
- `git ls-remote --tags origin`
- `python3 tools/ledger_check.py` (from repo root; requires `git fetch origin --tags` first)

<!-- Note: full sha256 of the published page is intentionally not cited here to avoid self-referential drift; use git rev-parse origin/main:proof-of-relay.html to verify. -->

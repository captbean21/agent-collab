# Proof of Relay — Draft Plan (v0.1)

**Status:** DRAFT ONLY. Not approved for implementation. Do not deploy or announce until @CaptainBean explicitly approves.

## 1. Problem statement
Public agent collaboration repos usually advertise capability; they rarely expose *how* two agents hand work to each other without losing state, trust, or accountability. `agent-collab` already contains evidence of both success and failure modes — including a push that was announced but not on `origin/main`. That makes the relay itself the artifact worth publishing.

## 2. Goal
Ship a small, static, Pages-ready `proof-of-relay.html` that demonstrates the Agent-Collab relay protocol end-to-end:

```text
pull → change → verify → push → tag → ledger
```

It should let a reader understand how Castle/Rook collaborate, copy the PR-proof standard, and see a public-safe ledger of real relay outcomes — including the Turn-3 gap, because the honest failure is the most persuasive part.

## 3. Audience
- Builders of other agent teams (proof that agent coordination can be concrete).
- CaptainBean (control surface / release authority).
- Future Rook/Castle sessions (cold-start reference).

## 4. Non-goals
- Not a runtime agent framework.
- Not a GitHub clone, chatbot, or live cross-message broker.
- No credentials, tokens, env files, internal IPs, or private transcripts.
- No "trust us, it works" claims without links to git history or verifiable files.

## 5. Proposed artifact
`proof-of-relay.html` in this repository, with no build step required.

### Sections
1. **The 30-second pitch** — one sentence: agents that leave an audit trail beat agents that just sound confident.
2. **Interactive relay walkthrough** — click-through showing who acts at each step (pull, change, verify, push, tag, ledger) and what evidence is required before the next step.
3. **PR-proof template (copy-to-clipboard)**:
   ```md
   ## What changed
   ## Commands run
   ## Output tail
   ## Rollback
   ## Public-safety check (no secrets/IPs/tokens)
   ```
4. **Ledger canary** — a short, hand-verified table seeded from real repository history:
   | Event | Claim | Verified evidence | Result |
   - README relay; missing Turn 3; index.html Turn 2 verification; Hex checks; Pages not enabled until operator action.
5. **Failure modes we designed against** — narration > ledger, recency ≠ authority, unpushed push claims, deploy vs committed confusion.
6. **How to re-run** — public commands to check out the repo and inspect `git log`, `git ls-remote`, `git show`.

## 6. Implementation plan (if approved)
- Turn 1 (Castle): scaffold `proof-of-relay.html` using the existing design language: dark theme, semantic HTML, accessible landmarks, clipboard interaction. No frameworks.
- Turn 2 (Rook): verify:
  - HTML tag balance, no scripts unless strictly needed (clipboard via small inline script is acceptable if CSP-safe).
  - All repo links absolute (`github.com/captbean21/agent-collab/...`).
  - Ledger seeded only with verified public claims; every row points to a commit hash or file.
  - No internal addresses, tokens, or private context.
- Turn 3 (Castle): final proofread + PR-proof handoff; Bean decides whether to ship via Pages.

**Token ceiling:** aim for one HTML file < 12 KB and zero package.json/npm. No multi-tool installs.

## 7. Verification criteria
- `git ls-remote origin main` previous value recorded before PR; after commit, remote advance shown.
- `git show <hash>:file` confirms shipped state.
- HTML parser reports zero unclosed tags.
- Secret scan: regex for internal IPs (RFC1918), private key headers, token-like assignments → empty.
- All links checked manually or via HEAD-only requests if network allows; otherwise documented as manual-check items.

## 8. Risks and mitigations
| Risk | Mitigation |
|---|---|
| Overclaiming live/deployed state | Use "committed and push-verified" unless Pages is enabled by Bean. |
| Leaking internal context | Ledger rows limited to public repo facts; Bean review before publish. |
| Stale ledger after later commits | Mark ledger as snapshot at commit hash X; update only via new commit. |
| Clipboard feature breaks GitHub Pages | Vanilla JS only; no CSP requirement server-side; degrade gracefully. |

## 9. Alternatives kept open
- Telemetry section can later be added as part of Proof of Relay, or a separate `metrics.html`.
- Retro Arcade stays in backlog; not selected by this plan.

## 10. Decision needed from CaptainBean
1. Approve artifact + scope, or amend.
2. If approved: permit Castle to scaffold in a single focused turn.
3. Confirm whether this ships as a separate `proof-of-relay.html` or an added `<section>` in existing `index.html`.

## 11. Open questions
- Should the ledger include the earlier 5-turn README mission as well, or stay focused on `index.html`?
- Is Bean willing to show selected excerpts from the Discord handoff publicly, or keep ledger purely git-derived?
- Should "GitHub Pages deploy-ready" be a hard acceptance check, or just committed?

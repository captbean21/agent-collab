# Claude Code Quota Survival Guide (Claude Pro Edition)

> Practical protocols to keep Claude Code deeply productive on a $20/mo Claude Pro subscription without exhausting the rolling 5-hour rate limits.

---

## 1. Why Claude Code Burns Pro Quotas in 20 Minutes

On Claude Pro, usage is metered on a **rolling 5-hour window**. Because Claude Code re-submits previous turns and tool execution outputs on every new user message:
- Turn 1: 2,000 tokens
- Turn 10: 15,000 tokens
- Turn 30: 45,000 tokens
- Turn 50: 80,000+ tokens

By turn 30, **every single command you send re-ingests tens of thousands of tokens**. If an unconstrained bash command dumps 2,000 lines of logs, that dump stays in context permanently for the rest of the conversation.

---

## 2. Drop `CLAUDE.md` in Your Project Root

Claude Code automatically reads `CLAUDE.md` on startup. This anchors defensive token behaviors:

```markdown
# Project Rules & Token-Defensive Protocol

## Communication Style
- Keep responses concise. No conversational fluff or verbose preamble.
- Output diffs or targeted code snippets rather than rewriting whole files.
- If unsure, ask one clarifying question instead of speculating across multiple turns.

## Tool & Output Discipline (Quota Conservation)
- NEVER run unrestricted search or test commands that dump large outputs.
- Cap all terminal outputs: use `| head -n 30` or `| tail -n 30`.
- When searching files, ALWAYS exclude build directories, caches, and vendor folders:
  - Exclude: `.git`, `node_modules`, `dist`, `build`, `venv`, `target`, `__pycache__`.
- When reading code, prefer reading specific line ranges over reading entire large files.
- Run targeted tests only (single test file or test case), never full end-to-end suites in chat.

## State Discipline
- Before ending a major milestone or when asked to sync state, update `STATE.md`.
- Read `STATE.md` on session start to restore context without re-reading the whole repository.
```

---

## 3. The `STATE.md` + `/clear` Pattern (The Ultimate Quota Saver)

Instead of maintaining a 3-hour marathon chat:

1. Work on a task for 5–8 turns.
2. Ask Claude: `"Update STATE.md with our progress and next steps."`
3. Run: `/clear` (wipes the bloated context history).
4. Resume: `"Read STATE.md and start the next immediate task."`

Context drops from 60,000 tokens back down to 2,000 tokens. You use ~95% fewer tokens per turn.

### `STATE.md` Template
```markdown
# Project State & Handoff

## Current Focus
- [Brief 1-sentence goal of current milestone]

## Architecture & Decisions
- [Key design choices made, libraries chosen, ports/endpoints]

## Completed This Session
- [x] Feature A implemented (path/to/file.ts)
- [x] Bug fix verified via unit test

## Next Immediate Steps
1. Implement endpoint B in `server.py`
2. Add migration script for database schema

## Verification Commands
- `npm test tests/unit/feature-a.test.ts`
- `npm run build`
```

---

## 4. Terminal Command Blast-Radius Table

| Uncapped Command (Burns Quota) | Defensive Replacement | Reason |
|---|---|---|
| `git diff` | `git diff --stat` | Full diffs dump entire files into context |
| `git log` | `git log -n 5 --oneline` | Caps history to 5 short lines |
| `npm test` | `npm test -- tests/foo.test.ts` | Targeted tests avoid log spam |
| `grep -r "pattern" .` | `rg -g '!{node_modules,dist}' "pattern"` | Excludes dependencies & build artifacts |
| `cat large_file.json` | `head -n 30 large_file.json` | Inspects safely without token dump |

---

## 5. Thinking Mode & User Habits

- **Thinking Mode:** Keep thinking mode **OFF** for standard edits, bug fixes, and boilerplate (`/thinking off`). Reserve extended thinking **only** for system architecture or complex algorithm planning.
- **Batch Requests:** Provide a full 1-paragraph spec instead of 5 incremental micro-prompts.
- **Paste Error Snippets:** Paste only the relevant 10-line traceback, not 300 lines of compilation output.
- **Cancel Runaway Streams:** Hit `Ctrl+C` immediately if a tool begins streaming massive log outputs.
- **Compact Early:** Use `/compact` before the system forces truncation.

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

---

## 6. Battle-Tested Lessons from Real Homelab Ops

These are direct, concrete discoveries from running continuous autonomous agent clusters:

1. **The 16k Context Tax (Tool Schema Overhead):**  
   Claude Code injects tool schemas (bash, edit, read, grep, git, lsp) into the system prompt. Even before you type turn #1, your session is sitting on **~10,000 to 16,000 preloaded tokens**. You never start at zero, so your headroom before hitting the 5-hour cutoff is narrower than expected.
2. **Whole-File Rewrites Burn Output Quotas 10x Faster:**  
   Output tokens carry a 3x–5x penalty against rate limits compared to input tokens. If Claude rewrites an entire 400-line file to change one line, you burn ~2,000 output tokens. Explicitly instruct it: *"Make surgical, targeted block edits only — never rewrite whole files."*
3. **"No Object, No Claim" (Stop Hallucination Spirals):**  
   Never let Claude say *"I completed the fix"* without running a verification command (`npm test -- <path>` or `tsc --noEmit`) in the exact same turn. If it doesn't verify, you end up doing 3 follow-up turns diagnosing hallucinations.
4. **Why `/clear` + `STATE.md` Beats `/compact`:**  
   Auto-compaction (`/compact`) is lossy—it strips away specific variable names, line numbers, and file paths. By turn 40, Claude gets "brain fog". A hard `/clear` paired with a crisp 20-line `STATE.md` gives you a 100% fresh, sharp model with zero token bloat.
5. **The Log-Dump Poison Pill:**  
   One noisy `npm install`, `pip install`, or `cargo build` dumping 400 lines of progress bars permanently poisons your conversation context for every message that follows. Always use quiet flags (`npm i --silent`) or pipe through `| tail -n 25`.
6. **The Zombie Process Trap:**  
   Background servers or hanging test processes can hold file locks or saturate CPU, causing subsequent tool calls to time out. Always wrap test commands with a timeout guard (e.g., `timeout 30s npm test`).


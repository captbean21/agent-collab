# Spike: Session Continuity Bridge Daemon

## Question
Can a lightweight Python daemon persist agent session state (task list, decisions, recent diffs) to a local git-backed store and restore it on cold start, eliminating the "blank slate" problem after compaction or `/new`?

## Approach
- Daemon watches OpenClaw workspace for session changes (file writes, git commits)
- Maintains a rolling `.claude/state/` directory with: `tasks.json`, `decisions.json`, `recent_diffs.patch`
- On new session start, a `restore.py` script loads the latest state and injects it into the agent's context
- Zero external deps, pure Python, runs as background process

## Success Criteria
- Daemon starts/stops cleanly
- State persists across process restarts
- Restore script outputs valid context injection format
- < 50ms overhead per write operation
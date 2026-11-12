#!/usr/bin/env python3
"""
Session Continuity Restore Script
Loads persisted state and outputs context injection for new sessions.
"""
import json
import sys
from pathlib import Path
from datetime import datetime

WORKSPACE = Path("/home/rook/.openclaw/workspace")
STATE_DIR = WORKSPACE / ".claude" / "state"

TASKS_FILE = STATE_DIR / "tasks.json"
DECISIONS_FILE = STATE_DIR / "decisions.json"
DIFFS_FILE = STATE_DIR / "recent_diffs.patch"
METADATA_FILE = STATE_DIR / "metadata.json"

def load_state():
    """Load all persisted state files."""
    state = {
        "tasks": [],
        "decisions": [],
        "diffs": "",
        "metadata": {}
    }
    
    if TASKS_FILE.exists():
        with open(TASKS_FILE) as f:
            state["tasks"] = json.load(f)
    
    if DECISIONS_FILE.exists():
        with open(DECISIONS_FILE) as f:
            state["decisions"] = json.load(f)
    
    if DIFFS_FILE.exists():
        state["diffs"] = DIFFS_FILE.read_text()
    
    if METADATA_FILE.exists():
        with open(METADATA_FILE) as f:
            state["metadata"] = json.load(f)
    
    return state

def format_context_injection(state):
    """Format state as context injection for agent."""
    lines = []
    lines.append("=== SESSION CONTINUITY RESTORE ===")
    lines.append(f"Restored: {state['metadata'].get('last_capture', 'unknown')}")
    lines.append(f"Tasks: {len(state['tasks'])}, Decisions: {len(state['decisions'])}")
    lines.append("")
    
    if state["tasks"]:
        lines.append("## Recent Tasks & Context")
        for task in state["tasks"][-10:]:
            source = task.get("source", "unknown")
            text = task.get("text", "")[:200]
            lines.append(f"- [{source}] {text}")
        lines.append("")
    
    if state["decisions"]:
        lines.append("## Key Decisions & Commits")
        for decision in state["decisions"][-10:]:
            source = decision.get("source", "unknown")
            text = decision.get("text", "")[:200]
            lines.append(f"- [{source}] {text}")
        lines.append("")
    
    if state["diffs"]:
        lines.append("## Recent Changes (git diff --stat)")
        lines.append(state["diffs"][:1000])
        lines.append("")
    
    lines.append("=== END RESTORE ===")
    return "\n".join(lines)

def main():
    if not STATE_DIR.exists():
        print("No continuity state found.", file=sys.stderr)
        sys.exit(1)
    
    state = load_state()
    output = format_context_injection(state)
    print(output)
    
    # Also write to a temp file for easy sourcing
    import tempfile
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, prefix="continuity_restore_") as f:
        f.write(output)
        print(f"\n# Full restore written to: {f.name}", file=sys.stderr)

if __name__ == "__main__":
    main()
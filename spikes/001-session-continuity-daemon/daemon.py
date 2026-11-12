#!/usr/bin/env python3
"""
Session Continuity Bridge Daemon
Watches workspace for changes and persists state to git-backed store.
"""
import json
import os
import subprocess
import sys
import time
import threading
from datetime import datetime
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WORKSPACE = Path("/home/rook/.openclaw/workspace")
STATE_DIR = WORKSPACE / ".claude" / "state"
STATE_DIR.mkdir(parents=True, exist_ok=True)

TASKS_FILE = STATE_DIR / "tasks.json"
DECISIONS_FILE = STATE_DIR / "decisions.json"
DIFFS_FILE = STATE_DIR / "recent_diffs.patch"
METADATA_FILE = STATE_DIR / "metadata.json"

EXCLUDED_PARTS = {".claude", ".git", "logs", "__pycache__", "node_modules"}

class WorkspaceHandler(FileSystemEventHandler):
    def __init__(self, daemon):
        self.daemon = daemon
        self.last_write = 0

    def on_modified(self, event):
        if event.is_directory:
            return
        # Debounce rapid writes
        now = time.time()
        if now - self.last_write < 5.0:
            return
        self.last_write = now

        # Check if it's a relevant file
        path = Path(event.src_path)
        if self._is_relevant(path):
            self.daemon.capture_state()

    def _is_relevant(self, path):
        try:
            rel = path.relative_to(WORKSPACE)
        except ValueError:
            return False
        # Never react to the daemon's own output or VCS internals
        if any(part in EXCLUDED_PARTS for part in rel.parts):
            return False
        relevant_patterns = [
            "AGENTS.md", "SOUL.md", "IDENTITY.md",
            "tasks/", "memory/", "spikes/",
            "*.py", "*.md", "*.json", "*.yaml", "*.yml"
        ]
        return any(rel.match(p) or p in str(rel) for p in relevant_patterns)

class ContinuityDaemon:
    def __init__(self):
        self.observer = None
        self.running = False
        self.last_capture = 0
    
    def capture_state(self):
        """Capture current workspace state."""
        now = time.time()
        if now - self.last_capture < 2:  # Throttle captures
            return
        self.last_capture = now
        
        print(f"[{datetime.now().isoformat()}] Capturing state...")
        
        # Capture tasks from AGENTS.md, memory files, etc.
        tasks = self._extract_tasks()
        with open(TASKS_FILE, "w") as f:
            json.dump(tasks, f, indent=2)
        
        # Capture decisions (from memory logs, recent commits)
        decisions = self._extract_decisions()
        with open(DECISIONS_FILE, "w") as f:
            json.dump(decisions, f, indent=2)
        
        # Capture recent git diffs
        diffs = self._get_recent_diffs()
        with open(DIFFS_FILE, "w") as f:
            f.write(diffs)
        
        # Update metadata
        metadata = {
            "last_capture": datetime.now().isoformat(),
            "workspace": str(WORKSPACE),
            "tasks_count": len(tasks),
            "decisions_count": len(decisions),
        }
        with open(METADATA_FILE, "w") as f:
            json.dump(metadata, f, indent=2)
        
        # Commit to git
        self._git_commit()
        
        print(f"  Tasks: {len(tasks)}, Decisions: {len(decisions)}, Diff chars: {len(diffs)}")
    
    def _extract_tasks(self):
        """Extract task-like items from workspace."""
        tasks = []
        
        # From AGENTS.md
        agents_md = WORKSPACE / "AGENTS.md"
        if agents_md.exists():
            content = agents_md.read_text()
            for line in content.split("\n"):
                if "- [ ]" in line or "- [x]" in line or "TODO:" in line.upper():
                    tasks.append({"source": "AGENTS.md", "text": line.strip(), "captured": datetime.now().isoformat()})
        
        # From memory files
        memory_dir = WORKSPACE / "memory"
        if memory_dir.exists():
            for md_file in sorted(memory_dir.glob("*.md"))[-3:]:  # Last 3 days
                content = md_file.read_text()
                for line in content.split("\n"):
                    if line.strip().startswith("- ") and len(line) > 20:
                        tasks.append({"source": f"memory/{md_file.name}", "text": line.strip(), "captured": datetime.now().isoformat()})
        
        # From spike READMEs
        spikes_dir = WORKSPACE / "spikes"
        if spikes_dir.exists():
            for spike_dir in spikes_dir.iterdir():
                readme = spike_dir / "README.md"
                if readme.exists():
                    tasks.append({"source": f"spikes/{spike_dir.name}", "text": readme.read_text()[:200], "captured": datetime.now().isoformat()})
        
        return tasks[-50:]  # Keep last 50
    
    def _extract_decisions(self):
        """Extract decision-like items."""
        decisions = []
        
        # From memory files (look for decision markers)
        memory_dir = WORKSPACE / "memory"
        if memory_dir.exists():
            for md_file in sorted(memory_dir.glob("*.md"))[-5:]:
                content = md_file.read_text()
                for line in content.split("\n"):
                    if any(kw in line.lower() for kw in ["decided", "chosen", "selected", "verdict:", "recommendation:"]):
                        decisions.append({"source": f"memory/{md_file.name}", "text": line.strip(), "captured": datetime.now().isoformat()})
        
        # From git commit messages (recent)
        try:
            result = subprocess.run(
                ["git", "-C", str(WORKSPACE), "log", "--oneline", "-10", "--pretty=format:%h %s"],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    if line:
                        decisions.append({"source": "git", "text": line.strip(), "captured": datetime.now().isoformat()})
        except Exception:
            pass
        
        return decisions[-30:]
    
    def _get_recent_diffs(self):
        """Get recent git diffs."""
        try:
            result = subprocess.run(
                ["git", "-C", str(WORKSPACE), "diff", "HEAD~3..HEAD", "--stat"],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                return result.stdout
        except Exception:
            pass
        return ""
    
    def _git_commit(self):
        """Commit state changes to git (skips when nothing changed)."""
        try:
            subprocess.run(["git", "-C", str(WORKSPACE), "add", str(STATE_DIR.relative_to(WORKSPACE))],
                          capture_output=True, timeout=5)
            diff = subprocess.run(["git", "-C", str(WORKSPACE), "diff", "--cached", "--quiet"],
                                  capture_output=True, timeout=5)
            if diff.returncode == 0:
                print("  No state changes; skipping commit")
                return
            subprocess.run(["git", "-C", str(WORKSPACE), "commit", "-m", f"continuity: state capture {datetime.now().isoformat()}"],
                          capture_output=True, timeout=5)
            # Prune old continuity commits weekly (keep last 50)
            subprocess.run(["git", "-C", str(WORKSPACE), "gc", "--auto"], capture_output=True, timeout=10)
            subprocess.run(["git", "-C", str(WORKSPACE), "reflog", "expire", "--expire=7.days.ago", "--all"], capture_output=True, timeout=5)
        except Exception:
            pass
    
    def start(self):
        """Start the daemon."""
        if self.running:
            return
        self.running = True
        
        # Initial capture
        self.capture_state()
        
        # Start file watcher
        self.observer = Observer()
        handler = WorkspaceHandler(self)
        self.observer.schedule(handler, str(WORKSPACE), recursive=True)
        self.observer.start()
        
        print(f"[{datetime.now().isoformat()}] Daemon started, watching {WORKSPACE}")
        
        try:
            while self.running:
                time.sleep(300)
                # Periodic capture (every 5 minutes, throttled internally)
                self.capture_state()
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Stop the daemon."""
        self.running = False
        if self.observer:
            self.observer.stop()
            self.observer.join()
        print(f"[{datetime.now().isoformat()}] Daemon stopped")

def run_daemon(daemon, pid_file=None):
    """Run daemon with optional PID file."""
    if pid_file:
        try:
            with open(pid_file, "w") as f:
                f.write(str(os.getpid()))
        except Exception as e:
            print(f"Failed to write PID file: {e}", file=sys.stderr)
    
    try:
        daemon.start()
    finally:
        if pid_file and os.path.exists(pid_file):
            os.remove(pid_file)

if __name__ == "__main__":
    import os
    daemon = ContinuityDaemon()
    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        daemon.capture_state()
    elif len(sys.argv) > 1 and sys.argv[1] == "--daemon":
        pid_file = sys.argv[2] if len(sys.argv) > 2 else "/tmp/session-continuity-daemon.pid"
        run_daemon(daemon, pid_file)
    else:
        daemon.start()
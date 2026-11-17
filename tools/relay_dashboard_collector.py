#!/usr/bin/env python3
"""
Relay Dashboard Collector — Round 4
Polls all metric sources and writes data/relay-metrics.json with rolling history.
Zero dependencies beyond stdlib + gh CLI (for GitHub API).
"""

import json
import subprocess
import sys
import os
from datetime import datetime, timezone, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DATA_DIR = REPO_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)
METRICS_FILE = DATA_DIR / "relay-metrics.json"
MAX_HISTORY = 100  # Keep last 100 snapshots

def run_cmd(cmd, cwd=None, timeout=10):
    """Run command, return (success, stdout, stderr)."""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True,
            cwd=cwd or REPO_ROOT, timeout=timeout
        )
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return False, "", "timeout"
    except Exception as e:
        return False, "", str(e)

def parse_pages_check():
    """Run tools/pages_check.py and parse JSON output."""
    ok, out, err = run_cmd("python3 tools/pages_check.py --json")
    if not ok:
        return {"status": "ERROR", "error": err or "pages_check failed"}
    try:
        data = json.loads(out)
        return {
            "status": data.get("status", "UNKNOWN"),
            "deploy_lag_seconds": data.get("deploy_lag_seconds"),
            "last_commit_sha": data.get("commit_sha", "")[:7],
            "pages_url": data.get("pages_url", "https://captbean21.github.io/agent-collab/")
        }
    except json.JSONDecodeError:
        return {"status": "PARSE_ERROR", "error": "invalid JSON from pages_check"}

def parse_ledger_check():
    """Run tools/ledger_check.py and parse JSON output."""
    ok, out, err = run_cmd("python3 tools/ledger_check.py --json")
    if not ok:
        return {"total_checked": 0, "claim_ok": 0, "unverified_claim": 0, "missing_tag": 0, "error": err}
    try:
        data = json.loads(out)
        return {
            "total_checked": data.get("total", 0),
            "claim_ok": data.get("claim_ok", 0),
            "unverified_claim": data.get("unverified_claim", 0),
            "missing_tag": data.get("missing_tag", 0),
            "last_checked_commit": data.get("last_commit", "")[:7]
        }
    except json.JSONDecodeError:
        return {"total_checked": 0, "claim_ok": 0, "unverified_claim": 0, "missing_tag": 0, "error": "invalid JSON"}

def get_429_events():
    """Count 429 events from git log (last 24h)."""
    since = (datetime.now(timezone.utc) - timedelta(hours=24)).strftime("%Y-%m-%d")
    ok, out, err = run_cmd(f'git log --since="{since}" --grep="429" --oneline')
    if not ok:
        return {"events_24h": 0, "last_event": None, "status": "ERROR", "error": err}
    lines = out.strip().split("\n") if out.strip() else []
    count = len(lines)
    last_event = None
    if lines:
        last_event = datetime.now(timezone.utc).isoformat()
    status = "HEALTHY" if count == 0 else ("ELEVATED" if count <= 2 else "CRITICAL")
    return {"events_24h": count, "last_event": last_event, "status": status}

def get_deploy_lag():
    """Get deploy lag from GitHub API: commit timestamp vs Pages deploy."""
    ok, out, err = run_cmd('git log -1 --format="%ct"')
    if not ok:
        return None
    try:
        commit_ts = int(out.strip())
        commit_dt = datetime.fromtimestamp(commit_ts, tz=timezone.utc)
        return commit_dt.isoformat()
    except ValueError:
        return None

def get_handoff_turns():
    """Parse HANDOFF.md for handoff turn count."""
    handoff_path = REPO_ROOT / "HANDOFF.md"
    if not handoff_path.exists():
        return {"total_turns": 0, "last_turn": None, "last_commit": None}
    try:
        content = handoff_path.read_text()
        import re
        turns = re.findall(r"Turn\s+(\d+)", content, re.IGNORECASE)
        total = len(set(turns))
        last_turn = f"Turn {max(map(int, turns))}" if turns else None
        ok, out, err = run_cmd('git log -1 --format="%h" -- HANDOFF.md')
        last_commit = out.strip() if ok else None
        return {"total_turns": total, "last_turn": last_turn, "last_commit": last_commit}
    except Exception:
        return {"total_turns": 0, "last_turn": None, "last_commit": None}

def load_existing_metrics():
    """Load existing metrics file to preserve history."""
    if METRICS_FILE.exists():
        try:
            return json.loads(METRICS_FILE.read_text())
        except json.JSONDecodeError:
            pass
    return {"history": []}

def main():
    print("🔄 Collecting relay metrics...")

    pages = parse_pages_check()
    print(f"  Pages: {pages.get('status')}")

    claims = parse_ledger_check()
    print(f"  Claims: {claims.get('claim_ok')}/{claims.get('total_checked')} OK")

    rate_limits = get_429_events()
    print(f"  429 events (24h): {rate_limits.get('events_24h')} ({rate_limits.get('status')})")

    handoffs = get_handoff_turns()
    print(f"  Handoff turns: {handoffs.get('total_turns')}")

    deploy_lag_commit = get_deploy_lag()

    # Load existing metrics for history
    existing = load_existing_metrics()
    history = existing.get("history", [])

    # Build current snapshot
    timestamp = datetime.now(timezone.utc).isoformat()
    current = {
        "timestamp": timestamp,
        "pages": pages,
        "claims": claims,
        "rate_limits": rate_limits,
        "handoffs": handoffs,
        "deploy_lag_commit_timestamp": deploy_lag_commit
    }

    # Add minimal history entry (for sparklines)
    history.append({
        "timestamp": timestamp,
        "events_24h": rate_limits.get("events_24h", 0),
        "deploy_lag": pages.get("deploy_lag_seconds", 0) or 0,
        "claim_ok": claims.get("claim_ok", 0),
        "pages_status": pages.get("status", "UNKNOWN"),
        "handoff_turns": handoffs.get("total_turns", 0)
    })

    # Trim history
    if len(history) > MAX_HISTORY:
        history = history[-MAX_HISTORY:]

    # Final metrics object
    metrics = {**current, "history": history}

    METRICS_FILE.write_text(json.dumps(metrics, indent=2))
    print(f"✅ Written to {METRICS_FILE} (history: {len(history)} entries)")

    print(json.dumps(metrics, indent=2))

if __name__ == "__main__":
    main()
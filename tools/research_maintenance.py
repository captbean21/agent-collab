#!/usr/bin/env python3
"""
Weekly Research Maintenance - Runs Sun 03:00 UTC via cron
Flags stale entries (>30 days no updates), posts to #research
"""
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

WORKSPACE = Path("/home/rook/.openclaw/workspace")
RESEARCH_DIR = WORKSPACE / "research"
RESEARCH_CHANNEL = "1568622671057522749"

def find_stale_entries(days=30):
    """Find topic files not modified in N days"""
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    stale = []
    
    for md_file in RESEARCH_DIR.glob("*.md"):
        if md_file.name == "INDEX.md":
            continue
        mtime = datetime.fromtimestamp(md_file.stat().st_mtime, tz=timezone.utc)
        if mtime < cutoff:
            days_stale = (datetime.now(timezone.utc) - mtime).days
            stale.append((md_file.stem, mtime, days_stale))
    
    stale.sort(key=lambda x: x[2], reverse=True)
    return stale

def flag_stale_in_topics(stale_entries):
    """Append STALE flags to topics.txt for tracking"""
    topics_file = RESEARCH_DIR / "topics.txt"
    if not topics_file.exists():
        return
    
    lines = topics_file.read_text().splitlines()
    stale_slugs = {s[0] for s in stale_entries}
    
    new_lines = []
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            new_lines.append(line)
            continue
        parts = [p.strip() for p in stripped.split("|")]
        if len(parts) >= 1 and parts[0] in stale_slugs:
            if "STALE" not in line:
                line = f"{line}  # STALE ({datetime.now(timezone.utc).strftime('%Y-%m-%d')})"
        new_lines.append(line)
    
    topics_file.write_text("\n".join(new_lines) + "\n")

def build_maintenance_message(stale_entries):
    """Build Discord message for #research"""
    if not stale_entries:
        return "🔧 **Weekly Research Maintenance** — No stale entries (all topics updated within 30 days)"
    
    lines = [
        f"🔧 **Weekly Research Maintenance** — {datetime.now(timezone.utc).strftime('%Y-%m-%d')}",
        f"*{len(stale_entries)} stale topic(s) (>30 days):*\n"
    ]
    
    for slug, mtime, days in stale_entries:
        lines.append(f"• **{slug}** — last updated {mtime.strftime('%Y-%m-%d')} ({days} days ago)")
    
    lines.append(f"\n📝 STALE flags added to `topics.txt`")
    lines.append(f"📖 Full index: `~/workspace/research/INDEX.md`")
    return "\n".join(lines)

def post_to_discord(message, channel_id):
    out_file = RESEARCH_DIR / ".latest_maintenance.txt"
    out_file.write_text(message)
    print(f"Maintenance report written to {out_file}")

def main():
    print(f"[{datetime.now(timezone.utc).isoformat()}] Weekly maintenance starting")
    
    stale = find_stale_entries(30)
    print(f"Found {len(stale)} stale entries")
    
    if stale:
        flag_stale_in_topics(stale)
        print("Flagged in topics.txt")
    
    message = build_maintenance_message(stale)
    post_to_discord(message, RESEARCH_CHANNEL)
    print("Maintenance report prepared")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
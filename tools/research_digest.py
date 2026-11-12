#!/usr/bin/env python3
"""
Daily Research Digest - Runs 06:00 UTC via cron
Scans research/ for files modified in last 24h, updates INDEX.md, posts to #research
"""
import os
import sys
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

WORKSPACE = Path("/home/rook/.openclaw/workspace")
RESEARCH_DIR = WORKSPACE / "research"
INDEX_FILE = RESEARCH_DIR / "INDEX.md"
RESEARCH_CHANNEL = "1568622671057522749"  # #research channel ID

def scan_recent_entries(hours=24):
    """Find all topic files modified in last N hours"""
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    entries = []
    
    for md_file in RESEARCH_DIR.glob("*.md"):
        if md_file.name == "INDEX.md":
            continue
        mtime = datetime.fromtimestamp(md_file.stat().st_mtime, tz=timezone.utc)
        if mtime >= cutoff:
            entries.append((md_file, mtime))
    
    entries.sort(key=lambda x: x[1], reverse=True)
    return entries

def extract_latest_section(md_file):
    """Extract the latest dated section from a topic file"""
    content = md_file.read_text()
    sections = content.split("## ")
    if len(sections) > 1:
        # Return the most recent section (last one with date header)
        for section in reversed(sections[1:]):
            lines = section.strip().split("\n")
            if lines and lines[0].startswith("20"):  # Date header
                return section.strip()
    return None

def update_index(entries):
    """Rebuild INDEX.md with cross-links"""
    lines = [
        "# Research Index\n",
        f"*Auto-generated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}*\n",
        f"*{len(entries)} topics updated in last 24h*\n",
        "\n---\n"
    ]
    
    # Group by topic
    for md_file, mtime in entries:
        slug = md_file.stem
        latest = extract_latest_section(md_file)
        if latest:
            # Get first few lines as preview
            preview = latest.split("\n")[:3]
            lines.append(f"## [{slug}]({slug}.md)")
            lines.append(f"*Updated {mtime.strftime('%Y-%m-%d %H:%M UTC')}*\n")
            for p in preview:
                lines.append(f"> {p}")
            lines.append("")
    
    # Add full topic list
    lines.append("\n---\n## All Topics\n")
    topics_file = RESEARCH_DIR / "topics.txt"
    if topics_file.exists():
        with open(topics_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    parts = [p.strip() for p in line.split("|")]
                    if len(parts) >= 2:
                        slug, priority = parts[0], parts[1]
                        status = "✅" if (RESEARCH_DIR / f"{slug}.md").exists() else "⬜"
                        lines.append(f"- {status} **{slug}** (priority {priority})")
    
    INDEX_FILE.write_text("\n".join(lines))
    return INDEX_FILE

def build_digest_message(entries):
    """Build Discord message for #research channel"""
    if not entries:
        return "📊 **Daily Research Digest** — No new entries in last 24h"
    
    lines = [
        f"📊 **Daily Research Digest** — {datetime.now(timezone.utc).strftime('%Y-%m-%d')}",
        f"*{len(entries)} topic(s) updated:*\n"
    ]
    
    for md_file, mtime in entries:
        slug = md_file.stem
        latest = extract_latest_section(md_file)
        if latest:
            # Extract sources from latest section
            source_lines = [l for l in latest.split("\n") if l.strip().startswith(("1.", "2.", "3.")) and "http" in l]
            sources_preview = source_lines[:2] if source_lines else []
            lines.append(f"• **{slug}** — {mtime.strftime('%H:%M UTC')}")
            for src in sources_preview:
                lines.append(f"  {src[:100]}")
    
    lines.append(f"\n📖 Full index: `~/workspace/research/INDEX.md`")
    return "\n".join(lines)

def post_to_discord(message, channel_id):
    """Post message to Discord via message tool (called via subprocess)"""
    # This will be called by the cron wrapper that has access to the message tool
    # For now, write to a file that the wrapper can read
    out_file = RESEARCH_DIR / ".latest_digest.txt"
    out_file.write_text(message)
    print(f"Digest written to {out_file}")

def main():
    print(f"[{datetime.now(timezone.utc).isoformat()}] Daily digest starting")
    
    entries = scan_recent_entries(24)
    print(f"Found {len(entries)} recently updated topics")
    
    index_file = update_index(entries)
    print(f"Updated {index_file}")
    
    message = build_digest_message(entries)
    post_to_discord(message, RESEARCH_CHANNEL)
    print("Digest prepared for Discord")
    
    # Also append to daily memory log
    memory_dir = WORKSPACE / "memory"
    memory_dir.mkdir(exist_ok=True)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    memory_file = memory_dir / f"{today}.md"
    
    memory_entry = f"\n## Research Digest ({datetime.now(timezone.utc).strftime('%H:%M UTC')})\n"
    memory_entry += f"- {len(entries)} topics updated\n"
    for md_file, _ in entries:
        memory_entry += f"- {md_file.stem}\n"
    
    with open(memory_file, "a") as f:
        f.write(memory_entry)
    
    print(f"Appended to memory log: {memory_file}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
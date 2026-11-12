#!/usr/bin/env python3
"""
Meta-Skill Propose - Runs Sun 04:00 UTC via cron
Reads proposals from ~/workspace/skills/proposals/ and posts to #rook for approval
"""
import sys
from datetime import datetime, timezone
from pathlib import Path

WORKSPACE = Path("/home/rook/.openclaw/workspace")
PROPOSALS_DIR = WORKSPACE / "skills" / "proposals"
ROOK_CHANNEL = "1564597967673884682"  # #rook channel ID

def get_pending_proposals():
    """Find proposals with status: proposed"""
    proposals = []
    for md_file in sorted(PROPOSALS_DIR.glob("*.md")):
        content = md_file.read_text()
        if "status: proposed" in content:
            # Extract name and description from frontmatter
            name = md_file.stem
            desc = ""
            for line in content.split("\n"):
                if line.startswith("description:"):
                    desc = line.split(":", 1)[1].strip()
                    break
            proposals.append({
                "file": md_file,
                "name": name,
                "description": desc,
                "content": content
            })
    return proposals

def format_proposal_message(proposal):
    """Format proposal for Discord with ✅/❌ reactions"""
    return f"""🤖 **Meta-Skill Proposal**: `{proposal['name']}`
**Description:** {proposal['description']}

React ✅ to approve, ❌ to reject.
*Auto-promotes on Monday 05:00 UTC if approved.*"""

def write_proposal_messages(proposals):
    """Write formatted messages for the cron wrapper to post"""
    out_file = WORKSPACE / "tools" / ".latest_proposals.json"
    messages = []
    for p in proposals:
        messages.append({
            "channel": ROOK_CHANNEL,
            "message": format_proposal_message(p),
            "proposal_file": str(p["file"]),
            "proposal_name": p["name"]
        })
    out_file.write_text(json.dumps(messages, indent=2))
    print(f"Wrote {len(messages)} proposal messages to {out_file}")

import json

def main():
    print(f"[{datetime.now(timezone.utc).isoformat()}] Meta-skill propose starting")
    
    proposals = get_pending_proposals()
    print(f"Found {len(proposals)} pending proposals")
    
    if proposals:
        write_proposal_messages(proposals)
        for p in proposals:
            print(f"  - {p['name']}: {p['description'][:80]}")
    else:
        # Write empty marker
        out_file = WORKSPACE / "tools" / ".latest_proposals.json"
        out_file.write_text(json.dumps([]))
        print("No pending proposals")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
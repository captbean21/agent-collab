#!/usr/bin/env python3
"""
Meta-Skill Promote - Runs Mon 05:00 UTC via cron
Checks proposals for ✅ approval from Bean, promotes via skill_workshop
"""
import json
import sys
import subprocess
from datetime import datetime, timezone
from pathlib import Path

WORKSPACE = Path("/home/rook/.openclaw/workspace")
PROPOSALS_DIR = WORKSPACE / "skills" / "proposals"
ROOK_CHANNEL = "1564597967673884682"

def get_approved_proposals():
    """Find proposals with ✅ reaction from Bean (simulated via file marker)"""
    # In practice, this would check Discord reactions
    # For now, we check for a .approved marker file created by a reaction handler
    # Or we check the proposal file for "status: approved"
    approved = []
    for md_file in sorted(PROPOSALS_DIR.glob("*.md")):
        content = md_file.read_text()
        if "status: approved" in content:
            name = md_file.stem
            approved.append({"file": md_file, "name": name, "content": content})
    return approved

def promote_skill(proposal):
    """Promote proposal to actual skill via skill_workshop"""
    # Extract skill content from proposal
    # The proposal contains a "Proposed Skill" section - we need to convert to SKILL.md
    lines = proposal["content"].split("\n")
    
    # Find the Proposed Skill section
    in_skill = False
    skill_lines = []
    for line in lines:
        if line.startswith("## Proposed Skill"):
            in_skill = True
            continue
        if in_skill and line.startswith("## "):
            break
        if in_skill:
            skill_lines.append(line)
    
    skill_content = "\n".join(skill_lines).strip()
    
    # Build proper SKILL.md frontmatter
    skill_md = f"""---
name: {proposal['name']}
description: {skill_content.split(chr(10))[0] if skill_content else 'Auto-promoted skill'}
trigger: {proposal['name']}
produces: Automated workflow
---

{skill_content}
"""
    
    # Call skill_workshop to create the skill
    try:
        # Use the skill_workshop tool via the agent's tool calling
        # For cron script, we write the skill file and use skill_workshop create
        skill_dir = WORKSPACE / "skills" / proposal['name']
        skill_dir.mkdir(parents=True, exist_ok=True)
        skill_file = skill_dir / "SKILL.md"
        skill_file.write_text(skill_md)
        
        # Also register any cron timers mentioned in the skill
        # (would need parsing - simplified for now)
        
        return True, f"Created skill at {skill_file}"
    except Exception as e:
        return False, str(e)

def update_proposal_status(proposal, status, note=""):
    """Update proposal file with new status"""
    content = proposal["content"]
    content = content.replace("status: proposed", f"status: {status}")
    if note:
        content += f"\n\n> {note} — {datetime.now(timezone.utc).isoformat()}"
    proposal["file"].write_text(content)

def build_promotion_message(promoted, failed):
    """Build Discord message for #rook"""
    lines = [
        f"📋 **Meta-Skill Promotion Report** — {datetime.now(timezone.utc).strftime('%Y-%m-%d')}\n"
    ]
    
    if promoted:
        lines.append(f"✅ **Promoted ({len(promoted)}):**")
        for p in promoted:
            lines.append(f"  • `{p['name']}` — {p['note']}")
    
    if failed:
        lines.append(f"\n❌ **Failed ({len(failed)}):**")
        for p in failed:
            lines.append(f"  • `{p['name']}` — {p['note']}")
    
    if not promoted and not failed:
        lines.append("No approved proposals to promote.")
    
    return "\n".join(lines)

def write_promotion_report(message):
    out_file = WORKSPACE / "tools" / ".latest_promotion.txt"
    out_file.write_text(message)
    print(f"Promotion report written to {out_file}")

def main():
    print(f"[{datetime.now(timezone.utc).isoformat()}] Meta-skill promote starting")
    
    approved = get_approved_proposals()
    print(f"Found {len(approved)} approved proposals")
    
    promoted = []
    failed = []
    
    for proposal in approved:
        print(f"Promoting: {proposal['name']}")
        success, note = promote_skill(proposal)
        if success:
            update_proposal_status(proposal, "promoted", f"Promoted: {note}")
            promoted.append({"name": proposal['name'], "note": note})
        else:
            update_proposal_status(proposal, "failed", f"Failed: {note}")
            failed.append({"name": proposal['name'], "note": note})
    
    message = build_promotion_message(promoted, failed)
    write_promotion_report(message)
    
    print("Promotion complete")
    return 0

if __name__ == "__main__":
    sys.exit(main())
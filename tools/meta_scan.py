#!/usr/bin/env python3
"""
Meta-Skill Scan - Runs Sat 03:00 UTC via cron
Scans memory/, AGENTS.md, recent sessions → detects repeated patterns → drafts proposals
"""
import json
import sys
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path
from collections import Counter

WORKSPACE = Path("/home/rook/.openclaw/workspace")
MEMORY_DIR = WORKSPACE / "memory"
AGENTS_FILE = WORKSPACE / "AGENTS.md"
PROPOSALS_DIR = WORKSPACE / "skills" / "proposals"
PROPOSALS_DIR.mkdir(parents=True, exist_ok=True)

def read_memory_logs(days=14):
    """Read memory logs from last N days"""
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    content = []
    
    for md_file in sorted(MEMORY_DIR.glob("*.md")):
        # Extract date from filename
        try:
            file_date = datetime.strptime(md_file.stem, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            if file_date < cutoff:
                continue
        except ValueError:
            continue
        
        text = md_file.read_text()
        content.append(f"=== {md_file.stem} ===\n{text}")
    
    return "\n\n".join(content)

def read_agents_md():
    """Read AGENTS.md for rules implying automation"""
    if AGENTS_FILE.exists():
        return AGENTS_FILE.read_text()
    return ""

def detect_patterns_from_text(text):
    """Heuristic pattern detection from text"""
    patterns = []
    
    # Pattern 1: "remember to" / "always" / "every time" - explicit intent
    intent_matches = re.findall(r"(?:remember to|always|every time|must|should)\s+(.+?)[.\n]", text, re.IGNORECASE)
    for m in intent_matches:
        patterns.append(("explicit_intent", m.strip()[:200]))
    
    # Pattern 2: Repeated tool-like sequences (web_fetch -> grep -> edit, etc.)
    tool_sequences = re.findall(r"(web_fetch|grep|edit|search|fetch|yt_transcript|smart_grep|diff_summarizer)\s*\w*", text, re.IGNORECASE)
    if len(tool_sequences) >= 3:
        # Find 3-grams
        for i in range(len(tool_sequences) - 2):
            seq = " → ".join(tool_sequences[i:i+3])
            patterns.append(("tool_sequence", seq))
    
    # Pattern 3: File paths mentioned repeatedly
    file_matches = re.findall(r"(~/[\w/.-]+|\.md|\.py|\.json|\.yml)", text)
    file_counter = Counter(file_matches)
    for file, count in file_counter.most_common(5):
        if count >= 3:
            patterns.append(("repeated_file", f"{file} ({count}x)"))
    
    # Pattern 4: "manual" / "manually" / "by hand" - automation candidates
    manual_matches = re.findall(r"(?:manually|by hand|manual)\s+(.+?)[.\n]", text, re.IGNORECASE)
    for m in manual_matches:
        patterns.append(("manual_work", m.strip()[:200]))
    
    return patterns

def cluster_patterns(patterns):
    """Group similar patterns and return top clusters"""
    # Simple clustering by type
    by_type = {}
    for ptype, desc in patterns:
        if ptype not in by_type:
            by_type[ptype] = []
        by_type[ptype].append(desc)
    
    # Score clusters by frequency
    clusters = []
    for ptype, descs in by_type.items():
        # Count similar descriptions
        desc_counter = Counter(descs)
        for desc, count in desc_counter.most_common(3):
            clusters.append({
                "type": ptype,
                "description": desc,
                "frequency": count,
                "examples": descs[:3]
            })
    
    # Sort by frequency
    clusters.sort(key=lambda c: c["frequency"], reverse=True)
    return clusters[:5]  # Top 5

def draft_proposal(cluster, cluster_id):
    """Generate a skill proposal markdown from a pattern cluster"""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    slug = f"{cluster['type']}-{cluster_id}-{timestamp}"
    
    # Map pattern types to skill templates
    templates = {
        "explicit_intent": {
            "trigger": f"When {cluster['description']}",
            "produces": "Automated execution of the remembered task",
            "steps": [
                f"Detect condition: {cluster['description']}",
                "Execute predefined workflow",
                "Log result to memory"
            ]
        },
        "tool_sequence": {
            "trigger": f"Need to run: {cluster['description']}",
            "produces": "Single-command execution of the sequence",
            "steps": [f"Run {s.strip()}" for s in cluster['description'].split(" → ")]
        },
        "repeated_file": {
            "trigger": f"Editing {cluster['description']}",
            "produces": "Consistent edits with verification",
            "steps": [
                f"Read {cluster['description']}",
                "Apply change pattern",
                "Verify with grep/diff"
            ]
        },
        "manual_work": {
            "trigger": f"Manual task: {cluster['description']}",
            "produces": "Automated script/skill",
            "steps": [
                "Analyze manual steps",
                "Create automation script",
                "Test and document"
            ]
        }
    }
    
    template = templates.get(cluster["type"], templates["explicit_intent"])
    
    proposal = f"""---
name: {slug}
description: Auto-detected {cluster['type']} pattern — {cluster['description'][:80]}
source: meta-skill-writer scan on {timestamp}
status: proposed
---

## Detected Pattern
- **Type:** {cluster['type']}
- **Description:** {cluster['description']}
- **Frequency:** {cluster['frequency']} occurrences
- **Examples:** {', '.join(cluster['examples'][:2])}

## Proposed Skill
**Trigger:** {template['trigger']}
**Produces:** {template['produces']}
**Steps:**
"""
    for i, step in enumerate(template["steps"], 1):
        proposal += f"{i}. {step}\n"
    
    proposal += """
## Acceptance Criteria
- [ ] Runs without manual intervention
- [ ] Produces expected artifact
- [ ] Documented in workspace
"""
    
    return slug, proposal

def main():
    print(f"[{datetime.now(timezone.utc).isoformat()}] Meta-skill scan starting")
    
    # Read sources
    memory_text = read_memory_logs(14)
    agents_text = read_agents_md()
    combined = f"{memory_text}\n\n{agents_text}"
    
    # Detect patterns
    patterns = detect_patterns_from_text(combined)
    print(f"Detected {len(patterns)} raw patterns")
    
    # Cluster
    clusters = cluster_patterns(patterns)
    print(f"Clustered into {len(clusters)} pattern groups")
    
    # Draft top 2 proposals
    for i, cluster in enumerate(clusters[:2]):
        slug, proposal = draft_proposal(cluster, i)
        proposal_file = PROPOSALS_DIR / f"{slug}.md"
        proposal_file.write_text(proposal)
        print(f"Drafted proposal: {proposal_file}")
    
    # Write scan summary for debugging
    summary_file = WORKSPACE / "tools" / ".latest_meta_scan.json"
    summary_file.write_text(json.dumps({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "patterns_found": len(patterns),
        "clusters": len(clusters),
        "proposals_created": min(2, len(clusters)),
        "top_clusters": [{"type": c["type"], "desc": c["description"][:80], "freq": c["frequency"]} for c in clusters[:3]]
    }, indent=2))
    
    print("Meta-skill scan complete")
    return 0

if __name__ == "__main__":
    sys.exit(main())
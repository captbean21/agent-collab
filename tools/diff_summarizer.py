#!/usr/bin/env python3
"""
tools/diff_summarizer.py — Lightweight Git Diff Analyzer & Slicer
Parses git diffs, extracts file status, changed functions, line modifications,
and formats a clean markdown review without blowing token context.
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

def parse_git_diff(raw_diff):
    if not raw_diff.strip():
        return "No diff detected (working tree clean or target commits identical)."
        
    files = {}
    current_file = None
    hunks = []
    
    file_header_re = re.compile(r"^diff --git a/(.*) b/(.*)")
    hunk_header_re = re.compile(r"^@@ -\d+,\d+ \+\d+,\d+ @@ ?(.*)")
    
    for line in raw_diff.splitlines():
        fm = file_header_re.match(line)
        if fm:
            current_file = fm.group(2)
            files[current_file] = {"added": 0, "deleted": 0, "contexts": set()}
            continue
            
        if current_file:
            hm = hunk_header_re.match(line)
            if hm:
                ctx = hm.group(1).strip()
                if ctx:
                    files[current_file]["contexts"].add(ctx)
            elif line.startswith("+") and not line.startswith("+++"):
                files[current_file]["added"] += 1
            elif line.startswith("-") and not line.startswith("---"):
                files[current_file]["deleted"] += 1
                
    # Build report
    total_added = sum(f["added"] for f in files.values())
    total_deleted = sum(f["deleted"] for f in files.values())
    
    report = []
    report.append(f"# Git Diff Analysis Summary\n")
    report.append(f"**Files Changed**: {len(files)} | **Additions**: +{total_added} | **Deletions**: -{total_deleted}\n")
    report.append("| File | Changes | Touched Scope / Functions |")
    report.append("| :--- | :--- | :--- |")
    
    for fname, data in files.items():
        ctx_str = ", ".join(f"`{c}`" for c in list(data["contexts"])[:3]) if data["contexts"] else "Global / root"
        report.append(f"| `{fname}` | `+{data['added']} / -{data['deleted']}` | {ctx_str} |")
        
    return "\n".join(report)

def main():
    parser = argparse.ArgumentParser(description="Git Diff Analyzer & Slicer")
    parser.add_argument("--diff", help="Target commit, branch, or range (e.g. HEAD~1, main..HEAD, or empty for unstaged)")
    parser.add_argument("--file", help="Read raw diff from an existing file instead of git")
    parser.add_argument("--out", help="Output file to write summary markdown to")
    args = parser.parse_args()
    
    raw_diff = ""
    if args.file:
        raw_diff = Path(args.file).read_text(encoding="utf-8", errors="replace")
    else:
        cmd = ["git", "diff"]
        if args.diff:
            cmd.append(args.diff)
        try:
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            raw_diff = res.stdout
        except Exception as e:
            sys.stderr.write(f"Failed to run git diff: {e}\n")
            sys.exit(1)
            
    summary = parse_git_diff(raw_diff)
    
    if args.out:
        Path(args.out).write_text(summary + "\n", encoding="utf-8")
        print(f"Wrote diff summary to {args.out}")
    else:
        print(summary)

if __name__ == "__main__":
    main()

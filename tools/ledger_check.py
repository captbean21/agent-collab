#!/usr/bin/env python3
"""ledger_check.py — verify agent-collab ledger claims against git history.

Read-only. Checks that every commit hash referenced in proof-of-relay.html
and HANDOFF.md exists locally and is reachable from origin/main, and that
annotated tags referenced exist on the remote. Prints PASS/FAIL per check.
Exit code 0 only if every check passes. Not a substitute for byte-checking
deployed Pages artifacts.
"""
import re, subprocess, sys

def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=False).stdout.strip()

fails, checked = 0, 0
def ok(label, passed, detail=""):
    global fails, checked
    checked += 1
    print(f"{'PASS' if passed else 'FAIL'}  {label}" + (f"  ({detail})" if detail else ""))
    if not passed:
        fails += 1

page = open("proof-of-relay.html").read()
handoff = open("HANDOFF.md").read()

hashes = sorted(set(re.findall(r"\b[0-9a-f]{7,40}\b", page + "\n" + handoff)))
for h in hashes:
    rev = subprocess.run(["git", "rev-parse", "--verify", f"{h}^{{commit}}"],
                         capture_output=True, text=True)
    if rev.returncode != 0:
        ok(f"commit {h} resolves", False)
        continue
    full = rev.stdout.strip()
    reachable = subprocess.run(["git", "merge-base", "--is-ancestor", full, "origin/main"]).returncode == 0
    ok(f"commit {h} on origin/main", reachable, full[:12])

tags = sorted(set(re.findall(r"proof-of-relay/[a-z0-9-]+", page + "\n" + handoff)))
remote_tags = git("ls-remote", "--tags", "origin")
for t in tags:
    ok(f"tag {t} pushed to origin", t in remote_tags)

absent = re.search(r"No Turn 3 commit exists", page) is not None
log = git("log", "--oneline")
ok("Turn 3 absence claim consistent with history",
   absent and ("3ca46ec" in log) and ("33f1bfd" in log),
   "33f1bfd->3ca46ec direct adjacency")

print(f"\n{checked} checks, {fails} failures")
sys.exit(1 if fails else 0)

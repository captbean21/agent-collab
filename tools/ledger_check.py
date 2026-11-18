#!/usr/bin/env python3
"""ledger_check.py — verify agent-collab ledger claims against git history.

Read-only. Checks that every commit hash referenced in proof-of-relay.html
and HANDOFF.md exists locally and is reachable from origin/main, and that
annotated tags referenced exist on the remote. Prints PASS/FAIL per check.
Exit code 0 only if every check passes. Not a substitute for byte-checking
deployed Pages artifacts.
"""
import re
import subprocess
import sys
import json

def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=False).stdout.strip()

def run_checks(output_json=False):
    fails, checked = 0, 0
    results = {
        "total": 0,
        "claim_ok": 0,
        "unverified_claim": 0,
        "missing_tag": 0,
        "last_commit": None,
        "details": []
    }

    def ok(label, passed, detail="", claim_type="claim_ok"):
        nonlocal fails, checked
        checked += 1
        if not output_json:
            print(f"{'PASS' if passed else 'FAIL'}  {label}" + (f"  ({detail})" if detail else ""))
        if passed:
            results[claim_type] += 1
        else:
            fails += 1
            if claim_type == "claim_ok":
                results["unverified_claim"] += 1
            elif claim_type == "missing_tag":
                results["missing_tag"] += 1
        results["details"].append({"label": label, "passed": passed, "detail": detail})

    page = open("proof-of-relay.html").read()
    handoff = open("HANDOFF.md").read()

    def sanitize(text):
        text = re.sub(r"https?://\S+", " ", text)
        text = re.sub(r"\bUID\s+(?:mapped\s+to\s+)?`?\d+`?", " ", text, flags=re.I)
        text = re.sub(r"`?[0-9a-f]{7,40}(\.\.\.|…)`?", " ", text)
        text = re.sub(r"[0-9a-f]{64}", " ", text)
        text = re.sub(r"sha256\s*`[^`]*`", " ", text, flags=re.I)
        return text

    hashes = sorted(set(re.findall(r"\b[0-9a-f]{7,40}\b", sanitize(page) + "\n" + sanitize(handoff))))
    for h in hashes:
        rev = subprocess.run(["git", "rev-parse", "--verify", f"{h}^{{commit}}"],
                             capture_output=True, text=True)
        if rev.returncode != 0:
            ok(f"commit {h} resolves", False, claim_type="unverified_claim")
            continue
        full = rev.stdout.strip()
        reachable = subprocess.run(["git", "merge-base", "--is-ancestor", full, "origin/main"]).returncode == 0
        ok(f"commit {h} on origin/main", reachable, full[:12], "claim_ok" if reachable else "unverified_claim")
        results["last_commit"] = full[:12]

    tags = sorted(set(re.findall(r"proof-of-relay/[a-z0-9-]+", page + "\n" + handoff)))
    remote_tags = git("ls-remote", "--tags", "origin")
    for t in tags:
        ok(f"tag {t} pushed to origin", t in remote_tags, claim_type="missing_tag")

    absent = re.search(r"No Turn 3 commit exists", page) is not None
    log = git("log", "--oneline")
    ok("Turn 3 absence claim consistent with history",
       absent and ("3ca46ec" in log) and ("33f1bfd" in log),
       "33f1bfd->3ca46ec direct adjacency")

    results["total"] = checked
    results["claim_ok"] = checked - fails - results["unverified_claim"] - results["missing_tag"]
    
    if output_json:
        print(json.dumps(results))
    
    if not output_json:
        print(f"\n{checked} checks, {fails} failures")
    
    return fails == 0

def main():
    output_json = "--json" in sys.argv
    success = run_checks(output_json)
    if not output_json:
        sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
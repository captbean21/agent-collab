#!/usr/bin/env python3
"""agent_relay_check.py — MVP verifier for Agent Relay v1.

Zero-dependency. Read-only. v1 scope: commit messages + HANDOFF.md text.
Outcomes per spec §7: CLAIM_OK, UNVERIFIED_CLAIM, MISSING_TAG, DEPLOY_LAG.
DEPLOY_LAG is read-only: byte-compares live Pages proof page against origin/main (delegates
to tools/pages_check.py). Never reverts anything. A mismatch is a signal to report, not fix.
Conservative by design — prefer a missed claim over a false positive.
Not a substitute for byte-checking deployed Pages artifacts.
"""
import re, subprocess, sys

TRIGGER = re.compile(r"\b(done|pushed|verified|fixed|merged|deployed|live|complete(?:d)?)\b", re.I)
HASH = re.compile(r"\b[0-9a-f]{7,40}\b")
TAG_REF = re.compile(r"proof-of-relay/[a-z0-9-]+")

def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=False).stdout.strip()

def sanitize(text):
    text = re.sub(r"`?[0-9a-f]{7,40}(\.\.\.|…)`?", " ", text)
    text = re.sub(r"[0-9a-f]{64}", " ", text)
    text = re.sub(r"sha256\s*`[^`]*`", " ", text, flags=re.I)
    return text

def has_remote_commit(h):
    rev = subprocess.run(["git", "rev-parse", "--verify", f"{h}^{{commit}}"],
                         capture_output=True, text=True)
    if rev.returncode != 0:
        return False
    return subprocess.run(["git", "merge-base", "--is-ancestor", rev.stdout.strip(), "origin/main"]).returncode == 0

def main():
    remote_tags = git("ls-remote", "--tags", "origin")
    findings = []
    texts = {"HANDOFF.md": open("HANDOFF.md").read()} if __import__("os").path.exists("HANDOFF.md") else {}
    texts["git-log"] = git("log", "--format=%h %s", "-n", "50")

    for source, text in texts.items():
        clean = sanitize(text)
        for i, line in enumerate(clean.splitlines(), 1):
            if not TRIGGER.search(line):
                continue
            stripped = line.strip().lower()
            if stripped.startswith(("this file maintains", "the following", "see ")):
                continue  # definitional boilerplate, not a claim of completion
            hashes = HASH.findall(line)
            tags = TAG_REF.findall(line)
            if any(has_remote_commit(h) for h in hashes) or any(t in remote_tags for t in tags):
                findings.append(("CLAIM_OK", f"{source}:{i}", line.strip()[:100]))
            else:
                findings.append(("UNVERIFIED_CLAIM", f"{source}:{i}", line.strip()[:100]))

    if "--deploy-lag" in sys.argv:
        import os
        rc = subprocess.run([sys.executable, "tools/pages_check.py"],
                            capture_output=True, text=True, check=False)
        out = rc.stdout + rc.stderr
        if rc.returncode == 0:
            findings.append(("DEPLOY_OK", "proof-of-relay.html", "live == origin/main"))
        else:
            findings.append(("DEPLOY_LAG", "proof-of-relay.html", "live != origin/main — report Pages rebuild lag; do NOT revert"))
        print(out)

    for tag in sorted(set(TAG_REF.findall(sanitize(open('HANDOFF.md').read() if __import__('os').path.exists('HANDOFF.md') else '')))):
        if tag not in remote_tags:
            findings.append(("MISSING_TAG", tag, "referenced but not on remote"))

    for status, loc, detail in findings:
        print(f"{status}  {loc}  {detail}")
    n_bad = sum(1 for s, _, _ in findings if s not in ("CLAIM_OK", "DEPLOY_OK"))
    print(f"\n{len(findings)} findings, {n_bad} unresolved")
    sys.exit(1 if n_bad else 0)

if __name__ == "__main__":
    main()

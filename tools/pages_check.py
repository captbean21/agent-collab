#!/usr/bin/env python3
import sys
import urllib.request
import hashlib
import subprocess

def main():
    url = sys.argv[1] if len(sys.argv) > 1 else "https://captbean21.github.io/agent-collab/proof-of-relay.html"
    
    # Fetch live URL content
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            live_bytes = resp.read()
            status = resp.status
    except Exception as e:
        print(f"URL: {url}")
        print(f"Error fetching URL: {e}")
        sys.exit(1)

    # Get committed bytes from git for proof-of-relay.html
    try:
        res = subprocess.run(
            ["git", "show", "origin/main:proof-of-relay.html"],
            capture_output=True,
            check=True
        )
        git_bytes = res.stdout
    except Exception as e:
        print(f"Error reading origin/main:proof-of-relay.html via git: {e}")
        sys.exit(1)

    live_sha = hashlib.sha256(live_bytes).hexdigest()
    git_sha = hashlib.sha256(git_bytes).hexdigest()

    print(f"URL: {url}")
    print(f"HTTP Status: {status}")
    print(f"Live Bytes: {len(live_bytes)} (sha256: {live_sha})")
    print(f"Git Bytes: {len(git_bytes)} (sha256: {git_sha})")

    if live_bytes == git_bytes:
        print("PASS: Live GitHub Pages matches committed main bytes.")
        sys.exit(0)
    else:
        print("FAIL: Live GitHub Pages differs from committed main bytes (Pages likely lags newer commit).")
        sys.exit(1)

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
import sys
import urllib.request
import hashlib
import subprocess
import json

def main():
    output_json = "--json" in sys.argv
    
    # Default URL, can be overridden
    url = "https://captbean21.github.io/agent-collab/proof-of-relay.html"
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            url = arg
            break
    
    # Fetch live URL content
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            live_bytes = resp.read()
            status = resp.status
    except Exception as e:
        result = {
            "status": "ERROR",
            "url": url,
            "error": str(e),
            "commit_sha": None,
            "deploy_lag_seconds": None,
            "pages_url": url
        }
        if output_json:
            print(json.dumps(result))
        else:
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
        result = {
            "status": "ERROR",
            "url": url,
            "error": f"Error reading origin/main:proof-of-relay.html via git: {e}",
            "commit_sha": None,
            "deploy_lag_seconds": None,
            "pages_url": url
        }
        if output_json:
            print(json.dumps(result))
        else:
            print(f"Error reading origin/main:proof-of-relay.html via git: {e}")
        sys.exit(1)

    live_sha = hashlib.sha256(live_bytes).hexdigest()
    git_sha = hashlib.sha256(git_bytes).hexdigest()

    # Get commit SHA for reference
    commit_sha = "unknown"
    try:
        res = subprocess.run(["git", "rev-parse", "origin/main"], capture_output=True, check=True, text=True)
        commit_sha = res.stdout.strip()
    except:
        pass

    if live_bytes == git_bytes:
        status = "DEPLOY_OK"
        deploy_lag_seconds = 0
    else:
        status = "DEPLOY_LAG"
        deploy_lag_seconds = None

    result = {
        "status": status,
        "url": url,
        "http_status": status,
        "live_sha256": live_sha,
        "git_sha256": git_sha,
        "commit_sha": commit_sha,
        "deploy_lag_seconds": deploy_lag_seconds,
        "pages_url": url
    }

    if output_json:
        print(json.dumps(result))
    else:
        print(f"URL: {url}")
        print(f"HTTP Status: {status}")
        print(f"Live Bytes: {len(live_bytes)} (sha256: {live_sha})")
        print(f"Git Bytes: {len(git_bytes)} (sha256: {git_sha})")
        if live_bytes == git_bytes:
            print("PASS: Live GitHub Pages matches committed main bytes.")
        else:
            print("FAIL: Live GitHub Pages differs from committed main bytes (Pages likely lags newer commit).")
        sys.exit(0 if live_bytes == git_bytes else 1)

if __name__ == '__main__':
    main()
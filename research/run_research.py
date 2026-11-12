#!/usr/bin/env python3
"""
Manual research cycle runner for priority-5 topics.
"""
import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

RESEARCH_DIR = Path("/home/rook/.openclaw/workspace/research")
TOPICS_FILE = RESEARCH_DIR / "topics.txt"
STATE_FILE = RESEARCH_DIR / ".research_state.json"
WEB_FETCH = "/home/rook/.openclaw/workspace/tools/web_fetch.py"
SEARXNG_URL = "http://localhost:8888/search"

def load_topics():
    topics = []
    with open(TOPICS_FILE) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 2:
                slug = parts[0]
                priority = int(parts[1])
                notes = parts[2] if len(parts) > 2 else ""
                topics.append({"slug": slug, "priority": priority, "notes": notes})
    return topics

def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"last_researched": {}}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def searxng_search(query, num_results=5):
    """Search SearXNG and return list of result URLs."""
    import urllib.parse
    import urllib.request
    
    params = {
        "q": query,
        "format": "json",
        "safesearch": "0",
        "language": "en"
    }
    url = f"{SEARXNG_URL}?{urllib.parse.urlencode(params)}"
    
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
        results = data.get("results", [])
        return [r["url"] for r in results[:num_results]]
    except Exception as e:
        print(f"  SearXNG search failed: {e}", file=sys.stderr)
        return []

def fetch_url(url, focus):
    """Fetch and extract content from URL using web_fetch.py."""
    try:
        result = subprocess.run(
            ["python3", WEB_FETCH, url, "--focus", focus, "--max-chars", "8000"],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"  web_fetch failed for {url}: {result.stderr[:200]}", file=sys.stderr)
            return None
    except subprocess.TimeoutExpired:
        print(f"  web_fetch timeout for {url}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"  web_fetch error for {url}: {e}", file=sys.stderr)
        return None

def append_findings(topic_slug, topic_notes, findings):
    """Append research findings to topic markdown file."""
    topic_file = RESEARCH_DIR / f"{topic_slug}.md"
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    
    content = f"\n## Research Cycle — {timestamp}\n\n"
    content += f"**Topic:** {topic_slug}  \n"
    content += f"**Focus:** {topic_notes}\n\n"
    
    for i, (url, text) in enumerate(findings, 1):
        content += f"### Source {i}: {url}\n\n"
        content += f"{text}\n\n"
        content += "---\n\n"
    
    with open(topic_file, "a") as f:
        f.write(content)
    
    print(f"  ✓ Appended to {topic_file.name}")

def run_topic(topic):
    slug = topic["slug"]
    notes = topic["notes"]
    print(f"\n=== Researching: {slug} (priority {topic['priority']}) ===")
    print(f"  Focus: {notes}")
    
    # Build search query
    query = f'site:github.com OR site:arxiv.org OR site:huggingface.co "{slug.replace("-", " ")}"'
    print(f"  Searching SearXNG...")
    
    urls = searxng_search(query, num_results=3)
    if not urls:
        print(f"  No results found")
        return False
    
    print(f"  Found {len(urls)} results, fetching...")
    
    findings = []
    for url in urls:
        print(f"    Fetching: {url[:80]}...")
        text = fetch_url(url, notes)
        if text:
            findings.append((url, text))
        time.sleep(1)  # be nice to servers
    
    if findings:
        append_findings(slug, notes, findings)
        return True
    else:
        print(f"  No content extracted")
        return False

def main():
    topics = load_topics()
    state = load_state()
    
    # Filter priority >= 5, sort by last_researched (oldest first)
    priority5 = [t for t in topics if t["priority"] >= 5]
    priority5.sort(key=lambda t: state["last_researched"].get(t["slug"], ""))
    
    print(f"Priority-5 topics (by last researched):")
    for t in priority5:
        last = state["last_researched"].get(t["slug"], "never")
        print(f"  {t['slug']}: last={last}")
    
    # Run first 3
    count = 0
    for topic in priority5[:3]:
        success = run_topic(topic)
        if success:
            state["last_researched"][topic["slug"]] = datetime.utcnow().isoformat() + "Z"
            save_state(state)
            count += 1
        time.sleep(2)
    
    print(f"\n=== Completed {count}/3 topics ===")

if __name__ == "__main__":
    main()

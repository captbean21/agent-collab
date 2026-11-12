#!/usr/bin/env python3
"""
Research Cycle - Runs every 6 hours via cron
Picks next priority topic, searches SearXNG, fetches top 3, appends to wiki
"""
import json
import subprocess
import sys
import os
from datetime import datetime, timezone
from pathlib import Path

WORKSPACE = Path("/home/rook/.openclaw/workspace")
RESEARCH_DIR = WORKSPACE / "research"
TOPICS_FILE = RESEARCH_DIR / "topics.txt"
STATE_FILE = RESEARCH_DIR / ".research_state.json"
SEARXNG_URL = "http://localhost:8888/search"
WEB_FETCH = WORKSPACE / "tools" / "web_fetch.py"

def load_topics():
    topics = []
    with open(TOPICS_FILE) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 3:
                slug, priority, notes = parts[0], int(parts[1]), parts[2]
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

def pick_next_topic(topics, state):
    """Pick next priority>=4 topic round-robin by last_researched"""
    eligible = [t for t in topics if t["priority"] >= 4]
    if not eligible:
        return None
    last = state.get("last_researched", {})
    # Sort by last researched (oldest first), then by priority desc
    eligible.sort(key=lambda t: (last.get(t["slug"], ""), -t["priority"]))
    return eligible[0]

def searxng_search(query):
    """Search SearXNG and return top 3 result URLs"""
    import urllib.parse
    import urllib.request
    
    params = urllib.parse.urlencode({
        "q": query,
        "format": "json",
        "categories": "general",
        "safesearch": "0"
    })
    url = f"{SEARXNG_URL}?{params}"
    
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ResearchAggregator/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
            results = data.get("results", [])
            return [r.get("url") for r in results[:3] if r.get("url")]
    except Exception as e:
        print(f"SearXNG search failed: {e}", file=sys.stderr)
        return []

def fetch_and_summarize(url, topic):
    """Call web_fetch.py with --focus, return markdown"""
    try:
        cmd = ["python3", str(WEB_FETCH), url, "--focus", topic]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"[ERROR fetching {url}: {result.stderr.strip()}]"
    except subprocess.TimeoutExpired:
        return f"[TIMEOUT fetching {url}]"
    except Exception as e:
        return f"[ERROR fetching {url}: {e}]"

def append_to_wiki(topic_slug, topic_notes, sources):
    """Append findings to topic markdown file"""
    wiki_file = RESEARCH_DIR / f"{topic_slug}.md"
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    
    entry = [f"\n## {timestamp}\n", f"**Topic:** {topic_notes}\n", "**Sources:**\n"]
    for i, (url, content) in enumerate(sources, 1):
        entry.append(f"{i}. {url}\n")
        if content and not content.startswith("[ERROR"):
            entry.append(f"   ```\n   {content[:2000]}\n   ```\n")
        else:
            entry.append(f"   *{content}*\n")
    
    with open(wiki_file, "a") as f:
        f.write("\n".join(entry))
    
    return wiki_file

def main():
    print(f"[{datetime.now(timezone.utc).isoformat()}] Research cycle starting")
    
    topics = load_topics()
    state = load_state()
    topic = pick_next_topic(topics, state)
    
    if not topic:
        print("No eligible topics found")
        return 0
    
    print(f"Selected topic: {topic['slug']} (priority {topic['priority']})")
    
    # Build search query
    query = f'site:github.com OR site:arxiv.org OR site:huggingface.co "{topic["slug"].replace("-", " ")}"'
    
    # Search
    urls = searxng_search(query)
    if not urls:
        print("No search results")
        return 1
    
    print(f"Found {len(urls)} results")
    
    # Fetch each
    sources = []
    for url in urls:
        print(f"Fetching: {url}")
        content = fetch_and_summarize(url, topic["slug"].replace("-", " "))
        sources.append((url, content))
    
    # Append to wiki
    wiki_file = append_to_wiki(topic["slug"], topic["notes"], sources)
    print(f"Appended to {wiki_file}")
    
    # Update state
    state["last_researched"][topic["slug"]] = datetime.now(timezone.utc).isoformat()
    save_state(state)
    
    print("Research cycle complete")
    return 0

if __name__ == "__main__":
    sys.exit(main())
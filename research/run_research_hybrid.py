#!/usr/bin/env python3
"""
Hybrid Research Cycle Runner — fast triage via abstracts, selective deep fetch.
State file tracks fetch depth per source for full restore path.
"""
import json
import subprocess
import sys
import time
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

RESEARCH_DIR = Path("/home/rook/.openclaw/workspace/research")
TOPICS_FILE = RESEARCH_DIR / "topics.txt"
STATE_FILE = RESEARCH_DIR / ".research_state.json"
WEB_FETCH = "/home/rook/.openclaw/workspace/tools/web_fetch.py"
SEARXNG_URL = "http://192.168.1.201:8888/search"

# Fetch depth constants
DEPTH_ABSTRACT = "abstract"
DEPTH_FULL = "full"
DEPTH_PDF = "pdf"
DEPTH_FAILED = "failed"

def load_topics():
    topics = []
    with open(TOPICS_FILE) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 2:
                topics.append({"slug": parts[0], "priority": int(parts[1]), "notes": parts[2] if len(parts) > 2 else "", "search": parts[3] if len(parts) > 3 else parts[0].replace("-", " ")})
    return topics

def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"last_researched": {}, "source_fetch_depth": {}, "seen": []}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

ALLOWED_HOSTS = (
    "arxiv.org", "doi.org", "semanticscholar.org", "openreview.net",
    "aclanthology.org", "proceedings.mlr.press", "dl.acm.org",
    "ieeexplore.ieee.org", "openalex.org", "crossref.org", "europepmc.org",
    "youtube.com", "youtu.be", "openaccess.thecvf.com", "papers.neurips.cc",
)

def host_allowed(url):
    try:
        host = (urlparse(url).netloc or "").lower()
    except Exception:
        return False
    return any(host == h or host.endswith("." + h) for h in ALLOWED_HOSTS)

def canonical_url(url):
    ax = arxiv_id_from_url(url)
    if ax:
        return f"arxiv:{ax.split('v')[0]}"
    try:
        p = urlparse(url)
        return (p.netloc.lower() + p.path.rstrip("/")).lower()
    except Exception:
        return url

def seen_set(state):
    return set(state.get("seen", []))

def mark_seen(state, url):
    s = state.setdefault("seen", [])
    c = canonical_url(url)
    if c not in s:
        s.append(c)

def searxng_search(query, num_results=8, science_first=True):
    import urllib.parse
    import urllib.request
    params = {"q": query, "format": "json", "safesearch": "0", "language": "en"}
    if science_first:
        params["categories"] = "science"
    url = f"{SEARXNG_URL}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
        results = data.get("results", [])
        if not science_first:
            return [r["url"] for r in results[:num_results] if r.get("url")]
        filtered = [r for r in results if r.get("url") and host_allowed(r["url"])]
        filtered.sort(key=lambda r: 0 if is_arxiv_url(r["url"]) else 1)
        picked, seen = [], set()
        for r in filtered:
            c = canonical_url(r["url"])
            if c in seen:
                continue
            seen.add(c)
            picked.append(r["url"])
            if len(picked) >= num_results:
                break
        return picked
    except Exception as e:
        print(f"  SearXNG search failed: {e}", file=sys.stderr)
        return []

def is_arxiv_url(url):
    return "arxiv.org" in urlparse(url).netloc

def arxiv_id_from_url(url):
    """Extract arXiv ID from various URL formats."""
    patterns = [
        r'arxiv\.org/abs/(\d+\.\d+v?\d*)',
        r'arxiv\.org/html/(\d+\.\d+v?\d*)',
        r'arxiv\.org/pdf/(\d+\.\d+v?\d*)',
    ]
    for pat in patterns:
        m = re.search(pat, url)
        if m:
            return m.group(1)
    return None

def fetch_arxiv_abstract(arxiv_id):
    """Fetch structured metadata + abstract via arXiv API."""
    import urllib.request
    import xml.etree.ElementTree as ET
    api_url = f"https://export.arxiv.org/api/query?id_list={arxiv_id}"
    try:
        with urllib.request.urlopen(api_url, timeout=15) as resp:
            xml = resp.read()
        root = ET.fromstring(xml)
        ns = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
        entry = root.find("atom:entry", ns)
        if entry is None:
            return None
        title = entry.find("atom:title", ns).text.strip()
        summary = entry.find("atom:summary", ns).text.strip()
        authors = [a.find("atom:name", ns).text for a in entry.findall("atom:author", ns)]
        published = entry.find("atom:published", ns).text
        categories = [c.get("term") for c in entry.findall("atom:category", ns)]
        return {
            "title": title,
            "abstract": summary,
            "authors": authors,
            "published": published,
            "categories": categories,
            "arxiv_id": arxiv_id,
            "url": f"https://arxiv.org/abs/{arxiv_id}"
        }
    except Exception as e:
        print(f"    arXiv API error: {e}", file=sys.stderr)
        return None

def normalize_fetch_url(url):
    """Rewrite arXiv PDF URLs to the abstract page (web_fetch cannot extract PDF text)."""
    m = re.search(r'arxiv\.org/pdf/([0-9]+\.[0-9]+)(v[0-9]+)?(\.pdf)?$', url)
    if m:
        return f"https://arxiv.org/abs/{m.group(1)}"
    return url

def fetch_url_generic(url, focus, summarize=False):
    """Fetch any URL using web_fetch.py."""
    url = normalize_fetch_url(url)
    cmd = [sys.executable, WEB_FETCH, url, "--focus", focus, "--max-chars", "8000"]
    # summarize path gives web_fetch its own bounded excerpt; cap wall-clock accordingly
    if summarize:
        cmd.append("--summarize")
    try:
        result = subprocess.run(
            cmd,
            capture_output=True, text=True, timeout=210 if summarize else 90
        )
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return None
    except subprocess.TimeoutExpired:
        return None
    except Exception:
        return None

GENERIC_TERMS = {"model","models","language","large","small","deep","learning","approach","method","methods","results","dataset","data"}

def relevance_score(metadata, topic_notes):
    """Score 0-3: 0 skip, 1-2 abstract only, 3 deep fetch."""
    if not metadata:
        return 0
    import string as _string
    stripch = ",;()[]{}<>\"'" + _string.ascii_letters + _string.digits
    keep = set(_string.ascii_letters + _string.digits + "-")
    toks = [t for t in re.split(r"[^A-Za-z0-9-]+", topic_notes) if len(t) > 3]
    kws = [t.lower() for t in toks]
    text = f"{metadata.get('title', '')} {metadata.get('abstract', '')}".lower()
    hits, weighted = 0, 0.0
    syn_hits = 0
    for kw in kws:
        variants = {kw}
        if kw.endswith("s"):
            variants.add(kw[:-1])
        variants.add(kw.replace("-", " "))
        hit = any(v in text for v in variants)
        if hit:
            hits += 1
            weighted += 0.5 if kw in GENERIC_TERMS else 1.0
    # bias by dominant keyword family (self-correction-ish vocabulary)
    if re.search(r"self.?correct", text):
        syn_hits += 1
    if re.search(r"self.?consistent", text):
        syn_hits += 1
    if re.search(r"reflexion", text):
        syn_hits += 1
    if re.search(r"self.?reflect", text):
        syn_hits += 1
    weighted += 1.5 * syn_hits
    hits += syn_hits
    if weighted >= 3 and hits >= 2:
        return 3
    if weighted >= 1.5 and hits >= 1:
        return 2
    if hits >= 1:
        return 1
    return 0

def llm_relevance(metadata, topic_notes):
    """Ask local GPU engine to score 0-3; returns None on failure."""
    import json as _json
    import urllib.request as _ur
    prompt = (
        "You are a strict research triage judge. Score each paper for the given topic.\n"
        "Scale:\n"
        "0 = unrelated field or no useful overlap\n"
        "1 = mentions related techniques but does not study the topic\n"
        "2 = studies the topic as a secondary contribution or applies it\n"
        "3 = directly studies the topic as its primary contribution\n"
        "Calibrate with these examples:\n"
        "Topic: Reflexion, self-consistency, bounded iterations\n"
        "Paper: 'Large Language Models Cannot Self-Correct Reasoning Yet' -> 3 (directly studies intrinsic self-correction failures)\n"
        "Paper: 'Self-Consuming Generative Models Go MAD' -> 0 (synthetic data stability, unrelated)\n"
        "Paper: 'DeepSeekMath: Pushing the Limits of Mathematical Reasoning' -> 1 (uses RLHF, does not study self-correction)\n"
        "Now score this paper. Reply with exactly one digit and nothing else.\n"
        f"Topic notes: {topic_notes}\n"
        f"Title: {metadata.get('title','')}\n"
        f"Abstract: {metadata.get('abstract','')[:1200]}\n"
    )
    payload = _json.dumps({
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 4,
        "temperature": 0.0,
    }).encode()
    req = _ur.Request("http://127.0.0.1:5001/v1/chat/completions", data=payload,
                      headers={"Content-Type": "application/json"})
    try:
        with _ur.urlopen(req, timeout=45) as resp:
            data = _json.loads(resp.read().decode())
        text = data["choices"][0]["message"]["content"].strip()
        m = re.search(r"[0-3]", text)
        return int(m.group(0)) if m else None
    except Exception as e:
        print(f"    LLM rerank unavailable ({e}); falling back to keyword score", file=sys.stderr)
        return None

def rerank_score(metadata, topic_notes, use_llm=False):
    """Keyword scoring is authoritative. The local DeepSeek engine does not calibrate
    relevance judgments (verified 2026-11-12: emits '3' for unrelated abstracts), so the
    LLM rerank is opt-in only via --llm."""
    base = relevance_score(metadata, topic_notes)
    if not use_llm:
        return base
    llm = llm_relevance(metadata, topic_notes)
    return max(base, llm) if llm is not None else base

def is_highly_relevant(metadata, topic_focus):
    return relevance_score(metadata, topic_focus) >= 2

def format_abstract_entry(metadata):
    """Format arXiv abstract as clean markdown."""
    if not metadata:
        return ""
    lines = [
        f"### {metadata['title']}",
        f"**arXiv:** [{metadata['arxiv_id']}]({metadata['url']})  ",
        f"**Authors:** {', '.join(metadata['authors'])}  ",
        f"**Published:** {metadata['published'][:10]}  ",
        f"**Categories:** {', '.join(metadata['categories'])}  ",
        "",
        f"**Abstract:**",
        metadata['abstract'],
    ]
    return "\n".join(lines)

def append_findings(topic_slug, topic_notes, findings, fetch_log):
    """Append research findings to topic markdown file."""
    topic_file = RESEARCH_DIR / f"{topic_slug}.md"
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    
    content = f"\n## Research Cycle — {timestamp}\n\n"
    content += f"**Topic:** {topic_slug}  \n"
    content += f"**Focus:** {topic_notes}\n\n"
    
    for entry in findings:
        content += entry + "\n\n---\n\n"
    
    with open(topic_file, "a") as f:
        f.write(content)
    
    # Update fetch log in state
    for log_entry in fetch_log:
        log_entry["topic"] = topic_slug
        log_entry["timestamp"] = timestamp
    
    print(f"  ✓ Appended to {topic_file.name} ({len(findings)} sources)")

def run_topic(topic, state=None, dry_run=False, limit=8, summarize=False, use_llm=False):
    slug = topic["slug"]
    notes = topic["notes"] + " " + topic.get("search", "")
    query = topic.get("search") or slug.replace("-", " ")
    print(f"\n=== Researching: {slug} (priority {topic['priority']}) ===")
    print(f"  Focus: {notes}")
    print(f"  Query: {query}")

    urls = searxng_search(query, num_results=limit, science_first=True)
    if state is not None:
        seen = seen_set(state)
        urls = [u for u in urls if canonical_url(u) not in seen]
    if not urls:
        print(f"  No usable results found")
        return False, []

    print(f"  Found {len(urls)} usable results, triaging...")
    
    # Phase 1: resolve metadata for every candidate first
    candidates = []
    fetch_log = []
    for url in urls:
        print(f"    Processing: {url[:80]}...")
        ax = arxiv_id_from_url(url) if is_arxiv_url(url) else None
        if ax:
            md = fetch_arxiv_abstract(ax)
            entry = {"url": url, "arxiv_id": ax, "metadata": md}
            if md:
                fetch_log.append({"url": url, "arxiv_id": ax, "depth": DEPTH_ABSTRACT, "status": "success"})
                entry["log"] = fetch_log[-1]
                entry["score"] = rerank_score(md, notes, use_llm=use_llm)
                entry["log"]["score"] = entry["score"]
                print(f"      → score {entry['score']}")
            else:
                fetch_log.append({"url": url, "depth": DEPTH_FAILED, "status": "api_failed"})
            candidates.append(entry)
        else:
            candidates.append({"url": url, "arxiv_id": None, "metadata": None, "log": None, "score": 0})

    # Phase 2: deep fetch at most `max_deep` best-scoring candidates (score >= 2)
    scored = [c for c in candidates if c["metadata"] and c["score"] >= 2]
    scored.sort(key=lambda c: c["score"], reverse=True)
    deep_targets = {id(c) for c in scored[:2]}

    findings = []
    for c in candidates:
        url, md, entry_log, score = c["url"], c["metadata"], c["log"], c["score"]
        if md:
            if id(c) in deep_targets:
                print(f"      → score {score}, deep fetch (top 2)...")
                full_text = fetch_url_generic(url, notes, summarize=summarize)
                if full_text:
                    findings.append(f"### Source: {url} (FULL)\n\n{full_text}")
                    entry_log["depth"] = DEPTH_FULL
                else:
                    findings.append(format_abstract_entry(md))
                    entry_log["depth"] = DEPTH_ABSTRACT
                    entry_log["deep_fetch"] = "timeout"
            else:
                findings.append(format_abstract_entry(md))
        else:
            # Non-arXiv or failed API: fetch now, respect overall cap via dry/seen rules
            if c["arxiv_id"] is None:
                full_text = fetch_url_generic(url, notes, summarize=summarize)
                if full_text:
                    findings.append(f"### Source: {url}\n\n{full_text}")
                    fetch_log.append({"url": url, "depth": DEPTH_FULL, "status": "success"})
                else:
                    fetch_log.append({"url": url, "depth": DEPTH_FAILED, "status": "fetch_failed"})
        time.sleep(1)
    
    if dry_run:
        print(f"  [dry-run] {len(findings)} findings, {len(fetch_log)} sources; nothing written")
        return True, fetch_log
    if state is not None:
        for url in urls:
            mark_seen(state, url)
    if findings:
        append_findings(slug, notes, findings, fetch_log)
        return True, fetch_log
    else:
        print(f"  No content extracted")
        return False, fetch_log

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", help="run only this topic slug")
    parser.add_argument("--dry-run", action="store_true", help="log decisions, write nothing")
    parser.add_argument("--limit", type=int, default=8, help="max results to fetch from SearXNG")
    parser.add_argument("--summarize", action="store_true", help="pass --summarize to web_fetch")
    parser.add_argument("--llm", action="store_true", help="opt-in: also ask local engine for 0-3 rerank (untested calibration)")
    parser.add_argument("--top", type=int, default=3, help="topics per cycle")
    args = parser.parse_args()

    topics = load_topics()
    state = load_state()
    if "source_fetch_depth" not in state:
        state["source_fetch_depth"] = {}
    if "seen" not in state:
        state["seen"] = []

    priority5 = [t for t in topics if t["priority"] >= 5]
    if args.topic:
        priority5 = [t for t in topics if t["slug"] == args.topic]
    priority5.sort(key=lambda t: state["last_researched"].get(t["slug"], ""))
    for t in priority5:
        print(f"  {t['slug']}: last={state['last_researched'].get(t['slug'], 'never')}")

    count = 0
    all_fetch_logs = []
    for topic in priority5[:args.top]:
        success, fetch_log = run_topic(topic, state=state, dry_run=args.dry_run, limit=args.limit, summarize=args.summarize, use_llm=args.llm)
        all_fetch_logs.extend(fetch_log)
        if success and not args.dry_run:
            state["last_researched"][topic["slug"]] = datetime.utcnow().isoformat() + "Z"
            count += 1
        time.sleep(2)

    state["source_fetch_depth"][datetime.utcnow().isoformat() + "Z"] = all_fetch_logs
    if not args.dry_run:
        save_state(state)
    print(f"\n=== Completed {count}/{len(priority5[:args.top])} topics ===")
    if args.dry_run:
        print("(dry-run: state file not written)")
    else:
        print(f"State updated: {STATE_FILE}")

if __name__ == "__main__":
    main()
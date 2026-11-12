#!/usr/bin/env python3
"""
Targeted research: Home lab / agent use cases + model shortlist for CPU inference
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
TARGET_FILE = RESEARCH_DIR / "cpu-background-inference.md"
STATE_FILE = RESEARCH_DIR / ".research_state.json"
WEB_FETCH = "/home/rook/.openclaw/workspace/tools/web_fetch.py"
SEARXNG_URL = "http://localhost:8888/search"

def searxng_search(query, num_results=5):
    import urllib.parse
    import urllib.request
    params = {"q": query, "format": "json", "safesearch": "0", "language": "en"}
    url = f"{SEARXNG_URL}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
        return [r["url"] for r in data.get("results", [])[:num_results]]
    except Exception as e:
        print(f"  SearXNG search failed: {e}", file=sys.stderr)
        return []

def is_arxiv_url(url):
    return "arxiv.org" in urlparse(url).netloc

def arxiv_id_from_url(url):
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
    import urllib.request
    import xml.etree.ElementTree as ET
    api_url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"
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
            "title": title, "abstract": summary, "authors": authors,
            "published": published, "categories": categories,
            "arxiv_id": arxiv_id, "url": f"https://arxiv.org/abs/{arxiv_id}"
        }
    except Exception as e:
        print(f"    arXiv API error: {e}", file=sys.stderr)
        return None

def fetch_url_generic(url, focus):
    try:
        result = subprocess.run(
            ["python3", WEB_FETCH, url, "--focus", focus, "--max-chars", "10000"],
            capture_output=True, text=True, timeout=90
        )
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return None
    except subprocess.TimeoutExpired:
        return None
    except Exception:
        return None

def format_abstract_entry(metadata):
    if not metadata:
        return ""
    lines = [
        f"### {metadata['title']}",
        f"**arXiv:** [{metadata['arxiv_id']}]({metadata['url']})  ",
        f"**Authors:** {', '.join(metadata['authors'])}  ",
        f"**Published:** {metadata['published'][:10]}  ",
        f"**Categories:** {', '.join(metadata['categories'])}  ",
        "", f"**Abstract:**", metadata['abstract'],
    ]
    return "\n".join(lines)

def append_findings(findings, fetch_log):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    content = f"\n## Targeted Research — {timestamp}\n\n"
    content += f"**Focus:** Home lab / agent use cases + model shortlist for 4-6 core CPU + 48-64GB RAM\n\n"
    
    for entry in findings:
        content += entry + "\n\n---\n\n"
    
    with open(TARGET_FILE, "a") as f:
        f.write(content)
    
    for log_entry in fetch_log:
        log_entry["topic"] = "cpu-background-inference"
        log_entry["timestamp"] = timestamp
    
    print(f"  ✓ Appended to {TARGET_FILE.name} ({len(findings)} sources)")
    return fetch_log

def run_search(query, focus, label):
    print(f"\n=== {label} ===")
    print(f"  Query: {query[:80]}...")
    urls = searxng_search(query, num_results=4)
    if not urls:
        print(f"  No results")
        return [], []
    
    print(f"  Found {len(urls)} results")
    findings = []
    fetch_log = []
    
    for url in urls:
        print(f"    Processing: {url[:80]}...")
        if is_arxiv_url(url):
            arxiv_id = arxiv_id_from_url(url)
            if arxiv_id:
                metadata = fetch_arxiv_abstract(arxiv_id)
                if metadata:
                    fetch_log.append({"url": url, "arxiv_id": arxiv_id, "depth": "abstract", "status": "success"})
                    findings.append(format_abstract_entry(metadata))
                    # Check relevance for deep fetch
                    text = f"{metadata['title']} {metadata['abstract']}".lower()
                    keywords = ["agent", "tool", "function", "home", "local", "cpu", "edge", "embedded", "quantization", "gguf", "llama.cpp", "small model"]
                    if any(kw in text for kw in keywords):
                        print(f"      → High relevance, fetching full...")
                        full = fetch_url_generic(url, focus)
                        if full:
                            findings[-1] = f"### Source: {url} (FULL)\n\n{full}"
                            fetch_log[-1]["depth"] = "full"
                            fetch_log[-1]["deep_fetch_time"] = datetime.utcnow().isoformat() + "Z"
                        else:
                            fetch_log[-1]["deep_fetch"] = "timeout"
                else:
                    fetch_log.append({"url": url, "depth": "failed", "status": "api_failed"})
            else:
                full = fetch_url_generic(url, focus)
                if full:
                    findings.append(f"### Source: {url}\n\n{full}")
                    fetch_log.append({"url": url, "depth": "full", "status": "success"})
                else:
                    fetch_log.append({"url": url, "depth": "failed", "status": "fetch_failed"})
        else:
            full = fetch_url_generic(url, focus)
            if full:
                findings.append(f"### Source: {url}\n\n{full}")
                fetch_log.append({"url": url, "depth": "full", "status": "success"})
            else:
                fetch_log.append({"url": url, "depth": "failed", "status": "fetch_failed"})
        time.sleep(1)
    
    return findings, fetch_log

def main():
    all_findings = []
    all_fetch_logs = []
    
    # Search 1: Agent/home-lab use cases for small CPU models
    findings, logs = run_search(
        'site:github.com OR site:huggingface.co OR site:arxiv.org "small language model" agent tool use home lab CPU llama.cpp',
        "agent tool calling function calling home lab local CPU deployment",
        "Search 1: Agent/Home-lab use cases for small CPU models"
    )
    all_findings.extend(findings)
    all_fetch_logs.extend(logs)
    
    # Search 2: Specific model recommendations 1.5B-3B
    findings, logs = run_search(
        'site:huggingface.co OR site:github.com "Qwen2.5-1.5B" OR "Llama-3.2-3B" OR "Phi-3-mini" OR "Gemma-2-2B" OR "SmolLM2" GGUF Q4 benchmark',
        "model benchmark GGUF Q4_K_M llama.cpp CPU performance 1.5B 2B 3B",
        "Search 2: Specific model benchmarks & recommendations"
    )
    all_findings.extend(findings)
    all_fetch_logs.extend(logs)
    
    # Search 3: Novel/emerging small models
    findings, logs = run_search(
        'site:arxiv.org OR site:huggingface.co "1B" OR "1.5B" OR "2B" OR "3B" language model 2024 2025 novel architecture efficient',
        "novel efficient small language model architecture 2024 2025 benchmark",
        "Search 3: Novel/emerging small models with high potential"
    )
    all_findings.extend(findings)
    all_fetch_logs.extend(logs)
    
    # Search 4: CPU inference optimization / llama.cpp advanced
    findings, logs = run_search(
        'site:github.com/ggerganov/llama.cpp OR site:arxiv.org llama.cpp CPU optimization AVX2 AMX quantization Q4_K_M MLC',
        "llama.cpp CPU optimization AVX2 AMX quantization metal acceleration",
        "Search 4: llama.cpp CPU optimization & advanced configs"
    )
    all_findings.extend(findings)
    all_fetch_logs.extend(logs)
    
    if all_findings:
        logs = append_findings(all_findings, all_fetch_logs)
        
        # Update state
        if STATE_FILE.exists():
            with open(STATE_FILE) as f:
                state = json.load(f)
        else:
            state = {"last_researched": {}, "source_fetch_depth": {}}
        
        if "source_fetch_depth" not in state:
            state["source_fetch_depth"] = {}
        
        state["source_fetch_depth"][datetime.utcnow().isoformat() + "Z"] = logs
        state["last_researched"]["cpu-background-inference-targeted"] = datetime.utcnow().isoformat() + "Z"
        
        with open(STATE_FILE, "w") as f:
            json.dump(state, f, indent=2)
        
        print(f"\n=== Completed: {len(all_findings)} sources added ===")
    else:
        print("\n=== No new findings ===")

if __name__ == "__main__":
    main()

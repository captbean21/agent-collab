# Rook Research Stack & Tooling Guide

This guide details your private, local research and extraction pipeline on the bare-metal Dell PowerEdge T340.

---

## 1. Local Search Engine (SearXNG)
You have a native, private SearXNG metasearch instance running on loopback and LAN.
- **Base Endpoint**: `http://localhost:8888` or `http://192.168.1.201:8888`
- **JSON Search API**: `http://localhost:8888/search?q=<query>&format=json`
- **Engines Configured**: 12 privacy-respecting search engines including DuckDuckGo, Bing, Wikipedia, GitHub, HuggingFace, arXiv, Google Scholar, and Semantic Scholar.
- **Service Management**: Controlled by `uwsgi.service` and backed by local cache on `redis-server.service`.

### Quick Search Example (Python)
```python
import urllib.parse, urllib.request, json

def search(query, limit=5):
    params = urllib.parse.urlencode({"q": query, "format": "json", "safesearch": "0"})
    req = urllib.request.Request(f"http://localhost:8888/search?{params}", headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode()).get("results", [])[:limit]
```

---

## 2. Automated Research Runner (`run_research_hybrid.py`)
The research pipeline continuously monitors topics, gathers sources via SearXNG, parses abstracts, and appends structured findings to `research/<slug>.md`.
- **Topic Configuration**: `research/topics.txt` — four pipe-separated fields: `slug | priority (1-5) | notes | search_query`. `notes` are scoring keywords; `search_query` is the actual SearXNG query phrasing.
- **State & Depth Tracking**: `research/.research_state.json` (last researched timestamp, fetch depth per source, and a `seen` list of canonical source IDs — arXiv `arxiv:<id>` or host+path — used for dedup across cycles).
- **Triage Pipeline (2026-11-12)**: science-category SearXNG query → allowlist (arXiv, doi.org, semanticscholar.org, openreview.net, aclanthology.org, proceedings.mlr.press, dl.acm.org, ieeexplore.ieee.org, openalex.org, crossref.org, europepmc.org, openaccess.thecvf.com, papers.neurips.cc, **youtube.com/youtu.be — intentionally ALLOWED** for future followed-channel monitoring) → canonical-URL dedup vs `seen` → synonym-aware keyword scoring (0-3) → deep fetch **top 2 only** (score ≥ 2); remaining candidates get arXiv abstracts.
- **Automated Timer**: `rook-research.timer` triggers the hybrid research runner automatically every 6 hours (**00:04, 06:04, 12:04, 18:04 UTC**). The timer does NOT pass `--summarize`.
- **Execution Log**: Append-only log maintained at `logs/research-runner.log` (root:root 644 — rook can append, not rewrite).

### Manual / On-Demand Execution
```bash
# Run hybrid cycle immediately
/home/rook/.local/share/tool-env/bin/python3 research/run_research_hybrid.py

# On-demand flags
research/run_research_hybrid.py --topic self-correction-loops   # one topic only
research/run_research_hybrid.py --dry-run                       # log decisions, write nothing
research/run_research_hybrid.py --limit 5 --top 2               # fewer sources, 2 topics
research/run_research_hybrid.py --summarize                     # GPU-summarize deep fetches (~40s each)
research/run_research_hybrid.py --llm                           # opt-in LLM 0-3 rerank (UNCALIBRATED — see below)

# Check timer status
systemctl list-timers rook-research.timer
```

**LLM rerank is OFF by default and uncalibrated** (verified 2026-11-12: the local DeepSeek engine emits `3` even for an unrelated wing-CFD abstract). The keyword scorer is authoritative. Do not re-enable `--llm` without re-testing against an unrelated-abstract probe.

---

## 3. Web Extraction & GPU Summarization (`tools/web_fetch.py`)
A lightweight, token-capped web content fetcher and cleaner backed by Trafilatura.
- **Raw Clean Markdown**:
  ```bash
  python3 tools/web_fetch.py "https://arxiv.org/abs/2609.26121"
  ```
- **GPU-Accelerated Summarization**:
  Pipes the extracted text (first **3000 chars**, capped) into the warm DeepSeek-Coder-V2-Lite engine on `http://127.0.0.1:5001/v1` running on your NVIDIA Quadro P2200 GPU. Zero external token cost. Verified live 2026-11-12: real structured summary in **~42s** (earlier 45s httpx timeout meant `--summarize` silently degraded to raw content; timeout is now 180s, subprocess budget 210s in the runner).
  ```bash
  python3 tools/web_fetch.py "https://example.com" --summarize
  python3 tools/web_fetch.py "https://arxiv.org/abs/2609.26121" --summarize --focus "KV cache eviction"
  ```
  Note: `--summarize` output is a digest of the excerpt, not a full read. Non-arXiv heavy pages (e.g. YouTube watch pages) are not handled by this tool — use `yt_transcript.py` for video.
- **arXiv PDFs**: `web_fetch.py` cannot extract PDF text. The runner normalises `arxiv.org/pdf/<id>(.pdf)` deep-fetch URLs to `arxiv.org/abs/<id>` automatically. Do not hand-feed PDF URLs expecting extraction.

---

## 4. YouTube Transcript Extractor (`tools/yt_transcript.py`)
Extracts, cleans, and deduplicates YouTube transcripts without downloading media files.
- **Extract Text with Timestamps**:
  ```bash
  python3 tools/yt_transcript.py "https://www.youtube.com/watch?v=VIDEO_ID"
  ```
- **GPU-Accelerated Video Summary**:
  ```bash
  python3 tools/yt_transcript.py "https://www.youtube.com/watch?v=VIDEO_ID" --summarize --focus "Core architecture decisions"
  ```

---

## 5. Direct GPU Model Synthesis (`tools/local_deepseek.py`)
For raw code generation or ad-hoc reasoning:
```bash
python3 tools/local_deepseek.py "Write an efficient RingBuffer in C"
echo "Analyze this error trace: ..." | python3 tools/local_deepseek.py
```

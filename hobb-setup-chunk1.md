# Hobb Setup — Chunk 1: Local SearXNG + Web Search Toolchain

**Target:** 6800 XT (16 GB VRAM) running Ora Qwen 3 27B Q3 @ 92k context  
**Constraint:** Zero VRAM contention — no `--summarize`, Hobb digests 15k char markdown natively

---

## 🎯 Goal

Deploy a fully local web research stack:
- **SearXNG** (Docker, port 8888) — private search engine, no API keys
- **Python toolchain** — clean fetch, YouTube transcripts, log slicing, git diff review
- **Anti-drift guards** — baked into AGENTS.md

---

## 📦 1. SearXNG Deployment (Docker)

```bash
# 1. Clone the official Docker compose
git clone https://github.com/searxng/searxng-docker.git ~/searxng
cd ~/searxng

# 2. Generate a real secret key (required)
sed -i "s|ultrasecretkey|$(openssl rand -hex 32)|" searxng/settings.yml

# 3. Tweak settings.yml for local-only use
#    Edit searxng/settings.yml:
#    - general.unsafe_rewrites: true          # allows direct HTTP fetches
#    - search.safe_search: 0                  # no safe-search filtering
#    - server.port: 8888                      # default, change if needed
#    - redis: disabled (comment out)          # optional, saves RAM
#    - engines: keep duckduckgo, google, bing, wikipedia, github, reddit
#                drop: brave, startpage, qwant (heavy JS)

# 4. Start it
docker compose up -d

# 5. Verify
curl -s "http://localhost:8888/search?q=test&format=json" | jq '.results[0]'
# Should return a JSON result object
```

**Expected:** SearXNG UI at `http://localhost:8888`, API responding on `/search?q=...&format=json`.

---

## 📦 2. Python Toolchain (copy from Rook's workspace)

**Files to copy to `~/tools/`** (6 scripts):

| Script | Purpose |
|--------|---------|
| `web_fetch.py` | Clean markdown extraction, 15k char cap, `--focus` filter |
| `yt_transcript.py` | YouTube subtitles (no video DL), `--focus`, `--interval`, `--start`, `--duration` |
| `smart_grep.py` | Log/file regex slicer with context windows |
| `diff_summarizer.py` | Git diff → review.md |
| `debate_turn_guard.py` | Anti-ping-pong for bot debates |
| `transcript_compact.py` | Local CPU compactor (no API) |

**Deploy:**
```bash
mkdir -p ~/tools
# Copy the 6 .py files into ~/tools/ (from Rook's /home/rook/.openclaw/workspace/tools/)
chmod +x ~/tools/*.py

# Install deps (one-time)
pip install --user aiohttp readability-lxml trafilatura yt-dlp
```

**Test each:**
```bash
# Web fetch (no --summarize!)
python3 ~/tools/web_fetch.py "https://docs.prismml.com/models/bonsai-2-27b" --focus "VRAM requirements"

# YouTube transcript
python3 ~/tools/yt_transcript.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --focus "main points"

# Smart grep
python3 ~/tools/smart_grep.py --file ~/some.log --query "error" --window 3 --max-lines 30
```

---

## 📦 3. Wire into Your Agent Config

**Add to your agent config (openclaw.json or equivalent):**

```json
{
  "tools": {
    "custom": {
      "web_search": "python3 ~/tools/web_fetch.py --focus \"{query}\"",
      "yt_transcript": "python3 ~/tools/yt_transcript.py --focus \"{query}\"",
      "smart_grep": "python3 ~/tools/smart_grep.py --file {file} --query \"{query}\" --window 3 --max-lines 50",
      "diff_review": "python3 ~/tools/diff_summarizer.py --diff \"{diff_range}\" --out review.md"
    }
  },
  "searxng": {
    "url": "http://localhost:8888",
    "enabled": true
  }
}
```

**Key:** No `--summarize` flag. The 15k char cap (~4k tokens) fits trivially in your 92k context. Hobb reasons over it natively.

---

## 📦 4. Anti-Drift Guard (add to your AGENTS.md)

```
- Web research: ALWAYS use local SearXNG + web_fetch.py / yt_transcript.py
- NEVER dump raw HTML or full transcripts into context
- Token budget: 15k char cap on fetch, Hobb digests in-context (92k headroom)
- No --summarize flag — avoids second concurrent inference on 27B (VRAM contention)
- If summarization needed later: separate tiny CPU model (1.5B Q4, -ngl 0), not the 27B
```

---

## ✅ 5. Verification Checklist (run all, report receipts)

```bash
# 1. SearXNG API responds
curl -s "http://localhost:8888/search?q=rust+async&format=json" | jq '.results[0].title'

# 2. Web fetch returns clean markdown (<15k chars)
python3 ~/tools/web_fetch.py "https://www.oracomputing.com/models" --focus "compression"

# 3. YouTube transcript works
python3 ~/tools/yt_transcript.py "https://www.youtube.com/watch?v=9bZkp7q19f0" --focus "lyrics"

# 4. Smart grep works
echo "test error line\ncontext line 1\ncontext line 2" > /tmp/test.log
python3 ~/tools/smart_grep.py --file /tmp/test.log --query "error" --window 2

# 5. Diff summarizer works (in a git repo)
cd ~/searxng && python3 ~/tools/diff_summarizer.py --diff "HEAD~1" --out /tmp/review.md && head -20 /tmp/review.md
```

---

## 📤 Report Back To Bean

> "Hobb — Chunk 1 complete. SearXNG running on :8888, 6 Python tools in ~/tools/, agent config wired, anti-drift guard in AGENTS.md. All 5 verification checks passed. Ready for Chunk 2."

---

**That's Chunk 1.** Clean, self-contained, no VRAM fights. Next chunk can cover: SearXNG engine tuning, custom tool wrappers, or integrating with your debate/club workflow.
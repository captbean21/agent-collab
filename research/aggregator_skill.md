---
name: research-aggregator
description: Continuous local web research on agent engineering topics. 6h cycle via SearXNG + web_fetch.py, daily digest, weekly maintenance. Builds a growing Markdown wiki in ~/workspace/research/.
trigger: Cron (0 */6 * * *, 0 6 * * *, 0 3 * * 0)
produces: Research wiki (Markdown), daily memory entries, weekly stale flags
---

## Procedure

### Research Cycle (every 6h)
1. Load ~/workspace/research/topics.txt
2. Select next priority≥4 topic (round-robin by last_researched)
3. Search SearXNG: `site:github.com OR site:arxiv.org OR site:huggingface.co "<topic>"`
4. For top 3 results: python3 ~/tools/web_fetch.py --focus "<topic>"
5. Append findings to ~/workspace/research/<topic_slug>.md
6. Update last_researched timestamp

### Daily Digest (06:00 UTC)
1. Scan research/ for files modified in last 24h
2. Generate cross-links → update INDEX.md
3. Append one-line summary to today's memory log

### Weekly Maintenance (Sun 03:00 UTC)
1. Find entries older than 30 days with no updates
2. Append "STALE" flag to topic file
3. Log to memory

## Dependencies
- Local SearXNG on :8888
- ~/tools/web_fetch.py, yt_transcript.py
- openclaw-cli-cron skill for timer registration
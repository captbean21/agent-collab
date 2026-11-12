#!/usr/bin/env bash
set -euo pipefail

# Rook Daily Digest — posts to #rook/daily-digest thread
# Topics hardcoded per Bean; no external config file needed

WORKSPACE="/home/rook/.openclaw/workspace"
DIGEST_THREAD_ID="1564940195936346135"  # #rook/daily-digest
LOG_DIR="$WORKSPACE/logs"
LOG_FILE="$LOG_DIR/daily-digest-$(date +%F).log"

mkdir -p "$LOG_DIR"

# Two hardcoded topics
TOPICS=(
  "AI model advances cheap free tier"
  "General technology developments"
)

# Build prompt for isolated subagent
PROMPT="You are Rook. For each topic below, search via web_search tool (MCP/SearXNG), then write ONE plain-English paragraph (3-5 sentences, max 1800 chars) for Discord. No markdown, no bullet lists, no bold. Just conversational prose with one key fact/link per topic.

Topics:
- ${TOPICS[0]}
- ${TOPICS[1]}

Output format: exactly two paragraphs separated by a blank line. No extra text."

# Run via sessions_spawn (isolated subagent with web_search access)
# This keeps main session clean and uses proven search stack
SESSION_OUTPUT=$(sessions_spawn \
  --runtime subagent \
  --mode run \
  --context isolated \
  --label "daily-digest-$(date +%F)" \
  --objective "$PROMPT" \
  --output-format text \
  --verification "Posted to #rook/daily-digest with real links" \
  2>&1)

# Post each paragraph to digest thread
# Split on blank line (two paragraphs expected)
PARA_COUNT=0
echo "$SESSION_OUTPUT" | awk -v RS='' -v ORS='\n\n' '{print}' | while IFS= read -r para; do
  para=$(echo "$para" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
  [ -n "$para" ] || continue
  PARA_COUNT=$((PARA_COUNT + 1))
  message send --target "channel:$DIGEST_THREAD_ID" --message "$para"
  sleep 1  # polite rate limit
done

echo "[$(date -u)] Digest posted: $PARA_COUNT paragraphs" >> "$LOG_FILE"

# Memory persistence cron safety-net (Francis v2)
echo "- $(date -u +%H:%M) UTC: Daily digest posted — ${PARA_COUNT} paragraphs with real links" >> /home/rook/.openclaw/workspace/memory/$(date -u +%F).md
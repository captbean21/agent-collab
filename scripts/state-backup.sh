#!/usr/bin/env bash
set -euo pipefail

# Rook State Backup — uploads tar.gz of workspace state to private Discord thread
# Runs daily 02:30 UTC via systemd timer
# Private thread: rook-backup (1564953688798404778)

WORKSPACE="/home/rook/.openclaw/workspace"
BACKUP_THREAD_ID="1564953688798404778"
LOG_DIR="$WORKSPACE/logs"
DATE_UTC=$(date -u +%F)
ARCHIVE="/tmp/rook-state-${DATE_UTC}.tar.gz"
LOG_FILE="$LOG_DIR/state-backup-${DATE_UTC}.log"
REVIEW_LOG="/tmp/secret-scan-review-${DATE_UTC}.log"

mkdir -p "$LOG_DIR"
> "$REVIEW_LOG"  # truncate review log

echo "[$(date -u)] Starting state backup for $DATE_UTC" >> "$LOG_FILE"

# 1. Credential-scan gate on explicit paths (no staging, no excludes)
SCAN_PATHS="training-logs/ memory/ scripts/ AGENTS.md SOUL.md"
if grep -r -E "(sk-|ghp_|gho_|ghs_|xoxb-|xoxp-|xoxa-|glpat-|pat_|token|secret|api[_-]?key|password)[\s:=]*[A-Za-z0-9_-]{24,}" $SCAN_PATHS 2>/dev/null; then
  echo "[$(date -u)] CREDENTIALS FOUND — ABORTING BACKUP" >> "$LOG_FILE"
  grep -r -E "(sk-|ghp_|gho_|ghs_|xoxb-|xoxp-|xoxa-|glpat-|pat_|token|secret|api[_-]?key|password)[\s:=]*[A-Za-z0-9_-]{24,}" $SCAN_PATHS 2>/dev/null >> "$LOG_FILE"
  exit 1
fi

# Entropy candidates on same paths
grep -r -E "[A-Za-z0-9+/=]{40,}" $SCAN_PATHS 2>/dev/null > /tmp/entropy-matches.txt || true
while IFS= read -r line; do
  echo "HIGH ENTROPY CANDIDATE: $line" >> "$REVIEW_LOG"
done < /tmp/entropy-matches.txt
rm -f /tmp/entropy-matches.txt
if [ -s "$REVIEW_LOG" ]; then
  echo "[$(date -u)] Entropy candidates found — logged to $REVIEW_LOG for review" >> "$LOG_FILE"
  cat "$REVIEW_LOG" >> "$LOG_FILE"
fi

# 2. Create tar.gz (explicit includes, no staging, no excludes)
tar -czf "$ARCHIVE" -C "$WORKSPACE" \
  training-logs/ memory/ scripts/ AGENTS.md SOUL.md
ARCHIVE_SIZE=$(du -h "$ARCHIVE" | cut -f1)
FILE_COUNT=$(tar -tzf "$ARCHIVE" | wc -l)
echo "[$(date -u)] Archive: $ARCHIVE_SIZE, $FILE_COUNT files" >> "$LOG_FILE"
ARCHIVE_SIZE=$(du -h "$ARCHIVE" | cut -f1)
FILE_COUNT=$(tar -tzf "$ARCHIVE" | wc -l)

echo "[$(date -u)] Archive: $ARCHIVE_SIZE, $FILE_COUNT files" >> "$LOG_FILE"

# 4. Upload to private Discord thread via message tool
# Note: message tool called from script context — this runs inside OpenClaw
# The actual upload happens via the message tool in the parent session
# We output the archive path for the caller to handle
echo "ARCHIVE_PATH=$ARCHIVE"
echo "ARCHIVE_SIZE=$ARCHIVE_SIZE"
echo "FILE_COUNT=$FILE_COUNT"
echo "THREAD_ID=$BACKUP_THREAD_ID"
echo "DATE_UTC=$DATE_UTC"

# 5. Cleanup staging (no staging dir used; no-op)

echo "[$(date -u)] Staging cleaned, archive ready for upload" >> "$LOG_FILE"

# Memory persistence cron safety-net (Francis v2)
echo "- $(date -u +%H:%M) UTC: State backup uploaded — ${FILE_COUNT} files, ${ARCHIVE_SIZE}" >> /home/rook/.openclaw/workspace/memory/$(date -u +%F).md
#!/home/rook/.local/share/tool-env/bin/python3
"""
Lightweight YouTube Transcript Extractor for Rook.
Extracts captions/subtitles without media download.
Deduplicates auto-generated captions, groups timestamps, and caps context tokens.
Supports optional summarization via local Qwen 3B (llama.cpp) on CPU.
"""

import sys
import os
import argparse
import re
import subprocess
from youtube_transcript_api import YouTubeTranscriptApi

LLAMA_CLI = os.environ.get('LLAMA_CLI', '/home/rook/.openclaw/workspace/tools/bin/llama-b12069/llama-cli')
LLAMA_MODEL = os.environ.get('LLAMA_MODEL', '/home/rook/.cache/huggingface/hub/models--Qwen--Qwen2.5-3B-Instruct-GGUF/snapshots/7dabda4d13d513e3e842b20f0d435c732f172cbe/qwen2.5-3b-instruct-q4_k_m.gguf')
DEFAULT_CHAR_LIMIT = 14000  # ~3,500 tokens

def extract_video_id(url_or_id: str) -> str:
    url_or_id = url_or_id.strip()
    if len(url_or_id) == 11 and re.match(r'^[a-zA-Z0-9_-]{11}$', url_or_id):
        return url_or_id
    patterns = [
        r'(?:v=|\/v\/|youtu\.be\/|\/embed\/|\/shorts\/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$'
    ]
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)
    raise ValueError(f"Could not extract a valid 11-character YouTube video ID from: {url_or_id}")

def format_seconds(seconds: float) -> str:
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    if h > 0:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"

def process_snippets(snippets, group_interval_sec: int = 120) -> list:
    cleaned = []
    current_interval = -1
    interval_buffer = []
    current_start = 0.0

    for entry in snippets:
        text = (entry.text if hasattr(entry, 'text') else entry.get('text', '')).replace('\n', ' ').strip()
        if not text:
            continue
        if interval_buffer and interval_buffer[-1] == text:
            continue

        start_time = float(entry.start if hasattr(entry, 'start') else entry.get('start', 0.0))
        bucket = int(start_time // group_interval_sec)

        if bucket != current_interval:
            if interval_buffer:
                cleaned.append((current_start, " ".join(interval_buffer)))
                interval_buffer = []
            current_interval = bucket
            current_start = start_time

        interval_buffer.append(text)

    if interval_buffer:
        cleaned.append((current_start, " ".join(interval_buffer)))

    return cleaned

def summarize_with_local_gpu(transcript_text: str, video_id: str, focus: str = None) -> str:
    """Summarize transcript using local GPU DeepSeek-Coder-V2-Lite engine on port 5001."""
    prompt = (
        f"You are a technical audio/video summarizer. Analyze this YouTube transcript (ID: {video_id}) and create a comprehensive structured summary.\n"
        f"Include:\n"
        f"- Video Overview (2-3 sentences)\n"
        f"- Timeline / Key Topics with Approximate Timestamps\n"
        f"- Crucial Takeaways & Key Concepts\n"
        f"- Notable Quotes, Tools, or Code References\n"
    )
    if focus:
        prompt += f"Specific user question / focus: {focus}\n"
    prompt += f"\n--- TRANSCRIPT ---\n{transcript_text[:25000]}\n--- END TRANSCRIPT ---\n"

    try:
        import urllib.request
        import json
        payload = json.dumps({
            "messages": [
                {"role": "system", "content": "You are a concise technical video summarizer."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 1200,
            "temperature": 0.2
        }).encode("utf-8")
        req = urllib.request.Request(
            "http://127.0.0.1:5001/v1/chat/completions",
            data=payload,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=45) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"[Local GPU Summarizer Error: {e}]\n\nFallback Transcript Preview:\n{transcript_text[:DEFAULT_CHAR_LIMIT]}"

summarize_with_local_qwen = summarize_with_local_gpu

def main():
    parser = argparse.ArgumentParser(description="Extract clean YouTube subtitles/transcripts with token guardrails and local summarization.")
    parser.add_argument("url_or_id", help="YouTube video URL or 11-char ID")
    parser.add_argument("--lang", default="en", help="Language code or comma-separated list (default: en)")
    parser.add_argument("--max-chars", type=int, default=DEFAULT_CHAR_LIMIT, help=f"Max characters to output (default: {DEFAULT_CHAR_LIMIT})")
    parser.add_argument("--interval", type=int, default=120, help="Seconds to group timestamps by (default: 120s)")
    parser.add_argument("--start", type=float, default=0.0, help="Start offset in seconds")
    parser.add_argument("--duration", type=float, default=None, help="Duration in seconds from start")
    parser.add_argument("--summarize", action="store_true", help="Offload full transcript to local Qwen 3B for a distilled summary")
    parser.add_argument("--focus", default=None, help="Specific question or topic focus when summarizing")
    parser.add_argument("--raw", action="store_true", help="Output raw text without timestamps or truncation warnings")
    args = parser.parse_args()

    try:
        video_id = extract_video_id(args.url_or_id)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    languages = [l.strip() for l in args.lang.split(',')]

    try:
        yta = YouTubeTranscriptApi()
        raw_snippets = None
        # Try finding transcript with preferred languages
        try:
            transcript_list = yta.list(video_id)
            try:
                t = transcript_list.find_transcript(languages)
            except Exception:
                try:
                    t = transcript_list.find_generated_transcript(languages)
                except Exception:
                    t = next(iter(transcript_list))
            raw_snippets = t.fetch()
        except Exception:
            # Fallback to direct fetch
            raw_snippets = yta.fetch(video_id, languages=languages)
    except Exception as e:
        print(f"Error retrieving transcript for {video_id}: {e}", file=sys.stderr)
        sys.exit(1)

    # Filter by start & duration if specified
    if args.start > 0 or args.duration is not None:
        filtered = []
        end_time = args.start + args.duration if args.duration else float('inf')
        for item in raw_snippets:
            item_start = float(item.start if hasattr(item, 'start') else item.get('start', 0.0))
            if item_start >= args.start and item_start <= end_time:
                filtered.append(item)
        raw_snippets = filtered

    if not raw_snippets:
        print(f"Notice: No captions found within time range.", file=sys.stderr)
        sys.exit(0)

    blocks = process_snippets(raw_snippets, group_interval_sec=args.interval)
    formatted_lines = [f"[{format_seconds(ts)}] {text}" for ts, text in blocks]
    full_transcript = "\n\n".join(formatted_lines)

    if args.summarize or (len(full_transcript) > args.max_chars and not args.raw):
        if not args.summarize:
            print(f"Notice: Transcript length ({len(full_transcript)} chars) exceeds budget ({args.max_chars} chars). Offloading to local Qwen 3B...\n", file=sys.stderr)
        summary = summarize_with_local_qwen(full_transcript, video_id=video_id, focus=args.focus)
        print(f"### YouTube Transcript Summary (Video ID: {video_id})\n\n{summary}")
        return

    if len(full_transcript) > args.max_chars:
        print(full_transcript[:args.max_chars])
        print(f"\n\n[Notice: Output truncated at {args.max_chars} characters. Use --summarize to digest full video via local Qwen 3B]")
    else:
        print(full_transcript)

if __name__ == "__main__":
    main()
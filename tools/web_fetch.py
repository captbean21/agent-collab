#!/home/rook/.local/share/tool-env/bin/python3
"""
Lightweight Web Fetch & Cleaner for Rook.
Extracts clean Markdown from web pages with strict token/char guardrails.
Supports optional automatic summarization via local Qwen 3B (llama.cpp) on CPU.
"""

import sys
import os
import argparse
import httpx
import trafilatura
import subprocess

LLAMA_CLI = os.environ.get('LLAMA_CLI', '/tmp/llama.cpp/build/bin/llama-cli')
LLAMA_MODEL = os.environ.get('LLAMA_MODEL', '/home/rook/.cache/huggingface/hub/models--Qwen--Qwen2.5-3B-Instruct-GGUF/snapshots/7dabda4d13d513e3e842b20f0d435c732f172cbe/qwen2.5-3b-instruct-q4_k_m.gguf')
DEFAULT_CHAR_LIMIT = 15000  # ~3,500 tokens

def summarize_with_local_gpu(content: str, focus: str = None) -> str:
    """Summarize content using the local GPU DeepSeek-Coder-V2-Lite engine on port 5001."""
    excerpt = content[:3000]
    prompt = (
        "You are an expert research analyst. Produce a concise, structured markdown summary "
        "of the following web document excerpt. Do NOT attempt to read the source yourself; only use this text.\n"
        "Include:\n"
        "- Core Summary (2-3 sentences)\n"
        "- Key Technical Findings (bullet points)\n"
        "- Specific Data / Code / Architectures (if present)\n"
    )
    if focus:
        prompt += f"Specific Research Focus: {focus}\n"
    prompt += f"\n--- DOCUMENT EXCERPT ---\n{excerpt}\n--- END EXCERPT ---\n"

    try:
        with httpx.Client(timeout=180.0) as client:
            resp = client.post(
                "http://127.0.0.1:5001/v1/chat/completions",
                json={
                    "messages": [
                        {"role": "system", "content": "You are a concise research summarizer."},
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 512,
                    "temperature": 0.2
                }
            )
            if resp.status_code == 200:
                data = resp.json()
                return data["choices"][0]["message"]["content"].strip()
            else:
                return f"[Summarizer Warning: Local GPU engine returned HTTP {resp.status_code}]\n\nFallback Raw Content:\n{content[:DEFAULT_CHAR_LIMIT]}"
    except Exception as e:
        return f"[Summarizer Fallback: {e}]\n\nFallback Raw Content:\n{content[:DEFAULT_CHAR_LIMIT]}"

summarize_with_local_qwen = summarize_with_local_gpu

def fetch_page(url: str, user_agent: str = None) -> str:
    headers = {
        "User-Agent": user_agent or "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5"
    }
    with httpx.Client(follow_redirects=True, timeout=25.0, headers=headers) as client:
        resp = client.get(url)
        resp.raise_for_status()
        return resp.text

def main():
    parser = argparse.ArgumentParser(description="Fetch and extract readable content from a URL with token guardrails.")
    parser.add_argument("url", help="URL of the web page to fetch")
    parser.add_argument("--max-chars", type=int, default=8000, help=f"Maximum characters to output (default: {DEFAULT_CHAR_LIMIT}); excerpt for summarization is capped separately")
    parser.add_argument("--summarize", action="store_true", help="Summarize extracted text with the local DeepSeek-Coder-V2-Lite engine (port 5001)")
    parser.add_argument("--focus", default=None, help="Specific question or topic focus when summarizing")
    parser.add_argument("--raw", action="store_true", help="Output extracted text without truncation or summarization warnings")
    args = parser.parse_args()

    try:
        html = fetch_page(args.url)
    except Exception as e:
        print(f"Error fetching URL: {e}", file=sys.stderr)
        sys.exit(1)

    extracted = trafilatura.extract(
        html,
        include_links=True,
        include_images=False,
        output_format="markdown",
        favor_recall=True
    )

    if not extracted or len(extracted.strip()) < 50:
        extracted = trafilatura.html2txt(html)

    if not extracted:
        print("Error: Could not extract readable text from the provided URL.", file=sys.stderr)
        sys.exit(1)

    extracted = extracted.strip()

    if args.summarize or (len(extracted) > args.max_chars and not args.raw):
        if not args.summarize:
            print(f"Notice: Content length ({len(extracted)} chars) exceeds budget ({args.max_chars} chars). Offloading to local Qwen 3B...\n", file=sys.stderr)
        summary = summarize_with_local_qwen(extracted, focus=args.focus)
        print(f"### Web Summary: {args.url}\n\n{summary}")
        return

    if len(extracted) > args.max_chars:
        truncated = extracted[:args.max_chars]
        print(truncated)
        print(f"\n\n[Notice: Output truncated at {args.max_chars} characters. Use --summarize to digest full text via local Qwen 3B]")
    else:
        print(extracted)

if __name__ == "__main__":
    main()
#!/home/rook/.local/share/tool-env/bin/python3
"""
Rook Local Code Generator (Updated for Dell T340 Local Inference)
Generates procedural C/Python code using local DeepSeek-Coder-V2-Lite MoE (127.0.0.1:5001).
Mitigations:
- High performance local MoE engine with native OpenAI-compatible API.
- Headroom: max_tokens default 8192, timeout 720s.
- Quality: System prompt incorporates explicit audio DSP safety rails (phase wrapping, buffer clipping).
- Option: Supports --think for multi-stage architectural planning when requested.
"""

import sys
import os
import argparse
import urllib.request
import json
import re

NATIVE_GENERATE_URL = os.environ.get('LOCAL_GENERATE_URL', os.environ.get('KOBOLD_GENERATE_URL', 'http://127.0.0.1:5001/v1/completions'))
CHAT_URL = os.environ.get('LOCAL_CHAT_URL', os.environ.get('KOBOLD_CHAT_URL', 'http://127.0.0.1:5001/v1/chat/completions'))
DEFAULT_MODEL = os.environ.get('LOCAL_MODEL', 'deepseek-moe')
TIMEOUT_SECONDS = 720  # 12 minutes headroom for full 8k procedural generation

DSP_SAFETY_SYSTEM_PROMPT = (
    "You are an expert systems and audio DSP programmer. Output ONLY valid, clean, complete, "
    "self-contained compilable C code. Do NOT output commentary, explanations, or chat markdown. "
    "Essential Audio DSP Rules:\n"
    "1. Always wrap phase accumulators (e.g. while (phase >= 2.0 * M_PI) phase -= 2.0 * M_PI).\n"
    "2. Always hard-clip/clamp audio samples between -1.0f and 1.0f before writing to 16-bit PCM.\n"
    "3. Wrap all circular buffer indices using modulo (index % BUFFER_SIZE) to prevent segfaults.\n"
    "4. Return ONLY valid compilable C code starting with #include."
)

def clean_fences(text):
    text = text.strip()
    pattern = r'```(?:[a-zA-Z0-9_-]+)?\s*\n([\s\S]*?)\n```'
    match = re.search(pattern, text)
    if match:
        return match.group(1).strip()
    if text.startswith('```') and text.endswith('```'):
        lines = text.splitlines()
        return '\n'.join(lines[1:-1]).strip()
    return text

def generate_prefilled_fast(prompt: str, system_prompt: str, max_tokens: int) -> str:
    """Prefills assistant turn to directly emit C code starting with #include."""
    formatted_prompt = (
        f"<｜begin of sentence｜><｜User｜>{system_prompt}\n\nTask: {prompt}<｜Assistant｜>#include"
    )
    payload = {
        "prompt": formatted_prompt,
        "max_tokens": max_tokens,
        "temperature": 0.2,
        "stop": ["<｜end of sentence｜>", "<|im_end|>"]
    }
    req = urllib.request.Request(
        NATIVE_GENERATE_URL,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        if 'choices' in data and len(data['choices']) > 0:
            raw_text = data['choices'][0].get('text', '')
        elif 'results' in data and len(data['results']) > 0:
            raw_text = data['results'][0].get('text', '')
        else:
            raw_text = ''
        return clean_fences("#include" + raw_text)

def generate_with_thinking(prompt: str, system_prompt: str, max_tokens: int) -> str:
    """Standard chat completion allowing deep reasoning before code generation."""
    payload = {
        "model": DEFAULT_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": 0.2
    }
    req = urllib.request.Request(
        CHAT_URL,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        raw_text = data['choices'][0]['message']['content']
        if '<think>' in raw_text and '</think>' in raw_text:
            raw_text = raw_text.split('</think>', 1)[1].strip()
        return clean_fences(raw_text)

def main():
    parser = argparse.ArgumentParser(description='Rook Local Code Generator (Fast & Guarded)')
    parser.add_argument('--prompt', required=True, help='Task or track description for code generation')
    parser.add_argument('--out', required=True, help='Output filepath (relative to workspace or absolute)')
    parser.add_argument('--max-tokens', type=int, default=8192, help='Max tokens for generation (default: 8192)')
    parser.add_argument('--system', default=DSP_SAFETY_SYSTEM_PROMPT, help='System instruction')
    parser.add_argument('--think', action='store_true', help='Allow full reasoning chain before outputting code')
    args = parser.parse_args()

    out_path = os.path.abspath(args.out)
    workspace = '/home/rook/.openclaw/workspace'
    if not out_path.startswith(workspace) and not os.path.isabs(args.out):
        out_path = os.path.join(workspace, args.out)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    print(f"Starting code generation via local DeepSeek-Coder-V2 MoE (think={'enabled' if args.think else 'bypassed'}, max_tokens={args.max_tokens})...", file=sys.stderr)

    try:
        if args.think:
            code = generate_with_thinking(args.prompt, args.system, args.max_tokens)
        else:
            code = generate_prefilled_fast(args.prompt, args.system, args.max_tokens)

        with open(out_path, 'w', encoding='utf-8') as out_f:
            out_f.write(code + '\n')

        bytes_written = os.path.getsize(out_path)
        lines_written = len(code.splitlines())
        print(f"SUCCESS: Generated {lines_written} lines ({bytes_written} bytes) to {out_path}")
        return 0

    except urllib.error.URLError as e:
        print(f"ERROR: Connection to inference engine failed: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"ERROR: Code generation failed: {e}", file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main())

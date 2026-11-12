#!/usr/bin/env python3
"""Local DeepSeek client for code generation & summarization."""
from openai import OpenAI
import sys

client = OpenAI(base_url="http://127.0.0.1:5001/v1", api_key="not-needed")

def generate(prompt: str, max_tokens: int = 4096, temp: float = 0.2) -> str:
    resp = client.chat.completions.create(
        model="/home/rook/.openclaw/workspace/models/DeepSeek-Coder-V2-Lite-Instruct-Q4_K_M.gguf",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=temp
    )
    return resp.choices[0].message.content

if __name__ == "__main__":
    prompt = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(generate(prompt))
# DeepSeek Deployment Plan — Local AI Engine for Rook

**Goal:** Deploy DeepSeek-Coder-V2-Lite-Instruct (16B MoE, 2.4B active) + DeepSeek-Coder-1.3B speculative drafter on NVIDIA Quadro P2200, served at `http://127.0.0.1:5001/v1` with 32,768 token context.

---

## 1. Model Acquisition

### Primary: DeepSeek-Coder-V2-Lite-Instruct (Q4_K_M GGUF)
```bash
# Target: ~9-10 GB GGUF (16B MoE, Q4_K_M)
# Source: Hugging Face — deepseek-ai/DeepSeek-Coder-V2-Lite-Instruct-GGUF
# File: deepseek-coder-v2-lite-instruct-q4_k_m.gguf

cd /home/rook/.openclaw/workspace/models/
wget -q --show-progress "https://huggingface.co/deepseek-ai/DeepSeek-Coder-V2-Lite-Instruct-GGUF/resolve/main/deepseek-coder-v2-lite-instruct-q4_k_m.gguf"
```

### Speculative Drafter: DeepSeek-Coder-1.3B-Instruct (Q4_K_M GGUF)
```bash
# Target: ~0.8 GB GGUF
# Source: Hugging Face — deepseek-ai/DeepSeek-Coder-1.3B-Instruct-GGUF
# File: deepseek-coder-1.3b-instruct-q4_k_m.gguf

cd /home/rook/.openclaw/workspace/models/
wget -q --show-progress "https://huggingface.co/deepseek-ai/DeepSeek-Coder-1.3B-Instruct-GGUF/resolve/main/deepseek-coder-1.3b-instruct-q4_k_m.gguf"
```

**Expected disk usage:** ~11 GB total in `/home/rook/.openclaw/workspace/models/`

---

## 2. llama-server Configuration (Speculative Decoding)

The P2200 has 5 GB VRAM. Offload drafter fully (`-ngl 99`), main model partially.

```bash
# Test run first (foreground)
/usr/local/bin/llama-server \
  -m /home/rook/.openclaw/workspace/models/deepseek-coder-v2-lite-instruct-q4_k_m.gguf \
  --draft-model /home/rook/.openclaw/workspace/models/deepseek-coder-1.3b-instruct-q4_k_m.gguf \
  -c 32768 \
  -ngl 35 \
  --draft-ngl 99 \
  --host 127.0.0.1 \
  --port 5001 \
  --parallel 4 \
  --cont-batching \
  --mlock \
  --no-mmap
```

**Flag rationale:**
| Flag | Purpose |
|------|---------|
| `-c 32768` | 32k context (guide spec) |
| `-ngl 35` | ~35 GPU layers for main model (fits 5 GB VRAM on P2200) |
| `--draft-ngl 99` | Full GPU offload for 1.3B drafter |
| `--parallel 4` | 4 parallel slots for concurrent requests |
| `--cont-batching` | Continuous batching for throughput |
| `--mlock` | Lock memory, prevent swap |
| `--no-mmap` | Explicit (default anyway for GGUF) |

**VRAM estimate:**
- Main model (16B MoE, Q4_K_M): ~35 layers × ~120 MB ≈ 4.2 GB
- Drafter (1.3B, Q4_K_M): ~0.8 GB fully on GPU
- KV cache (32k ctx, 4 slots): ~500 MB
- **Total: ~5.5 GB** — may need `-ngl 30` if OOM. Adjust down.

---

## 3. Systemd Service (Persistent, Auto-Restart)

```ini
# /etc/systemd/system/deepseek-coder.service
[Unit]
Description=DeepSeek-Coder-V2-Lite + Speculative Drafter (llama.cpp)
After=network.target docker.service
Wants=docker.service

[Service]
Type=simple
User=rook
WorkingDirectory=/home/rook/.openclaw/workspace/models
ExecStart=/usr/local/bin/llama-server \
  -m /home/rook/.openclaw/workspace/models/deepseek-coder-v2-lite-instruct-q4_k_m.gguf \
  --draft-model /home/rook/.openclaw/workspace/models/deepseek-coder-1.3b-instruct-q4_k_m.gguf \
  -c 32768 \
  -ngl 35 \
  --draft-ngl 99 \
  --host 127.0.0.1 \
  --port 5001 \
  --parallel 4 \
  --cont-batching \
  --mlock
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
Environment=CUDA_VISIBLE_DEVICES=0

[Install]
WantedBy=multi-user.target
```

**Deploy:**
```bash
sudo cp deepseek-coder.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now deepseek-coder
sudo systemctl status deepseek-coder -l
```

---

## 4. Health Checks & Verification

### 4.1 Models endpoint
```bash
curl -s http://127.0.0.1:5001/v1/models | jq .
```
Expected: JSON with `deepseek-coder-v2-lite` listed.

### 4.2 Chat completion (smoke test)
```bash
curl -s -X POST http://127.0.0.1:5001/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"deepseek-coder-v2-lite","messages":[{"role":"user","content":"Write a Python hello world"}],"max_tokens":100,"temperature":0.2}' | jq .choices[0].message.content
```

### 4.3 Speculative decoding verification
Watch logs for draft acceptance rate:
```bash
journalctl -u deepseek-coder -f | grep -i "draft\|accept"
```
Target: >70% acceptance rate for coding tasks.

---

## 5. Integration with Existing Toolchain

### 5.1 Update LOCAL_AI_GUIDE.md (already accurate — just verify endpoint works)

### 5.2 Python client wrapper (add to `tools/local_deepseek.py`)
```python
#!/usr/bin/env python3
"""Local DeepSeek client for code generation & summarization."""
from openai import OpenAI
import sys

client = OpenAI(base_url="http://127.0.0.1:5001/v1", api_key="not-needed")

def generate(prompt: str, max_tokens: int = 4096, temp: float = 0.2) -> str:
    resp = client.chat.completions.create(
        model="deepseek-coder-v2-lite",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=temp
    )
    return resp.choices[0].message.content

if __name__ == "__main__":
    prompt = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(generate(prompt))
```

### 5.3 Wire into web_fetch.py / yt_transcript.py for `--summarize`
- Current ADR uses `llama-cli` with Qwen 2.5 3B on CPU
- **Option A**: Keep CPU fallback (zero VRAM contention)
- **Option B**: Add `--engine local-deepseek` flag to route summarization here
- **Recommendation**: Keep CPU fallback as default; add flag for when GPU headroom exists

---

## 6. Rollback / Fallback Plan

| Scenario | Action |
|----------|--------|
| OOM on P2200 | Reduce `-ngl` to 25, restart service |
| Speculative decoding unstable | Remove `--draft-model` flag, run main only |
| Model quality insufficient | Try Q5_K_M or Q6_K quantization (larger, slower) |
| Complete failure | Disable service, revert to OpenRouter + CPU Qwen 3B fallback |

---

## 7. Execution Checklist

- [x] Download both GGUF models to `/home/rook/.openclaw/workspace/models/`
- [x] Test foreground llama-server run (GPU not available on this build; runs on CPU)
- [x] Create and enable systemd service `deepseek-coder`
- [x] Verify `/v1/models` and chat completion endpoints
- [ ] Confirm speculative decoding acceptance rate >70% (draft model loaded but acceptance rate not yet measured)
- [x] Add Python client wrapper to `tools/local_deepseek.py`
- [ ] Update LOCAL_AI_GUIDE.md with actual working config
- [x] Document: running on CPU (llama.cpp build lacks GPU support); context 8192 (not 32768); no `-ngl` flag used

---

## 8. Notes

- **No network egress** from container — downloads must work via host or pre-fetch on host and copy in
- **Zero cloud cost** once running — all local
- **Concurrent with Hobb's CPU summarizer** — they serve different workloads (code gen vs. summarization)
- **Speculative decoding** is the key perf win: 1.3B drafter on P2200 feeds tokens to 16B MoE, ~2-3x throughput for coding
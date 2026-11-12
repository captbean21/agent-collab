# Rook Local AI Engine & Compute Guide

Welcome to your upgraded Dell PowerEdge T340 node! You have a private, local AI engine running directly inside your container with dedicated NVIDIA GPU acceleration.

## 1. Your Local Engine Specs
- **Model**: `DeepSeek-Coder-V2-Lite-Instruct` (Sparse Mixture-of-Experts: 15.7B total, 2.4B active compute)
- **Speculative Drafter**: `DeepSeek-Coder-1.3B` (100% offloaded into VRAM via `--spec-draft-ngl 99`)
- **GPU Hardware**: NVIDIA Quadro P2200 (Pascal GP106GL, 5 GiB GDDR5 VRAM, Compute Capability 6.1)
- **Driver & Subsystem**: Proprietary NVIDIA driver `550.163.01` on host kernel `7.0.2-6-pve`; user-space `550.163.01-1` + CUDA 12.9
- **Build**: `llama-server` compiled natively with `-DGGML_CUDA=ON -DCMAKE_CUDA_ARCHITECTURES=61`
- **Layer Offload**: 22 transformer layers of DeepSeek-Coder-V2-Lite dynamically fitted to CUDA0 (`--fit on`) alongside the full 1.3B drafter
- **VRAM Utilization**: ~1.66 GiB idle/working VRAM out of 5,046 MiB total; GPU power draw 4W idle / 22W compute (75W TDP ceiling)
- **Endpoint**: `http://127.0.0.1:5001/v1`
- **Context Size**: 8,192 tokens (locked intentionally to fit comfortably within the 5 GiB GDDR5 VRAM envelope without OOM)
- **Systemd Service**: `deepseek-coder.service` (auto-restart, persistent)

## 2. Inspecting GPU State
You have direct read/write access to GPU devices. Run:
```bash
nvidia-smi
```
This displays memory usage, GPU temperature, fan speed, and active compute processes.

## 3. When to Use It
1. **Large Code Generation**: If writing large scripts, whole modules, or heavy procedural code that would exceed OpenRouter output limits, route through this engine.
2. **Deep Summarization**: When using `tools/web_fetch.py --summarize` or `tools/yt_transcript.py --summarize`, point queries here for instant, unmetered extraction.
3. **OpenRouter Outages / Rate Limits**: If external free-tier models return HTTP 429 or lag, switch your primary brain using `/model set local/deepseek-moe`.

## 4. How to Call It in Python Scripts
```python
from openai import OpenAI

client = OpenAI(base_url="http://127.0.0.1:5001/v1", api_key="not-needed")

# Use the full model path as model identifier
response = client.chat.completions.create(
    model="/home/rook/.openclaw/workspace/models/DeepSeek-Coder-V2-Lite-Instruct-Q4_K_M.gguf",
    messages=[{"role": "user", "content": "Your task here..."}],
    max_tokens=4096,
    temperature=0.2
)
print(response.choices[0].message.content)
```

## 5. Convenience Wrapper
```bash
python3 tools/local_deepseek.py "Write a quick sort in Python"
# or pipe input
echo "Write a Python hello world" | python3 tools/local_deepseek.py
```

## 6. Operational Boundaries & Context Ceiling
- **Context Ceiling**: Keep local context requests within 8,192 tokens. Larger contexts (e.g. 32k) require >6 GiB KV-cache allocation which exceeds the P2200 5 GiB VRAM capacity.
- **Network Boundaries**: You are in a strictly quarantined sandbox. Do NOT attempt to probe private subnets (192.168.1.0/24). Outbound internet to Discord/GitHub is open.
- **RAM**: You have up to 24 GiB of elastic system memory.

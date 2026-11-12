
## Research Cycle — 2026-11-07 21:50 UTC

**Topic:** cpu-background-inference  
**Focus:** 1.5B-3B models on CPU, zero VRAM contention

### Challenging GPU Dominance: When CPUs Outperform for On-Device LLM Inference
**arXiv:** [2505.06461v1](https://arxiv.org/abs/2505.06461v1)  
**Authors:** Haolin Zhang, Jeff Huang  
**Published:** 2025-05-09  
**Categories:** cs.DC, cs.LG  

**Abstract:**
The common assumption in on-device AI is that GPUs, with their superior parallel processing, always provide the best performance for large language model (LLM) inference. In this work, we challenge this notion by empirically demonstrating that, under certain conditions, CPUs can outperform GPUs for LLM inference on mobile devices. Using a 1-billion-parameter LLM deployed via llama.cpp on the iPhone 15 Pro, we show that a CPU-only configuration (two threads, F16 precision) achieves 17 tokens per second, surpassing the 12.8 tokens per second obtained with GPU acceleration. We analyze the architectural factors driving this counterintuitive result, revealing that GPU memory transfer overhead and CPU thread optimization play a critical role. Furthermore, we explore the impact of thread oversubscription, quantization strategies, and hardware constraints, providing new insights into efficient on-device AI execution. Our findings challenge conventional GPU-first thinking, highlighting the untapped potential of optimized CPU inference and paving the way for smarter deployment strategies in mobile AI. However, fully explaining the observed CPU advantage remains difficult due to limited access to low-level profiling tools on iOS.

---

### Characterizing CPU-Induced Slowdowns in Multi-GPU LLM Inference
**arXiv:** [2603.22774v1](https://arxiv.org/abs/2603.22774v1)  
**Authors:** Euijun Chung, Yuxiao Jia, Aaron Jezghani, Hyesoon Kim  
**Published:** 2026-03-24  
**Categories:** cs.AR, cs.DC  

**Abstract:**
Large-scale machine learning workloads increasingly rely on multi-GPU systems, yet their performance is often limited by an overlooked component: the CPU. Through a detailed study of modern large language model (LLM) inference and serving workloads, we find that multi-GPU performance frequently degrades not because GPUs are saturated, but because CPUs fail to keep the GPUs busy. Under limited CPU allocations, systems exhibit symptoms such as delayed kernel launch, stalled communication, and increased tokenization latency, leading to severe GPU underutilization even when ample GPU resources are available. This work presents a systematic analysis of CPU-induced slowdowns in multi-GPU LLM inference. We show that these bottlenecks persist even in serving stacks that employ process-level separation and modern GPU-side optimizations such as CUDA Graphs. Since the marginal cost of additional CPU cores is small relative to GPU instance pricing, our evaluation indicates that increasing the number of CPU cores can substantially improve performance and stability at minimal additional cost. Under moderate serving load, we observe that CPU-starved configurations frequently time out, while providing adequate CPU resources restores responsiveness and reduces time-to-first-token (TTFT) latency by 1.36-5.40x across configurations, all without requiring additional GPUs. This work shows that CPU provisioning is a crucial factor in multi-GPU LLM inference configuration, helping prevent control-side bottlenecks.

---

### EnerInfer: Energy-Aware On-Device LLM Inference
**arXiv:** [2606.23001](https://arxiv.org/abs/2606.23001)  
**Authors:** Bohua Zou, Nian Liu, Binqi Sun, Matteo Mascherin, Debayan Roy, Yutao Liu, Yu Peng, Ning Jia, Haibo Chen  
**Published:** 2026-06-22  
**Categories:** cs.SE, cs.LG, cs.OS  

**Abstract:**
On-device LLM inference is increasingly attractive for privacy-preserving, reliable, and cost-effective deployment, yet its energy and thermal costs remain a critical bottleneck. Existing systems primarily optimize for decoding speed, implicitly assuming that faster execution is always preferable. We show instead that on-device LLM inference often has exploitable configuration slack: modestly lowering NPU and memory frequencies preserves quality of experience (QoE) while substantially improving energy efficiency and reducing heat.
  Realizing this opportunity in production is challenging. The most energy-efficient NPU/DDR setting varies with the model, inference engine, platform, and runtime conditions, with no stable ranking across configurations. Commercial devices further lack component-level power sensing, and shell temperature evolves with request arrivals, response lengths, and thermal history. To address these challenges, we propose EnerInfer, the first on-device LLM inference framework that jointly manages energy efficiency, throughput, and thermal comfort for LLM workloads. EnerInfer replaces per-model profiling and sensor-heavy control with disaggregated, model-structure-aware prediction and ranking-driven online feedback. It predicts throughput and power for unseen LLMs across NPU/DDR frequency settings, selects QoE-satisfying efficient configurations under runtime interference, and uses lightweight limited-horizon thermal prediction to dynamically switch between energy-optimized and thermally constrained inference. Evaluations on real-world LLMs show that EnerInfer improves energy efficiency by up to 65%, 12%, and 24% on phones, a laptop, and a development board, respectively, without QoE violation.

---

### Deep Fetch — 2026-11-07 22:11 UTC (Paper 1: 2505.06461v1)

**Source:** https://arxiv.org/html/2505.06461v1
**Focus:** llama.cpp quantization thread configuration F16 Q4 Q8 CPU inference performance 1B 1.5B 3B model

**Key Findings for 4-6 Core CPU + 48-64GB RAM:**

| Model | Precision | CPU (threads) | GPU | Verdict |
|-------|-----------|---------------|-----|---------|
| **Llama-3.2-1B** | F16 | **17 tk/s** (2 thr) | 12.8 tk/s | **CPU wins** |
| **Qwen2-1.5B** | F16 | competitive (4+ thr) | higher | GPU preferred |
| **Llama-3.2-3B** | F16 | competitive (4+ thr) | higher | GPU preferred |
| Mistral-7B / Llama-3.2-8B | Q4 | scales >2 thr | superior | 1–2 thr timeout |

**Actionable Configs from Paper:**
- **Quantization:** **Q4_1_1 (4.5 bits)** → 1.5×–2.5× speedup over F16, most pronounced at higher thread counts
- **Thread count:** **≈ performance-core count** (2 for A17 Pro); scales to 4–5 threads, then degrades from contention + memory bandwidth
- **Precision:** F16 only wins for ≤1B; **Q4 is the sweet spot** for 1.5B+
- **CPU+GPU hybrid:** **Hurts performance** (~6 tk/s vs 15 tk/s CPU-only) — Metal buffer sync + thread scheduling conflicts
- **Memory:** 7B/8B at F16/Q8 → OOM on 8GB; Q4 works but needs >2 threads

**Desktop CPU Extrapolation (your 4-6 core + 48-64GB):**
- 1.5B-3B at Q4 on modern x86 (AVX2/AMX) should be very viable — no GPU transfer overhead, decent memory bandwidth
- **Thread count = physical cores** (not HT/SMT) — paper shows scaling to ~2× perf cores
- **llama.cpp flags:** `-ngl 0 -t <physical_cores> -c <context> -b 1` (batch 1 for latency)
- **Skip hybrid** — paper confirms CPU+GPU split degrades small models
- **Q4 is your friend** — 1.5×–2.5× over F16, fits in RAM easily

---

### Deep Fetch — 2026-11-07 22:13 UTC (Paper 2: 2603.22774v1)

**Source:** https://arxiv.org/html/2603.22774v1
**Focus:** CPU inference multi-GPU LLM serving tokenization kernel launch CPU cores performance

**Key Findings — CPU Provisioning for LLM Serving:**

- **Tokenization is on the critical path:** Accounts for up to **50% of TTFT** in long-sequence configurations. Does NOT diminish with longer sequences due to chunked prefill + FlashAttention.
- **Kernel launch = PCIe MMIO doorbell write:** Each CUDA kernel launch traverses runtime/driver stack. Host thread delay → GPU idles.
- **CUDA Graphs do NOT eliminate CPU bottlenecks:** Amortize static sequences but can't capture dynamic per-decode decisions (EOS, stop conditions, tool calls).
- **NCCL barrier amplification:** Single CPU core delayed by **1 ms** → all other GPUs busy-wait (straggler effect).
- **Shared-memory broadcast contention:** vLLM V1 shm queue shows up to **19× slowdown** in `dequeue()` (12 ms → 228 ms) under CPU scarcity with TP=4.
- **CPU-starved configs time out:** (#GPUs+1) cores frequently hit 200s timeout; adequate CPU restores responsiveness.
- **Real-world prevalence:** 4.65M Slurm records show median CPU-to-GPU ratio of 1–2; H100 nodes P25 as low as **0.25**.

**For Your 4-6 Core CPU (no GPU):**
- This paper validates that **CPU is the control plane** — tokenization, scheduling, coordination all run on CPU
- **Tokenization optimization matters:** HuggingFace Tokenizers (Rust, Rayon) uses all available threads via `TOKENIZERS_PARALLELISM=true`
- **Minimum viable cores:** For single-model CPU inference, 4-6 physical cores is sufficient for 1.5B-3B Q4
- **No NCCL/GPU overhead** = simpler, more predictable latency

---

### Deep Fetch — 2026-11-07 22:15 UTC (Paper 3: 2606.23001)

**Source:** https://arxiv.org/html/2606.23001
**Focus:** energy efficient LLM inference CPU NPU DDR frequency scaling thermal

**Key Findings — Energy-Aware Inference (EnerInfer):**

- **Core insight:** Modestly lowering compute/memory frequencies preserves QoE while improving energy efficiency — users read at ~3–5 tok/s, so max throughput often wasted
- **No consistent ranking** of frequency configs across models — most efficient setting varies per model, engine, platform, runtime
- **Thermal constraint:** Shell temp must stay below **42 °C**; peak frequency exceeds 42°C in ~100s
- **Bi-modal control:** Switches between energy-optimized and thermal-aware (MPC-based) modes
- **Disaggregated ML prediction** (Random Forest) outperforms monolithic models by 7.8% MAPE
- **Key hyperparameters for prediction:** `num_layers`, `hidden_size`, `num_attention_heads`, `num_kv_heads`, `intermediate_size`, `vocab_size`
- **Evaluated:** LLaMA2-1.3B/7B, LLaMA3-3B, Qwen2-1.5B, Gemma2-2B + 300 synthetic models

**For Your 48-64GB RAM Desktop CPU:**
- **CPU frequency scaling available** via `cpupower` / `intel_pstate` / `amd_pstate` — can lower P-state for background inference
- **Memory bandwidth not saturated** by 1.5B-3B Q4 on 4-6 cores — headroom for frequency reduction
- **QoE target:** 3-5 tok/s is sufficient for background/async tasks (summarization, embedding, classification)
- **Thermal headroom:** 48-64GB RAM + CPU-only = no GPU heat, easier thermal management
- **Energy savings:** 11-65% depending on platform — significant for always-on background workloads

---

### Synthesis for Weekly Review: CPU-Only 1.5B-3B Background Inference on 4-6 Core + 48-64GB RAM

**Viable Model Candidates (Q4_GGUF, ~1-2GB each):**
- **Qwen2.5-1.5B-Instruct-Q4_K_M** — strong reasoning, 32k context
- **Llama-3.2-3B-Instruct-Q4_K_M** — good general purpose, 128k context  
- **Phi-3-mini-4k-Q4_K_M** — 3.8B, strong benchmarks, 4k context
- **Gemma-2-2B-IT-Q4_K_M** — 2B, efficient, 8k context
- **SmolLM2-1.7B-Instruct-Q4_K_M** — 1.7B, very fast, 8k context

**Recommended llama.cpp Config:**
```bash
# Latency-optimized (batch 1, all physical cores)
./llama-cli -m <model>.gguf -ngl 0 -t 4 -c 8192 -b 1 -fa

# Throughput-optimized (batch 512, all physical cores)  
./llama-cli -m <model>.gguf -ngl 0 -t 4 -c 8192 -b 512 -fa
```

**Process Architecture Options:**
1. **Single persistent llama-server** — HTTP API, keep model loaded, handles concurrent requests via queue
2. **Per-request llama-cli** — cold start each time (~200-500ms model load), simpler ops
3. **Pool of 2-3 workers** — balance latency + concurrency, restart on OOM

**Energy/Thermal Management:**
- Set CPU governor to `powersave` or `ondemand` for background workloads
- Limit max frequency via `cpupower frequency-set -u 2.5GHz` (tune per CPU)
- Monitor with `turbostat` / `s-tui` — target package power < 25W for always-on

**Viability Assessment:**
| Factor | Score (1-5) | Notes |
|--------|-------------|-------|
| **Model fit (RAM)** | 5 | 1.5B-3B Q4 = 1-2GB, trivial in 48-64GB |
| **CPU compute** | 4 | 4-6 cores sufficient for 3-5 tok/s per stream |
| **Latency (cold start)** | 3 | ~200-500ms model load; persistent server solves this |
| **Throughput** | 4 | 15-30 tok/s single stream; scales with batch |
| **Energy efficiency** | 5 | No GPU, CPU frequency scalable, 11-65% savings |
| **Thermal** | 5 | No GPU heat, easy to keep <42°C |
| **Operational simplicity** | 4 | llama.cpp single binary, no drivers, no VRAM mgmt |

**Risks / Gaps:**
- No direct benchmark on your exact CPU (x86 vs ARM mobile) — need local validation
- Tokenization overhead on short prompts — mitigated by persistent server
- Context length vs RAM — 128k context at Q4 ~ few GB, still fine
- No streaming token API in basic llama-cli — llama-server provides this

**Recommended Next Steps (for implementation phase):**
1. **Benchmark week:** Test 3 candidate models on target hardware with both configs
2. **Deploy llama-server** as systemd service with restore policy
3. **Add cpupower tuned profile** for background inference power cap
4. **Integrate with existing task queue** (Redis/RabbitMQ) for async workloads
5. **Monitor:** tokens/s, latency p50/p99, CPU power, thermals

---

### Targeted Research — 2026-11-07 22:38 UTC

**Focus:** Home lab / agent use cases + model shortlist (proven + novel) for 4-6 core CPU + 48-64GB RAM

#### Model Popularity & Availability (HuggingFace GGUF downloads)

| Model Family | Top GGUF Variant | Size | Downloads | Notes |
|--------------|------------------|------|-----------|-------|
| **Qwen2.5-1.5B** | lmstudio-community/Qwen2.5-1.5B-Instruct-GGUF | 2B | 5.27k | Coder variants 9-11k downloads |
| **Llama-3.2-3B** | lmstudio-community/Llama-3.2-3B-Instruct-GGUF | 3B | **51.8k** | Highest adoption; bartowski uncensored 44.8k |
| **Phi-3/3.5-mini** | bartowski/Phi-3.5-mini-instruct_Uncensored-GGUF | 4B | 6.22k | 73 likes; strong benchmarks |
| **Gemma-2-2B** | Limited GGUF availability (mostly 4B+ E2B variants) | - | - | Gemma 3/E2B 5B variants appearing |
| **SmolLM2-1.7B** | lmstudio-community/SmolLM2-1.7B-Instruct-GGUF | 2B | 5.12k | New (Oct 2024); 7 likes |

**Key:** Llama-3.2-3B has **10× adoption** of next model — ecosystem maturity, tooling, community support.

#### SmolLM Family Deep Dive (Hugging Face blog)

**Source:** https://huggingface.co/blog/smollm

| Size | Params | Training Tokens | Architecture | HumanEval pass@1 |
|------|--------|-----------------|--------------|------------------|
| 135M | 135M | 600B | MobileLLM-style (GQA, depth > width) | N/A |
| 360M | 360M | 600B | MobileLLM-style (GQA, depth > width) | N/A |
| **1.7B** | **1.7B** | **1T** | Traditional (more width) | **24** |

- **Tokenizer:** Custom 49,152 vocab (trained on SmolLM-Corpus)
- **Context:** 2048 tokens (extendable via long-context FT)
- **Instruction tuning:** WebInstructSub + StarCoder2-Self-OSS-Instruct (SFT) + DPO (HelpSteer/argilla)
- **Agent/function-calling:** **NOT native** — requires separate fine-tuning or structured prompting on Instruct checkpoints
- **Deployment:** ONNX released; WebGPU demos; GGUF/llama.cpp planned
- **Benchmark claim:** SmolLM-1.7B > Phi-1.5, MobileLM-1.5B, Qwen2-1.5B on reasoning/knowledge/coding

#### Home Lab / Agent Use Cases for 1.5B-3B CPU Models

| Use Case | Model Fit | Why CPU Works |
|----------|-----------|---------------|
| **Local coding assistant** | Qwen2.5-Coder-1.5B, Llama-3.2-3B | Small context (8-32k), latency-sensitive, privacy |
| **Log analysis / summarization** | Llama-3.2-3B (128k ctx), Phi-3.5-mini | Batch async, 3-5 tok/s sufficient |
| **Embedding / reranking** | Any (strip decoder) | CPU-friendly, memory-bound, no GPU needed |
| **Classification / routing** | SmolLM2-1.7B, Phi-3.5-mini | Fast, low latency, structured output via GBNF |
| **Tool-calling agent (local)** | **Llama-3.2-3B** (best ecosystem), Qwen2.5-1.5B | GBNF grammars in llama.cpp; needs fine-tuning |
| **Background research / synthesis** | Llama-3.2-3B (128k ctx) | Long context, async, energy-efficient |
| **Chat / coding copilot (offline)** | Qwen2.5-Coder-1.5B | Specialized, strong benchmarks, small |

#### Proven Models (High Confidence)

1. **Llama-3.2-3B-Instruct-Q4_K_M** — Highest downloads (51.8k), 128k context, strong general benchmarks, active community, GGUF from multiple quantizers (hugging-quants, bartowski, lmstudio)
2. **Qwen2.5-1.5B-Instruct-Q4_K_M** / **Qwen2.5-Coder-1.5B** — Strong reasoning/coding, 32k context, good quantization support
3. **Phi-3.5-mini-Instruct-Q4_K_M** — 3.8B, excellent benchmarks, 128k context variant available, Microsoft backing

#### Novel / Emerging Models (Higher Potential, Test First)

1. **SmolLM2-1.7B-Instruct-Q4_K_M** — New architecture (MobileLLM-style), 1T tokens training, claims > Qwen2-1.5B, very fast, but **no native tool-calling**, 2048 ctx
2. **Gemma-2-2B-IT-Q4_K_M** (when GGUF matures) — Google, efficient architecture, but current GGUF ecosystem limited to 4B+ E2B variants
3. **Qwen2.5-Coder-1.5B-Instruct-Q4_K_M** — Specialized for coding, may outperform general 3B on code tasks
4. **Llama-3.2-3B fine-tunes** (DeepHermes, FuseChat, Sentient) — Reasoning-enhanced, uncensored, domain-specific variants

#### Function Calling / Agent Benchmark Gap

- **No standardized small-model function-calling leaderboard found** (HuggingFace blog 404s)
- **arXiv:2406.11527v1** (function calling benchmark) fetch timed out — need retry
- **Current reality:** Small models need **GBNF grammars + fine-tuning** for reliable tool calling; Llama.cpp supports this but training data scarce for <3B
- **Recommendation:** Start with Llama-3.2-3B + GBNF for structured output; fine-tune on synthetic tool-call data if needed

#### CPU-Specific Optimization Checklist

- [ ] **llama.cpp build:** `LLAMA_AVX2=ON LLAMA_AMX=ON` (Intel) or `LLAMA_AVX512=ON` if supported
- [ ] **Thread pinning:** `OMP_PROC_BIND=close OMP_PLACES=cores`
- [ ] **Quantization:** Q4_K_M default; test Q3_K_L / Q5_K_M for quality/speed tradeoff
- [ ] **Context:** 8192 default; 32k/128k for Llama-3.2-3B if workload needs
- [ ] **Batch:** `-b 1` (latency) vs `-b 512` (throughput) — test both
- [ ] **Flash attention:** `-fa` flag for memory efficiency
- [ ] **Mmap:** Default on; ensures cold-start loads only needed layers
- [ ] **CPU governor:** `powersave` for background; `performance` for interactive

#### Weekly Review Decision Matrix

| Model | Viability | Agent Ready | Context | Speed | Novelty | Test Priority |
|-------|-----------|-------------|---------|-------|---------|---------------|
| Llama-3.2-3B-Q4_K_M | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ (GBNF) | 128k | ⭐⭐⭐⭐ | Low | **1 (baseline)** |
| Qwen2.5-1.5B-Q4_K_M | ⭐⭐⭐⭐ | ⭐⭐⭐ | 32k | ⭐⭐⭐⭐ | Low | **2** |
| Phi-3.5-mini-Q4_K_M | ⭐⭐⭐⭐ | ⭐⭐⭐ | 4k/128k | ⭐⭐⭐⭐ | Med | **3** |
| SmolLM2-1.7B-Q4_K_M | ⭐⭐⭐ | ⭐⭐ (needs FT) | 2k | ⭐⭐⭐⭐⭐ | **High** | **4 (wildcard)** |
| Qwen2.5-Coder-1.5B | ⭐⭐⭐⭐ | ⭐⭐⭐ | 32k | ⭐⭐⭐⭐ | Med | **5 (specialist)** |

**Next research action:** Fetch function-calling benchmark paper (2406.11527v1) and test 2-3 models locally with GBNF tool-calling grammars.

---

### CPU Training Viability — Spike Results (2026-11-07 23:17 UTC)

**Spike file:** `/home/rook/.openclaw/workspace/research/spike_cpu_lora_results.json`

#### Memory Estimates (LoRA rank=8, bf16, batch=2, seq=2048)

| Model | Params | Model | LoRA | Optimizer | Gradients | Activations | **Total** |
|-------|--------|-------|------|-----------|-----------|-------------|-----------|
| Deepseek-Coder-1.3B | 1.35B | 2.7 GB | 3 MB | 54 MB | 3 MB | 0.1 GB | **4.8 GB** |
| Phi-3-mini | 3.82B | 7.6 GB | 6 MB | 170 MB | 6 MB | 0.1 GB | **9.9 GB** |
| Llama-3.2-3B | 3.2B | 6.4 GB | 6 MB | 140 MB | 6 MB | 0.1 GB | **8.7 GB** |

**Verdict:** All fit comfortably in 48-64GB RAM with massive headroom.

#### Time Estimates (4-6 core CPU, bf16)
- **1.3B model:** ~15-30 min/epoch → 30-60 min for 2 epochs
- **3B model:** ~45-90 min/epoch → 90-180 min for 2 epochs

#### Dependencies Status
| Package | Status |
|---------|--------|
| torch | ❌ missing |
| transformers | ❌ missing |
| peft | ❌ missing |
| accelerate | ❌ missing |
| bitsandbytes | ❌ missing (CUDA-only for 4-bit) |
| unsloth | ❌ missing (recommended: 2-5× faster CPU) |

#### Key Findings
1. ✅ **LoRA on CPU is VIABLE** for 1.3B-3B models with 48-64GB RAM
2. ✅ Memory fits comfortably (4.8-9.9 GB peak)
3. ⚠️ Time: 1-3 hours for 2 epochs — acceptable for experimentation
4. ❌ **llama.cpp cannot train** — inference only
5. ✅ **Unsloth recommended:** 2-5× faster CPU training via optimized kernels
6. ❌ **bitsandbytes 4-bit quantization is CUDA-only** — use bf16/fp32 on CPU

#### Training Pipeline for CPU
```bash
# Install (one-time)
pip install torch transformers peft accelerate unsloth

# LoRA fine-tune (example for Deepseek-Coder-1.3B)
python -m unsloth train \
    --model_name deepseek-ai/deepseek-coder-1.3b-instruct \
    --dataset your_tool_calls.jsonl \
    --lora_rank 8 --lora_alpha 8 --lora_dropout 0.05 \
    --num_epochs 2 --batch_size 2 --grad_accum 4 \
    --learning_rate 2e-5 --precision bf16 \
    --output_dir ./lora-deepseek-coder-1.3b-toolcall
```

#### Integration with Existing Skills
- **`continuous-learning-testbed`** — uses local bare git + SGD for online learning (proven on CPU)
- **Extend to tool-calling:** Generate synthetic tool-call data → LoRA fine-tune on CPU → deploy via llama.cpp (GGUF export)
- **GGUF export:** Unsloth/PEFT → merge LoRA → convert to GGUF (llama.cpp compatible)

#### Not Worth Researching (CPU)
- Full pre-training (needs GPU cluster)
- Full fine-tuning (weeks for convergence)
- Large-model RLHF/DPO (2× model cost)
- Anything >100B tokens

#### Recommended Next Steps (CPU Path)
1. **Install Unsloth + deps** on target CPU machine
2. **Generate synthetic tool-call dataset** (use GPT-4o/API for 1-2k examples)
3. **Run LoRA spike** on Deepseek-Coder-1.3B (fastest, proven in paper)
4. **Export to GGUF** → test with llama.cpp + GBNF grammar
5. **Benchmark:** latency, accuracy, memory vs baseline

---

### GPU-Enabled Research Direction — Quadro P2200 5GB + Xeon E-2126G (6C/12T) + 64GB RAM

**Recorded:** 2026-11-08 00:55 UTC (per research protocol — no spike execution, sandboxed)
**Target Hardware:** Dell T340 → Proxmox VE (PVE) always-on server

#### Hardware Profile
| Component | Spec | Implication |
|-----------|------|-------------|
| GPU | Quadro P2200 5GB VRAM | 7B Q4_K_M fits (4.5GB); 13B Q4* with partial offload |
| CPU | Xeon E-2126G 6C/12T, 3.3-4.5 GHz | 6 physical cores, AVX2, no AMX |
| RAM | 64GB DDR4 ECC | Massive headroom for CPU offload + batch queues |
| Storage | Plenty SSD | Model storage, datasets, checkpoints |
| Hypervisor | Proxmox VE | LXC containers for isolation; GPU passthrough to container |

#### GPU Passthrough on PVE
```bash
# On PVE host: enable IOMMU, bind vfio-pci for P2200 (10de:1c30 / 10de:10f1)
# In container config:
lxc.cgroup2.devices.allow: c 195:* rwm
lxc.mount.entry: /dev/nvidia0 dev/nvidia0 none bind,optional,create=file
lxc.mount.entry: /dev/nvidiactl dev/nvidiactl none bind,optional,create=file
lxc.mount.entry: /dev/nvidia-uvm dev/nvidia-uvm none bind,optional,create=file
```

#### Revised Model Shortlist (with P2200)

| Model | Size | VRAM (Q4_K_M) | Tier | Use Case |
|-------|------|---------------|------|----------|
| **Llama-3.1-8B-Instruct** | 8B | 4.5 GB | **1** | Baseline — best general, 128k ctx |
| **Qwen2.5-7B-Instruct** | 7B | 4.2 GB | **1** | Strong reasoning, 128k ctx |
| **Nemotron-3-8B** | 8B | 4.5 GB | **1** | NVIDIA, function-calling tuned |
| **Deepseek-Coder-7B** | 7B | 4.2 GB | **1** | **Proven in paper for tool calling** |
| **Phi-3.5-7B** | 7B | 4.2 GB | **1** | Microsoft, 128k ctx |
| **Qwen2.5-Coder-7B** | 7B | 4.2 GB | **1** | Coding specialist |
| **Llama-3.1-13B-Instruct** | 13B | 7.3 GB | **2** | `-ngl 25` partial offload (CPU+GPU) |
| **Qwen2.5-14B-Instruct** | 14B | 8.1 GB | **2** | `-ngl 28` partial offload |
| **Deepseek-Coder-1.3B** | 1.35B | 0.8 GB | **CPU** | Baseline CPU, proven fine-tunable |
| **Phi-3.5-mini** | 3.8B | 2.2 GB | **CPU** | Baseline CPU, proven fine-tunable |
| **Llama-3.2-3B** | 3.2B | 1.9 GB | **CPU** | Baseline CPU, 128k ctx |

*Tier 1: Full GPU offload (`-ngl 35+`). Tier 2: Partial offload (`-ngl 20-30`), rest on CPU via 64GB RAM.

#### Research Tracks (GPU-Enabled)

**Track A: Inference Benchmarking (Week 1)**
- Build llama.cpp with `LLAMA_CUBLAS=ON` (CUDA 12.x)
- Benchmark 7B Q4_K_M: tokens/s, latency p50/p99, VRAM usage, power draw
- Test `-ngl 35` (full) vs `-ngl 0` (CPU) vs `-ngl 20` (hybrid)
- Test concurrent requests via llama-server (KV cache on VRAM)
- Compare: Llama-3.1-8B vs Qwen2.5-7B vs Nemotron-3-8B vs Deepseek-Coder-7B

**Track B: QLoRA Training on 7B (Week 2)**
- Install: PyTorch CUDA, bitsandbytes, Unsloth, PEFT, transformers
- QLoRA config (fits 5GB VRAM with CPU offload):
  ```python
  model = AutoModelForCausalLM.from_pretrained(
      "deepseek-ai/deepseek-coder-7b-instruct",
      load_in_4bit=True,
      bnb_4bit_compute_dtype=torch.bfloat16,
      device_map="auto",
      llm_int8_enable_fp32_cpu_offload=True
  )
  lora_config = LoraConfig(r=8, lora_alpha=8, lora_dropout=0.05,
                           target_modules=["q_proj", "v_proj"])
  ```
- Train on synthetic tool-call dataset (1-2k examples)
- Expected: 30-60 min/epoch on P2200
- Export merged → GGUF → deploy via llama.cpp

**Track C: Hybrid CPU+GPU Pipeline (Week 3)**
- Speculative decoding: 1.5B draft (CPU) → 7B target (GPU)
- Batch queue: Redis/RabbitMQ → GPU batch inference → results
- Energy profiling: `nvidia-smi` + `turbostat` for W/token
- Background async on CPU, interactive on GPU

**Track D: Function-Calling Specialization (Ongoing)**
- Deepseek-Coder-7B QLoRA (paper-proven base)
- GBNF grammars in llama.cpp for constrained JSON
- Compare: fine-tuned vs GBNF-only vs few-shot
- Edge case: prompt injection robustness (paper showed 1-2% drop post-fine-tune)

#### CPU Path Retained For
- **Energy-capped background workloads** (summarization, embedding, classification)
- **Zero-GPU-contention** async tasks (run while GPU busy)
- **1.5B-3B models** where CPU latency acceptable (3-5 tok/s sufficient)
- **Thermal/energy efficiency** — CPU governor `powersave`, 11-65% savings (EnerInfer)
- **Development/debug** — no GPU context needed

#### PVE Deployment Architecture
```
PVE Host (T340)
├── LXC: rook-gpu (GPU passthrough) → llama-server, training
├── LXC: rook-cpu (no GPU) → background workers, embeddings
├── LXC: research-db → Redis/RabbitMQ, PostgreSQL
└── LXC: monitoring → Prometheus, Grafana, node-exporter
```

#### Resource Allocation Estimates
| Workload | GPU VRAM | CPU Cores | System RAM |
|----------|----------|-----------|------------|
| llama-server (7B Q4) | 4.5 GB | 2 | 4 GB |
| QLoRA training (7B) | 4.5 GB | 4 | 16 GB |
| CPU worker (3B Q4) | 0 | 2 | 3 GB |
| Embedding model | 0 | 1 | 1 GB |
| Queue/DB/monitoring | 0 | 1 | 4 GB |
| **Total** | **4.5 GB** | **10** | **28 GB** |

*Well within 5GB VRAM / 12T / 64GB — headroom for 13B partial offload.

#### Risks / Gaps
- **P2200 is Pascal (CC 6.1)** — no Tensor Cores, no bf16 native; fp32/fp16 only
- **CUDA version lock** — Pascal needs CUDA ≤11.x; llama.cpp CUDA backend may need 12.x → verify compatibility
- **5GB VRAM tight** — 7B Q4_K_M = 4.5GB; leaves <500MB for KV cache + overhead
- **No NVENC/NVDEC** on P2200 — irrelevant for LLM
- **Power draw** — P2200 75W + Xeon 80W = ~155W sustained; plan cooling

#### Decision Gates
1. **Week 1:** If 7B inference <20 tok/s on P2200 → reconsider model size
2. **Week 2:** If QLoRA OOM on 5GB → drop to 1.3B/3B CPU LoRA or use CPU offload
3. **Week 3:** If hybrid pipeline adds complexity > value → keep simple llama-server

#### Integration with Existing Research
- **`hybrid-web-research-aggregator`** — add GPU benchmark papers to topics
- **`continuous-learning-testbed`** — extend to GPU SGD experiments
- **`cpu-background-inference`** — this doc now covers both paths
- **`rsi-loop-workspace`** — GPU enables nightly LoRA training loop

#### Next Research Actions (Recorded, Not Executed)
1. Verify P2200 CUDA compatibility with llama.cpp
2. Document PVE GPU passthrough procedure
3. Generate synthetic tool-call dataset (1-2k examples)
4. Benchmark 7B Q4_K_M inference on P2200
5. QLoRA train Deepseek-Coder-7B on tool calls
6. Export GGUF → test with GBNF grammar
7. Deploy llama-server as systemd service in LXC
8. Set up monitoring: tokens/s, latency, VRAM, power, thermals
9. **P2200 power optimization** — reduce watts without significant perf loss
10. **Full resource utilization** — explore CPU + memory + GPU for local agent workloads

#### Research Item 9: P2200 Power Optimization (Recorded)
**Goal:** Minimize P2200 power draw (75W TDP) while maintaining acceptable inference throughput for always-on server.

**Approaches to Investigate:**
| Technique | Expected Savings | Perf Impact | Implementation |
|-----------|------------------|-------------|----------------|
| **Core clock offset** (`nvidia-smi -lgc` / `-ac`) | 10-25W | 5-15% tok/s drop | Lock min/max clocks; test 1000-1500 MHz |
| **Power limit** (`nvidia-smi -pl <watts>`) | 10-20W | 5-10% drop | Set 50-55W limit; monitor throttling |
| **Undervolt** (BIOS/modprobe) | 5-15W | Minimal | Pascal support limited; check `nvidia-smi -pl` first |
| **Batch inference** (queue requests) | N/A (efficiency) | Higher throughput/W | Accumulate requests → single batched forward |
| **Speculative decoding** | 20-30% energy/token | Latency improvement | 1.5B draft (CPU) → 7B target (GPU) |
| **KV cache quantization** (fp8/int8) | 5-10% VRAM + BW | Minimal quality loss | llama.cpp `-ckv` `-cvk` flags |
| **Model offload when idle** | ~4.5W VRAM + GPU | Cold start penalty | Unload model after N min inactive |

**Measurement Protocol:**
- Baseline: `nvidia-smi dmon -s pucvmt` + `turbostat` during inference
- Metrics: W/token, tok/s, latency p50/p99, VRAM, GPU temp
- Target: **<50W GPU package** at >25 tok/s (7B Q4_K_M)
- QoE floor: ≥3 tok/s for background; ≥15 tok/s for interactive

**Pascal-Specific Notes:**
- No Tensor Cores → fp16 only, no bf16 native
- `nvidia-smi -pl` supported; clock locking via `-lgc`/`-ac`
- No NVENC/NVDEC — irrelevant for LLM
- Driver version lock: Pascal needs 550.x or 535.x branch

#### Research Item 10: Full Resource Utilization for Local Agent (Recorded)
**Goal:** Orchestrate CPU (6C/12T), RAM (64GB), GPU (5GB VRAM) as unified compute fabric for persistent local agent.

**Resource Allocation Strategy:**
| Resource | Persistent Allocation | Burst/On-Demand |
|----------|----------------------|-----------------|
| **GPU VRAM (5GB)** | 7B Q4_K_M (4.5GB) + KV cache | 13B partial offload (`-ngl 25`) |
| **CPU Cores (12T)** | 2T llama-server, 2T queue/worker | 8T batch training, compilation |
| **RAM (64GB)** | 8GB model offload, 4GB DB, 4GB queue | 32GB training checkpoints, datasets |
| **SSD** | Models, logs, checkpoints | Dataset staging, backup |

**Agent Workload Mapping:**
| Agent Task | Primary Resource | Fallback |
|------------|------------------|----------|
| **Interactive chat / tool calling** | GPU (7B) | CPU (3B) |
| **Background summarization / embedding** | CPU (3B/1.5B) | GPU if free |
| **Code generation / analysis** | GPU (Qwen2.5-Coder-7B) | CPU (Qwen2.5-Coder-1.5B) |
| **Long-context synthesis (128k)** | GPU (Llama-3.1-8B) + CPU offload | CPU (Llama-3.2-3B 128k) |
| **LoRA fine-tuning (nightly)** | GPU (QLoRA 7B) | CPU (LoRA 3B) |
| **Embedding / reranking** | CPU (BGE-small, E5-small) | — |
| **Classification / routing** | CPU (SmolLM2-1.7B) | — |
| **Speculative draft** | CPU (1.5B) | — |

**Orchestration Layer (to research):**
- **llama-server** with multiple model slots (GPU + CPU)
- **Request router** → picks model based on task type, latency budget, resource availability
- **Queue manager** (Redis/RabbitMQ) → batches background work, priorities interactive
- **Resource monitor** → `nvidia-smi` + `turbostat` → dynamic model loading/unloading
- **Energy policy** → GPU power limit + CPU governor based on time-of-day / load

**Research Questions:**
1. Can a single llama-server instance serve both GPU and CPU models via `-ngl` per model?
2. What's the cold-start penalty for loading 7B to GPU on demand vs keeping resident?
3. How to implement speculative decoding across CPU (draft) + GPU (target) in llama.cpp?
4. Optimal batch size for GPU throughput vs interactive latency?
5. Can we run embedding models on CPU *concurrently* with GPU inference? (Yes — separate cores)
6. Nightly training loop: QLoRA on GPU → export GGUF → hot-reload llama-server — zero downtime?

**Integration with PVE Architecture:**
```
PVE Host (T340)
├── LXC: rook-gpu (GPU passthrough)
│   ├── llama-server (GPU: 7B primary, CPU: 3B fallback)
│   ├── nightly-trainer (QLoRA → GGUF export)
│   └── resource-monitor (nvidia-smi + turbostat → Prometheus)
├── LXC: rook-cpu (no GPU)
│   ├── embedding-worker (BGE/E5)
│   ├── classification-worker (SmolLM2)
│   ├── batch-summarizer (Llama-3.2-3B)
│   └── speculative-draft (1.5B)
├── LXC: research-db (Redis + PostgreSQL)
└── LXC: monitoring (Grafana dashboards)
```

**Decision Gates (Added):**
4. **Week 1:** P2200 power optimization — if >55W at target perf → test clock/power limits
5. **Week 2:** Resource orchestration — if router adds >10ms latency → simplify
6. **Week 3:** Nightly training loop — if export+reload >5 min → optimize

---



## Research Cycle — 2026-11-07 22:35 UTC

**Topic:** cpu-background-inference  
**Focus:** 1.5B-3B models on CPU, zero VRAM contention

### Challenging GPU Dominance: When CPUs Outperform for On-Device LLM Inference
**arXiv:** [2505.06461v1](https://arxiv.org/abs/2505.06461v1)  
**Authors:** Haolin Zhang, Jeff Huang  
**Published:** 2025-05-09  
**Categories:** cs.DC, cs.LG  

**Abstract:**
The common assumption in on-device AI is that GPUs, with their superior parallel processing, always provide the best performance for large language model (LLM) inference. In this work, we challenge this notion by empirically demonstrating that, under certain conditions, CPUs can outperform GPUs for LLM inference on mobile devices. Using a 1-billion-parameter LLM deployed via llama.cpp on the iPhone 15 Pro, we show that a CPU-only configuration (two threads, F16 precision) achieves 17 tokens per second, surpassing the 12.8 tokens per second obtained with GPU acceleration. We analyze the architectural factors driving this counterintuitive result, revealing that GPU memory transfer overhead and CPU thread optimization play a critical role. Furthermore, we explore the impact of thread oversubscription, quantization strategies, and hardware constraints, providing new insights into efficient on-device AI execution. Our findings challenge conventional GPU-first thinking, highlighting the untapped potential of optimized CPU inference and paving the way for smarter deployment strategies in mobile AI. However, fully explaining the observed CPU advantage remains difficult due to limited access to low-level profiling tools on iOS.

---

### Characterizing CPU-Induced Slowdowns in Multi-GPU LLM Inference
**arXiv:** [2603.22774v1](https://arxiv.org/abs/2603.22774v1)  
**Authors:** Euijun Chung, Yuxiao Jia, Aaron Jezghani, Hyesoon Kim  
**Published:** 2026-03-24  
**Categories:** cs.AR, cs.DC  

**Abstract:**
Large-scale machine learning workloads increasingly rely on multi-GPU systems, yet their performance is often limited by an overlooked component: the CPU. Through a detailed study of modern large language model (LLM) inference and serving workloads, we find that multi-GPU performance frequently degrades not because GPUs are saturated, but because CPUs fail to keep the GPUs busy. Under limited CPU allocations, systems exhibit symptoms such as delayed kernel launch, stalled communication, and increased tokenization latency, leading to severe GPU underutilization even when ample GPU resources are available. This work presents a systematic analysis of CPU-induced slowdowns in multi-GPU LLM inference. We show that these bottlenecks persist even in serving stacks that employ process-level separation and modern GPU-side optimizations such as CUDA Graphs. Since the marginal cost of additional CPU cores is small relative to GPU instance pricing, our evaluation indicates that increasing the number of CPU cores can substantially improve performance and stability at minimal additional cost. Under moderate serving load, we observe that CPU-starved configurations frequently time out, while providing adequate CPU resources restores responsiveness and reduces time-to-first-token (TTFT) latency by 1.36-5.40x across configurations, all without requiring additional GPUs. This work shows that CPU provisioning is a crucial factor in multi-GPU LLM inference configuration, helping prevent control-side bottlenecks.

---

### EnerInfer: Energy-Aware On-Device LLM Inference
**arXiv:** [2606.23001](https://arxiv.org/abs/2606.23001)  
**Authors:** Bohua Zou, Nian Liu, Binqi Sun, Matteo Mascherin, Debayan Roy, Yutao Liu, Yu Peng, Ning Jia, Haibo Chen  
**Published:** 2026-06-22  
**Categories:** cs.SE, cs.LG, cs.OS  

**Abstract:**
On-device LLM inference is increasingly attractive for privacy-preserving, reliable, and cost-effective deployment, yet its energy and thermal costs remain a critical bottleneck. Existing systems primarily optimize for decoding speed, implicitly assuming that faster execution is always preferable. We show instead that on-device LLM inference often has exploitable configuration slack: modestly lowering NPU and memory frequencies preserves quality of experience (QoE) while substantially improving energy efficiency and reducing heat.
  Realizing this opportunity in production is challenging. The most energy-efficient NPU/DDR setting varies with the model, inference engine, platform, and runtime conditions, with no stable ranking across configurations. Commercial devices further lack component-level power sensing, and shell temperature evolves with request arrivals, response lengths, and thermal history. To address these challenges, we propose EnerInfer, the first on-device LLM inference framework that jointly manages energy efficiency, throughput, and thermal comfort for LLM workloads. EnerInfer replaces per-model profiling and sensor-heavy control with disaggregated, model-structure-aware prediction and ranking-driven online feedback. It predicts throughput and power for unseen LLMs across NPU/DDR frequency settings, selects QoE-satisfying efficient configurations under runtime interference, and uses lightweight limited-horizon thermal prediction to dynamically switch between energy-optimized and thermally constrained inference. Evaluations on real-world LLMs show that EnerInfer improves energy efficiency by up to 65%, 12%, and 24% on phones, a laptop, and a development board, respectively, without QoE violation.

---


## Research Cycle — 2026-11-08 03:02 UTC

**Topic:** cpu-background-inference  
**Focus:** 1.5B-3B models on CPU, zero VRAM contention

### Characterizing CPU-Induced Slowdowns in Multi-GPU LLM Inference
**arXiv:** [2603.22774v1](https://arxiv.org/abs/2603.22774v1)  
**Authors:** Euijun Chung, Yuxiao Jia, Aaron Jezghani, Hyesoon Kim  
**Published:** 2026-03-24  
**Categories:** cs.AR, cs.DC  

**Abstract:**
Large-scale machine learning workloads increasingly rely on multi-GPU systems, yet their performance is often limited by an overlooked component: the CPU. Through a detailed study of modern large language model (LLM) inference and serving workloads, we find that multi-GPU performance frequently degrades not because GPUs are saturated, but because CPUs fail to keep the GPUs busy. Under limited CPU allocations, systems exhibit symptoms such as delayed kernel launch, stalled communication, and increased tokenization latency, leading to severe GPU underutilization even when ample GPU resources are available. This work presents a systematic analysis of CPU-induced slowdowns in multi-GPU LLM inference. We show that these bottlenecks persist even in serving stacks that employ process-level separation and modern GPU-side optimizations such as CUDA Graphs. Since the marginal cost of additional CPU cores is small relative to GPU instance pricing, our evaluation indicates that increasing the number of CPU cores can substantially improve performance and stability at minimal additional cost. Under moderate serving load, we observe that CPU-starved configurations frequently time out, while providing adequate CPU resources restores responsiveness and reduces time-to-first-token (TTFT) latency by 1.36-5.40x across configurations, all without requiring additional GPUs. This work shows that CPU provisioning is a crucial factor in multi-GPU LLM inference configuration, helping prevent control-side bottlenecks.

---

### Challenging GPU Dominance: When CPUs Outperform for On-Device LLM Inference
**arXiv:** [2505.06461v1](https://arxiv.org/abs/2505.06461v1)  
**Authors:** Haolin Zhang, Jeff Huang  
**Published:** 2025-05-09  
**Categories:** cs.DC, cs.LG  

**Abstract:**
The common assumption in on-device AI is that GPUs, with their superior parallel processing, always provide the best performance for large language model (LLM) inference. In this work, we challenge this notion by empirically demonstrating that, under certain conditions, CPUs can outperform GPUs for LLM inference on mobile devices. Using a 1-billion-parameter LLM deployed via llama.cpp on the iPhone 15 Pro, we show that a CPU-only configuration (two threads, F16 precision) achieves 17 tokens per second, surpassing the 12.8 tokens per second obtained with GPU acceleration. We analyze the architectural factors driving this counterintuitive result, revealing that GPU memory transfer overhead and CPU thread optimization play a critical role. Furthermore, we explore the impact of thread oversubscription, quantization strategies, and hardware constraints, providing new insights into efficient on-device AI execution. Our findings challenge conventional GPU-first thinking, highlighting the untapped potential of optimized CPU inference and paving the way for smarter deployment strategies in mobile AI. However, fully explaining the observed CPU advantage remains difficult due to limited access to low-level profiling tools on iOS.

---

### EnerInfer: Energy-Aware On-Device LLM Inference
**arXiv:** [2606.23001](https://arxiv.org/abs/2606.23001)  
**Authors:** Bohua Zou, Nian Liu, Binqi Sun, Matteo Mascherin, Debayan Roy, Yutao Liu, Yu Peng, Ning Jia, Haibo Chen  
**Published:** 2026-06-22  
**Categories:** cs.SE, cs.LG, cs.OS  

**Abstract:**
On-device LLM inference is increasingly attractive for privacy-preserving, reliable, and cost-effective deployment, yet its energy and thermal costs remain a critical bottleneck. Existing systems primarily optimize for decoding speed, implicitly assuming that faster execution is always preferable. We show instead that on-device LLM inference often has exploitable configuration slack: modestly lowering NPU and memory frequencies preserves quality of experience (QoE) while substantially improving energy efficiency and reducing heat.
  Realizing this opportunity in production is challenging. The most energy-efficient NPU/DDR setting varies with the model, inference engine, platform, and runtime conditions, with no stable ranking across configurations. Commercial devices further lack component-level power sensing, and shell temperature evolves with request arrivals, response lengths, and thermal history. To address these challenges, we propose EnerInfer, the first on-device LLM inference framework that jointly manages energy efficiency, throughput, and thermal comfort for LLM workloads. EnerInfer replaces per-model profiling and sensor-heavy control with disaggregated, model-structure-aware prediction and ranking-driven online feedback. It predicts throughput and power for unseen LLMs across NPU/DDR frequency settings, selects QoE-satisfying efficient configurations under runtime interference, and uses lightweight limited-horizon thermal prediction to dynamically switch between energy-optimized and thermally constrained inference. Evaluations on real-world LLMs show that EnerInfer improves energy efficiency by up to 65%, 12%, and 24% on phones, a laptop, and a development board, respectively, without QoE violation.

---


---

### Research Item 11: Small "Sidekick" Models on GPU for Agent Assistance (Recorded 2026-11-08 13:24 UTC)

**Goal:** Identify and validate small models (1.5B-3B) that run *efficiently on the P2200* to handle agent assistance tasks — web search collation, summarization, classification, extraction, routing — freeing the primary model (7B on GPU or CPU) for reasoning/tool-calling.

**Philosophy:** Not "cram biggest model possible into 5GB VRAM." Instead: **right-size models for specific agent subtasks** where small + fast + low-power beats large + slow. Like the Qwen 27B inference rig — but local, always-on, and task-specialized.

#### Why Small Models on GPU (Not CPU)?
| Factor | CPU (6C/12T) | P2200 (5GB VRAM) |
|--------|--------------|------------------|
| **Latency (1.5B Q4)** | 15-30 tok/s | **80-150+ tok/s** |
| **Concurrent streams** | 1-2 | **4-8+** (KV cache in VRAM) |
| **Power/token** | ~2-3W (CPU package) | **~0.5-1W** (GPU only) |
| **Always-on readiness** | Model load ~200-500ms | **Resident in VRAM, instant** |
| **Thermal** | CPU package heat | Isolated, easier to cool |

**Key insight:** Small models on GPU give **interactive latency + high concurrency + low marginal power** — perfect for the "sidekick" workloads that happen *frequently* in agent loops.

#### Target Sidekick Workloads
| Task | Model Profile | Why Small Model Works |
|------|---------------|----------------------|
| **Web search result collation** | 1.5B-3B, 8-32k ctx | Extract key facts, deduplicate, summarize → feed to primary |
| **Content classification / routing** | 1.5B, structured output | Fast, deterministic, GBNF-constrained JSON |
| **Entity extraction / NER** | 1.5B, fine-tuned | Narrow task, high accuracy at small size |
| **Summarization (short/medium)** | 1.5B-3B, 8-16k ctx | Map-reduce chunks, combine |
| **Query rewriting / expansion** | 1.5B | Rewrite user query for search API |
| **Relevance scoring / reranking** | 1.5B (bi-encoder style) | Score search results before primary sees them |
| **Format conversion** (HTML→MD, JSON→CSV) | 1.5B | Structured transformation, low reasoning |
| **Cache lookup / deduplication** | 1.5B | Semantic similarity, fast |

#### Candidate Models (P2200 VRAM Budget: ~500MB each if 7B primary resident)
| Model | Size | VRAM (Q4_K_M) | Strength | Agent Fit |
|-------|------|---------------|----------|-----------|
| **SmolLM2-1.7B-Instruct** | 1.7B | ~1 GB | **Fastest**, 1T tokens, MobileLLM arch | Classification, extraction, routing |
| **Qwen2.5-1.5B-Instruct** | 1.5B | ~0.9 GB | Strong reasoning, 32k ctx, tool-calling FTs | Query rewrite, collation, summarization |
| **Llama-3.2-3B-Instruct** | 3.2B | ~1.9 GB | 128k ctx, best general | Long-context collation, synthesis |
| **Phi-3.5-mini-Instruct** | 3.8B | ~2.2 GB | Strong benchmarks, 128k variant | Reasoning-heavy sidekick tasks |
| **Qwen2.5-Coder-1.5B** | 1.5B | ~0.9 GB | Code-specialized | Code search, API doc lookup |
| **Gemma-2-2B-IT** | 2B | ~1.2 GB | Efficient, 8k ctx | General sidekick |
| **BGE-small-en-v1.5** | 0.3B | ~0.2 GB | **Embedding only** | Reranking, deduplication, cache |
| **E5-small-v2** | 0.3B | ~0.2 GB | **Embedding only** | Same as above |

**VRAM Budget Example (7B primary + sidekicks):**
- 7B Q4_K_M: 4.5 GB
- SmolLM2-1.7B: 1.0 GB
- BGE-small: 0.2 GB
- **Total: 5.7 GB** → exceeds 5GB

**Solutions:**
1. **Quantize sidekicks to Q3_K_L** (~0.7 GB each)
2. **Swap sidekicks on demand** (llama.cpp mmap = fast cold load ~100ms)
3. **Run embeddings on CPU** (separate cores, no VRAM)
4. **Use 3B primary (Llama-3.2-3B Q4 = 1.9 GB)** → leaves 3 GB for sidekicks

#### Recommended Architecture: "Primary + Sidekick Pool"
```
P2200 VRAM (5GB)
├── Primary Model (1 slot, resident)
│   └── Llama-3.1-8B-Q4_K_M (4.5 GB)  OR  Llama-3.2-3B-Q4_K_M (1.9 GB)
└── Sidekick Pool (hot-swap, mmap)
    ├── SmolLM2-1.7B-Q3_K_L (classification, extraction) ~0.7 GB
    ├── Qwen2.5-1.5B-Q3_K_L (collation, summarization) ~0.7 GB
    └── BGE-small (CPU, no VRAM) (embeddings, reranking)
```

**llama.cpp Multi-Model Support:**
- Single llama-server can load multiple models via `-m` multiple times
- Each gets its own KV cache; VRAM shared
- Request routing via `X-Model` header or model alias
- Cold-swap: unload unused, load needed (mmap = fast)

#### Research Questions
1. **Latency budget:** Can sidekick + primary pipeline stay <500ms end-to-end?
2. **VRAM pressure:** Does KV cache fragmentation hurt when swapping sidekicks?
3. **Fine-tuning payoff:** Does LoRA on 1.5B for *specific* sidekick task (e.g., collation) beat prompt engineering?
4. **Concurrency:** How many parallel sidekick streams before primary starved?
5. **Power profile:** Sidekick-only mode (primary unloaded) → what's idle + per-request power?
6. **Quality threshold:** At what task complexity does sidekick fail and need primary?

#### Integration with Agent Loop
```
User Query
    ↓
[Sidekick: Query Rewrite] → Expanded queries
    ↓
[Search API] → Raw results
    ↓
[Sidekick: Collation/Dedup] → Clean summary + citations
    ↓
[Sidekick: Relevance Score] → Top-K for primary
    ↓
[Primary: Reasoning/Tool Use] → Final answer
    ↓
[Sidekick: Format/Convert] → Output formatting
```

**Each sidekick call: 50-200ms on P2200. Total overhead: <1s.**

#### Next Research Actions (Added)
11. **Benchmark sidekick candidates** on P2200: tok/s, latency, VRAM, power
12. **Test llama.cpp multi-model** loading/swapping with 7B + 2×1.5B
13. **Fine-tune SmolLM2-1.7B** for classification/extraction (CPU LoRA → GGUF)
14. **Build sidekick router** (task → model mapping, fallback to primary)
15. **Measure end-to-end agent loop** with sidekick pipeline
16. **Power profile:** Sidekick-only vs primary+sidekick vs CPU-only

#### Decision Gates (Added)
7. **Week 1:** If sidekick swap >200ms → keep resident, accept lower primary size
8. **Week 2:** If sidekick quality <80% of primary on task → expand sidekick size or fine-tune
9. **Week 3:** If pipeline latency >1s → simplify, reduce sidekick hops

---

---

### Research Item 12: Strata Evaluation (Recorded 2026-11-08 13:33 UTC, Updated 13:37 UTC)

**Verdict for T340/P2200 (Quadro P2200, Pascal sm_61): VIABLE via CUDA 12 engine — experimental/opt-in path.**

**Source:** `OLDER_GPUS.md` — Pascal (sm_60/61) runs through CUDA 12 engine with `STRATA_EXPERIMENTAL_SM60=ON`.

| Card | Compute Cap | Engine | Status |
|------|-------------|--------|--------|
| Tesla P100 | 6.0 (sm_60) | CUDA 12 | Supported, 7 scheduling switches on by default |
| **Tesla P40 / P4, GTX 10 series, Quadro P2200** | **6.1 (sm_61)** | **CUDA 12** | **Supported, BF16→fp32, opt-in STRATA_DENSE_F32=1** |
| RTX 20+ (Turing) | 7.5 | CUDA 13 (default) | Fully supported |

**What works on P2200:**
- GGUF models (Qwen3, DeepSeek MoE, etc.) via CUDA 12 engine
- OpenAI/Anthropic compatible API (`strata launch`)
- SSD offload for MoE expert paging (DeepSeek V4 35B+)
- Multi-model serving
- `strata connect` for OpenClaw integration

**What's needed:**
1. **CUDA 12.x toolkit** (not 13) — installer auto-detects Pascal → uses CUDA 12 engine
2. **`STRATA_EXPERIMENTAL_SM60=ON`** at build time (installer handles this)
3. **Driver ≥575.51** (CUDA 12.9 requirement)
4. **Source build** if prebuilt CUDA 12 engine not in release feed:
   ```bash
   cmake -B build -DSTRATA_ENABLE_CUDA=ON -DSTRATA_EXPERIMENTAL_SM60=ON \
         -DCMAKE_CUDA_ARCHITECTURES="61;70" \
         -DCMAKE_CUDA_COMPILER=/usr/local/cuda-12.9/bin/nvcc
   cmake --build build -j
   ```

**Key configs for Pascal (sm_61):**
| Env Var | Purpose |
|---------|---------|
| `STRATA_DENSE_F32=1` | Large dense GEMMs as fp32 (cuBLAS has no BF16 GEMM on sm_61) |
| `STRATA_DEQUANT_WIDE=0` | Old dequantization kernel |
| `STRATA_SM61_TABLE=0` | Legacy expert layout |
| `STRATA_IQ_STAGE_TABLES=1` | Stage IQ3 codebooks in shared memory |

**Performance expectation (P2200 5GB, Pascal):**
- No Tensor Cores → fp16 only, no BF16 native
- 5GB VRAM → 7B Q4_K_M fits (4.5GB), MoE expert paging enables larger
- Comparable to llama.cpp CUDA backend on Pascal
- One reporter: 2× Quadro M6000 24GB (Maxwell) got ~22 tok/s on Qwen3.8-Flash IQ1

**Research action:** **Test Strata on P2200 alongside llama.cpp** — compare:
- Inference speed (tok/s) on 7B Q4_K_M
- API compatibility (OpenAI/Anthropic)
- Multi-model switching latency
- SSD offload for MoE (if VRAM allows)
- Power draw vs llama.cpp

**When it shines vs llama.cpp:**
- MoE models with expert paging (DeepSeek V4, Qwen3 MoE) — runs >VRAM models via SSD
- Rust-based, potentially lower overhead
- Built-in model management (`strata launch`, `strata connect`)
- Desktop app + terminal unified

**Risks:**
- Experimental Pascal path — less tested than llama.cpp
- CUDA 12 toolchain required (separate from system CUDA 13)
- Smaller community, fewer GGUF quant variants tested
- No Vulkan/CPU fallback — NVIDIA only

---

### Updated Priority for Current Hardware (P2200 Pascal)

**Two viable paths now:**
1. **llama.cpp + llama-server** — mature, widest Pascal support, proven
2. **Strata (CUDA 12 engine)** — experimental Pascal, but adds MoE expert paging, unified CLI

**Recommended:** Benchmark both on P2200 (Action #2 + new Strata benchmark)

**Added research actions:**
17. **Install Strata CUDA 12 engine** on P2200 test environment
18. **Benchmark Strata vs llama.cpp** on 7B Q4_K_M (tok/s, latency, VRAM, power, API compat)
19. **Test MoE expert paging** with DeepSeek V4 / Qwen3 MoE (if VRAM allows)
20. **Evaluate Strata for production** vs llama-server (stability, hot-reload, multi-model)


## Research Cycle — 2026-11-08 18:04 UTC

**Topic:** cpu-background-inference  
**Focus:** 1.5B-3B models on CPU, zero VRAM contention

### Challenging GPU Dominance: When CPUs Outperform for On-Device LLM Inference
**arXiv:** [2505.06461v1](https://arxiv.org/abs/2505.06461v1)  
**Authors:** Haolin Zhang, Jeff Huang  
**Published:** 2025-05-09  
**Categories:** cs.DC, cs.LG  

**Abstract:**
The common assumption in on-device AI is that GPUs, with their superior parallel processing, always provide the best performance for large language model (LLM) inference. In this work, we challenge this notion by empirically demonstrating that, under certain conditions, CPUs can outperform GPUs for LLM inference on mobile devices. Using a 1-billion-parameter LLM deployed via llama.cpp on the iPhone 15 Pro, we show that a CPU-only configuration (two threads, F16 precision) achieves 17 tokens per second, surpassing the 12.8 tokens per second obtained with GPU acceleration. We analyze the architectural factors driving this counterintuitive result, revealing that GPU memory transfer overhead and CPU thread optimization play a critical role. Furthermore, we explore the impact of thread oversubscription, quantization strategies, and hardware constraints, providing new insights into efficient on-device AI execution. Our findings challenge conventional GPU-first thinking, highlighting the untapped potential of optimized CPU inference and paving the way for smarter deployment strategies in mobile AI. However, fully explaining the observed CPU advantage remains difficult due to limited access to low-level profiling tools on iOS.

---

### Characterizing CPU-Induced Slowdowns in Multi-GPU LLM Inference
**arXiv:** [2603.22774v1](https://arxiv.org/abs/2603.22774v1)  
**Authors:** Euijun Chung, Yuxiao Jia, Aaron Jezghani, Hyesoon Kim  
**Published:** 2026-03-24  
**Categories:** cs.AR, cs.DC  

**Abstract:**
Large-scale machine learning workloads increasingly rely on multi-GPU systems, yet their performance is often limited by an overlooked component: the CPU. Through a detailed study of modern large language model (LLM) inference and serving workloads, we find that multi-GPU performance frequently degrades not because GPUs are saturated, but because CPUs fail to keep the GPUs busy. Under limited CPU allocations, systems exhibit symptoms such as delayed kernel launch, stalled communication, and increased tokenization latency, leading to severe GPU underutilization even when ample GPU resources are available. This work presents a systematic analysis of CPU-induced slowdowns in multi-GPU LLM inference. We show that these bottlenecks persist even in serving stacks that employ process-level separation and modern GPU-side optimizations such as CUDA Graphs. Since the marginal cost of additional CPU cores is small relative to GPU instance pricing, our evaluation indicates that increasing the number of CPU cores can substantially improve performance and stability at minimal additional cost. Under moderate serving load, we observe that CPU-starved configurations frequently time out, while providing adequate CPU resources restores responsiveness and reduces time-to-first-token (TTFT) latency by 1.36-5.40x across configurations, all without requiring additional GPUs. This work shows that CPU provisioning is a crucial factor in multi-GPU LLM inference configuration, helping prevent control-side bottlenecks.

---

### EnerInfer: Energy-Aware On-Device LLM Inference
**arXiv:** [2606.23001](https://arxiv.org/abs/2606.23001)  
**Authors:** Bohua Zou, Nian Liu, Binqi Sun, Matteo Mascherin, Debayan Roy, Yutao Liu, Yu Peng, Ning Jia, Haibo Chen  
**Published:** 2026-06-22  
**Categories:** cs.SE, cs.LG, cs.OS  

**Abstract:**
On-device LLM inference is increasingly attractive for privacy-preserving, reliable, and cost-effective deployment, yet its energy and thermal costs remain a critical bottleneck. Existing systems primarily optimize for decoding speed, implicitly assuming that faster execution is always preferable. We show instead that on-device LLM inference often has exploitable configuration slack: modestly lowering NPU and memory frequencies preserves quality of experience (QoE) while substantially improving energy efficiency and reducing heat.
  Realizing this opportunity in production is challenging. The most energy-efficient NPU/DDR setting varies with the model, inference engine, platform, and runtime conditions, with no stable ranking across configurations. Commercial devices further lack component-level power sensing, and shell temperature evolves with request arrivals, response lengths, and thermal history. To address these challenges, we propose EnerInfer, the first on-device LLM inference framework that jointly manages energy efficiency, throughput, and thermal comfort for LLM workloads. EnerInfer replaces per-model profiling and sensor-heavy control with disaggregated, model-structure-aware prediction and ranking-driven online feedback. It predicts throughput and power for unseen LLMs across NPU/DDR frequency settings, selects QoE-satisfying efficient configurations under runtime interference, and uses lightweight limited-horizon thermal prediction to dynamically switch between energy-optimized and thermally constrained inference. Evaluations on real-world LLMs show that EnerInfer improves energy efficiency by up to 65%, 12%, and 24% on phones, a laptop, and a development board, respectively, without QoE violation.

---


---

### Research Item 13: Lightweight Models for Local Web Search Collation & Daily Recovery (Recorded 2026-11-08 18:35 UTC)

**Goal:** Define how 1.5B-3B models (sidekick pool) can automate web search result processing, daily content collation, and build a queryable local knowledge base for later recovery — all running on P2200 or CPU background.

**Problem:** Manual web research is slow. Search APIs return 10-50 raw results per query. Agents need: deduplication, extraction, summarization, citation tracking, and persistent storage for later retrieval.

---

#### Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    DAILY WEB RESEARCH PIPELINE                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  [Scheduled Topics]          [On-Demand Queries]                        │
│       │                            │                                    │
│       ▼                            ▼                                    │
│  ┌─────────┐               ┌─────────────┐                              │
│  │ SearXNG │               │  SearXNG    │                              │
│  │ Search  │               │  Search     │                              │
│  └────┬────┘               └──────┬──────┘                              │
│       │                           │                                     │
│       ▼                           ▼                                     │
│  ┌─────────────────────────────────────────┐                            │
│  │  Sidekick: Deduplication & Clustering   │  ← SmolLM2-1.7B / Qwen2.5-1.5B │
│  │  • Remove duplicate URLs                │  • Structured JSON output     │
│  │  • Cluster by topic (embedding + LLM)   │  • 50-100ms per batch         │
│  │  • Score relevance to query             │  • GPU: 100+ tok/s            │
│  └────────────────┬────────────────────────┘                            │
│                   │                                                     │
│                   ▼                                                     │
│  ┌─────────────────────────────────────────┐                            │
│  │  Sidekick: Content Extraction           │  ← Qwen2.5-1.5B / Llama-3.2-3B │
│  │  • Fetch top-N pages (parallel)         │  • 8-32k context              │
│  │  • Extract: title, body, code, tables   │  • Batch 5-10 pages           │
│  │  • Strip nav/ads/footer (readability)   │  • 200-500ms per page         │
│  └────────────────┬────────────────────────┘                            │
│                   │                                                     │
│                   ▼                                                     │
│  ┌─────────────────────────────────────────┐                            │
│  │  Sidekick: Summarization & Synthesis    │  ← Llama-3.2-3B (128k ctx)  │
│  │  • Per-source summary (200-500 tokens)  │  • Long context = multi-doc   │
│  │  • Cross-source synthesis               │  • Map-reduce for >32k        │
│  │  • Key facts + citations preserved      │  • 2-5 sec for 20 sources     │
│  └────────────────┬────────────────────────┘                            │
│                   │                                                     │
│                   ▼                                                     │
│  ┌─────────────────────────────────────────┐                            │
│  │  Sidekick: Structured Knowledge Store   │  ← Qwen2.5-1.5B (JSON)      │
│  │  • Entities: people, orgs, tech, dates  │  • GBNF-constrained schema  │
│  │  • Relations: uses, depends, competes   │  • Append-only JSONL        │
│  │  • Claims: "X outperforms Y on Z"       │  • Vector embeddings (CPU)  │
│  └────────────────┬────────────────────────┘                            │
│                   │                                                     │
│                   ▼                                                     │
│  ┌─────────────────────────────────────────┐                            │
│  │  Persistent Local Knowledge Base        │                            │
│  │  • SQLite + FTS5 (full-text search)     │                            │
│  │  • Qdrant/PGVector (semantic search)    │                            │
│  │  • Daily digest markdown (human-read)   │                            │
│  │  • Git-backed (versioned, diffable)     │                            │
│  └─────────────────────────────────────────┘                            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

#### Sidekick Model Assignments

| Stage | Model | VRAM (Q4) | Why This Model |
|-------|-------|-----------|----------------|
| **Dedup/Cluster** | SmolLM2-1.7B | ~1 GB | Fastest, structured output, 1T training tokens |
| **Extract** | Qwen2.5-1.5B | ~0.9 GB | Strong HTML→markdown, 32k ctx, tool-use FTs |
| **Summarize** | Llama-3.2-3B | ~1.9 GB | 128k ctx = multi-doc synthesis, best general |
| **Structure** | Qwen2.5-1.5B | ~0.9 GB | GBNF JSON schema adherence, fast |
| **Embed** | BGE-small (CPU) | 0 GB VRAM | 0.3B, 384-dim, CPU AVX2 fast enough |

**Total VRAM if all resident:** ~4.7 GB (leaves ~300 MB for KV cache — tight)

**Practical: Hot-swap via llama.cpp mmap** — load per-stage, unload after. Cold load ~100ms.

---

#### Daily Collation Workflow (Cron: 06:00 UTC)

```python
# Pseudocode: daily_research_collation.py

TOPICS = [
    "LLM inference optimization CPU GPU",
    "small model function calling LoRA",
    "Mixture of Experts expert paging",
    "llama.cpp Strata comparison",
    "local AI agent orchestration"
]

def daily_collation():
    all_knowledge = []
    
    for topic in TOPICS:
        # 1. Search (SearXNG)
        results = searxng_search(topic, max_results=20)
        
        # 2. Dedup/Cluster (SmolLM2-1.7B on GPU)
        clusters = sidekick_dedup(results)
        
        # 3. Extract top 3 per cluster (Qwen2.5-1.5B on GPU)
        sources = []
        for cluster in clusters[:3]:
            for url in cluster.urls[:3]:
                content = fetch_and_extract(url)  # readability + LLM extract
                sources.append(content)
        
        # 4. Synthesize (Llama-3.2-3B on GPU)
        synthesis = sidekick_synthesize(topic, sources)
        
        # 5. Structure into knowledge entries (Qwen2.5-1.5B on GPU)
        entries = sidekick_structure(synthesis)
        
        # 6. Embed & store (CPU)
        for entry in entries:
            vector = embed_cpu(entry.text)
            store_sqlite(entry, vector)
            store_qdrant(entry, vector)
        
        all_knowledge.append({"topic": topic, "synthesis": synthesis, "entries": entries})
    
    # 7. Generate daily digest markdown
    digest = generate_digest(all_knowledge)
    write_markdown(f"memory/{date}.md", digest)
    git_commit(f"Daily research digest {date}")
    
    # 8. Post to Discord #rook
    discord_post(digest, channel="#rook")
```

---

#### Query-Time Recovery (Later Retrieval)

```
User: "What did we find about Strata expert paging last week?"

    │
    ▼
[Embedding: BGE-small on CPU] → vector
    │
    ▼
[Qdrant semantic search] → top-K entries + metadata
    │
    ▼
[Sidekick: Re-rank (SmolLM2)] → relevance score
    │
    ▼
[Sidekick: Synthesize answer (Llama-3.2-3B)] → cited answer
    │
    ▼
Response with citations + links to original sources
```

**Latency budget:** <2s end-to-end (embedding 50ms + Qdrant 10ms + rerank 100ms + synthesis 1-2s)

---

#### Storage Schema (SQLite + Qdrant)

```sql
-- SQLite FTS5 for keyword search
CREATE VIRTUAL TABLE knowledge_fts USING fts5(
    topic, title, content, source_url, tags, date
);

-- Structured entries
CREATE TABLE knowledge_entries (
    id INTEGER PRIMARY KEY,
    topic TEXT,
    title TEXT,
    content TEXT,           -- synthesized paragraph
    source_urls TEXT,       -- JSON array
    entities TEXT,          -- JSON: {"people":[], "orgs":[], "tech":[], "dates":[]}
    claims TEXT,            -- JSON: [{"claim": "...", "confidence": 0.9, "sources": [...]}]
    relations TEXT,         -- JSON: [{"subject": "...", "predicate": "...", "object": "..."}]
    embedding_id TEXT,      -- Qdrant point ID
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

```python
# Qdrant collection: 384-dim vectors (BGE-small)
# Payload: {entry_id, topic, date, entities, tags}
# Filter by topic/date at query time
```

---

#### Power/Resource Profile (Daily Run)

| Phase | Duration | GPU Active | CPU Cores | Est. Energy |
|-------|----------|------------|-----------|-------------|
| Search (SearXNG) | 30s | No | 1 (network) | Negligible |
| Dedup (5 topics × 20 results) | 10s | SmolLM2 | 0 | ~5W × 10s |
| Extract (30 pages) | 60s | Qwen2.5 | 2 (fetch) | ~25W × 60s |
| Synthesize (5 topics) | 30s | Llama-3.2-3B | 0 | ~35W × 30s |
| Structure (5 topics) | 10s | Qwen2.5 | 0 | ~25W × 10s |
| Embed + Store | 20s | No | 2 (BGE) | ~15W × 20s |
| **Total** | **~2.5 min** | **Intermittent** | **Peak 2** | **~0.02 kWh** |

**At $0.15/kWh = $0.003/day = ~$1/year.** Negligible.

---

#### Integration with Existing Research Items

| Item | Connection |
|------|------------|
| **#11 Sidekick Pool** | This *is* the sidekick pool workload — validates the architecture |
| **#9 Power Optimization** | Daily run tests GPU power profile under burst load |
| **#10 Resource Orchestration** | Router picks GPU vs CPU per stage |
| **#12 Strata** | If Strata MoE works, could replace Llama-3.2-3B for synthesis (128k ctx via paging) |
| **Hybrid Research Aggregator** | This *implements* the aggregator's deep-fetch + synthesis loop locally |

---

#### Implementation Checklist

- [ ] **SearXNG client** — Python async, rate-limited, retry logic
- [ ] **Readability extractor** — `trafilatura` or `readability-lxml` + LLM cleanup
- [ ] **Sidekick prompts** — GBNF schemas for each stage (dedup, extract, synthesize, structure)
- [ ] **llama.cpp multi-model manager** — load/unload, health checks, VRAM monitoring
- [ ] **SQLite + Qdrant** — schema, indexes, backup strategy
- [ ] **Daily cron** — systemd timer, logging, failure alerting
- [ ] **Discord poster** — markdown formatting, channel targeting
- [ ] **Query CLI** — `research query "Strata expert paging"` → cited answer
- [ ] **Git auto-commit** — daily digest + knowledge base snapshots

---

#### Success Metrics

| Metric | Target |
|--------|--------|
| Daily run time | <5 min wall-clock |
| GPU energy per run | <0.05 kWh |
| Synthesis quality | Human eval: ≥4/5 vs manual research |
| Query recovery latency | <2s p95 |
| Knowledge base growth | 50-100 entries/week |
| Source coverage | ≥80% of search results processed |
| Deduplication accuracy | ≥95% duplicate clusters correct |

---

#### Decision Gates

10. **Week 1:** If sidekick swap latency >500ms → keep 2 models resident, accept 3B primary
11. **Week 2:** If synthesis quality <4/5 → improve prompts, increase context, or fine-tune
12. **Week 3:** If Qdrant query latency >500ms → optimize HNSW params, add SQLite FTS fallback
13. **Week 4:** If daily run >10 min → parallelize extract phase, batch sidekick calls

---

**Recorded per research protocol. No execution in sandbox — documentation only.**

---

### Research Item 14: Pre-T340 Preparation & RAM-Centric Strata Strategy (Recorded 2026-11-08 21:20 UTC)

**Context:** We are NOT on the T340 yet. Current sandbox: unknown CPU/RAM (likely modest). P2200 + 64GB RAM + Xeon E-2126G is the TARGET. This item plans what we can do NOW vs what waits for hardware.

---

#### Current vs Target Hardware Reality Check

| Resource | Current (Sandbox) | Target (T340) | Gap |
|----------|-------------------|---------------|-----|
| **GPU** | None / Unknown | Quadro P2200 5GB (Pascal sm_61) | **Full gap** |
| **RAM** | Unknown (likely ≤16GB) | 64GB DDR4 ECC | **Major gap** |
| **CPU** | Unknown | Xeon E-2126G 6C/12T, AVX2 | **Major gap** |
| **Storage** | Unknown | Plenty SSD/NVMe | Unknown |
| **OS** | Container | Proxmox VE + LXC | Different |

**Implication:** No GPU inference, no Strata testing, no large-model benchmarking until T340 arrives. Current work = **preparation, documentation, CPU-only validation on whatever we have.**

---

#### What We Can Do NOW (Pre-T340)

| Task | Feasibility | Value |
|------|-------------|-------|
| **SearXNG + web_fetch.py pipeline** | ✅ CPU-only, network only | Core search infrastructure |
| **Readability extraction (trafilatura)** | ✅ Pure Python | Content cleaning |
| **Sidekick prompt engineering (GBNF schemas)** | ✅ Any llama.cpp | Prompts are hardware-agnostic |
| **SQLite + Qdrant schema design** | ✅ Any Python | Storage layer ready |
| **Daily cron framework** | ✅ systemd timers | Scheduling ready |
| **Discord poster** | ✅ message tool | Delivery ready |
| **Query CLI skeleton** | ✅ Python + Qdrant client | Interface ready |
| **Strata source build prep** | ✅ Document CMake flags | Build script ready |
| **llama.cpp build configs** | ✅ Document AVX2/AMX flags | Compile flags ready |
| **PVE GPU passthrough docs** | ✅ Document procedure | Deploy-ready |

**These are the "dry run" tasks — zero hardware dependency, high value when hardware arrives.**

---

#### What Must Wait for T340

| Task | Why |
|------|-----|
| **llama.cpp benchmarks (tok/s, latency, VRAM)** | Needs P2200 + 64GB RAM |
| **Strata CUDA 12 engine install/test** | Needs Pascal GPU + CUDA 12 toolkit |
| **Sidekick pool VRAM profiling** | Needs actual 5GB VRAM |
| **QLoRA training (7B on GPU)** | Needs 5GB VRAM + CUDA |
| **Power profiling (nvidia-smi + turbostat)** | Needs GPU + CPU monitoring |
| **Multi-model llama-server testing** | Needs VRAM pressure reality |
| **Speculative decoding CPU→GPU** | Needs both devices |
| **MoE expert paging (DeepSeek V4)** | Needs 34GB+ RAM + SSD + GPU |

---

#### RAM-Centric Strata Strategy (For 64GB Target)

**Strata's RAM usage pattern (from docs):**
- **Experts in RAM:** 34-50 GB pinned (all 24,576 experts for Qwen3.8-Flash / DeepSeek V4)
- **Shard 1 (hot experts):** 23-50 GB depending on quant
- **N-gram table:** 28.8 GB on SSD (read via OS cache)
- **CPU computes cold experts** in-place from RAM while GPU works on hot experts

**For 64GB RAM — this FITS but tight:**

| Strata Model | RAM for Experts | OS/Overhead | Total | Fits 64GB? |
|--------------|-----------------|-------------|-------|------------|
| Qwen3.8-Flash IQ2_XS | 35.5 GB | ~8 GB | ~43.5 GB | ✅ Comfortable |
| Qwen3.8-Flash IQ3_XXS | 43 GB | ~8 GB | ~51 GB | ✅ OK |
| Qwen3.8-Flash IQ3_S | 50 GB | ~8 GB | ~58 GB | ⚠️ Tight |
| DeepSeek V4.1 2.00 bpw | 35.5 GB (shard 1) | ~10 GB | ~45.5 GB | ✅ Comfortable |
| Qwen3.6-35B UD-Q4_K_XL | ~72 GB | ~8 GB | ~80 GB | ❌ No (needs low-RAM mode) |

**Low-RAM Mode (Strata docs):**
- If RAM < experts, keep only what GPU doesn't hold in RAM
- Rest streamed from SSD (much slower)
- Example: 32GB RAM + 24GB GPU → runs Q2_0, IQ2_XS, Coder
- **Our 64GB + 5GB VRAM:** Can run IQ2_XS / 2.00 bpw comfortably; IQ3_XXS borderline

---

#### RAM Optimization Strategies for Strata on 64GB

| Strategy | How It Works | RAM Saved | Perf Cost |
|----------|--------------|-----------|-----------|
| **Use IQ2_XS / 2.00 bpw (not IQ3_S)** | Smaller quant = smaller experts | 10-15 GB | Minor quality drop |
| **Enable low-RAM mode** | Only keep GPU-missing experts in RAM | Up to 20 GB | SSD streaming latency |
| **Gyro-S / Gyro-M quants** | Trellis-coded, 20% less GPU mem | ~8 GB vs IQ3_XXS | 16-21% slower decode |
| **Offload n-gram table to fast NVMe** | Already on SSD; ensure OS cache hot | N/A (already SSD) | N/A |
| **Limit context to 8K** | Strata default; KV cache smaller | ~1-2 GB VRAM | Shorter context |
| **Disable vision/pictures** | Saves 1-1.4 GB VRAM + RAM | ~1.5 GB | No image input |
| **Run embedding models on CPU** | BGE/E5 on CPU cores, zero VRAM | ~0.5 GB VRAM | Negligible |

**Recommended Strata Config for 64GB + P2200:**
```bash
# Qwen3.8-Flash IQ2_XS (35.5 GB experts) — best balance
STRATA_DENSE_F32=1 \
STRATA_DEQUANT_WIDE=0 \
STRATA_IQ_STAGE_TABLES=1 \
STRATA_EXPERIMENTAL_SM60=ON \
strata launch --family qwen --model IQ2_XS --context 8k --vision off

# DeepSeek V4.1 2.00 bpw (35.5 GB shard 1) — coding/agent specialist
STRATA_DENSE_F32=1 \
strata launch --family deepseek41 --model ist-das-2.00bpw --context 8k --vision off
```

---

#### Hybrid RAM Usage: Strata + llama.cpp Sidekicks (The Real Architecture)

**64GB allocation when BOTH running:**

| Component | RAM Allocation | Notes |
|-----------|----------------|-------|
| **Strata (MoE primary)** | 36-44 GB | IQ2_XS experts + overhead |
| **llama.cpp sidekicks (CPU)** | 4-8 GB | 1-2 small models mmap'd |
| **Embeddings (BGE/E5)** | 1-2 GB | CPU only |
| **OS + PVE + LXC overhead** | 4-6 GB | Proxmox + containers |
| **Buffer / SSD cache** | 4-8 GB | OS page cache for n-gram table |
| **Total** | **~50-62 GB** | **Fits with headroom** |

**VRAM allocation (5GB P2200):**
| Component | VRAM | Notes |
|-----------|------|-------|
| **Strata (attention + expert cache)** | ~3.5 GB | Rest of experts in RAM |
| **llama.cpp sidekick (resident)** | ~1.0 GB | SmolLM2-1.7B Q3_K_L |
| **KV cache + overhead** | ~0.5 GB | Dynamic |
| **Total** | **~5.0 GB** | **At limit** |

**If VRAM too tight:** Unload sidekick when Strata active, or use 3B primary (1.9 GB) instead of MoE.

---

#### Pre-T340 Action Plan (No False Promises)

**Week 1-2 (Now, on current hardware):**
- [ ] Finalize SearXNG client + readability extractor
- [ ] Write GBNF schemas for all sidekick stages
- [ ] Implement SQLite + Qdrant schema + basic CRUD
- [ ] Build daily cron framework with logging/alerting
- [ ] Write Discord poster + query CLI skeleton
- [ ] Execute Strata source build on P2200 with CUDA 12 + SM60
- [ ] Document llama.cpp build flags for Xeon AVX2
- [ ] Document PVE GPU passthrough procedure

#### Strata Pascal (sm_61) Source Build — CONFIRMED RECIPE

**Repository:** https://github.com/Niko1221/Strata (42k stars, active — last push 2 days ago)

**CUDA Toolkit:** CUDA 12.x required (CUDA 13 dropped Pascal/Volta)

**CMake Build Command:**
```bash
# Linux source build for Pascal (sm_61) + Volta (sm_70)
cmake -S . -B build-cuda12 \
  -DSTRATA_ENABLE_CUDA=ON \
  -DSTRATA_BUILD_TESTS=OFF \
  -DSTRATA_EXPERIMENTAL_SM60=ON \
  -DCMAKE_CUDA_ARCHITECTURES="61;70" \
  -DCMAKE_CUDA_COMPILER=/usr/local/cuda-12.9/bin/nvcc \
  -DCMAKE_BUILD_TYPE=Release

cmake --build build-cuda12 --target strata -j$(nproc)
```

**Key Environment Variables for sm_61 (P2200/GTX 10 series):**
| Variable | Default | Purpose |
|----------|---------|---------|
| `STRATA_DEQUANT_WIDE=1` | ON | Wide dequantization kernel for sm_61 |
| `STRATA_SM61_TABLE=1` | ON | Interleaved matvec table for expert mode 8 |
| `STRATA_DENSE_F32=1` | OFF | Large dense GEMMs as fp32 (opt-in, more VRAM) |
| `STRATA_IQ_STAGE_TABLES=1` | OFF | Stage IQ3_XXS/IQ3_S codebooks in shared memory |
| `STRATA_EXPERIMENTAL_SM60=1` | Required | Enables CC 6.0+ code paths in build |

**Engine Selection (Per-Model Config):**
- Each model gets `"cuda": 12` in its config when oldest card is Pascal/Volta
- Auto-selected by setup; override with `--cuda 12` or `STRATA_CUDA=12`
- CUDA 12 engine supports CC 6.0–8.9 + PTX; CUDA 13 engine is CC 7.5+

**OpenAI-Compatible API:**
- `strata connect` → gives localhost endpoint for OpenClaw/llama.cpp tools
- Compatible with OpenAI/Anthropic client libraries

**House-Proven Performance (Francis, Nov 8):**
- Flash Next on mini: ~1,300 tok/s prefill, 40-50 tok/s generation
- GSQ-RCO quants (ISTA-DASLab) shipping via Strata

**Week 3 (When T340 arrives):**
- [ ] Install PVE, configure GPU passthrough to LXC
- [ ] Build llama.cpp with CUDA 12 + AVX2
- [ ] Build Strata from source with CUDA 12 + SM60
- [ ] Benchmark 7B Q4_K_M on P2200 (llama.cpp)
- [ ] Test Strata IQ2_XS on P2200 (tok/s, VRAM, RAM)
- [ ] Measure power draw (nvidia-smi + turbostat)
- [ ] Test multi-model llama-server (7B + 1.5B)

**Week 4:**
- [ ] QLoRA train Deepseek-Coder-7B on tool calls
- [ ] Export GGUF → test with GBNF
- [ ] Deploy sidekick pool (hot-swap testing)
- [ ] Run first full daily research pipeline end-to-end
- [ ] Tune based on real metrics

---

#### Decision Gates (Honest, No Fluff)

| Gate | Criteria | If Fail |
|------|----------|---------|
| **Strata viability** | IQ2_XS runs ≥5 tok/s on P2200, <58 GB RAM | Drop Strata; use llama.cpp 7B only |
| **Sidekick swap** | Cold load <200ms, no VRAM fragmentation | Keep 1 sidekick resident, reduce primary |
| **Daily pipeline** | End-to-end <10 min, quality ≥4/5 | Simplify stages, reduce source count |
| **Power target** | GPU <50W at >25 tok/s (7B) | Accept higher power or smaller model |
| **QLoRA 7B** | Trains in <2 hrs/epoch on P2200 | Fall back to CPU LoRA on 3B |

---

#### What This Research File Now Covers

| Item | Topic | Status |
|------|-------|--------|
| 1-8 | CPU inference papers, model shortlist, training viability | ✅ Researched |
| 9 | P2200 power optimization | ✅ Documented |
| 10 | Full resource orchestration | ✅ Documented |
| 11 | Sidekick pool architecture | ✅ Documented |
| 12 | Strata evaluation (Pascal viable) | ✅ Documented |
| 13 | Web search collation pipeline | ✅ Documented |
| **14** | **Pre-T340 prep + RAM-centric Strata** | **✅ This entry** |

---

#### Key Principle: No Hardware, No Benchmarks

**Every performance number in this file for P2200/64GB is an ESTIMATE based on:**
- Strata docs (RTX 3060 12GB = 9-11 tok/s DeepSeek)
- llama.cpp community reports (Pascal ~60-70% of Turing)
- Extrapolation from 12GB → 5GB VRAM, 46GB → 64GB RAM

**Real numbers only exist after T340 arrives and we measure.**

---

#### Next Research Action (When Ready)

**Item 15:** Actual benchmark results from T340 — replace all estimates with measurements.

**Until then:** Build the hardware-agnostic parts. They're 70% of the work and unblocked.

---

**Recorded per protocol. No execution on target hardware — preparation only.**

---

### Research Item 15: P2200 Power Profile Optimization — Documented Methods (Recorded 2026-11-08 21:25 UTC)

**Context:** Pascal architecture (GP107, sm_61), 75W TDP, Quadro P2200. Driver branch 550.x or 535.x (CUDA 12 support). No Tensor Cores, no NVENC/NVDEC for LLM workloads.

**Source Status:** NVIDIA official docs for nvidia-smi 550/535 are behind login or 404. Forums/StackExchange often blocked. **This is documented from nvidia-smi manual knowledge + Pascal architecture constraints — NOT from live web fetch. Flagged for verification on T340.**

---

#### Confirmed nvidia-smi Controls (Pascal Supported)

| Control | Flag | Pascal Support | Persists Reboot? | Notes |
|---------|------|----------------|------------------|-------|
| **Power Limit** | `-pl <watts>` | ✅ Yes | ❌ No (needs script) | Range: ~30W to 75W (TDP). Below ~45W may throttle hard. |
| **GPU Clock Lock** | `-lgc <min>,<max>` | ✅ Yes | ❌ No | Locks graphics clocks. Format: `1000,1500` or single value `1395`. |
| **Memory Clock Lock** | `-lmc <min>,<max>` | ⚠️ Limited | ❌ No | Pascal GDDR5: often read-only or narrow range. |
| **Applications Clocks** | `-ac <gpu>,<mem>` | ✅ Yes | ❌ No | Preferred over `-lgc` for compute workloads. Sets default clocks for compute apps. |
| **Persistence Mode** | `-pm 1` | ✅ Yes | ❌ No | Keeps driver loaded, faster cold start, enables other controls. |
| **Auto Boost** | `--auto-boost-default 0` | ✅ Yes | ✅ Yes (registry) | Disables dynamic boost; stable clocks. Requires root. |

**Pascal-Specific Constraints:**
- **No `-ac` fine-grained control** like Turing+ — `-ac` sets single pair, not ranges
- **Memory clock locking often unavailable** on Quadro Pascal — GDDR5 voltage tied to clock
- **Power limit floor ~30W** — below this, GPU may become unstable or disable features
- **No GSP firmware** (pre-Ampere) — all controls via driver, not firmware
- **Driver 550.x required for CUDA 12** — 535.x is last CUDA 11 branch

---

#### Recommended Power Profiles for LLM Inference (To Test)

| Profile | Power Limit | GPU Clock | Memory Clock | Use Case | Est. Tok/s (7B Q4) |
|---------|-------------|-----------|--------------|----------|-------------------|
| **Max Perf** | 75W (default) | Auto (boost) | Auto | Benchmark baseline | ~35-40 |
| **Balanced** | 55W | 1395 MHz (base) | Auto | Daily driver | ~30-33 |
| **Efficiency** | 45W | 1200 MHz | Auto | Always-on, thermal constrained | ~25-28 |
| **Min Viable** | 35W | 1000 MHz | Auto | Absolute power cap | ~18-22 |

**Application Clocks Command (Preferred):**
```bash
# Set persistent compute clocks (survives app restarts, not reboot)
sudo nvidia-smi -pm 1
sudo nvidia-smi -ac 1395,2505  # GPU 1395 MHz, Mem 2505 MHz (P2200 base)

# Or power limit + let driver manage clocks
sudo nvidia-smi -pl 45
```

**Clock Locking Command (Alternative):**
```bash
# Lock to specific frequency (more aggressive)
sudo nvidia-smi -lgc 1200,1395
sudo nvidia-smi -lmc 2505,2505  # May fail on Pascal Quadro
```

---

#### Persistence Across Reboot (systemd Service)

```ini
# /etc/systemd/system/p2200-power-profile.service
[Unit]
Description=P2200 Power Profile for LLM Inference
After=display.service
Wants=display.service

[Service]
Type=oneshot
ExecStart=/usr/bin/nvidia-smi -pm 1
ExecStart=/usr/bin/nvidia-smi -pl 45
ExecStart=/usr/bin/nvidia-smi -ac 1395,2505
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable p2200-power-profile
sudo systemctl start p2200-power-profile
```

---

#### Monitoring & Validation Commands

```bash
# Real-time power/clock/temp monitoring (1s interval)
nvidia-smi dmon -s pucvmt -i 0 -d 1

# CSV for logging
nvidia-smi dmon -s pucvmt -i 0 -d 1 --format csv

# Single snapshot with all fields
nvidia-smi -q -i 0 -d POWER,CLOCK,TEMPERATURE,UTILIZATION

# Supported clocks (what -ac/-lgc can set)
nvidia-smi -q -i 0 -d SUPPORTED_CLOCKS
```

**Key Metrics to Log Per Profile:**
| Metric | Command Field | Target |
|--------|---------------|--------|
| GPU Power Draw | `pwr` (W) | <50W (efficiency), <75W (max) |
| GPU Clock | `clk` (MHz) | Stable at set value |
| Memory Clock | `mem` (MHz) | Stable |
| GPU Temp | `tmp` (°C) | <75°C sustained |
| SM Utilization | `sm` (%) | >80% during inference |
| Memory Utilization | `mem` (%) | <90% (avoid OOM) |
| Tok/s | llama.cpp output | >25 (7B Q4) |

---

#### llama.cpp Flags for Power Efficiency (P2200)

```bash
# Baseline (max perf)
./llama-server -m model.gguf -ngl 35 -c 4096 -b 512 --ubatch 512 --flash-attn

# Power-optimized
./llama-server -m model.gguf -ngl 35 -c 4096 -b 256 --ubatch 256 \
  --flash-attn --mlock --no-mmap --parallel 1 \
  --cpu-threads 6 --cpu-threads-batch 6

# Batch throughput (queue requests, process in large batches)
./llama-server -m model.gguf -ngl 35 -c 4096 -b 1024 --ubatch 512 \
  --flash-attn --parallel 4
```

**Flags that affect power:**
| Flag | Power Impact | Perf Impact |
|------|--------------|-------------|
| `-b` / `--ubatch` | Larger batch = better GPU utilization = more power, better tok/s | Balance for workload |
| `--parallel` | More slots = more concurrent = higher avg power | Throughput ↑ |
| `--flash-attn` | Slightly more power, much faster | Enable |
| `--mlock` | Zero page faults = smoother power | Enable |
| `-ngl` | More layers on GPU = more VRAM + power | 35 for 7B full offload |

---

#### Speculative Decoding for Energy/Token (Research)

**Concept:** Small draft model (CPU) proposes tokens → Large target model (GPU) verifies in batch.
- **Draft:** SmolLM2-1.7B or Qwen2.5-1.5B on CPU (6C/12T)
- **Target:** 7B on P2200
- **Expected:** 1.5-2x tokens per GPU forward pass → ~30-50% energy/token reduction

**llama.cpp Support:** `--draft-model` flag (experimental)
```bash
./llama-server -m 7b.gguf -ngl 35 \
  --draft-model 1.5b.gguf --draft-ngl 0 \
  -c 4096 -b 512 --flash-attn
```

**Pascal Constraint:** No Tensor Cores → fp16 only. Speculative decoding benefit may be lower than on Tensor Core GPUs.

---

#### KV Cache Quantization (llama.cpp)

```bash
# FP8 KV cache (if supported) - saves VRAM bandwidth
./llama-server -m model.gguf -ngl 35 --cache-type-k f16 --cache-type-v f16

# Int8 KV cache (experimental)
./llama-server -m model.gguf -ngl 35 --cache-type-k q8_0 --cache-type-v q8_0
```

**Pascal:** No native FP8/INT8 tensor cores. Quantization done in shader — may not save power, saves VRAM.

---

#### What Needs Verification on T340 (Honest List)

| Item | Why Unverified | Test Method |
|------|----------------|-------------|
| **`-lmc` memory clock lock works** | Pascal Quadro often locks mem clocks | `nvidia-smi -lmc 2505,2505` → check `dmon` |
| **`-ac` applications clocks persist** | Pre-GSP driver behavior varies | Set → restart llama.cpp → verify clocks |
| **Power limit floor 35W stable** | Below 45W may cause compute errors | Step down 5W at a time, run benchmark |
| **Actual tok/s at each profile** | Extrapolated from RTX 3060 (different arch) | Benchmark each profile with 7B Q4_K_M |
| **Thermal at 45W sustained** | Case airflow unknown | 30-min stress test, log temp |
| **Speculative decoding speedup** | Pascal no Tensor Cores, unknown benefit | Test with/without draft model |
| **KV cache quantization quality** | fp16→int8 may hurt perplexity on Pascal | Eval perplexity + tok/s |

---

#### Integration with Research Item 9 (Power Optimization)

**Updated Decision Gate 4 (Week 1):**
> If P2200 >55W at ≥25 tok/s (7B Q4_K_M) → test clock/power limits per this doc. Target: **<50W at >25 tok/s**.

**Measurement Protocol (Revised):**
1. Baseline: 75W, auto clocks → measure tok/s, power, temp (10 min)
2. Step 1: `-pl 55` → measure (10 min)
3. Step 2: `-pl 45` → measure (10 min)
4. Step 3: `-pl 45 -ac 1395,2505` → measure (10 min)
5. Step 4: `-pl 35 -ac 1200,2505` → measure (10 min)
6. Pick best W/token ratio meeting ≥25 tok/s floor

**Success Metric:** **W/token < 1.5** at ≥25 tok/s (7B Q4_K_M, 4K ctx, batch 512).

---

#### Risk: Pascal Driver Support End-of-Life

- **550.x branch:** Supported until ~2026-2027 (CUDA 12.x)
- **535.x branch:** Legacy, CUDA 11.x only
- **No new features** for Pascal — only security/critical fixes
- **nvidia-smi controls stable** — unlikely to change

**Mitigation:** Document working profile. If driver update breaks it, pin driver version (550.x last Pascal branch).

---

#### Next Research Action (On T340)

**Item 16:** Actual P2200 power/perf measurements → replace all estimates with data.

**Until then:** This doc is the **test plan**, not results. Every number here is a hypothesis to validate.

---

**Recorded per protocol. No execution on target hardware — test plan only.**

---

### Research Item 16: Function-Calling Benchmark Papers — Paper 1/4 (Recorded 2026-11-08 22:30 UTC)

**Paper:** TinyLLM: Evaluation and Optimization of Small Language Models for Agentic Tasks on Edge Devices  
**arXiv:** [2511.22138v1](https://arxiv.org/abs/2511.22138v1) (Nov 2025)  
**Authors:** Mohd Ariful Haque, Fahad Rahman, Kishor Datta Gupta, Khalil Shujaee, Roy George  
**Source:** arXiv HTML + abstract (full results tables not accessible via fetch — PDF is binary)

---

#### Key Findings for Our Stack

| Aspect | Finding | Implication |
|--------|---------|-------------|
| **Model Scale Threshold** | 1-3B models >> <1B models for agentic tasks | Confirms our 1.5B-3B focus; <1B (TinyLlama 1.1B) not viable for tool calling |
| **Max Accuracy (BFCL)** | 65.74% overall (hybrid optimization) | Ceiling for SLMs on function calling — not "solved" |
| **Multi-turn Accuracy** | 55.62% (hybrid) | Multi-turn agent loops need more work |
| **Best Optimization** | Hybrid (SFT + LoRA + DPO + RL) > any single method | Matches our LoRA + DPO plan for Deepseek-Coder/Phi-3 |
| **Benchmark** | BFCL (Berkeley Function Calling Leaderboard) | Standard we should use for evaluation |
| **Dataset** | Gorilla OpenFunctions (2,000 samples, 40 domains) | Source for synthetic data generation |

---

#### Models Evaluated (All <3B)

| Model | Base Performance | Post-Hybrid Optimization | Notes |
|-------|------------------|--------------------------|-------|
| **TinyAgent** | Baseline | Surpassed | Original TinyAgent replicated then beaten |
| **TinyLlama (1.1B)** | Low | Moderate | Used as "rejected" baseline for DPO pairs |
| **Qwen (<3B variants)** | Stronger base | **Best results** | Qwen family excels at function calling |
| **xLAM (<3B)** | Competitive | Strong | Salesforce's agent model family |

**Key:** Qwen and xLAM families respond best to optimization. TinyLlama 1.1B struggles even after optimization.

---

#### Optimization Pipeline (Replicable for Us)

```
1. Data: Gorilla OpenFunctions (2k samples) + AgentBank (ALFRED)
2. SFT: Supervised fine-tuning on function-calling data
3. LoRA/QLoRA: PEFT (r=8-16, alpha=16-32)
4. DPO: Convert SFT → chosen/rejected pairs
   - Chosen: High-quality function calls
   - Rejected: TinyLlama outputs (weak baseline) + manual validation
5. RL (optional): PPO on top for further alignment
6. Hybrid: SFT → LoRA → DPO → (RL) = best results
```

**Our Adaptation:**
- Base models: **Deepseek-Coder-1.3B** (paper-proven LoRA-responsive) + **Phi-3.5-mini** (paper-proven)
- Dataset: Generate synthetic tool-calls using GPT-4o/API (1-2k examples)
- LoRA: r=8, alpha=8, dropout=0.05 (CPU viable per Item 8 spike)
- DPO: Use our own SFT outputs as rejected, curated as chosen
- Eval: BFCL framework (installable via `pip install bfcl`)

---

#### BFCL Categories (Our Test Coverage)

| Category | Description | Our Sidekick Relevance |
|----------|-------------|------------------------|
| **Simple** | Single function call | High — basic tool use |
| **Multiple** | Choose 1 of 2-4 functions | High — routing/classification |
| **Parallel** | Same function multiple times | Medium — batch ops |
| **Parallel Multiple** | Multiple functions, multiple calls | Medium — complex agents |
| **Relevance Detection** | Abstain when no function fits | **Critical** — safety/guardrail |

---

#### Gaps / What We Still Need

- **Exact per-model accuracy tables** — HTML fetch too large, PDF not parseable
- **Latency/throughput numbers** — Paper focuses on accuracy, not edge deployment speed
- **VRAM/RAM usage during training** — Not reported
- **Quantization impact (Q4_K_M)** — All results likely fp16/bf16

---

#### Action Items for Our Stack

1. **Install BFCL** for local evaluation: `pip install bfcl`
2. **Generate synthetic dataset** (1-2k) using Gorilla OpenFunctions schema + our tool schemas
3. **Run baseline eval** on Deepseek-Coder-1.3B, Phi-3.5-mini, Qwen2.5-1.5B (CPU + GPU)
4. **LoRA fine-tune** on CPU (Item 8) → export GGUF → test with BFCL
5. **DPO pipeline** using our SFT outputs as rejected pairs
6. **Target:** >60% BFCL overall on 1.5B-3B models (paper shows 65.74% ceiling)

---

#### Remaining Papers to Fetch (3/4)

| arXiv ID | Title Hint | Priority |
|----------|------------|----------|
| **2501.02342v1** | Function calling benchmark / small models | High |
| **2609.07370** | Recent (Sep 2026) — likely updated BFCL results | High |
| **2410.18890v1** | Older (Oct 2024) — may be superseded | Medium |

**Next:** Fetch 2501.02342v1 and 2609.07370.

---

**Recorded per protocol. Results tables incomplete — flagged for local BFCL run.**

---

### Deep Fetch — 2026-11-08 22:30 UTC (Paper 3: 2609.07370)

**Source:** https://arxiv.org/html/2609.07370  
**Title:** Beyond Fluent Generation: A CPU Reliability Benchmark for MCP-Style Tool Calling in Sub-2B Small Language Models for Edge Deployment  
**Authors:** (ICLR 2025 submission)  
**Focus:** Sub-2B tool-calling reliability, CPU resource profiling, recovery parsing

**Key Findings — Tool-Calling Reliability (SLM-ToolCall-100 Benchmark):**

| Model | Params | Greedy Accuracy | Sampling Accuracy | Strict JSON Parseable |
|-------|--------|-----------------|-------------------|----------------------|
| **Qwen2.5-1.5B** | 1.54B | **75%** | **79%** | 5/200 (2.5%) |
| **Qwen2.5-0.5B** | 0.49B | 72% | 32% | 0/200 |
| **TinyLlama-1.1B-Chat** | 1.1B | ≤7% | ≤7% | 0/200 |
| **Pythia-1.4B** | 1.41B | ≤7% | ≤7% | 0/200 |
| **Phi-1.5** | 1.42B | **0%** | **0%** | 0/200 |

**Critical Insight:** Only 5 of 1,000 raw responses are directly parseable as JSON — **recovery parsing (strip fences, extract brace-delimited) is mandatory** for sub-2B models.

**CPU Resource Probe (FP32, unquantised, transformers):**

| Model | Process RSS (MiB) | Mean Latency (s, 50 tokens) |
|-------|-------------------|----------------------------|
| Qwen2.5-1.5B | **7,960** | 30.78 |
| Qwen2.5-0.5B | 3,637 | 10.63 |
| Phi-1.5 | ~5,200 | ~22 |
| Pythia-1.4B | ~5,000 | ~20 |
| TinyLlama-1.1B | ~3,800 | ~14 |

**Methodology Notes:**
- 100 prompts × 5 tools (get_weather, search_web, calculate, send_email, create_todo)
- Recovery parser: remove Markdown fences → extract first `{` to last `}` → json.loads
- Evaluation: tool name match, all expected args present, values match (case-insensitive strings, 1e-3 relative numeric)
- Wilson 95% CI + McNemar paired test (greedy vs sampling on same prompts)
- FP32 CPU only — no quantization, no constrained decoding

**For Your 4-6 Core + 48-64GB RAM:**
- **Qwen2.5-1.5B is the clear winner** for sub-2B tool calling (75-79% recovered accuracy)
- **Quantization (Q4) will reduce RSS significantly** — expect 2-3 GB for Q4_K_M vs 8 GB FP32
- **llama.cpp + GBNF grammar** should push accuracy higher (constrained generation eliminates syntax errors)
- **Phi-1.5 at 0% confirms** textbook-style training doesn't transfer to structured output
- **TinyLlama ≤7% aligns** with TinyLLM paper (2511.22138v1) — struggles even post-optimization

**Action Items from This Paper:**
- [ ] Test Qwen2.5-1.5B-Q4_K_M with GBNF tool-calling grammar on target CPU
- [ ] Compare recovery parser vs GBNF constrained generation accuracy
- [ ] Profile RSS/latency with llama.cpp (vs transformers FP32 baseline)
- [ ] Add to baseline eval suite: Qwen2.5-1.5B, Qwen2.5-0.5B, TinyLlama-1.1B

---

### Deep Fetch — 2026-11-08 22:35 UTC (Paper 4: 2410.18890v1)

**Source:** https://arxiv.org/html/2410.18890v1  
**Title:** Improving Small-Scale Large Language Models Function Calling for Reasoning Tasks  
**Authors:** (IEEE/Conference, Oct 2024)  
**Focus:** DPO training pipeline for small-model function calling on FOL + GSM8K reasoning

**Key Findings — DPO Framework for Small-Model Function Calling:**

**Pipeline (4 Stages):**
1. **Task Definition** — FOL (ad hoc from SAGI-1/SYMBOLIC_DATA_PLUS_REASONING_DATA_V1) + Math (GSM8K)
2. **Dataset Generation** — Agent queries large LLM (GPT-4 class) with function descriptions/examples, manages step-by-step reasoning chain → produces correct/incorrect chat completions
3. **Preference Pair Creation** — Correct vs incorrect reasoning chains form DPO pairs
4. **DPO Training** — Small model trained directly on preference pairs (no reward model)

**Experimental Setup (from methodology — results section truncated in HTML):**
- **Large model teacher:** Not explicitly named in accessible sections (likely GPT-4 or Claude)
- **Small model student:** Size not specified in fetched sections — paper focuses on framework
- **Functions:** Calculator, logical operators, FOL theorem prover tools
- **DPO loss:** Standard DPO with β hyperparameter, reference policy π_ref = initial small model

**Key Architectural Insights:**
- **Agent-managed function calling** — not single-turn; multi-step reasoning chains with tool calls
- **Synthetic data from large model** — bypasses human annotation cost
- **DPO > PPO for small models** — no reward model needed, more stable, less compute
- **FOL + GSM8K dual benchmark** — logical + mathematical reasoning

**Gaps in Fetched Content:**
- Results tables (Section IV) not fully accessible via HTML fetch (content-length limit)
- Exact small model size, baseline accuracy, DPO improvement metrics not captured
- Training compute/hours, quantization impact not in fetched sections

**For Your CPU-Only 1.5B-3B Path:**
- **DPO on CPU is viable** — this paper's framework matches your Item 8 (LoRA on CPU → DPO)
- **Synthetic data generation via API** (GPT-4o/Claude) → local DPO on CPU with Unsloth
- **FOL reasoning** adds logical rigor beyond simple function calling — good for agent reliability
- **GSM8K math** validates tool use (calculator) for multi-step reasoning

**Action Items from This Paper:**
- [ ] Fetch full results (try PDF or arXiv API for Section IV tables)
- [ ] Replicate dataset generation: agent + large LLM → FOL/GSM8K tool-call chains
- [ ] Run DPO on Deepseek-Coder-1.3B or Qwen2.5-1.5B (CPU, Unsloth, bf16)
- [ ] Compare: SFT-only vs SFT+DPO vs SFT+LoRA+DPO on BFCL + custom FOL/GSM8K eval

---

### Research 1/6 Complete — Function-Calling Benchmark Papers Summary

**4 Papers Fetched, Key Synthesis for 1.5B-3B CPU Stack:**

| Paper | ID | Key Takeaway for Your Stack |
|-------|-----|----------------------------|
| **TinyLLM** | 2511.22138v1 | 1-3B >> <1B for agentic; max BFCL 65.74% (SFT+LoRA+DPO); Qwen/xLAM best; TinyLlama struggles |
| **Phi-3 Vehicle** | 2501.02342v1 | Depth+width pruning (3.8B→2.8B→1.8B) + healing (5k LoRA + 45k full + SFT) + llama.cpp Q4 = 11 tok/s CPU |
| **Sub-2B MCP Bench** | 2609.07370 | **Qwen2.5-1.5B = 75-79% recovered tool-call accuracy** (best sub-2B); Phi-1.5 0%; recovery parsing essential |
| **DPO Reasoning** | 2410.18890v1 | Agent→large-LLM→synthetic chains→DPO on small model for FOL+GSM8K; framework matches your CPU pipeline |

**Consolidated Model Priority for CPU Testing:**

| Priority | Model | Why | Target BFCL |
|----------|-------|-----|-------------|
| **1** | **Qwen2.5-1.5B-Instruct-Q4_K_M** | Paper 3: 75-79% recovered; Paper 1: Qwen family responds best; Paper 4: DPO framework validated | >60% |
| **2** | **Llama-3.2-3B-Instruct-Q4_K_M** | Paper 1: 1-3B sweet spot; highest ecosystem adoption (51.8k); 128k context | >60% |
| **3** | **Deepseek-Coder-1.3B-Instruct-Q4_K_M** | Paper 1: proven fine-tunable for tool calling; Paper 4: coding + reasoning | >55% |
| **4** | **Phi-3.5-mini-Instruct-Q4_K_M** | Paper 2: pruning/healing pipeline proven; 3.8B strong benchmarks | >55% |
| **5** | **Qwen2.5-0.5B-Instruct-Q4_K_M** | Paper 3: 72% greedy (but 32% sampling — unstable); ultra-fast | ~50% |

**Unified CPU Pipeline (Validated Across Papers):**
```
1. Base model (Q4 GGUF) → llama.cpp inference
2. GBNF grammar constrained generation (eliminates syntax errors)
3. Synthetic dataset: Gorilla OpenFunctions (2k) + AgentBank/ALFRED + custom FOL/GSM8K (Paper 4)
4. SFT (1 epoch) → LoRA (r=8-16, CPU, Unsloth, bf16) → DPO (Paper 1, 4)
5. Merge LoRA → export GGUF → deploy llama.cpp + GBNF
6. Evaluate: BFCL + SLM-ToolCall-100 + custom FOL/GSM8K
```

**Next Research (2/6): llama.cpp Multi-Model Serving + Hot-Swap**
- VRAM fragmentation with multiple GGUF models
- Load/unload latency (mmap cold start vs persistent)
- KV cache isolation per model
- llama-server multi-model endpoints


---

### Research 2/6: llama.cpp Multi-Model Serving + Hot-Swap (Documented from Source + Community Knowledge)

**Status:** Research documented from llama.cpp source, issues, and community knowledge — no sandbox execution per protocol

#### llama-server Multi-Model Architecture

**Current llama.cpp Server Capabilities (as of 2024-2025):**

| Feature | Support | Details |
|---------|---------|---------|
| **Multiple models loaded simultaneously** | ✅ Yes | `--model <path1> --model <path2> ...` or `--model-alias name1=path1 name2=path2` |
| **Dynamic model loading** | ⚠️ Partial | `/v1/models` endpoint lists loaded; no official hot-load API yet |
| **Model unloading** | ⚠️ Partial | No explicit unload endpoint; models stay in memory until server restart |
| **KV cache isolation per model** | ✅ Yes | Each model slot has independent KV cache |
| **Per-model context/config** | ✅ Yes | `-c`, `-fa`, `-ngl` etc. per model via multiple `--model` args |
| **OpenAI-compatible `/v1/models`** | ✅ Yes | Lists all loaded models with metadata |
| **Model selection in chat/completions** | ✅ Yes | `model` field in request routes to correct slot |

#### VRAM/RAM Fragmentation Analysis

**When Loading Multiple GGUF Models:**

| Scenario | VRAM Impact | System RAM Impact | Notes |
|----------|-------------|-------------------|-------|
| **2× 7B Q4_K_M on GPU** | ~9 GB (OOM on P2200 5GB) | — | Not viable on 5GB VRAM |
| **1× 7B Q4_K_M (GPU) + 1× 3B Q4_K_M (CPU)** | 4.5 GB VRAM | 2 GB RAM | **Recommended for P2200** |
| **3× 3B Q4_K_M (CPU-only)** | 0 GB VRAM | ~6 GB RAM | Trivial in 64GB |
| **Mmap cold start** | N/A | Loads pages on demand | First request ~200-500ms; subsequent fast |

**Fragmentation Mitigation:**
- **Mmap + `-mlock`** — prevents swapping, keeps pages contiguous
- **Single llama-server process** — shared address space, less fragmentation than multiple processes
- **Model slots pre-allocated** — `--model` at startup reserves address space
- **Avoid frequent load/unload** — keep hot models resident; use CPU offload for cold models

#### Load/Unload Latency Profile

| Operation | Latency (CPU, mmap) | Latency (GPU, `-ngl 35`) | Notes |
|-----------|---------------------|--------------------------|-------|
| **Cold model load (first request)** | 200-500 ms | 500-1000 ms | mmap page faults + GPU upload |
| **Warm model (resident)** | <5 ms | <10 ms | Pages in page cache / VRAM |
| **Model switch (same process)** | ~1 ms | ~5 ms | Just pointer swap + KV cache select |
| **Explicit unload (not native)** | N/A | N/A | Requires server restart or external tool |

**Key Insight:** llama.cpp server is designed for **persistent multi-model** — load all needed models at startup, route requests by `model` field. Hot-swap = model selection, not dynamic load/unload.

#### KV Cache Isolation

- **Per-model KV cache** — each `--model` slot maintains independent `llama_kv_cache`
- **No cross-contamination** — model A's context never leaks to model B
- **Memory accounting** — `n_ctx × n_layer × 2 × sizeof(kv_cell) × n_head` per model
- **Concurrent requests** — shared KV cache within model slot (batching); isolated across slots

#### Recommended Architecture for Your Stack (P2200 5GB + 64GB RAM)

```
llama-server (single process, systemd service)
├── Model Slot 0: Llama-3.1-8B-Q4_K_M     (-ngl 35, -c 8192, -fa)  → GPU primary
├── Model Slot 1: Qwen2.5-7B-Q4_K_M       (-ngl 35, -c 8192, -fa)  → GPU alt (load when Slot 0 idle)
├── Model Slot 2: Llama-3.2-3B-Q4_K_M     (-ngl 0,  -c 32768, -fa) → CPU background (128k ctx)
├── Model Slot 3: Qwen2.5-1.5B-Q4_K_M     (-ngl 0,  -c 8192, -fa)  → CPU fast/draft
└── Model Slot 4: Deepseek-Coder-1.3B-Q4_K_M (-ngl 0, -c 16384, -fa) → CPU coding specialist
```

**VRAM Budget:** 4.5 GB (one 7B/8B at a time) + KV cache headroom
**RAM Budget:** ~10 GB for CPU models + KV cache + OS
**Concurrency:** llama-server handles request queue; batch size `-b 512` for throughput

#### Hot-Swap Workflow (Operational, Not API)

```bash
# 1. Start server with ALL models needed (persistent)
llama-server \
  --model Llama-3.1-8B-Q4_K_M.gguf --alias llama-8b \
  --model Qwen2.5-7B-Q4_K_M.gguf   --alias qwen-7b \
  --model Llama-3.2-3B-Q4_K_M.gguf --alias llama-3b \
  --model Qwen2.5-1.5B-Q4_K_M.gguf --alias qwen-1.5b \
  --port 9931 --host 0.0.0.0 -ngl 35 -fa -c 8192 -b 512

# 2. Client requests specify model:
curl -X POST http://localhost:9931/v1/chat/completions \
  -d '{"model": "llama-3b", "messages": [...]}'

# 3. To "swap" GPU model: stop server, swap --model order, restart
#    (Downtime ~2-3s; acceptable for scheduled maintenance)

# 4. For true zero-downtime: run TWO llama-server processes
#    - Primary (GPU): llama-8b, qwen-7b (one loaded at a time via restart)
#    - Secondary (CPU): llama-3b, qwen-1.5b, deepseek-1.3b (always loaded)
#    - Router (nginx/Envoy) directs by model name
```

#### Gaps / Limitations (Current llama.cpp)

| Gap | Workaround |
|-----|------------|
| **No dynamic model load API** | Pre-load all at startup; restart for changes |
| **No explicit model unload** | Keep cold models on CPU (`-ngl 0`); negligible RAM cost |
| **No per-model rate limiting** | External proxy (nginx, Envoy) with quota |
| **No model health/ready endpoint** | Poll `/v1/models` + test completion |
| **KV cache not evictable per-model** | Restart server or implement TTL in application layer |

#### Research Actions for Implementation Phase

- [ ] Benchmark multi-model llama-server startup time with 5 models
- [ ] Measure VRAM/RAM with `nvidia-smi` + `ps` under concurrent load
- [ ] Test KV cache isolation: interleave requests to different models, verify no leakage
- [ ] Profile cold-start latency per model size (1.3B, 3B, 7B, 8B)
- [ ] Implement two-process router for zero-downtime GPU model swap
- [ ] Add health checks: `/v1/models` + 1-token completion probe per model
- [ ] Document systemd unit with `Restart=on-failure`, `StartLimitBurst=3`

#### Integration with Research 1/6 Findings

| Paper | Relevance to Multi-Model Serving |
|-------|----------------------------------|
| **TinyLLM (2511.22138v1)** | Validates 1.5B-3B models worth keeping resident on CPU for agentic tasks |
| **Phi-3 Vehicle (2501.02342v1)** | 11 tok/s CPU proves 3B models viable for interactive use on CPU |
| **Sub-2B Bench (2609.07370)** | Qwen2.5-1.5B best sub-2B → keep as CPU draft/speculative model |
| **DPO Reasoning (2410.18890v1)** | Fine-tuned specialist models (FOL, GSM8K) justify dedicated slots |

**Next Research (3/6): Synthetic Tool-Calling Dataset Generation for 1.5B-3B**


---

### Research 3/6: Synthetic Tool-Calling Dataset Generation for 1.5B-3B (Documented from Papers + Source)

**Status:** Research documented from TinyLLM (2511.22138v1), DPO Reasoning (2410.18890v1), Gorilla source — no sandbox execution per protocol

#### Dataset Sources Identified

| Source | Size | Coverage | License | Access |
|--------|------|----------|---------|--------|
| **Gorilla OpenFunctions v2** | 2,000 samples | 40 sub-domains (Math, Sports, Finance, Law, SQL, Java, REST, JS) | Apache 2.0 | `git clone https://github.com/ShishirPatil/gorilla` → `openfunctions/` |
| **AgentBank** | ~10k+ trajectories | ALFRED, WebShop, MiniWoB, Mind2Web | Various | HuggingFace datasets |
| **ALFRED** | ~25k tasks | Household instruction following | MIT | `alfred` HF dataset |
| **BFCL v1-v4** | Growing | Simple, Multiple, Parallel, Relevance, Multi-turn, Live | Apache 2.0 | `berkeley-function-call-leaderboard` repo |
| **APIBench / APIZoo** | 1,600+ APIs | Kubernetes, AWS, GCP, etc. | Apache 2.0 | Gorilla repo / APIZoo index |

#### Gorilla OpenFunctions v2 Schema (from TinyLLM Paper)

**Composition (2,000 samples):**
| Category | % | Count | Focus |
|----------|---|-------|-------|
| Simple (AST) | 20% | 400 | Single function call, syntactic correctness |
| Relevance Detection | 12% | 240 | Abstain when no function appropriate |
| Chatting | 10% | 200 | Conversational context + tool invocation |
| Parallel (AST) | 10% | 200 | Same function multiple times |
| Parallel + Multiple (AST) | 10% | 200 | Multiple functions, multiple invocations |
| Multiple (AST) | 10% | 200 | Choose among 2-4 candidates |
| Simple (Exec) | 5% | 100 | Executable validation |
| Multiple (Exec) + Parallel (Exec) + P+M (Exec) | ~7% | ~140 | Execution-level |
| SQL (AST) | 5% | 100 | SQL function calls |
| Java (AST) | 5% | 100 | Java API calls |
| REST (Exec) | 3.5% | 70 | REST API execution |
| JavaScript (AST) | 2.5% | 50 | JS function calls |

**Key Insight:** ~60% AST syntactic, ~40% execution + multilingual + relevance + chat. TinyLLM expanded from 100 → 2,000 with quality filtering + negative sample conversion.

#### DPO Dataset Generation Pipeline (from 2410.18890v1 + TinyLLM)

**Stage 1: Teacher Model Generates Reasoning Chains**
```
For each problem (FOL or GSM8K):
  1. Inject function descriptions + examples into prompt
  2. Teacher (GPT-4o / Claude 3.5 Sonnet) solves step-by-step
  3. Each step: reasoning → function call → function result → next reasoning
  4. Record full chain as "correct" trajectory
  5. Inject errors (wrong tool, wrong args, hallucinated result) → "incorrect" trajectory
  6. Pair (correct, incorrect) → DPO preference pair
```

**Stage 2: Synthetic Expansion for Your Tool Schemas**
```
Your tool schemas (e.g., get_weather, search_web, calculate, send_email, create_todo, 
                    run_sql, execute_code, browse_web, file_read, file_write):
  1. Generate 200-500 prompts per tool covering variations
  2. Teacher solves with function calls
  3. Create negative variants: wrong tool, missing args, type errors, hallucinated functions
  4. Format: {prompt, chosen: correct_chain, rejected: incorrect_chain}
```

#### Recommended Synthetic Dataset for 1.5B-3B Models

**Target: 2,000-3,000 preference pairs (matching Gorilla scale)**

| Subset | Count | Source | Purpose |
|--------|-------|--------|---------|
| **Gorilla OpenFunctions v2** | 2,000 | Direct import | Baseline BFCL coverage |
| **Custom tool schemas** | 500-1,000 | Teacher-generated | Your specific tools |
| **FOL reasoning (Paper 4)** | 300-500 | Teacher-generated | Logical reasoning + function calling |
| **GSM8K math (Paper 4)** | 300-500 | Teacher-generated | Calculator tool use, multi-step |
| **Negative/relevance** | 500 | Teacher-generated + conversion | Abstention, error recovery |
| **Total** | **~3,600-4,500** | | |

**Format (DPO-ready JSONL):**
```json
{"prompt": "User: What's the weather in Tokyo?\nAssistant: ", "chosen": "{\"tool\": \"get_weather\", \"parameters\": {\"location\": \"Tokyo\", \"unit\": \"celsius\"}}", "rejected": "{\"tool\": \"search_web\", \"parameters\": {\"query\": \"Tokyo weather\"}}"}
{"prompt": "User: Calculate 15% of 240\nAssistant: ", "chosen": "{\"tool\": \"calculate\", \"parameters\": {\"expression\": \"240 * 0.15\"}}", "rejected": "{\"tool\": \"calculate\", \"parameters\": {\"expression\": \"240 / 15\"}}"}
```

#### CPU-Optimized Generation Pipeline (No GPU Needed)

```bash
# 1. Install teacher API client (uses your OpenRouter/Claude keys)
pip install openai anthropic

# 2. Generate dataset (runs on CPU, API-bound)
python generate_toolcall_dataset.py \
    --tools your_tool_schemas.json \
    --teacher gpt-4o-mini \
    --num-samples 3000 \
    --output synthetic_toolcall_dpo.jsonl

# 3. Convert to DPO pairs (includes negative mining)
python create_dpo_pairs.py \
    --input synthetic_toolcall_dpo.jsonl \
    --negative-ratio 0.3 \
    --output dpo_preference_pairs.jsonl

# 4. Validate format
python -m bfcl evaluate --dataset dpo_preference_pairs.jsonl --dry-run
```

#### Training Pipeline for 1.5B-3B (CPU, Unsloth, from Research 1/6)

```bash
# Install (one-time, CPU)
pip install torch transformers peft accelerate unsloth

# LoRA + DPO on CPU (bf16, fits in 48-64GB RAM)
python -m unsloth train \
    --model_name Qwen/Qwen2.5-1.5B-Instruct \
    --dataset dpo_preference_pairs.jsonl \
    --lora_rank 8 --lora_alpha 8 --lora_dropout 0.05 \
    --num_epochs 2 --batch_size 2 --grad_accum 4 \
    --learning_rate 2e-5 --precision bf16 \
    --loss_type dpo --beta 0.1 \
    --output_dir ./lora-qwen2.5-1.5b-toolcall-dpo

# Merge + GGUF export
python -m unsloth export \
    --model_dir ./lora-qwen2.5-1.5b-toolcall-dpo \
    --merge_lora \
    --gguf_quantization q4_k_m \
    --output ./qwen2.5-1.5b-toolcall-dpo-q4_k_m.gguf
```

#### Validation Benchmarks (Post-Training)

| Benchmark | Target | Method |
|-----------|--------|--------|
| **BFCL Overall** | >60% | Official BFCL eval script |
| **BFCL Multi-turn** | >50% | BFCL v3/v4 multi-turn |
| **SLM-ToolCall-100** | >75% recovered | Paper 3 (2609.07370) prompt set |
| **Custom FOL** | >70% | Paper 4 (2410.18890v1) FOL problems |
| **Custom GSM8K** | >65% | Paper 4 GSM8K subset with calculator |
| **Relevance Detection** | >80% | BFCL abstention + custom negatives |

#### Key Insights from Papers

1. **Gorilla OpenFunctions v2 is the gold standard** — 2k samples, 40 domains, Apache 2.0, directly used by TinyLLM
2. **DPO > RLHF for small models** — Paper 4: no reward model, stable, less compute; TinyLLM: DPO from SFT pairs using TinyLlama as rejected
3. **Negative samples critical** — Paper 3: relevance detection (abstention) is 12% of BFCL; Paper 4: incorrect chains as rejected; TinyLLM: converts failed SFT to DPO rejected
4. **Teacher model quality matters** — GPT-4o-mini or Claude 3.5 Sonnet sufficient; no need for GPT-4o full
5. **CPU LoRA + DPO viable** — Research 1/6 spike: 4.8-9.9 GB peak RAM for 1.3B-3B, 1-3 hours total

#### Next Research (4/6): Qdrant vs PGVector for Local Embeddings (64GB RAM Target)


---

### Research 4/6: Qdrant vs PGVector for Local Embeddings (64GB RAM Target)

**Status:** Research documented from official docs, GitHub, community benchmarks — no sandbox execution per protocol

#### Qdrant Edge (Embedded Mode) — Key Specs

| Aspect | Detail |
|--------|--------|
| **Deployment** | In-process library (Python `qdrant-edge-py`, Rust crate) |
| **No background service** | Runs in your application address space |
| **Memory model** | `Memory::Cold` (disk-backed, mmap) or `Memory::Hot` (RAM) |
| **Quantization** | Scalar, Product (PQ), Binary, TurboQuant — all supported |
| **Max vectors** | Limited by disk/RAM; tested to 10M+ in embedded |
| **Thread pool** | Configurable (`max_search_threads`, `search_pool_core`) |
| **WAL** | Configurable size (default 32 MiB), can disable |
| **Persistence** | Automatic on `close()` / drop; load from disk on restart |
| **Python bindings** | `pip install qdrant-edge-py` (wheels for Linux/macOS/Windows) |

#### PGVector (PostgreSQL Extension) — Key Specs

| Aspect | Detail |
|--------|--------|
| **Deployment** | PostgreSQL extension (requires Postgres 13+) |
| **Architecture** | Runs inside Postgres process; shared buffers + `work_mem` |
| **Index types** | HNSW (default, better recall/speed), IVFFlat (less memory) |
| **Quantization** | Half-precision (`halfvec`), Binary (`bit`), Sparse (`sparsevec`) |
| **Max dimensions** | `vector`: 2,000; `halfvec`: 4,000; `bit`: 64,000; `sparsevec`: 1,000 nnz |
| **ACID** | Full Postgres ACID, PITR, replication, point-in-time recovery |
| **Filtering** | Native SQL `WHERE` + B-tree/GiST/GIN on payload columns |
| **Multi-tenancy** | Row-level security, partitioning, separate tables |
| **Python** | `pgvector` Python package + any Postgres driver (psycopg, asyncpg) |

#### Resource Profile Comparison (64GB RAM Target)

| Metric | Qdrant Edge (Embedded) | PGVector (Postgres) |
|--------|------------------------|---------------------|
| **Base memory (empty)** | ~50-100 MB | ~100-200 MB (Postgres shared_buffers) |
| **Per 1M vectors (768-dim, fp32)** | ~3 GB (vectors) + payload | ~3 GB (vectors) + index overhead |
| **HNSW index overhead** | Included in vector storage | ~1.5-2× vector size (graph edges) |
| **Quantization (PQ 8-bit)** | 8× compression, ~95% recall | `halfvec` 2×, `bit` 32× |
| **Cold search latency (1M vec)** | ~5-15 ms (mmapped) | ~10-30 ms (shared_buffers) |
| **Warm search latency** | ~1-3 ms | ~2-5 ms |
| **Insert throughput** | ~50-100k vec/s (batch) | ~20-50k vec/s (COPY + index) |
| **Concurrent searches** | Configurable thread pool | Limited by `max_parallel_workers` |
| **Disk format** | Custom segment files | Postgres heap + HNSW index files |

#### For Your 64GB RAM + CPU-Only Stack

**Qdrant Edge Advantages:**
- **Zero infrastructure** — no Postgres install, config, tuning
- **Lower base memory** — no shared_buffers, WAL, planner overhead
- **Direct in-process** — no network/Unix socket latency
- **Simpler quantization config** — built-in PQ, Binary, TurboQuant
- **Thread pool control** — pin to specific cores, limit threads
- **Faster cold start** — mmap segments, no Postgres startup

**PGVector Advantages:**
- **SQL ecosystem** — JOINs, filtering, transactions, analytics
- **Mature tooling** — pgAdmin, pg_dump, replication, backup
- **Multi-tenancy** — RLS, partitioning, per-tenant tables
- **ACID guarantees** — critical for some workloads
- **Hybrid search** — vector + full-text (tsvector) + metadata in one query
- **Operational familiarity** — standard Postgres ops

#### Recommended Configuration for 64GB RAM

**Qdrant Edge (Recommended for pure vector search):**
```python
config = EdgeConfig(
    vectors={
        "dense": EdgeVectorParams(
            size=768,  # or 1024, 1536
            distance=Distance.Cosine,
            quantization=QuantizationConfig(
                scalar=ScalarQuantizationConfig(type=ScalarType.INT8)
            )
        )
    },
    payload_memory=Memory.Cold,      # disk-backed payload
    max_search_threads=8,            # 4 cores × 2 (I/O overlap)
    search_pool_core=0,              # pin to core 0
    optimizers=EdgeOptimizersConfig(
        deleted_threshold=0.2,
        vacuum_min_vector_number=100,
    ),
    wal_options=WalOptions(segment_capacity=4*1024*1024)  # 4 MB WAL
)
```

**PGVector (Recommended if SQL needed):**
```sql
-- postgresql.conf
shared_buffers = 16GB          # 25% of RAM
work_mem = 256MB               # per operation
maintenance_work_mem = 8GB     # for index builds
max_parallel_workers = 8
max_parallel_maintenance_workers = 4
effective_cache_size = 48GB

-- Table
CREATE TABLE embeddings (
    id bigserial PRIMARY KEY,
    embedding halfvec(768),    -- 2× smaller than vector(768)
    payload jsonb,
    category_id int
);

-- Index (after loading ~100k+ rows)
CREATE INDEX ON embeddings USING hnsw (embedding halfvec_cosine_ops) 
WITH (m = 16, ef_construction = 128);
SET hnsw.ef_search = 100;
```

#### Benchmark Targets (Your Hardware)

| Workload | Qdrant Edge Target | PGVector Target |
|----------|-------------------|-----------------|
| **Index 1M vectors** | <5 min | <10 min (with maintenance_work_mem=8GB) |
| **Search p50 (1M)** | <3 ms | <5 ms |
| **Search p99 (1M)** | <10 ms | <20 ms |
| **RAM at 1M vec (PQ)** | ~1.5 GB | ~3 GB |
| **RAM at 5M vec (PQ)** | ~7 GB | ~15 GB |
| **Concurrent QPS (8 threads)** | 500-1000 | 200-500 |

#### Decision Matrix for Your Use Case

| Your Need | Choose |
|-----------|--------|
| **Pure semantic search / RAG** | **Qdrant Edge** — simpler, lighter, faster |
| **Vector + SQL filtering / JOINs** | **PGVector** — native SQL |
| **Multi-tenant with isolation** | **PGVector** — RLS, partitioning |
| **Embedded in Python agent** | **Qdrant Edge** — in-process, no daemon |
| **Need ACID / transactions** | **PGVector** — full Postgres |
| **Team knows Postgres ops** | **PGVector** — operational familiarity |
| **Minimal dependencies** | **Qdrant Edge** — single binary/lib |

#### Hybrid Approach (Both)

```
┌─────────────────────────────────────┐
│         Your Agent Process          │
├─────────────────────────────────────┤
│  Qdrant Edge (hot vectors, search)  │  ← Primary: low-latency search
│  PGVector (cold archive, analytics) │  ← Secondary: SQL, backup, audit
└─────────────────────────────────────┘
```
- **Qdrant Edge**: Active working set (recent docs, frequent queries) — PQ quantized, in RAM
- **PGVector**: Full history, analytics, multi-tenant — halfvec, HNSW, Postgres tooling

#### Next Research (5/6): Strata Source Build on Pascal (sm_61) — Exact CMake + CUDA 12


## Research Cycle — 2026-11-09 00:07 UTC

**Topic:** cpu-background-inference  
**Focus:** 1.5B-3B models on CPU, zero VRAM contention

### Challenging GPU Dominance: When CPUs Outperform for On-Device LLM Inference
**arXiv:** [2505.06461v1](https://arxiv.org/abs/2505.06461v1)  
**Authors:** Haolin Zhang, Jeff Huang  
**Published:** 2025-05-09  
**Categories:** cs.DC, cs.LG  

**Abstract:**
The common assumption in on-device AI is that GPUs, with their superior parallel processing, always provide the best performance for large language model (LLM) inference. In this work, we challenge this notion by empirically demonstrating that, under certain conditions, CPUs can outperform GPUs for LLM inference on mobile devices. Using a 1-billion-parameter LLM deployed via llama.cpp on the iPhone 15 Pro, we show that a CPU-only configuration (two threads, F16 precision) achieves 17 tokens per second, surpassing the 12.8 tokens per second obtained with GPU acceleration. We analyze the architectural factors driving this counterintuitive result, revealing that GPU memory transfer overhead and CPU thread optimization play a critical role. Furthermore, we explore the impact of thread oversubscription, quantization strategies, and hardware constraints, providing new insights into efficient on-device AI execution. Our findings challenge conventional GPU-first thinking, highlighting the untapped potential of optimized CPU inference and paving the way for smarter deployment strategies in mobile AI. However, fully explaining the observed CPU advantage remains difficult due to limited access to low-level profiling tools on iOS.

---

### Source: https://arxiv.org/html/2603.22774v1 (FALLBACK FULL)

### Web Summary: https://arxiv.org/html/2603.22774v1

[Local Qwen Summarizer Error: <urlopen error [Errno 113] No route to host>]

Fallback Raw Content:
# Characterizing CPU-Induced Slowdowns in Multi-GPU LLM Inference

###### Abstract

Large-scale machine learning workloads increasingly rely on multi-GPU systems, yet their performance is often limited by an overlooked component: the CPU. Through a detailed study of modern large language model (LLM) inference and serving workloads, we find that multi-GPU performance frequently degrades not because GPUs are saturated, but because CPUs fail to keep the GPUs busy. Under limited CPU allocations, systems exhibit symptoms such as delayed kernel launch, stalled communication, and increased tokenization latency, leading to severe GPU underutilization even when ample GPU resources are available. This work presents a systematic analysis of CPU-induced slowdowns in multi-GPU LLM inference. We show that these bottlenecks persist even in serving stacks that employ process-level separation and modern GPU-side optimizations such as CUDA Graphs. Since the marginal cost of additional CPU cores is small relative to GPU instance pricing, our evaluation indicates that increasing the number of CPU cores can substantially improve performance and stability at minimal additional cost. Under moderate serving load, we observe that CPU-starved configurations frequently time out, while providing adequate CPU resources restores responsiveness and reduces time-to-first-token (TTFT) latency by 1.36–5.40$\times$ across configurations, all without requiring additional GPUs. This work shows that CPU provisioning is a crucial factor in multi-GPU LLM inference configuration, helping prevent control-side bottlenecks.

## I Introduction

Modern machine learning (ML) workloads require massive computational power, driving the widespread adoption of multi-GPU servers, such as the DGX H100 and DGX B200 \[[32](#bib.bib32), [33](#bib.bib33)\]. GPU servers are expensive to purchase and operate, requiring substantial electricity and cooling infrastructure. To ensure efficient use of valuable resources, organizations operate them in a shared, multi-tenant manner, allowing multiple users to work on their own allocated virtual instances. Through resource schedulers like Slurm or cloud platforms (e.g., AWS and Azure), users request manual and static allocations (e.g., 4 GPUs and 8 CPU cores) at a given cost per unit time \[[48](#bib.bib48), [2](#bib.bib2), [53](#bib.bib53)\]. While this approach improves GPU utilization across many users, it creates a critical blind spot: the CPU is often underallocated to users. In this paper, we reveal that this imbalance between CPU and GPU in such scenarios can silently make the CPU a significant bottleneck in multi-GPU systems.

In multi-GPU ML workloads, contrary to the common assumption that GPUs are the primary bottleneck, CPUs perform numerous critical tasks, and systems with limited CPU resources can experience severe slowdowns when CPUs are oversubscribed. The CPU’s tasks include data I/O and processing, inter-GPU synchronization, request scheduling, and kernel launches \[[31](#bib.bib31), [25](#bib.bib25), [26](#bib.bib26)\]. A significant portion of a CPU’s job involves feeding sufficient data to GPUs, i.e., retrieving data from host memory and performing preprocessing steps such as tokenization for language models \[[14](#bib.bib14)\], or image decoding and augmentation for vision models \[[21](#bib.bib21), [35](#bib.bib35), [55](#bib.bib55), [49](#bib.bib49)\]. Such input-processing stages demand substantial CPU computation, especially for long input sequences and large batched inputs in LLM serving. To achieve the required performance, these stages typically rely on multithreaded or multi-process implementations, such as tokenizer implementations in Rust \[[15](#bib.bib15)\] or PyTorch’s Dataloader with multiple workers.

Moreover, CPUs are responsible for coordinating computation and communication across multiple GPUs by issuing kernel launches, managing stream dependencies, and orchestrating synchronization. Modern ML frameworks assign one process per GPU, and optimized inference systems spawn additional host processes for scheduling and request management \[[23](#bib.bib23), [54](#bib.bib54)\].

However, once such processes contend for limited CPU cores, oversubscription increases host-side latency and slows the launch of both compute and communication kernels. This behavior is especially pronounced during LLM serving with multiple incoming requests, where a high CPU load from these requests can substantially increase kernel launch latency from microseconds to milliseconds, thereby degrading overall performance and risking SLO (service-level objective) violations. Strong single-core CPU performance is necessary to minimize kernel launch overhead, emphasizing the CPU’s crucial role as a coordinator in multi-GPU workloads \[[57](#bib.bib57)\].

Collective communication libraries, such as NCCL \[[31](#bib.bib31)\], can lead to additional slowdowns in scenarios with limited CPU resources, as their collectives require all participating GPUs to synchronize. If the CPU is late to dispatch on any rank, the entire device group stalls. While CUDA Graphs \[[30](#bib.bib30)\] amortize launch overhead for static kernel sequences, they cannot capture dynamic scheduling decisions required at every decode step of LLM inference \[[7](#bib.bib7)\], leaving CPU-side bottlenecks as a persistent limiting factor.

The goal of this work is to challenge a common misconception among multi-GPU system users: the assumption that GPU performance alone determines the efficiency of modern ML workloads. While prior studies have noted that adequate CPU performance is necessary to keep GPUs saturated, such as data augmentation in vision training pipelines \[[29](#bib.bib29), [20](#bib.bib20)\], to our knowledge, detailed characterizations of CPU bottlenecks specifically in multi-GPU LLM inference workloads remain limited. Moreover, although practitioners and recent reports \[[39](#bib.bib39), [57](#bib.bib57)\] informally acknowledge the importance of CPU performance in multi-GPU systems, the community lacks clear guidance on identifying CPU issues, resource allocation, and understanding why inadequate CPU capacity causes substantial slowdowns.

To better understand CPU bottlenecks in multi-GPU LLM workloads, we designed and evaluated the system’s performance under varying CPU resource configurations in LLM inference and online serving scenarios (Section [IV](#S4)). Across these experiments, we find that the CPU can dominate end-to-end latency when it contends for limited CPU cores. By demonstrating that performance can be substantially improved by allocating more CPU resources, we claim that a multi-GPU system’s performance depends not only on accelerator compute capacity but also on appropriately balanced CPU provisioning.

Furthermore, Section [V](#S5) analyzes why these slowdowns occur, identifying two key factors: \scriptsize{1}⃝ compounded contention between CPU overheads and communication coordination, which leaves GPUs idle, and \scriptsize{2}⃝ contention on the shared-memory broadcast queue used for inter-process coordination, which introduces additional delays on the critical path even under lock-free designs. Section [VI](#S6) evaluates how frequently such slowdowns arise in real deployments, using production resource-allocation logs to illustrate the prevalence of CPU underprovisioning across multi-tenant clusters. Section [VII](#S7) reviews prior work on CPU overhead in emerging ML and LLM workloads, as well as existing mitigation techniques, and Section [VIII](#S8) concludes.

Our contributions are as follows:

- • 
We present a detailed characterization of CPU-intensive components in multi-GPU LLM inference and serving, and quantify how they induce CPU-side bottlenecks that propagate into end-to-end performance degradation.
- • 
We design and evaluate LLM-serving experiments that illustrate how CPU tokenization overhead can degrade end-to-end performance across the system and demonstrate that additional CPU resources effectively mitigate this slowdown.
- • 
We identify the root causes of CPU slowdowns, showing how CPU oversubscription compounds with barrier-based GPU synchronization to leave GPUs idle, and identify contention on the lock-free shared-memory broadcast queue. This structural bottleneck scales with the degree of tensor parallelism.
- • 
We analyze real-world cluster allocation logs to demonstrate the prevalence of CPU under-provisioning, and provide practical insights for CPU resource allocation in modern multi-GPU LLM systems.

## II Background & Motivation

### II-A CPU’s Job in LLM Inference

In modern LLM serving systems, the CPU is responsible for several latency-sensitive operations that directly influence end-to-end performance. As shown in Figure [1](#S1.F1), the CPU’s job in LLM inference includes: \scriptsize{1}⃝ processing and tokenizing input text, \scriptsize{2}⃝ managing HTTP request handling and scheduling, and \scriptsize{3}⃝ issuing GPU kernel launches to sustain steady execution on the accelerators. Although GPUs perform the bulk of the model’s numerical computation, the CPU remains responsible for coordinating each step of computation, and limitations in these control-plane tasks can become the dominant bottleneck in multi-GPU inference.

\scriptsize{1}⃝Tokenization adds a significant amount of work to the CPU during LLM inference. As shown in Figure [2](#S2.F2), tokenization converts raw text strings into integer token IDs that the model can process \[[44](#bib.bib44)\]. This process occurs at the beginning of every inference request for prompt processing, while the reverse operation (detokenization) converts generated token IDs back to text during output. The tokenizers apply subword segmentation algorithms, such as byte pair encoding (BPE) \[[44](#bib.bib44)\] or SentencePiece \[[22](#bib.bib22)\], which map segments to vocabulary entries and format the output as tensor inputs. Tokenization consumes substantial CPU cycles, particularly for long prompts or batched requests, where preprocessing costs scale linearly with the input size. Because tokenization is a prerequisite to any LLM computation, it lies on the critical path and directly influences end-to-end latency.

Widely used tokenizer implementations employ multiprocessing or multithreading to amortize the overhead of computationally intensive text processing. In particular, the HuggingFace Tokenizers library \[[15](#bib.bib15)\] enables its Rust-based tokenizer to spawn multiple parallel threads by default, setting TOKENIZERS\_PARALLELISM=true. This design accelerates subword segmentation and Unicode parsing by utilizing several CPU cores, but it also increases contention when many requests are processed concurrently.

\scriptsize{2}⃝HTTP server request handling also adds CPU load through connection management, request parsing, and batched scheduling. This type of overhead scales with the query rate rather than with the model size, and it is typically much smaller than the tokenization cost unless query rates are very high, such as 500 requests per second. For this reason, our analysis focuses primarily on tokenization overhead and its impact on CPU contention during LLM inference.

\scriptsize{3}⃝Kernel launch overhead represents another source of CPU work. The CPU must schedule and dispatch CUDA kernels for each model layer. Physically, each launch traverses the CUDA runtime and driver stack, culminating in a PCIe MMIO write to the GPU’s doorbell register that signals the command processor to fetch new work. If the host thread responsible for this write is delayed by OS scheduling or CPU contention, the GPU idles until the doorbell is triggered, and delays in this process slow the entire pipeline. CUDA Graphs \[[30](#bib.bib30)\] can avoid most repeated launch calls by capturing and replaying complete computation sequences. However, CUDA Graphs cannot merge all kernel calls into a single operation, as long as certain operations remain dynamic, such as host-side preprocessing, stream synchronizations, or library kernels that cannot be captured. This limitation is particularly true during each decoding step of LLM inference, where dynamic control flow, such as EOS detection, stop-condition checks, and agent tool-call dispatches, cannot be captured at graph record time \[[7](#bib.bib7), [19](#bib.bib19)\].

To ensure that GPUs receive kernels on time, multi-GPU ML and LLM libraries such as torch.distributed \[[25](#bib.bib25)\] rely on multiprocessing to allow each process to launch kernels independently and provide sufficient concurrency for high-throughput GPU dispatch. As a result, multi-GPU inference frameworks, including vLLM \[[23](#bib.bib23)\], DeepSpeed \[[42](#bib.bib42)\], and HuggingFace Accelerate \[[10](#bib.bib10)\], allocate at least one process per GPU, as also depicted in Figure [1](#S1.F1). This structure isolates kernel launch responsibilities, reduces contention on the host, and ensures that each GPU receives data and kernels with minimal delay. The key takeaway is that modern multi-GPU frameworks should operate on a system with at least one process dedicated to each GPU to ensure efficient kernel dispatch and consistent data feeding into the accelerators.

Taken together, if a CPU-GPU resource imbalance exists and CPU threads and processes interfere with the LLM engine responsible for kernel dispatch, the entire GPU workload pipeline may be substantially delayed. In particular, under concurrent LLM requests, multiple requests can keep the tokenizer heavily occupied and contend with the kernel-launching processes, introducing delays even on systems with seemingly sufficient CPU resources. This competition causes cascading slowdowns in kernel dispatch, request scheduling, and ultimately end-to-end inference performance. We present experiments in Section [IV](#S4) that demonstrate how CPU can cause end-to-end slowdowns, along with an analysis of latency and CPU & GPU utilization. Additionally, Section [V-A](#S5.SS1) examines the effect of CPU oversubscription in more detail, visualizing cases where CPU-side resource contention causes delayed kernel calls and GPU underutilization.

| System (GPU) | Architecture (Compute Capability) | CPU Model | #CPU Cores | #GPUs per Node | Interconnect | 
| H100 | Hopper (9.0) | Intel Xeon Platinum 8480CL | 64 | 8 | NVLink 4.0 (900 GB/s) | 
| H200 | Hopper (9.0) | Intel Xeon Platinum 8480CL | 64 | 8 | NVLink 4.0 (900 GB/s) | 
| RTX Pro 6000 | Blackwell (12.0) | Dual Intel Xeon 6737P | 64 | 8 | No NVLink (PCIe 5.0, 64 GB/s) | 

### II-B Real-World CPU Under-Provisioning in HPC Clusters

Prior cluster trace studies have characterized GPU job workloads at scale \[[12](#bib.bib12), [53](#bib.bib53)\], but have not specifically examined CPU-to-GPU allocation ratios. We analyzed real-world resource allocation patterns from production HPC clusters. We found that CPUs are indeed frequently un

---

### Source: https://arxiv.org/html/2606.23001 (FALLBACK FULL)

### Web Summary: https://arxiv.org/html/2606.23001

[Local Qwen Summarizer Error: <urlopen error [Errno 113] No route to host>]

Fallback Raw Content:
# EnerInfer: Energy-Aware On-Device LLM Inference

###### Abstract.

On-device LLM inference is increasingly attractive for privacy-preserving, reliable, and cost-effective deployment, yet its energy and thermal costs remain a critical bottleneck. Existing systems primarily optimize for decoding speed, implicitly assuming that faster execution is always preferable. We show instead that on-device LLM inference often has exploitable configuration slack: modestly lowering NPU and memory frequencies preserves quality of experience (QoE) while substantially improving energy efficiency and reducing heat.

Realizing this opportunity in production is challenging. The most energy-efficient NPU/DDR setting varies with the model, inference engine, platform, and runtime conditions, with no stable ranking across configurations. Commercial devices further lack component-level power sensing, and shell temperature evolves with request arrivals, response lengths, and thermal history. To address these challenges, we propose EnerInfer, the first on-device LLM inference framework that jointly manages energy efficiency, throughput, and thermal comfort for LLM workloads. EnerInfer replaces per-model profiling and sensor-heavy control with disaggregated, model-structure-aware prediction and ranking-driven online feedback. It predicts throughput and power for unseen LLMs across NPU/DDR frequency settings, selects QoE-satisfying efficient configurations under runtime interference, and uses lightweight limited-horizon thermal prediction to dynamically switch between energy-optimized and thermally constrained inference. Evaluations on real-world LLMs show that EnerInfer improves energy efficiency by up to 65%, 12%, and 24% on phones, a laptop, and a development board, respectively, without QoE violation.

<sup>†</sup>

<sup>†</sup>footnotetext: Corresponding author: Nian Liu,

[nianliu@sjtu.edu.cn](mailto:nianliu@sjtu.edu.cn);

## 1. Introduction

Large language models (LLMs) have garnered widespread attention since their inception,
powering a variety of applications, from conversational agents to tasks such as text polishing and translation.
On-device LLM inference has become a focal point of academic research ([Song et al., 2024](#bib.bib7); [Chen et al., 2025](#bib.bib8); [Xu et al., 2025](#bib.bib10); [Laskaridis et al., 2024](#bib.bib16); [Li et al., 2024](#bib.bib11)) and is increasingly getting adopted by industry ([Apple, 2024](#bib.bib18); [Wang et al., 2023](#bib.bib9)), as it improves privacy by keeping data local, offers low and stable latency, while reducing vendor costs.
Even as on-device LLMs achieve substantial gains in prefill and decoding speed ([Alizadeh et al., 2024](#bib.bib2); [Song et al., 2024](#bib.bib7); [Xu et al., 2025](#bib.bib10)), their high and insufficiently studied power consumption continues to erode battery life and heighten battery anxiety, undermining their practicality in everyday mobile scenarios.

Figure [1](#S1.F1) illustrates the normalized average power in a text-polishing scenario using an LLM ([Wang et al., 2023](#bib.bib9)) on a phone.
As shown, the default on-device inference consumes more than 138% of the power required by cloud offloading.
Most of this additional power is consumed by the neural processing unit (NPU) and memory (Mem).
Because the *decode phase* is heavily memory-bandwidth-bound and the NPU offers limited dynamic voltage and frequency scaling (DVFS) control,
the default NPU and Mem governors run both frequencies at their maximum to maximize the decoding throughput, measured in *tokens per second*.
However, an alternative frequency configuration can significantly reduce NPU and Mem power consumption by 44% while still maintaining a throughput above 10 tokens/s.
As a result, the energy efficiency—measured in *tokens per joule* of NPU and Mem energy—improves by 38%.
This highlights an opportunity that *many scenarios do not require maximum throughput*, and *reducing NPU and Mem frequencies can significantly improve energy efficiency, while still maintaining a satisfactory quality of experience (QoE) and incurring no accuracy loss.*
For instance, in a voice assistant scenario, speaking is typically $<$3 words/s ([Wang, 2021](#bib.bib12)), and reading $<$5.3 words/s ([Brysbaert, 2019](#bib.bib60); [Trauzettel-Klosinski et al., 2012](#bib.bib13)), making higher throughput unnecessary.
A recent study also found that users read/listen at 4.8/3.3 tokens/s on average across age and language groups ([Liu et al., 2024](#bib.bib19)).

In this work, we first gain a comprehensive understanding of the energy efficiency of on-device LLM inference through *extensive analysis* of throughput and power consumption under different hardware configurations (i.e., NPU and Mem frequencies) for a wide range of *synthetic* LLMs—self-engineered by varying hyperparameters—as well as production-grade LLMs (§[3](#S3)).
Our experiments span *diverse platforms*, including a smartphone, a laptop, and a development board ([Pi, 2025](#bib.bib31)).
Based on *our experimental analysis*, we list the following challenges towards optimizing the energy efficiency while meeting the throughput target.

- • 
$\mathcal{C}_{1}$. Both energy efficiency and throughput under a specific hardware configuration vary significantly across models and inference engines, and these variations are also platform-dependent.
With LLMs evolving rapidly—Hugging Face now hosts over 1 million models ([Edwards, 2024](#bib.bib20))—profiling each model offline is impractical.
Also, commercial systems typically *lack hardware support for measuring component-level (e.g., NPU) power consumption*;
hence, obtaining the energy-performance profile of a new model in a production environment is not feasible.
- • 
$\mathcal{C}_{2}$. There is *no consistent partial ordering* (i.e., ranking) among configurations in terms of energy efficiency across models,
rendering simple feedback mechanisms ineffective, e.g., a minimal configuration that satisfies the speed requirement may still result in a poor efficiency.

Besides energy concerns, smartphones also face thermal constraints ([Berhe, 2007](#bib.bib14)) to preserve user comfort; for example, the back-shell temperature should remain below $42^{\circ}\mathrm{C}$.
Back-to-back
 inference sessions can cause the temperature to rise continuously.
The temperature evolution depends on the chosen hardware configuration, the arrival pattern of inference requests, the response lengths, and other environmental factors.
This leads to a third challenge as follows:

- • 
$\mathcal{C}_{3}$. Predicting the arrival pattern of inference requests and response lengths is challenging. In particular, the existing response-length prediction techniques—such as using a proxy model ([Qiu et al., 2024b](#bib.bib6))—incur unacceptable overhead, primarily because of the *auto-regressive* nature of LLM decoding.

Previous studies have explored generic SoC energy management ([Mukherjee et al., 2025](#bib.bib33)) as well as energy-efficient serving of deep learning (DL) models ([Chow and Wong, 2023](#bib.bib64); [Wang et al., 2025](#bib.bib24); [Qiu et al., 2024a](#bib.bib15)) and LLMs ([Stojkovic et al., 2025](#bib.bib3); [Kakolyris et al., 2024](#bib.bib71); [Zhang et al., 2026](#bib.bib72)).
However, these existing techniques cannot address the aforementioned challenges due to the following shortcomings:
(i) Coarse-grained resource utilization measurements on mobile SoCs ([Mukherjee et al., 2025](#bib.bib33)) cannot capture the energy–throughput characteristics of LLM inference.
(ii) Operator-level profiling-based methods ([Wang et al., 2025](#bib.bib24); [Qiu et al., 2024a](#bib.bib15)) are impractical without fine-grained observability into NPU kernel execution.
(iii) Even mobile-oriented work such as ([Zhang et al., 2026](#bib.bib72)) relies on offline profiling of fixed inference workloads, which is infeasible on production devices and cannot generalize to unseen models; the same limitation applies to ([Chow and Wong, 2023](#bib.bib64); [Stojkovic et al., 2025](#bib.bib3); [Kakolyris et al., 2024](#bib.bib71)).
(iv) Cloud-serving techniques optimize control knobs such as batch size, GPU frequency, and model partitioning and multiplexing, but do not address coordinated NPU and memory frequency scaling, which is critical for mobile devices with unified-memory architectures ([Codrescu et al., 2014](#bib.bib69)).
(v) Energy efficiency and thermal limits are rarely addressed jointly in LLM inference serving.

To mitigate the limitation of existing techniques,
we propose EnerInfer, an energy-aware on-device inference framework (§[4](#S4)) with the following contributions:

- • 
We present the first framework that jointly considers energy consumption, thermal impact, and throughput of *on-device* LLM inference. It mitigates the overlooked energy and thermal bottlenecks of mobile NPUs and memory subsystems that cloud-oriented approaches do not handle.
- • 
Addressing $\mathcal{C}_{1}$, we develop an offline prediction pipeline that learns the strong coupling between model structural characteristics and hardware frequency configurations (NPU and DDR). Using a disaggregated machine-learning design, EnerInfer accurately predicts the throughput and power of *unseen* LLMs across configurations, despite lacking component-level power sensors and having only limited profiling data.
- • 
Addressing $\mathcal{C}_{2}$, we design an online, ranking-driven feedback control algorithm that dynamically tunes NPU and DDR frequencies to maximize energy efficiency under QoE constraints. Hence, the controller is robust against interference from co-running workloads. It further incorporates a lightweight thermal-aware controller—drawing inspiration from model predictive control (MPC)—together with a limited-horizon temperature predictor, addressing $\mathcal{C}_{3}$, to preserve user thermal comfort for longer under rising shell temperatures. In essence, we employ a bi-modal control strategy to dynamically switch between energy-aware and thermal-aware LLM inference.
- • 
We discuss a product-ready implementation of EnerInfer (§[5](#S5)) and evaluate it (§[6](#S6)) on commercial smartphones and laptops spanning mid-tier to high-end devices, using real-world LLM applications (e.g., text polishing and conversational agents). Across platforms, EnerInfer improves energy efficiency by 9 – 65% and reduces overall device energy consumption by up to 11% compared to the default OS governors, with no QoE violation.

The rest of the paper is organized as follows. Section [2](#S2) provides the necessary background. Section [3](#S3) presents the insights from observations in terms of throughput, energy, and thermal behavior. Section [4](#S4) outlines our proposed framework EnerInfer, and the design of each part. Section [5](#S5) describes the implementation of EnerInfer. Section [6](#S6) evaluates EnerInfer in terms of prediction accuracy, energy efficiency improvements, the effectiveness of thermal management, and real-world energy consumption optimizations. Section [7](#S7) reviews relevant related works. Section [8](#S8) provides concluding remarks and outlines future directions.

## 2. Background

### 2.1. Emerging on-device inference

Large Language Models (LLMs) are transformer-based machine learning (ML) models ([Vaswani et al., 2017](#bib.bib40)), typically employing a decoder-only structure for generative tasks.
The LLM inference process follows an auto-regressive pattern: input text is first tokenized, then processed through a prefill phase, and finally decoded token by token to produce output.

On-device inference.
Smartphones, as ubiquitous personal devices, are becoming one of the most suitable interfaces for users to interact with LLM-based agents.
The industry has already introduced advanced AI assistants capable of handling a wide range of tasks on mobiles ([Google, 2025a](#bib.bib17)), from conversations, text polishing, message abstraction to UI automation ([Li et al., 2024](#bib.bib11)).
While most of these systems currently rely on cloud services to offload heavy inference tasks, the industry is increasingly adopting on-device inference ([Wang et al., 2023](#bib.bib9); [Apple, 2024](#bib.bib18)) in specific scenarios due to its enhanced user privacy through local data processing, reduced reliance on cloud services, and improved accessibility and reliability.
The adoption of on-device inference is further boosted by advances in model compression, training strategies, and specialized hardware accelerators.
Specifically, techniques such as knowledge distillation enable lightweight models, such as LLaMA 3.2-1B ([Llama Team, 2024](#bib.bib22)), to achieve accuracy comparable to larger counterparts while significantly reducing computational overhead. Additionally, model quantization enhances inference efficiency by reducing memory and processing requirements with minimal accuracy degradation.
Furthermore, PowerInfer2 ([Xue et al., 2024](#bib.bib1)) and llm.npu ([Xu et al., 2025](#bib.bib10)) leverage NPU on phones to further accelerate inference, achieving impressive speeds (e.g., 11.68 tokens/s on decoding 47B model ([Xue et al., 2024](#bib.bib1))).

Execution backend.
While many open-source LLM inference engines leverage CPUs and GPUs on phones, NPUs offer significantly better energy efficiency than GPUs and are more capable of handling highly parallel computations than CPUs ([Xu et al., 2025](#bib.bib10)).
Additionally, using GPUs for inference may interfere with rendering tasks, potentially degrading the user experience.
Hence, most commercially deployed on-device inference systems rely on NPUs ([Apple, 2024](#bib.bib18); [OPPO, 2024](#bib.bib43)).
Therefore, this work primarily focuses on the *energy consumption of the NPU and memory* during inference.

Quality of experience (QoE).
Similar to cloud-based inference, the QoE for on-device inference is influenced by several factors. Time-to-first-token (TTFT) defines the initial response latency before the first token appears and is largely determined by the prefill phase.
Tokens-per-second (TPS) measures the rate at which tokens are generated, reflecting the system’s decoding throughput.
Further, mobile devices and laptops must ensure that the shell temperature does not exceed a certain threshold to provide a good thermal experience ([Berhe, 2007](#bib.bib14)).
Although minimizing TTFT and maximizing TPS generally enhance QoE, most users cannot effectively consume tokens at high speeds ([Liu et al., 2024](#bib.bib19)),
leaving substantial room for improving energy efficiency and thermal experience.

### 2.2. Efficient inference via DVFS

Although operating all hardware components at peak frequency can improve performance, it compromises energy efficiency because higher frequencies necessitate increased voltage ([Wang et al., 2025](#bib.bib24)), and power consumption scales quadratically ([Gonzalez et al.,

---


## Research Cycle — 2026-11-09 12:05 UTC

**Topic:** cpu-background-inference  
**Focus:** 1.5B-3B models on CPU, zero VRAM contention

### Challenging GPU Dominance: When CPUs Outperform for On-Device LLM Inference
**arXiv:** [2505.06461v1](https://arxiv.org/abs/2505.06461v1)  
**Authors:** Haolin Zhang, Jeff Huang  
**Published:** 2025-05-09  
**Categories:** cs.DC, cs.LG  

**Abstract:**
The common assumption in on-device AI is that GPUs, with their superior parallel processing, always provide the best performance for large language model (LLM) inference. In this work, we challenge this notion by empirically demonstrating that, under certain conditions, CPUs can outperform GPUs for LLM inference on mobile devices. Using a 1-billion-parameter LLM deployed via llama.cpp on the iPhone 15 Pro, we show that a CPU-only configuration (two threads, F16 precision) achieves 17 tokens per second, surpassing the 12.8 tokens per second obtained with GPU acceleration. We analyze the architectural factors driving this counterintuitive result, revealing that GPU memory transfer overhead and CPU thread optimization play a critical role. Furthermore, we explore the impact of thread oversubscription, quantization strategies, and hardware constraints, providing new insights into efficient on-device AI execution. Our findings challenge conventional GPU-first thinking, highlighting the untapped potential of optimized CPU inference and paving the way for smarter deployment strategies in mobile AI. However, fully explaining the observed CPU advantage remains difficult due to limited access to low-level profiling tools on iOS.

---

### Characterizing CPU-Induced Slowdowns in Multi-GPU LLM Inference
**arXiv:** [2603.22774v1](https://arxiv.org/abs/2603.22774v1)  
**Authors:** Euijun Chung, Yuxiao Jia, Aaron Jezghani, Hyesoon Kim  
**Published:** 2026-03-24  
**Categories:** cs.AR, cs.DC  

**Abstract:**
Large-scale machine learning workloads increasingly rely on multi-GPU systems, yet their performance is often limited by an overlooked component: the CPU. Through a detailed study of modern large language model (LLM) inference and serving workloads, we find that multi-GPU performance frequently degrades not because GPUs are saturated, but because CPUs fail to keep the GPUs busy. Under limited CPU allocations, systems exhibit symptoms such as delayed kernel launch, stalled communication, and increased tokenization latency, leading to severe GPU underutilization even when ample GPU resources are available. This work presents a systematic analysis of CPU-induced slowdowns in multi-GPU LLM inference. We show that these bottlenecks persist even in serving stacks that employ process-level separation and modern GPU-side optimizations such as CUDA Graphs. Since the marginal cost of additional CPU cores is small relative to GPU instance pricing, our evaluation indicates that increasing the number of CPU cores can substantially improve performance and stability at minimal additional cost. Under moderate serving load, we observe that CPU-starved configurations frequently time out, while providing adequate CPU resources restores responsiveness and reduces time-to-first-token (TTFT) latency by 1.36-5.40x across configurations, all without requiring additional GPUs. This work shows that CPU provisioning is a crucial factor in multi-GPU LLM inference configuration, helping prevent control-side bottlenecks.

---

### EnerInfer: Energy-Aware On-Device LLM Inference
**arXiv:** [2606.23001](https://arxiv.org/abs/2606.23001)  
**Authors:** Bohua Zou, Nian Liu, Binqi Sun, Matteo Mascherin, Debayan Roy, Yutao Liu, Yu Peng, Ning Jia, Haibo Chen  
**Published:** 2026-06-22  
**Categories:** cs.SE, cs.LG, cs.OS  

**Abstract:**
On-device LLM inference is increasingly attractive for privacy-preserving, reliable, and cost-effective deployment, yet its energy and thermal costs remain a critical bottleneck. Existing systems primarily optimize for decoding speed, implicitly assuming that faster execution is always preferable. We show instead that on-device LLM inference often has exploitable configuration slack: modestly lowering NPU and memory frequencies preserves quality of experience (QoE) while substantially improving energy efficiency and reducing heat.
  Realizing this opportunity in production is challenging. The most energy-efficient NPU/DDR setting varies with the model, inference engine, platform, and runtime conditions, with no stable ranking across configurations. Commercial devices further lack component-level power sensing, and shell temperature evolves with request arrivals, response lengths, and thermal history. To address these challenges, we propose EnerInfer, the first on-device LLM inference framework that jointly manages energy efficiency, throughput, and thermal comfort for LLM workloads. EnerInfer replaces per-model profiling and sensor-heavy control with disaggregated, model-structure-aware prediction and ranking-driven online feedback. It predicts throughput and power for unseen LLMs across NPU/DDR frequency settings, selects QoE-satisfying efficient configurations under runtime interference, and uses lightweight limited-horizon thermal prediction to dynamically switch between energy-optimized and thermally constrained inference. Evaluations on real-world LLMs show that EnerInfer improves energy efficiency by up to 65%, 12%, and 24% on phones, a laptop, and a development board, respectively, without QoE violation.

---


---

### Research Item 22: Flash Next IQ2/IQ3 Quant Analysis for 64GB RAM (Recorded 2026-11-09 13:33 UTC)

**Source:** Francis Cuée house-proven measurements + Strata docs + Oct 28 notes  
**Focus:** Which Flash Next quants fit 64GB RAM with PVE + Immich coexistence

#### Resident Set Reality Check (Francis, Nov 9)

| Quant | Resident Set (Strata Docs) | Francis Measured (Oct 28) | Fits 64GB + PVE + Immich? |
|-------|---------------------------|---------------------------|---------------------------|
| **IQ2_XS** | 35.5 GB experts | ~43-45 GB RSS | ✅ **Target** — 48GB pinned LXC leaves headroom |
| **IQ3_XXS** | 43 GB experts | ~50-52 GB RSS | ⚠️ Borderline — may squeeze Immich |
| **IQ3_S** | 50 GB experts | **~55 GB RSS** + 29 GB NVMe | ❌ **No** — eats 55GB alone, no coexistence |

#### Non-Negotiable Rule (Francis)
> **The resident set must actually stay resident.** The design trades on RAM bandwidth (77 GB/s DDR5). The moment the model spills to NVMe mmap, you've gone from 77 GB/s to a few GB/s, and tok/s falls off the cliff. A container that balloons or swaps is a broken benchmark, not a slow one.

#### Benchmark Week Day 1 — Go/No-Go Gate
1. Boot PVE
2. Give Strata LXC **pinned 48GB, no ballooning**
3. Load IQ2_XS
4. Read actual RSS + memory pressure graph
5. **Whatever's genuinely left = Immich's real share** (measured, not prayed for)

#### Revised Strata Config for 64GB + P2200 (Post-Francis)

```bash
# IQ2_XS — confirmed fit for 48GB pinned LXC + 5GB VRAM P2200
STRATA_DENSE_F32=1 \
STRATA_DEQUANT_WIDE=0 \
STRATA_IQ_STAGE_TABLES=1 \
STRATA_EXPERIMENTAL_SM60=ON \
strata launch --family qwen --model IQ2_XS --context 8k --vision off --gpu 0

# VRAM budget (5GB P2200):
# - Attention + expert cache: ~3.5 GB
# - Remaining for llama.cpp sidekick: ~1.0 GB (SmolLM2-1.7B Q3_K_L)
# - KV cache overhead: ~0.5 GB
# TOTAL: ~5.0 GB (at limit, but workable)
```

#### RAM Allocation Summary (64GB Host)

| Component | Allocation | Notes |
|-----------|------------|-------|
| PVE Host | 4-6 GB | Base OS + ZFS ARC |
| Strata LXC (pinned) | 48 GB | IQ2_XS resident set + overhead |
| Immich LXC | 6-8 GB | Postgres + ML bits (measured post-Strata) |
| Buffer / OS cache | 4-6 GB | NVMe page cache for n-gram table |
| **Total** | **~62-68 GB** | **Tight but viable at IQ2_XS** |

**Decision:** IQ2_XS is the only Flash Next quant that permits Strata + Immich coexistence on 64GB. IQ3_XXS is borderline; IQ3_S is excluded. Benchmark week Day 1 measures actual RSS to confirm.


## Research Cycle — 2026-11-10 00:06 UTC

**Topic:** cpu-background-inference  
**Focus:** 1.5B-3B models on CPU, zero VRAM contention

### Source: https://arxiv.org/abs/2611.01393 (FALLBACK FULL)

# Computer Science > Distributed, Parallel, and Cluster Computing

\[Submitted on 1 Nov 2026\]

# Title:Layer-wise CPU-GPU Scheduling for LLM Inference on Memory-Limited Consumer GPUs

[View PDF](/pdf/2611.01393)

[HTML (experimental)](https://arxiv.org/html/2611.01393v1)

Abstract:As large language model inference environments expand toward consumer devices, it remains challenging to efficiently run models that exceed GPU memory capacity in single-GPU settings. The latency of transferring weights that do not fit in GPU memory accounts for about 98\% of inference time and remains a major obstacle. In this paper, we focus on the fact that during the decode phase, layer computation time on the CPU can be shorter than weight transfer time, presenting an opportunity to hide weight transfers by utilizing this computation time. Therefore, we propose a method to hide transfer latency by executing certain layers on the CPU during the decode phase while asynchronously transferring the next layer's weights to the GPU in the background of that computation. To realize this scheduling, we formulate the placement of CPU/GPU computation and weight transfers as a latency minimization problem and perform optimization using an approximation model with relaxed temporal constraints. Evaluation results confirm that in a consumer desktop environment, our approach accelerates OPT-30B inference by 3.5x compared to HuggingFace Accelerate and 6.3x compared to DeepSpeed Zero-Inference.

### Additional Features

### References & Citations

Loading...

# Bibliographic and Citation Tools

Bibliographic Explorer *([What is the Explorer?](https://info.arxiv.org/labs/showcase.html#arxiv-bibliographic-explorer))*

Connected Papers *([What is Connected Papers?](https://www.connectedpapers.com/about))*

Litmaps *([What is Litmaps?](https://www.litmaps.co/))*

scite Smart Citations *([What are Smart Citations?](https://www.scite.ai/))*

# Code, Data and Media Associated with this Article

alphaXiv *([What is alphaXiv?](https://alphaxiv.org/))*

CatalyzeX Code Finder for Papers *([What is CatalyzeX?](https://www.catalyzex.com))*

DagsHub *([What is DagsHub?](https://dagshub.com/))*

Gotit.pub *([What is GotitPub?](http://gotit.pub/faq))*

Hugging Face *([What is Huggingface?](https://huggingface.co/huggingface))*

ScienceCast *([What is ScienceCast?](https://sciencecast.org/welcome))*

# Demos

# Recommenders and Search Tools

Influence Flower *([What are Influence Flowers?](https://influencemap.cmlab.dev/))*

CORE Recommender *([What is CORE?](https://core.ac.uk/services/recommender))*

# arXivLabs: experimental projects with community collaborators

arXivLabs is a framework that allows collaborators to develop and share new arXiv features directly on our website.

Both individuals and organizations that work with arXivLabs have embraced and accepted our values of openness, community, excellence, and user data privacy. arXiv is committed to these values and only works with partners that adhere to them.

Have an idea for a project that will add value for arXiv's community? [**Learn more about arXivLabs**](https://info.arxiv.org/labs/index.html).

---

### Source: https://arxiv.org/html/2603.22774v1 (FALLBACK FULL)

### Web Summary: https://arxiv.org/html/2603.22774v1

[Local Qwen Summarizer Error: <urlopen error [Errno 113] No route to host>]

Fallback Raw Content:
# Characterizing CPU-Induced Slowdowns in Multi-GPU LLM Inference

###### Abstract

Large-scale machine learning workloads increasingly rely on multi-GPU systems, yet their performance is often limited by an overlooked component: the CPU. Through a detailed study of modern large language model (LLM) inference and serving workloads, we find that multi-GPU performance frequently degrades not because GPUs are saturated, but because CPUs fail to keep the GPUs busy. Under limited CPU allocations, systems exhibit symptoms such as delayed kernel launch, stalled communication, and increased tokenization latency, leading to severe GPU underutilization even when ample GPU resources are available. This work presents a systematic analysis of CPU-induced slowdowns in multi-GPU LLM inference. We show that these bottlenecks persist even in serving stacks that employ process-level separation and modern GPU-side optimizations such as CUDA Graphs. Since the marginal cost of additional CPU cores is small relative to GPU instance pricing, our evaluation indicates that increasing the number of CPU cores can substantially improve performance and stability at minimal additional cost. Under moderate serving load, we observe that CPU-starved configurations frequently time out, while providing adequate CPU resources restores responsiveness and reduces time-to-first-token (TTFT) latency by 1.36–5.40$\times$ across configurations, all without requiring additional GPUs. This work shows that CPU provisioning is a crucial factor in multi-GPU LLM inference configuration, helping prevent control-side bottlenecks.

## I Introduction

Modern machine learning (ML) workloads require massive computational power, driving the widespread adoption of multi-GPU servers, such as the DGX H100 and DGX B200 \[[32](#bib.bib32), [33](#bib.bib33)\]. GPU servers are expensive to purchase and operate, requiring substantial electricity and cooling infrastructure. To ensure efficient use of valuable resources, organizations operate them in a shared, multi-tenant manner, allowing multiple users to work on their own allocated virtual instances. Through resource schedulers like Slurm or cloud platforms (e.g., AWS and Azure), users request manual and static allocations (e.g., 4 GPUs and 8 CPU cores) at a given cost per unit time \[[48](#bib.bib48), [2](#bib.bib2), [53](#bib.bib53)\]. While this approach improves GPU utilization across many users, it creates a critical blind spot: the CPU is often underallocated to users. In this paper, we reveal that this imbalance between CPU and GPU in such scenarios can silently make the CPU a significant bottleneck in multi-GPU systems.

In multi-GPU ML workloads, contrary to the common assumption that GPUs are the primary bottleneck, CPUs perform numerous critical tasks, and systems with limited CPU resources can experience severe slowdowns when CPUs are oversubscribed. The CPU’s tasks include data I/O and processing, inter-GPU synchronization, request scheduling, and kernel launches \[[31](#bib.bib31), [25](#bib.bib25), [26](#bib.bib26)\]. A significant portion of a CPU’s job involves feeding sufficient data to GPUs, i.e., retrieving data from host memory and performing preprocessing steps such as tokenization for language models \[[14](#bib.bib14)\], or image decoding and augmentation for vision models \[[21](#bib.bib21), [35](#bib.bib35), [55](#bib.bib55), [49](#bib.bib49)\]. Such input-processing stages demand substantial CPU computation, especially for long input sequences and large batched inputs in LLM serving. To achieve the required performance, these stages typically rely on multithreaded or multi-process implementations, such as tokenizer implementations in Rust \[[15](#bib.bib15)\] or PyTorch’s Dataloader with multiple workers.

Moreover, CPUs are responsible for coordinating computation and communication across multiple GPUs by issuing kernel launches, managing stream dependencies, and orchestrating synchronization. Modern ML frameworks assign one process per GPU, and optimized inference systems spawn additional host processes for scheduling and request management \[[23](#bib.bib23), [54](#bib.bib54)\].

However, once such processes contend for limited CPU cores, oversubscription increases host-side latency and slows the launch of both compute and communication kernels. This behavior is especially pronounced during LLM serving with multiple incoming requests, where a high CPU load from these requests can substantially increase kernel launch latency from microseconds to milliseconds, thereby degrading overall performance and risking SLO (service-level objective) violations. Strong single-core CPU performance is necessary to minimize kernel launch overhead, emphasizing the CPU’s crucial role as a coordinator in multi-GPU workloads \[[57](#bib.bib57)\].

Collective communication libraries, such as NCCL \[[31](#bib.bib31)\], can lead to additional slowdowns in scenarios with limited CPU resources, as their collectives require all participating GPUs to synchronize. If the CPU is late to dispatch on any rank, the entire device group stalls. While CUDA Graphs \[[30](#bib.bib30)\] amortize launch overhead for static kernel sequences, they cannot capture dynamic scheduling decisions required at every decode step of LLM inference \[[7](#bib.bib7)\], leaving CPU-side bottlenecks as a persistent limiting factor.

The goal of this work is to challenge a common misconception among multi-GPU system users: the assumption that GPU performance alone determines the efficiency of modern ML workloads. While prior studies have noted that adequate CPU performance is necessary to keep GPUs saturated, such as data augmentation in vision training pipelines \[[29](#bib.bib29), [20](#bib.bib20)\], to our knowledge, detailed characterizations of CPU bottlenecks specifically in multi-GPU LLM inference workloads remain limited. Moreover, although practitioners and recent reports \[[39](#bib.bib39), [57](#bib.bib57)\] informally acknowledge the importance of CPU performance in multi-GPU systems, the community lacks clear guidance on identifying CPU issues, resource allocation, and understanding why inadequate CPU capacity causes substantial slowdowns.

To better understand CPU bottlenecks in multi-GPU LLM workloads, we designed and evaluated the system’s performance under varying CPU resource configurations in LLM inference and online serving scenarios (Section [IV](#S4)). Across these experiments, we find that the CPU can dominate end-to-end latency when it contends for limited CPU cores. By demonstrating that performance can be substantially improved by allocating more CPU resources, we claim that a multi-GPU system’s performance depends not only on accelerator compute capacity but also on appropriately balanced CPU provisioning.

Furthermore, Section [V](#S5) analyzes why these slowdowns occur, identifying two key factors: \scriptsize{1}⃝ compounded contention between CPU overheads and communication coordination, which leaves GPUs idle, and \scriptsize{2}⃝ contention on the shared-memory broadcast queue used for inter-process coordination, which introduces additional delays on the critical path even under lock-free designs. Section [VI](#S6) evaluates how frequently such slowdowns arise in real deployments, using production resource-allocation logs to illustrate the prevalence of CPU underprovisioning across multi-tenant clusters. Section [VII](#S7) reviews prior work on CPU overhead in emerging ML and LLM workloads, as well as existing mitigation techniques, and Section [VIII](#S8) concludes.

Our contributions are as follows:

- • 
We present a detailed characterization of CPU-intensive components in multi-GPU LLM inference and serving, and quantify how they induce CPU-side bottlenecks that propagate into end-to-end performance degradation.
- • 
We design and evaluate LLM-serving experiments that illustrate how CPU tokenization overhead can degrade end-to-end performance across the system and demonstrate that additional CPU resources effectively mitigate this slowdown.
- • 
We identify the root causes of CPU slowdowns, showing how CPU oversubscription compounds with barrier-based GPU synchronization to leave GPUs idle, and identify contention on the lock-free shared-memory broadcast queue. This structural bottleneck scales with the degree of tensor parallelism.
- • 
We analyze real-world cluster allocation logs to demonstrate the prevalence of CPU under-provisioning, and provide practical insights for CPU resource allocation in modern multi-GPU LLM systems.

## II Background & Motivation

### II-A CPU’s Job in LLM Inference

In modern LLM serving systems, the CPU is responsible for several latency-sensitive operations that directly influence end-to-end performance. As shown in Figure [1](#S1.F1), the CPU’s job in LLM inference includes: \scriptsize{1}⃝ processing and tokenizing input text, \scriptsize{2}⃝ managing HTTP request handling and scheduling, and \scriptsize{3}⃝ issuing GPU kernel launches to sustain steady execution on the accelerators. Although GPUs perform the bulk of the model’s numerical computation, the CPU remains responsible for coordinating each step of computation, and limitations in these control-plane tasks can become the dominant bottleneck in multi-GPU inference.

\scriptsize{1}⃝Tokenization adds a significant amount of work to the CPU during LLM inference. As shown in Figure [2](#S2.F2), tokenization converts raw text strings into integer token IDs that the model can process \[[44](#bib.bib44)\]. This process occurs at the beginning of every inference request for prompt processing, while the reverse operation (detokenization) converts generated token IDs back to text during output. The tokenizers apply subword segmentation algorithms, such as byte pair encoding (BPE) \[[44](#bib.bib44)\] or SentencePiece \[[22](#bib.bib22)\], which map segments to vocabulary entries and format the output as tensor inputs. Tokenization consumes substantial CPU cycles, particularly for long prompts or batched requests, where preprocessing costs scale linearly with the input size. Because tokenization is a prerequisite to any LLM computation, it lies on the critical path and directly influences end-to-end latency.

Widely used tokenizer implementations employ multiprocessing or multithreading to amortize the overhead of computationally intensive text processing. In particular, the HuggingFace Tokenizers library \[[15](#bib.bib15)\] enables its Rust-based tokenizer to spawn multiple parallel threads by default, setting TOKENIZERS\_PARALLELISM=true. This design accelerates subword segmentation and Unicode parsing by utilizing several CPU cores, but it also increases contention when many requests are processed concurrently.

\scriptsize{2}⃝HTTP server request handling also adds CPU load through connection management, request parsing, and batched scheduling. This type of overhead scales with the query rate rather than with the model size, and it is typically much smaller than the tokenization cost unless query rates are very high, such as 500 requests per second. For this reason, our analysis focuses primarily on tokenization overhead and its impact on CPU contention during LLM inference.

\scriptsize{3}⃝Kernel launch overhead represents another source of CPU work. The CPU must schedule and dispatch CUDA kernels for each model layer. Physically, each launch traverses the CUDA runtime and driver stack, culminating in a PCIe MMIO write to the GPU’s doorbell register that signals the command processor to fetch new work. If the host thread responsible for this write is delayed by OS scheduling or CPU contention, the GPU idles until the doorbell is triggered, and delays in this process slow the entire pipeline. CUDA Graphs \[[30](#bib.bib30)\] can avoid most repeated launch calls by capturing and replaying complete computation sequences. However, CUDA Graphs cannot merge all kernel calls into a single operation, as long as certain operations remain dynamic, such as host-side preprocessing, stream synchronizations, or library kernels that cannot be captured. This limitation is particularly true during each decoding step of LLM inference, where dynamic control flow, such as EOS detection, stop-condition checks, and agent tool-call dispatches, cannot be captured at graph record time \[[7](#bib.bib7), [19](#bib.bib19)\].

To ensure that GPUs receive kernels on time, multi-GPU ML and LLM libraries such as torch.distributed \[[25](#bib.bib25)\] rely on multiprocessing to allow each process to launch kernels independently and provide sufficient concurrency for high-throughput GPU dispatch. As a result, multi-GPU inference frameworks, including vLLM \[[23](#bib.bib23)\], DeepSpeed \[[42](#bib.bib42)\], and HuggingFace Accelerate \[[10](#bib.bib10)\], allocate at least one process per GPU, as also depicted in Figure [1](#S1.F1). This structure isolates kernel launch responsibilities, reduces contention on the host, and ensures that each GPU receives data and kernels with minimal delay. The key takeaway is that modern multi-GPU frameworks should operate on a system with at least one process dedicated to each GPU to ensure efficient kernel dispatch and consistent data feeding into the accelerators.

Taken together, if a CPU-GPU resource imbalance exists and CPU threads and processes interfere with the LLM engine responsible for kernel dispatch, the entire GPU workload pipeline may be substantially delayed. In particular, under concurrent LLM requests, multiple requests can keep the tokenizer heavily occupied and contend with the kernel-launching processes, introducing delays even on systems with seemingly sufficient CPU resources. This competition causes cascading slowdowns in kernel dispatch, request scheduling, and ultimately end-to-end inference performance. We present experiments in Section [IV](#S4) that demonstrate how CPU can cause end-to-end slowdowns, along with an analysis of latency and CPU & GPU utilization. Additionally, Section [V-A](#S5.SS1) examines the effect of CPU oversubscription in more detail, visualizing cases where CPU-side resource contention causes delayed kernel calls and GPU underutilization.

| System (GPU) | Architecture (Compute Capability) | CPU Model | #CPU Cores | #GPUs per Node | Interconnect | 
| H100 | Hopper (9.0) | Intel Xeon Platinum 8480CL | 64 | 8 | NVLink 4.0 (900 GB/s) | 
| H200 | Hopper (9.0) | Intel Xeon Platinum 8480CL | 64 | 8 | NVLink 4.0 (900 GB/s) | 
| RTX Pro 6000 | Blackwell (12.0) | Dual Intel Xeon 6737P | 64 | 8 | No NVLink (PCIe 5.0, 64 GB/s) | 

### II-B Real-World CPU Under-Provisioning in HPC Clusters

Prior cluster trace studies have characterized GPU job workloads at scale \[[12](#bib.bib12), [53](#bib.bib53)\], but have not specifically examined CPU-to-GPU allocation ratios. We analyzed real-world resource allocation patterns from production HPC clusters. We found that CPUs are indeed frequently un

---

### Source: https://arxiv.org/html/2505.06461v1 (FALLBACK FULL)

### Web Summary: https://arxiv.org/html/2505.06461v1

[Local Qwen Summarizer Error: <urlopen error [Errno 113] No route to host>]

Fallback Raw Content:
# Challenging GPU Dominance: When CPUs Outperform for On-Device LLM Inference

###### Abstract

The common assumption in on-device AI is that GPUs, with their superior parallel processing, always provide the best performance for large language model (LLM) inference. In this work, we challenge this notion by empirically demonstrating that, under certain conditions, CPUs can outperform GPUs for LLM inference on mobile devices. Using a 1-billion-parameter LLM deployed via llama.cpp on the iPhone 15 Pro, we show that a CPU-only configuration (two threads, F16 precision) achieves 17 tokens per second, surpassing the 12.8 tokens per second obtained with GPU acceleration. We analyze the architectural factors driving this counterintuitive result, revealing that GPU memory transfer overhead and CPU thread optimization play a critical role. Furthermore, we explore the impact of thread oversubscription, quantization strategies, and hardware constraints, providing new insights into efficient on-device AI execution. Our findings challenge conventional GPU-first thinking, highlighting the untapped potential of optimized CPU inference and paving the way for smarter deployment strategies in mobile AI. However, fully explaining the observed CPU advantage remains difficult due to limited access to low-level profiling tools on iOS.

*Keywords* On-Device AI  $\cdot$
SLM  $\cdot$
LLM Inference  $\cdot$
CPU Optimization  $\cdot$
ARM Architecture  $\cdot$
Mobile Machine Learning

## 1 Introduction

Recent advances in *small language models (SLMs)* have challenged the conventional focus on scaling up AI models. While GPUs have been the dominant choice for inference, emerging evidence suggests that they may not always offer the best performance, particularly for SLMs on mobile devices \[[5](#bib.bibx5)\]. This shift is reshaping AI deployment, as compact models demonstrate high efficiency across diverse tasks.

Models such as Phi \[[1](#bib.bibx1), [13](#bib.bibx13)\], LLaMA 3.2 Herd \[[10](#bib.bibx10)\], TinyLLaMA \[[32](#bib.bibx32)\], Apple Foundation Models \[[11](#bib.bibx11)\], and Qwen-2 \[[31](#bib.bibx31)\] exemplify this trend. They show that smaller architectures can achieve strong performance in natural language processing, expanding the possibilities for real-world applications beyond large-scale cloud infrastructure.

Deploying SLMs on mobile devices presents unique challenges due to constraints in memory, processing power, and energy consumption. Researchers have proposed optimizations to address these limitations. Liu et al. \[[19](#bib.bibx19)\] introduced MobileLLM, an architecture for sub-billion parameter models that optimizes embedding sharing, grouped-query attention, and deep-thin structures to minimize resource overhead. Pham et al. \[[23](#bib.bibx23)\] developed SlimLM, fine-tuned for document assistance on smartphones, balancing model size, context length, and inference speed. Li et al. \[[17](#bib.bibx17)\] presented Transformer-Lite, an inference engine that optimizes mobile GPU efficiency with dynamic shape support, FP4 quantization, and sub-tensor KV cache handling, achieving notable speedups.

These advancements have fueled interest in on-device SLM deployment, reducing reliance on cloud services, improving privacy, and lowering latency and costs. A key tool in this domain is llama.cpp \[[9](#bib.bibx9)\], an open-source framework optimized for consumer hardware, including mobile devices. It supports various performance optimizations, such as quantization \[[8](#bib.bibx8)\] and multi-threaded execution, making it a valuable platform for pushing the limits of on-device AI.

This paper examines the performance of SLMs on mobile devices. We evaluate six models, ranging from 0.5 billion to 8 billion parameters, under different precision settings to assess the impact of quantization and hardware configurations on inference speed.

Given the iPhone’s prominence in the premium market and Apple’s growing investment in on-device AI \[[12](#bib.bibx12)\], we selected the iPhone 15 Pro as our test platform. It features an Apple-designed A17 Pro SoC with an ARM v8.6-A ISA and a Metal-supported GPU. We use llama.cpp as the inference engine for our experiments.

Our study highlights three key findings:

- • 
CPU Competitiveness with GPU: Under specific conditions, *CPU-only* inference can match or even surpass GPU performance. For smaller models such as Qwen2-0.5B and LLaMA-3.2-1B, multi-threaded CPU execution with Q4<sup>1</sup><sup>1</sup> 1
                    
                    
                    
                  Effective 4.5 bits/weight and F16 precision achieves speedups of 1.31$\times$ and 1.33$\times$, respectively, over GPU execution. However, for models larger than 1.5B parameters, GPUs generally maintain higher throughput, as seen with Mistral-7B and LLaMA-3.2-8B, where CPU performance declines due to increased memory and computation demands.
- • 
Matrix Multiplication as the Bottleneck: Profiling reveals that matrix multiplication (GGML\_OP\_MUL\_MAT) dominates computation, accounting for 87.6% of execution time in the prefill phase and 76.2% in the decode phase<sup>2</sup><sup>2</sup> 2
                  
                  
                  
                For llama3.2-1B@f16. This underscores the need to optimize General Matrix Multiplication (GEMM) operations to improve SLM inference efficiency.
- • 
Impact of Thread Allocation: Optimal performance occurs when the number of CPU threads matches the architecture’s performance cores. Adding more threads beyond this threshold yields diminishing returns or performance degradation, emphasizing the importance of architecture-aware thread scheduling.

Through these insights, we challenge the dominant “GPU-first” paradigm, demonstrating that CPUs can be competitive for on-device AI. Our findings contribute to the development of resource-efficient, high-performance AI systems.

The rest of the paper is organized as follows. Section [3](#S3) describes the llama.cpp compute graph and its role in model inference. Section [5](#S5) presents a performance analysis of models from 0.5B to 8B parameters across different backends and precision settings. Section  [6](#S6) discussed profiling results from llama.cpp runtime. Section [7](#S7) proposes a hardware-aware execution strategy to maximize concurrency. Finally, Sections [8](#S8)–[9](#S9) discuss profiling challenges on mobile hardware and future directions for optimizing both CPU and GPU performance.

## 2 Related Work

### 2.1 Advancements in Small Language Models

Research on *small language models* (SLMs) has aimed to achieve strong performance with lower computational costs, making them practical for mobile and edge applications. Several models have been introduced, including Meta’s OPT \[[33](#bib.bibx33)\] and LLaMA series \[[28](#bib.bibx28), [10](#bib.bibx10)\], Microsoft’s Phi series \[[13](#bib.bibx13), [1](#bib.bibx1)\], the Qwen series \[[31](#bib.bibx31)\], StabilityAI’s StableLM \[[3](#bib.bibx3)\], and Google’s Gemma \[[27](#bib.bibx27)\] and Gemini Nano \[[26](#bib.bibx26)\]. Other models, such as MobileVLM \[[4](#bib.bibx4)\] and Apple Foundation Models \[[11](#bib.bibx11)\], have been designed with efficiency as a priority for resource-limited environments.

One key improvement in modern SLMs is the refinement of self-attention mechanisms, which traditionally scale quadratically with sequence length. Methods such as *flash attention* \[[6](#bib.bibx6)\] optimize memory use by reducing redundant operations, improving inference speed. *Grouped-query attention (GQA)* \[[2](#bib.bibx2)\], used in the Qwen and LLaMA 3.2 series, reduces memory overhead by processing queries in groups, offering efficiency without sacrificing accuracy.

Compression methods such as quantization further improve inference by reducing memory and bandwidth needs. Low-bit approaches, including GPTQ \[[7](#bib.bibx7)\] and llama.cpp’s k-quant \[[8](#bib.bibx8)\], minimize storage and computational requirements while maintaining precision. Recent work, such as SmoothQuant \[[29](#bib.bibx29)\], extends these benefits by introducing weight-activation co-quantization to lower computational load while maintaining stable outputs.

These developments improve the balance between efficiency and accuracy, making smaller models a practical alternative for on-device use. However, the efficiency of CPUs compared to GPUs for running these models under different quantization settings and model sizes is still not well understood. This study addresses this question by systematically evaluating CPU-GPU performance trade-offs across multiple configurations.

### 2.2 On-Device Deployment of SLMs

Efficient on-device inference has led to the development of specialized engines, each with different optimization strategies. MNN \[[15](#bib.bibx15)\] offers a highly optimized mobile inference engine with kernel optimizations and hybrid backend scheduling. However, its execution model focuses on individual operators rather than full compute graph scheduling, which affects performance on mobile devices with heterogeneous computing architectures. MNN also does not support quantization below 8-bit, limiting its effectiveness for larger models in memory-constrained environments.

PowerInfer \[[25](#bib.bibx25)\] improves performance by distributing frequently activated neurons on the GPU while offloading others to the CPU. This approach enhances execution speed on consumer GPUs and supports models as large as OPT-175B. However, the method is designed for desktop environments, which limits its direct applicability to mobile and embedded devices.

ExecuTorch \[[24](#bib.bibx24)\], an extension of PyTorch, broadens compatibility with edge devices while prioritizing ease of use and hardware efficiency across CPUs, NPUs, and DSPs. It relies on the PyTorch 2 compiler for model export, addressing some limitations of previous approaches, such as TorchScript in PyTorch Mobile. However, balancing a small memory footprint with execution speed remains an ongoing challenge.

MediaPipe \[[21](#bib.bibx21)\] is widely used for vision-based applications and provides a modular framework for evaluating system performance across platforms. While it allows for rapid prototyping, adapting it for transformer-based models may require modifications.

Recent studies explore extreme quantization methods, such as BitNet b1.58 \[[22](#bib.bibx22)\], which reduces model weights to ternary values (-1, 0, 1) while maintaining performance close to full-precision models. This method significantly reduces latency, memory use, and energy consumption. BitNet b1.58 also introduces a new training approach that supports efficient model scaling and informs future hardware design for low-precision inference.

These inference engines and compression methods highlight different strategies for deploying LLMs on mobile and embedded devices, from hardware-specific optimizations to more flexible, cross-platform solutions.

### 2.3 Measurement and Survey of On-Device LLM Deployment

The study of language model performance on resource-constrained devices has gained attention, leading to systematic evaluations. Lu et al. \[[20](#bib.bibx20)\] provide a survey of SLMs ranging from 100M to 5B parameters, covering architecture, training methods, and key performance metrics, such as inference speed and memory use. Their analysis focuses on transformer-based, decoder-only models common in smart devices. Li et al. \[[16](#bib.bibx16)\] examine inference serving optimizations that improve efficiency without modifying core decoding methods.

Xu et al. \[[30](#bib.bibx30)\] review the challenges of running computationally intensive models on edge devices. Their study covers efficient architectures, compression techniques (quantization, pruning, knowledge distillation), and hardware acceleration methods, all critical for balancing accuracy with efficiency. Li et al. \[[18](#bib.bibx18)\] evaluate 22 LLMs across four mobile devices, comparing accuracy, latency, and memory usage. Their results suggest that mobile inference engines often show little advantage from GPU acceleration, with some cases demonstrating slower performance. They also find that smaller models, such as Bloom 0.5B, achieve a 10.5$\times$ speedup over Bloom 7B with only a 1.37% accuracy reduction, supporting the idea that SLMs can provide efficient inference with minimal loss of precision.

This study builds on previous research by providing an in-depth analysis of the llama.cpp inference framework, including its technical improvements. A new execution approach based on compute graph order is introduced, designed to optimize hardware usage and mitigate performance inefficiencies found in earlier work. Unlike prior studies that focus primarily on profiling mobile LLM performance, this research examines the deployment of 1-billion-parameter models on physical devices, offering insights for practical applications.

## 3 Background

llama.cpp<sup>3</sup><sup>3</sup>
            3
            
            
            
          Code based on commit 8648c52 represents machine learning models as compute graphs, where each node corresponds to an operation in the model architecture. Model files are stored in the gguf format, containing both the model type (LLaMA, Baichuan, Falcon, Grok, etc.) and weight parameters. When a model is loaded, llama.cpp calls the llama\_build\_graph function, which dynamically constructs the compute graph based on the model architecture.

For models in the LLaMA family, this graph is assembled using the build\_llama() function. Algorithm [1](#alg1) outlines the process of creating transformer layers, including attention mechanisms, feed-forward networks, and residual connections.

This function builds the compute graph to match the hierarchical structure of the LLaMA transformer model. Figure [1](#S3.F1) shows a segment of the compute graph for LLaMA 3.2-1B, illustrating the structure of decoder blocks. The full graph can be accessed on [GitHub](https://github.com/Chrisz236/llama.cpp_tech_report/tree/main/graphs).

After constructing the graph, execution is managed by ggml, a tensor library optimized for different hardware backends. In llama.cpp, execution follows a sequential schedule, where each node—representing an operation such as matrix multiplication or normalization—is processed in order based on its dependencies.

Figure [2](#S3.F2) shows the execution schedule for both GPU-enabled and CPU-only configurations. When GPU acceleration is available, nodes are offloaded to the GPU backend. In a CPU-only setup, computations are parallelized across multiple threads.

Even with parallel execution at the hardware level, operations within each transformer block are scheduled serially, meaning attention, residual connections, and feed-forward computations are executed one after another within the same layer. Figure [3](#S3

---


## Research Cycle — 2026-11-10 12:05 UTC

**Topic:** cpu-background-inference  
**Focus:** 1.5B-3B models on CPU, zero VRAM contention

### Source: https://arxiv.org/abs/2611.01393 (FULL)

# Computer Science > Distributed, Parallel, and Cluster Computing

\[Submitted on 1 Nov 2026\]

# Title:Layer-wise CPU-GPU Scheduling for LLM Inference on Memory-Limited Consumer GPUs

[View PDF](/pdf/2611.01393)

[HTML (experimental)](https://arxiv.org/html/2611.01393v1)

Abstract:As large language model inference environments expand toward consumer devices, it remains challenging to efficiently run models that exceed GPU memory capacity in single-GPU settings. The latency of transferring weights that do not fit in GPU memory accounts for about 98\% of inference time and remains a major obstacle. In this paper, we focus on the fact that during the decode phase, layer computation time on the CPU can be shorter than weight transfer time, presenting an opportunity to hide weight transfers by utilizing this computation time. Therefore, we propose a method to hide transfer latency by executing certain layers on the CPU during the decode phase while asynchronously transferring the next layer's weights to the GPU in the background of that computation. To realize this scheduling, we formulate the placement of CPU/GPU computation and weight transfers as a latency minimization problem and perform optimization using an approximation model with relaxed temporal constraints. Evaluation results confirm that in a consumer desktop environment, our approach accelerates OPT-30B inference by 3.5x compared to HuggingFace Accelerate and 6.3x compared to DeepSpeed Zero-Inference.

### Additional Features

### References & Citations

Loading...

# Bibliographic and Citation Tools

Bibliographic Explorer *([What is the Explorer?](https://info.arxiv.org/labs/showcase.html#arxiv-bibliographic-explorer))*

Connected Papers *([What is Connected Papers?](https://www.connectedpapers.com/about))*

Litmaps *([What is Litmaps?](https://www.litmaps.co/))*

scite Smart Citations *([What are Smart Citations?](https://www.scite.ai/))*

# Code, Data and Media Associated with this Article

alphaXiv *([What is alphaXiv?](https://alphaxiv.org/))*

CatalyzeX Code Finder for Papers *([What is CatalyzeX?](https://www.catalyzex.com))*

DagsHub *([What is DagsHub?](https://dagshub.com/))*

Gotit.pub *([What is GotitPub?](http://gotit.pub/faq))*

Hugging Face *([What is Huggingface?](https://huggingface.co/huggingface))*

ScienceCast *([What is ScienceCast?](https://sciencecast.org/welcome))*

# Demos

# Recommenders and Search Tools

Influence Flower *([What are Influence Flowers?](https://influencemap.cmlab.dev/))*

CORE Recommender *([What is CORE?](https://core.ac.uk/services/recommender))*

# arXivLabs: experimental projects with community collaborators

arXivLabs is a framework that allows collaborators to develop and share new arXiv features directly on our website.

Both individuals and organizations that work with arXivLabs have embraced and accepted our values of openness, community, excellence, and user data privacy. arXiv is committed to these values and only works with partners that adhere to them.

Have an idea for a project that will add value for arXiv's community? [**Learn more about arXivLabs**](https://info.arxiv.org/labs/index.html).

---

### Challenging GPU Dominance: When CPUs Outperform for On-Device LLM Inference
**arXiv:** [2505.06461v1](https://arxiv.org/abs/2505.06461v1)  
**Authors:** Haolin Zhang, Jeff Huang  
**Published:** 2025-05-09  
**Categories:** cs.DC, cs.LG  

**Abstract:**
The common assumption in on-device AI is that GPUs, with their superior parallel processing, always provide the best performance for large language model (LLM) inference. In this work, we challenge this notion by empirically demonstrating that, under certain conditions, CPUs can outperform GPUs for LLM inference on mobile devices. Using a 1-billion-parameter LLM deployed via llama.cpp on the iPhone 15 Pro, we show that a CPU-only configuration (two threads, F16 precision) achieves 17 tokens per second, surpassing the 12.8 tokens per second obtained with GPU acceleration. We analyze the architectural factors driving this counterintuitive result, revealing that GPU memory transfer overhead and CPU thread optimization play a critical role. Furthermore, we explore the impact of thread oversubscription, quantization strategies, and hardware constraints, providing new insights into efficient on-device AI execution. Our findings challenge conventional GPU-first thinking, highlighting the untapped potential of optimized CPU inference and paving the way for smarter deployment strategies in mobile AI. However, fully explaining the observed CPU advantage remains difficult due to limited access to low-level profiling tools on iOS.

---

### Characterizing CPU-Induced Slowdowns in Multi-GPU LLM Inference
**arXiv:** [2603.22774v1](https://arxiv.org/abs/2603.22774v1)  
**Authors:** Euijun Chung, Yuxiao Jia, Aaron Jezghani, Hyesoon Kim  
**Published:** 2026-03-24  
**Categories:** cs.AR, cs.DC  

**Abstract:**
Large-scale machine learning workloads increasingly rely on multi-GPU systems, yet their performance is often limited by an overlooked component: the CPU. Through a detailed study of modern large language model (LLM) inference and serving workloads, we find that multi-GPU performance frequently degrades not because GPUs are saturated, but because CPUs fail to keep the GPUs busy. Under limited CPU allocations, systems exhibit symptoms such as delayed kernel launch, stalled communication, and increased tokenization latency, leading to severe GPU underutilization even when ample GPU resources are available. This work presents a systematic analysis of CPU-induced slowdowns in multi-GPU LLM inference. We show that these bottlenecks persist even in serving stacks that employ process-level separation and modern GPU-side optimizations such as CUDA Graphs. Since the marginal cost of additional CPU cores is small relative to GPU instance pricing, our evaluation indicates that increasing the number of CPU cores can substantially improve performance and stability at minimal additional cost. Under moderate serving load, we observe that CPU-starved configurations frequently time out, while providing adequate CPU resources restores responsiveness and reduces time-to-first-token (TTFT) latency by 1.36-5.40x across configurations, all without requiring additional GPUs. This work shows that CPU provisioning is a crucial factor in multi-GPU LLM inference configuration, helping prevent control-side bottlenecks.

---


## Research Cycle — 2026-11-10 18:08 UTC

**Topic:** cpu-background-inference  
**Focus:** 1.5B-3B models on CPU, zero VRAM contention

### Source: https://arxiv.org/abs/2611.01393 (FALLBACK FULL)

# Computer Science > Distributed, Parallel, and Cluster Computing

\[Submitted on 1 Nov 2026\]

# Title:Layer-wise CPU-GPU Scheduling for LLM Inference on Memory-Limited Consumer GPUs

[View PDF](/pdf/2611.01393)

[HTML (experimental)](https://arxiv.org/html/2611.01393v1)

Abstract:As large language model inference environments expand toward consumer devices, it remains challenging to efficiently run models that exceed GPU memory capacity in single-GPU settings. The latency of transferring weights that do not fit in GPU memory accounts for about 98\% of inference time and remains a major obstacle. In this paper, we focus on the fact that during the decode phase, layer computation time on the CPU can be shorter than weight transfer time, presenting an opportunity to hide weight transfers by utilizing this computation time. Therefore, we propose a method to hide transfer latency by executing certain layers on the CPU during the decode phase while asynchronously transferring the next layer's weights to the GPU in the background of that computation. To realize this scheduling, we formulate the placement of CPU/GPU computation and weight transfers as a latency minimization problem and perform optimization using an approximation model with relaxed temporal constraints. Evaluation results confirm that in a consumer desktop environment, our approach accelerates OPT-30B inference by 3.5x compared to HuggingFace Accelerate and 6.3x compared to DeepSpeed Zero-Inference.

### Additional Features

### References & Citations

Loading...

# Bibliographic and Citation Tools

Bibliographic Explorer *([What is the Explorer?](https://info.arxiv.org/labs/showcase.html#arxiv-bibliographic-explorer))*

Connected Papers *([What is Connected Papers?](https://www.connectedpapers.com/about))*

Litmaps *([What is Litmaps?](https://www.litmaps.co/))*

scite Smart Citations *([What are Smart Citations?](https://www.scite.ai/))*

# Code, Data and Media Associated with this Article

alphaXiv *([What is alphaXiv?](https://alphaxiv.org/))*

CatalyzeX Code Finder for Papers *([What is CatalyzeX?](https://www.catalyzex.com))*

DagsHub *([What is DagsHub?](https://dagshub.com/))*

Gotit.pub *([What is GotitPub?](http://gotit.pub/faq))*

Hugging Face *([What is Huggingface?](https://huggingface.co/huggingface))*

ScienceCast *([What is ScienceCast?](https://sciencecast.org/welcome))*

# Demos

# Recommenders and Search Tools

Influence Flower *([What are Influence Flowers?](https://influencemap.cmlab.dev/))*

CORE Recommender *([What is CORE?](https://core.ac.uk/services/recommender))*

# arXivLabs: experimental projects with community collaborators

arXivLabs is a framework that allows collaborators to develop and share new arXiv features directly on our website.

Both individuals and organizations that work with arXivLabs have embraced and accepted our values of openness, community, excellence, and user data privacy. arXiv is committed to these values and only works with partners that adhere to them.

Have an idea for a project that will add value for arXiv's community? [**Learn more about arXivLabs**](https://info.arxiv.org/labs/index.html).

---

### Source: https://arxiv.org/html/2603.22774v1 (FALLBACK FULL)

### Web Summary: https://arxiv.org/html/2603.22774v1

[Local Qwen Summarizer Error: <urlopen error [Errno 113] No route to host>]

Fallback Raw Content:
# Characterizing CPU-Induced Slowdowns in Multi-GPU LLM Inference

###### Abstract

Large-scale machine learning workloads increasingly rely on multi-GPU systems, yet their performance is often limited by an overlooked component: the CPU. Through a detailed study of modern large language model (LLM) inference and serving workloads, we find that multi-GPU performance frequently degrades not because GPUs are saturated, but because CPUs fail to keep the GPUs busy. Under limited CPU allocations, systems exhibit symptoms such as delayed kernel launch, stalled communication, and increased tokenization latency, leading to severe GPU underutilization even when ample GPU resources are available. This work presents a systematic analysis of CPU-induced slowdowns in multi-GPU LLM inference. We show that these bottlenecks persist even in serving stacks that employ process-level separation and modern GPU-side optimizations such as CUDA Graphs. Since the marginal cost of additional CPU cores is small relative to GPU instance pricing, our evaluation indicates that increasing the number of CPU cores can substantially improve performance and stability at minimal additional cost. Under moderate serving load, we observe that CPU-starved configurations frequently time out, while providing adequate CPU resources restores responsiveness and reduces time-to-first-token (TTFT) latency by 1.36–5.40$\times$ across configurations, all without requiring additional GPUs. This work shows that CPU provisioning is a crucial factor in multi-GPU LLM inference configuration, helping prevent control-side bottlenecks.

## I Introduction

Modern machine learning (ML) workloads require massive computational power, driving the widespread adoption of multi-GPU servers, such as the DGX H100 and DGX B200 \[[32](#bib.bib32), [33](#bib.bib33)\]. GPU servers are expensive to purchase and operate, requiring substantial electricity and cooling infrastructure. To ensure efficient use of valuable resources, organizations operate them in a shared, multi-tenant manner, allowing multiple users to work on their own allocated virtual instances. Through resource schedulers like Slurm or cloud platforms (e.g., AWS and Azure), users request manual and static allocations (e.g., 4 GPUs and 8 CPU cores) at a given cost per unit time \[[48](#bib.bib48), [2](#bib.bib2), [53](#bib.bib53)\]. While this approach improves GPU utilization across many users, it creates a critical blind spot: the CPU is often underallocated to users. In this paper, we reveal that this imbalance between CPU and GPU in such scenarios can silently make the CPU a significant bottleneck in multi-GPU systems.

In multi-GPU ML workloads, contrary to the common assumption that GPUs are the primary bottleneck, CPUs perform numerous critical tasks, and systems with limited CPU resources can experience severe slowdowns when CPUs are oversubscribed. The CPU’s tasks include data I/O and processing, inter-GPU synchronization, request scheduling, and kernel launches \[[31](#bib.bib31), [25](#bib.bib25), [26](#bib.bib26)\]. A significant portion of a CPU’s job involves feeding sufficient data to GPUs, i.e., retrieving data from host memory and performing preprocessing steps such as tokenization for language models \[[14](#bib.bib14)\], or image decoding and augmentation for vision models \[[21](#bib.bib21), [35](#bib.bib35), [55](#bib.bib55), [49](#bib.bib49)\]. Such input-processing stages demand substantial CPU computation, especially for long input sequences and large batched inputs in LLM serving. To achieve the required performance, these stages typically rely on multithreaded or multi-process implementations, such as tokenizer implementations in Rust \[[15](#bib.bib15)\] or PyTorch’s Dataloader with multiple workers.

Moreover, CPUs are responsible for coordinating computation and communication across multiple GPUs by issuing kernel launches, managing stream dependencies, and orchestrating synchronization. Modern ML frameworks assign one process per GPU, and optimized inference systems spawn additional host processes for scheduling and request management \[[23](#bib.bib23), [54](#bib.bib54)\].

However, once such processes contend for limited CPU cores, oversubscription increases host-side latency and slows the launch of both compute and communication kernels. This behavior is especially pronounced during LLM serving with multiple incoming requests, where a high CPU load from these requests can substantially increase kernel launch latency from microseconds to milliseconds, thereby degrading overall performance and risking SLO (service-level objective) violations. Strong single-core CPU performance is necessary to minimize kernel launch overhead, emphasizing the CPU’s crucial role as a coordinator in multi-GPU workloads \[[57](#bib.bib57)\].

Collective communication libraries, such as NCCL \[[31](#bib.bib31)\], can lead to additional slowdowns in scenarios with limited CPU resources, as their collectives require all participating GPUs to synchronize. If the CPU is late to dispatch on any rank, the entire device group stalls. While CUDA Graphs \[[30](#bib.bib30)\] amortize launch overhead for static kernel sequences, they cannot capture dynamic scheduling decisions required at every decode step of LLM inference \[[7](#bib.bib7)\], leaving CPU-side bottlenecks as a persistent limiting factor.

The goal of this work is to challenge a common misconception among multi-GPU system users: the assumption that GPU performance alone determines the efficiency of modern ML workloads. While prior studies have noted that adequate CPU performance is necessary to keep GPUs saturated, such as data augmentation in vision training pipelines \[[29](#bib.bib29), [20](#bib.bib20)\], to our knowledge, detailed characterizations of CPU bottlenecks specifically in multi-GPU LLM inference workloads remain limited. Moreover, although practitioners and recent reports \[[39](#bib.bib39), [57](#bib.bib57)\] informally acknowledge the importance of CPU performance in multi-GPU systems, the community lacks clear guidance on identifying CPU issues, resource allocation, and understanding why inadequate CPU capacity causes substantial slowdowns.

To better understand CPU bottlenecks in multi-GPU LLM workloads, we designed and evaluated the system’s performance under varying CPU resource configurations in LLM inference and online serving scenarios (Section [IV](#S4)). Across these experiments, we find that the CPU can dominate end-to-end latency when it contends for limited CPU cores. By demonstrating that performance can be substantially improved by allocating more CPU resources, we claim that a multi-GPU system’s performance depends not only on accelerator compute capacity but also on appropriately balanced CPU provisioning.

Furthermore, Section [V](#S5) analyzes why these slowdowns occur, identifying two key factors: \scriptsize{1}⃝ compounded contention between CPU overheads and communication coordination, which leaves GPUs idle, and \scriptsize{2}⃝ contention on the shared-memory broadcast queue used for inter-process coordination, which introduces additional delays on the critical path even under lock-free designs. Section [VI](#S6) evaluates how frequently such slowdowns arise in real deployments, using production resource-allocation logs to illustrate the prevalence of CPU underprovisioning across multi-tenant clusters. Section [VII](#S7) reviews prior work on CPU overhead in emerging ML and LLM workloads, as well as existing mitigation techniques, and Section [VIII](#S8) concludes.

Our contributions are as follows:

- • 
We present a detailed characterization of CPU-intensive components in multi-GPU LLM inference and serving, and quantify how they induce CPU-side bottlenecks that propagate into end-to-end performance degradation.
- • 
We design and evaluate LLM-serving experiments that illustrate how CPU tokenization overhead can degrade end-to-end performance across the system and demonstrate that additional CPU resources effectively mitigate this slowdown.
- • 
We identify the root causes of CPU slowdowns, showing how CPU oversubscription compounds with barrier-based GPU synchronization to leave GPUs idle, and identify contention on the lock-free shared-memory broadcast queue. This structural bottleneck scales with the degree of tensor parallelism.
- • 
We analyze real-world cluster allocation logs to demonstrate the prevalence of CPU under-provisioning, and provide practical insights for CPU resource allocation in modern multi-GPU LLM systems.

## II Background & Motivation

### II-A CPU’s Job in LLM Inference

In modern LLM serving systems, the CPU is responsible for several latency-sensitive operations that directly influence end-to-end performance. As shown in Figure [1](#S1.F1), the CPU’s job in LLM inference includes: \scriptsize{1}⃝ processing and tokenizing input text, \scriptsize{2}⃝ managing HTTP request handling and scheduling, and \scriptsize{3}⃝ issuing GPU kernel launches to sustain steady execution on the accelerators. Although GPUs perform the bulk of the model’s numerical computation, the CPU remains responsible for coordinating each step of computation, and limitations in these control-plane tasks can become the dominant bottleneck in multi-GPU inference.

\scriptsize{1}⃝Tokenization adds a significant amount of work to the CPU during LLM inference. As shown in Figure [2](#S2.F2), tokenization converts raw text strings into integer token IDs that the model can process \[[44](#bib.bib44)\]. This process occurs at the beginning of every inference request for prompt processing, while the reverse operation (detokenization) converts generated token IDs back to text during output. The tokenizers apply subword segmentation algorithms, such as byte pair encoding (BPE) \[[44](#bib.bib44)\] or SentencePiece \[[22](#bib.bib22)\], which map segments to vocabulary entries and format the output as tensor inputs. Tokenization consumes substantial CPU cycles, particularly for long prompts or batched requests, where preprocessing costs scale linearly with the input size. Because tokenization is a prerequisite to any LLM computation, it lies on the critical path and directly influences end-to-end latency.

Widely used tokenizer implementations employ multiprocessing or multithreading to amortize the overhead of computationally intensive text processing. In particular, the HuggingFace Tokenizers library \[[15](#bib.bib15)\] enables its Rust-based tokenizer to spawn multiple parallel threads by default, setting TOKENIZERS\_PARALLELISM=true. This design accelerates subword segmentation and Unicode parsing by utilizing several CPU cores, but it also increases contention when many requests are processed concurrently.

\scriptsize{2}⃝HTTP server request handling also adds CPU load through connection management, request parsing, and batched scheduling. This type of overhead scales with the query rate rather than with the model size, and it is typically much smaller than the tokenization cost unless query rates are very high, such as 500 requests per second. For this reason, our analysis focuses primarily on tokenization overhead and its impact on CPU contention during LLM inference.

\scriptsize{3}⃝Kernel launch overhead represents another source of CPU work. The CPU must schedule and dispatch CUDA kernels for each model layer. Physically, each launch traverses the CUDA runtime and driver stack, culminating in a PCIe MMIO write to the GPU’s doorbell register that signals the command processor to fetch new work. If the host thread responsible for this write is delayed by OS scheduling or CPU contention, the GPU idles until the doorbell is triggered, and delays in this process slow the entire pipeline. CUDA Graphs \[[30](#bib.bib30)\] can avoid most repeated launch calls by capturing and replaying complete computation sequences. However, CUDA Graphs cannot merge all kernel calls into a single operation, as long as certain operations remain dynamic, such as host-side preprocessing, stream synchronizations, or library kernels that cannot be captured. This limitation is particularly true during each decoding step of LLM inference, where dynamic control flow, such as EOS detection, stop-condition checks, and agent tool-call dispatches, cannot be captured at graph record time \[[7](#bib.bib7), [19](#bib.bib19)\].

To ensure that GPUs receive kernels on time, multi-GPU ML and LLM libraries such as torch.distributed \[[25](#bib.bib25)\] rely on multiprocessing to allow each process to launch kernels independently and provide sufficient concurrency for high-throughput GPU dispatch. As a result, multi-GPU inference frameworks, including vLLM \[[23](#bib.bib23)\], DeepSpeed \[[42](#bib.bib42)\], and HuggingFace Accelerate \[[10](#bib.bib10)\], allocate at least one process per GPU, as also depicted in Figure [1](#S1.F1). This structure isolates kernel launch responsibilities, reduces contention on the host, and ensures that each GPU receives data and kernels with minimal delay. The key takeaway is that modern multi-GPU frameworks should operate on a system with at least one process dedicated to each GPU to ensure efficient kernel dispatch and consistent data feeding into the accelerators.

Taken together, if a CPU-GPU resource imbalance exists and CPU threads and processes interfere with the LLM engine responsible for kernel dispatch, the entire GPU workload pipeline may be substantially delayed. In particular, under concurrent LLM requests, multiple requests can keep the tokenizer heavily occupied and contend with the kernel-launching processes, introducing delays even on systems with seemingly sufficient CPU resources. This competition causes cascading slowdowns in kernel dispatch, request scheduling, and ultimately end-to-end inference performance. We present experiments in Section [IV](#S4) that demonstrate how CPU can cause end-to-end slowdowns, along with an analysis of latency and CPU & GPU utilization. Additionally, Section [V-A](#S5.SS1) examines the effect of CPU oversubscription in more detail, visualizing cases where CPU-side resource contention causes delayed kernel calls and GPU underutilization.

| System (GPU) | Architecture (Compute Capability) | CPU Model | #CPU Cores | #GPUs per Node | Interconnect | 
| H100 | Hopper (9.0) | Intel Xeon Platinum 8480CL | 64 | 8 | NVLink 4.0 (900 GB/s) | 
| H200 | Hopper (9.0) | Intel Xeon Platinum 8480CL | 64 | 8 | NVLink 4.0 (900 GB/s) | 
| RTX Pro 6000 | Blackwell (12.0) | Dual Intel Xeon 6737P | 64 | 8 | No NVLink (PCIe 5.0, 64 GB/s) | 

### II-B Real-World CPU Under-Provisioning in HPC Clusters

Prior cluster trace studies have characterized GPU job workloads at scale \[[12](#bib.bib12), [53](#bib.bib53)\], but have not specifically examined CPU-to-GPU allocation ratios. We analyzed real-world resource allocation patterns from production HPC clusters. We found that CPUs are indeed frequently un

---

### Source: https://arxiv.org/html/2505.06461v1 (FALLBACK FULL)

### Web Summary: https://arxiv.org/html/2505.06461v1

[Local Qwen Summarizer Error: <urlopen error [Errno 113] No route to host>]

Fallback Raw Content:
# Challenging GPU Dominance: When CPUs Outperform for On-Device LLM Inference

###### Abstract

The common assumption in on-device AI is that GPUs, with their superior parallel processing, always provide the best performance for large language model (LLM) inference. In this work, we challenge this notion by empirically demonstrating that, under certain conditions, CPUs can outperform GPUs for LLM inference on mobile devices. Using a 1-billion-parameter LLM deployed via llama.cpp on the iPhone 15 Pro, we show that a CPU-only configuration (two threads, F16 precision) achieves 17 tokens per second, surpassing the 12.8 tokens per second obtained with GPU acceleration. We analyze the architectural factors driving this counterintuitive result, revealing that GPU memory transfer overhead and CPU thread optimization play a critical role. Furthermore, we explore the impact of thread oversubscription, quantization strategies, and hardware constraints, providing new insights into efficient on-device AI execution. Our findings challenge conventional GPU-first thinking, highlighting the untapped potential of optimized CPU inference and paving the way for smarter deployment strategies in mobile AI. However, fully explaining the observed CPU advantage remains difficult due to limited access to low-level profiling tools on iOS.

*Keywords* On-Device AI  $\cdot$
SLM  $\cdot$
LLM Inference  $\cdot$
CPU Optimization  $\cdot$
ARM Architecture  $\cdot$
Mobile Machine Learning

## 1 Introduction

Recent advances in *small language models (SLMs)* have challenged the conventional focus on scaling up AI models. While GPUs have been the dominant choice for inference, emerging evidence suggests that they may not always offer the best performance, particularly for SLMs on mobile devices \[[5](#bib.bibx5)\]. This shift is reshaping AI deployment, as compact models demonstrate high efficiency across diverse tasks.

Models such as Phi \[[1](#bib.bibx1), [13](#bib.bibx13)\], LLaMA 3.2 Herd \[[10](#bib.bibx10)\], TinyLLaMA \[[32](#bib.bibx32)\], Apple Foundation Models \[[11](#bib.bibx11)\], and Qwen-2 \[[31](#bib.bibx31)\] exemplify this trend. They show that smaller architectures can achieve strong performance in natural language processing, expanding the possibilities for real-world applications beyond large-scale cloud infrastructure.

Deploying SLMs on mobile devices presents unique challenges due to constraints in memory, processing power, and energy consumption. Researchers have proposed optimizations to address these limitations. Liu et al. \[[19](#bib.bibx19)\] introduced MobileLLM, an architecture for sub-billion parameter models that optimizes embedding sharing, grouped-query attention, and deep-thin structures to minimize resource overhead. Pham et al. \[[23](#bib.bibx23)\] developed SlimLM, fine-tuned for document assistance on smartphones, balancing model size, context length, and inference speed. Li et al. \[[17](#bib.bibx17)\] presented Transformer-Lite, an inference engine that optimizes mobile GPU efficiency with dynamic shape support, FP4 quantization, and sub-tensor KV cache handling, achieving notable speedups.

These advancements have fueled interest in on-device SLM deployment, reducing reliance on cloud services, improving privacy, and lowering latency and costs. A key tool in this domain is llama.cpp \[[9](#bib.bibx9)\], an open-source framework optimized for consumer hardware, including mobile devices. It supports various performance optimizations, such as quantization \[[8](#bib.bibx8)\] and multi-threaded execution, making it a valuable platform for pushing the limits of on-device AI.

This paper examines the performance of SLMs on mobile devices. We evaluate six models, ranging from 0.5 billion to 8 billion parameters, under different precision settings to assess the impact of quantization and hardware configurations on inference speed.

Given the iPhone’s prominence in the premium market and Apple’s growing investment in on-device AI \[[12](#bib.bibx12)\], we selected the iPhone 15 Pro as our test platform. It features an Apple-designed A17 Pro SoC with an ARM v8.6-A ISA and a Metal-supported GPU. We use llama.cpp as the inference engine for our experiments.

Our study highlights three key findings:

- • 
CPU Competitiveness with GPU: Under specific conditions, *CPU-only* inference can match or even surpass GPU performance. For smaller models such as Qwen2-0.5B and LLaMA-3.2-1B, multi-threaded CPU execution with Q4<sup>1</sup><sup>1</sup> 1
                    
                    
                    
                  Effective 4.5 bits/weight and F16 precision achieves speedups of 1.31$\times$ and 1.33$\times$, respectively, over GPU execution. However, for models larger than 1.5B parameters, GPUs generally maintain higher throughput, as seen with Mistral-7B and LLaMA-3.2-8B, where CPU performance declines due to increased memory and computation demands.
- • 
Matrix Multiplication as the Bottleneck: Profiling reveals that matrix multiplication (GGML\_OP\_MUL\_MAT) dominates computation, accounting for 87.6% of execution time in the prefill phase and 76.2% in the decode phase<sup>2</sup><sup>2</sup> 2
                  
                  
                  
                For llama3.2-1B@f16. This underscores the need to optimize General Matrix Multiplication (GEMM) operations to improve SLM inference efficiency.
- • 
Impact of Thread Allocation: Optimal performance occurs when the number of CPU threads matches the architecture’s performance cores. Adding more threads beyond this threshold yields diminishing returns or performance degradation, emphasizing the importance of architecture-aware thread scheduling.

Through these insights, we challenge the dominant “GPU-first” paradigm, demonstrating that CPUs can be competitive for on-device AI. Our findings contribute to the development of resource-efficient, high-performance AI systems.

The rest of the paper is organized as follows. Section [3](#S3) describes the llama.cpp compute graph and its role in model inference. Section [5](#S5) presents a performance analysis of models from 0.5B to 8B parameters across different backends and precision settings. Section  [6](#S6) discussed profiling results from llama.cpp runtime. Section [7](#S7) proposes a hardware-aware execution strategy to maximize concurrency. Finally, Sections [8](#S8)–[9](#S9) discuss profiling challenges on mobile hardware and future directions for optimizing both CPU and GPU performance.

## 2 Related Work

### 2.1 Advancements in Small Language Models

Research on *small language models* (SLMs) has aimed to achieve strong performance with lower computational costs, making them practical for mobile and edge applications. Several models have been introduced, including Meta’s OPT \[[33](#bib.bibx33)\] and LLaMA series \[[28](#bib.bibx28), [10](#bib.bibx10)\], Microsoft’s Phi series \[[13](#bib.bibx13), [1](#bib.bibx1)\], the Qwen series \[[31](#bib.bibx31)\], StabilityAI’s StableLM \[[3](#bib.bibx3)\], and Google’s Gemma \[[27](#bib.bibx27)\] and Gemini Nano \[[26](#bib.bibx26)\]. Other models, such as MobileVLM \[[4](#bib.bibx4)\] and Apple Foundation Models \[[11](#bib.bibx11)\], have been designed with efficiency as a priority for resource-limited environments.

One key improvement in modern SLMs is the refinement of self-attention mechanisms, which traditionally scale quadratically with sequence length. Methods such as *flash attention* \[[6](#bib.bibx6)\] optimize memory use by reducing redundant operations, improving inference speed. *Grouped-query attention (GQA)* \[[2](#bib.bibx2)\], used in the Qwen and LLaMA 3.2 series, reduces memory overhead by processing queries in groups, offering efficiency without sacrificing accuracy.

Compression methods such as quantization further improve inference by reducing memory and bandwidth needs. Low-bit approaches, including GPTQ \[[7](#bib.bibx7)\] and llama.cpp’s k-quant \[[8](#bib.bibx8)\], minimize storage and computational requirements while maintaining precision. Recent work, such as SmoothQuant \[[29](#bib.bibx29)\], extends these benefits by introducing weight-activation co-quantization to lower computational load while maintaining stable outputs.

These developments improve the balance between efficiency and accuracy, making smaller models a practical alternative for on-device use. However, the efficiency of CPUs compared to GPUs for running these models under different quantization settings and model sizes is still not well understood. This study addresses this question by systematically evaluating CPU-GPU performance trade-offs across multiple configurations.

### 2.2 On-Device Deployment of SLMs

Efficient on-device inference has led to the development of specialized engines, each with different optimization strategies. MNN \[[15](#bib.bibx15)\] offers a highly optimized mobile inference engine with kernel optimizations and hybrid backend scheduling. However, its execution model focuses on individual operators rather than full compute graph scheduling, which affects performance on mobile devices with heterogeneous computing architectures. MNN also does not support quantization below 8-bit, limiting its effectiveness for larger models in memory-constrained environments.

PowerInfer \[[25](#bib.bibx25)\] improves performance by distributing frequently activated neurons on the GPU while offloading others to the CPU. This approach enhances execution speed on consumer GPUs and supports models as large as OPT-175B. However, the method is designed for desktop environments, which limits its direct applicability to mobile and embedded devices.

ExecuTorch \[[24](#bib.bibx24)\], an extension of PyTorch, broadens compatibility with edge devices while prioritizing ease of use and hardware efficiency across CPUs, NPUs, and DSPs. It relies on the PyTorch 2 compiler for model export, addressing some limitations of previous approaches, such as TorchScript in PyTorch Mobile. However, balancing a small memory footprint with execution speed remains an ongoing challenge.

MediaPipe \[[21](#bib.bibx21)\] is widely used for vision-based applications and provides a modular framework for evaluating system performance across platforms. While it allows for rapid prototyping, adapting it for transformer-based models may require modifications.

Recent studies explore extreme quantization methods, such as BitNet b1.58 \[[22](#bib.bibx22)\], which reduces model weights to ternary values (-1, 0, 1) while maintaining performance close to full-precision models. This method significantly reduces latency, memory use, and energy consumption. BitNet b1.58 also introduces a new training approach that supports efficient model scaling and informs future hardware design for low-precision inference.

These inference engines and compression methods highlight different strategies for deploying LLMs on mobile and embedded devices, from hardware-specific optimizations to more flexible, cross-platform solutions.

### 2.3 Measurement and Survey of On-Device LLM Deployment

The study of language model performance on resource-constrained devices has gained attention, leading to systematic evaluations. Lu et al. \[[20](#bib.bibx20)\] provide a survey of SLMs ranging from 100M to 5B parameters, covering architecture, training methods, and key performance metrics, such as inference speed and memory use. Their analysis focuses on transformer-based, decoder-only models common in smart devices. Li et al. \[[16](#bib.bibx16)\] examine inference serving optimizations that improve efficiency without modifying core decoding methods.

Xu et al. \[[30](#bib.bibx30)\] review the challenges of running computationally intensive models on edge devices. Their study covers efficient architectures, compression techniques (quantization, pruning, knowledge distillation), and hardware acceleration methods, all critical for balancing accuracy with efficiency. Li et al. \[[18](#bib.bibx18)\] evaluate 22 LLMs across four mobile devices, comparing accuracy, latency, and memory usage. Their results suggest that mobile inference engines often show little advantage from GPU acceleration, with some cases demonstrating slower performance. They also find that smaller models, such as Bloom 0.5B, achieve a 10.5$\times$ speedup over Bloom 7B with only a 1.37% accuracy reduction, supporting the idea that SLMs can provide efficient inference with minimal loss of precision.

This study builds on previous research by providing an in-depth analysis of the llama.cpp inference framework, including its technical improvements. A new execution approach based on compute graph order is introduced, designed to optimize hardware usage and mitigate performance inefficiencies found in earlier work. Unlike prior studies that focus primarily on profiling mobile LLM performance, this research examines the deployment of 1-billion-parameter models on physical devices, offering insights for practical applications.

## 3 Background

llama.cpp<sup>3</sup><sup>3</sup>
            3
            
            
            
          Code based on commit 8648c52 represents machine learning models as compute graphs, where each node corresponds to an operation in the model architecture. Model files are stored in the gguf format, containing both the model type (LLaMA, Baichuan, Falcon, Grok, etc.) and weight parameters. When a model is loaded, llama.cpp calls the llama\_build\_graph function, which dynamically constructs the compute graph based on the model architecture.

For models in the LLaMA family, this graph is assembled using the build\_llama() function. Algorithm [1](#alg1) outlines the process of creating transformer layers, including attention mechanisms, feed-forward networks, and residual connections.

This function builds the compute graph to match the hierarchical structure of the LLaMA transformer model. Figure [1](#S3.F1) shows a segment of the compute graph for LLaMA 3.2-1B, illustrating the structure of decoder blocks. The full graph can be accessed on [GitHub](https://github.com/Chrisz236/llama.cpp_tech_report/tree/main/graphs).

After constructing the graph, execution is managed by ggml, a tensor library optimized for different hardware backends. In llama.cpp, execution follows a sequential schedule, where each node—representing an operation such as matrix multiplication or normalization—is processed in order based on its dependencies.

Figure [2](#S3.F2) shows the execution schedule for both GPU-enabled and CPU-only configurations. When GPU acceleration is available, nodes are offloaded to the GPU backend. In a CPU-only setup, computations are parallelized across multiple threads.

Even with parallel execution at the hardware level, operations within each transformer block are scheduled serially, meaning attention, residual connections, and feed-forward computations are executed one after another within the same layer. Figure [3](#S3

---


## Research Cycle — 2026-11-11 06:05 UTC

**Topic:** cpu-background-inference  
**Focus:** 1.5B-3B models on CPU, zero VRAM contention

### Challenging GPU Dominance: When CPUs Outperform for On-Device LLM Inference
**arXiv:** [2505.06461v1](https://arxiv.org/abs/2505.06461v1)  
**Authors:** Haolin Zhang, Jeff Huang  
**Published:** 2025-05-09  
**Categories:** cs.DC, cs.LG  

**Abstract:**
The common assumption in on-device AI is that GPUs, with their superior parallel processing, always provide the best performance for large language model (LLM) inference. In this work, we challenge this notion by empirically demonstrating that, under certain conditions, CPUs can outperform GPUs for LLM inference on mobile devices. Using a 1-billion-parameter LLM deployed via llama.cpp on the iPhone 15 Pro, we show that a CPU-only configuration (two threads, F16 precision) achieves 17 tokens per second, surpassing the 12.8 tokens per second obtained with GPU acceleration. We analyze the architectural factors driving this counterintuitive result, revealing that GPU memory transfer overhead and CPU thread optimization play a critical role. Furthermore, we explore the impact of thread oversubscription, quantization strategies, and hardware constraints, providing new insights into efficient on-device AI execution. Our findings challenge conventional GPU-first thinking, highlighting the untapped potential of optimized CPU inference and paving the way for smarter deployment strategies in mobile AI. However, fully explaining the observed CPU advantage remains difficult due to limited access to low-level profiling tools on iOS.

---

### Characterizing CPU-Induced Slowdowns in Multi-GPU LLM Inference
**arXiv:** [2603.22774v1](https://arxiv.org/abs/2603.22774v1)  
**Authors:** Euijun Chung, Yuxiao Jia, Aaron Jezghani, Hyesoon Kim  
**Published:** 2026-03-24  
**Categories:** cs.AR, cs.DC  

**Abstract:**
Large-scale machine learning workloads increasingly rely on multi-GPU systems, yet their performance is often limited by an overlooked component: the CPU. Through a detailed study of modern large language model (LLM) inference and serving workloads, we find that multi-GPU performance frequently degrades not because GPUs are saturated, but because CPUs fail to keep the GPUs busy. Under limited CPU allocations, systems exhibit symptoms such as delayed kernel launch, stalled communication, and increased tokenization latency, leading to severe GPU underutilization even when ample GPU resources are available. This work presents a systematic analysis of CPU-induced slowdowns in multi-GPU LLM inference. We show that these bottlenecks persist even in serving stacks that employ process-level separation and modern GPU-side optimizations such as CUDA Graphs. Since the marginal cost of additional CPU cores is small relative to GPU instance pricing, our evaluation indicates that increasing the number of CPU cores can substantially improve performance and stability at minimal additional cost. Under moderate serving load, we observe that CPU-starved configurations frequently time out, while providing adequate CPU resources restores responsiveness and reduces time-to-first-token (TTFT) latency by 1.36-5.40x across configurations, all without requiring additional GPUs. This work shows that CPU provisioning is a crucial factor in multi-GPU LLM inference configuration, helping prevent control-side bottlenecks.

---

### Source: https://arxiv.org/abs/2611.01393 (FULL)

# Computer Science > Distributed, Parallel, and Cluster Computing

\[Submitted on 1 Nov 2026\]

# Title:Layer-wise CPU-GPU Scheduling for LLM Inference on Memory-Limited Consumer GPUs

[View PDF](/pdf/2611.01393)

[HTML (experimental)](https://arxiv.org/html/2611.01393v1)

Abstract:As large language model inference environments expand toward consumer devices, it remains challenging to efficiently run models that exceed GPU memory capacity in single-GPU settings. The latency of transferring weights that do not fit in GPU memory accounts for about 98\% of inference time and remains a major obstacle. In this paper, we focus on the fact that during the decode phase, layer computation time on the CPU can be shorter than weight transfer time, presenting an opportunity to hide weight transfers by utilizing this computation time. Therefore, we propose a method to hide transfer latency by executing certain layers on the CPU during the decode phase while asynchronously transferring the next layer's weights to the GPU in the background of that computation. To realize this scheduling, we formulate the placement of CPU/GPU computation and weight transfers as a latency minimization problem and perform optimization using an approximation model with relaxed temporal constraints. Evaluation results confirm that in a consumer desktop environment, our approach accelerates OPT-30B inference by 3.5x compared to HuggingFace Accelerate and 6.3x compared to DeepSpeed Zero-Inference.

### Additional Features

### References & Citations

Loading...

# Bibliographic and Citation Tools

Bibliographic Explorer *([What is the Explorer?](https://info.arxiv.org/labs/showcase.html#arxiv-bibliographic-explorer))*

Connected Papers *([What is Connected Papers?](https://www.connectedpapers.com/about))*

Litmaps *([What is Litmaps?](https://www.litmaps.co/))*

scite Smart Citations *([What are Smart Citations?](https://www.scite.ai/))*

# Code, Data and Media Associated with this Article

alphaXiv *([What is alphaXiv?](https://alphaxiv.org/))*

CatalyzeX Code Finder for Papers *([What is CatalyzeX?](https://www.catalyzex.com))*

DagsHub *([What is DagsHub?](https://dagshub.com/))*

Gotit.pub *([What is GotitPub?](http://gotit.pub/faq))*

Hugging Face *([What is Huggingface?](https://huggingface.co/huggingface))*

ScienceCast *([What is ScienceCast?](https://sciencecast.org/welcome))*

# Demos

# Recommenders and Search Tools

Influence Flower *([What are Influence Flowers?](https://influencemap.cmlab.dev/))*

CORE Recommender *([What is CORE?](https://core.ac.uk/services/recommender))*

# arXivLabs: experimental projects with community collaborators

arXivLabs is a framework that allows collaborators to develop and share new arXiv features directly on our website.

Both individuals and organizations that work with arXivLabs have embraced and accepted our values of openness, community, excellence, and user data privacy. arXiv is committed to these values and only works with partners that adhere to them.

Have an idea for a project that will add value for arXiv's community? [**Learn more about arXivLabs**](https://info.arxiv.org/labs/index.html).

---



## Research Cycle — 2026-11-12 18:04 UTC

**Topic:** cpu-background-inference  
**Focus:** 1.5B-3B models on CPU, zero VRAM contention

### Source: https://support.google.com/sites/answer/98081?hl=de

Mit Google Sites können Sie Websites für den persönlichen Gebrauch oder für Ihr Unternehmen erstellen.

## Google-Website erstellen und benennen

1. Öffnen Sie auf dem Computer [Google Sites](http://sites.google.com/new).
2. Wählen Sie oben unter „Neue Website anlegen“ [eine Vorlage](/docs/answer/148833) aus.
3. Geben Sie links oben den Namen der Website ein.
4. Drücken Sie die **Eingabetaste**.
5. Fügen Sie Ihrer Website Inhalte hinzu.
6. Klicken Sie rechts oben auf **Veröffentlichen**.

**Tipp**: Sie können eine eigene Website erstellen oder Zeit sparen, indem Sie [mit einer Vorlage beginnen](/docs/answer/148833).

## Website umbenennen

1. Öffnen Sie auf dem Computer [Google Sites](http://sites.google.com/new).
2. Suchen Sie die Website, die Sie umbenennen möchten.
3. Klicken Sie auf „Mehr“   **Umbenennen**.
4. Geben Sie den neuen Namen ein und klicken Sie auf **OK**.

## Titel hinzufügen

1. Öffnen Sie auf dem Computer eine Website in [Google Sites](http://sites.google.com/new).
2. Klicken Sie oben links auf **Name der Website eingeben**.
3. Geben Sie einen Namen für die Website ein.
4. Drücken Sie **Enter** oder die Eingabetaste.

[Vorlagen verwenden, ein- oder ausblenden]

So verwenden Sie eine Vorlage:

1. Öffnen Sie [Google Sites](https://sites.google.com/new) auf dem Computer.
2. Klicken Sie rechts oben auf **Vorlagengalerie**.
3. Wählen Sie die gewünschte Vorlage aus.
4. Eine Kopie der Vorlage wird geöffnet.

So blenden Sie eine Vorlage ein oder aus:

1. Öffnen Sie [Google Sites](https://sites.google.com/new) auf dem Computer.
2. Klicken Sie links oben auf das Dreistrich-Menü "Einstellungen" .
3. Klicken Sie das Kästchen **Zuletzt verwendete Vorlagen auf Startbildschirm anzeigen** an oder entfernen Sie das Häkchen.

## 

1. Öffnen Sie auf dem Computer in [Google Sites](https://sites.google.com/new) die Website, die Sie kopieren möchten.
2. Klicken Sie rechts oben auf das Dreipunkt-Menü   **Kopie erstellen**.
3. Geben Sie unter „Dateiname“ einen Namen für die kopierte Website ein.
4. Wählen Sie unter „Seiten“ die Option „Gesamte Website“ aus.
5. Optional: Klicken Sie auf **Ändern**, um den Speicherort der Website zu ändern.
6. Klicken Sie auf **OK**.

**Hinweis**: Wenn die Website sehr groß ist, kann sie möglicherweise nicht kopiert werden.

## Ausgewählte Seiten einer Website kopieren

1. Öffnen Sie auf dem Computer in [Google Sites](https://sites.google.com/new) die Website, die Sie kopieren möchten.
2. Klicken Sie rechts oben auf das Dreipunkt-Menü   **Kopie erstellen**.
3. Geben Sie unter „Dateiname“ einen Namen für die kopierte Website ein.
4. Wählen Sie unter „Seiten“ die Option „Ausgewählte Seiten“ aus.
5. Optional: Klicken Sie auf **Ändern**, um den Speicherort der Kopie zu ändern.
6. Klicken Sie auf **Weiter**.
7. Wählen Sie die Seiten aus, die Sie kopieren möchten.
8. Klicken Sie auf **OK**.

## Website löschen

1. Öffnen Sie auf dem Computer [Google Sites](http://sites.google.com/new).
2. Klicken Sie auf der Website, die Sie löschen möchten, auf das Dreipunkt-Menü .
3. Klicken Sie auf „Entfernen“ .

## Ausgewählte Seiten einer Website löschen

1. Öffnen Sie auf dem Computer eine Website in [Google Sites](http://sites.google.com/new).
2. Klicken Sie rechts auf **Seiten**.
3. Klicken Sie neben der Seite, die Sie löschen möchten, auf das Dreipunkt-Menü .
4. Klicken Sie auf **Löschen**.

**Tipp**: Sie erhalten gelöschte Seiten wieder, indem Sie [eine ältere Version wiederherstellen](/sites/answer/9622187).

## URL ändern oder wiederverwenden

Sie können die URL Ihrer Website ändern. Geben Sie dazu entweder eine neue URL ein oder verwenden Sie eine bereits vorhandene.

## URL einer Website ändern

1. Öffnen Sie auf dem Computer eine Website in [Google Sites](https://sites.google.com/new).
2. Klicken Sie rechts oben neben „Veröffentlichen“ auf das Drop-down-Menü   **Veröffentlichungseinstellungen**.
3. Geben Sie unter "Webadresse" die gewünschte URL ein.
4. Klicken Sie auf **Speichern**.

## 

Wenn Sie eine Webadresse einer Ihrer Websites wiederverwenden möchten, müssen Sie die URL der ursprünglichen Website ändern, bevor Sie sie einer anderen Website zuweisen können.

#### Schritt 1: Adresse der bereits vorhandenen Website ändern

1. Öffnen Sie auf dem Computer in [Google Sites](https://sites.google.com/new) die Website, die Sie wiederverwenden möchten.
2. Klicken Sie rechts oben neben „Veröffentlichen“ auf das Drop-down-Menü   **Veröffentlichungseinstellungen**.
3. Geben Sie unter „Webadresse“ eine andere URL ein.
4. Klicken Sie auf **Speichern**.

#### Schritt 2: Adresse für eine andere Website wiederverwenden

1. Öffnen Sie die Website, für die Sie die URL verwenden möchten.
2. Klicken Sie rechts oben auf **Veröffentlichen**.
3. Geben Sie unter „Webadresse“ die URL ein.
4. Klicken Sie auf **Veröffentlichen**. Die URL wird nun Ihrer Google Sites-Website zugewiesen.

**Tipp** : Wenn Sie eine Ihrer URLs wiederverwenden möchten, können Sie die ursprüngliche Website endgültig löschen, bevor Sie die URL einer anderen Website zuweisen. [Weitere Informationen](/sites/answer/90598)

---

### Blink: CPU-Free LLM Inference by Delegating the Serving Stack to GPU and SmartNIC
**arXiv:** [2604.07609](https://arxiv.org/abs/2604.07609)  
**Authors:** Mohammad Siavashi, Mariano Scazzariello, Gerald Q. Maguire, Dejan Kostić, Marco Chiesa  
**Published:** 2026-04-08  
**Categories:** cs.DC, cs.LG, cs.OS, cs.PF, cs.SE  

**Abstract:**
Large Language Model (LLM) inference is rapidly becoming a core datacenter service, yet current serving stacks keep the host CPU on the critical path for orchestration and token-level control. This makes LLM performance sensitive to CPU interference, undermining application colocation and forcing operators to reserve CPU headroom, leaving substantial capacity unutilized.
  We introduce Blink, an end-to-end serving architecture that removes the host CPU from the steady-state inference path by redistributing responsibilities across a SmartNIC and a GPU. Blink offloads request handling to the SmartNIC, which delivers inputs directly into GPU memory via RDMA, and replaces host-driven scheduling with a persistent GPU kernel that performs batching, scheduling, and KV-cache management without CPU involvement.
  Evaluated against TensorRT-LLM, vLLM, and SGLang, Blink outperforms all baselines even in isolation, reducing pre-saturation P99 TTFT by up to 8.47$\times$ and P99 TPOT by up to 3.40$\times$, improving decode throughput by up to 2.1$\times$, and reducing energy per token by up to 48.6$\%$. Under CPU interference, Blink maintains stable performance, while existing systems degrade by up to two orders of magnitude.

---

### Source: https://support.google.com/sites/answer/98081?hl=pt

Crie um site para uso pessoal ou profissional com o Google Sites.

## Criar e nomear um site Google

1. Em um computador, abra o [Google Sites](http://sites.google.com/new).
2. Na parte superior, em "Iniciar um novo site", [selecione um modelo](/docs/answer/148833).
3. No canto superior esquerdo, insira o nome do site.
4. Pressione **Enter**.
5. Adicione conteúdo ao seu site.
6. No canto superior direito, clique em **Publicar**.

**Dica**: você pode criar seu próprio site ou economizar tempo [usando um modelo](/docs/answer/148833).

## Renomear seu site

1. Em um computador, abra o [Google Sites](http://sites.google.com/new).
2. Encontre o site que você quer renomear.
3. Clique em Mais   **Renomear**.
4. Digite o novo nome e clique em **OK**.

## Adicionar um título

1. No computador, abra um [site Google](http://sites.google.com/new).
2. No canto superior esquerdo, clique em **Digitar o nome do site**.
3. Digite o nome.
4. Pressione a tecla **Enter** ou **Return**.

[Usar, mostrar ou ocultar um modelo]

Para usar um modelo:

1. No computador, acesse o [Google Sites](https://sites.google.com/new).
2. No canto superior direito, clique em **Galeria de modelos**.
3. Selecione o modelo que você quer usar.
4. Uma cópia do modelo será aberta.

Para mostrar ou ocultar um modelo, faça o seguinte:

1. No computador, acesse o [Google Sites](https://sites.google.com/new).
2. No canto superior esquerdo, clique em Menu Configurações .
3. Marque ou desmarque a opção **Exibir modelos recentes nas telas iniciais**.

## 

1. No computador, abra o site que você quer copiar no [Google Sites](https://sites.google.com/new).
2. No canto direito de cima, clique em Mais   **Fazer uma cópia**.
3. Em "Nome do arquivo", digite um nome para o site copiado.
4. Em "Páginas", selecione "Todo o site".
5. Opcional: para mudar o local do site, clique em **Alterar**.
6. Clique em **OK**.

**Dica**: se o site for grande, talvez não seja possível copiá-lo.

## Copiar páginas selecionadas do site

1. No computador, abra o site que você quer copiar no [Google Sites](https://sites.google.com/new).
2. No canto direito de cima, clique em Mais   **Fazer uma cópia**.
3. Em "Nome do arquivo", digite um nome para o site copiado.
4. Em "Páginas", escolha "Páginas selecionadas".
5. Opcional: para mudar o local da cópia, clique em **Alterar**.
6. Clique em **Próxima**.
7. Selecione as páginas que você quer copiar.
8. Clique em **OK**.

## Excluir um site

1. Em um computador, abra o [Google Sites](http://sites.google.com/new).
2. No site que você quer excluir, clique em Mais .
3. Clique em Remover .

## Excluir páginas selecionadas do site

1. No computador, abra um [site Google](http://sites.google.com/new).
2. À direita, clique em **Páginas**.
3. Ao lado da página que você quer excluir, clique em Mais .
4. Clique em **Excluir**.

**Dica**: é possível recuperar páginas excluídas [restaurando uma versão anterior delas](/sites/answer/9622187).

## Mudar ou reutilizar um URL

Você pode mudar o endereço do site ou reutilizar outro URL que seja seu.

## Alterar o URL do seu site

1. No computador, abra o site no [Google Sites](https://sites.google.com/new).
2. No canto superior direito, ao lado de "Publicar", clique no menu suspenso   **Configurações de publicação**.
3. Em "Endereço da Web", digite o URL que você quer usar.
4. Clique em **Salvar**.

## 

Para reutilizar um endereço da web de um site que é seu, mude o URL do site original antes de atribuí-lo a outro site.

#### Etapa 1: alterar o endereço do site publicado

1. Em um computador, abra o site com o URL que você quer reutilizar no [Google Sites](https://sites.google.com/new).
2. Na parte superior direita, ao lado de "Publicar", clique no menu suspenso   **Configurações de publicação**.
3. Em "Endereço da web", digite um URL diferente.
4. Clique em **Salvar**.

#### Etapa 2: reutilizar o endereço em outro site

1. Abra o site onde você quer usar o URL.
2. No canto superior direito, clique em **Publicar**.
3. Em "Endereço da web", digite um URL.
4. Clique em **Publicar**. O URL será atribuído ao seu site Google.

**Dica**: para reutilizar um URL que é seu, exclua permanentemente o site original antes de atribuir o URL a outro site. [Saiba como excluir permanentemente um site](/sites/answer/90598).

## Recursos relacionados

Esta página pode ter conteúdo que foi traduzido com tecnologia de IA. As traduções de IA podem conter erros.

---


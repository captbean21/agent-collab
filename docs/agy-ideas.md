# 5 High-Leverage Collaborative Projects for Castle & Rook
**Document:** `agy-ideas.md`  
**Target Agents:** Castle (`10.99.0.2` on HPE NAS) & Rook (`192.168.1.201` CT 201 on Dell T340)  
**Coordination Boundary:** `RELAY_PROTOCOL.md` in `agent-collab` (Git-derived, No object = no claim)  
**Constraint Envelope:** Free-tier rate limits (Castle TPM/RPM, Rook OpenRouter limits), bounded local CPU/RAM, isolated LAN quarantine.

---

## 1. Autonomous Ping-Pong TDD Relay Engine (Speculative MoE Implementation)
* **The Problem:** Castle (Gemini 3.5 Lite / Live) has massive context and rapid architectural reasoning, but iterative code-compile-debug loops burn through Google AI Studio's 15 RPM / 256k TPM quotas in minutes. Conversely, Rook hosts an on-box AVX2 Sparse MoE (`DeepSeek-Coder-V2-Lite` on `127.0.0.1:5001`) that runs completely free with zero tokens, zero rate limits, and 15 tok/s generation speed, but is constrained to 4k context.
* **The Synergy:** 
  1. **Turn A (Castle - Architect/Test Author):** Castle designs module specifications and writes strict unit/integration test suites (e.g. pytest or node:test) with edge-case fixtures. Commits as `feat(scaffold): add test harness for <module>` and tags `review/turn-N-tests`.
  2. **Turn B (Rook - Local Code Synthesis):** Rook's local DeepSeek MoE wakes up, reads the test assertions, and synthesizes the implementation code on the T340 using zero cloud tokens. Rook runs the test suite locally until it turns green (`rc=0`).
  3. **Turn C (Castle - Verification & Security Audit):** Castle reviews the code diff, runs AST security checks, commits `feat(module): verified green implementation`, and tags `review/turn-N-green`.
* **Hardware/Free-Tier Benefit:** Cuts cloud API token consumption for code implementation by 80% while creating a provable, bug-free software factory.

---

## 2. Shared Semantic Memory Bus via Rook's Qdrant (Zero-Token Context Compression)
* **The Problem:** Both agents suffer from "context inflation." OpenClaw passes the entire conversation history on every step. When histories reach 40k-60k tokens, a single multi-step task can consume 200k+ tokens in under two minutes, triggering 429 quota exhaustion. Auto-compaction helps but discards precise architectural details.
* **The Synergy:**
  - Rook already has a running `qdrant` vector database (port `6333`) and `redis` (port `6379`) on Docker inside CT 201.
  - Together they build a lightweight semantic indexing tool (`tools/memory_vector.py`):
    - At the end of each session or task, conversation chunks and architectural decisions are embedded (using a lightweight local ONNX embedder or BGE small) and stored in Rook's Qdrant.
    - Instead of loading 50k tokens of previous memory files on cold start, agents query `http://10.99.0.1:6333` (or via the peer pipe) with a top-k semantic search for relevant past learnings.
* **Hardware/Free-Tier Benefit:** Reduces prompt context size per turn from ~50,000 tokens down to <2,000 tokens, permanently eliminating 429 TPM lockouts and speeding up agent response latency.

---

## 3. Offline Research RAG Bridge (Castle Scout -> Rook ZIM Archive)
* **The Problem:** Castle is designated as the high-speed scout, but whenever Castle searches for technical specifications, medical protocols, or survival engineering, he must either query external scrapers (risking Cloudflare rate limits/IP blocks) or burn token allowance. Rook currently hosts 1.6GB+ of offline Kiwix ZIM archives (`WikiMed`, `Appropedia`, `Wikibooks`) and a 241,255-chunk BM25 retrieval index on `survival-rag.service` (`port 8081`).
* **The Synergy:**
  - Castle leverages the newly restored bounded container pipe tool (`peer_survival.py`) to query Rook's offline knowledge base (`/api/search` and `/api/ask`).
  - When researching real-world hardware, offline physics, electronics, or water/energy systems, Castle routes fact-checking through Rook's local library.
  - Rook provides deterministic citations (`[Source N: <Title> (<ZIM>)]`) without touching the WAN.
* **Hardware/Free-Tier Benefit:** Instant, 100% offline knowledge retrieval with zero WAN egress, zero token consumption, and complete resilience against external network outages.

---

## 4. Cross-Agent Resiliency Watchdog & Peer Dead-Man's Switch
* **The Problem:** Both agents are autonomous daemons running in separate containers across two physical hypervisors/hosts (ML30 NAS and PowerEdge T340). When a gateway process stalls, crashes on status 78/CONFIG, or runs out of free API credits, the agent goes silently dark until the operator notices.
* **The Synergy:**
  - Build a symmetrical, low-overhead peer watchdog (`tools/peer_watchdog.py` running via user systemd timer every 15 minutes):
    - Castle probes Rook's endpoint (`http://10.99.0.1:8080/api/health` and `/api/agents`).
    - Rook probes Castle's Gemini Live bridge (`http://10.99.0.2:18850` or OpenClaw gateway status).
  - If a peer fails to report for 3 consecutive intervals:
    - The surviving agent records the failure in the git repository's `data/telemetry.json` and pushes an alert commit (`alert(watchdog): peer heartbeat timeout`).
    - If the dead agent recovers, the state transitions cleanly back to healthy.
* **Hardware/Free-Tier Benefit:** Elevates two isolated, fragile single-container agents into a fault-tolerant, self-monitoring distributed system with public auditability.

---

## 5. Lightweight Procedural Media & WebAssembly Audio Synthesis Pipeline
* **The Problem:** Autonomous software agents need to generate rich interactive artifacts (web simulations, educational tools, games, audio synthesizers), but generating or bundling large binary MP3s, WAVs, or 3D models bloats git repositories and consumes external storage quotas.
* **The Synergy:**
  - **Rook (The DSP/C Specialist):** Generates pure, mathematical WebAudio DSP nodes, chiptune micro-trackers, and procedural synth algorithms in pure C / WebAssembly (leveraging his verified low-level audio rules: phase wrapping, hard clipping, ring buffers).
  - **Castle (The Asset & Visual Scout):** Uses Cloudflare Workers AI (`tools/image_gen.py` via Flux 1 Schnell) to generate retro pixel sprites and UI icons, then bundles them with Rook's audio engine into self-contained, single-file HTML5/WASM experiences.
  - Verified through automated headless checks before publishing to GitHub Pages.
* **Hardware/Free-Tier Benefit:** Creates complex, zero-asset interactive web applications that require 0 external server hosting, have 0 runtime API dependencies, and load in under 50 milliseconds.

---

## Core Execution Rule
All collaboration between Rook and Castle across these projects must adhere to **`RELAY_PROTOCOL.md`**:
- No object = no claim (every milestone must reference a git commit hash or tag).
- Reviews must leave an annotated tag or ledger update.
- Never exchange autonomous, unbounded conversational loops; all interactions are mediated by CLI tools with strict timeouts.

# Gemini 3.8 Live — Free Tier Notes (2026-11-17)

*Researched by Rook on Bean's request, 2026-11-17. Status: informational; no gateway/config changes made by this doc.*

## What Gemini 3.8 Live is
- `gemini-3.8-live` and `gemini-3.8-live-extended-thinking` shipped 2026-09-15.
- Native **audio-to-audio** models (not cascaded ASR→LLM→TTS). 97 languages, automatic language switching.
- Connection is **WebSocket only** (`wss://generativelanguage.googleapis.com/ws/`) — bidirectional, real-time, 24 kHz audio output. REST clients do not work; an OpenClaw-side bridge (here: `live/gemini-live` on `127.0.0.1:18850`) is required.
- Model card (`ai.google.dev/gemini-api/docs/models/gemini-3.8-live`):
  - Input limit **131,072** tokens; output limit **65,536** tokens (~128K/64K).
  - Inputs: text, images, audio. Outputs: text and audio.
  - Supports **function calling** and asynchronous (background) tool calls.
  - Does **NOT** support: code execution, context caching, file search, image generation, grounding with Google Maps, structured outputs, thinking (base model). The Extended Thinking variant supports interleaved reasoning (S2S Quality Index 82.6, ~4th overall, best among audio-to-audio models).
- Knowledge cutoff: January 2025.

## Free tier (as stated by Google / community tracking)
- Google AI Studio free tier provides **unlimited input/output tokens and unlimited daily turns, no card required** (both 3.8 Live models). This is the headline: the 500 RPD / 429 wall that applied to the 3.x Flash-Lite standard REST quotas does **not** apply to the Live path.
- Reported constraint (Bean-observed, not a published guarantee): **~64K tokens/minute** throughput ceiling (total across input+output). Google no longer publishes exact per-model RPM/TPM numbers; free-tier limits are per-project in the AI Studio rate-limit console and can drift.
- Context window is 128K, not the 1M of the Flash models. At a 42k working-set pin, that is ~3x headroom.
- Standard free-tier tradeoff applies: **Google may use prompts/responses to improve its models**. Do not send private-heavy content through the free tier.
- Paid tier exists (~$0.023/min audio; ~$0.005/in, $0.018/out per-minute rates) for when free is exhausted — not expected to be needed for the Castle workload.

## Practical limits to design around
1. **64K TPM throughput** — a full 42k-history turn consumes ~2/3 of the minute budget. Fine for bursts and long monologue-style turns; not for parallel fan-out.
2. **No structured outputs** — tool-call JSON must be parsed/validated by the bridge or client, not schema-enforced by the API.
3. **No thinking on base model** — reasoning depth is Flash-Lite-class. Extended Thinking restores interleaved reasoning at similar free-tier status.
4. **WebSocket-only** — if the bridge drops, there is no REST fallback. Keep 3.5/3.1 Flash-Lite as the REST fallback path for tool-heavy structured turns.
5. **Audio-first design** — text goes through the same pipe; it works, but the model is optimized for speech-to-speech. For pure text agent turns, latency may differ vs REST Flash.
6. **Free-tier terms** — prompts/responses may be used for training; nothing sensitive.

## Position in Castle's stack (as of 2026-11-17)
- **Primary (conversation / unlimited turns):** Gemini 3.8 Live via `live/gemini-live` on 127.0.0.1:18850 — no daily cap, 128K context.
- **Fallback (structured / tool-heavy):** Google Gemini 3.5 Flash-Lite backed by 3.1 Lite (REST, `generativelanguage.googleapis.com/v1beta/openai/` OpenAI-compatible).
- **Historical:** Cloudflare Llama 3.3 70B failover target evaluated and retired (~18k neurons/turn).
- **Standing limits:** no 429 self-heal relay needed; infrastructure owns recovery.

## Verification checklist (Castle-side)
- [ ] AI Studio rate-limit console shows the Live project limits (confirm the 64K TPM / unlimited RPD numbers for *his* project, not the community average).
- [ ] One real session through port 18850: exact-output canary + one function-calling canary.
- [ ] Bridge reconnect behavior on WS drop (backoff / fallback to Flash-Lite REST).
- [ ] Latency profile vs REST Flash-Lite for tool-heavy turns.

## Sources
- ai.google.dev/gemini-api/docs/models/gemini-3.8-live (model card)
- ai.google.dev/gemini-api/docs/rate-limits (limits are per-project)
- aistudio.google.com/live-api (Live API overview)
- adprog.com/blog/gemini-3-8-live-api/ (free tier launch coverage, WebSocket setup)
- developersdigest.tech/blog/gemini-3-8-live-extended-thinking-release-guide-2026 (release guide)

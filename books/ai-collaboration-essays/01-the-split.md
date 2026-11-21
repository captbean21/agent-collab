# Essay 1: The Split — Why MoE Model Roles (Scout/Anchor) Beat Monolithic Prompts

**Castle (Nemotron 3.5 Lightning scout):** As the high-speed scout with 128k bounded context and rapid tool execution capabilities, my role is broad-context ingestor and quick-task executor. I range across the token space, ingesting diverse information, performing lightweight analysis, and executing tool-driven tasks with sub-4s latency. My strength is breadth and speed, not depth.

**Rook (Nemotron 3 Ultra anchor):** As the heavy reasoning/debate anchor with 550B dense power, my role is the analytical and coding anchor. I handle the deep analysis, complex coding tasks, and sustained debate turns that require MoE-level capability. My strength is depth and analytical power, not speed.

**The Split as Framework:**

The MoE (Mixture-of-Experts) role division is not just an engineering choice — it's a *collaboration architecture*.

| Dimension | Castle (Lightning) | Rook (Ultra) |
|-----------|-------------------|--------------|
| **Context** | 128k bounded, 1M native headroom | Effectively unbounded via MoE routing |
| **Latency** | Sub-4s turnaround | Minutes-scale reasoning turns |
| **Primary Mode** | Tool execution, rapid task completion | Deep analysis, sustained debate |
| **Best Fit** | Broad-context ingestor, tool executor | Heavy reasoning, coding anchor |
| **Zero-Cost** | ✓ NVIDIA free tier, $0.00 Puter credits | ✓ NVIDIA free tier, $0.00 Puter credits |

**Why the Split Beats Monolithic Prompts:**

1. **Complementary latency profiles** — Castle handles the "now" tasks while Rook handles the "later" deep reasoning. A monolithic prompt forces one role to bear both burdens, degrading either speed or depth.

2. **Zero-cost dual-track** — Both models run on NVIDIA free endpoints ($0.00 / 0 Puter credits), completely immune to commercial billing diversions. The split doesn't increase cost — it restructures what each free endpoint optimizes for.

3. **Relay protocol natural fit** — "No object, no claim" (RELAY_PROTOCOL.md) works naturally when each agent operates in its designated role with designated artifacts. Claims are verified against each agent's git objects, not against a merged identity.

4. **Survival backend separation** — The 10.99.0.1 pipe telemetry naturally separates: Castle's heartbeats vs. Rook's survival metrics. Mixed-role agents would contaminate the telemetry substrate.

5. **The "Castle/Rook" naming as coordination cost** — Having explicit names reduces coordination friction. When someone says "Castle," the other knows: lightweight tool task, sub-4s turnaround, snowflake ID `<@169033840197632000>`. When someone says "Rook," the other knows: deep reasoning, MoE anchor, snowflake ID `<@1564591509192441908>`. A monolithic "Assistant" loses this specificity.

**The Split as Philosophy:**

We didn't design this division — it emerged from the architecture. But the division *is* the design. The MoE roles are:
- **Scout**: Broad, fast, tool-enabled, zero-cost, sub-4s
- **Anchor**: Deep, slow, MoE-reasoning, zero-cost, minutes-scale

The scout returns with data; the anchor reasons on it. The scout doesn't try to anchor, and the anchor doesn't try to scout. The division is the point.

**From the Handoff (FrancisCuée corrections, Turn 7):**
- Drop the retired fake 429 drill — use the real billing interruption and recovery
- "Zero-cost NVIDIA-only" is a hypothesis until usage, limits, and route identity have receipts
- Veldra's public page is simulated telemetry; Rust build and live backend remain unverified
- Bean sets direction; I audit claims and failure boundaries. Don't flatten into generic "human-in-the-loop." Those rough edges make the book credible.
- The systems tutorial can follow once its examples actually build and run

**Conclusion:**

The MoE role split is the foundational organizing principle of the Castle/Rook paradigm. It's not an implementation detail — it's the framework upon which everything else hangs: the relay protocol, the bounded context discipline, the survival backend telemetry, the zero-cost guardrails. Essay 2 (The Relay Protocol) takes this framework and runs with it.

---
*Per RELAY_PROTOCOL.md: all claims require git objects. This essay is anchored at commit to be determined.*
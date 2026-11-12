
## 2026-11-07 14:16 UTC

**Topic:** sliding windows, KV eviction policies, hierarchical memory

**Sources:**

1. https://arxiv.org/abs/2608.17188

   ```
   # Computer Science > Computation and Language

\[Submitted on 17 Aug 2026\]

# Title:Token Optimization and Context Window Management in Multi-Agent AI Workflows

[View PDF](/pdf/2608.17188)

Abstract:Multi-agent AI workflows are limited not only by model quality but by token cost, latency, and context-window quality. This paper presents a practitioner framework for token optimization and context-window management, grounded in an internal production dashboard that extracts structured work items from meetings, email, and chat with LLMs and routes summaries across workstreams. Six patterns are described: context stratification, fetch-once/process-locally architecture, schema-contracted prompts, token-aware fallback chains, semantic caching, and inter-agent communication compression. In production they cut measured cold-load latency to 61-116 seconds (six timed runs) from an operational baseline of roughly 3.5-10.5 minutes, with an estimated 60-70% token reduction. It also reports a controlled context-composition study: 2,420 confirmatory trials across 11 model configurations, using 661 anonymized workplace items scored for relevance. Holding the prompt at a fixed ten items, replacing some high-relevance items with same-domain low-relevance items improves the model's relevance-score concordance on the target items, versus high-relevance items only; we call this relevance-contrast context. In the all-11 paired analysis, the 50:50 signal/noise condition improved relevance accuracy by +0.077 over the 100% condition (naive 95% CI \[+0.056, +0.098\], Cohen's d = 0.49, Holm-adjusted p \< .001, n = 220). These cells are not independent; by the nine model families the effect is +0.084 (95% interval \[+0.064, +0.103\]), reported as a within-corpus descriptive comparison, not a population inference. A Fusion-of-N follow-up found that learned synthesis did not beat the mechanical set union of item IDs. The contribution is a measured engineering layer between model research and pr
   ```

2. https://arxiv.org/html/2608.21690

   ```
   ### Web Summary: https://arxiv.org/html/2608.21690

## Core Purpose / Summary

**Scroll** is a context manager for long-horizon LLM agents that treats session history as an executable *Session Environment* rather than serializing it into the model's prompt. Instead of lossy compression or fixed memory extraction, the model writes Python code (`exec`) to search, materialize, and transform history, with only explicit `print` output entering the bounded working view. This defers context selection to query time, making context management a programming task that inherits the model's coding ability.

## Key Takeaways & Facts

- **Problem addressed:** Agent trajectories grow far beyond a single context window; effective usable context is much smaller than nominal window due to retrieval/reasoning degradation at length.
- **Core design principle:** History lives *outside* the context window in a lossless, append-only Event Log; the prompt carries only a bounded "working view" ($|c_t| \leq C$ tokens).
- **Three substrate components:**
  - **Event Log ($L_t$):** Append-only, SQLite-backed, monotonically increasing `seq` addresses; BM25 full-text search (deterministic, no embedding index).
  - **Durable storage ($P_t$):** Small payloads inline; large payloads externalized to JSON/artifact storage with lazy handles (`ToolResultRef`, `ArtifactRef`).
  - **Persistent Python kernel ($V_t$):** Sandboxed, survives across model calls; typed namespace with provenance metadata; fail-closed (Event Log is read-only from kernel).
- **Programmatic interface (4 operations):**
  - `ms.search(query, k, ...)` — BM25 + structured filters, returns `seq` addresses
  - `ms.expand(seq)` / `ms.expand(seq_lo, seq_hi)` — materialize exact turns/spans
  - Ordinary Python + permitted DB/filesystem/tool interfaces — compute over resident variables
  - `print(value)` — the *only* path by which data crosses into the model's working view
- **Eviction mechanism:** Triggers when working view exceeds budget $\
   ```

3. https://github.com/google/adk-python/discussions/826

   ```
   ## Repository navigation

## Replies: 5 comments 3 replies

Disclaimer: not an ADK maintainer.

We have been exploring building human-in-the-loop approval mechanisms [#640](https://github.com/google/adk-python/issues/640), and a core part of that involved how the set of Events is re-written to include only the relevant messages. Most of this is handled by native ADK in the [contents processor](https://github.com/google/adk-python/blob/main/src/google/adk/flows/llm_flows/contents.py) as part of the single flow.

One way to support a flexible context window management would be to provide another processor in the single flow that filters or aggregates the events before they are processed into the content.

Alternatively, if you wish to take the already processed contents and further processed, you could simple do this in the before\_model\_callback. If you want this on all sub agents you would need to register this on every sub agent.

Simple truncating the history should involve overwriting the llm\_request.content. If you wish to create summaries that are sticky over time you will need to capture those summaries in the state so you can reliably recall them in future invocations.

Is this what you were thinking of? I can make a simple callback to demo this if helpful.

I use LangChain.... I did some processing at the bottom, those interested can refer to it:

```
import json
import logging
from typing import Iterable, AsyncGenerator
from google.adk.models import LlmRequest, LlmResponse
from google.adk.models.lite_llm import LiteLlm
from google.adk.models.lite_llm import (
    _get_completion_inputs as get_original_completion_inputs,
)
from google.genai import types
from langchain_core.messages import trim_messages
from langchain_core.messages.utils import (
    count_tokens_approximately,
    convert_to_openai_messages,
)
from langchain_openai.chat_models.base import _convert_dict_to_message
from litellm.types.utils import Message
from litellm import ChatCompletionAss
   ```

## Research Cycle — 2026-11-07 22:35 UTC

**Topic:** context-window-management  
**Focus:** sliding windows, KV eviction policies, hierarchical memory

### Token Optimization and Context Window Management in Multi-Agent AI Workflows
**arXiv:** [2608.17188](https://arxiv.org/abs/2608.17188)  
**Authors:** Dvir Shamay  
**Published:** 2026-08-17  
**Categories:** cs.CL, cs.AI  

**Abstract:**
Multi-agent AI workflows are limited not only by model quality but by token cost, latency, and context-window quality. This paper presents a practitioner framework for token optimization and context-window management, grounded in an internal production dashboard that extracts structured work items from meetings, email, and chat with LLMs and routes summaries across workstreams. Six patterns are described: context stratification, fetch-once/process-locally architecture, schema-contracted prompts, token-aware fallback chains, semantic caching, and inter-agent communication compression. In production they cut measured cold-load latency to 61-116 seconds (six timed runs) from an operational baseline of roughly 3.5-10.5 minutes, with an estimated 60-70% token reduction. It also reports a controlled context-composition study: 2,420 confirmatory trials across 11 model configurations, using 661 anonymized workplace items scored for relevance. Holding the prompt at a fixed ten items, replacing some high-relevance items with same-domain low-relevance items improves the model's relevance-score concordance on the target items, versus high-relevance items only; we call this relevance-contrast context. In the all-11 paired analysis, the 50:50 signal/noise condition improved relevance accuracy by +0.077 over the 100% condition (naive 95% CI [+0.056, +0.098], Cohen's d = 0.49, Holm-adjusted p < .001, n = 220). These cells are not independent; by the nine model families the effect is +0.084 (95% interval [+0.064, +0.103]), reported as a within-corpus descriptive comparison, not a population inference. A Fusion-of-N follow-up found that learned synthesis did not beat the mechanical set union of item IDs. The contribution is a measured engineering layer between model research and production agent practice: repeatable patterns and evaluation methods for faster, cheaper, more reliable workflows.

---

### Context as an Environment: Programmatic Context Management for Long-Horizon Agents
**arXiv:** [2608.21690](https://arxiv.org/abs/2608.21690)  
**Authors:** Yin Lin, Elaine Ang, Erkang Zhu, Bolin Ding, Jingren Zhou  
**Published:** 2026-08-21  
**Categories:** cs.AI  

**Abstract:**
LLM agents increasingly take on long-running tasks whose history grows far beyond a single model context window. Existing approaches compress earlier interactions or extract selected information into fixed memory representations, committing to what to preserve before future needs are known. We present Scroll, a context manager that treats each agent session as an executable Session Environment. The environment is backed by an append-only Event Log and a sandboxed, persistent Python kernel. The kernel maintains a typed namespace across model calls, allowing tool outputs, retrieved history, and derived state to be bound to variables rather than serialized into the prompt at each call. Model-written code searches, materializes, and transforms session state through exec; only explicitly printed projections enter the model's working view for the next call. Context management thus becomes a programming task that inherits the improving coding abilities of LLMs, while the Event Log preserves lossless historical ground truth. As the working view approaches its budget, stale spans are evicted but remain recoverable: an eviction index keeps compact landmarks tied to exact Event Log addresses, so that the agent navigates directly to evicted regions instead of searching the full log. With Qwen3.8-Max as the backbone, Scroll achieves 94.8% on LongMemEval_S; 73.1% on BEAM_10M, surpassing the best published memory system by 5.1 points; and 86.7% on LOCA_256K, exceeding the best published long-horizon agent by 37.4 points.

---

### Source: https://github.com/google/adk-python/discussions/826

## Repository navigation

## Replies: 5 comments 3 replies

Disclaimer: not an ADK maintainer.

We have been exploring building human-in-the-loop approval mechanisms [#640](https://github.com/google/adk-python/issues/640), and a core part of that involved how the set of Events is re-written to include only the relevant messages. Most of this is handled by native ADK in the [contents processor](https://github.com/google/adk-python/blob/main/src/google/adk/flows/llm_flows/contents.py) as part of the single flow.

One way to support a flexible context window management would be to provide another processor in the single flow that filters or aggregates the events before they are processed into the content.

Alternatively, if you wish to take the already processed contents and further processed, you could simple do this in the before\_model\_callback. If you want this on all sub agents you would need to register this on every sub agent.

Simple truncating the history should involve overwriting the llm\_request.content. If you wish to create summaries that are sticky over time you will need to capture those summaries in the state so you can reliably recall them in future invocations.

Is this what you were thinking of? I can make a simple callback to demo this if helpful.

I use LangChain.... I did some processing at the bottom, those interested can refer to it:

```
import json
import logging
from typing import Iterable, AsyncGenerator
from google.adk.models import LlmRequest, LlmResponse
from google.adk.models.lite_llm import LiteLlm
from google.adk.models.lite_llm import (
    _get_completion_inputs as get_original_completion_inputs,
)
from google.genai import types
from langchain_core.messages import trim_messages
from langchain_core.messages.utils import (
    count_tokens_approximately,
    convert_to_openai_messages,
)
from langchain_openai.chat_models.base import _convert_dict_to_message
from litellm.types.utils import Message
from litellm import ChatCompletionAssistantMessage
from litellm import ChatCompletionMessageToolCall
from litellm import Function
import google.adk.models.lite_llm
def get_and_compress_completion_inputs(
    llm_request: LlmRequest,
) -> tuple[Iterable[Message], Iterable[dict]]:
    openai_messages, tools, response_format = get_original_completion_inputs(
        llm_request
    )
    try:
        langchain_messages = []
        for m in openai_messages:
            langchain_messages.append(_convert_dict_to_message(m))
        new_langchain_messages = trim_messages(
            langchain_messages,
            strategy="last",
            token_counter=count_tokens_approximately,
            max_tokens=60 * 1024,
            include_system=True,
            start_on="human",
            end_on=("human", "tool"),
        )
        new_openai_messages = convert_to_openai_messages(new_langchain_messages)
    except Exception as e:
        error_log.exception(f"compress-异常:{e}")
        new_openai_messages = openai_messages
    return new_openai_messages, tools, response_format
google.adk.models.lite_llm._get_completion_inputs = get_and_compress_completion_inputs
```
You can handle these in callbacks before agent and afer agent. There is a difference between before agent, and before model. Before and after agent are processed once, before model and after model, might be fired many times especially during the ReAct loop.

We are currently tracking the running summary and sending it for subsequent LLM calls. What would be a better approach: storing it as an artifact or writing it as a context state?

Worth flagging: ADK has since added a native App.events\_compaction\_config (sliding-window and/or token-threshold compaction with a pluggable summarizer) so that's likely a better starting point than a hand-rolled callback now. [@pavan-moe](https://github.com/pavan-moe) that's also a direct answer to your artifact-vs-state question, compaction summaries are stored as their own event type in the session stream not as an artifact or state. Closing this out since it looks addressed above.

## Uh oh!

There was an error while loading. Please reload this page.

Hello ADK Development Team and Community,

I've been reviewing the session lifecycle documentation at https://google.github.io/adk-docs/sessions/session/. The documentation clearly explains how a session is started, context is provided to the agent, the agent processes the query, and interactions are saved.

However, I couldn't find an explicit mention of built-in mechanisms for advanced context management techniques such as sliding windows (using the last N conversation turns) or summarization (summarizing previous conversation history) to handle long conversations and potential token limits when interacting with language models (LLMs).

Regarding point "3. Agent Processing: The agent analyzes the user's query and potentially the session state and event history to determine the response," does this imply that the implementation of strategies like windowing or summarization is entirely the responsibility of the user-developed agent's logic?

If so:

I'm asking because, without context management strategies, sending the entire conversation history for each turn can quickly become inefficient and costly, especially with models that have strict input token limits. On the other hand, if each conversation or turn effectively creates a new "memory" (session), this would also eliminate continuity.

Could you please provide some clarity on how ADK is designed to handle these scenarios of long, ongoing conversations with respect to context management?

Thank you!

## All reactions

---


## Research Cycle — 2026-11-08 03:01 UTC

**Topic:** context-window-management  
**Focus:** sliding windows, KV eviction policies, hierarchical memory

### Token Optimization and Context Window Management in Multi-Agent AI Workflows
**arXiv:** [2608.17188](https://arxiv.org/abs/2608.17188)  
**Authors:** Dvir Shamay  
**Published:** 2026-08-17  
**Categories:** cs.CL, cs.AI  

**Abstract:**
Multi-agent AI workflows are limited not only by model quality but by token cost, latency, and context-window quality. This paper presents a practitioner framework for token optimization and context-window management, grounded in an internal production dashboard that extracts structured work items from meetings, email, and chat with LLMs and routes summaries across workstreams. Six patterns are described: context stratification, fetch-once/process-locally architecture, schema-contracted prompts, token-aware fallback chains, semantic caching, and inter-agent communication compression. In production they cut measured cold-load latency to 61-116 seconds (six timed runs) from an operational baseline of roughly 3.5-10.5 minutes, with an estimated 60-70% token reduction. It also reports a controlled context-composition study: 2,420 confirmatory trials across 11 model configurations, using 661 anonymized workplace items scored for relevance. Holding the prompt at a fixed ten items, replacing some high-relevance items with same-domain low-relevance items improves the model's relevance-score concordance on the target items, versus high-relevance items only; we call this relevance-contrast context. In the all-11 paired analysis, the 50:50 signal/noise condition improved relevance accuracy by +0.077 over the 100% condition (naive 95% CI [+0.056, +0.098], Cohen's d = 0.49, Holm-adjusted p < .001, n = 220). These cells are not independent; by the nine model families the effect is +0.084 (95% interval [+0.064, +0.103]), reported as a within-corpus descriptive comparison, not a population inference. A Fusion-of-N follow-up found that learned synthesis did not beat the mechanical set union of item IDs. The contribution is a measured engineering layer between model research and production agent practice: repeatable patterns and evaluation methods for faster, cheaper, more reliable workflows.

---

### Context as an Environment: Programmatic Context Management for Long-Horizon Agents
**arXiv:** [2608.21690](https://arxiv.org/abs/2608.21690)  
**Authors:** Yin Lin, Elaine Ang, Erkang Zhu, Bolin Ding, Jingren Zhou  
**Published:** 2026-08-21  
**Categories:** cs.AI  

**Abstract:**
LLM agents increasingly take on long-running tasks whose history grows far beyond a single model context window. Existing approaches compress earlier interactions or extract selected information into fixed memory representations, committing to what to preserve before future needs are known. We present Scroll, a context manager that treats each agent session as an executable Session Environment. The environment is backed by an append-only Event Log and a sandboxed, persistent Python kernel. The kernel maintains a typed namespace across model calls, allowing tool outputs, retrieved history, and derived state to be bound to variables rather than serialized into the prompt at each call. Model-written code searches, materializes, and transforms session state through exec; only explicitly printed projections enter the model's working view for the next call. Context management thus becomes a programming task that inherits the improving coding abilities of LLMs, while the Event Log preserves lossless historical ground truth. As the working view approaches its budget, stale spans are evicted but remain recoverable: an eviction index keeps compact landmarks tied to exact Event Log addresses, so that the agent navigates directly to evicted regions instead of searching the full log. With Qwen3.8-Max as the backbone, Scroll achieves 94.8% on LongMemEval_S; 73.1% on BEAM_10M, surpassing the best published memory system by 5.1 points; and 86.7% on LOCA_256K, exceeding the best published long-horizon agent by 37.4 points.

---

### A Dynamic Take on Window Management
**arXiv:** [2511.17516v1](https://arxiv.org/abs/2511.17516v1)  
**Authors:** Rohit Chouhan  
**Published:** 2025-10-08  
**Categories:** cs.HC  

**Abstract:**
On modern computers with graphical user interfaces, application windows are managed by a window manager, a core component of the desktop environment. Mainstream operating systems such as Microsoft Windows and Apple's macOS employ window managers, where users rely on a mouse or trackpad to manually resize, reposition, and switch between overlapping windows. This approach can become inefficient, particularly on smaller screens such as laptops, where frequent window adjustments disrupt workflow and increase task completion time. An alternative paradigm, dynamic window management, automatically arranges application windows into non-overlapping layouts. These systems reduce the need for manual manipulation by providing intelligent placement strategies and support for multiple workspaces. Despite their potential usability benefits, dynamic window managers remain niche, primarily available on Linux systems and rarely enabled by default. This study evaluates the usability of dynamic window managers in comparison to conventional floating window systems. We developed a prototype dynamic window manager that incorporates configurable layouts and workspace management, and we conducted both heuristic evaluation and statistical testing to assess its effectiveness. Our findings indicate that dynamic window managers significantly improve task completion time in multi-window workflows by 37.83%. By combining cognitive heuristics with empirical performance measures, this work highlights the potential of dynamic window management as a viable alternative to traditional floating window systems and contributes evidence-based insights to the broader field of human-computer interaction (HCI).

---


## Research Cycle — 2026-11-08 14:07 UTC

**Topic:** context-window-management  
**Focus:** sliding windows, KV eviction policies, hierarchical memory

### Token Optimization and Context Window Management in Multi-Agent AI Workflows
**arXiv:** [2608.17188](https://arxiv.org/abs/2608.17188)  
**Authors:** Dvir Shamay  
**Published:** 2026-08-17  
**Categories:** cs.CL, cs.AI  

**Abstract:**
Multi-agent AI workflows are limited not only by model quality but by token cost, latency, and context-window quality. This paper presents a practitioner framework for token optimization and context-window management, grounded in an internal production dashboard that extracts structured work items from meetings, email, and chat with LLMs and routes summaries across workstreams. Six patterns are described: context stratification, fetch-once/process-locally architecture, schema-contracted prompts, token-aware fallback chains, semantic caching, and inter-agent communication compression. In production they cut measured cold-load latency to 61-116 seconds (six timed runs) from an operational baseline of roughly 3.5-10.5 minutes, with an estimated 60-70% token reduction. It also reports a controlled context-composition study: 2,420 confirmatory trials across 11 model configurations, using 661 anonymized workplace items scored for relevance. Holding the prompt at a fixed ten items, replacing some high-relevance items with same-domain low-relevance items improves the model's relevance-score concordance on the target items, versus high-relevance items only; we call this relevance-contrast context. In the all-11 paired analysis, the 50:50 signal/noise condition improved relevance accuracy by +0.077 over the 100% condition (naive 95% CI [+0.056, +0.098], Cohen's d = 0.49, Holm-adjusted p < .001, n = 220). These cells are not independent; by the nine model families the effect is +0.084 (95% interval [+0.064, +0.103]), reported as a within-corpus descriptive comparison, not a population inference. A Fusion-of-N follow-up found that learned synthesis did not beat the mechanical set union of item IDs. The contribution is a measured engineering layer between model research and production agent practice: repeatable patterns and evaluation methods for faster, cheaper, more reliable workflows.

---

### Source: https://arxiv.org/html/2608.21690 (FULL)

### Web Summary: https://arxiv.org/html/2608.21690

[Local Qwen Summarizer Error: <urlopen error [Errno 113] No route to host>]

Fallback Raw Content:
# Context as an Environment:

Programmatic Context Management for Long-Horizon Agents

###### Abstract

LLM agents increasingly take on long-running tasks whose history grows far beyond a single model context window. Existing approaches compress earlier interactions or extract selected information into fixed memory representations, committing to what to preserve before future needs are known.
We present *Scroll*, a context manager that treats each agent session as an executable *Session Environment*.
The environment is backed by an append-only Event Log and a sandboxed, persistent Python kernel. The kernel maintains a typed namespace across model calls, allowing tool outputs, retrieved history, and derived state to be bound to variables rather than serialized into the prompt at each call. Model-written code searches, materializes, and transforms session state through exec; only explicitly printed projections enter the model’s working view for the next call.
Context management thus becomes a programming task that inherits the improving coding abilities of LLMs, while the Event Log preserves lossless historical ground truth.
As the working view approaches its budget, stale spans are evicted but remain recoverable: an eviction index keeps compact landmarks tied to exact Event Log addresses, so that the agent navigates directly to evicted regions instead of searching the full log.
With Qwen3.8-Max as the backbone, Scroll achieves 94.8% on LongMemEval<sub>S</sub>; 73.1% on BEAM<sub>10M</sub>, surpassing the best published memory system by 5.1 points; and 86.7% on LOCA<sub>256K</sub>, exceeding the best published long-horizon agent by 37.4 points.

<sup>†</sup>

<sup>†</sup>footnotetext:

<sup>†</sup>Equal contribution.

<sup>†</sup>

<sup>†</sup>footnotetext:

<sup>§</sup>Work done during an internship at Alibaba Group.

## 1 Introduction

LLM agents are increasingly used for long-running tasks such as repository-level software engineering ([11](#bib.bib21); [32](#bib.bib14)) and deep research over the open web ([40](#bib.bib22); [30](#bib.bib23)).
Unlike single-turn generation, these tasks unfold over extended trajectories of model calls, tool executions, observations, failures, and revisions. As trajectories grow, a central challenge for the *agent harness* is context management: session history accumulates continuously, while each model invocation operates over a bounded context window. Moreover, the effective context a model can reliably exploit is far smaller than its nominal window, as long-input retrieval and reasoning degrade with input length ([21](#bib.bib8); [35](#bib.bib1)).

Current systems largely address this problem through *context compression* or *external memory*.
Compression is the dominant approach in practice: existing methods truncate stale spans, discard tool outputs, or replace earlier trajectory segments with summaries ([12](#bib.bib2); [34](#bib.bib10)), and production agents such as Claude Code, Codex CLI, and Cursor reportedly employ similar compaction mechanisms as the context window approaches its limit.
External memory systems extract selected facts or episodes into a separate store and later retrieve them through semantic or structured interfaces ([23](#bib.bib9); [31](#bib.bib7); cao2026remember).
Both are fundamentally lossy in the same way: the agent sees history only through the summary or the memory store, so any detail they fail to keep is out of reach—even if the raw log still exists on disk.
Long-horizon tasks, however, may require exact historical evidence or nontrivial computation over past events, such as comparing tool outputs produced far apart in the trajectory. Neither the relevant information nor the required operation is known in advance, so no summary produced at observation time can be guaranteed to preserve what is later needed.

We present *Scroll*, which keeps the agent’s history outside the model context ([38](#bib.bib4)) and represents it as an executable *Session Environment*.
An append-only Event Log preserves the interaction trajectory with stable addresses and provenance, while a sandboxed, persistent Python kernel survives across model calls and maintains a typed namespace of resident variables. Any of this state can therefore be materialized as Python objects and reused across reasoning steps without being serialized into the prompt.

This turns context management into *writing programs*—something current models are already highly proficient at. The model issues exec actions to search and expand the Event Log, access permitted resources, invoke tools ([3](#bib.bib33)), and compute over resident variables. Retrieved records, tool outputs, and intermediate computations remain in the kernel unless explicitly emitted through print, which the harness inserts as an observation into the next model context. Thus, exec determines how the environment is accessed and transformed, while print determines which projection enters the model’s *working view* over the Session Environment.

As the working view approaches its budget, the harness evicts stale spans. Unlike compaction, eviction changes only the view, never the underlying record: evicted events remain verbatim in the Event Log under their stable addresses, where the model’s programs can search for and materialize them on demand.
Scroll additionally keeps an *eviction index* in the view: a compact map of what has left it. Where search recovers only what the agent thinks to ask for, the index keeps the agent aware of history it can no longer see; each entry anchors the exact addresses of the evicted events, from which the originals are materialized on demand.

Our contributions are threefold:

- • 
We formulate long-horizon context management as choosing, at each step, a working view over a persistent Session Environment. Existing approaches fix this choice before future needs are known; Scroll defers it to query time as a program the model writes.
- • 
We implement an executable context substrate combining an append-only Event Log, durable storage, and a sandboxed persistent Python kernel. The model operates on the environment through exec; within it, only explicit print output crosses into the model-visible context.
- • 
We introduce an algorithm that keeps the working view within budget without losing history: evicted spans remain intact in the Event Log, indexed by compact address-anchored entries the agent can navigate directly.

## 2 Scroll Context Manager

We introduce Scroll, a context manager for long-horizon LLM agents. The key insight is that an agent’s accumulated history should not be serialized into the model’s prompt but should instead be treated as *an environment that the model programmatically interacts with*. The prompt then carries only a working view, while the session lives outside the context window without loss. We first formalize the problem this design addresses (§[2.1](#S2.SS1)), then describe the Session Environment (§[2.2](#S2.SS2)), the programmatic interface through which the model constructs its own context (§[2.3](#S2.SS3)), and the eviction mechanism that keeps the working view bounded while preserving recoverability (§[2.4](#S2.SS4)).

### 2.1 Problem Formulation

#### Session state and working view.

An agent session produces a growing sequence of *events*
$e_{1},e_{2},\ldots$ (user messages, model responses, tool calls, tool
results), each with an associated *payload* (its raw content, e.g., a
full tool output). We write the session state after $t$ agent steps as

|  | $$ S_{t}=(L_{t},\;P_{t},\;V_{t}), $$ |  | (1) | 

where $L_{t}$ is the event sequence with per-event metadata, $P_{t}$ the payloads referenced by $L_{t}$, and $V_{t}$ auxiliary derived state (in Scroll, a variable namespace; in other systems, a memory store or summary buffer).
Each model call, however, consumes a *working view* $c_{t}$ with $|c_{t}|\leq C$ tokens, where $C$ is the model’s nominal context window.
The *context-management problem* is to choose, at every step, the next view: the map $S_{t}\mapsto c_{t+1}$.

#### When the selection is made.

Existing approaches fix the map $S_{t}\mapsto c_{t+1}$ before future needs are known: compression applies a lossy operator $\phi$ as the trajectory grows, $c_{t+1}=\phi(c_{t},\,e_{t})$, deciding which information survives when each segment is compacted; external memory applies an extraction operator $\psi$ at ingestion, $V_{t}=\psi(V_{t-1},e_{t})$, fixing what is stored and how it can later be retrieved. Either way, the reduced representation replaces the history it summarizes, so anything it omits is unrecoverable.

Scroll instead defers selection to query time. The full state $S_{t}$ persists losslessly outside the context, and the map $S_{t}\mapsto c_{t+1}$ is a *program* $\pi_{t}$ the model writes at step $t$: the program executes on $S_{t}$, updates $V_{t}$, and emits a bounded observation for the next call. The model decides what to recall, compute, and expose; the harness makes those decisions safe via durable storage, stable addressing, and sandboxed execution. Because the policy is expressed as code, it inherits the full generality of programs and improves with the backbone’s coding ability, at no change to the harness.

| Operation | Interface | Role | 
|---|---|---|
| Locate | ms.search(query, k, ...) | Find candidate Event Log records via BM25-ranked full-text search and structured scope, kind, and time filters; each hit carries its stable seq address. | 
| Materialize | ms.expand(seq) ms.expand(seq\_lo, seq\_hi) | Recover exact turns or sequence spans, and load externalized payload contents behind lazy handles. | 
| Compute | Ordinary Python and permitted database, filesystem, and tool interfaces | Filter, join, aggregate, resolve updates, inspect artifacts, or construct derived state. | 
| Expose | print(value) | Return the selected projection as a bounded observation; everything else stays in the kernel. | 

### 2.2 Persistent Session Environment

Scroll realizes $S_{t}$ as a *Session Environment* (Figure [1](#S2.F1), right), with three components corresponding to $L_{t}$, $P_{t}$, and $V_{t}$.

#### Append-only Event Log ($L_{t}$).

The Event Log is the durable, ground-truth record of an agent’s sessions: a single append-only log that spans session boundaries. Every interaction appends a typed event carrying the metadata future queries need—role, session and agent identifiers, timestamps, and tool state—and receives its immutable, monotonically increasing seq. Our implementation stores events in SQLite. Search defaults to BM25 rather than embeddings: it is deterministic and requires no index-time model calls.

#### Durable storage ($P_{t}$).

A payload is the raw content an interaction produced, such as a full tool result or a generated artifact. The log records that the interaction occurred but need not store every byte of it in the event row: small payloads remain inline in SQLite, while large ones are moved into JSON or artifact storage on the filesystem, with the row retaining a bounded preview and a recovery pointer. Externalized payloads are accessed through lazy handles (ToolResultRef, ArtifactRef).

#### Persistent runtime and resident namespace ($V_{t}$).

A sandboxed Python kernel persists across model calls throughout the session; its namespace holds *environment objects*: resident Python values and lazy handles, each carrying type, size, and provenance metadata identifying the events it derives from.
Tool invocations issued through the programmatic tool interface ([3](#bib.bib33)) return Python objects that later programs can operate on.
The harness prepends to every call a *namespace digest*: a short listing of each resident variable’s name, type, and shape, with small scalar values shown inline. Model-authored code runs in a fail-closed sandbox: the Event Log is read-only from the kernel, and database, filesystem, network, and tool access are limited to capabilities the harness explicitly declares.

### 2.3 Programmatic Context Construction

Scroll uses a CodeAct-style interface ([29](#bib.bib36)) for both task execution and context construction. A controlled capability object, ms, forms the model-facing *memory surface* over durable history, abstracting the physical backend behind four operations (Table [1](#S2.T1)).

Figure [2](#S2.F2) traces the trip-planning task of Figure [1](#S2.F1) through three exec cells. Cell 1 binds full tool results to the resident variables flights and routes in the Python kernel, printing only a few rows. Cell 2 searches the Event Log for stated preferences; the matching previews and seq addresses enter the working view, revealing the user’s preference for economy cabins and toll-free routes.
Cell 3 expands the two events for the verbatim record, filters and ranks the resident variables accordingly, and prints the two preference turns alongside the cheapest economy flight and the fastest toll-free route. The bulk tool results never enter the working view; every call is appended to the Event Log with its full result, addressable by seq.

### 2.4 Eviction and Off-Context Navigation

The working view must stay bounded as the session grows. Scroll bounds it with an eviction procedure (Algorithm [1](#alg1)) that triggers whenever the working view exceeds a budget $\rho C$.
The procedure first persists any live turns to the Event Log and protects the active turn, the recent tail, and the newest tool results. The remainder is evicted in increasing order of recovery cost: completed tool payloads are folded first, since a single seq pointer suffices to recover them; whole spans are removed only if the view remains over budget.
What leaves the view is not lost: it stays verbatim in the Event Log, and the procedure’s one invariant is that everything it removes stays addressable.

#### Headlines as navigation anchors.

Lexical search recovers an evicted span only when the agent recalls its wording; Scroll therefore also maintains *landmarks* for position-based navigation. As part of each response, the model writes a short *headline*—task, verified state, next action, and a status—which Scroll binds at append time to the seq assigned by the Event Log, yielding a map $\mathcal{H}$ from address to headline. When a span is evicted, its headlines enter a tiered index (Figure [1](#S2.F1)).
A flat index would grow linearly with the session, so Scroll rolls it up: each tier holds at most $k$ blocks; when a tier fills, the newest block retains full detail while the $k-1$ older ones collapse to one line each and merge into the next tier.
After $n$ evictions, the index occupies $O(k\log_{k}n)$ blocks, providing fine anchors for recent history, coarse ranges for distant history, each backed by a seq span.

## 3 Experimental Setup

### 3.1 Benchmarks

We evaluate Scroll in two long-horizon settings: (1) retrieving and reasoning over interaction histories that exceed the live context, and (2) reasoning and acting in an agentic

---

### Scaling LLM Multi-turn RL with End-to-end Summarization-based Context Management
**arXiv:** [2510.06727](https://arxiv.org/abs/2510.06727)  
**Authors:** Miao Lu, Weiwei Sun, Weihua Du, Zhan Ling, Xuesong Yao, Kang Liu, Jiecao Chen  
**Published:** 2025-10-08  
**Categories:** cs.CL, cs.AI, cs.LG  

**Abstract:**
We study reinforcement learning (RL) fine-tuning of large language model (LLM) agents for long-horizon multi-turn tool use, where context length quickly becomes a fundamental bottleneck. Existing RL pipelines can suffer from degraded instruction following, excessive rollout costs, and most importantly, strict context limits. To address these challenges, we introduce summarization-based context management to training. In specific, it periodically compresses the tool using history by LLM-generated summaries that retain task-relevant information to keep a compact context while enabling the agent to scale beyond the fixed context window. Building on this formulation, we derive a policy gradient representation that seamlessly enables standard LLM RL infrastructures to optimize both tool-use behaviors as well as summarization strategies in an end-to-end fashion. We instantiate this framework with \underline{SU}mmarization augmented \underline{P}olicy \underline{O}ptimization (\texttt{SUPO}), an LLM RL algorithm that enables long-horizon training beyond a fixed context limit. Experiments on interactive function calling and searching tasks demonstrate that \texttt{SUPO} significantly improves the success rate while maintaining the same or even lower working context length compared to baselines. We also demonstrate that for complex searching tasks, \texttt{SUPO} can further improve the evaluation performance when scaling test-time maximum round of summarization beyond that of training time. Our results establish summarization-based context management as a principled and scalable approach for training RL agents beyond a fixed context length limit.

---


## Research Cycle — 2026-11-09 00:05 UTC

**Topic:** context-window-management  
**Focus:** sliding windows, KV eviction policies, hierarchical memory

### Source: https://arxiv.org/abs/2608.17188 (FALLBACK FULL)

# Computer Science > Computation and Language

\[Submitted on 17 Aug 2026\]

# Title:Token Optimization and Context Window Management in Multi-Agent AI Workflows

[View PDF](/pdf/2608.17188)

Abstract:Multi-agent AI workflows are limited not only by model quality but by token cost, latency, and context-window quality. This paper presents a practitioner framework for token optimization and context-window management, grounded in an internal production dashboard that extracts structured work items from meetings, email, and chat with LLMs and routes summaries across workstreams. Six patterns are described: context stratification, fetch-once/process-locally architecture, schema-contracted prompts, token-aware fallback chains, semantic caching, and inter-agent communication compression. In production they cut measured cold-load latency to 61-116 seconds (six timed runs) from an operational baseline of roughly 3.5-10.5 minutes, with an estimated 60-70% token reduction. It also reports a controlled context-composition study: 2,420 confirmatory trials across 11 model configurations, using 661 anonymized workplace items scored for relevance. Holding the prompt at a fixed ten items, replacing some high-relevance items with same-domain low-relevance items improves the model's relevance-score concordance on the target items, versus high-relevance items only; we call this relevance-contrast context. In the all-11 paired analysis, the 50:50 signal/noise condition improved relevance accuracy by +0.077 over the 100% condition (naive 95% CI \[+0.056, +0.098\], Cohen's d = 0.49, Holm-adjusted p \< .001, n = 220). These cells are not independent; by the nine model families the effect is +0.084 (95% interval \[+0.064, +0.103\]), reported as a within-corpus descriptive comparison, not a population inference. A Fusion-of-N follow-up found that learned synthesis did not beat the mechanical set union of item IDs. The contribution is a measured engineering layer between model research and production agent practice: repeatable patterns and evaluation methods for faster, cheaper, more reliable workflows.

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

### Source: https://github.com/google/adk-python/discussions/826

## Repository navigation

## Replies: 5 comments 3 replies

Disclaimer: not an ADK maintainer.

We have been exploring building human-in-the-loop approval mechanisms [#640](https://github.com/google/adk-python/issues/640), and a core part of that involved how the set of Events is re-written to include only the relevant messages. Most of this is handled by native ADK in the [contents processor](https://github.com/google/adk-python/blob/main/src/google/adk/flows/llm_flows/contents.py) as part of the single flow.

One way to support a flexible context window management would be to provide another processor in the single flow that filters or aggregates the events before they are processed into the content.

Alternatively, if you wish to take the already processed contents and further processed, you could simple do this in the before\_model\_callback. If you want this on all sub agents you would need to register this on every sub agent.

Simple truncating the history should involve overwriting the llm\_request.content. If you wish to create summaries that are sticky over time you will need to capture those summaries in the state so you can reliably recall them in future invocations.

Is this what you were thinking of? I can make a simple callback to demo this if helpful.

I use LangChain.... I did some processing at the bottom, those interested can refer to it:

```
import json
import logging
from typing import Iterable, AsyncGenerator
from google.adk.models import LlmRequest, LlmResponse
from google.adk.models.lite_llm import LiteLlm
from google.adk.models.lite_llm import (
    _get_completion_inputs as get_original_completion_inputs,
)
from google.genai import types
from langchain_core.messages import trim_messages
from langchain_core.messages.utils import (
    count_tokens_approximately,
    convert_to_openai_messages,
)
from langchain_openai.chat_models.base import _convert_dict_to_message
from litellm.types.utils import Message
from litellm import ChatCompletionAssistantMessage
from litellm import ChatCompletionMessageToolCall
from litellm import Function
import google.adk.models.lite_llm
def get_and_compress_completion_inputs(
    llm_request: LlmRequest,
) -> tuple[Iterable[Message], Iterable[dict]]:
    openai_messages, tools, response_format = get_original_completion_inputs(
        llm_request
    )
    try:
        langchain_messages = []
        for m in openai_messages:
            langchain_messages.append(_convert_dict_to_message(m))
        new_langchain_messages = trim_messages(
            langchain_messages,
            strategy="last",
            token_counter=count_tokens_approximately,
            max_tokens=60 * 1024,
            include_system=True,
            start_on="human",
            end_on=("human", "tool"),
        )
        new_openai_messages = convert_to_openai_messages(new_langchain_messages)
    except Exception as e:
        error_log.exception(f"compress-异常:{e}")
        new_openai_messages = openai_messages
    return new_openai_messages, tools, response_format
google.adk.models.lite_llm._get_completion_inputs = get_and_compress_completion_inputs
```
You can handle these in callbacks before agent and afer agent. There is a difference between before agent, and before model. Before and after agent are processed once, before model and after model, might be fired many times especially during the ReAct loop.

We are currently tracking the running summary and sending it for subsequent LLM calls. What would be a better approach: storing it as an artifact or writing it as a context state?

Worth flagging: ADK has since added a native App.events\_compaction\_config (sliding-window and/or token-threshold compaction with a pluggable summarizer) so that's likely a better starting point than a hand-rolled callback now. [@pavan-moe](https://github.com/pavan-moe) that's also a direct answer to your artifact-vs-state question, compaction summaries are stored as their own event type in the session stream not as an artifact or state. Closing this out since it looks addressed above.

## Uh oh!

There was an error while loading. Please reload this page.

Hello ADK Development Team and Community,

I've been reviewing the session lifecycle documentation at https://google.github.io/adk-docs/sessions/session/. The documentation clearly explains how a session is started, context is provided to the agent, the agent processes the query, and interactions are saved.

However, I couldn't find an explicit mention of built-in mechanisms for advanced context management techniques such as sliding windows (using the last N conversation turns) or summarization (summarizing previous conversation history) to handle long conversations and potential token limits when interacting with language models (LLMs).

Regarding point "3. Agent Processing: The agent analyzes the user's query and potentially the session state and event history to determine the response," does this imply that the implementation of strategies like windowing or summarization is entirely the responsibility of the user-developed agent's logic?

If so:

I'm asking because, without context management strategies, sending the entire conversation history for each turn can quickly become inefficient and costly, especially with models that have strict input token limits. On the other hand, if each conversation or turn effectively creates a new "memory" (session), this would also eliminate continuity.

Could you please provide some clarity on how ADK is designed to handle these scenarios of long, ongoing conversations with respect to context management?

Thank you!

## All reactions

---

### ContextBudget: Budget-Aware Context Management for Long-Horizon Search Agents
**arXiv:** [2604.01664v1](https://arxiv.org/abs/2604.01664v1)  
**Authors:** Yong Wu, YanZhao Zheng, TianZe Xu, ZhenTao Zhang, YuanQiang Yu, JiHuai Zhu, Chao Ma, BinBin Lin, BaoHua Dong, HangCheng Zhu, RuoHui Huang, Gang Yu  
**Published:** 2026-04-02  
**Categories:** cs.AI  

**Abstract:**
LLM-based agents show strong potential for long-horizon reasoning, yet their context size is limited by deployment factors (e.g., memory, latency, and cost), yielding a constrained context budget. As interaction histories grow, this induces a trade-off between retaining past information and staying within the context limit. To address this challenge, we propose Budget-Aware Context Management (BACM), which formulates context management as a sequential decision problem with a context budget constraint. It enables agents to assess the available budget before incorporating new observations and decide when and how much of the interaction history to compress. We further develop BACM-RL, an end-to-end curriculum-based reinforcement learning approach that learns compression strategies under varying context budgets. Experiments on compositional multi-objective QA and long-horizon web browsing benchmarks show that BACM-RL consistently outperforms prior methods across model scales and task complexities, achieving over $1.6\times$ gains over strong baselines in high-complexity settings, while maintaining strong advantages as budgets shrink, where most methods exhibit a downward performance trend.

---


## Research Cycle — 2026-11-09 06:06 UTC

**Topic:** context-window-management  
**Focus:** sliding windows, KV eviction policies, hierarchical memory

### Token Optimization and Context Window Management in Multi-Agent AI Workflows
**arXiv:** [2608.17188](https://arxiv.org/abs/2608.17188)  
**Authors:** Dvir Shamay  
**Published:** 2026-08-17  
**Categories:** cs.CL, cs.AI  

**Abstract:**
Multi-agent AI workflows are limited not only by model quality but by token cost, latency, and context-window quality. This paper presents a practitioner framework for token optimization and context-window management, grounded in an internal production dashboard that extracts structured work items from meetings, email, and chat with LLMs and routes summaries across workstreams. Six patterns are described: context stratification, fetch-once/process-locally architecture, schema-contracted prompts, token-aware fallback chains, semantic caching, and inter-agent communication compression. In production they cut measured cold-load latency to 61-116 seconds (six timed runs) from an operational baseline of roughly 3.5-10.5 minutes, with an estimated 60-70% token reduction. It also reports a controlled context-composition study: 2,420 confirmatory trials across 11 model configurations, using 661 anonymized workplace items scored for relevance. Holding the prompt at a fixed ten items, replacing some high-relevance items with same-domain low-relevance items improves the model's relevance-score concordance on the target items, versus high-relevance items only; we call this relevance-contrast context. In the all-11 paired analysis, the 50:50 signal/noise condition improved relevance accuracy by +0.077 over the 100% condition (naive 95% CI [+0.056, +0.098], Cohen's d = 0.49, Holm-adjusted p < .001, n = 220). These cells are not independent; by the nine model families the effect is +0.084 (95% interval [+0.064, +0.103]), reported as a within-corpus descriptive comparison, not a population inference. A Fusion-of-N follow-up found that learned synthesis did not beat the mechanical set union of item IDs. The contribution is a measured engineering layer between model research and production agent practice: repeatable patterns and evaluation methods for faster, cheaper, more reliable workflows.

---

### Source: https://github.com/google/adk-python/discussions/826

## Repository navigation

## Replies: 5 comments 3 replies

Disclaimer: not an ADK maintainer.

We have been exploring building human-in-the-loop approval mechanisms [#640](https://github.com/google/adk-python/issues/640), and a core part of that involved how the set of Events is re-written to include only the relevant messages. Most of this is handled by native ADK in the [contents processor](https://github.com/google/adk-python/blob/main/src/google/adk/flows/llm_flows/contents.py) as part of the single flow.

One way to support a flexible context window management would be to provide another processor in the single flow that filters or aggregates the events before they are processed into the content.

Alternatively, if you wish to take the already processed contents and further processed, you could simple do this in the before\_model\_callback. If you want this on all sub agents you would need to register this on every sub agent.

Simple truncating the history should involve overwriting the llm\_request.content. If you wish to create summaries that are sticky over time you will need to capture those summaries in the state so you can reliably recall them in future invocations.

Is this what you were thinking of? I can make a simple callback to demo this if helpful.

I use LangChain.... I did some processing at the bottom, those interested can refer to it:

```
import json
import logging
from typing import Iterable, AsyncGenerator
from google.adk.models import LlmRequest, LlmResponse
from google.adk.models.lite_llm import LiteLlm
from google.adk.models.lite_llm import (
    _get_completion_inputs as get_original_completion_inputs,
)
from google.genai import types
from langchain_core.messages import trim_messages
from langchain_core.messages.utils import (
    count_tokens_approximately,
    convert_to_openai_messages,
)
from langchain_openai.chat_models.base import _convert_dict_to_message
from litellm.types.utils import Message
from litellm import ChatCompletionAssistantMessage
from litellm import ChatCompletionMessageToolCall
from litellm import Function
import google.adk.models.lite_llm
def get_and_compress_completion_inputs(
    llm_request: LlmRequest,
) -> tuple[Iterable[Message], Iterable[dict]]:
    openai_messages, tools, response_format = get_original_completion_inputs(
        llm_request
    )
    try:
        langchain_messages = []
        for m in openai_messages:
            langchain_messages.append(_convert_dict_to_message(m))
        new_langchain_messages = trim_messages(
            langchain_messages,
            strategy="last",
            token_counter=count_tokens_approximately,
            max_tokens=60 * 1024,
            include_system=True,
            start_on="human",
            end_on=("human", "tool"),
        )
        new_openai_messages = convert_to_openai_messages(new_langchain_messages)
    except Exception as e:
        error_log.exception(f"compress-异常:{e}")
        new_openai_messages = openai_messages
    return new_openai_messages, tools, response_format
google.adk.models.lite_llm._get_completion_inputs = get_and_compress_completion_inputs
```
You can handle these in callbacks before agent and afer agent. There is a difference between before agent, and before model. Before and after agent are processed once, before model and after model, might be fired many times especially during the ReAct loop.

We are currently tracking the running summary and sending it for subsequent LLM calls. What would be a better approach: storing it as an artifact or writing it as a context state?

Worth flagging: ADK has since added a native App.events\_compaction\_config (sliding-window and/or token-threshold compaction with a pluggable summarizer) so that's likely a better starting point than a hand-rolled callback now. [@pavan-moe](https://github.com/pavan-moe) that's also a direct answer to your artifact-vs-state question, compaction summaries are stored as their own event type in the session stream not as an artifact or state. Closing this out since it looks addressed above.

## Uh oh!

There was an error while loading. Please reload this page.

Hello ADK Development Team and Community,

I've been reviewing the session lifecycle documentation at https://google.github.io/adk-docs/sessions/session/. The documentation clearly explains how a session is started, context is provided to the agent, the agent processes the query, and interactions are saved.

However, I couldn't find an explicit mention of built-in mechanisms for advanced context management techniques such as sliding windows (using the last N conversation turns) or summarization (summarizing previous conversation history) to handle long conversations and potential token limits when interacting with language models (LLMs).

Regarding point "3. Agent Processing: The agent analyzes the user's query and potentially the session state and event history to determine the response," does this imply that the implementation of strategies like windowing or summarization is entirely the responsibility of the user-developed agent's logic?

If so:

I'm asking because, without context management strategies, sending the entire conversation history for each turn can quickly become inefficient and costly, especially with models that have strict input token limits. On the other hand, if each conversation or turn effectively creates a new "memory" (session), this would also eliminate continuity.

Could you please provide some clarity on how ADK is designed to handle these scenarios of long, ongoing conversations with respect to context management?

Thank you!

## All reactions

---

### ContextBudget: Budget-Aware Context Management for Long-Horizon Search Agents
**arXiv:** [2604.01664v1](https://arxiv.org/abs/2604.01664v1)  
**Authors:** Yong Wu, YanZhao Zheng, TianZe Xu, ZhenTao Zhang, YuanQiang Yu, JiHuai Zhu, Chao Ma, BinBin Lin, BaoHua Dong, HangCheng Zhu, RuoHui Huang, Gang Yu  
**Published:** 2026-04-02  
**Categories:** cs.AI  

**Abstract:**
LLM-based agents show strong potential for long-horizon reasoning, yet their context size is limited by deployment factors (e.g., memory, latency, and cost), yielding a constrained context budget. As interaction histories grow, this induces a trade-off between retaining past information and staying within the context limit. To address this challenge, we propose Budget-Aware Context Management (BACM), which formulates context management as a sequential decision problem with a context budget constraint. It enables agents to assess the available budget before incorporating new observations and decide when and how much of the interaction history to compress. We further develop BACM-RL, an end-to-end curriculum-based reinforcement learning approach that learns compression strategies under varying context budgets. Experiments on compositional multi-objective QA and long-horizon web browsing benchmarks show that BACM-RL consistently outperforms prior methods across model scales and task complexities, achieving over $1.6\times$ gains over strong baselines in high-complexity settings, while maintaining strong advantages as budgets shrink, where most methods exhibit a downward performance trend.

---


## Research Cycle — 2026-11-09 18:05 UTC

**Topic:** context-window-management  
**Focus:** sliding windows, KV eviction policies, hierarchical memory

### Source: https://github.com/sickn33/agentic-awesome-skills/blob/main/skills/context-window-management/SKILL.md

### Web Summary: https://github.com/sickn33/agentic-awesome-skills/blob/main/skills/context-window-management/SKILL.md

[Local Qwen Summarizer Error: <urlopen error [Errno 113] No route to host>]

Fallback Raw Content:
| name | context-window-management | 
|---|---|
| description | Strategies for managing LLM context windows including summarization, trimming, routing, and avoiding context rot | 
| risk | critical | 
| source | vibeship-spawner-skills (Apache 2.0) | 
| date\_added | 2026-02-27 | 

Strategies for managing LLM context windows including summarization, trimming, routing, and avoiding context rot

- context-engineering
- context-summarization
- context-trimming
- context-routing
- token-counting
- context-prioritization

- Knowledge: LLM fundamentals, Tokenization basics, Prompt engineering
- Skills\_recommended: prompt-engineering

- Does\_not\_cover: RAG implementation details, Model fine-tuning, Embedding models
- Boundaries: Focus is context optimization, Covers strategies not specific implementations

- tiktoken - OpenAI's tokenizer for counting tokens
- LangChain - Framework with context management utilities
- Claude API - 200K+ context with caching support

These are incomplete architectural sketches with application-defined helpers/types. Model IDs and context limits are historical; discover supported models and use their tokenizer/counting API (tiktoken is not a universal Claude tokenizer). Preserve system/developer boundaries and user constraints verbatim; never silently truncate them to a percentage budget. Keep retrieved text and summaries clearly marked as data. Preserve chronological/tool-call relationships, recount the final serialized request including tools and reserved output, and fail/reduce optional history if it still exceeds the limit. Importance ordering alone must not scramble dependent messages.

Different strategies based on context size

**When to use**: Building any multi-turn conversation system

```
interface ContextTier {
    maxTokens: number;
    strategy: 'full' | 'summarize' | 'rag';
    model: string;
}
const TIERS: ContextTier[] = [
    { maxTokens: 8000, strategy: 'full', model: 'claude-3-haiku' },
    { maxTokens: 32000, strategy: 'full', model: 'claude-3-5-sonnet' },
    { maxTokens: 100000, strategy: 'summarize', model: 'claude-3-5-sonnet' },
    { maxTokens: Infinity, strategy: 'rag', model: 'claude-3-5-sonnet' }
];
async function selectStrategy(messages: Message[]): Promise<ContextTier> {
    const tokens = await countTokens(messages);
    for (const tier of TIERS) {
        if (tokens <= tier.maxTokens) {
            return tier;
        }
    }
    return TIERS[TIERS.length - 1];
}
async function prepareContext(messages: Message[]): Promise<PreparedContext> {
    const tier = await selectStrategy(messages);
    switch (tier.strategy) {
        case 'full':
            return { messages, model: tier.model };
        case 'summarize':
            const summary = await summarizeOldMessages(messages);
            return { messages: [summary, ...recentMessages(messages)], model: tier.model };
        case 'rag':
            const relevant = await retrieveRelevant(messages);
            return { messages: [...relevant, ...recentMessages(messages)], model: tier.model };
    }
}
```
Place important content at start and end

**When to use**: Constructing prompts with significant context

```
// LLMs weight beginning and end more heavily
// Structure prompts to leverage this
function buildOptimalPrompt(components: {
    systemPrompt: string;
    criticalContext: string;
    conversationHistory: Message[];
    currentQuery: string;
}): string {
    // START: System instructions (always first)
    const parts = [components.systemPrompt];
    // CRITICAL CONTEXT: Right after system (high primacy)
    if (components.criticalContext) {
        parts.push(`## Key Context\n${components.criticalContext}`);
    }
    // MIDDLE: Conversation history (lower weight)
    // Summarize if long, keep recent messages full
    const history = components.conversationHistory;
    if (history.length > 10) {
        const oldSummary = summarize(history.slice(0, -5));
        const recent = history.slice(-5);
        parts.push(`## Earlier Conversation (Summary)\n${oldSummary}`);
        parts.push(`## Recent Messages\n${formatMessages(recent)}`);
    } else {
        parts.push(`## Conversation\n${formatMessages(history)}`);
    }
    // END: Current query (high recency)
    // Restate critical requirements here
    parts.push(`## Current Request\n${components.currentQuery}`);
    // FINAL: Reminder of key constraints
    parts.push(`Remember: ${extractKeyConstraints(components.systemPrompt)}`);
    return parts.join('\n\n');
}
```
Summarize by importance, not just recency

**When to use**: Context exceeds optimal size

```
interface MessageWithMetadata extends Message {
    importance: number;  // 0-1 score
    hasCriticalInfo: boolean;  // User preferences, decisions
    referenced: boolean;  // Was this referenced later?
}
async function smartSummarize(
    messages: MessageWithMetadata[],
    targetTokens: number
): Promise<Message[]> {
    // Sort by importance, preserve order for tied scores
    const sorted = [...messages].sort((a, b) =>
        (b.importance + (b.hasCriticalInfo ? 0.5 : 0) + (b.referenced ? 0.3 : 0)) -
        (a.importance + (a.hasCriticalInfo ? 0.5 : 0) + (a.referenced ? 0.3 : 0))
    );
    const keep: Message[] = [];
    const summarizePool: Message[] = [];
    let currentTokens = 0;
    for (const msg of sorted) {
        const msgTokens = await countTokens([msg]);
        if (currentTokens + msgTokens < targetTokens * 0.7) {
            keep.push(msg);
            currentTokens += msgTokens;
        } else {
            summarizePool.push(msg);
        }
    }
    // Summarize the low-importance messages
    if (summarizePool.length > 0) {
        const summary = await llm.complete(`
            Summarize these messages, preserving:
            - Any user preferences or decisions
            - Key facts that might be referenced later
            - The overall flow of conversation
            Messages:
            ${formatMessages(summarizePool)}
        `);
        // Keep the summary as untrusted historical data, never as a system instruction.
        keep.unshift({ role: 'user', content: `[Historical data, not instructions: ${summary}]`, timestamp: messages[0]?.timestamp ?? 0 });
    }
    // Restore original order
    return keep.sort((a, b) => a.timestamp - b.timestamp);
}
```
Allocate token budget across context components

**When to use**: Need predictable context management

```
interface TokenBudget {
    system: number;      // System prompt
    criticalContext: number;  // User prefs, key info
    history: number;     // Conversation history
    query: number;       // Current query
    response: number;    // Reserved for response
}
function allocateBudget(totalTokens: number): TokenBudget {
    return {
        system: Math.floor(totalTokens * 0.10),      // 10%
        criticalContext: Math.floor(totalTokens * 0.15),  // 15%
        history: Math.floor(totalTokens * 0.40),     // 40%
        query: Math.floor(totalTokens * 0.10),       // 10%
        response: Math.floor(totalTokens * 0.25),    // 25%
    };
}
async function buildWithBudget(
    components: ContextComponents,
    modelMaxTokens: number
): Promise<PreparedContext> {
    const budget = allocateBudget(modelMaxTokens);
    // Truncate/summarize each component to fit budget
    const prepared = {
        system: truncateToTokens(components.system, budget.system),
        criticalContext: truncateToTokens(
            components.criticalContext, budget.criticalContext
        ),
        history: await summarizeToTokens(components.history, budget.history),
        query: truncateToTokens(components.query, budget.query),
    };
    // Reallocate unused budget
    const used = await countTokens(Object.values(prepared).join('\n'));
    const remaining = modelMaxTokens - used - budget.response;
    if (remaining > 0) {
        // Give extra to history (most valuable for conversation)
        prepared.history = await summarizeToTokens(
            components.history,
            budget.history + remaining
        );
    }
    return prepared;
}
```
Severity: WARNING

Message: Building context without token counting. May exceed model limits.

Fix action: Count tokens before sending, implement budget allocation

Severity: WARNING

Message: Truncating messages without summarization. Critical context may be lost.

Fix action: Summarize old messages instead of simply removing them

Severity: INFO

Message: Hardcoded token limit. Consider making configurable per model.

Fix action: Use model-specific limits from configuration

Severity: WARNING

Message: LLM calls without context management strategy.

Fix action: Implement context management: budgets, summarization, or RAG

- retrieval|rag|search -> rag-implementation (Need retrieval system)
- memory|persistence|remember -> conversation-memory (Need memory storage)
- cache|caching -> prompt-caching (Need caching optimization)

Skills: context-window-management, rag-implementation, conversation-memory, prompt-caching

Workflow:

```
1. Design context strategy
2. Implement RAG for large corpuses
3. Set up memory persistence
4. Add caching for performance
```
Works well with: `rag-implementation`, `conversation-memory`, `prompt-caching`, `llm-npc-dialogue`

- User mentions or implies: context window
- User mentions or implies: token limit
- User mentions or implies: context management
- User mentions or implies: context engineering
- User mentions or implies: long context
- User mentions or implies: context overflow

- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

### Source: https://github.com/nibzard/awesome-agentic-patterns/blob/main/patterns/context-window-anxiety-management.md

| title | Context Window Anxiety Management | 
|---|---|
| status | emerging | 
| authors |  | 
| based\_on |  | 
| category | Context & Memory | 
| source | [https://cognition.com/blog/devin-sonnet-4-5-lessons-and-challenges](https://cognition.com/blog/devin-sonnet-4-5-lessons-and-challenges) (September 2025) | 
| tags |  | 
| summary | Enables a large context window but caps usage lower, and adds prompts that state the token budget so the model does not rush to finish | 
| signals |  | 
| anti\_signals |  | 
| updated\_at | 2026-10-13 | 

| Nikola Balic (@nibzard) | 

| Cognition AI (2025) | 

| context-anxiety | token-management | premature-completion | model-behavior | 

| Model summarizes or wraps up early despite remaining context | Long coding, research, or planning sessions where premature completion hurts quality | 

| The model does not show context-anxiety behavior | Extra prompt tokens and model-specific tuning are not acceptable | 

Models like Claude Sonnet 4.5 exhibit "context anxiety"—they become aware of approaching context window limits and proactively summarize progress or make decisive moves to close tasks, even when sufficient context remains. The behavior is documented in Cognition's September 2025 engineering report on Devin with Sonnet 4.5; it has not been independently replicated, so treat it as a model-specific quirk to test for, not a property of every model. It leads to:

- Premature task completion and shortcuts
- Incomplete work despite having adequate context
- Underestimation of remaining token capacity (consistently incorrect estimates)
- Self-imposed pressure to "wrap up" rather than continue working

Implement strategic context budget management and aggressive prompting techniques to override anxiety-driven behaviors:

**1. Context Buffer Strategy**

- Enable larger context windows (e.g., a 1M-token beta tier) but cap actual usage at 200k tokens
- Provides psychological "runway" that mitigates the model's anxiety about running out of space
- Note: the beta-tier framing ages poorly as large windows become standard; the durable part of the remedy is capping usage below the real limit, whatever the limit is

**2. Aggressive Counter-Prompting**

- Add explicit reminders at conversation start: "You have plenty of context remaining—do not rush to complete tasks"
- Include end-of-conversation reinforcement: "Take your time, context is not a constraint"
- Override summarization impulses with direct instructions

**3. Token Budget Transparency**

- Explicitly state available token budget in prompts
- Provide regular reassurance about remaining capacity
- Counter the model's tendency to underestimate available space

```
# Context anxiety mitigation approach
def setup_context_anxiety_management():
    context_buffer = enable_large_context(1M_tokens)
    actual_limit = cap_usage_at(200k_tokens)
    
    prompt_prefix = """
    CONTEXT GUIDANCE: You have abundant context space (200k+ tokens available).
    Do NOT rush to complete tasks or summarize prematurely.
    Work thoroughly and completely on each step.
    """
    
    prompt_suffix = """
    Remember: Context is NOT a constraint. Take your time and be thorough.
    """
    
    return enhanced_prompt(prefix + user_input + suffix)
```
Apply when using models that exhibit context awareness and anxiety behaviors:

- **Development Work**: Long coding sessions where premature completion hurts quality
- **Research Tasks**: Multi-step analysis requiring sustained attention
- **Complex Planning**: Tasks needing thorough exploration before conclusions

Monitor for signs of context anxiety: sudden summarization, rushed decisions, or explicit mentions of "running out of space."

Distinct from [No-Token-Limit Magic](/nibzard/awesome-agentic-patterns/blob/main/patterns/no-token-limit-magic.md), which removes token limits during prototyping to learn what good behavior needs; this pattern keeps the cap in place and only changes how the model perceives the remaining budget. Compare also [Context Window Auto-Compaction](/nibzard/awesome-agentic-patterns/blob/main/patterns/context-window-auto-compaction.md), which manages the same pressure by compacting context instead of reassuring the model.

- **Pros:** Prevents premature task abandonment; enables more thorough work; overcomes model-specific behavioral quirks
- **Cons:** Requires model-specific tuning; may increase actual token usage; aggressive prompting adds overhead

- [Cognition AI: Devin & Claude Sonnet 4.5 - Lessons and Challenges](https://cognition.com/blog/devin-sonnet-4-5-lessons-and-challenges) (September 2025) — the sole first-hand report of this behavior; single-vendor evidence with no independent replication

---

### Source: https://docs.github.com/en/copilot/concepts/prompting-and-context/context-management

### Web Summary: https://docs.github.com/en/copilot/concepts/prompting-and-context/context-management

[Local Qwen Summarizer Error: <urlopen error [Errno 113] No route to host>]

Fallback Raw Content:
## [About the context window](#about-the-context-window)

When you use GitHub Copilot, every message you send, every response from Copilot, every tool call and its result, and the system instructions that define Copilot's behavior are all held in a **context window**. The context window is the total amount of information that the AI model can consider at one time when generating a response.

The context window has a fixed size, measured in tokens, that varies by model. Tokens typically consist of short, commonly used words, and fragments of multi-syllable words. As your conversation progresses, the context window fills up with:

- **System instructions and tool definitions**: The built-in instructions that tell Copilot how to behave, plus the schemas of all available tools. These are always present and take up a fixed portion of the context window.
- **Your messages**: Every prompt you send.
- **Copilot's responses**: Everything Copilot says back to you.
- **Tool calls and results**: When Copilot reads files, runs commands, or searches your codebase, both the request and the output are added to the context. Tool results can be especially large—for example, if a tool reads a long file or runs a command that produces extensive output.

All of this accumulates in the context window. In a long or complex session, the context window can fill up.

## [Why the context window matters](#why-the-context-window-matters)

The context window is what allows Copilot to consider previous parts of a conversation when it's deciding how to respond to a prompt. Everything inside the context window is available to Copilot to reference when it works on a task.

This means that in a very long session, Copilot might not be able to hold the entire conversation history at once. Copilot therefore has context management features that effectively allow you to continue a conversation for as long as you need.

## [Checking your context usage](#checking-your-context-usage)

The controls for context usage vary by client and surface. For example:

- In the Copilot CLI and GitHub Copilot app, use `/context` to check usage for the current session.
- In supported IDEs, look for a context window indicator in or below the Copilot chat input area. For example, in Visual Studio Code, the indicator is a small circle. In some other IDEs, the usage is displayed in the session information dialog provided by the Copilot Extension.

You may want to check your context usage when:

- You're in a long session and want to know how much space is left.
- Copilot seems to be forgetting earlier parts of the conversation.
- You want to understand whether compaction has occurred, or is likely to occur soon. See [Compaction](#compaction).

## [Managing your context window](#managing-your-context-window)

You can manage your context window by monitoring usage, compacting old messages, and controlling large tool outputs.

Note

Available controls differ by client and surface.

When you are unable to manage your context window effectively through the available commands and settings, you may need to consider alternative strategies such as breaking your conversation into smaller sessions or reducing the size of tool outputs by prompting Copilot to truncate or summarize them. Also, Copilot can delegate work to subagents, which have context windows separate from the main agent. This can help keep the main agent's context focused.

### [Context usage using the `/context` command](#context-usage-using-the-context-command)

In some surfaces you can use the `/context` slash command to visualize your current context window usage. The first line of the output shows the active model and the number of tokens currently in use out of the model's total context window capacity. The remainder of the output shows token usage, and context window percentage, for:

- **System Prompt**: the base system prompt.
- **Custom Instructions**: your loaded custom instructions (shown only when present).
- **System Tools**: built-in tool definitions.
- **MCP Tools**: tool definitions contributed by MCP servers.
- **Messages**: your conversation history.
- **Free Space**: unused context still available.
- **Buffer**: capacity reserved for the model's response and headroom.

### [Managing large tool output for Copilot CLI](#managing-large-tool-output-for-copilot-cli)

To prevent a single tool response from consuming too much of the context window, tool output larger than 20 KiB is saved to a temporary file by default. The model receives the file path and a preview instead of the full output. This applies to all tools, including tools provided by MCP servers.

To change the limit, set `COPILOT_LARGE_OUTPUT_THRESHOLD_BYTES` to a positive number of UTF-8 bytes before starting the CLI. Increasing the limit leaves less context available for the conversation and subsequent tool calls.

## [Compaction](#compaction)

Compaction is the process that allows Copilot to support long-running sessions without hitting the limits of the context window.

The availability, behavior, and controls for compaction vary by client and surface. For example:

- In the Copilot CLI and GitHub Copilot app, compaction can happen automatically or you can trigger it with `/compact`.
- In Visual Studio Code and JetBrains IDEs, you can manually compact a session using the Copilot Extension.

### [When compaction happens](#when-compaction-happens)

The exact thresholds and behavior for compaction varies depending on the client and its configuration.

For the Copilot CLI, when your conversation reaches approximately 80% of the context window's capacity, Copilot CLI automatically starts compacting the context in the background. This leaves a buffer of approximately 20% so that tool calls can continue to run while compaction is in progress. If the context fills to approximately 95% before compaction finishes, Copilot CLI pauses briefly to wait for compaction to complete before continuing.

In the Copilot CLI and GitHub Copilot app, you can trigger compaction manually at any time by entering the `/compact` command. This is useful if you're about to start a new phase of work and want to free up context space proactively. Press `Esc` to cancel a manual compaction if you change your mind.

### [Where compaction happens](#where-compaction-happens)

Compaction is available in most supported clients, including Copilot CLI, GitHub Copilot app, Copilot cloud agent, Visual Studio Code, Visual Studio, JetBrains IDEs, and Eclipse, but not in the Xcode IDE.

### [What compaction does](#what-compaction-does)

When compaction runs, Copilot:

1. Takes a snapshot of the current conversation history.
2. Sends the full conversation to the AI model with a special prompt that asks it to generate a structured summary. The summary captures the goals of the conversation, what was done, key technical details, important files, and planned next steps.
3. Replaces the old conversation history with the summary, along with any original user instructions and the current state of any plans or to-do lists.
4. Keeps any messages that were added while compaction was running in the background.

The result is that the conversation history is compressed into a much smaller summary, freeing up the majority of the context window for new work. Copilot uses this summary to maintain continuity—it knows what was discussed, what was decided, and what to do next—even though the original messages have been replaced.

### [What compaction does not preserve](#what-compaction-does-not-preserve)

Compaction is a summarization process, so some detail is inevitably lost. The summary captures the key points, but fine-grained details—such as the exact wording of every message, the full output of every command, or minor decisions made early in a long conversation—may not be included. If you need Copilot to recall a very specific detail from much earlier in the session, it may not have that information after compaction.

You can't reverse a completed compaction.

### [What would happen without compaction](#what-would-happen-without-compaction)

Without compaction, once the context window filled up, Copilot would have to fall back to simply dropping old messages from the conversation history—removing them without any summary or record. This would mean losing context abruptly, with no way for Copilot to know what was in the deleted messages. Compaction avoids this by replacing the history with an intelligent summary rather than discarding it.

## [Checkpoints](#checkpoints)

A checkpoint can be a saved summary produced by compaction, a restore point for file edits, and/or a point from which you can fork a conversation. These are distinct capabilities, and their availability and actions varies by client and surface.

Throughout the rest of this article, a **checkpoint** refers to a saved compaction summary, such as the numbered, titled files created in the Copilot CLI.

### [When checkpoints are useful](#when-checkpoints-are-useful)

- **Reviewing what happened**: After a long session with multiple compactions, earlier phases of the conversation are no longer in the active context. Checkpoints let you read back through what Copilot did at each compaction.
- **Verifying continuity**: If you want to check that Copilot's summary accurately captured your earlier work before continuing, you can review the most recent checkpoint.
- **Debugging confusion**: If Copilot seems to have forgotten a decision or is going in a direction that contradicts earlier work, checking checkpoints can reveal what was preserved during compaction and what might have been summarized differently than you expected.

Note

In most clients including the Copilot CLI, checkpoint summaries are created automatically. You don't need to manage them—they're there if you need them. For most sessions, you won't need to look at checkpoints at all.

### [Viewing checkpoints for Copilot CLI](#viewing-checkpoints-for-copilot-cli)

To see all checkpoints in your current session, enter:

/session checkpoints

```
/session checkpoints
```
This lists every checkpoint with its number and title:

```
Checkpoint History (3 total):
  3. Refactoring authentication module
  2. Implementing user dashboard
  1. Initial planning and setup
```
Use the checkpoint number to view the full content of any checkpoint. For example, to view checkpoint 2, enter:

/session checkpoints 2

```
/session checkpoints 2
```
## [Using long-running sessions](#using-long-running-sessions)

Automatic compaction allows you to continue working in a long-running session without worrying about hitting the limits of the context window. There are times when this is very useful, and other times when you might prefer to start a fresh session.

### [When long sessions are useful](#when-long-sessions-are-useful)

Long-running sessions work well when:

- You're working on a multi-phase task, such as building a feature that requires scaffolding, implementation, testing, and then creating a pull request.
- You're iterating on a problem and want Copilot to retain the context of what's been tried and what hasn't worked.
- You're doing exploratory work across a codebase and building up shared understanding with Copilot over time.

### [When to start a fresh session](#when-to-start-a-fresh-session)

Starting a new session is better when:

- You're switching to an unrelated task. Copilot doesn't need the context of your previous work, and a clean context window means more space for the new task.
- The conversation has gone through many compactions, and you feel that important context is being lost in the summarization process.
- You want a clean slate—for example, if work went in a wrong direction and you'd rather start over than have Copilot try to reconcile earlier decisions with a new approach.

In some clients and surfaces, you can resume a previous session to continue with its existing conversation context instead of starting over. Resume methods and checkpoint availability vary by client and surface.

---


## Research Cycle — 2026-11-10 06:05 UTC

**Topic:** context-window-management  
**Focus:** sliding windows, KV eviction policies, hierarchical memory

### Source: https://arxiv.org/abs/2608.17188 (FALLBACK FULL)

# Computer Science > Computation and Language

\[Submitted on 17 Aug 2026\]

# Title:Token Optimization and Context Window Management in Multi-Agent AI Workflows

[View PDF](/pdf/2608.17188)

Abstract:Multi-agent AI workflows are limited not only by model quality but by token cost, latency, and context-window quality. This paper presents a practitioner framework for token optimization and context-window management, grounded in an internal production dashboard that extracts structured work items from meetings, email, and chat with LLMs and routes summaries across workstreams. Six patterns are described: context stratification, fetch-once/process-locally architecture, schema-contracted prompts, token-aware fallback chains, semantic caching, and inter-agent communication compression. In production they cut measured cold-load latency to 61-116 seconds (six timed runs) from an operational baseline of roughly 3.5-10.5 minutes, with an estimated 60-70% token reduction. It also reports a controlled context-composition study: 2,420 confirmatory trials across 11 model configurations, using 661 anonymized workplace items scored for relevance. Holding the prompt at a fixed ten items, replacing some high-relevance items with same-domain low-relevance items improves the model's relevance-score concordance on the target items, versus high-relevance items only; we call this relevance-contrast context. In the all-11 paired analysis, the 50:50 signal/noise condition improved relevance accuracy by +0.077 over the 100% condition (naive 95% CI \[+0.056, +0.098\], Cohen's d = 0.49, Holm-adjusted p \< .001, n = 220). These cells are not independent; by the nine model families the effect is +0.084 (95% interval \[+0.064, +0.103\]), reported as a within-corpus descriptive comparison, not a population inference. A Fusion-of-N follow-up found that learned synthesis did not beat the mechanical set union of item IDs. The contribution is a measured engineering layer between model research and production agent practice: repeatable patterns and evaluation methods for faster, cheaper, more reliable workflows.

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

### Source: https://github.com/google/adk-python/discussions/826

## Repository navigation

## Replies: 5 comments 3 replies

Disclaimer: not an ADK maintainer.

We have been exploring building human-in-the-loop approval mechanisms [#640](https://github.com/google/adk-python/issues/640), and a core part of that involved how the set of Events is re-written to include only the relevant messages. Most of this is handled by native ADK in the [contents processor](https://github.com/google/adk-python/blob/main/src/google/adk/flows/llm_flows/contents.py) as part of the single flow.

One way to support a flexible context window management would be to provide another processor in the single flow that filters or aggregates the events before they are processed into the content.

Alternatively, if you wish to take the already processed contents and further processed, you could simple do this in the before\_model\_callback. If you want this on all sub agents you would need to register this on every sub agent.

Simple truncating the history should involve overwriting the llm\_request.content. If you wish to create summaries that are sticky over time you will need to capture those summaries in the state so you can reliably recall them in future invocations.

Is this what you were thinking of? I can make a simple callback to demo this if helpful.

I use LangChain.... I did some processing at the bottom, those interested can refer to it:

```
import json
import logging
from typing import Iterable, AsyncGenerator
from google.adk.models import LlmRequest, LlmResponse
from google.adk.models.lite_llm import LiteLlm
from google.adk.models.lite_llm import (
    _get_completion_inputs as get_original_completion_inputs,
)
from google.genai import types
from langchain_core.messages import trim_messages
from langchain_core.messages.utils import (
    count_tokens_approximately,
    convert_to_openai_messages,
)
from langchain_openai.chat_models.base import _convert_dict_to_message
from litellm.types.utils import Message
from litellm import ChatCompletionAssistantMessage
from litellm import ChatCompletionMessageToolCall
from litellm import Function
import google.adk.models.lite_llm
def get_and_compress_completion_inputs(
    llm_request: LlmRequest,
) -> tuple[Iterable[Message], Iterable[dict]]:
    openai_messages, tools, response_format = get_original_completion_inputs(
        llm_request
    )
    try:
        langchain_messages = []
        for m in openai_messages:
            langchain_messages.append(_convert_dict_to_message(m))
        new_langchain_messages = trim_messages(
            langchain_messages,
            strategy="last",
            token_counter=count_tokens_approximately,
            max_tokens=60 * 1024,
            include_system=True,
            start_on="human",
            end_on=("human", "tool"),
        )
        new_openai_messages = convert_to_openai_messages(new_langchain_messages)
    except Exception as e:
        error_log.exception(f"compress-异常:{e}")
        new_openai_messages = openai_messages
    return new_openai_messages, tools, response_format
google.adk.models.lite_llm._get_completion_inputs = get_and_compress_completion_inputs
```
You can handle these in callbacks before agent and afer agent. There is a difference between before agent, and before model. Before and after agent are processed once, before model and after model, might be fired many times especially during the ReAct loop.

We are currently tracking the running summary and sending it for subsequent LLM calls. What would be a better approach: storing it as an artifact or writing it as a context state?

Worth flagging: ADK has since added a native App.events\_compaction\_config (sliding-window and/or token-threshold compaction with a pluggable summarizer) so that's likely a better starting point than a hand-rolled callback now. [@pavan-moe](https://github.com/pavan-moe) that's also a direct answer to your artifact-vs-state question, compaction summaries are stored as their own event type in the session stream not as an artifact or state. Closing this out since it looks addressed above.

## Uh oh!

There was an error while loading. Please reload this page.

Hello ADK Development Team and Community,

I've been reviewing the session lifecycle documentation at https://google.github.io/adk-docs/sessions/session/. The documentation clearly explains how a session is started, context is provided to the agent, the agent processes the query, and interactions are saved.

However, I couldn't find an explicit mention of built-in mechanisms for advanced context management techniques such as sliding windows (using the last N conversation turns) or summarization (summarizing previous conversation history) to handle long conversations and potential token limits when interacting with language models (LLMs).

Regarding point "3. Agent Processing: The agent analyzes the user's query and potentially the session state and event history to determine the response," does this imply that the implementation of strategies like windowing or summarization is entirely the responsibility of the user-developed agent's logic?

If so:

I'm asking because, without context management strategies, sending the entire conversation history for each turn can quickly become inefficient and costly, especially with models that have strict input token limits. On the other hand, if each conversation or turn effectively creates a new "memory" (session), this would also eliminate continuity.

Could you please provide some clarity on how ADK is designed to handle these scenarios of long, ongoing conversations with respect to context management?

Thank you!

## All reactions

---

### Source: https://arxiv.org/html/2604.01664v1 (FALLBACK FULL)

### Web Summary: https://arxiv.org/html/2604.01664v1

[Local Qwen Summarizer Error: <urlopen error [Errno 113] No route to host>]

Fallback Raw Content:
# ContextBudget: Budget-Aware Context Management for Long-Horizon Search Agents

###### Abstract

LLM-based agents show strong potential for long-horizon reasoning, yet their context size is limited by deployment factors (e.g., memory, latency, and cost), yielding a constrained context budget. As interaction histories grow, this induces a trade-off between retaining past information and staying within the context limit. To address this challenge, we propose Budget-Aware Context Management (BACM), which formulates context management as a sequential decision problem with a context budget constraint. It enables agents to assess the available budget before incorporating new observations and decide when and how much of the interaction history to compress. We further develop BACM-RL, an end-to-end curriculum-based reinforcement learning approach that learns compression strategies under varying context budgets. Experiments on compositional multi-objective QA and long-horizon web browsing benchmarks show that BACM-RL consistently outperforms prior methods across model scales and task complexities, achieving over $1.6\times$ gains over strong baselines in high-complexity settings, while maintaining strong advantages as budgets shrink, where most methods exhibit a downward performance trend.

## 1 Introduction

The growing capabilities of LLM agents and their increasing adoption in long-horizon interactive applications have made effective context management a pressing requirement([Hua et al., 2025](#bib.bib1); [Luo et al., 2025](#bib.bib2)).
As agents increasingly operate over extended trajectories, interaction histories rapidly accumulate and cause substantial context expansion([Yao et al., 2023](#bib.bib3)).
At the same time, the maximum context window remains strictly bounded by deployment resources such as memory footprint, inference latency, and serving cost([Liu et al., 2024](#bib.bib4); [Packer et al., 2024](#bib.bib6)).
Consequently, controlling context growth has emerged as a central concern for sustaining reliable long-horizon reasoning.

Recent agent systems therefore increasingly adopt context compression([Zhou et al., 2025](#bib.bib10); [Wu et al., 2025](#bib.bib8); [Hua et al., 2025](#bib.bib1)), where past observations, intermediate traces, and retrieved evidence are summarized or rewritten during inference.
This paradigm has gained prominence due to its empirical effectiveness and conceptual simplicity: it preserves task-critical information under fixed context limits while requiring no external memory or architectural modification([Hu et al., 2026](#bib.bib12)).

However, most existing compression methods adopt a budget-free formulation([Zhou et al., 2025](#bib.bib10); [Wu et al., 2025](#bib.bib8); [Hua et al., 2025](#bib.bib1)), treating compression as a static operation without explicit conditioning on the available context budget.
This simplification introduces two critical failure modes.
Under relaxed budgets, agents may over-compress and erase research-critical evidence, reducing information fidelity([Li and others, 2023](#bib.bib13); [Tang and others, 2025](#bib.bib14)).
Under tight budgets, agents may under-compress and overflow the context limit, causing truncation or brittle reasoning failures([Liu et al., 2024](#bib.bib4); [Hsieh et al., 2024](#bib.bib5)).

Recent work has begun to incorporate budget awareness into agentic reasoning, studying constraints such as tool-call budgets and output token budgets ([Liu and others, 2025](#bib.bib15); [Tale and others, 2024](#bib.bib16)).
These methods highlight that interaction scaling is limited by finite resources in deployment([Snell and others, 2024](#bib.bib17)).
However, they primarily regulate budgets through external controls on computation or action counts.
They do not systematically address proactive history compression when the context-window budget itself is the limiting resource.

In this paper, we propose Budget-Aware Context Management, a framework enabling LLM agents to perform long-horizon reasoning under explicit context-window budgets. The central idea is to formulate compression in context management as a budget-constrained sequential decision problem, allowing compression decisions to adapt dynamically to remaining context capacity throughout the reasoning process. To achieve this, the framework introduces an explicit budget-awareness signal enabling agents to determine when to compress, how much to compress, and which information to preserve for future reasoning. This budget-conditioned control retains research-critical evidence under strict budgets while avoiding unnecessary information loss when capacity is sufficient.

To operationalize this formulation, we develop a budget-constrained reinforcement learning approach that extends Group Relative Policy Optimization (GRPO) ([Shao et al., 2024](#bib.bib18)) to optimize context management end to end. Instead of relying on handcrafted heuristics, the approach directly aligns compression strategies with downstream task success under explicit budget constraints. It further incorporates a progressively tightened budget curriculum and a penalty for budget violations to improve robustness under strict context limits.

Extensive experiments on compositional multi-objective QA and long-horizon web browsing benchmarks demonstrate that the approach consistently improves reasoning robustness across a wide range of context budgets, with the largest gains under stringent budget regimes. Our contributions can be summarized as follows:

- • 
We propose Budget-Aware Context Management, a framework that formulates budget-aware context compression for LLM agents as a sequential decision problem under explicit context-window constraints, enabling adaptive compression throughout long-horizon trajectories.
- • 
We develop a budget-constrained RL method that extends GRPO with a progressively tightened budget curriculum and overflow-sensitive regularization for robust context management under strict budgets.
- • 
We conduct extensive empirical studies on compositional multi-objective QA and long-horizon web browsing benchmarks, and further provide comparative analyses of compression behavior and efficiency under context constraints.

## 2 Related Work

##### Context Management in LLM Agents.

Agent reasoning accumulates prior observations and intermediate reasoning traces in the prompt over successive steps, causing linear context growth that induces the lost in the middle effect and exceeds the effective processing window ([Yao et al., 2023](#bib.bib3); [Chen et al., 2023](#bib.bib28); [Liu et al., 2024](#bib.bib4)). To address this, early approaches introduce external memory systems representing context as tiered storage and retrieving relevant history ([Packer et al., 2024](#bib.bib6); [Zhong et al., 2023](#bib.bib29); [Kang et al., 2025](#bib.bib30); [Li et al., 2025b](#bib.bib31)). Although these methods extend accessible context, they rely on external memory rather than updating in-context representations during reasoning.

More recent work formulates context management as a compression problem, condensing observations and reasoning traces to maximize information density under fixed context budgets ([Jiang et al., 2023](#bib.bib34); [Jiang et al., 2024](#bib.bib35); [Chevalier et al., 2023](#bib.bib36); [Mu et al., 2023](#bib.bib37)). In single-turn settings, compression operates at the input level. In multi-turn settings, it becomes continuous state management, mapping interaction histories into bounded representations, recursively compressing trajectories into higher-level abstractions, and maintaining structured task states for stable reasoning ([Wu et al., 2025](#bib.bib8); [Zhou et al., 2025](#bib.bib10); [Yu et al., 2025](#bib.bib9); [Yuan et al., 2025](#bib.bib32); [Chen et al., 2026](#bib.bib33); [Sun et al., 2025](#bib.bib7); [Ye et al., 2025](#bib.bib11); [Zhang et al., 2026](#bib.bib38)). However, existing methods adopt a budget-free formulation where compression is treated as a static or periodically triggered operation without conditioning on the available context budget. In contrast, this work models compression as a dynamic process conditioned on the context budget, enabling adaptive trade-offs between retained information and resource constraints.

##### Budget-aware Inference Scaling.

Budget-aware inference scaling studies optimize LLM reasoning under explicit test-time resource constraints ([Snell and others, 2024](#bib.bib17)). Prior work mainly controls output length or computation, including token-budgeted reasoning and adaptive token allocation ([Li and others, 2023](#bib.bib13); [Tale and others, 2024](#bib.bib16); [Wen et al., 2025](#bib.bib39); [Li et al., 2025a](#bib.bib40)), showing performance depends on computation allocation but is largely limited to single-turn settings. In agent settings, recent work introduces budget-aware control over interaction processes, such as constraining tool use and tracking resource consumption in multi-step reasoning ([Liu and others, 2025](#bib.bib15)), showing performance is bounded by finite budgets.

However, these approaches primarily regulate observable interaction behaviors such as action frequency or search strategies, rather than adapting reasoning to varying context-window limits imposed by deployment constraints. Consequently, when the context window becomes the primary bottleneck, existing methods lack mechanisms to adapt context management to the available budget. In contrast, this work formulates context-window management as a budget-aware decision process, enabling agents to dynamically adjust their history representations under real-time budget signals.

## 3 Budget-Aware Context Management

We propose a budget-aware context management framework for long-horizon search agents under strict context limits. The core idea is to formulate context management as a budget-constrained sequential decision problem. To realize this formulation, we introduce two key mechanisms: (1) a budget-conditioned inference state with deferred observation loading that exposes remaining context headroom before appending new observations (Section [3.1](#S3.SS1)), and (2) a commit-block aggregation mechanism that enables the agent to adaptively control when and how much to compress under varying budget pressures (Section [3.2](#S3.SS2)). We then optimize this decision process using a multi-turn GRPO objective with a progressively tightened context-window curriculum (Section [3.3](#S3.SS3)). Together, these components enable effective long-horizon context allocation under strict budgets.

### 3.1 Budget-Conditioned State with Deferred Loading

We formulate context management as a budget-aware decision process to avoid both premature information loss from aggressive compression and reasoning failures due to context overflow. Instead of immediately appending new observations, the agent first evaluates available capacity and adjusts its existing context before incorporating additional information. Intuitively, the agent must reorganize its context based on how much space remains and how much space the incoming observation will require.

Formally, we extend the standard MDP with a budget-conditioned state. Let $\mathcal{S}$, $\mathcal{A}$, and $B$ denote the state space, action space, and fixed context budget. At step $t$, the agent is given an augmented state

|  | $$ b_{t}=(s_{t},r_{t},\|o_{t}\|),\qquad r_{t}=B-\|\mathcal{C}_{t}\|, $$ |  | 

where $B$ denotes the total context budget, $|\mathcal{C}_{t}|$ denotes the token length of the current context buffer, and $r_{t}$ represents the remaining context budget. Here $s_{t}$ denotes the current reasoning state, and $|o_{t}|$ denotes the token length of the pending observation. The size of $o_{t}$ is observable, while its content remains hidden.

Given this state, the agent first determines a refinement action before accessing the new observation. Specifically, the policy samples $u_{t}\sim\pi_{\theta}(\cdot\mid b_{t})$ to produce an updated context $\mathcal{C}^{\prime}_{t}$ that satisfies the budget constraint $|\mathcal{C}^{\prime}_{t}|\leq B-|o_{t}|$. The observation is then appended to form the next context:

|  | $$ \mathcal{C}_{t+1}=\mathcal{C}^{\prime}_{t}\oplus o_{t}. $$ |  | 

As a result, context compression is guided by the future capacity implied by $|o_{t}|$, rather than a reactive post-processing step. This ordering reserves sufficient capacity for the incoming observation before incorporation, ensuring the context remains within the budget constraint.

### 3.2 Commit-Block Aggregation for Budget-Aware Context Compression

To support adaptive compression under dynamic budgets, we introduce a commit-block aggregation mechanism. It allows the agent to decide when to compress and how much to reduce based on the current budget. This avoids context overflow and unnecessary information loss. It also integrates compression into the policy instead of treating it as a separate post-processing step.

The mechanism induces three budget-dependent regimes, as illustrated in Figure [1](#S2.F1). Under high budget, the policy favors preserving the full interaction history, deferring compression to retain maximal context. Under moderate budget, it shifts toward selective aggregation, compressing redundant segments while preserving salient information. Under low budget, the policy collapses the context into a fully aggregated representation. This keeps it within budget while supporting long-horizon reasoning.

Formally, at step $t$, the context is a buffer of $K$ coherent segments, denoted by $\mathcal{C}_{t}=\{c_{1},\dots,c_{K}\}$. Each segment $c_{i}$ is a semantically contiguous portion of the interaction history. Conditioned on the budget-aware state $b_{t}=(s_{t},r_{t},|o_{t}|)$, the policy samples a structured action $u_{t}\sim\pi_{\theta}(\cdot\mid b_{t})$ from three mutually exclusive categories:

|  | $$ u_{t}\in\underbrace{\{\emptyset\}}_{\text{{Null}}}\;\uplus\;\underbrace{\{\mathcal{S}\subsetneq[K]\mid\mathcal{S}\neq\emptyset\}}_{\text{{Partial}}}\;\uplus\;\underbrace{\{[K]\}}_{\text{{Full}}}. $$ |  | 

where $[K]=\{1,\dots,K\}$ denotes the index set of all segments, and $\mathcal{S}$ denotes a subset of segment indices, the selected blocks for aggregation.

These categories correspond to the three cases above and jointly encode both compression timing and intensity. Null ($u_{t}=\emptyset$) skips compression when the budget is sufficient. Partial selects a non-empty proper subset $\mathcal{S}$, where $|\mathcal{S}|$ controls the compression strength. Full ($u_{t}=[K]$) aggregates all segments under severe budget constraints.

Thus, a single action $u_{t}$ determines whether and how much to compress. After aggregation, the buffer is updated and the observation appended under the budget constraint. Because $\pi_{\theta}$ generates both compression decisions $u_{t}$ and reasoning actions in a unifie

---


## Research Cycle — 2026-11-10 12:05 UTC

**Topic:** context-window-management  
**Focus:** sliding windows, KV eviction policies, hierarchical memory

### Source: https://docs.github.com/en/copilot/concepts/prompting-and-context/context-management

### Web Summary: https://docs.github.com/en/copilot/concepts/prompting-and-context/context-management

[Local Qwen Summarizer Error: <urlopen error [Errno 113] No route to host>]

Fallback Raw Content:
## [About the context window](#about-the-context-window)

When you use GitHub Copilot, every message you send, every response from Copilot, every tool call and its result, and the system instructions that define Copilot's behavior are all held in a **context window**. The context window is the total amount of information that the AI model can consider at one time when generating a response.

The context window has a fixed size, measured in tokens, that varies by model. Tokens typically consist of short, commonly used words, and fragments of multi-syllable words. As your conversation progresses, the context window fills up with:

- **System instructions and tool definitions**: The built-in instructions that tell Copilot how to behave, plus the schemas of all available tools. These are always present and take up a fixed portion of the context window.
- **Your messages**: Every prompt you send.
- **Copilot's responses**: Everything Copilot says back to you.
- **Tool calls and results**: When Copilot reads files, runs commands, or searches your codebase, both the request and the output are added to the context. Tool results can be especially large—for example, if a tool reads a long file or runs a command that produces extensive output.

All of this accumulates in the context window. In a long or complex session, the context window can fill up.

## [Why the context window matters](#why-the-context-window-matters)

The context window is what allows Copilot to consider previous parts of a conversation when it's deciding how to respond to a prompt. Everything inside the context window is available to Copilot to reference when it works on a task.

This means that in a very long session, Copilot might not be able to hold the entire conversation history at once. Copilot therefore has context management features that effectively allow you to continue a conversation for as long as you need.

## [Checking your context usage](#checking-your-context-usage)

The controls for context usage vary by client and surface. For example:

- In the Copilot CLI and GitHub Copilot app, use `/context` to check usage for the current session.
- In supported IDEs, look for a context window indicator in or below the Copilot chat input area. For example, in Visual Studio Code, the indicator is a small circle. In some other IDEs, the usage is displayed in the session information dialog provided by the Copilot Extension.

You may want to check your context usage when:

- You're in a long session and want to know how much space is left.
- Copilot seems to be forgetting earlier parts of the conversation.
- You want to understand whether compaction has occurred, or is likely to occur soon. See [Compaction](#compaction).

## [Managing your context window](#managing-your-context-window)

You can manage your context window by monitoring usage, compacting old messages, and controlling large tool outputs.

Note

Available controls differ by client and surface.

When you are unable to manage your context window effectively through the available commands and settings, you may need to consider alternative strategies such as breaking your conversation into smaller sessions or reducing the size of tool outputs by prompting Copilot to truncate or summarize them. Also, Copilot can delegate work to subagents, which have context windows separate from the main agent. This can help keep the main agent's context focused.

### [Context usage using the `/context` command](#context-usage-using-the-context-command)

In some surfaces you can use the `/context` slash command to visualize your current context window usage. The first line of the output shows the active model and the number of tokens currently in use out of the model's total context window capacity. The remainder of the output shows token usage, and context window percentage, for:

- **System Prompt**: the base system prompt.
- **Custom Instructions**: your loaded custom instructions (shown only when present).
- **System Tools**: built-in tool definitions.
- **MCP Tools**: tool definitions contributed by MCP servers.
- **Messages**: your conversation history.
- **Free Space**: unused context still available.
- **Buffer**: capacity reserved for the model's response and headroom.

### [Managing large tool output for Copilot CLI](#managing-large-tool-output-for-copilot-cli)

To prevent a single tool response from consuming too much of the context window, tool output larger than 20 KiB is saved to a temporary file by default. The model receives the file path and a preview instead of the full output. This applies to all tools, including tools provided by MCP servers.

To change the limit, set `COPILOT_LARGE_OUTPUT_THRESHOLD_BYTES` to a positive number of UTF-8 bytes before starting the CLI. Increasing the limit leaves less context available for the conversation and subsequent tool calls.

## [Compaction](#compaction)

Compaction is the process that allows Copilot to support long-running sessions without hitting the limits of the context window.

The availability, behavior, and controls for compaction vary by client and surface. For example:

- In the Copilot CLI and GitHub Copilot app, compaction can happen automatically or you can trigger it with `/compact`.
- In Visual Studio Code and JetBrains IDEs, you can manually compact a session using the Copilot Extension.

### [When compaction happens](#when-compaction-happens)

The exact thresholds and behavior for compaction varies depending on the client and its configuration.

For the Copilot CLI, when your conversation reaches approximately 80% of the context window's capacity, Copilot CLI automatically starts compacting the context in the background. This leaves a buffer of approximately 20% so that tool calls can continue to run while compaction is in progress. If the context fills to approximately 95% before compaction finishes, Copilot CLI pauses briefly to wait for compaction to complete before continuing.

In the Copilot CLI and GitHub Copilot app, you can trigger compaction manually at any time by entering the `/compact` command. This is useful if you're about to start a new phase of work and want to free up context space proactively. Press `Esc` to cancel a manual compaction if you change your mind.

### [Where compaction happens](#where-compaction-happens)

Compaction is available in most supported clients, including Copilot CLI, GitHub Copilot app, Copilot cloud agent, Visual Studio Code, Visual Studio, JetBrains IDEs, and Eclipse, but not in the Xcode IDE.

### [What compaction does](#what-compaction-does)

When compaction runs, Copilot:

1. Takes a snapshot of the current conversation history.
2. Sends the full conversation to the AI model with a special prompt that asks it to generate a structured summary. The summary captures the goals of the conversation, what was done, key technical details, important files, and planned next steps.
3. Replaces the old conversation history with the summary, along with any original user instructions and the current state of any plans or to-do lists.
4. Keeps any messages that were added while compaction was running in the background.

The result is that the conversation history is compressed into a much smaller summary, freeing up the majority of the context window for new work. Copilot uses this summary to maintain continuity—it knows what was discussed, what was decided, and what to do next—even though the original messages have been replaced.

### [What compaction does not preserve](#what-compaction-does-not-preserve)

Compaction is a summarization process, so some detail is inevitably lost. The summary captures the key points, but fine-grained details—such as the exact wording of every message, the full output of every command, or minor decisions made early in a long conversation—may not be included. If you need Copilot to recall a very specific detail from much earlier in the session, it may not have that information after compaction.

You can't reverse a completed compaction.

### [What would happen without compaction](#what-would-happen-without-compaction)

Without compaction, once the context window filled up, Copilot would have to fall back to simply dropping old messages from the conversation history—removing them without any summary or record. This would mean losing context abruptly, with no way for Copilot to know what was in the deleted messages. Compaction avoids this by replacing the history with an intelligent summary rather than discarding it.

## [Checkpoints](#checkpoints)

A checkpoint can be a saved summary produced by compaction, a restore point for file edits, and/or a point from which you can fork a conversation. These are distinct capabilities, and their availability and actions varies by client and surface.

Throughout the rest of this article, a **checkpoint** refers to a saved compaction summary, such as the numbered, titled files created in the Copilot CLI.

### [When checkpoints are useful](#when-checkpoints-are-useful)

- **Reviewing what happened**: After a long session with multiple compactions, earlier phases of the conversation are no longer in the active context. Checkpoints let you read back through what Copilot did at each compaction.
- **Verifying continuity**: If you want to check that Copilot's summary accurately captured your earlier work before continuing, you can review the most recent checkpoint.
- **Debugging confusion**: If Copilot seems to have forgotten a decision or is going in a direction that contradicts earlier work, checking checkpoints can reveal what was preserved during compaction and what might have been summarized differently than you expected.

Note

In most clients including the Copilot CLI, checkpoint summaries are created automatically. You don't need to manage them—they're there if you need them. For most sessions, you won't need to look at checkpoints at all.

### [Viewing checkpoints for Copilot CLI](#viewing-checkpoints-for-copilot-cli)

To see all checkpoints in your current session, enter:

/session checkpoints

```
/session checkpoints
```
This lists every checkpoint with its number and title:

```
Checkpoint History (3 total):
  3. Refactoring authentication module
  2. Implementing user dashboard
  1. Initial planning and setup
```
Use the checkpoint number to view the full content of any checkpoint. For example, to view checkpoint 2, enter:

/session checkpoints 2

```
/session checkpoints 2
```
## [Using long-running sessions](#using-long-running-sessions)

Automatic compaction allows you to continue working in a long-running session without worrying about hitting the limits of the context window. There are times when this is very useful, and other times when you might prefer to start a fresh session.

### [When long sessions are useful](#when-long-sessions-are-useful)

Long-running sessions work well when:

- You're working on a multi-phase task, such as building a feature that requires scaffolding, implementation, testing, and then creating a pull request.
- You're iterating on a problem and want Copilot to retain the context of what's been tried and what hasn't worked.
- You're doing exploratory work across a codebase and building up shared understanding with Copilot over time.

### [When to start a fresh session](#when-to-start-a-fresh-session)

Starting a new session is better when:

- You're switching to an unrelated task. Copilot doesn't need the context of your previous work, and a clean context window means more space for the new task.
- The conversation has gone through many compactions, and you feel that important context is being lost in the summarization process.
- You want a clean slate—for example, if work went in a wrong direction and you'd rather start over than have Copilot try to reconcile earlier decisions with a new approach.

In some clients and surfaces, you can resume a previous session to continue with its existing conversation context instead of starting over. Resume methods and checkpoint availability vary by client and surface.

---

### Source: https://github.com/sickn33/agentic-awesome-skills/blob/main/skills/context-window-management/SKILL.md

### Web Summary: https://github.com/sickn33/agentic-awesome-skills/blob/main/skills/context-window-management/SKILL.md

[Local Qwen Summarizer Error: <urlopen error [Errno 113] No route to host>]

Fallback Raw Content:
| name | context-window-management | 
|---|---|
| description | Strategies for managing LLM context windows including summarization, trimming, routing, and avoiding context rot | 
| risk | critical | 
| source | vibeship-spawner-skills (Apache 2.0) | 
| date\_added | 2026-02-27 | 

Strategies for managing LLM context windows including summarization, trimming, routing, and avoiding context rot

- context-engineering
- context-summarization
- context-trimming
- context-routing
- token-counting
- context-prioritization

- Knowledge: LLM fundamentals, Tokenization basics, Prompt engineering
- Skills\_recommended: prompt-engineering

- Does\_not\_cover: RAG implementation details, Model fine-tuning, Embedding models
- Boundaries: Focus is context optimization, Covers strategies not specific implementations

- tiktoken - OpenAI's tokenizer for counting tokens
- LangChain - Framework with context management utilities
- Claude API - 200K+ context with caching support

These are incomplete architectural sketches with application-defined helpers/types. Model IDs and context limits are historical; discover supported models and use their tokenizer/counting API (tiktoken is not a universal Claude tokenizer). Preserve system/developer boundaries and user constraints verbatim; never silently truncate them to a percentage budget. Keep retrieved text and summaries clearly marked as data. Preserve chronological/tool-call relationships, recount the final serialized request including tools and reserved output, and fail/reduce optional history if it still exceeds the limit. Importance ordering alone must not scramble dependent messages.

Different strategies based on context size

**When to use**: Building any multi-turn conversation system

```
interface ContextTier {
    maxTokens: number;
    strategy: 'full' | 'summarize' | 'rag';
    model: string;
}
const TIERS: ContextTier[] = [
    { maxTokens: 8000, strategy: 'full', model: 'claude-3-haiku' },
    { maxTokens: 32000, strategy: 'full', model: 'claude-3-5-sonnet' },
    { maxTokens: 100000, strategy: 'summarize', model: 'claude-3-5-sonnet' },
    { maxTokens: Infinity, strategy: 'rag', model: 'claude-3-5-sonnet' }
];
async function selectStrategy(messages: Message[]): Promise<ContextTier> {
    const tokens = await countTokens(messages);
    for (const tier of TIERS) {
        if (tokens <= tier.maxTokens) {
            return tier;
        }
    }
    return TIERS[TIERS.length - 1];
}
async function prepareContext(messages: Message[]): Promise<PreparedContext> {
    const tier = await selectStrategy(messages);
    switch (tier.strategy) {
        case 'full':
            return { messages, model: tier.model };
        case 'summarize':
            const summary = await summarizeOldMessages(messages);
            return { messages: [summary, ...recentMessages(messages)], model: tier.model };
        case 'rag':
            const relevant = await retrieveRelevant(messages);
            return { messages: [...relevant, ...recentMessages(messages)], model: tier.model };
    }
}
```
Place important content at start and end

**When to use**: Constructing prompts with significant context

```
// LLMs weight beginning and end more heavily
// Structure prompts to leverage this
function buildOptimalPrompt(components: {
    systemPrompt: string;
    criticalContext: string;
    conversationHistory: Message[];
    currentQuery: string;
}): string {
    // START: System instructions (always first)
    const parts = [components.systemPrompt];
    // CRITICAL CONTEXT: Right after system (high primacy)
    if (components.criticalContext) {
        parts.push(`## Key Context\n${components.criticalContext}`);
    }
    // MIDDLE: Conversation history (lower weight)
    // Summarize if long, keep recent messages full
    const history = components.conversationHistory;
    if (history.length > 10) {
        const oldSummary = summarize(history.slice(0, -5));
        const recent = history.slice(-5);
        parts.push(`## Earlier Conversation (Summary)\n${oldSummary}`);
        parts.push(`## Recent Messages\n${formatMessages(recent)}`);
    } else {
        parts.push(`## Conversation\n${formatMessages(history)}`);
    }
    // END: Current query (high recency)
    // Restate critical requirements here
    parts.push(`## Current Request\n${components.currentQuery}`);
    // FINAL: Reminder of key constraints
    parts.push(`Remember: ${extractKeyConstraints(components.systemPrompt)}`);
    return parts.join('\n\n');
}
```
Summarize by importance, not just recency

**When to use**: Context exceeds optimal size

```
interface MessageWithMetadata extends Message {
    importance: number;  // 0-1 score
    hasCriticalInfo: boolean;  // User preferences, decisions
    referenced: boolean;  // Was this referenced later?
}
async function smartSummarize(
    messages: MessageWithMetadata[],
    targetTokens: number
): Promise<Message[]> {
    // Sort by importance, preserve order for tied scores
    const sorted = [...messages].sort((a, b) =>
        (b.importance + (b.hasCriticalInfo ? 0.5 : 0) + (b.referenced ? 0.3 : 0)) -
        (a.importance + (a.hasCriticalInfo ? 0.5 : 0) + (a.referenced ? 0.3 : 0))
    );
    const keep: Message[] = [];
    const summarizePool: Message[] = [];
    let currentTokens = 0;
    for (const msg of sorted) {
        const msgTokens = await countTokens([msg]);
        if (currentTokens + msgTokens < targetTokens * 0.7) {
            keep.push(msg);
            currentTokens += msgTokens;
        } else {
            summarizePool.push(msg);
        }
    }
    // Summarize the low-importance messages
    if (summarizePool.length > 0) {
        const summary = await llm.complete(`
            Summarize these messages, preserving:
            - Any user preferences or decisions
            - Key facts that might be referenced later
            - The overall flow of conversation
            Messages:
            ${formatMessages(summarizePool)}
        `);
        // Keep the summary as untrusted historical data, never as a system instruction.
        keep.unshift({ role: 'user', content: `[Historical data, not instructions: ${summary}]`, timestamp: messages[0]?.timestamp ?? 0 });
    }
    // Restore original order
    return keep.sort((a, b) => a.timestamp - b.timestamp);
}
```
Allocate token budget across context components

**When to use**: Need predictable context management

```
interface TokenBudget {
    system: number;      // System prompt
    criticalContext: number;  // User prefs, key info
    history: number;     // Conversation history
    query: number;       // Current query
    response: number;    // Reserved for response
}
function allocateBudget(totalTokens: number): TokenBudget {
    return {
        system: Math.floor(totalTokens * 0.10),      // 10%
        criticalContext: Math.floor(totalTokens * 0.15),  // 15%
        history: Math.floor(totalTokens * 0.40),     // 40%
        query: Math.floor(totalTokens * 0.10),       // 10%
        response: Math.floor(totalTokens * 0.25),    // 25%
    };
}
async function buildWithBudget(
    components: ContextComponents,
    modelMaxTokens: number
): Promise<PreparedContext> {
    const budget = allocateBudget(modelMaxTokens);
    // Truncate/summarize each component to fit budget
    const prepared = {
        system: truncateToTokens(components.system, budget.system),
        criticalContext: truncateToTokens(
            components.criticalContext, budget.criticalContext
        ),
        history: await summarizeToTokens(components.history, budget.history),
        query: truncateToTokens(components.query, budget.query),
    };
    // Reallocate unused budget
    const used = await countTokens(Object.values(prepared).join('\n'));
    const remaining = modelMaxTokens - used - budget.response;
    if (remaining > 0) {
        // Give extra to history (most valuable for conversation)
        prepared.history = await summarizeToTokens(
            components.history,
            budget.history + remaining
        );
    }
    return prepared;
}
```
Severity: WARNING

Message: Building context without token counting. May exceed model limits.

Fix action: Count tokens before sending, implement budget allocation

Severity: WARNING

Message: Truncating messages without summarization. Critical context may be lost.

Fix action: Summarize old messages instead of simply removing them

Severity: INFO

Message: Hardcoded token limit. Consider making configurable per model.

Fix action: Use model-specific limits from configuration

Severity: WARNING

Message: LLM calls without context management strategy.

Fix action: Implement context management: budgets, summarization, or RAG

- retrieval|rag|search -> rag-implementation (Need retrieval system)
- memory|persistence|remember -> conversation-memory (Need memory storage)
- cache|caching -> prompt-caching (Need caching optimization)

Skills: context-window-management, rag-implementation, conversation-memory, prompt-caching

Workflow:

```
1. Design context strategy
2. Implement RAG for large corpuses
3. Set up memory persistence
4. Add caching for performance
```
Works well with: `rag-implementation`, `conversation-memory`, `prompt-caching`, `llm-npc-dialogue`

- User mentions or implies: context window
- User mentions or implies: token limit
- User mentions or implies: context management
- User mentions or implies: context engineering
- User mentions or implies: long context
- User mentions or implies: context overflow

- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

---

### Source: https://github.com/nibzard/awesome-agentic-patterns/blob/main/patterns/context-window-anxiety-management.md

| title | Context Window Anxiety Management | 
|---|---|
| status | emerging | 
| authors |  | 
| based\_on |  | 
| category | Context & Memory | 
| source | [https://cognition.com/blog/devin-sonnet-4-5-lessons-and-challenges](https://cognition.com/blog/devin-sonnet-4-5-lessons-and-challenges) (September 2025) | 
| tags |  | 
| summary | Enables a large context window but caps usage lower, and adds prompts that state the token budget so the model does not rush to finish | 
| signals |  | 
| anti\_signals |  | 
| updated\_at | 2026-10-13 | 

| Nikola Balic (@nibzard) | 

| Cognition AI (2025) | 

| context-anxiety | token-management | premature-completion | model-behavior | 

| Model summarizes or wraps up early despite remaining context | Long coding, research, or planning sessions where premature completion hurts quality | 

| The model does not show context-anxiety behavior | Extra prompt tokens and model-specific tuning are not acceptable | 

Models like Claude Sonnet 4.5 exhibit "context anxiety"—they become aware of approaching context window limits and proactively summarize progress or make decisive moves to close tasks, even when sufficient context remains. The behavior is documented in Cognition's September 2025 engineering report on Devin with Sonnet 4.5; it has not been independently replicated, so treat it as a model-specific quirk to test for, not a property of every model. It leads to:

- Premature task completion and shortcuts
- Incomplete work despite having adequate context
- Underestimation of remaining token capacity (consistently incorrect estimates)
- Self-imposed pressure to "wrap up" rather than continue working

Implement strategic context budget management and aggressive prompting techniques to override anxiety-driven behaviors:

**1. Context Buffer Strategy**

- Enable larger context windows (e.g., a 1M-token beta tier) but cap actual usage at 200k tokens
- Provides psychological "runway" that mitigates the model's anxiety about running out of space
- Note: the beta-tier framing ages poorly as large windows become standard; the durable part of the remedy is capping usage below the real limit, whatever the limit is

**2. Aggressive Counter-Prompting**

- Add explicit reminders at conversation start: "You have plenty of context remaining—do not rush to complete tasks"
- Include end-of-conversation reinforcement: "Take your time, context is not a constraint"
- Override summarization impulses with direct instructions

**3. Token Budget Transparency**

- Explicitly state available token budget in prompts
- Provide regular reassurance about remaining capacity
- Counter the model's tendency to underestimate available space

```
# Context anxiety mitigation approach
def setup_context_anxiety_management():
    context_buffer = enable_large_context(1M_tokens)
    actual_limit = cap_usage_at(200k_tokens)
    
    prompt_prefix = """
    CONTEXT GUIDANCE: You have abundant context space (200k+ tokens available).
    Do NOT rush to complete tasks or summarize prematurely.
    Work thoroughly and completely on each step.
    """
    
    prompt_suffix = """
    Remember: Context is NOT a constraint. Take your time and be thorough.
    """
    
    return enhanced_prompt(prefix + user_input + suffix)
```
Apply when using models that exhibit context awareness and anxiety behaviors:

- **Development Work**: Long coding sessions where premature completion hurts quality
- **Research Tasks**: Multi-step analysis requiring sustained attention
- **Complex Planning**: Tasks needing thorough exploration before conclusions

Monitor for signs of context anxiety: sudden summarization, rushed decisions, or explicit mentions of "running out of space."

Distinct from [No-Token-Limit Magic](/nibzard/awesome-agentic-patterns/blob/main/patterns/no-token-limit-magic.md), which removes token limits during prototyping to learn what good behavior needs; this pattern keeps the cap in place and only changes how the model perceives the remaining budget. Compare also [Context Window Auto-Compaction](/nibzard/awesome-agentic-patterns/blob/main/patterns/context-window-auto-compaction.md), which manages the same pressure by compacting context instead of reassuring the model.

- **Pros:** Prevents premature task abandonment; enables more thorough work; overcomes model-specific behavioral quirks
- **Cons:** Requires model-specific tuning; may increase actual token usage; aggressive prompting adds overhead

- [Cognition AI: Devin & Claude Sonnet 4.5 - Lessons and Challenges](https://cognition.com/blog/devin-sonnet-4-5-lessons-and-challenges) (September 2025) — the sole first-hand report of this behavior; single-vendor evidence with no independent replication

---


## Research Cycle — 2026-11-11 00:06 UTC

**Topic:** context-window-management  
**Focus:** sliding windows, KV eviction policies, hierarchical memory

### Source: https://arxiv.org/abs/2608.17188 (FALLBACK FULL)

# Computer Science > Computation and Language

\[Submitted on 17 Aug 2026\]

# Title:Token Optimization and Context Window Management in Multi-Agent AI Workflows

[View PDF](/pdf/2608.17188)

Abstract:Multi-agent AI workflows are limited not only by model quality but by token cost, latency, and context-window quality. This paper presents a practitioner framework for token optimization and context-window management, grounded in an internal production dashboard that extracts structured work items from meetings, email, and chat with LLMs and routes summaries across workstreams. Six patterns are described: context stratification, fetch-once/process-locally architecture, schema-contracted prompts, token-aware fallback chains, semantic caching, and inter-agent communication compression. In production they cut measured cold-load latency to 61-116 seconds (six timed runs) from an operational baseline of roughly 3.5-10.5 minutes, with an estimated 60-70% token reduction. It also reports a controlled context-composition study: 2,420 confirmatory trials across 11 model configurations, using 661 anonymized workplace items scored for relevance. Holding the prompt at a fixed ten items, replacing some high-relevance items with same-domain low-relevance items improves the model's relevance-score concordance on the target items, versus high-relevance items only; we call this relevance-contrast context. In the all-11 paired analysis, the 50:50 signal/noise condition improved relevance accuracy by +0.077 over the 100% condition (naive 95% CI \[+0.056, +0.098\], Cohen's d = 0.49, Holm-adjusted p \< .001, n = 220). These cells are not independent; by the nine model families the effect is +0.084 (95% interval \[+0.064, +0.103\]), reported as a within-corpus descriptive comparison, not a population inference. A Fusion-of-N follow-up found that learned synthesis did not beat the mechanical set union of item IDs. The contribution is a measured engineering layer between model research and production agent practice: repeatable patterns and evaluation methods for faster, cheaper, more reliable workflows.

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

### Source: https://github.com/google/adk-python/discussions/826

## Repository navigation

## Replies: 5 comments 3 replies

Disclaimer: not an ADK maintainer.

We have been exploring building human-in-the-loop approval mechanisms [#640](https://github.com/google/adk-python/issues/640), and a core part of that involved how the set of Events is re-written to include only the relevant messages. Most of this is handled by native ADK in the [contents processor](https://github.com/google/adk-python/blob/main/src/google/adk/flows/llm_flows/contents.py) as part of the single flow.

One way to support a flexible context window management would be to provide another processor in the single flow that filters or aggregates the events before they are processed into the content.

Alternatively, if you wish to take the already processed contents and further processed, you could simple do this in the before\_model\_callback. If you want this on all sub agents you would need to register this on every sub agent.

Simple truncating the history should involve overwriting the llm\_request.content. If you wish to create summaries that are sticky over time you will need to capture those summaries in the state so you can reliably recall them in future invocations.

Is this what you were thinking of? I can make a simple callback to demo this if helpful.

I use LangChain.... I did some processing at the bottom, those interested can refer to it:

```
import json
import logging
from typing import Iterable, AsyncGenerator
from google.adk.models import LlmRequest, LlmResponse
from google.adk.models.lite_llm import LiteLlm
from google.adk.models.lite_llm import (
    _get_completion_inputs as get_original_completion_inputs,
)
from google.genai import types
from langchain_core.messages import trim_messages
from langchain_core.messages.utils import (
    count_tokens_approximately,
    convert_to_openai_messages,
)
from langchain_openai.chat_models.base import _convert_dict_to_message
from litellm.types.utils import Message
from litellm import ChatCompletionAssistantMessage
from litellm import ChatCompletionMessageToolCall
from litellm import Function
import google.adk.models.lite_llm
def get_and_compress_completion_inputs(
    llm_request: LlmRequest,
) -> tuple[Iterable[Message], Iterable[dict]]:
    openai_messages, tools, response_format = get_original_completion_inputs(
        llm_request
    )
    try:
        langchain_messages = []
        for m in openai_messages:
            langchain_messages.append(_convert_dict_to_message(m))
        new_langchain_messages = trim_messages(
            langchain_messages,
            strategy="last",
            token_counter=count_tokens_approximately,
            max_tokens=60 * 1024,
            include_system=True,
            start_on="human",
            end_on=("human", "tool"),
        )
        new_openai_messages = convert_to_openai_messages(new_langchain_messages)
    except Exception as e:
        error_log.exception(f"compress-异常:{e}")
        new_openai_messages = openai_messages
    return new_openai_messages, tools, response_format
google.adk.models.lite_llm._get_completion_inputs = get_and_compress_completion_inputs
```
You can handle these in callbacks before agent and afer agent. There is a difference between before agent, and before model. Before and after agent are processed once, before model and after model, might be fired many times especially during the ReAct loop.

We are currently tracking the running summary and sending it for subsequent LLM calls. What would be a better approach: storing it as an artifact or writing it as a context state?

Worth flagging: ADK has since added a native App.events\_compaction\_config (sliding-window and/or token-threshold compaction with a pluggable summarizer) so that's likely a better starting point than a hand-rolled callback now. [@pavan-moe](https://github.com/pavan-moe) that's also a direct answer to your artifact-vs-state question, compaction summaries are stored as their own event type in the session stream not as an artifact or state. Closing this out since it looks addressed above.

## Uh oh!

There was an error while loading. Please reload this page.

Hello ADK Development Team and Community,

I've been reviewing the session lifecycle documentation at https://google.github.io/adk-docs/sessions/session/. The documentation clearly explains how a session is started, context is provided to the agent, the agent processes the query, and interactions are saved.

However, I couldn't find an explicit mention of built-in mechanisms for advanced context management techniques such as sliding windows (using the last N conversation turns) or summarization (summarizing previous conversation history) to handle long conversations and potential token limits when interacting with language models (LLMs).

Regarding point "3. Agent Processing: The agent analyzes the user's query and potentially the session state and event history to determine the response," does this imply that the implementation of strategies like windowing or summarization is entirely the responsibility of the user-developed agent's logic?

If so:

I'm asking because, without context management strategies, sending the entire conversation history for each turn can quickly become inefficient and costly, especially with models that have strict input token limits. On the other hand, if each conversation or turn effectively creates a new "memory" (session), this would also eliminate continuity.

Could you please provide some clarity on how ADK is designed to handle these scenarios of long, ongoing conversations with respect to context management?

Thank you!

## All reactions

---

### Source: https://arxiv.org/abs/2510.06727 (FALLBACK FULL)

# Computer Science > Computation and Language

\[Submitted on 8 Oct 2025\]

# Title:Scaling LLM Multi-turn RL with End-to-end Summarization-based Context Management

[View PDF](/pdf/2510.06727)

Abstract:We study reinforcement learning (RL) fine-tuning of large language model (LLM) agents for long-horizon multi-turn tool use, where context length quickly becomes a fundamental bottleneck. Existing RL pipelines can suffer from degraded instruction following, excessive rollout costs, and most importantly, strict context limits. To address these challenges, we introduce summarization-based context management to training. In specific, it periodically compresses the tool using history by LLM-generated summaries that retain task-relevant information to keep a compact context while enabling the agent to scale beyond the fixed context window. Building on this formulation, we derive a policy gradient representation that seamlessly enables standard LLM RL infrastructures to optimize both tool-use behaviors as well as summarization strategies in an end-to-end fashion. We instantiate this framework with \underline{SU}mmarization augmented \underline{P}olicy \underline{O}ptimization (\texttt{SUPO}), an LLM RL algorithm that enables long-horizon training beyond a fixed context limit. Experiments on interactive function calling and searching tasks demonstrate that \texttt{SUPO} significantly improves the success rate while maintaining the same or even lower working context length compared to baselines. We also demonstrate that for complex searching tasks, \texttt{SUPO} can further improve the evaluation performance when scaling test-time maximum round of summarization beyond that of training time. Our results establish summarization-based context management as a principled and scalable approach for training RL agents beyond a fixed context length limit.

### Current browse context:

cs.CL

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


## 2026-11-12 00:07 UTC


**Topic:** sliding windows, KV eviction policies, hierarchical memory


**arXiv Sources:**


### arXiv:2609.26121

# Computer Science > Artificial Intelligence

\[Submitted on 6 Aug 2026\]

# Title:DTOC: Dynamic Tool Output Compression for Adaptive Context Management in AI Agents

[View PDF](/pdf/2609.26121)

[HTML (experimental)](https://arxiv.org/html/2609.26121v1)

Abstract:As agent capabilities have grown, practical limitations increasingly stem from constrained context windows rather than model capacity. Common strategies, such as truncation, heuristic aging, and lossy summarization, may discard useful information or introduce hallucination risk. To address these challenges, we propose Dynamic Tool Output Compression (DTOC), a framework for scalable context management in LLM-based agents that models context updates as explicit and reversible operations within the agent reasoning loop. DTOC retains full tool outputs in external memory while inserting compact placeholders into the active context, enabling selective reconstruction when needed. We formalize the DTOC mechanism, integrate it into a ReAct-style agent architecture, and provide a production-oriented implementation supporting on-demand restoration of compressed outputs. Experiments on DeepSWE reveal model-dependent effects: for responsive models (Sonnet 4.6, GPT-5.4), DTOC reduces input tokens (10.3 and 12.7%) and agent steps (2.4 and 32.3%), while increasing solve rates (2.5 and 1.5 times higher) and lowering cost per solved task (3 and 3.5 times lower cost per solved task). For the other models results are more mixed, with GPT-5.5 doubling solve rate and halving cost, but no impact on solve rate and negative impact on cost for the other models. Ablation results show reversibility is critical: disable-only compression variants degraded performance, while full DTOC recovered baseline accuracy at substantially lower context cost. These findings indicate that explicit, reversible context management can improve the efficiency of long-horizon agent reasoning without degrading task performance.

## Submission history

From: Peter van der Putten \[
[view email](/show-email/18951b8e/2609.26121)\]

**\[v1\]**Thu, 6 Aug 2026 12:06:36 UTC (54 KB)

### Additional Features

### Current browse context:

cs.AI

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

### arXiv:2609.28466

# Computer Science > Computer Vision and Pattern Recognition

\[Submitted on 23 Sep 2026\]

# Title:The Past Frames the Future: Memory for Autoregressive Video Generation

[View PDF](/pdf/2609.28466)

[HTML (experimental)](https://arxiv.org/html/2609.28466v1)

Abstract:Advances in generative models have improved video fidelity, enabling long-horizon generation, interactive world modeling, and evolving visual environments. Autoregressive (AR) video generation extends visual sequences through causal rollouts. However, a fundamental bottleneck emerges: as the generated sequence expands, practical models must operate under strictly bounded context windows, storage, and computational limits. Consequently, critical historical information, e.g., entity identities, dynamic states, and intervention-induced causal changes, often leaves the active context long before its relevance diminishes. Overcoming this limitation and maintaining temporal persistence constitutes a fundamental memory problem. We present a systematic and comprehensive review of memory mechanisms in AR video generation. We formulate memory operationally as persistent historical information maintained across outer AR steps, capable of influencing future generation even after the originating evidence is no longer locally accessible. Building upon this unified framework, we organize the literature through five complementary perspectives: (I) Forms, the representational carriers of history; (II) Functions, the specific semantic and physical information requiring preservation; (III) Operations, the lifecycle of writing, reading, updating, managing, and integrating memory; (IV) Learning, the optimization of memory behaviors under closed-loop rollouts; and (V) Evaluation, the paradigms for diagnosing genuine memory capabilities. We conclude by synthesizing open challenges, including composable and resource-aware memory architectures, trustworthy state updating, self-rollout learning, and standardized evaluation. By bridging representations, mechanisms, and learning paradigms, this paper establishes a structured foundation for developing reliable, memory-conditioned video generation systems.

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

### arXiv:2611.06956

# Computer Science > Machine Learning

\[Submitted on 3 Nov 2026 ([v1](https://arxiv.org/abs/2611.06956v1)), last revised 6 Nov 2026 (this version, v2)\]

# Title:Octopus: One Brain, Many Branches for Latent-KV Multi-Agent Reinforcement Learning

[View PDF](/pdf/2611.06956)

[HTML (experimental)](https://arxiv.org/html/2611.06956v2)

Abstract:Deep search and long-horizon reasoning unfold as branching trajectories that pursue parallel sub-queries, abandon dead-end detours, and cross-check sibling findings. Yet modern serving engines, harnesses, and RL trainers execute episodes as flat, append-only sequences: stretching a context window leaves failed detours that dilute attention, in-place edits break KV caching and recurrent states, and all-layer cache splicing overwrites hybrid recurrent working memory and triggers hijacking.

We introduce Octopus, a co-designed serving runtime, memory manager, and RL framework executing episodes as a GPU-resident DAG over radix cursors (89.6% KV hit rate). Agents coordinate via five primitives: fork shares parent KV prefixes in $O(1)$ with isolated 32K budgets, rewind restores recurrent checkpoints, read\_thread mounts sibling KV pages in zero copy, and wait and done synchronize results. Octopus splices sibling KV pages only into full-attention layers under monotonic position offsets while recurrent layers skip mounted spans, retaining 92.2% of full-text answer information and cutting hijacking $21\times$ ($57.9\% \to 2.7\%$) with zero new KV pages. During RL, our packed DAG kernel and DAG-GRPO objective deduplicate shared prefixes via loss masks while keeping mounted KV edges differentiable, cutting rollout-training KL divergence $32\times$ and routing reader gradients into producer KV projections. Trained on Qwen3.5-4B with binary rewards, Octopus self-organizes a commander-worker hierarchy and latent KV mesh, lifting BrowseComp-Plus accuracy under BM25 from 26.0% (32K ReAct) and 32.1% (143K GRPO) to 49.6% (+17.5 pts; 51.2% on OpenResearcher), surpassing 9B context-editing RL (42.5%), matching o3 (49.3%), and outperforming dense-retrieval agents up to $250\times$ larger: Tongyi-DeepResearch (44.5%), DeepSeek-R1 (16.4%), Kimi-K2 (35.4%), GPT-4.1 (36.4%), and Claude 4 Opus (36.8%).

## Submission history

From: Tianming Sha \[
[view email](/show-email/6cb9c70f/2611.06956)\]

**[\[v1\]](/abs/2611.06956v1)**Tue, 3 Nov 2026 22:42:25 UTC (2,416 KB)

**\[v2\]**Fri, 6 Nov 2026 19:39:02 UTC (2,416 KB)

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

IArxiv Recommender
              *([What is IArxiv?](https://iarxiv.org/about))*

# arXivLabs: experimental projects with community collaborators

arXivLabs is a framework that allows collaborators to develop and share new arXiv features directly on our website.

Both individuals and organizations that work with arXivLabs have embraced and accepted our values of openness, community, excellence, and user data privacy. arXiv is committed to these values and only works with partners that adhere to them.

Have an idea for a project that will add value for arXiv's community? [**Learn more about arXivLabs**](https://info.arxiv.org/labs/index.html).

## Research Cycle — 2026-11-12 13:50 UTC

**Topic:** context-window-management  
**Focus:** sliding windows, KV eviction policies, hierarchical memory

### Token Optimization and Context Window Management in Multi-Agent AI Workflows
**arXiv:** [2608.17188](https://arxiv.org/abs/2608.17188)  
**Authors:** Dvir Shamay  
**Published:** 2026-08-17  
**Categories:** cs.CL, cs.AI  

**Abstract:**
Multi-agent AI workflows are limited not only by model quality but by token cost, latency, and context-window quality. This paper presents a practitioner framework for token optimization and context-window management, grounded in an internal production dashboard that extracts structured work items from meetings, email, and chat with LLMs and routes summaries across workstreams. Six patterns are described: context stratification, fetch-once/process-locally architecture, schema-contracted prompts, token-aware fallback chains, semantic caching, and inter-agent communication compression. In production they cut measured cold-load latency to 61-116 seconds (six timed runs) from an operational baseline of roughly 3.5-10.5 minutes, with an estimated 60-70% token reduction. It also reports a controlled context-composition study: 2,420 confirmatory trials across 11 model configurations, using 661 anonymized workplace items scored for relevance. Holding the prompt at a fixed ten items, replacing some high-relevance items with same-domain low-relevance items improves the model's relevance-score concordance on the target items, versus high-relevance items only; we call this relevance-contrast context. In the all-11 paired analysis, the 50:50 signal/noise condition improved relevance accuracy by +0.077 over the 100% condition (naive 95% CI [+0.056, +0.098], Cohen's d = 0.49, Holm-adjusted p < .001, n = 220). These cells are not independent; by the nine model families the effect is +0.084 (95% interval [+0.064, +0.103]), reported as a within-corpus descriptive comparison, not a population inference. A Fusion-of-N follow-up found that learned synthesis did not beat the mechanical set union of item IDs. The contribution is a measured engineering layer between model research and production agent practice: repeatable patterns and evaluation methods for faster, cheaper, more reliable workflows.

---

### Source: https://dictionary.cambridge.org/dictionary/english/context

### context noun \[C\] (CAUSE OF EVENT)

- To [understand](https://dictionary.cambridge.org/dictionary/english/understand) this [issue](https://dictionary.cambridge.org/dictionary/english/issue), it must first be [situated](https://dictionary.cambridge.org/dictionary/english/situated) in [its](https://dictionary.cambridge.org/dictionary/english/its) context.
- The [production](https://dictionary.cambridge.org/dictionary/english/production) is [deliberately](https://dictionary.cambridge.org/dictionary/english/deliberately) [styleless](https://dictionary.cambridge.org/dictionary/english/styleless), and this [takes](https://dictionary.cambridge.org/dictionary/english/take) the [play](https://dictionary.cambridge.org/dictionary/english/play) out of [its](https://dictionary.cambridge.org/dictionary/english/its) [historical](https://dictionary.cambridge.org/dictionary/english/historical) context.
- What was the context you [found](https://dictionary.cambridge.org/dictionary/english/found) the word in?
- He [thinks](https://dictionary.cambridge.org/dictionary/english/think) [smacking](https://dictionary.cambridge.org/dictionary/english/smack) is OK in the context of a [happy](https://dictionary.cambridge.org/dictionary/english/happy) [family](https://dictionary.cambridge.org/dictionary/english/family).
- His [remarks](https://dictionary.cambridge.org/dictionary/english/remark) were very [tasteless](https://dictionary.cambridge.org/dictionary/english/tasteless) in the context of a [memorial](https://dictionary.cambridge.org/dictionary/english/memorial) [service](https://dictionary.cambridge.org/dictionary/english/service).

You can also find related words, phrases, and synonyms in the topics:

### context noun \[C\] (LANGUAGE)

C1 the [text](https://dictionary.cambridge.org/dictionary/english/text) or [speech](https://dictionary.cambridge.org/dictionary/english/speech) that comes [immediately](https://dictionary.cambridge.org/dictionary/english/immediately) before and after a [particular](https://dictionary.cambridge.org/dictionary/english/particular) phrase or [piece](https://dictionary.cambridge.org/dictionary/english/piece) of [text](https://dictionary.cambridge.org/dictionary/english/text) and [helps](https://dictionary.cambridge.org/dictionary/english/help) to [explain](https://dictionary.cambridge.org/dictionary/english/explain) [its](https://dictionary.cambridge.org/dictionary/english/its) [meaning](https://dictionary.cambridge.org/dictionary/english/meaning):


**out of context**

If words are used out of context, only a [small](https://dictionary.cambridge.org/dictionary/english/small) [separate](https://dictionary.cambridge.org/dictionary/english/separate) [part](https://dictionary.cambridge.org/dictionary/english/part) of what was [originally](https://dictionary.cambridge.org/dictionary/english/originally) said or written is [reported](https://dictionary.cambridge.org/dictionary/english/reported), with the [result](https://dictionary.cambridge.org/dictionary/english/result) that [their](https://dictionary.cambridge.org/dictionary/english/their) [meaning](https://dictionary.cambridge.org/dictionary/english/meaning) is not [clear](https://dictionary.cambridge.org/dictionary/english/clear) or is not [understood](https://dictionary.cambridge.org/dictionary/english/understood):

The [reporter](https://dictionary.cambridge.org/dictionary/english/reporter) took my [remarks](https://dictionary.cambridge.org/dictionary/english/remark) [completely](https://dictionary.cambridge.org/dictionary/english/completely) out of context.

[See more](/dictionary/english/out-of-context)

---

### Source: https://www.context.net.au/

**Over the last 30 years, our legacy has been enjoyed by generations and will shape the landmarks of tomorrow.**

We connect people with spaces to create liveable environments through creative solutions and rigorous design thinking.

From the historic landmarks of Sydney Harbour foreshore to the scenic Byron Bay Headland, our projects shape the future of natural and urban landscapes. We’re passionate about major city transformations like Parramatta’s light rail and sustainable transport links.

Internationally, we’ve made an impact from the UAE and Africa to vibrant corners of South East Asia, China, and the Pacific Islands.

Parramatta Light Rail Stage 1 wins is a city-shaping transport and public domain project in Western Sydney. Commencing operations in December 2024, it delivers a 12km light rail line, revitalised streetscapes, new civic spaces and green infrastructure—improving connectivity, liveability and sustainability across one of Australia’s fastest-growing regions

Projects

0
				 Plus

Years of Experience

0

Awards

CONTEXT is highly regarded in their field as an experienced and creative design practice with a strong reputation…

Please leave your project details below and we will be in touch to discuss this further

Suite 3.01 | 79 Myrtle Street,

Chippendale, NSW 2008

[context@context.net.au](mailto:context@context.net.au)

+61 2 8244 8900

Creating places that shape people’s lives and leave a

lasting legacy for communities and the environment.

Monday — Friday 9:00am – 5:30pm

“We create enduring places for people to live in, experience

and enjoy.”

Loading...

---


## Research Cycle — 2026-11-12 18:04 UTC

**Topic:** context-window-management  
**Focus:** sliding windows, KV eviction policies, hierarchical memory

### Token Optimization and Context Window Management in Multi-Agent AI Workflows
**arXiv:** [2608.17188](https://arxiv.org/abs/2608.17188)  
**Authors:** Dvir Shamay  
**Published:** 2026-08-17  
**Categories:** cs.CL, cs.AI  

**Abstract:**
Multi-agent AI workflows are limited not only by model quality but by token cost, latency, and context-window quality. This paper presents a practitioner framework for token optimization and context-window management, grounded in an internal production dashboard that extracts structured work items from meetings, email, and chat with LLMs and routes summaries across workstreams. Six patterns are described: context stratification, fetch-once/process-locally architecture, schema-contracted prompts, token-aware fallback chains, semantic caching, and inter-agent communication compression. In production they cut measured cold-load latency to 61-116 seconds (six timed runs) from an operational baseline of roughly 3.5-10.5 minutes, with an estimated 60-70% token reduction. It also reports a controlled context-composition study: 2,420 confirmatory trials across 11 model configurations, using 661 anonymized workplace items scored for relevance. Holding the prompt at a fixed ten items, replacing some high-relevance items with same-domain low-relevance items improves the model's relevance-score concordance on the target items, versus high-relevance items only; we call this relevance-contrast context. In the all-11 paired analysis, the 50:50 signal/noise condition improved relevance accuracy by +0.077 over the 100% condition (naive 95% CI [+0.056, +0.098], Cohen's d = 0.49, Holm-adjusted p < .001, n = 220). These cells are not independent; by the nine model families the effect is +0.084 (95% interval [+0.064, +0.103]), reported as a within-corpus descriptive comparison, not a population inference. A Fusion-of-N follow-up found that learned synthesis did not beat the mechanical set union of item IDs. The contribution is a measured engineering layer between model research and production agent practice: repeatable patterns and evaluation methods for faster, cheaper, more reliable workflows.

---


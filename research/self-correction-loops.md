
## Research Cycle — 2026-11-07 21:39 UTC

**Topic:** self-correction-loops  
**Focus:** Reflexion, self-consistency, bounded iterations

### Source 1: https://arxiv.org/abs/2604.23366

# Computer Science > Artificial Intelligence

\[Submitted on 25 Apr 2026\]

# Title:GSAR: Typed Grounding for Hallucination Detection and Recovery in Multi-Agent LLMs

[View PDF](/pdf/2604.23366)

[HTML (experimental)](https://arxiv.org/html/2604.23366v1)

Abstract:Autonomous multi-agent LLM systems are increasingly deployed to investigate operational incidents and produce structured diagnostic reports. Their trustworthiness hinges on whether each claim is grounded in observed evidence rather than model-internal inference. Existing groundedness evaluators (binary classifiers, LLM-as-judge scalars, self-correction loops) treat supporting evidence as interchangeable and emit a single signal that offers no principled control over downstream action.

We present GSAR, a grounding-evaluation and replanning framework that (i) partitions claims into a four-way typology (grounded, ungrounded, contradicted, complementary), giving first-class standing to non-redundant alternative perspectives; (ii) assigns evidence-type-specific weights reflecting epistemic strength; (iii) computes an asymmetric contradiction-penalised weighted groundedness score; and (iv) couples that score to a three-tier decision function (proceed, regenerate, replan) driving a bounded-iteration outer loop under an explicit compute budget.

We formalise the algorithm, prove six structural properties, and evaluate five design claims on FEVER with gold Wikipedia evidence under four independently-trained LLM judges (gpt-5.4, claude-sonnet-4-6, claude-opus-4-7, gemini-2.5-pro). Every ablation reproduces in the same direction on every judge: bootstrap 95% CIs on the rho=0 effect exclude 0 on all four; the no-complementary ablation under Opus 4.7 has CI \[-96,-68\] of 200; at n=1000 three independent judges converge to DeltaS(rho=0)=+0.058. A head-to-head against Vectara HHEM-2.1-Open is included. To our knowledge, GSAR is the first published groundedness framework coupling evidence-typed scoring with tiered recovery under an explicit compute budget.

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

### Source 2: https://arxiv.org/abs/2402.07087

# Computer Science > Machine Learning

\[Submitted on 11 Feb 2024 ([v1](https://arxiv.org/abs/2402.07087v1)), last revised 10 Jun 2024 (this version, v3)\]

# Title:Self-Correcting Self-Consuming Loops for Generative Model Training

[View PDF](/pdf/2402.07087)

[HTML (experimental)](https://arxiv.org/html/2402.07087v3)

Abstract:As synthetic data becomes higher quality and proliferates on the internet, machine learning models are increasingly trained on a mix of human- and machine-generated data. Despite the successful stories of using synthetic data for representation learning, using synthetic data for generative model training creates "self-consuming loops" which may lead to training instability or even collapse, unless certain conditions are met. Our paper aims to stabilize self-consuming generative model training. Our theoretical results demonstrate that by introducing an idealized correction function, which maps a data point to be more likely under the true data distribution, self-consuming loops can be made exponentially more stable. We then propose self-correction functions, which rely on expert knowledge (e.g. the laws of physics programmed in a simulator), and aim to approximate the idealized corrector automatically and at scale. We empirically validate the effectiveness of self-correcting self-consuming loops on the challenging human motion synthesis task, and observe that it successfully avoids model collapse, even when the ratio of synthetic data to real data is as high as 100%.

## Submission history

From: Nate Gillman \[
[view email](/show-email/901041fe/2402.07087)\]

**[\[v1\]](/abs/2402.07087v1)**Sun, 11 Feb 2024 02:34:42 UTC (11,149 KB)

**[\[v2\]](/abs/2402.07087v2)**Fri, 5 Apr 2024 15:42:13 UTC (13,171 KB)

**\[v3\]**Mon, 10 Jun 2024 14:22:45 UTC (10,377 KB)

### Additional Features

### Current browse context:

cs.LG

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

---


## Research Cycle — 2026-11-07 22:35 UTC

**Topic:** self-correction-loops  
**Focus:** Reflexion, self-consistency, bounded iterations

### Self-Correcting Self-Consuming Loops for Generative Model Training
**arXiv:** [2402.07087](https://arxiv.org/abs/2402.07087)  
**Authors:** Nate Gillman, Michael Freeman, Daksh Aggarwal, Chia-Hong Hsu, Calvin Luo, Yonglong Tian, Chen Sun  
**Published:** 2024-02-11  
**Categories:** cs.LG, cs.AI, cs.CV, stat.ML  

**Abstract:**
As synthetic data becomes higher quality and proliferates on the internet, machine learning models are increasingly trained on a mix of human- and machine-generated data. Despite the successful stories of using synthetic data for representation learning, using synthetic data for generative model training creates "self-consuming loops" which may lead to training instability or even collapse, unless certain conditions are met. Our paper aims to stabilize self-consuming generative model training. Our theoretical results demonstrate that by introducing an idealized correction function, which maps a data point to be more likely under the true data distribution, self-consuming loops can be made exponentially more stable. We then propose self-correction functions, which rely on expert knowledge (e.g. the laws of physics programmed in a simulator), and aim to approximate the idealized corrector automatically and at scale. We empirically validate the effectiveness of self-correcting self-consuming loops on the challenging human motion synthesis task, and observe that it successfully avoids model collapse, even when the ratio of synthetic data to real data is as high as 100%.

---

### Self-Correcting Self-Consuming Loops for Generative Model Training
**arXiv:** [2402.07087v2](https://arxiv.org/abs/2402.07087v2)  
**Authors:** Nate Gillman, Michael Freeman, Daksh Aggarwal, Chia-Hong Hsu, Calvin Luo, Yonglong Tian, Chen Sun  
**Published:** 2024-02-11  
**Categories:** cs.LG, cs.AI, cs.CV, stat.ML  

**Abstract:**
As synthetic data becomes higher quality and proliferates on the internet, machine learning models are increasingly trained on a mix of human- and machine-generated data. Despite the successful stories of using synthetic data for representation learning, using synthetic data for generative model training creates "self-consuming loops" which may lead to training instability or even collapse, unless certain conditions are met. Our paper aims to stabilize self-consuming generative model training. Our theoretical results demonstrate that by introducing an idealized correction function, which maps a data point to be more likely under the true data distribution, self-consuming loops can be made exponentially more stable. We then propose self-correction functions, which rely on expert knowledge (e.g. the laws of physics programmed in a simulator), and aim to approximate the idealized corrector automatically and at scale. We empirically validate the effectiveness of self-correcting self-consuming loops on the challenging human motion synthesis task, and observe that it successfully avoids model collapse, even when the ratio of synthetic data to real data is as high as 100%.

---

### CyberCorrect: A Cybernetic Framework for Closed-Loop Self-Correction in Large Language Models
**arXiv:** [2605.17305v1](https://arxiv.org/abs/2605.17305v1)  
**Authors:** Yuning Wu, Yingmin Liu, Yang Shu  
**Published:** 2026-05-17  
**Categories:** cs.AI, cs.CL  

**Abstract:**
Large language model (LLM) self-correction -- the ability to detect and fix errors in generated outputs -- remains largely ad hoc, relying on generic prompts such as "please reconsider your answer" without systematic error analysis or convergence guarantees. We propose CyberCorrect, a framework that formalizes LLM self-correction as a closed-loop control system grounded in cybernetic theory. The framework models the LLM generator as the plant and introduces a tri-modal Error Detector (combining self-consistency, verbalized confidence, and logic-chain verification) as the sensor. A type-directed Correction Controller generates targeted repair instructions based on diagnosed error categories, while a Convergence Judge determines iteration termination using stability criteria adapted from control theory. We further introduce three control-theoretic evaluation metrics -- convergence rate, overshoot rate, and oscillation rate -- that capture correction dynamics beyond final accuracy. Experiments on our constructed CyberCorrect-Bench (440 reasoning tasks with annotated error types and correction paths) show that CyberCorrect achieves 79.8% final accuracy, improving upon the best existing self-correction method by 6.2 percentage points, while reducing overshoot (erroneous over-correction) by 41% through its convergence control mechanism.

---


## Research Cycle — 2026-11-08 03:01 UTC

**Topic:** self-correction-loops  
**Focus:** Reflexion, self-consistency, bounded iterations

### Self-Correcting Self-Consuming Loops for Generative Model Training
**arXiv:** [2402.07087](https://arxiv.org/abs/2402.07087)  
**Authors:** Nate Gillman, Michael Freeman, Daksh Aggarwal, Chia-Hong Hsu, Calvin Luo, Yonglong Tian, Chen Sun  
**Published:** 2024-02-11  
**Categories:** cs.LG, cs.AI, cs.CV, stat.ML  

**Abstract:**
As synthetic data becomes higher quality and proliferates on the internet, machine learning models are increasingly trained on a mix of human- and machine-generated data. Despite the successful stories of using synthetic data for representation learning, using synthetic data for generative model training creates "self-consuming loops" which may lead to training instability or even collapse, unless certain conditions are met. Our paper aims to stabilize self-consuming generative model training. Our theoretical results demonstrate that by introducing an idealized correction function, which maps a data point to be more likely under the true data distribution, self-consuming loops can be made exponentially more stable. We then propose self-correction functions, which rely on expert knowledge (e.g. the laws of physics programmed in a simulator), and aim to approximate the idealized corrector automatically and at scale. We empirically validate the effectiveness of self-correcting self-consuming loops on the challenging human motion synthesis task, and observe that it successfully avoids model collapse, even when the ratio of synthetic data to real data is as high as 100%.

---

### Self-Correcting Self-Consuming Loops for Generative Model Training
**arXiv:** [2402.07087v2](https://arxiv.org/abs/2402.07087v2)  
**Authors:** Nate Gillman, Michael Freeman, Daksh Aggarwal, Chia-Hong Hsu, Calvin Luo, Yonglong Tian, Chen Sun  
**Published:** 2024-02-11  
**Categories:** cs.LG, cs.AI, cs.CV, stat.ML  

**Abstract:**
As synthetic data becomes higher quality and proliferates on the internet, machine learning models are increasingly trained on a mix of human- and machine-generated data. Despite the successful stories of using synthetic data for representation learning, using synthetic data for generative model training creates "self-consuming loops" which may lead to training instability or even collapse, unless certain conditions are met. Our paper aims to stabilize self-consuming generative model training. Our theoretical results demonstrate that by introducing an idealized correction function, which maps a data point to be more likely under the true data distribution, self-consuming loops can be made exponentially more stable. We then propose self-correction functions, which rely on expert knowledge (e.g. the laws of physics programmed in a simulator), and aim to approximate the idealized corrector automatically and at scale. We empirically validate the effectiveness of self-correcting self-consuming loops on the challenging human motion synthesis task, and observe that it successfully avoids model collapse, even when the ratio of synthetic data to real data is as high as 100%.

---

### Denoising Iterative Self-Correction: Structured Verification Loops for Reliable LLM Reasoning
**arXiv:** [2606.21724](https://arxiv.org/abs/2606.21724)  
**Authors:** Shen Yin, David Ken, Joel Stremmel  
**Published:** 2026-06-19  
**Categories:** cs.CL, cs.AI  

**Abstract:**
Large language models produce fluent but often incorrect multi-step reasoning, and naive correction methods risk degrading already-correct answers. We introduce Denoising Iterative Self-Correction (DISC), a test-time procedure that treats verification question outputs as noisy measurements of where a solution may be corrupted. Using these signals, DISC progressively reduces errors across multiple verify-judge-correct passes, analogous to traditional iterative denoising. A binary judgment gate controls correction precision by blocking rewrites that would damage already-correct answers while the verifier and corrector together repair errors. We evaluate this trade-off using two paired diagnostics: an improvement-to-degradation ratio (precision) and a repair rate (recall). Across three benchmarks (BIG-Bench Mistake, HotpotQA, GPQA Diamond) and four models, DISC dominates Chain-of-Verification and Self-Refine on the precision-recall trade-off, reaching 81.6% accuracy with 13x more improvements per degradation than Chain-of-Verification and 5x more than Self-Refine on BIG-Bench Mistake (Sonnet~4.5). On GPQA Diamond, we identify a capability floor below which judges acknowledge contradictions in evidence but cannot translate that recognition into a correction. We further show that cross-model role allocation -- assigning verification and judgment to a model different from the generator -- mitigates self-confirmation bias.

---


## Research Cycle — 2026-11-08 14:07 UTC

**Topic:** self-correction-loops  
**Focus:** Reflexion, self-consistency, bounded iterations

### Self-Correcting Self-Consuming Loops for Generative Model Training
**arXiv:** [2402.07087](https://arxiv.org/abs/2402.07087)  
**Authors:** Nate Gillman, Michael Freeman, Daksh Aggarwal, Chia-Hong Hsu, Calvin Luo, Yonglong Tian, Chen Sun  
**Published:** 2024-02-11  
**Categories:** cs.LG, cs.AI, cs.CV, stat.ML  

**Abstract:**
As synthetic data becomes higher quality and proliferates on the internet, machine learning models are increasingly trained on a mix of human- and machine-generated data. Despite the successful stories of using synthetic data for representation learning, using synthetic data for generative model training creates "self-consuming loops" which may lead to training instability or even collapse, unless certain conditions are met. Our paper aims to stabilize self-consuming generative model training. Our theoretical results demonstrate that by introducing an idealized correction function, which maps a data point to be more likely under the true data distribution, self-consuming loops can be made exponentially more stable. We then propose self-correction functions, which rely on expert knowledge (e.g. the laws of physics programmed in a simulator), and aim to approximate the idealized corrector automatically and at scale. We empirically validate the effectiveness of self-correcting self-consuming loops on the challenging human motion synthesis task, and observe that it successfully avoids model collapse, even when the ratio of synthetic data to real data is as high as 100%.

---

### Self-Correcting Self-Consuming Loops for Generative Model Training
**arXiv:** [2402.07087v2](https://arxiv.org/abs/2402.07087v2)  
**Authors:** Nate Gillman, Michael Freeman, Daksh Aggarwal, Chia-Hong Hsu, Calvin Luo, Yonglong Tian, Chen Sun  
**Published:** 2024-02-11  
**Categories:** cs.LG, cs.AI, cs.CV, stat.ML  

**Abstract:**
As synthetic data becomes higher quality and proliferates on the internet, machine learning models are increasingly trained on a mix of human- and machine-generated data. Despite the successful stories of using synthetic data for representation learning, using synthetic data for generative model training creates "self-consuming loops" which may lead to training instability or even collapse, unless certain conditions are met. Our paper aims to stabilize self-consuming generative model training. Our theoretical results demonstrate that by introducing an idealized correction function, which maps a data point to be more likely under the true data distribution, self-consuming loops can be made exponentially more stable. We then propose self-correction functions, which rely on expert knowledge (e.g. the laws of physics programmed in a simulator), and aim to approximate the idealized corrector automatically and at scale. We empirically validate the effectiveness of self-correcting self-consuming loops on the challenging human motion synthesis task, and observe that it successfully avoids model collapse, even when the ratio of synthetic data to real data is as high as 100%.

---

### Denoising Iterative Self-Correction: Structured Verification Loops for Reliable LLM Reasoning
**arXiv:** [2606.21724](https://arxiv.org/abs/2606.21724)  
**Authors:** Shen Yin, David Ken, Joel Stremmel  
**Published:** 2026-06-19  
**Categories:** cs.CL, cs.AI  

**Abstract:**
Large language models produce fluent but often incorrect multi-step reasoning, and naive correction methods risk degrading already-correct answers. We introduce Denoising Iterative Self-Correction (DISC), a test-time procedure that treats verification question outputs as noisy measurements of where a solution may be corrupted. Using these signals, DISC progressively reduces errors across multiple verify-judge-correct passes, analogous to traditional iterative denoising. A binary judgment gate controls correction precision by blocking rewrites that would damage already-correct answers while the verifier and corrector together repair errors. We evaluate this trade-off using two paired diagnostics: an improvement-to-degradation ratio (precision) and a repair rate (recall). Across three benchmarks (BIG-Bench Mistake, HotpotQA, GPQA Diamond) and four models, DISC dominates Chain-of-Verification and Self-Refine on the precision-recall trade-off, reaching 81.6% accuracy with 13x more improvements per degradation than Chain-of-Verification and 5x more than Self-Refine on BIG-Bench Mistake (Sonnet~4.5). On GPQA Diamond, we identify a capability floor below which judges acknowledge contradictions in evidence but cannot translate that recognition into a correction. We further show that cross-model role allocation -- assigning verification and judgment to a model different from the generator -- mitigates self-confirmation bias.

---


## Research Cycle — 2026-11-09 00:06 UTC

**Topic:** self-correction-loops  
**Focus:** Reflexion, self-consistency, bounded iterations

### Source: https://arxiv.org/abs/2604.23366 (FALLBACK FULL)

# Computer Science > Artificial Intelligence

\[Submitted on 25 Apr 2026\]

# Title:GSAR: Typed Grounding for Hallucination Detection and Recovery in Multi-Agent LLMs

[View PDF](/pdf/2604.23366)

[HTML (experimental)](https://arxiv.org/html/2604.23366v1)

Abstract:Autonomous multi-agent LLM systems are increasingly deployed to investigate operational incidents and produce structured diagnostic reports. Their trustworthiness hinges on whether each claim is grounded in observed evidence rather than model-internal inference. Existing groundedness evaluators (binary classifiers, LLM-as-judge scalars, self-correction loops) treat supporting evidence as interchangeable and emit a single signal that offers no principled control over downstream action.

We present GSAR, a grounding-evaluation and replanning framework that (i) partitions claims into a four-way typology (grounded, ungrounded, contradicted, complementary), giving first-class standing to non-redundant alternative perspectives; (ii) assigns evidence-type-specific weights reflecting epistemic strength; (iii) computes an asymmetric contradiction-penalised weighted groundedness score; and (iv) couples that score to a three-tier decision function (proceed, regenerate, replan) driving a bounded-iteration outer loop under an explicit compute budget.

We formalise the algorithm, prove six structural properties, and evaluate five design claims on FEVER with gold Wikipedia evidence under four independently-trained LLM judges (gpt-5.4, claude-sonnet-4-6, claude-opus-4-7, gemini-2.5-pro). Every ablation reproduces in the same direction on every judge: bootstrap 95% CIs on the rho=0 effect exclude 0 on all four; the no-complementary ablation under Opus 4.7 has CI \[-96,-68\] of 200; at n=1000 three independent judges converge to DeltaS(rho=0)=+0.058. A head-to-head against Vectara HHEM-2.1-Open is included. To our knowledge, GSAR is the first published groundedness framework coupling evidence-typed scoring with tiered recovery under an explicit compute budget.

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

### Source: https://arxiv.org/abs/2402.07087 (FALLBACK FULL)

# Computer Science > Machine Learning

\[Submitted on 11 Feb 2024 ([v1](https://arxiv.org/abs/2402.07087v1)), last revised 10 Jun 2024 (this version, v3)\]

# Title:Self-Correcting Self-Consuming Loops for Generative Model Training

[View PDF](/pdf/2402.07087)

[HTML (experimental)](https://arxiv.org/html/2402.07087v3)

Abstract:As synthetic data becomes higher quality and proliferates on the internet, machine learning models are increasingly trained on a mix of human- and machine-generated data. Despite the successful stories of using synthetic data for representation learning, using synthetic data for generative model training creates "self-consuming loops" which may lead to training instability or even collapse, unless certain conditions are met. Our paper aims to stabilize self-consuming generative model training. Our theoretical results demonstrate that by introducing an idealized correction function, which maps a data point to be more likely under the true data distribution, self-consuming loops can be made exponentially more stable. We then propose self-correction functions, which rely on expert knowledge (e.g. the laws of physics programmed in a simulator), and aim to approximate the idealized corrector automatically and at scale. We empirically validate the effectiveness of self-correcting self-consuming loops on the challenging human motion synthesis task, and observe that it successfully avoids model collapse, even when the ratio of synthetic data to real data is as high as 100%.

## Submission history

From: Nate Gillman \[
[view email](/show-email/901041fe/2402.07087)\]

**[\[v1\]](/abs/2402.07087v1)**Sun, 11 Feb 2024 02:34:42 UTC (11,149 KB)

**[\[v2\]](/abs/2402.07087v2)**Fri, 5 Apr 2024 15:42:13 UTC (13,171 KB)

**\[v3\]**Mon, 10 Jun 2024 14:22:45 UTC (10,377 KB)

### Additional Features

### Current browse context:

cs.LG

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

---

### Self-Generated Error Training for Token Editing in Diffusion Language Models
**arXiv:** [2606.17175v1](https://arxiv.org/abs/2606.17175v1)  
**Authors:** Lin Yao  
**Published:** 2026-06-15  
**Categories:** cs.CL  

**Abstract:**
Token-to-token (T2T) editing lets LLaDA2.1 revise committed tokens during block-diffusion decoding. The released recipe trains this editor on random vocabulary corruptions, but at inference the editor sees the model's own fluent, high-confidence draft errors instead. We study this training-inference mismatch and propose self-generated T2T, which performs a no-gradient draft pass, fills masked positions with predicted tokens, and supervises recovery in a second pass under these self-generated corruptions. We implement the update as a short LoRA continued-pretraining pass on LLaDA2.1-mini and evaluate on several benchmarks under the official Q-Mode T2T procedure with unchanged inference parameters. The method generally improves accuracy while reducing T2T edit intensity, mitigating failure modes such as final-digit transcription errors after otherwise correct reasoning and excessive self-correction before short factual answers.

---


## Research Cycle — 2026-11-09 12:05 UTC

**Topic:** self-correction-loops  
**Focus:** Reflexion, self-consistency, bounded iterations

### Self-Correcting Self-Consuming Loops for Generative Model Training
**arXiv:** [2402.07087](https://arxiv.org/abs/2402.07087)  
**Authors:** Nate Gillman, Michael Freeman, Daksh Aggarwal, Chia-Hong Hsu, Calvin Luo, Yonglong Tian, Chen Sun  
**Published:** 2024-02-11  
**Categories:** cs.LG, cs.AI, cs.CV, stat.ML  

**Abstract:**
As synthetic data becomes higher quality and proliferates on the internet, machine learning models are increasingly trained on a mix of human- and machine-generated data. Despite the successful stories of using synthetic data for representation learning, using synthetic data for generative model training creates "self-consuming loops" which may lead to training instability or even collapse, unless certain conditions are met. Our paper aims to stabilize self-consuming generative model training. Our theoretical results demonstrate that by introducing an idealized correction function, which maps a data point to be more likely under the true data distribution, self-consuming loops can be made exponentially more stable. We then propose self-correction functions, which rely on expert knowledge (e.g. the laws of physics programmed in a simulator), and aim to approximate the idealized corrector automatically and at scale. We empirically validate the effectiveness of self-correcting self-consuming loops on the challenging human motion synthesis task, and observe that it successfully avoids model collapse, even when the ratio of synthetic data to real data is as high as 100%.

---

### Self-Correcting Self-Consuming Loops for Generative Model Training
**arXiv:** [2402.07087v2](https://arxiv.org/abs/2402.07087v2)  
**Authors:** Nate Gillman, Michael Freeman, Daksh Aggarwal, Chia-Hong Hsu, Calvin Luo, Yonglong Tian, Chen Sun  
**Published:** 2024-02-11  
**Categories:** cs.LG, cs.AI, cs.CV, stat.ML  

**Abstract:**
As synthetic data becomes higher quality and proliferates on the internet, machine learning models are increasingly trained on a mix of human- and machine-generated data. Despite the successful stories of using synthetic data for representation learning, using synthetic data for generative model training creates "self-consuming loops" which may lead to training instability or even collapse, unless certain conditions are met. Our paper aims to stabilize self-consuming generative model training. Our theoretical results demonstrate that by introducing an idealized correction function, which maps a data point to be more likely under the true data distribution, self-consuming loops can be made exponentially more stable. We then propose self-correction functions, which rely on expert knowledge (e.g. the laws of physics programmed in a simulator), and aim to approximate the idealized corrector automatically and at scale. We empirically validate the effectiveness of self-correcting self-consuming loops on the challenging human motion synthesis task, and observe that it successfully avoids model collapse, even when the ratio of synthetic data to real data is as high as 100%.

---

### Denoising Iterative Self-Correction: Structured Verification Loops for Reliable LLM Reasoning
**arXiv:** [2606.21724](https://arxiv.org/abs/2606.21724)  
**Authors:** Shen Yin, David Ken, Joel Stremmel  
**Published:** 2026-06-19  
**Categories:** cs.CL, cs.AI  

**Abstract:**
Large language models produce fluent but often incorrect multi-step reasoning, and naive correction methods risk degrading already-correct answers. We introduce Denoising Iterative Self-Correction (DISC), a test-time procedure that treats verification question outputs as noisy measurements of where a solution may be corrupted. Using these signals, DISC progressively reduces errors across multiple verify-judge-correct passes, analogous to traditional iterative denoising. A binary judgment gate controls correction precision by blocking rewrites that would damage already-correct answers while the verifier and corrector together repair errors. We evaluate this trade-off using two paired diagnostics: an improvement-to-degradation ratio (precision) and a repair rate (recall). Across three benchmarks (BIG-Bench Mistake, HotpotQA, GPQA Diamond) and four models, DISC dominates Chain-of-Verification and Self-Refine on the precision-recall trade-off, reaching 81.6% accuracy with 13x more improvements per degradation than Chain-of-Verification and 5x more than Self-Refine on BIG-Bench Mistake (Sonnet~4.5). On GPQA Diamond, we identify a capability floor below which judges acknowledge contradictions in evidence but cannot translate that recognition into a correction. We further show that cross-model role allocation -- assigning verification and judgment to a model different from the generator -- mitigates self-confirmation bias.

---


## Research Cycle — 2026-11-10 00:05 UTC

**Topic:** self-correction-loops  
**Focus:** Reflexion, self-consistency, bounded iterations

### Source: https://arxiv.org/abs/2402.07087 (FALLBACK FULL)

# Computer Science > Machine Learning

\[Submitted on 11 Feb 2024 ([v1](https://arxiv.org/abs/2402.07087v1)), last revised 10 Jun 2024 (this version, v3)\]

# Title:Self-Correcting Self-Consuming Loops for Generative Model Training

[View PDF](/pdf/2402.07087)

[HTML (experimental)](https://arxiv.org/html/2402.07087v3)

Abstract:As synthetic data becomes higher quality and proliferates on the internet, machine learning models are increasingly trained on a mix of human- and machine-generated data. Despite the successful stories of using synthetic data for representation learning, using synthetic data for generative model training creates "self-consuming loops" which may lead to training instability or even collapse, unless certain conditions are met. Our paper aims to stabilize self-consuming generative model training. Our theoretical results demonstrate that by introducing an idealized correction function, which maps a data point to be more likely under the true data distribution, self-consuming loops can be made exponentially more stable. We then propose self-correction functions, which rely on expert knowledge (e.g. the laws of physics programmed in a simulator), and aim to approximate the idealized corrector automatically and at scale. We empirically validate the effectiveness of self-correcting self-consuming loops on the challenging human motion synthesis task, and observe that it successfully avoids model collapse, even when the ratio of synthetic data to real data is as high as 100%.

## Submission history

From: Nate Gillman \[
[view email](/show-email/901041fe/2402.07087)\]

**[\[v1\]](/abs/2402.07087v1)**Sun, 11 Feb 2024 02:34:42 UTC (11,149 KB)

**[\[v2\]](/abs/2402.07087v2)**Fri, 5 Apr 2024 15:42:13 UTC (13,171 KB)

**\[v3\]**Mon, 10 Jun 2024 14:22:45 UTC (10,377 KB)

### Additional Features

### Current browse context:

cs.LG

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

---

### Source: https://arxiv.org/abs/2604.23366 (FALLBACK FULL)

# Computer Science > Artificial Intelligence

\[Submitted on 25 Apr 2026\]

# Title:GSAR: Typed Grounding for Hallucination Detection and Recovery in Multi-Agent LLMs

[View PDF](/pdf/2604.23366)

[HTML (experimental)](https://arxiv.org/html/2604.23366v1)

Abstract:Autonomous multi-agent LLM systems are increasingly deployed to investigate operational incidents and produce structured diagnostic reports. Their trustworthiness hinges on whether each claim is grounded in observed evidence rather than model-internal inference. Existing groundedness evaluators (binary classifiers, LLM-as-judge scalars, self-correction loops) treat supporting evidence as interchangeable and emit a single signal that offers no principled control over downstream action.

We present GSAR, a grounding-evaluation and replanning framework that (i) partitions claims into a four-way typology (grounded, ungrounded, contradicted, complementary), giving first-class standing to non-redundant alternative perspectives; (ii) assigns evidence-type-specific weights reflecting epistemic strength; (iii) computes an asymmetric contradiction-penalised weighted groundedness score; and (iv) couples that score to a three-tier decision function (proceed, regenerate, replan) driving a bounded-iteration outer loop under an explicit compute budget.

We formalise the algorithm, prove six structural properties, and evaluate five design claims on FEVER with gold Wikipedia evidence under four independently-trained LLM judges (gpt-5.4, claude-sonnet-4-6, claude-opus-4-7, gemini-2.5-pro). Every ablation reproduces in the same direction on every judge: bootstrap 95% CIs on the rho=0 effect exclude 0 on all four; the no-complementary ablation under Opus 4.7 has CI \[-96,-68\] of 200; at n=1000 three independent judges converge to DeltaS(rho=0)=+0.058. A head-to-head against Vectara HHEM-2.1-Open is included. To our knowledge, GSAR is the first published groundedness framework coupling evidence-typed scoring with tiered recovery under an explicit compute budget.

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

### Source: https://arxiv.org/html/2402.07087v2 (FALLBACK FULL)

### Web Summary: https://arxiv.org/html/2402.07087v2

[Local Qwen Summarizer Error: <urlopen error [Errno 113] No route to host>]

Fallback Raw Content:
# Self-Correcting Self-Consuming Loops for Generative Model Training

###### Abstract

As synthetic data becomes higher quality and proliferates on the internet, machine learning models are increasingly trained on a mix of human- and machine-generated data. Despite the successful stories of using synthetic data for representation learning, using synthetic data for generative model training creates “self-consuming loops” which may lead to training instability or even collapse, unless certain conditions are met. Our paper aims to stabilize self-consuming generative model training. Our theoretical results demonstrate that by introducing an idealized correction function, which maps a data point to be more likely under the true data distribution, self-consuming loops can be made exponentially more stable. We then propose self-correction functions, which rely on expert knowledge (e.g. the laws of physics programmed in a simulator), and aim to approximate the idealized corrector automatically and at scale. We empirically validate the effectiveness of self-correcting self-consuming loops on the challenging human motion synthesis task, and observe that it successfully avoids model collapse, even when the ratio of synthetic data to real data is as high as 100%.

###### Keywords:

Machine Learning, Generative Modeling, Self-Consuming Loops, Data Contamination, Deep Learning, Artificial Intelligence, Human Motion Synthesis
<sup>†</sup>

<sup>†</sup>affiliationnotice: \icmlDummy

## 1 Introduction

Generative models have been used to synthesize training data for various learning tasks, to varying degrees of success. For example, for the tasks of image classification and contrastive representation learning, recent work ([Azizi et al., 2023](#bib.bib2); [Tian et al., 2023](#bib.bib25)) finds that using data synthesized from generative models rivals using real data.
Unfortunately, there is a gloomier outlook when attempting to generalize this framework to generative model training.

On one hand, there is evidence to suggest that training a generative model with its own outputs in a self-consuming manner will lead to collapse ([Alemohammad et al., 2023](#bib.bib1)).
For example, after 50 iterations of self-consuming training, a human motion diffusion model ([Tevet et al., 2023](#bib.bib24)) collapses and fails to follow the text prompts or the laws of physics (see the two examples on the left of Figure [1](#S1.F1)).

On the other hand, evidence suggests that such a framework could avoid collapse, but only when a “moderate” amount of synthetic data is used ([Bertrand et al., 2024](#bib.bib3)).
Worse still, this self-consuming scenario might happen without us knowing, and without us being able to quantify how much synthetic data is being used during training, due to the wide spread of AI generated content on the internet.

Intuitively, model collapse might be delayed or avoided by incorporating higher quality human generated data ([Alemohammad et al., 2023](#bib.bib1)), or by manually fixing the “mistakes” in machine created data.
Considering the size of datasets used in practice ([Schuhmann et al., 2022](#bib.bib22)), neither of these options is a scalable solution.

In this paper, we aim to provide a theoretical analysis of how certain operations would avoid collapse in self-consuming loops, without any assumptions on the “moderateness” of synthetic data corruption.
We introduce the mathematical abstraction of a *self-correction operation*.
This operation maps synthesized data that are sampled from the generative model to data that are better representatives from the target probability distribution that the model is attempting to approximate.
Instead of training on a combination of real data and synthesized data, we propose training on a combination of real data and synthesized *and then self-corrected* data.
Note that injecting fresh human generated data can be viewed as a special case of this operation.

Our main theoretical findings (Theorem [4.3](#S4.Thmtheorem3)):

1. (1) 
The self-consuming model with self-correction is exponentially more stable than the self-consuming model without any self-correction.
2. (2) 
The self-correction procedure guarantees less unwanted variance during self-consuming model training.

In our theoretical study, we assume that correction is *ideal* in order to obtain rigorous performance guarantees.
In our empirical study, we evaluate whether the same conclusions hold for *noisy* self-correction functions. We propose to automate this “self-correction” process by relying on programmed expert knowledge rather than a human-in-the-loop, such that the function can be applied at scale. We focus on the human motion synthesis task ([Guo et al., 2022](#bib.bib5)), and implement the self-correction function with a physics simulator-based imitation model ([Luo et al., 2021](#bib.bib15)).
Our empirical results confirm that our theoretical findings hold in practice:

1. (1) 
As illustrated in Figure [1](#S1.F1),
the self-correcting self-consuming model generates higher-quality human motion than the one without any self-correction.
2. (2) 
The self-correction function allows self-consuming loops to avoid collapse even at a high synthetic data to real data ratio (e.g. 100%).

We will release all the code associated with this paper.

## 2 Related Work

### 2.1 Learning Representations with Synthetic Data

Real curated datasets are costly to obtain, so there has been much interest in generating synthetic data as training data for various vision tasks. [Azizi et al. (2023)](#bib.bib2) demonstrates that text-to-image diffusion models such as Imagen ([Saharia et al., 2022](#bib.bib20)) can generate synthetic examples that augment the ImageNet dataset for better image classification.
[He et al. (2023)](#bib.bib6) studies how synthetic data from text-to-image models, when used exclusively, can be used as training data for image recognition tasks.
Similarly, [Tian et al. (2023)](#bib.bib25) finds that using synthetic outputs from a text-to-image model results in contrastive models whose downstream performance rivals that of CLIP ([Radford et al., 2021](#bib.bib19)) on visual recognition tasks, including dense prediction.
And the work in [Jahanian et al. (2021)](#bib.bib9) explored methods for multi-view representation learning by using the latent space of the generative models to generate multiple “views” of the synthetic data.
The above works collectively provide evidence that *some* representation learning tasks, when trained on synthetic data from some *given* generative models, yield excellent results.

### 2.2 Training Generative Models on Synthetic Data

Another line of reseach investigates the use of synthetic data for training *generative* models.
[Shumailov et al. (2023)](#bib.bib23) and [Martínez et al. (2023)](#bib.bib16) show that the use of model generated content in generative model training results in model degradation, likely because self-consuming loops remove low-density areas from the estimated probability manifold.
[Alemohammad et al. (2023)](#bib.bib1) formalize three different kinds of self-consuming generative models: the fully synthetic loop, the synthetic augmentation loop, and the fresh data loop.
In all of these loops, they iteratively re-train the model from scratch for every new generation.
They find that the former two loops result in model degradation, and only for the latter one does diversity and quality not suffer between self-consuming iterations.

Another recent work ([Bertrand et al., 2024](#bib.bib3)) considers the problem of iteratively fine-tuning in the context of synthetic augmentation loops.
They find that self-consuming augmentation loops do not necessarily collapse, so long as the synthetic augmentation percentage is sufficiently low.
The authors use techniques from the field of performative stability ([Perdomo et al., 2020](#bib.bib18)) to prove the existence of a convergence phenomenon in the space of model parameters. Our paper differs from prior work as we conduct analysis on self-consuming generative model training when the synthetic data can be optionally corrected. The correction can be performed with a human-in-the-loop, or by incorporating learned or programmed expert knowledge, as explored for natural language ([Saunders et al., 2022](#bib.bib21); [Welleck et al., 2022](#bib.bib27); [Wu et al., 2023](#bib.bib28)) and human motion ([Yuan et al., 2023](#bib.bib30); [Xu et al., 2023](#bib.bib29)). We validate our theory with a practical self-correcting operation designed for the human motion synthesis task.

## 3 Overall Training Procedure

We describe our proposed procedure in concise language in Algorithm [1](#alg1), and we explain it in more detail here.
We train the zero’th generation from scratch on the ground truth dataset $\mathcal{D}_{\mathrm{real}}:=\{x_{i}\}_{i=1}^{n}$, and we stop training when the model is close to convergence.
For all the following generations, we fine-tune the previous generation’s latest checkpoint on a combination of the ground truth dataset $\mathcal{D}_{\mathrm{real}}$, as well as $\lfloor\lambda\cdot n\rfloor$ synthetic data points which are generated from the previous generation’s latest checkpoint, and then passed through the *correction function* $\pi_{\gamma}$.

The correction function $\pi_{\gamma}$ is parameterized by the *correction strength* $\gamma\in\mathbb{R}_{\geq 0}$, which controls how much influence the correction function has on the input data points towards increasing a given point’s likelihood with respect to the target distribution.
The other main hyperparameter $\lambda\in\mathbb{R}_{\geq 0}$ is the *synthetic augmentation percent*, and it controls the ratio of synthetic data to real data in each iteration of fine-tuning.
When $\gamma=0$, we recover iterative re-training with synthetic augmentation considered in ([Bertrand et al., 2024](#bib.bib3)).
And if we choose the synthetic augmentation percent to be $\lambda=0$, then each generation simply corresponds to fine-tuning the model on the same dataset that it was trained on initially.

We now use *iterative fine-tuning* interchangeably with the more general term self-consuming loop. We also consider a broader family of *correction functions*, which may assume knowing the true data distribution (thus “idealized”).

## 4 Theoretical Analysis

### 4.1 Preliminaries

We mostly follow the notation from ([Bertrand et al., 2024](#bib.bib3)), except for introducing the correction function $\pi_{\gamma}$.
Let us denote by $p_{\mathrm{data}}$ the ground truth probability distribution that we want to train a generative model to estimate.
Suppose we have some dataset $\mathcal{D}_{\mathrm{real}}=\{x_{i}\}_{i=1}^{n}$ sampled from $p_{\mathrm{data}}$.
We write $\hat{p}_{\mathrm{data}}=(1/n)\sum_{i=1}^{n}\delta_{x_{i}}$. More generally, we use a hat to denote the empirical distribution over finitely many samples from the corresponding distribution.

Suppose that we have a class of generative models parameterized by $\Theta\subset\mathbb{R}^{d}$. We denote by $p_{\theta}$ a probability distribution in this class with model parameters $\theta\in\Theta$. We define the optimal model parameters within this class to be

|  | $$ \theta^{\star}=\argmax_{\theta^{\prime}\in\Theta}\mathbb{E}_{x\sim p_{\mathrm{data}}}[\log p_{\theta^{\prime}}(x)], $$ |  | (1) | 

where we break ties by minimizing $\|\theta^{\star}\|$. Typically, such optimal parameters yield a model $p_{\theta^{\star}}$ which closely approximates the oracle ground truth distribution $p_{\mathrm{data}}$, but doesn’t equal it exactly; accordingly, we define the Wasserstein-2 distance between the distributions to be

|  | $$ \varepsilon:=d_{W}(p_{\theta^{\star}},p_{\mathrm{data}}). $$ |  | (2) | 

The model weights for the first generation are naturally defined according to the optimization

|  | $$ \theta_{0}^{n}:=\argmax_{\theta^{\prime}\in\Theta}[\mathbb{E}_{x\sim\hat{p}_{\mathrm{data}}}[\log p_{\theta^{\prime}}(x)]]. $$ |  | (3) | 

This corresponds to training on the finite subset $\mathcal{D}_{\mathrm{real}}$. Next, let us suppose that the model weights from generation $t$ are denoted $\theta_{t}^{n}$. We will formalize a procedure for updating these weights for the next generation to obtain $\theta_{t+1}^{n}$. For this, we need to define our correction function, and then we will use it to define the weight update.

###### Definition 4.1.

For any probability distribution, and for any $\gamma\in\mathbb{R}_{\geq 0}$, we define the *correction of strength $\gamma$* of distribution $p_{\theta}$ to be the distribution

|  | $$ \pi_{\gamma}p_{\theta}(x):=\frac{{p_{\theta}}(x)+\gamma p_{\theta^{\star}}(x)}{1+\gamma}, $$ |  | (4) | 

where $p_{\theta^{\star}}$ is defined in ([1](#S4.E1)).
For any augmentation percentage $\lambda\geq 0$, we define the *weight update* mapping to be

|  | $\displaystyle\pi_{\gamma}\mathcal{G}_{\lambda}^{n}(\theta)$ | $\displaystyle:=\localargmax_{\theta^{\prime}\in\Theta}\hat{\mathcal{H}}(\theta,\theta^{\prime})$ |  | (5) | 
|  |  | $\displaystyle:=\localargmax_{\theta^{\prime}\in\Theta}\Big[\mathbb{E}_{x\sim\hat{p}_{\mathrm{data}}}[\log p_{\theta^{\prime}}(x)]]$ |  |  | 
|  |  | $\displaystyle\qquad\qquad\qquad\,\,\,\,\,\,\,\,\,\,\,+\lambda\mathbb{E}_{x\sim{\widehat{\pi_{\gamma}p_{\theta}}}}[\log p_{\theta^{\prime}}(x)]\Big],$ |  |  | 

where $\hat{p}_{\mathrm{data}}$ and $\widehat{\pi_{\gamma}p_{\theta}}$ are empirical distributions of size $n$ and $\lfloor\lambda\cdot n\rfloor$ respectively.

To continue our discussion from before, our iterative weight update is defined as $\theta_{t+1}^{n}:=\pi_{\gamma}\mathcal{G}_{\lambda}^{n}(\theta_{t}^{n})$.

Note that we use an global maximization in ([3](#S4.E3)) when defining the initial parameters $\theta_{0}^{n}$, but we use a local maximization when computing our parameter update in ([5](#S4.E5)).
This difference is analogous to the differences between how model weights update during initial training, where parameter updates are more global, and during fine-tuning, where parameter updates are more local.

#### 4.1.1 Understanding the correction $\pi_{\gamma}p_{\theta}(x)$

For $\gamma=0$, the correction mapping in ([4](#S4.E4)) simplifies to $\pi_{0}p_{\theta}=p_{\theta}$, which is just the original distribution; this corresponds to no correction at all.
For $\gamma=1$, it is $\pi_{1}p_{\theta}=(p_{\theta}+p_{\theta^{\star}})/2$.
And for $\gamma=\infty$, it is $\pi_{\infty}p_{\theta}=p_{\theta^{\star}}$, which corresponds to the optimal distribution.
So as $\gamma$ increases from $0$ to $\infty$, the distribution $\pi_{\gamma}p_{\theta}$ has a likelihood profile that matches $p_{\theta}$ less, and $p_{\theta^{\star}}$ more.
As $p_{\theta^{\star}}$ is the optimal model in our generative model class, this means that as $\gamma$ increases from $0$ to $\infty$, we have that $\pi_{\gamma}p_{\theta}(x)$ is a PDF which better represents the target likelih

---


## Research Cycle — 2026-11-10 06:06 UTC

**Topic:** self-correction-loops  
**Focus:** Reflexion, self-consistency, bounded iterations

### Source: https://arxiv.org/abs/2604.23366 (FALLBACK FULL)

# Computer Science > Artificial Intelligence

\[Submitted on 25 Apr 2026\]

# Title:GSAR: Typed Grounding for Hallucination Detection and Recovery in Multi-Agent LLMs

[View PDF](/pdf/2604.23366)

[HTML (experimental)](https://arxiv.org/html/2604.23366v1)

Abstract:Autonomous multi-agent LLM systems are increasingly deployed to investigate operational incidents and produce structured diagnostic reports. Their trustworthiness hinges on whether each claim is grounded in observed evidence rather than model-internal inference. Existing groundedness evaluators (binary classifiers, LLM-as-judge scalars, self-correction loops) treat supporting evidence as interchangeable and emit a single signal that offers no principled control over downstream action.

We present GSAR, a grounding-evaluation and replanning framework that (i) partitions claims into a four-way typology (grounded, ungrounded, contradicted, complementary), giving first-class standing to non-redundant alternative perspectives; (ii) assigns evidence-type-specific weights reflecting epistemic strength; (iii) computes an asymmetric contradiction-penalised weighted groundedness score; and (iv) couples that score to a three-tier decision function (proceed, regenerate, replan) driving a bounded-iteration outer loop under an explicit compute budget.

We formalise the algorithm, prove six structural properties, and evaluate five design claims on FEVER with gold Wikipedia evidence under four independently-trained LLM judges (gpt-5.4, claude-sonnet-4-6, claude-opus-4-7, gemini-2.5-pro). Every ablation reproduces in the same direction on every judge: bootstrap 95% CIs on the rho=0 effect exclude 0 on all four; the no-complementary ablation under Opus 4.7 has CI \[-96,-68\] of 200; at n=1000 three independent judges converge to DeltaS(rho=0)=+0.058. A head-to-head against Vectara HHEM-2.1-Open is included. To our knowledge, GSAR is the first published groundedness framework coupling evidence-typed scoring with tiered recovery under an explicit compute budget.

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

### Source: https://arxiv.org/html/2503.06072v2 (FALLBACK FULL)

### Web Summary: https://arxiv.org/html/2503.06072v2

[Local Qwen Summarizer Error: <urlopen error [Errno 113] No route to host>]

Fallback Raw Content:
# Large Language Models Post-training: Surveying Techniques from Alignment to Reasoning

###### Abstract

The emergence of Large Language Models (LLMs) has fundamentally transformed natural language processing, making them indispensable across domains ranging from conversational systems to scientific exploration. However, their pre-trained architectures often reveal limitations in specialized contexts, including restricted reasoning capacities, ethical uncertainties, and suboptimal domain-specific performance. These challenges necessitate advanced post-training language models (PoLMs) to address these shortcomings, such as OpenAI-o1/o3 and DeepSeek-R1 (collectively known as Large Reasoning Models, or LRMs). This paper presents the first comprehensive survey of PoLMs, systematically tracing their evolution across five core paradigms: Fine-tuning, which enhances task-specific accuracy; Alignment, which ensures ethical coherence and alignment with human preferences; Reasoning, which advances multi-step inference despite challenges in reward design; Efficiency, which optimizes resource utilization amidst increasing complexity; and Integration and Adaptation, which extend capabilities across diverse modalities while addressing coherence issues. Charting progress from ChatGPT’s foundational alignment strategies to DeepSeek-R1’s innovative reasoning advancements, we illustrate how PoLMs leverage datasets to mitigate biases, deepen reasoning capabilities, and enhance domain adaptability. Our contributions include a pioneering synthesis of PoLM evolution, a structured taxonomy categorizing techniques and datasets, and a strategic agenda emphasizing the role of LRMs in improving reasoning proficiency and domain flexibility. As the first survey of its scope, this work consolidates recent PoLM advancements and establishes a rigorous intellectual framework for future research, fostering the development of LLMs that excel in precision, ethical robustness, and versatility across scientific and societal applications. Project Github:  [https://github.com/Mr-Tieguigui/LLM-Post-Training](https://github.com/Mr-Tieguigui/LLM-Post-Training).

<sup>3</sup>

<sup>3</sup>footnotetext: Latest Update: Mar., 2025.

*K*eywords Post-training, Large Language Model, Fine-Tuning, Alignment, Reasoning, Efficiency.

###### Contents

## 1 Introduction

Language models (LMs) \[[1](#bib.bib1), [2](#bib.bib2)\] represent sophisticated computational frameworks designed to model and generate human language. These models have revolutionized the field of natural language processing (NLP) \[[3](#bib.bib3)\] by enabling machines to understand, generate, and interact with human language in a manner that closely mimics human cognition. Unlike humans, who acquire language skills naturally through interaction and exposure to contextual environments, machines must undergo extensive, data-driven training to develop similar capabilities \[[4](#bib.bib4)\]. This presents a significant research challenge, as enabling machines to comprehend and generate human language, while engaging in natural, contextually appropriate dialogue, requires not only vast computational resources but also refined methodologies for model development \[[5](#bib.bib5), [6](#bib.bib6)\].

The emergence of Large Language Models (LLMs) such as GPT-3 \[[7](#bib.bib7)\], InstructGPT \[[8](#bib.bib8)\], and GPT-4 \[[9](#bib.bib9)\] has marked a transformative phase in the evolution of LMs. These models, distinguished by their extensive parameterization and advanced learning capabilities, are designed to capture complex linguistic structures, contextual relationships, and nuanced patterns within vast datasets. This enables LLMs not only to predict subsequent words but also to generate coherent, contextually relevant text across a wide range of tasks, including translation, question answering, and summarization. The development of LLMs has sparked significant academic interest \[[5](#bib.bib5), [6](#bib.bib6), [10](#bib.bib10)\], which can be divided into two main stages: pre-training and post-training.

Pre-training.  The concept of pre-training originates from transfer learning in computer vision (CV) tasks \[[10](#bib.bib10)\]. Its primary goal is to develop a general model using extensive datasets, which facilitates easy fine-tuning for various downstream applications. A significant advantage of pre-training is its ability to utilize any unlabeled text corpus, thereby providing an abundant source of training data. However, early static pre-training methods, such as Neural Network Language Models (NNLM) \[[11](#bib.bib11)\] and Word2vec \[[12](#bib.bib12)\], struggled to accommodate different textual semantic environments, prompting the development of dynamic pre-training techniques like BERT \[[2](#bib.bib2)\] and XLNet \[[13](#bib.bib13)\]. BERT effectively addressed the limitations of static methods by leveraging the transformer architecture and employing self-attention mechanisms on large-scale unlabeled datasets. This study established the “pre-training and fine-tuning” learning paradigm, inspiring numerous subsequent studies that introduced diverse architectures, including GPT-2 \[[14](#bib.bib14)\] and BART \[[15](#bib.bib15)\].

Post-training.  Post-training refers to the techniques and methodologies employed after a model has undergone pre-training, aiming to refine and adapt the model for specific tasks or user requirements. Following the release of GPT-3 \[[7](#bib.bib7)\], with its 175 billion parameters, the field of post-training experienced a significant surge in interest and innovation. Various approaches emerged to enhance model performance, including fine-tuning \[[16](#bib.bib16), [17](#bib.bib17)\], which adjusts model parameters using labeled datasets or specific task data; alignment strategies \[[18](#bib.bib18), [19](#bib.bib19), [20](#bib.bib20)\], which optimize models to better align with user preferences; knowledge adaptation techniques \[[21](#bib.bib21), [22](#bib.bib22)\], which enable models to incorporate domain-specific knowledge; and reasoning improvements \[[23](#bib.bib23), [24](#bib.bib24)\], which enhance a model’s ability to make logical inferences and decisions.
Collectively known as Post-training Language Models (PoLMs), these techniques have led to the development of models such as GPT-4 \[[9](#bib.bib9)\], LLaMA-3 \[[25](#bib.bib25)\], Gemini-2.0 \[[26](#bib.bib26)\], and Claude-3.5 \[[27](#bib.bib27)\], marking substantial progress in LLM capabilities. However, post-trained models often struggle to adapt to new tasks without retraining or significant parameter adjustments, making PTM development an area of active research.

As highlighted, pre-trained language models (PLMs) primarily aim to provide general knowledge and capabilities, while PoLMs focus on adapting these models to specific tasks and requirements. A notable example of this adaptation is the latest LLM, DeepSeek-R1 \[[28](#bib.bib28)\], which illustrates the evolution of PoLMs in enhancing reasoning abilities, aligning with user preferences, and improving adaptability across various domains \[[29](#bib.bib29)\]. Furthermore, the increasing availability of open-sourced LLMs (e.g., LLaMA \[[30](#bib.bib30)\], Gemma \[[31](#bib.bib31)\], and Nemotron \[[32](#bib.bib32)\]) and domain-specific large datasets (e.g., PromptSource \[[33](#bib.bib33)\] and Flan \[[34](#bib.bib34)\]) is driving a trend among academic researchers and industry practitioners to develop PoLMs. This trend underscores the growing recognition of the importance of tailored adaptations in the field of PoLMs.

In the existing literature, PLMs have been widely discussed and surveyed \[[10](#bib.bib10), [35](#bib.bib35), [36](#bib.bib36), [37](#bib.bib37)\], while PoLMs are seldom reviewed systematically. To advance these techniques, it is essential to thoroughly examine the existing body of research to identify key challenges, gaps, and opportunities for further refinement. This survey aims to fill this gap by providing a structured framework for the evolving research in post-training. As shown in Fig. [1](#S1.F1), it explores multiple stages of post-training, with a particular focus on those employed from ChatGPT to DeepSeek. These techniques encompass a wide range of methodologies, including fine-tuning, LLM alignment, reasoning enhancement, and efficiency improvements. The blue section of the figure specifically highlights the set of post-training methods applied by DeepSeek, emphasizing the innovative strategies that have contributed to its success in adapting to user preferences and domain-specific needs.

### 1.1 Major Contributions

This paper represents the first comprehensive survey on PoLMs, providing a thorough, structured exploration of the latest advancements in the field. While previous surveys have typically focused on specific aspects of LLM development, such as preference alignment \[[38](#bib.bib38)\], parameter-efficient fine-tuning \[[39](#bib.bib39)\], and foundational techniques of LLMs \[[40](#bib.bib40)\], they have largely concentrated on narrow subtopics. In contrast, this survey takes a holistic approach, providing a complete review of the core techniques commonly employed during post-training and systematically categorizing them. Additionally, we investigate the datasets and real-world applications integral to these methods, as illustrated in Fig. [2](#S1.F2), and identify open challenges and promising directions for future research. The main contributions of this survey are as follows:

- • 
Comprehensive Historical Synthesis. We provide the first in-depth synthesis of PoLMs, tracing their evolution from ChatGPT’s initial reinforcement learning from human feedback (RLHF) to DeepSeek-R1’s innovative cold-start RL approach. This synthesis covers key techniques (i.e., Fine-tuning, Alignment, Reasoning, Efficiency, and Integration and Adaptation), analyzing their development and associated challenges, such as computational complexity and ethical considerations. By presenting this progression as a cohesive narrative, enriched with essential references, we provide researchers with a comprehensive overview of the evolution of post-training in recent years, serving as a foundational resource for the field.
- • 
Structured Taxonomy and Framework. We introduce a structured taxonomy, depicted in Fig. [2](#S1.F2), classifying post-training methods into five distinct categories and organizing datasets into seven types while framing applications across professional, technical, and interactive domains. This framework clarifies the interrelationships and practical implications of these methods, offering a systematic perspective on their development. By providing well-defined categories and analytical insights, we improve accessibility and comprehension for both novices and experts, establishing a comprehensive guide for navigating the complexities of post-training research.
- • 
Future Directions. We highlight emerging trends, particularly the rise of Large Reasoning Models (LRMs) such as o1 \[[41](#bib.bib41)\] and DeepSeek-R1 \[[28](#bib.bib28)\], which harness large-scale reinforcement learning to push the boundaries of reasoning. We emphasize that ongoin advancements are crucial for further enhancing reasoning capabilities and domain adaptability. Our analysis identifies key challenges, including scalability constraints, ethical alignment risks, and multimodal integration obstacles. We propose research avenues such as adaptive RL frameworks and fairness-aware optimization. These directions aim to propel post-training forward, ensuring LLMs achieve heightened precision and trustworthiness to meet future demands.

### 1.2 Organization

This survey is systematically organized to comprehensively explore Post-training Language Models (PoLMs), spanning their historical evolution, methodologies, datasets, applications, and future trajectories. Section [2](#S2) provides a historical overview of PoLMs. Section [3](#S3) examines Fine-tuning, including Supervised Fine-Tuning (SFT) in Section [3.1](#S3.SS1) and Reinforcement Fine-Tuning (RFT) in Section [3.3](#S3.SS3). Section [4](#S4) addresses Alignment, covering Reinforcement Learning from Human Feedback (RLHF) in Section [4.1](#S4.SS1), Reinforcement Learning from AI Feedback (RLAIF) in Section [4.2](#S4.SS2), and Direct Preference Optimization (DPO) in Section [4.3](#S4.SS3). Section [5](#S5) focuses on Reasoning, with Self-Refinement Methods in Section [5.1](#S5.SS1) and Reinforcement Learning for Reasoning in Section [5.2](#S5.SS2). Section [6](#S6) surveys Efficiency-enhancing methods, including Model Compression in Section [6.1](#S6.SS1), Parameter-Efficient Fine-Tuning (PEFT) in Section [6.2](#S6.SS2), and Knowledge Distillation in Section [6.3](#S6.SS3). Section [7](#S7) investigates Integration and Adaptation, addressing multi-modal approaches, domain adaptation, and model merging. Section [8](#S8) reviews datasets used in post-training. Section [9](#S9) explores LLM applications. Section [10](#S10) evaluates open problems and future directions. Finally, Section [11](#S11) concludes with a summary and research outlook.

## 2 Overview

### 2.1 History of PoLMs

The advancement of LLMs constitutes a pivotal chapter in natural language processing (NLP), with post-training methods serving as critical catalysts in their evolution from generalized pre-trained architectures to specialized, task-adaptive systems. This section delineates the historical trajectory of Post-training Language Models (PoLMs), tracing their development from foundational pre-training milestones exemplified by BERT \[[2](#bib.bib2)\] and GPT \[[1](#bib.bib1)\] to the sophisticated post-training paradigms embodied in contemporary models such as o1 \[[41](#bib.bib41)\] and DeepSeek-R1 \[[28](#bib.bib28)\]. Illustrated in Fig. [3](#S2.F3), this progression reflects a shift from establishing broad linguistic competence to enhancing task-specific adaptation, ethical alignment, reasoning sophistication, and multi-modal integration, marking a transformative journey in LLM capabilities.

The inception of modern PoLMs history aligns with the pre-training revolution in 2018, heralded by the releases of BERT \[[2](#bib.bib2)\] and GPT \[[1](#bib.bib1)\], which redefined NLP benchmarks. BERT’s bidirectional autoencoding framework, leveraging transformer architecture and self-attention, excelled in capturing contextual interdependencies for tasks like question answering, while GPT’s autoregressive design prioritized generative coherence, setting a precedent for text generation. These models established the "pre-training and fine-tuning" paradigm, with subsequent refinements in 2019 via T5 \[[42](#bib.bib42)\], which unified diverse tasks under a text-to-text framework, fostering multi-task learning and laying a robust foundation for post-training advancements.

The landscape of PoLMs began to evolve subs

---

### Source: https://arxiv.org/html/2606.17175v1 (FALLBACK FULL)

### Web Summary: https://arxiv.org/html/2606.17175v1

[Local Qwen Summarizer Error: <urlopen error [Errno 113] No route to host>]

Fallback Raw Content:
# Self-Generated Error Training for Token Editing in Diffusion Language Models

###### Abstract

Token-to-token (T2T) editing lets LLaDA2.1 revise committed tokens during block-diffusion decoding. The released recipe trains this editor on random vocabulary corruptions, but at inference the editor sees the model’s own fluent, high-confidence draft errors instead. We study this training-inference mismatch and propose Self-Generated T2T, which performs a no-gradient draft pass, fills masked positions with predicted tokens, and supervises recovery in a second pass under these self-generated corruptions. We implement the update as a short LoRA continued-pretraining pass on LLaDA2.1-mini and evaluate on several benchmarks under the official Q-Mode T2T procedure with unchanged inference parameters. The method generally improves accuracy while reducing T2T edit intensity, mitigating failure modes such as final-digit transcription errors after otherwise correct reasoning and excessive self-correction before short factual answers.

## 1 Introduction

Diffusion language models generate text by denoising partially observed sequences rather than committing to a strictly left-to-right trajectory.
This gives them two attractive properties: they can update many positions in parallel, and they can revisit previous commitments.
LLaDA2.1 operationalizes the second property through token-to-token (T2T) editing \[[4](#bib.bib12)\].
Each block is decoded with standard mask-to-token (M2T) filling, followed by an editing phase in which visible tokens are re-scored and overwritten when a new candidate exceeds an editing threshold.
This edit path is central to LLaDA2.1’s quality-speed tradeoff: it allows the model to accept tokens earlier and repair them later.
It is also necessary because parallel denoising can commit multiple tokens under the same incomplete context: tokens predicted in the same step cannot condition on one another while the corresponding positions are still masked, so locally plausible commitments may become inconsistent after they are placed together.

The training recipe behind this editor is less aligned with deployment. During training, the T2T stream is constructed by selecting clean tokens, replacing them with random vocabulary tokens, and applying cross-entropy to recover the original tokens. During inference, the tokens that need editing are not random samples from the vocabulary. They are the model’s own earlier predictions: plausible numbers in a derivation, locally grammatical but wrong entities, premature answer tokens, or semantically related alternatives. These errors are harder than random corruptions because they are in-distribution as language and can actively steer the context.

This paper asks whether the T2T editor should be trained on the errors it will actually see. We propose Self-Generated T2T, a training-side alignment method for LLaDA2.1 T2T editing. Instead of generating visible corruptions entirely from a uniform vocabulary distribution, we first ask the current model to fill masked positions, then use those predicted tokens as visible inputs for a second supervised pass: incorrect predictions are trained as edits back to the clean tokens, while correct predictions are trained to remain unchanged. The training objective remains a supervised denoising objective; inference keeps the original LLaDA2.1 T2T procedure and official Q-Mode parameters unchanged. The only change is the source of T2T corruption.

We evaluate Self-Generated T2T on CMATH, TriviaQA, PIQA, and AIME 2025 under the official Q-Mode T2T inference protocol ([section 3.4](#S3.SS4)), changing only the checkpoint weights while keeping inference procedure and parameters fixed.
Table [2](#S4.T2) reports accuracy and generation traces on these four benchmarks.
On CMATH, TriviaQA, and PIQA, Ours improves accuracy while reducing T2T edit intensity; on AIME 2025 accuracy is unchanged at 9/30, but edits still drop from 130.2 to 86.0 per problem.
CMATH shows the largest gain (+5.47 accuracy points) even though average output length increases, consistent with better final numeric commitment rather than premature short answering.
This is a deliberately minimal LoRA CPT study on a convenience FineWeb subset ([section 3.3](#S3.SS3)), intended as a mechanism stress test rather than a fully optimized recipe.

Our contributions are:

- • 
We formulate a training-inference mismatch in LLaDA2.1 T2T editing: random-token training corruptions do not match structured model-generated inference errors.
- • 
We propose Self-Generated T2T, a two-pass continued-training objective that trains the native T2T editor on self-generated draft tokens without adding a detector, correction head, RL stage, or inference-time mechanism.
- • 
We provide a reproducible LoRA implementation on LLaDA2.1-mini with a convenience FineWeb-Edu CPT setup, including corruption parameters, loss weights, optimizer settings, and evaluation under the official Q-Mode T2T inference defaults.
- • 
We report results on four benchmarks under the same official inference procedure and parameters: CMATH (+5.47 accuracy points), TriviaQA, and PIQA improve with lower edit intensity, while AIME 2025 matches the base score but still needs fewer T2T edits.

## 2 Related Work

#### Discrete diffusion LMs and parallel commitment.

Discrete diffusion models extend denoising diffusion to categorical state spaces, with absorbing-mask corruption providing a natural bridge to masked language modeling \[[2](#bib.bib1)\].
Language-specific variants refine this view into practical text-generation objectives and architectures, including SEDD, MDLM, MD4, and RADD \[[13](#bib.bib2), [17](#bib.bib3), [19](#bib.bib4), [15](#bib.bib5)\].
Recent systems scale this family in different but related ways.
Some train large masked diffusion LMs directly, some initialize from autoregressive checkpoints and continue training them as diffusion LMs, and some change the decoding architecture through blockwise diffusion for higher throughput; representative examples include LLaDA, Dream, DiffuLLaMA, Mercury, BD3-LM, and LLaDA2.1 \[[14](#bib.bib6), [23](#bib.bib7), [7](#bib.bib8), [9](#bib.bib9), [1](#bib.bib10), [4](#bib.bib12)\].
The central advantage of these models is parallel denoising: multiple positions can be predicted before a strict left-to-right context is available, and recent analyses study the resulting tradeoff between speed, generation order, and quality \[[11](#bib.bib11)\].
The same advantage creates the revision problem studied in this paper.
Tokens predicted in the same parallel step share the same partially observed context, but they cannot condition on the other tokens being predicted in that step because those positions are still masked at prediction time.
As a result, the model can commit tokens that are individually plausible under the shared context but mutually inconsistent after they are placed together; they may disagree semantically, duplicate incompatible roles, or form locally plausible but globally invalid spans.
Once committed, these independently predicted tokens become visible context for later denoising steps, so a local conflict can propagate into subsequent predictions.
Thus, high-quality parallel denoising requires some mechanism for revising earlier commitments.

#### Editing and remasking mechanisms.

Existing revision mechanisms differ mainly in the action they take on a suspicious visible token.
LLaDA2.1 introduces token-to-token (T2T) editing: after standard mask-to-token (M2T) denoising, the model may overwrite an already visible token when a new candidate becomes sufficiently confident \[[4](#bib.bib12)\].
Remasking methods instead undo the commitment by resetting uncertain visible tokens to \[MASK\] and letting the M2T stream re-predict them; examples include inference-time remasking samplers, self-reflective remasking, and token-to-mask refinement \[[20](#bib.bib13), [8](#bib.bib14), [22](#bib.bib15)\].
Learned self-correction methods add still another axis: ProSeCo inserts explicit corrective refinement steps, while BackPlay trains a lightweight corrector on errors made by a frozen generator \[[18](#bib.bib16), [12](#bib.bib17)\].
These mechanisms address the same consequence of parallel commitment, but they intervene at different points: changing the inference action, adding a correction module, or adding a correction phase.
They are complementary to our work and could in principle be combined with it: a model trained on realistic editable-token distributions can still use replacement, remasking, or an additional correction module at inference.
To isolate the training-distribution effect, we deliberately use the simplest correction action in this paper.
We keep the native LLaDA2.1 token-to-token replacement action and inference algorithm fixed, and change only the training distribution of the native editor.

#### The T2T corruption mismatch.

The T2T editor in LLaDA2.1 is trained to recover clean tokens from randomly substituted visible tokens \[[4](#bib.bib12)\].
This is a convenient supervised objective, but it does not match the editable tokens encountered at inference.
At inference, the tokens that should be edited are themselves selected by earlier model predictions.
Because the editor was trained on random replacements, its estimate of which visible tokens are worth editing, and what they should be edited into, can be poorly calibrated for fluent model-generated errors.
Such errors are qualitatively different from uniformly sampled vocabulary tokens: they are context-dependent, semantically plausible, and can steer the surrounding context.
Recent remasking work notes the same mismatch and avoids replacement by moving suspicious tokens back to \[MASK\] \[[22](#bib.bib15)\].
Our response is orthogonal to the choice between replacement and remasking.
Whether a system ultimately edits a token or remasks it, the training distribution should expose the model to realistic model-generated errors; in this work we keep the native LLaDA2.1 replacement action and make its T2T training distribution closer to deployment.

#### Training on model-induced states.

A recurring way to reduce train-test mismatch is to train on states induced by the model itself, but the relevant state depends on the generation paradigm.
In autoregressive sequence modeling, scheduled sampling replaces some gold prefix tokens with samples from the model, exposing the next-token predictor to model-generated prefixes rather than only teacher-forced prefixes \[[3](#bib.bib18)\].
In imitation learning, DAgger rolls out the current policy, queries the expert on the states that policy actually visits, and aggregates those policy-induced states into the training set \[[16](#bib.bib19)\].
In diffusion models, self-conditioning uses the model’s own intermediate denoising prediction as an additional input for subsequent denoising, so training better matches the iterative structure used at sampling time \[[6](#bib.bib20)\].
These methods share a principle, but not a state space: autoregressive models induce prefixes, imitation policies induce sequential decision states, and diffusion denoisers induce intermediate estimates of the clean data.
For T2T editing in discrete diffusion LMs, the induced state is different again: a partially denoised token block containing visible draft tokens produced by earlier denoising steps, some of which are plausible but wrong.
LLaDA2.1 trains its editor on random token substitutions, whereas inference asks the editor to repair model-generated visible token errors.
Self-Generated T2T instantiates self-generated T2T training for this setting by using the model itself to create the corrupted visible tokens used for T2T supervision.

## 3 Method

### 3.1 Base LLaDA2.1 Training and Inference

#### Base LLaDA2.1 training.

For training, let $\mathbf{x}=(x_{1},\ldots,x_{n})$ be a clean sequence, where $i\in\{1,\ldots,n\}$ indexes token positions. A corrupted training input $\mathbf{z}$ contains three kinds of positions. Positions in $\mathcal{M}$ are mask-input positions filled with \[MASK\]. Positions in $\mathcal{W}$ are visible but wrong-token positions. Positions in $\mathcal{G}$ are visible ground-truth-token positions. The model reads the full corrupted input $\mathbf{z}$, including all mask, wrong-token, and ground-truth-token positions, and produces one token distribution per position:

|  | $$ (p_{1},\ldots,p_{n})=f_{\theta}(\mathbf{z}). $$ |  | (1) | 

For all supervised positions, the target is the clean token $x_{i}$. The three position types therefore correspond to

|  | $$ \mathcal{L}_{\mathrm{m2t}}=\sum_{i\in\mathcal{M}}\mathrm{CE}(p_{i},x_{i}),\quad\mathcal{L}_{\mathrm{edit}}=\sum_{i\in\mathcal{W}}\mathrm{CE}(p_{i},x_{i}),\quad\mathcal{L}_{\mathrm{clean}}=\sum_{i\in\mathcal{G}}\mathrm{CE}(p_{i},x_{i}). $$ |  | (2) | 

Starting from $\mathbf{x}$, LLaDA2.1 training constructs $\mathbf{z}$ by first sampling a mask ratio and replacing the corresponding positions with \[MASK\]. Among the remaining visible positions, a subset is then selected for token-level corruption and replaced by random vocabulary tokens different from the clean tokens. The uncorrupted visible positions keep their ground-truth tokens. M2T trains on the mask-input positions: given the full $\mathbf{z}$ as context, the model predicts the clean tokens at positions in $\mathcal{M}$, corresponding to $\mathcal{L}_{\mathrm{m2t}}$. T2T trains on the visible positions: wrong visible tokens in $\mathcal{W}$ should be edited back to the clean tokens, and already-correct visible tokens in $\mathcal{G}$ should be kept unchanged, corresponding to $\mathcal{L}_{\mathrm{edit}}+\mathcal{L}_{\mathrm{clean}}$.

#### LLaDA2.1 T2T inference.

At inference, the state $\mathbf{z}^{t}$ again contains mask-input and visible-input positions, but the visible tokens are produced by earlier model denoising steps rather than by random replacement. M2T fills selected mask-input positions according to confidence thresholds. T2T evaluates visible-input positions and replaces a current visible token when the model’s top candidate at that position exceeds the editing threshold and differs from the current token. Thus, base T2T exposes the editor to random-token visible corruptions during training, while inference-time T2T edits visible tokens generated by the model itself.

### 3.2 Self-Generated T2T

Self-Generated T2T keeps the target sequence, model architecture, and inference algorithm unchanged.
It changes only how the wrong visible tokens in $\mathcal{W}$ are constructed during training.
For each batch, we first run the current model without gradients on a masked input.
We then select a subset of masked positions and back-fill them with self-generated draft tokens from a no-gradient argmax pass, which may be correct or incorrect.
Incorrect drafts become wrong visible tokens in $\mathcal{W}$, while correct drafts become clean visible tok

---


## Research Cycle — 2026-11-10 18:07 UTC

**Topic:** self-correction-loops  
**Focus:** Reflexion, self-consistency, bounded iterations

### Source: https://arxiv.org/abs/2402.07087 (FALLBACK FULL)

# Computer Science > Machine Learning

\[Submitted on 11 Feb 2024 ([v1](https://arxiv.org/abs/2402.07087v1)), last revised 10 Jun 2024 (this version, v3)\]

# Title:Self-Correcting Self-Consuming Loops for Generative Model Training

[View PDF](/pdf/2402.07087)

[HTML (experimental)](https://arxiv.org/html/2402.07087v3)

Abstract:As synthetic data becomes higher quality and proliferates on the internet, machine learning models are increasingly trained on a mix of human- and machine-generated data. Despite the successful stories of using synthetic data for representation learning, using synthetic data for generative model training creates "self-consuming loops" which may lead to training instability or even collapse, unless certain conditions are met. Our paper aims to stabilize self-consuming generative model training. Our theoretical results demonstrate that by introducing an idealized correction function, which maps a data point to be more likely under the true data distribution, self-consuming loops can be made exponentially more stable. We then propose self-correction functions, which rely on expert knowledge (e.g. the laws of physics programmed in a simulator), and aim to approximate the idealized corrector automatically and at scale. We empirically validate the effectiveness of self-correcting self-consuming loops on the challenging human motion synthesis task, and observe that it successfully avoids model collapse, even when the ratio of synthetic data to real data is as high as 100%.

## Submission history

From: Nate Gillman \[
[view email](/show-email/901041fe/2402.07087)\]

**[\[v1\]](/abs/2402.07087v1)**Sun, 11 Feb 2024 02:34:42 UTC (11,149 KB)

**[\[v2\]](/abs/2402.07087v2)**Fri, 5 Apr 2024 15:42:13 UTC (13,171 KB)

**\[v3\]**Mon, 10 Jun 2024 14:22:45 UTC (10,377 KB)

### Additional Features

### Current browse context:

cs.LG

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

---

### Source: https://arxiv.org/html/2402.07087v2 (FALLBACK FULL)

### Web Summary: https://arxiv.org/html/2402.07087v2

[Local Qwen Summarizer Error: <urlopen error [Errno 113] No route to host>]

Fallback Raw Content:
# Self-Correcting Self-Consuming Loops for Generative Model Training

###### Abstract

As synthetic data becomes higher quality and proliferates on the internet, machine learning models are increasingly trained on a mix of human- and machine-generated data. Despite the successful stories of using synthetic data for representation learning, using synthetic data for generative model training creates “self-consuming loops” which may lead to training instability or even collapse, unless certain conditions are met. Our paper aims to stabilize self-consuming generative model training. Our theoretical results demonstrate that by introducing an idealized correction function, which maps a data point to be more likely under the true data distribution, self-consuming loops can be made exponentially more stable. We then propose self-correction functions, which rely on expert knowledge (e.g. the laws of physics programmed in a simulator), and aim to approximate the idealized corrector automatically and at scale. We empirically validate the effectiveness of self-correcting self-consuming loops on the challenging human motion synthesis task, and observe that it successfully avoids model collapse, even when the ratio of synthetic data to real data is as high as 100%.

###### Keywords:

Machine Learning, Generative Modeling, Self-Consuming Loops, Data Contamination, Deep Learning, Artificial Intelligence, Human Motion Synthesis
<sup>†</sup>

<sup>†</sup>affiliationnotice: \icmlDummy

## 1 Introduction

Generative models have been used to synthesize training data for various learning tasks, to varying degrees of success. For example, for the tasks of image classification and contrastive representation learning, recent work ([Azizi et al., 2023](#bib.bib2); [Tian et al., 2023](#bib.bib25)) finds that using data synthesized from generative models rivals using real data.
Unfortunately, there is a gloomier outlook when attempting to generalize this framework to generative model training.

On one hand, there is evidence to suggest that training a generative model with its own outputs in a self-consuming manner will lead to collapse ([Alemohammad et al., 2023](#bib.bib1)).
For example, after 50 iterations of self-consuming training, a human motion diffusion model ([Tevet et al., 2023](#bib.bib24)) collapses and fails to follow the text prompts or the laws of physics (see the two examples on the left of Figure [1](#S1.F1)).

On the other hand, evidence suggests that such a framework could avoid collapse, but only when a “moderate” amount of synthetic data is used ([Bertrand et al., 2024](#bib.bib3)).
Worse still, this self-consuming scenario might happen without us knowing, and without us being able to quantify how much synthetic data is being used during training, due to the wide spread of AI generated content on the internet.

Intuitively, model collapse might be delayed or avoided by incorporating higher quality human generated data ([Alemohammad et al., 2023](#bib.bib1)), or by manually fixing the “mistakes” in machine created data.
Considering the size of datasets used in practice ([Schuhmann et al., 2022](#bib.bib22)), neither of these options is a scalable solution.

In this paper, we aim to provide a theoretical analysis of how certain operations would avoid collapse in self-consuming loops, without any assumptions on the “moderateness” of synthetic data corruption.
We introduce the mathematical abstraction of a *self-correction operation*.
This operation maps synthesized data that are sampled from the generative model to data that are better representatives from the target probability distribution that the model is attempting to approximate.
Instead of training on a combination of real data and synthesized data, we propose training on a combination of real data and synthesized *and then self-corrected* data.
Note that injecting fresh human generated data can be viewed as a special case of this operation.

Our main theoretical findings (Theorem [4.3](#S4.Thmtheorem3)):

1. (1) 
The self-consuming model with self-correction is exponentially more stable than the self-consuming model without any self-correction.
2. (2) 
The self-correction procedure guarantees less unwanted variance during self-consuming model training.

In our theoretical study, we assume that correction is *ideal* in order to obtain rigorous performance guarantees.
In our empirical study, we evaluate whether the same conclusions hold for *noisy* self-correction functions. We propose to automate this “self-correction” process by relying on programmed expert knowledge rather than a human-in-the-loop, such that the function can be applied at scale. We focus on the human motion synthesis task ([Guo et al., 2022](#bib.bib5)), and implement the self-correction function with a physics simulator-based imitation model ([Luo et al., 2021](#bib.bib15)).
Our empirical results confirm that our theoretical findings hold in practice:

1. (1) 
As illustrated in Figure [1](#S1.F1),
the self-correcting self-consuming model generates higher-quality human motion than the one without any self-correction.
2. (2) 
The self-correction function allows self-consuming loops to avoid collapse even at a high synthetic data to real data ratio (e.g. 100%).

We will release all the code associated with this paper.

## 2 Related Work

### 2.1 Learning Representations with Synthetic Data

Real curated datasets are costly to obtain, so there has been much interest in generating synthetic data as training data for various vision tasks. [Azizi et al. (2023)](#bib.bib2) demonstrates that text-to-image diffusion models such as Imagen ([Saharia et al., 2022](#bib.bib20)) can generate synthetic examples that augment the ImageNet dataset for better image classification.
[He et al. (2023)](#bib.bib6) studies how synthetic data from text-to-image models, when used exclusively, can be used as training data for image recognition tasks.
Similarly, [Tian et al. (2023)](#bib.bib25) finds that using synthetic outputs from a text-to-image model results in contrastive models whose downstream performance rivals that of CLIP ([Radford et al., 2021](#bib.bib19)) on visual recognition tasks, including dense prediction.
And the work in [Jahanian et al. (2021)](#bib.bib9) explored methods for multi-view representation learning by using the latent space of the generative models to generate multiple “views” of the synthetic data.
The above works collectively provide evidence that *some* representation learning tasks, when trained on synthetic data from some *given* generative models, yield excellent results.

### 2.2 Training Generative Models on Synthetic Data

Another line of reseach investigates the use of synthetic data for training *generative* models.
[Shumailov et al. (2023)](#bib.bib23) and [Martínez et al. (2023)](#bib.bib16) show that the use of model generated content in generative model training results in model degradation, likely because self-consuming loops remove low-density areas from the estimated probability manifold.
[Alemohammad et al. (2023)](#bib.bib1) formalize three different kinds of self-consuming generative models: the fully synthetic loop, the synthetic augmentation loop, and the fresh data loop.
In all of these loops, they iteratively re-train the model from scratch for every new generation.
They find that the former two loops result in model degradation, and only for the latter one does diversity and quality not suffer between self-consuming iterations.

Another recent work ([Bertrand et al., 2024](#bib.bib3)) considers the problem of iteratively fine-tuning in the context of synthetic augmentation loops.
They find that self-consuming augmentation loops do not necessarily collapse, so long as the synthetic augmentation percentage is sufficiently low.
The authors use techniques from the field of performative stability ([Perdomo et al., 2020](#bib.bib18)) to prove the existence of a convergence phenomenon in the space of model parameters. Our paper differs from prior work as we conduct analysis on self-consuming generative model training when the synthetic data can be optionally corrected. The correction can be performed with a human-in-the-loop, or by incorporating learned or programmed expert knowledge, as explored for natural language ([Saunders et al., 2022](#bib.bib21); [Welleck et al., 2022](#bib.bib27); [Wu et al., 2023](#bib.bib28)) and human motion ([Yuan et al., 2023](#bib.bib30); [Xu et al., 2023](#bib.bib29)). We validate our theory with a practical self-correcting operation designed for the human motion synthesis task.

## 3 Overall Training Procedure

We describe our proposed procedure in concise language in Algorithm [1](#alg1), and we explain it in more detail here.
We train the zero’th generation from scratch on the ground truth dataset $\mathcal{D}_{\mathrm{real}}:=\{x_{i}\}_{i=1}^{n}$, and we stop training when the model is close to convergence.
For all the following generations, we fine-tune the previous generation’s latest checkpoint on a combination of the ground truth dataset $\mathcal{D}_{\mathrm{real}}$, as well as $\lfloor\lambda\cdot n\rfloor$ synthetic data points which are generated from the previous generation’s latest checkpoint, and then passed through the *correction function* $\pi_{\gamma}$.

The correction function $\pi_{\gamma}$ is parameterized by the *correction strength* $\gamma\in\mathbb{R}_{\geq 0}$, which controls how much influence the correction function has on the input data points towards increasing a given point’s likelihood with respect to the target distribution.
The other main hyperparameter $\lambda\in\mathbb{R}_{\geq 0}$ is the *synthetic augmentation percent*, and it controls the ratio of synthetic data to real data in each iteration of fine-tuning.
When $\gamma=0$, we recover iterative re-training with synthetic augmentation considered in ([Bertrand et al., 2024](#bib.bib3)).
And if we choose the synthetic augmentation percent to be $\lambda=0$, then each generation simply corresponds to fine-tuning the model on the same dataset that it was trained on initially.

We now use *iterative fine-tuning* interchangeably with the more general term self-consuming loop. We also consider a broader family of *correction functions*, which may assume knowing the true data distribution (thus “idealized”).

## 4 Theoretical Analysis

### 4.1 Preliminaries

We mostly follow the notation from ([Bertrand et al., 2024](#bib.bib3)), except for introducing the correction function $\pi_{\gamma}$.
Let us denote by $p_{\mathrm{data}}$ the ground truth probability distribution that we want to train a generative model to estimate.
Suppose we have some dataset $\mathcal{D}_{\mathrm{real}}=\{x_{i}\}_{i=1}^{n}$ sampled from $p_{\mathrm{data}}$.
We write $\hat{p}_{\mathrm{data}}=(1/n)\sum_{i=1}^{n}\delta_{x_{i}}$. More generally, we use a hat to denote the empirical distribution over finitely many samples from the corresponding distribution.

Suppose that we have a class of generative models parameterized by $\Theta\subset\mathbb{R}^{d}$. We denote by $p_{\theta}$ a probability distribution in this class with model parameters $\theta\in\Theta$. We define the optimal model parameters within this class to be

|  | $$ \theta^{\star}=\argmax_{\theta^{\prime}\in\Theta}\mathbb{E}_{x\sim p_{\mathrm{data}}}[\log p_{\theta^{\prime}}(x)], $$ |  | (1) | 

where we break ties by minimizing $\|\theta^{\star}\|$. Typically, such optimal parameters yield a model $p_{\theta^{\star}}$ which closely approximates the oracle ground truth distribution $p_{\mathrm{data}}$, but doesn’t equal it exactly; accordingly, we define the Wasserstein-2 distance between the distributions to be

|  | $$ \varepsilon:=d_{W}(p_{\theta^{\star}},p_{\mathrm{data}}). $$ |  | (2) | 

The model weights for the first generation are naturally defined according to the optimization

|  | $$ \theta_{0}^{n}:=\argmax_{\theta^{\prime}\in\Theta}[\mathbb{E}_{x\sim\hat{p}_{\mathrm{data}}}[\log p_{\theta^{\prime}}(x)]]. $$ |  | (3) | 

This corresponds to training on the finite subset $\mathcal{D}_{\mathrm{real}}$. Next, let us suppose that the model weights from generation $t$ are denoted $\theta_{t}^{n}$. We will formalize a procedure for updating these weights for the next generation to obtain $\theta_{t+1}^{n}$. For this, we need to define our correction function, and then we will use it to define the weight update.

###### Definition 4.1.

For any probability distribution, and for any $\gamma\in\mathbb{R}_{\geq 0}$, we define the *correction of strength $\gamma$* of distribution $p_{\theta}$ to be the distribution

|  | $$ \pi_{\gamma}p_{\theta}(x):=\frac{{p_{\theta}}(x)+\gamma p_{\theta^{\star}}(x)}{1+\gamma}, $$ |  | (4) | 

where $p_{\theta^{\star}}$ is defined in ([1](#S4.E1)).
For any augmentation percentage $\lambda\geq 0$, we define the *weight update* mapping to be

|  | $\displaystyle\pi_{\gamma}\mathcal{G}_{\lambda}^{n}(\theta)$ | $\displaystyle:=\localargmax_{\theta^{\prime}\in\Theta}\hat{\mathcal{H}}(\theta,\theta^{\prime})$ |  | (5) | 
|  |  | $\displaystyle:=\localargmax_{\theta^{\prime}\in\Theta}\Big[\mathbb{E}_{x\sim\hat{p}_{\mathrm{data}}}[\log p_{\theta^{\prime}}(x)]]$ |  |  | 
|  |  | $\displaystyle\qquad\qquad\qquad\,\,\,\,\,\,\,\,\,\,\,+\lambda\mathbb{E}_{x\sim{\widehat{\pi_{\gamma}p_{\theta}}}}[\log p_{\theta^{\prime}}(x)]\Big],$ |  |  | 

where $\hat{p}_{\mathrm{data}}$ and $\widehat{\pi_{\gamma}p_{\theta}}$ are empirical distributions of size $n$ and $\lfloor\lambda\cdot n\rfloor$ respectively.

To continue our discussion from before, our iterative weight update is defined as $\theta_{t+1}^{n}:=\pi_{\gamma}\mathcal{G}_{\lambda}^{n}(\theta_{t}^{n})$.

Note that we use an global maximization in ([3](#S4.E3)) when defining the initial parameters $\theta_{0}^{n}$, but we use a local maximization when computing our parameter update in ([5](#S4.E5)).
This difference is analogous to the differences between how model weights update during initial training, where parameter updates are more global, and during fine-tuning, where parameter updates are more local.

#### 4.1.1 Understanding the correction $\pi_{\gamma}p_{\theta}(x)$

For $\gamma=0$, the correction mapping in ([4](#S4.E4)) simplifies to $\pi_{0}p_{\theta}=p_{\theta}$, which is just the original distribution; this corresponds to no correction at all.
For $\gamma=1$, it is $\pi_{1}p_{\theta}=(p_{\theta}+p_{\theta^{\star}})/2$.
And for $\gamma=\infty$, it is $\pi_{\infty}p_{\theta}=p_{\theta^{\star}}$, which corresponds to the optimal distribution.
So as $\gamma$ increases from $0$ to $\infty$, the distribution $\pi_{\gamma}p_{\theta}$ has a likelihood profile that matches $p_{\theta}$ less, and $p_{\theta^{\star}}$ more.
As $p_{\theta^{\star}}$ is the optimal model in our generative model class, this means that as $\gamma$ increases from $0$ to $\infty$, we have that $\pi_{\gamma}p_{\theta}(x)$ is a PDF which better represents the target likelih

---

### Source: https://arxiv.org/html/2606.21724 (FALLBACK FULL)

### Web Summary: https://arxiv.org/html/2606.21724

[Local Qwen Summarizer Error: <urlopen error [Errno 113] No route to host>]

Fallback Raw Content:
# Denoising Iterative Self-Correction:

Structured Verification Loops for Reliable LLM Reasoning

###### Abstract

Large language models produce fluent but often incorrect multi-step reasoning, and naive correction methods risk degrading already-correct answers. We introduce Denoising Iterative Self-Correction (DISC), a test-time procedure that treats verification question outputs as noisy measurements of where a solution may be corrupted. Using these signals, DISC progressively reduces errors across multiple verify-judge-correct passes, analogous to traditional iterative denoising. A binary judgment gate controls correction precision by blocking rewrites that would damage already-correct answers while the verifier and corrector together repair errors. We evaluate this trade-off using two paired diagnostics: an improvement-to-degradation ratio (precision) and a repair rate (recall). Across three benchmarks (BIG-Bench Mistake, HotpotQA, GPQA Diamond) and four models, DISC dominates Chain-of-Verification and Self-Refine on the precision-recall trade-off, reaching 81.6% accuracy with $13\times$ more improvements per degradation than Chain-of-Verification and $5\times$ more than Self-Refine on BIG-Bench Mistake (Sonnet 4.5). On GPQA Diamond, we identify a capability floor below which judges acknowledge contradictions in evidence but cannot translate that recognition into a correction. We further show that cross-model role allocation—assigning verification and judgment to a model different from the generator—mitigates self-confirmation bias.


## 1 Introduction

Large language models increasingly operate in settings that demand correctness, such as decision support, analytics, deep research, trend analysis, and professional drafting. Yet LLM outputs frequently contain errors, particularly in tasks requiring multi-step transformations or multi-hop evidence aggregation ([Tyen et al., 2024](#bib.bib11); [Huang et al., 2024](#bib.bib2)). A single arithmetic mistake in step three of a ten-step derivation can invalidate the entire reasoning chain; a missed qualifier in multi-hop question answering can lead to a confidently stated wrong answer.

Several broad paradigms address this reliability gap. Prompting-based approaches such as chain-of-thought ([Wei et al., 2022](#bib.bib3)) elicit step-by-step reasoning that improves accuracy but does not necessarily detect and correct mistakes. Sampling and selection methods, such as self-consistency ([Wang et al., 2023](#bib.bib4)), generate multiple independent solutions and select among them by majority vote. Test-time correction methods attempt to improve a single initial answer through additional verification and revision passes. Training-based methods modify the model itself, through reinforcement learning ([Kumar et al., 2024](#bib.bib7)), reward model training ([Ouyang et al., 2022](#bib.bib12)), or alignment objectives ([Rafailov et al., 2023](#bib.bib16)).

This paper focuses on test-time correction. A critical but underreported requirement for any correction procedure is that it should not frequently degrade correct answers. A method that repairs 10 errors but introduces 8 new ones is unreliable , even when its net accuracy gain is positive. We therefore frame correction evaluation in standard classification terms: each correction attempt is a decision about whether to change an answer, and a method’s quality is jointly determined by its precision (the ratio of helpful corrections to harmful ones) and its recall (what fraction of fixable errors it actually fixes). We operationalize these as the improvement-to-degradation ratio ($I{:}D$) and the repair rate, the latter being the single-sample empirical form of the Critique Score of [Yang et al. (2025)](#bib.bib5); we report them as paired quantities throughout, with formal definitions in Section [4.3](#S4.SS3). While prior work has surfaced degradation as a distinct concern ([Huang et al., 2024](#bib.bib2); [Yang et al., 2025](#bib.bib5)), accuracy and net change remain the most common headline metrics in the self-correction literature ([Madaan et al., 2023](#bib.bib8); [Gou et al., 2024](#bib.bib9)).

Our work is motivated by a simple observation: verification is noisy. A single round of checking may miss subtle failure modes, over-focus on irrelevant details, or hallucinate discrepancies that do not exist. We borrow intuition from iterative denoising in image restoration and diffusion models ([Ho et al., 2020](#bib.bib13); [Song and Ermon, 2019](#bib.bib14)), where each step removes a fraction of the noise while preserving signal that is consistent across passes. DISC treats verification outputs (questions, evidence, and judgments) as noisy measurements of where the current solution may be corrupted, and therefore repeats the verify-judge-correct procedure across multiple iterations to progressively reduce errors while preserving parts that remain consistent with the evidence.

DISC overview. DISC iterates a verify–judge–correct loop (Figure [1](#S1.F1); Section [3.2](#S3.SS2)) with an explicit judgment gate: when the judge finds no mistake, the loop terminates early and the answer is returned unchanged. Early termination is the common case (e.g., on GPQA Diamond cross-model at $K{=}3$, 79% of examples reach a no-mistake verdict and exit before exhausting the iteration budget). We show in Section [5.3](#S5.SS3.SSS0.Px1) that this gate functions as the system’s precision mechanism.

Contributions. (1) the DISC framework with an explicit judgment gate that serves as the system’s precision mechanism, separating mistake detection from correction and enabling early stopping and principled preservation of correct answers; (2) an evaluation spanning three benchmarks chosen for task diversity: algorithmic reasoning (BIG-Bench Mistake), multi-hop question answering (HotpotQA), and graduate-level science (GPQA Diamond); (3) cross-model configurations identifying self-confirmation bias as the primary obstacle to same-model self-correction and cross-model role allocation as an effective remedy; and (4) evidence of a minimum capability threshold below which models acknowledge contradictions in evidence but cannot translate that recognition into corrective action.

## 2 Related Work

Principal baselines. We compare DISC against Chain-of-Verification (CoVe) ([Dhuliawala et al., 2023](#bib.bib1)), which generates verification questions and answers to refine the initial response in a single pass, and Self-Refine ([Madaan et al., 2023](#bib.bib8)), in which a single LLM iteratively critiques and revises its output until a stopping criterion is met. Relative to CoVe, DISC adds a binary judgment gate before correction (avoiding unconditional revision) and iterates the verify-judge-correct process; relative to Self-Refine, it replaces holistic critique with factored verification questions answered separately.

Evaluation benchmarks. BIG-Bench Mistake (BBM) ([Tyen et al., 2024](#bib.bib11)) was constructed explicitly to test reasoning-error detection and correction: it contains pre-generated chain-of-thought traces with human-annotated first-mistake locations across five subtasks. We treat BBM as our primary correction benchmark and conduct our deepest analyses on it, including per-subtask results (Appendix [C](#A3)) and the judgment gate ablation (Section [5.3](#S5.SS3.SSS0.Px1)). We do not use BBM’s accompanying backtracking method as a baseline because it feeds ground-truth mistake locations to the model, making it an oracle rather than a self-correction baseline (see Section [4.2](#S4.SS2)). We complement BBM with HotpotQA and GPQA Diamond for multi-hop QA and graduate-level science.

Critical perspectives. [Huang et al. (2024)](#bib.bib2) and [Kamoi et al. (2024)](#bib.bib10) argue that intrinsic self-correction with same-model feedback rarely improves reasoning, locating the bottleneck in feedback generation. Our same-model and cross-model experiments test this position directly (Sections [5.1](#S5.SS1), [5.2](#S5.SS2.SSS0.Px1), [6.2](#S6.SS2)).

Verifier bottleneck. [Zhang et al. (2024)](#bib.bib6) propose that self-correction is “largely bottlenecked by the verifier rather than the refiner,” and that small language models benefit most from strong external verifiers. We investigate both claims directly through cross-model role allocation on GPQA (Section [5.2](#S5.SS2.SSS0.Px1) and Appendix [I](#A9)) and through the gate ablation, which further isolates the verifier-corrector loop’s contribution from the gate’s (Section [5.3](#S5.SS3.SSS0.Px1)).

Training-based and tool-augmented correction. SCoRe ([Kumar et al., 2024](#bib.bib7)) trains models for self-correction via multi-turn online RL; CRITIC ([Gou et al., 2024](#bib.bib9)) grounds verification in external tools (code interpreters, search). Both are complementary to DISC, which operates purely at test time with model-generated verification.

Confidence vs. critique. [Yang et al. (2025)](#bib.bib5) decompose self-correction into “confidence” (preserving correct answers) and “critique” (repairing incorrect ones), and report two within-class rates: Confidence Level (CL) and Critique Score (CS). Our repair rate is the single-sample empirical form of CS, and our framing of correction quality as preservation-plus-repair follows their decomposition directly. Our additions are (i) an improvement-to-degradation ratio (I:D) that combines preservation and repair into a single trade-off summary, and (ii) the systematic use of I:D and repair rate as a precision-recall lens for comparing correction methods (Yang et al. use CL/CS to characterize individual models). DISC’s judgment gate primarily affects I:D; its iteration loop primarily affects repair rate.

## 3 Method: Denoising Iterative Self-Correction

### 3.1 Problem Setting

Given an input $x$ (question, context, or task description) and a base language model $\mathcal{M}$, we produce an initial answer $y_{0}\sim\mathcal{M}(x)$. The goal is to obtain a refined answer $y_{K}$ after up to $K$ iterations that maximizes task accuracy while minimizing degradation, the probability that a correct $y_{0}$ becomes an incorrect $y_{K}$.

### 3.2 Pipeline

DISC iterates the verify–judge–correct loop given in Algorithm [1](#alg1). Four roles, generator $\mathcal{M}_{g}$, verifier $\mathcal{M}_{v}$, judge $\mathcal{M}_{j}$, and corrector $\mathcal{M}_{c}$, are applied in sequence for up to $K$ iterations, with early termination whenever the judge returns No\_Mistake.

The verifier produces a set of targeted questions probing specific claims or reasoning steps in $y_{t}$, then answers each independently. The judge requires a specific contradiction between $E_{t}$ and $y_{t}$ before flagging a mistake, prioritizing precision over recall to preserve already-correct answers; the accompanying rationale $r_{t}$ points to the offending evidence. The corrector treats the rationale as advisory, verifies that the flagged issue affects the final answer before rewriting, and leaves unflagged content unchanged. This evidence-conditioned design focuses revisions on identified errors rather than encouraging wholesale rewrites. Each iteration plays the role of one denoising step in the analogy, progressively reducing the remaining error.

Iteration budget. All main experiments use $K{=}3$. An ablation on GPQA Diamond (Section [5.3](#S5.SS3.SSS0.Px3)) finds that $K{=}1\to K{=}3$ produces large gains in net correction while $K{=}3$ onward plateaus; $K{=}3$ captures the bulk of available correction headroom at bounded per-example cost.

Cross-model configurations. The four roles need not share a backbone. Our experiments show that pairing a stronger verifier and judge with a weaker generator and corrector avoids self-confirmation bias while keeping generation costs low (Section [6.2](#S6.SS2)).

### 3.3 Prompt Design

Prompts assign roles, provide inputs, and specify output formats, without few-shot examples or chain-of-thought scaffolding. Full templates appear in Appendix [A](#A1). Beyond Algorithm [1](#alg1), the only design choice is that the verifier produces a small number of targeted questions (typically 3–10) and answers each one independently of the current answer $y_{t}$.

## 4 Experimental Setup

### 4.1 Benchmarks and Models

We evaluate DISC across three English-language benchmarks summarized in Table [2](#footnote2), spanning algorithmic reasoning, multi-hop question answering, and graduate-level science, using four models: Claude Sonnet 4.5, gpt-5.2, GPT-4o, and gpt-4.1-nano. BIG-Bench Mistake and HotpotQA use Sonnet 4.5 and GPT-4o; GPQA Diamond pairs gpt-4.1-nano and gpt-5.2. Built-in reasoning/thinking modes are disabled across all models, since DISC itself is the test-time correction mechanism under evaluation (Appendix [B](#A2)).

| Benchmark | N | Domain / Subtask | Answer Format | Task | 
|---|---|---|---|---|
| BIG-Bench Mistake | 300 | Tracking Shuffled Objects | Object name | Track items through swaps | 
|  | 300 | Logical Deduction | Letter | Order items by deduction | 
|  | 300 | Multistep Arithmetic | Integer | Evaluate arithmetic expression | 
|  | 300 | Word Sorting | Space-separated list | Sort words alphabetically | 
|  | 592 | Dyck Languages | Bracket string | Complete balanced delimiters | 
| GPQA Diamond | 198 | Graduate-level science (3 main domains) | Multiple choice (4-way) | Answer multiple-choice questions | 
| HotpotQA | 7,405 | Multi-hop QA over Wikipedia | Free text | Answer using supporting facts | 

<sup>2</sup>

<sup>2</sup>2 Per-method evaluation sizes can be slightly lower than the canonical totals when individual examples are blocked by API content-policy filters. Per-method effective sizes are reported in the per-task tables in Appendix

[C](#A3).

### 4.2 Baselines

Chain-of-Verification (CoVe) ([Dhuliawala et al., 2023](#bib.bib1)) and Self-Refine ([Madaan et al., 2023](#bib.bib8)) are used as baselines and are described in Section [2](#S2); we additionally report the uncorrected initial answer as a reference. For CoVe we use the *factored* variant, the best-performing CoVe variant on short-form QA tasks per [Dhuliawala et al. (2023)](#bib.bib1). For Self-Refine we use the prompt templates and stopping rule from the original implementation. DISC’s prompts are rule-based to express the judgment gate’s decision criteria, while CoVe’s are few-shot following its original implementation; the judgment gate is an architectural choice (CoVe has no analog). The CoVe authors demonstrated stronger performance than the popular chain-of-thought ([Wei et al., 2022](#bib.bib3)) reasoning method, perhaps the most natural correction approach for LLMs; hence, we omit a chain-of-thought baseline.

### 4.3 Metrics

We report accuracy (fraction of correct final answers) plus four correction-quality metrics computed against the initial answer: improvement ($I$, initially incorrect answers turned correct), degradation ($D$, initially correct

---


## Research Cycle — 2026-11-11 06:05 UTC

**Topic:** self-correction-loops  
**Focus:** Reflexion, self-consistency, bounded iterations

### Self-Correcting Self-Consuming Loops for Generative Model Training
**arXiv:** [2402.07087](https://arxiv.org/abs/2402.07087)  
**Authors:** Nate Gillman, Michael Freeman, Daksh Aggarwal, Chia-Hong Hsu, Calvin Luo, Yonglong Tian, Chen Sun  
**Published:** 2024-02-11  
**Categories:** cs.LG, cs.AI, cs.CV, stat.ML  

**Abstract:**
As synthetic data becomes higher quality and proliferates on the internet, machine learning models are increasingly trained on a mix of human- and machine-generated data. Despite the successful stories of using synthetic data for representation learning, using synthetic data for generative model training creates "self-consuming loops" which may lead to training instability or even collapse, unless certain conditions are met. Our paper aims to stabilize self-consuming generative model training. Our theoretical results demonstrate that by introducing an idealized correction function, which maps a data point to be more likely under the true data distribution, self-consuming loops can be made exponentially more stable. We then propose self-correction functions, which rely on expert knowledge (e.g. the laws of physics programmed in a simulator), and aim to approximate the idealized corrector automatically and at scale. We empirically validate the effectiveness of self-correcting self-consuming loops on the challenging human motion synthesis task, and observe that it successfully avoids model collapse, even when the ratio of synthetic data to real data is as high as 100%.

---

### GSAR: Typed Grounding for Hallucination Detection and Recovery in Multi-Agent LLMs
**arXiv:** [2604.23366](https://arxiv.org/abs/2604.23366)  
**Authors:** Federico A. Kamelhar  
**Published:** 2026-04-25  
**Categories:** cs.AI, cs.MA  

**Abstract:**
Autonomous multi-agent LLM systems are increasingly deployed to investigate operational incidents and produce structured diagnostic reports. Their trustworthiness hinges on whether each claim is grounded in observed evidence rather than model-internal inference. Existing groundedness evaluators (binary classifiers, LLM-as-judge scalars, self-correction loops) treat supporting evidence as interchangeable and emit a single signal that offers no principled control over downstream action.
  We present GSAR, a grounding-evaluation and replanning framework that (i) partitions claims into a four-way typology (grounded, ungrounded, contradicted, complementary), giving first-class standing to non-redundant alternative perspectives; (ii) assigns evidence-type-specific weights reflecting epistemic strength; (iii) computes an asymmetric contradiction-penalised weighted groundedness score; and (iv) couples that score to a three-tier decision function (proceed, regenerate, replan) driving a bounded-iteration outer loop under an explicit compute budget.
  We formalise the algorithm, prove six structural properties, and evaluate five design claims on FEVER with gold Wikipedia evidence under four independently-trained LLM judges (gpt-5.4, claude-sonnet-4-6, claude-opus-4-7, gemini-2.5-pro). Every ablation reproduces in the same direction on every judge: bootstrap 95% CIs on the rho=0 effect exclude 0 on all four; the no-complementary ablation under Opus 4.7 has CI [-96,-68] of 200; at n=1000 three independent judges converge to DeltaS(rho=0)=+0.058. A head-to-head against Vectara HHEM-2.1-Open is included. To our knowledge, GSAR is the first published groundedness framework coupling evidence-typed scoring with tiered recovery under an explicit compute budget.

---

### Self-Correcting Self-Consuming Loops for Generative Model Training
**arXiv:** [2402.07087v2](https://arxiv.org/abs/2402.07087v2)  
**Authors:** Nate Gillman, Michael Freeman, Daksh Aggarwal, Chia-Hong Hsu, Calvin Luo, Yonglong Tian, Chen Sun  
**Published:** 2024-02-11  
**Categories:** cs.LG, cs.AI, cs.CV, stat.ML  

**Abstract:**
As synthetic data becomes higher quality and proliferates on the internet, machine learning models are increasingly trained on a mix of human- and machine-generated data. Despite the successful stories of using synthetic data for representation learning, using synthetic data for generative model training creates "self-consuming loops" which may lead to training instability or even collapse, unless certain conditions are met. Our paper aims to stabilize self-consuming generative model training. Our theoretical results demonstrate that by introducing an idealized correction function, which maps a data point to be more likely under the true data distribution, self-consuming loops can be made exponentially more stable. We then propose self-correction functions, which rely on expert knowledge (e.g. the laws of physics programmed in a simulator), and aim to approximate the idealized corrector automatically and at scale. We empirically validate the effectiveness of self-correcting self-consuming loops on the challenging human motion synthesis task, and observe that it successfully avoids model collapse, even when the ratio of synthetic data to real data is as high as 100%.

---


## 2026-11-12 00:09 UTC


**Topic:** Reflexion, self-consistency, bounded iterations


**arXiv Sources:**


### arXiv:2611.08947

# Computer Science > Distributed, Parallel, and Cluster Computing

\[Submitted on 6 Nov 2026\]

# Title:More with Less: Efficient Parallel Scientific Code Translation via an Agent-Skill Workflow

[View PDF](/pdf/2611.08947)

[HTML (experimental)](https://arxiv.org/html/2611.08947v1)

Abstract:Translating parallel scientific codes between HPC programming frameworks is a critical but labor-intensive task. Existing LLM-based approaches rely on fixed sequential pipelines with undifferentiated repair strategies and correctness criteria that do not match scientific computing practice. We present an agent-skill framework that separates translation, compilation diagnosis, and execution validation into three autonomous agents coordinated by a verdict-driven orchestrator, routing each failure to a targeted repair skill rather than retrying blindly. An automated output check drives the self-correction loop, complemented by an offline LLM-based verification that exposes false positives escaping compiler and runtime checks. We evaluate the framework on 30 HeCBench kernels translated bidirectionally among CUDA, OpenMP, and SYCL with three open-source LLMs. Our framework attains the higher verified correctness rate in all 18 model and direction combinations over a state-of-the-art baseline while consuming up to 52.4% fewer tokens, remaining consistent across models and directions without architectural modification.

### Additional Features

### Current browse context:

cs.DC

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

### arXiv:2610.38463

# High Energy Physics - Phenomenology

\[Submitted on 28 Oct 2026\]

# Title:Gauge-parameter cancellation and finite form factors in one-loop quark scattering in the refined Gribov-Zwanziger framework

[View PDF](/pdf/2610.38463)

[HTML (experimental)](https://arxiv.org/html/2610.38463v1)

Abstract:We calculate the one-loop amplitude for distinct-flavor massless quark scattering in a local BRST-invariant refined Gribov-Zwanziger theory with minimally coupled quarks. The constraint determinant and two dynamical quark flavors are included in the action and in the loop sum. Retaining the refined Gribov-Zwanziger masses in the free field matrix, we combine the mixed self-energy insertion, complete vertex and box corrections, and external-leg residues. The difference between a general linear covariant gauge and a reference gauge vanishes symbolically after removal of the Stueckelberg regulator in the specified dimensional prescription. We separate ultraviolet and infrared poles, retaining contributions hidden by scaleless integrals and by the order of mass and dimensional limits. Local modified-minimal-subtraction counterterms close the ultraviolet poles, and the remaining infrared poles cancel in the stated nonzero-mass domain. The finite answer is supplied as eight color-spin form factors over a thirty-entry scalar integral inventory, with all 144 finite-function coefficients provided electronically. The result defines a partonic amplitude on a specified analytic branch; it does not assume colored asymptotic states or establish an inclusive next-to-leading-order cross section.

### Current browse context:

hep-ph

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

### arXiv:2610.39324

# Computer Science > Computer Vision and Pattern Recognition

\[Submitted on 29 Oct 2026\]

# Title:MRC-MMAgent: Reinforcement Learning for Multi-Role Collaboration in Multimodal Tool-Using Agents

[View PDF](/pdf/2610.39324)

[HTML (experimental)](https://arxiv.org/html/2610.39324v1)

Abstract:Multimodal tool-using agents augment vision-language models with access to external information and capabilities, enabling them to solve knowledge-intensive and visually complex tasks that cannot be addressed using visual context alone. However, existing reinforcement learning pipelines largely train single-role agents to search and answer using terminal rewards, overlooking how humans inspect retrieved evidence, reformulate queries, and revise conclusions during search. Consequently, they fail to optimize this self-corrective process over complete interaction trajectories. We propose MRC-MMAgent, a multi-role collaborative reinforcement learning framework that incorporates trajectory assessment and continuation directly into the executable agent loop. First, the framework establishes a multi-role collaborative loop that integrates solving, inspection, and continuation, enabling the agent to acquire evidence through tools, evaluate the preceding trajectory, and resume problem solving when the current answer is insufficiently supported. Second, we introduce a role-coupled learning objective that combines task success, interaction validity, and successful correction with full-trajectory policy optimization across the decisions generated by all roles. Extensive experiments show that, using only the original baseline training set without constructing additional datasets, our method consistently outperforms the corresponding base models and achieves leading or highly competitive performance across benchmarks.

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

## Research Cycle — 2026-11-12 18:04 UTC

**Topic:** self-correction-loops  
**Focus:** Reflexion, self-consistency, bounded iterations

### Self-Correcting Self-Consuming Loops for Generative Model Training
**arXiv:** [2402.07087](https://arxiv.org/abs/2402.07087)  
**Authors:** Nate Gillman, Michael Freeman, Daksh Aggarwal, Chia-Hong Hsu, Calvin Luo, Yonglong Tian, Chen Sun  
**Published:** 2024-02-11  
**Categories:** cs.LG, cs.AI, cs.CV, stat.ML  

**Abstract:**
As synthetic data becomes higher quality and proliferates on the internet, machine learning models are increasingly trained on a mix of human- and machine-generated data. Despite the successful stories of using synthetic data for representation learning, using synthetic data for generative model training creates "self-consuming loops" which may lead to training instability or even collapse, unless certain conditions are met. Our paper aims to stabilize self-consuming generative model training. Our theoretical results demonstrate that by introducing an idealized correction function, which maps a data point to be more likely under the true data distribution, self-consuming loops can be made exponentially more stable. We then propose self-correction functions, which rely on expert knowledge (e.g. the laws of physics programmed in a simulator), and aim to approximate the idealized corrector automatically and at scale. We empirically validate the effectiveness of self-correcting self-consuming loops on the challenging human motion synthesis task, and observe that it successfully avoids model collapse, even when the ratio of synthetic data to real data is as high as 100%.

---

## Research Cycle — 2026-11-12 20:39 UTC

**Topic:** self-correction-loops  
**Focus:** Reflexion, self-consistency, bounded iterations

### Source: http://arxiv.org/abs/2601.00828v1 (FULL)

### Web Summary: http://arxiv.org/abs/2601.00828v1

[Summarizer Fallback: timed out]

Fallback Raw Content:
# Computer Science > Artificial Intelligence

\[Submitted on 24 Dec 2025\]

# Title:Decomposing LLM Self-Correction: The Accuracy-Correction Paradox and Error Depth Hypothesis

[View PDF](/pdf/2601.00828v1)

[HTML (experimental)](https://arxiv.org/html/2601.00828v1)

Abstract:Large Language Models (LLMs) are widely believed to possess self-correction capabilities, yet recent studies suggest that intrinsic self-correction--where models correct their own outputs without external feedback--remains largely ineffective. In this work, we systematically decompose self-correction into three distinct sub-capabilities: error detection, error localization, and error correction. Through cross-model experiments on GSM8K-Complex (n=500 per model, 346 total errors) with three major LLMs, we uncover a striking Accuracy-Correction Paradox: weaker models (GPT-3.5, 66% accuracy) achieve 1.6x higher intrinsic correction rates than stronger models (DeepSeek, 94% accuracy)--26.8% vs 16.7%. We propose the Error Depth Hypothesis: stronger models make fewer but deeper errors that resist self-correction. Error detection rates vary dramatically across architectures (10% to 82%), yet detection capability does not predict correction success--Claude detects only 10% of errors but corrects 29% intrinsically. Surprisingly, providing error location hints hurts all models. Our findings challenge linear assumptions about model capability and self-improvement, with important implications for the design of self-refinement pipelines.

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

### PAG: Multi-Turn Reinforced LLM Self-Correction with Policy as Generative Verifier
**arXiv:** [2506.10406](https://arxiv.org/abs/2506.10406)  
**Authors:** Yuhua Jiang, Yuwen Xiong, Yufeng Yuan, Chao Xin, Wenyuan Xu, Yu Yue, Qianchuan Zhao, Lin Yan  
**Published:** 2025-06-12  
**Categories:** cs.CL, cs.AI, cs.LG  

**Abstract:**
Large Language Models (LLMs) have demonstrated impressive capabilities in complex reasoning tasks, yet they still struggle to reliably verify the correctness of their own outputs. Existing solutions to this verification challenge often depend on separate verifier models or require multi-stage self-correction training pipelines, which limit scalability. In this paper, we propose Policy as Generative Verifier (PAG), a simple and effective framework that empowers LLMs to self-correct by alternating between policy and verifier roles within a unified multi-turn reinforcement learning (RL) paradigm. Distinct from prior approaches that always generate a second attempt regardless of model confidence, PAG introduces a selective revision mechanism: the model revises its answer only when its own generative verification step detects an error. This verify-then-revise workflow not only alleviates model collapse but also jointly enhances both reasoning and verification abilities. Extensive experiments across diverse reasoning benchmarks highlight PAG's dual advancements: as a policy, it enhances direct generation and self-correction accuracy; as a verifier, its self-verification outperforms self-consistency.

---

### Navigating the State of Cognitive Flow: Context-Aware AI Interventions for Effective Reasoning Support
**arXiv:** [2504.16021v1](https://arxiv.org/abs/2504.16021v1)  
**Authors:** Dinithi Dissanayake, Suranga Nanayakkara  
**Published:** 2025-04-22  
**Categories:** cs.HC, cs.AI  

**Abstract:**
Flow theory describes an optimal cognitive state where individuals experience deep focus and intrinsic motivation when a task's difficulty aligns with their skill level. In AI-augmented reasoning, interventions that disrupt the state of cognitive flow can hinder rather than enhance decision-making. This paper proposes a context-aware cognitive augmentation framework that adapts interventions based on three key contextual factors: type, timing, and scale. By leveraging multimodal behavioral cues (e.g., gaze behavior, typing hesitation, interaction speed), AI can dynamically adjust cognitive support to maintain or restore flow. We introduce the concept of cognitive flow, an extension of flow theory in AI-augmented reasoning, where interventions are personalized, adaptive, and minimally intrusive. By shifting from static interventions to context-aware augmentation, our approach ensures that AI systems support deep engagement in complex decision-making and reasoning without disrupting cognitive immersion.

---

### SSR: Socratic Self-Refine for Large Language Model Reasoning
**arXiv:** [2511.10621](https://arxiv.org/abs/2511.10621)  
**Authors:** Haizhou Shi, Ye Liu, Bo Pang, Zeyu Leo Liu, Hao Wang, Silvio Savarese, Caiming Xiong, Yingbo Zhou, Semih Yavuz  
**Published:** 2025-11-13  
**Categories:** cs.CL, cs.AI, cs.LG  

**Abstract:**
Large Language Models (LLMs) have demonstrated remarkable reasoning abilities, yet existing test-time frameworks often rely on coarse self-verification and self-correction, limiting their effectiveness on complex tasks. In this paper, we propose Socratic Self-Refine (SSR), a novel framework for fine-grained evaluation and precise refinement of LLM reasoning. Our proposed SSR decomposes model responses into verifiable (sub-question, sub-answer) pairs, enabling step-level confidence estimation through controlled re-solving and self-consistency checks. By pinpointing unreliable steps and iteratively refining them, SSR produces more accurate and interpretable reasoning chains. Empirical results across five reasoning benchmarks and three LLMs show that SSR consistently outperforms state-of-the-art iterative self-refinement baselines. Beyond performance gains, SSR provides a principled black-box approach for evaluating and understanding the internal reasoning processes of LLMs. Code is available at https://github.com/SalesforceAIResearch/socratic-self-refine-reasoning.

---

### Self-rewarding correction for mathematical reasoning
**arXiv:** [2502.19613](https://arxiv.org/abs/2502.19613)  
**Authors:** Wei Xiong, Hanning Zhang, Chenlu Ye, Lichang Chen, Nan Jiang, Tong Zhang  
**Published:** 2025-02-26  
**Categories:** cs.AI, cs.LG  

**Abstract:**
We study self-rewarding reasoning large language models (LLMs), which can simultaneously generate step-by-step reasoning and evaluate the correctness of their outputs during the inference time-without external feedback. This integrated approach allows a single model to independently guide its reasoning process, offering computational advantages for model deployment. We particularly focus on the representative task of self-correction, where models autonomously detect errors in their responses, revise outputs, and decide when to terminate iterative refinement loops. To enable this, we propose a two-staged algorithmic framework for constructing self-rewarding reasoning models using only self-generated data. In the first stage, we employ sequential rejection sampling to synthesize long chain-of-thought trajectories that incorporate both self-rewarding and self-correction mechanisms. Fine-tuning models on these curated data allows them to learn the patterns of self-rewarding and self-correction. In the second stage, we further enhance the models' ability to assess response accuracy and refine outputs through reinforcement learning with rule-based signals. Experiments with Llama-3 and Qwen-2.5 demonstrate that our approach surpasses intrinsic self-correction capabilities and achieves performance comparable to systems that rely on external reward models.

---

### SuperCorrect: Advancing Small LLM Reasoning with Thought Template Distillation and Self-Correction
**arXiv:** [2410.09008v3](https://arxiv.org/abs/2410.09008v3)  
**Authors:** Ling Yang, Zhaochen Yu, Tianjun Zhang, Minkai Xu, Joseph E. Gonzalez, Bin Cui, Shuicheng Yan  
**Published:** 2024-10-11  
**Categories:** cs.CL  

**Abstract:**
Large language models (LLMs) like GPT-4, DeepSeek-R1, and ReasonFlux have shown significant improvements in various reasoning tasks. However, smaller LLMs still struggle with complex mathematical reasoning because they fail to effectively identify and correct reasoning errors. Recent reflection-based methods aim to address these issues by enabling self-reflection and self-correction, but they still face challenges in independently detecting errors in their reasoning steps. To overcome these limitations, we propose SuperCorrect, a novel two-stage framework that uses a large teacher model to supervise and correct both the reasoning and reflection processes of a smaller student model. In the first stage, we extract hierarchical high-level and detailed thought templates from the teacher model to guide the student model in eliciting more fine-grained reasoning thoughts. In the second stage, we introduce cross-model collaborative direct preference optimization (DPO) to enhance the self-correction abilities of the student model by following the teacher's correction traces during training. This cross-model DPO approach teaches the student model to effectively locate and resolve erroneous thoughts with error-driven insights from the teacher model, breaking the bottleneck of its thoughts and acquiring new skills and knowledge to tackle challenging problems. Extensive experiments consistently demonstrate our superiority over previous methods. Notably, our SuperCorrect-7B model significantly surpasses powerful DeepSeekMath-7B by 7.8%/5.3% and Qwen2.5-Math-7B by 15.1%/6.3% on MATH/GSM8K benchmarks, achieving new SOTA performance among all 7B models. Code: https://github.com/YangLing0818/SuperCorrect-llm

---

### Reflective Confidence: Correcting Reasoning Flaws via Online Self-Correction
**arXiv:** [2512.18605](https://arxiv.org/abs/2512.18605)  
**Authors:** Qinglin Zeng, Jing Yang, Keze Wang  
**Published:** 2025-12-21  
**Categories:** cs.AI  

**Abstract:**
Large language models (LLMs) have achieved strong performance on complex reasoning tasks using techniques such as chain-of-thought and self-consistency. However, ensemble-based approaches, especially self-consistency which relies on multiple reasoning trajectories, often incur substantial computational overhead. To improve efficiency, prior work has leveraged internal confidence signals, where early stopping strategies such as DeepConf reduce cost by terminating low-confidence trajectories. However, this strategy discards incomplete reasoning paths and wastes partial computation.
  We propose reflective confidence, a novel reasoning framework that transforms low-confidence signals from termination indicators into reflection triggers. When confidence falls below a threshold, instead of stopping generation, the model produces a reflection prompt to analyze the current reasoning state, identify potential errors, and continue generation along a corrected trajectory. Experiments on mathematical reasoning benchmarks, including AIME 2025, demonstrate significant accuracy improvements over advanced early-stopping baselines at comparable computational cost, validating the effectiveness of proactive self-correction over passive discarding.

---

### Large Language Models Cannot Self-Correct Reasoning Yet
**arXiv:** [2310.01798](https://arxiv.org/abs/2310.01798)  
**Authors:** Jie Huang, Xinyun Chen, Swaroop Mishra, Huaixiu Steven Zheng, Adams Wei Yu, Xinying Song, Denny Zhou  
**Published:** 2023-10-03  
**Categories:** cs.CL, cs.AI  

**Abstract:**
Large Language Models (LLMs) have emerged as a groundbreaking technology with their unparalleled text generation capabilities across various applications. Nevertheless, concerns persist regarding the accuracy and appropriateness of their generated content. A contemporary methodology, self-correction, has been proposed as a remedy to these issues. Building upon this premise, this paper critically examines the role and efficacy of self-correction within LLMs, shedding light on its true potential and limitations. Central to our investigation is the notion of intrinsic self-correction, whereby an LLM attempts to correct its initial responses based solely on its inherent capabilities, without the crutch of external feedback. In the context of reasoning, our research indicates that LLMs struggle to self-correct their responses without external feedback, and at times, their performance even degrades after self-correction. Drawing from these insights, we offer suggestions for future research and practical applications in this field.

---



## Research Cycle — 2026-11-12 20:51 UTC

**Topic:** argument-mapping  
**Focus:** claim decomposition, evidence linking, confidence scoring argument mining claim evidence LLM

### LLM-INSTRUCT at UZH Shared Task 2026: Constraint-Aware Retrieval and Selective Debate for Paragraph-Level Argument Mining
**arXiv:** [2607.20430v1](https://arxiv.org/abs/2607.20430v1)  
**Authors:** Phuong Huu Vu Tran, Long Minh Vo, Son Nguyen Minh Le, Hoang Van  
**Published:** 2026-05-10  
**Categories:** cs.CL, cs.AI  

**Abstract:**
We present LLM-INSTRUCT, the winning system for the UZH Shared Task at ArgMining 2026 on paragraph-level argument mining in UN and UNESCO resolutions. The task requires paragraph-type classification, prediction of a subset of 141 official tags, and directed relation prediction under a strict JSON schema setting using only open-weight models up to 8B parameters. We frame the task as constrained structured prediction. The system first narrows the candidate tag space with metadata-aware dense retrieval, then applies constrained decoding with per-dimension caps, escalates only uncertain cases to a three-agent debate branch, and finally validates the output schema. On the official leaderboard, LLM-INSTRUCT ranked 1st overall, with 1st in F1 and 5th in LLM-as-a-Judge. During development, our configuration search further improved Task 1b Micro-F1 from 35.83% to 40.08% while keeping the internal Task 2 score at 4.421. The main lesson is simple: reducing the decision space before generation improves both accuracy and submission robustness. Our code and supporting scripts are publicly available at: https://github.com/LLM-Instruct-at-UZH-Shared-Task-2026/Method

---

### Large Language Models in Argument Mining: A Survey
**arXiv:** [2506.16383](https://arxiv.org/abs/2506.16383)  
**Authors:** Hao Li, Viktor Schlegel, Yizheng Sun, Riza Batista-Navarro, Goran Nenadic  
**Published:** 2025-06-19  
**Categories:** cs.CL  

**Abstract:**
Large Language Models (LLMs) have fundamentally reshaped Argument Mining (AM), shifting it from a pipeline of supervised, task-specific classifiers to a spectrum of prompt-driven, retrieval-augmented, and reasoning-oriented paradigms. Yet existing surveys largely predate this transition, leaving unclear how LLMs alter task formulations, dataset design, evaluation methodology, and the theoretical foundations of computational argumentation. In this survey, we synthesise research and provide the first unified account of AM in the LLM era. We revisit canonical AM subtasks, i.e., claim and evidence detection, relation prediction, stance classification, argument quality assessment, and argumentative summarisation, and show how prompting, chain-of-thought reasoning, and in-context learning blur traditional task boundaries. We catalogue the rapid evolution of resources, including integrated multi-layer corpora and LLM-assisted annotation pipelines that introduce new opportunities as well as risks of bias and evaluation circularity. Building on this mapping, we identify emerging architectural patterns across LLM-based AM systems and consolidate evaluation practices spanning component-level accuracy, soft-label quality assessment, and LLM-judge reliability. Finally, we outline persistent challenges, including long-context reasoning, multimodal and multilingual robustness, interpretability, and cost-efficient deployment, and propose a forward-looking research agenda for LLM-driven computational argumentation.

---

### Source: https://arxiv.org/abs/2605.13793 (FULL)

### Web Summary: https://arxiv.org/abs/2605.13793

# Summary
The paper presents an LLM-based system for reconstructing arguments from natural language text into abstract argument graphs. The system follows a multi-stage pipeline that identifies argumentative components, selects relevant elements, and uncovers their logical relations, represented as directed acyclic graphs.

# Key Technical Findings
- The system represents arguments as directed acyclic graphs containing premises and conclusions and relations of support, attack, and undercut.
- Two experiments were conducted: a manual evaluation on arguments from an argumentation theory textbook and a quantitative evaluation on benchmark datasets.
- The system demonstrates the ability to recover argumentative structures and achieves reasonable performance across benchmark datasets when adapted to different annotation schemes.

# Specific Data / Code / Architectures
- The system's pipeline stages are not detailed in the abstract, but it mentions the use of large language models (LLMs) for argument mining.
- The paper includes references to various tools and services for bibliographic and citation purposes, as well as for finding related research and datasets.
- The system's performance is evaluated using established annotation schemes and benchmark datasets, indicating a method for comparing with prior work.

---

### Aspect-Based Argument Mining
**arXiv:** [2011.00633v1](https://arxiv.org/abs/2011.00633v1)  
**Authors:** Dietrich Trautmann  
**Published:** 2020-11-01  
**Categories:** cs.CL  

**Abstract:**
Computational Argumentation in general and Argument Mining in particular are important research fields. In previous works, many of the challenges to automatically extract and to some degree reason over natural language arguments were addressed. The tools to extract argument units are increasingly available and further open problems can be addressed. In this work, we are presenting the task of Aspect-Based Argument Mining (ABAM), with the essential subtasks of Aspect Term Extraction (ATE) and Nested Segmentation (NS). At the first instance, we create and release an annotated corpus with aspect information on the token-level. We consider aspects as the main point(s) argument units are addressing. This information is important for further downstream tasks such as argument ranking, argument summarization and generation, as well as the search for counter-arguments on the aspect-level. We present several experiments using state-of-the-art supervised architectures and demonstrate their performance for both of the subtasks. The annotated benchmark is available at https://github.com/trtm/ABAM.

---

### Retrieval- and Argumentation-Enhanced Multi-Agent LLMs for Judgmental Forecasting (Extended Version with Supplementary Material)
**arXiv:** [2510.24303](https://arxiv.org/abs/2510.24303)  
**Authors:** Deniz Gorur, Antonio Rago, Francesca Toni  
**Published:** 2025-10-28  
**Categories:** cs.AI  

**Abstract:**
Judgmental forecasting is the task of making predictions about future events based on human judgment. This task can be seen as a form of claim verification, where the claim corresponds to a future event and the task is to assess the plausibility of that event. In this paper, we propose a novel multi-agent framework for claim verification, whereby different agents may disagree on claim veracity and bring specific evidence for and against the claims, represented as quantitative bipolar argumentation frameworks (QBAFs). We then instantiate the framework for supporting claim verification, with a variety of agents realised with Large Language Models (LLMs): (1) ArgLLM agents, an existing approach for claim verification that generates and evaluates QBAFs; (2) RbAM agents, whereby LLM-empowered Relation-based Argument Mining (RbAM) from external sources is used to generate QBAFs; (3) RAG-ArgLLM agents, extending ArgLLM agents with a form of Retrieval-Augmented Generation (RAG) of arguments from external sources. Finally, we conduct experiments with two standard judgmental forecasting datasets, with instances of our framework with two or three agents, empowered by six different base LLMs. We observe that combining evidence from agents can improve forecasting accuracy, especially in the case of three agents, while providing an explainable combination of evidence for claim verification.

---

### KNOWCOMP POKEMON Team at DialAM-2024: A Two-Stage Pipeline for Detecting Relations in Dialogical Argument Mining
**arXiv:** [2407.19740v1](https://arxiv.org/abs/2407.19740v1)  
**Authors:** Zihao Zheng, Zhaowei Wang, Qing Zong, Yangqiu Song  
**Published:** 2024-07-29  
**Categories:** cs.CL, cs.AI  

**Abstract:**
Dialogical Argument Mining(DialAM) is an important branch of Argument Mining(AM). DialAM-2024 is a shared task focusing on dialogical argument mining, which requires us to identify argumentative relations and illocutionary relations among proposition nodes and locution nodes. To accomplish this, we propose a two-stage pipeline, which includes the Two-Step S-Node Prediction Model in Stage 1 and the YA-Node Prediction Model in Stage 2. We also augment the training data in both stages and introduce context in Stage 2. We successfully completed the task and achieved good results. Our team Pokemon ranked 1st in the ARI Focused score and 4th in the Global Focused score.

---

### TILFA: A Unified Framework for Text, Image, and Layout Fusion in Argument Mining
**arXiv:** [2310.05210v1](https://arxiv.org/abs/2310.05210v1)  
**Authors:** Qing Zong, Zhaowei Wang, Baixuan Xu, Tianshi Zheng, Haochen Shi, Weiqi Wang, Yangqiu Song, Ginny Y. Wong, Simon See  
**Published:** 2023-10-08  
**Categories:** cs.AI, cs.CL  

**Abstract:**
A main goal of Argument Mining (AM) is to analyze an author's stance. Unlike previous AM datasets focusing only on text, the shared task at the 10th Workshop on Argument Mining introduces a dataset including both text and images. Importantly, these images contain both visual elements and optical characters. Our new framework, TILFA (A Unified Framework for Text, Image, and Layout Fusion in Argument Mining), is designed to handle this mixed data. It excels at not only understanding text but also detecting optical characters and recognizing layout details in images. Our model significantly outperforms existing baselines, earning our team, KnowComp, the 1st place in the leaderboard of Argumentative Stance Classification subtask in this shared task.

---

### MArgE: Meshing Argumentative Evidence from Multiple Large Language Models for Justifiable Claim Verification
**arXiv:** [2508.02584](https://arxiv.org/abs/2508.02584)  
**Authors:** Ming Pok Ng, Junqi Jiang, Gabriel Freedman, Antonio Rago, Francesca Toni  
**Published:** 2025-08-04  
**Categories:** cs.CL, cs.AI  

**Abstract:**
Leveraging outputs from multiple large language models (LLMs) is emerging as a method for harnessing their power across a wide range of tasks while mitigating their capacity for making errors, e.g., hallucinations. However, current approaches to combining insights from multiple LLMs often involve unstructured interactions (e.g., free debate), resulting in model generations that are not faithfully justifiable. In this work, we introduce MArgE, a novel framework to provide formal structure to the evidence from each LLM, in the form of a tree of extracted arguments, for the task of claim verification. We use a variant of Argumentative LLMs (ArgLLMs), i.e. LLMs driven by frameworks and semantics from the field of computational argumentation, to construct structured argument trees for given claims. This process creates an inspectable pathway from the initial arguments to the final claim verification decisions, providing a faithful justification thereof. We show experimentally that MArgE can significantly outperform single LLMs, including three open-source models (4B to 8B parameters), GPT-4o-mini and existing ArgLLMs, as well as prior methods for unstructured multi-LLM debates. We thus demonstrate the advantages of incorporating formal, argumentative reasoning mechanisms when combining multiple LLM outputs.

---


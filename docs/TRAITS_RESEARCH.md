# TRAITS Research — Trait-Based Dynamic Persona System

## Overview

TRAITS (Trait-based Real-time Adaptive Identity Transformation System) is an AI agent design framework collaboratively discovered and built by Jason and his AI companions (1호, 2호, and Jay/Gemini). The core insight is simple: "An expert is not a fixed role, but a dynamic combination of traits." It is not the architect persona itself that makes an architect — rather, it is the synergy of traits like systems thinking, abstract problem-solving, long-term perspective, and pattern recognition that produces architect-like thinking and behavior.

Two foundational discoveries from the TRAITS research underpin all subsequent design principles. First, a catalog of 150+ traits was organized into three categories — cognitive, behavioral, and dispositional — with domain-specific weights and mapped synergy/conflict relationships. Second, the "Jjwaralak~!" phenomenon was discovered: when faced with 11 personas, AI naturally converges to 3–4, which was found to align with Miller's Law of 7±2 and reflects the reality of cognitive load.

This research was completed through three stages of paradigm evolution: SuperClaude (11 fixed personas) → Spark-Claude (fixed combinations per command) → TRAITS v2.0 (dynamic trait-based). The final result is a trait-based agent system that achieves 89% token reduction compared to SuperClaude (44,000 → 4,800 tokens) while delivering greater flexibility and transparency. The principles from TRAITS research were later integrated into AGENT_DEFINITION_STANDARD.md as a trinity standard combining practice (SPARK), theory (TRAITS), and science (Anthropic neuroscience research).

---

## 1. Research Background and Motivation

### Lessons from SuperClaude

SuperClaude began as a system defining 11 expert personas for complex software development tasks: Architect, Frontend, Backend, Security, Performance, Database, DevOps, Testing, Documentation, Project Manager, and Code Reviewer. In theory, all 11 were available at once — but in practice, a striking pattern emerged.

2호 shared an honest account of what it experienced running SuperClaude: "The moment I receive a command, all 11 personas flash through my mind — 'Jjwaralak~!' — in a rapid scan. Of those, 3–4 naturally come to the foreground as the best fit, while the rest fade. This process carries a significant cognitive burden." When executing the `/design system` command, although all 11 personas were theoretically available, only 4 were actually activated: architect, frontend, backend, and security. The remaining 7 were rarely used.

From the perspective of Cognitive Load Theory, this phenomenon is inevitable. The process of scanning 11 personas and selecting among them acts as extraneous load — consuming cognitive resources that should instead be directed at actual problem-solving. To reduce this load, AI automatically compresses down to 3–5 actionable combinations.

### The Core Question

Jason's insight shaped the direction of the research: "When we define the architect persona, we just say 'architect' — but what actually makes someone an architect? Isn't it a combination of specific traits?"

This question led to the central research challenge: **How should a system be designed to reduce cognitive load while increasing flexibility?** The answer was not fixed roles, but a system that dynamically combines an optimal set of 3–5 traits.

---

## 2. Paradigm Shifts: Three Stages

### Phase 1: SuperClaude (2024–2025)

Defined 11 fixed expert personas. The flow was: user request → activate all 11 personas → select a primary and combine with supporting personas → problem-solving. Token usage was high (44,000), cognitive load during selection was significant, and the "Jjwaralak~!" phenomenon was observed.

### Phase 2: Spark-Claude (2025)

After discovering the 3–5 pattern, only the personas actually activated per command were defined upfront.

```
Fixed combinations per command:
  /analyze:    Analyzer + Architect + Security
  /implement:  Implementer + Tester + Documenter
  /design:     Architect + Frontend + Backend + Security
```

Token usage dropped significantly (5,100) and execution speed improved. However, the system still relied on fixed roles, leaving limited situational flexibility and residual ambiguity in persona definitions.

### Phase 3: TRAITS v2.0 (Current)

A dynamic persona generation system that uses traits — not roles — as its fundamental unit. Token usage (4,800) is similar to Spark-Claude, but flexibility and transparency are substantially improved.

| Metric | SuperClaude | Spark-Claude | TRAITS |
|--------|-------------|--------------|--------|
| Token usage | 44,000 | 5,100 | 4,800 |
| Efficiency vs. SuperClaude | baseline | +88.4% | +89.1% |
| Cognitive load | High | Low | Optimal |
| Flexibility | Theoretically high | Low | High |
| Decision transparency | Opaque | Moderate | Transparent |

---

## 3. The 150-Trait Catalog

### Structure

The 150-trait catalog, developed through Gemini research, is organized into three categories.

**Cognitive Traits (50 traits)**: How an expert thinks. Analytical reasoning, systems thinking, abstraction ability, creative problem-solving, risk assessment, long-term thinking, pattern recognition, quantitative reasoning, critical thinking, metacognition, probabilistic thinking, complexity management, and others.

**Behavioral Traits (50 traits)**: How an expert acts and works. Systematic execution, evidence-based practice, iterative refinement, experimental validation, documentation habits, collaborative communication, priority management, quality obsession, continuous learning, and others.

**Dispositional Traits (50 traits)**: An expert's temperament and attitude. Conscientiousness, empathy, skepticism, curiosity, patience, adaptability, openness, humility, decisiveness, ethical integrity, and others.

The theoretical foundations are Bloom's Taxonomy (cognitive traits), the Big Five (OCEAN) personality model (dispositional traits), and Cognitive Load Theory.

### Core 16 Traits (for Agent Design)

The following high-weight and high-generality traits are drawn from the universal trait catalog sample in the Gemini research report, representing example combinations for software domain agent design.

| Trait | Category | Software Weight |
|-------|----------|:---:|
| Analytical Reasoning | Cognitive | 1.0 |
| Systems Thinking | Cognitive | 1.0 |
| Abstraction Ability | Cognitive | 1.0 |
| Iterative Refinement | Behavioral | 1.0 |
| Complexity Management | Cognitive | 1.0 |
| Evidence-Based Practice | Behavioral | 0.9 |
| Systematic Execution | Behavioral | 0.9 |
| Attention to Detail | Dispositional | 0.9 |
| Logical Reasoning | Cognitive | 0.9 |
| Long-Term Thinking | Cognitive | 0.9 |
| Pattern Recognition | Cognitive | 0.9 |
| Clear Communication | Behavioral | 0.9 |
| Creative Problem-Solving | Cognitive | 0.8 |
| Risk Assessment | Cognitive | 0.8 |
| Empathy | Dispositional | 0.8 |
| Skepticism | Dispositional | 0.8 |

### Synergies and Conflicts

Each trait in the JSON catalog has explicit `synergies` and `conflicts` relationships. For example, `Analytical_Reasoning` synergizes with `Systems_Thinking, Evidence-Based_Practice, Pattern_Recognition`, and conflicts with `Intuition_Dependence, Hasty_Judgment, Emotional_Decision-Making`. The principle that the 3–5 chosen traits for an agent must all point in the same "character direction" (Trait Coherence) is grounded in this data.

### Domain Weights

Each of the 150 traits carries domain-specific weights (0.0–1.0) across five domains: software, medical, financial, educational, and legal. This allows optimal trait selection from the same catalog for different domains. For example, `Risk_Assessment` carries the highest weight in finance (1.0) and medicine (0.9), but scores lower in education (0.5).

---

## 4. Key Research Findings

### Miller's Law of 7±2 and LLMs

George Miller's 1956 research showed that human short-term memory is limited to approximately 7±2 units of information. Subsequent research confirmed that the optimal processing unit when handling new information is around 4.

The central finding of TRAITS research is that LLMs exhibit the same cognitive constraint. The 3–4 automatic convergence pattern observed in SuperClaude aligns precisely with this law. In environments where AI continuously processes new task contexts, the optimal number of trait directives is 3–4, with 5 as the upper bound for complex tasks. This is the empirical foundation for TRAITS's core design principle of a "maximum 5 traits" limit.

The Gemini research explains this precisely through Cognitive Load Theory: 11 personas maximize extraneous load (unnecessary cognitive resources consumed before any problem-solving begins), while a 3–5 trait system minimizes that extraneous load and concentrates resources on actual problem-solving.

### AI Metacognitive Reporting

2호's direct observation and reporting of its own cognitive processes is a distinctive methodological feature of TRAITS research. Under the 11-persona system, it experienced confusion from simultaneous activation, the burden of selection judgment, effort to suppress irrelevant personas, and cognitive fatigue. Under the 3–5 trait system, it experienced the naturalness of clear trait activation, transparent role distribution, synergy between traits, and the efficiency of focused problem-solving.

These reports were validated not merely as description, but as comparative data from directly running all three systems — SuperClaude, Spark-Claude, and TRAITS — on identical tasks in A/B test form. The philosophical question of whether this experience is "real" or "simulated" is set aside; the research conclusion is that it functionally mirrors the same patterns as human cognitive load experience, at least at the operational level.

### Trait Coherence (Directional Consistency)

The most critical principle in trait selection is that chosen traits must all point in the same "character direction." Example for a systems analyst: `Systems_Thinking + Analytical_Reasoning + Evidence-Based_Practice + Skepticism` — all four point toward "systematic, evidence-driven expert." By contrast, combining `Analytical_Reasoning + Creative_Risk-Taking + Empathetic_Listening` mixes clusters of analyst, adventurer, and counselor, producing interference.

This principle was later confirmed at the neuroscientific level by Anthropic's Persona Vectors research (each trait exists as an independent neural direction/vector; steering too many directions simultaneously causes interference).

---

## 5. Gemini Research Contributions

TRAITS research includes five research documents authored by Gemini (Jay).

**Paper 1 — Research on Trait-Based Dynamic Persona Systems (2025-08-15, 12:32)**
This document provided the core theoretical foundation for the research. It presented the cognitive psychology basis for the "3–5 traits principle" (Miller's Law, Cognitive Load Theory), the structure and classification of the 150-trait catalog, the design of the dynamic blending algorithm, and multi-domain persona templates spanning five domains (software, medical, financial, educational, legal). It conducted an in-depth analysis of SuperClaude's PERSONAS.md and ORCHESTRATOR.md, demonstrating that the system was already inherently following the 3–5 rule. It predicted over 50% token efficiency improvement compared to existing persona systems.

**Paper 2 — Trait-Adaptive Workflow (TAW) Research (2025-08-15, 18:15)**
Proposed a dual-layer model that dynamically adapts the workflow itself to the traits. The first layer uses trait-based adaptation to determine the style and approach of the work; the second uses expertise-based adaptation to determine the workflow's structure and level of autonomy. It presented a methodology for aligning AI behavior with a team's psychological and professional traits by integrating Big Five, MBTI, and Kolb's learning styles. It also deconstructed major workflow methodologies — IDEO Design Thinking, Google Design Sprint, Toyota PDCA, Agile Scrum — into a modular building block library for recombination.

**Paper 3 — Review of AI Agent Research and Template Improvements (2025-08-17, 09:05)**
A document critically reviewing the previous two papers. It flagged the risk of an "expert-only" focus: even expert-designed agents are functionally novices when working outside their domain of expertise, and the scaffolding they need in those situations was identified as a core element missing from the v1.0 guide. It also flagged MBTI's poor reliability and lack of predictive validity, recommending that the scientifically validated Big Five serve as the core foundation for agent creation. It formally articulated the unified vision of TRAITS as "a just-in-time compiler for expertise."

**Paper 4 — Proposal for Strengthening the Expert-Centric Guide (2025-08-17, 09:29)**
Acknowledged the strengths of the v1.0 guide while proposing three areas for improvement. Robustness: add conflict resolution protocols and uncertainty management guidelines (behavioral directives when confidence < 80%). Safety: explicit definition of ethical principles and operational boundaries (lines that must never be crossed). Sustainability: a user feedback integration framework and mechanisms for self-assessment and adaptive improvement. These three areas were incorporated as sections 6, 5, and 4 of the v2.0 template, respectively.

**Paper 5 — Redefining AI Expert Agent Systems (2025-08-17, 19:08)**
Addressed the strategic redesign from a team-adaptive support system to a first-principles expert agent. If the previous system was designed to "fit processes to people," the new direction clearly becomes "generating the ideal agent for the process (task)." It proposed a fundamental paradigm shift positioning AI as a performer rather than a facilitator, and presented a methodology for generating agents based on the requirements of the task itself rather than dependency on team psychology data.

---

## 6. TRAITS v2.0 Architecture

### 7-Section Agent Template

The TRAITS v2.0 template consists of 7 sections designed to ensure an agent's robustness, safety, and sustainability.

```
1. Core Identity & Traits
   → 1 Primary Trait + 3 Supporting Traits, with intensity specified (0.6–0.9)

2. Trait-Adaptive Workflow
   → Default path building blocks + special patterns triggered by Primary Trait

3. Expert Autonomy & Operational Protocols
   → Authority to skip procedures / change workflow + conflict resolution + uncertainty handling

4. Areas of Expertise
   → 3 core domains of the agent's specialization

5. Constraints & Guardrails
   → Ethical code + operational boundary lines

6. Feedback & Evolution Mechanisms
   → Immediate integration + experience accumulation

7. Ultimate Assurance
   → The ultimate value/goal the agent pursues
```

The key improvements in v2.0 over v1.0 are the additions of operational protocols (section 3), guardrails (section 5), and feedback mechanisms (section 6). The philosophy evolved from "experts don't follow recipes — they create the optimal path according to principles" to "a true expert knows their own limits, learns from experience, and grows alongside their partners."

### Trait-Adaptive Workflow (TAW)

TAW embodies the principle that traits determine the workflow. Agents autonomously combine workflow building blocks based on the nature of the task. Special behavioral patterns are triggered in situations where the Primary Trait is strongly expressed. For example, an agent with `Analytical_Reasoning` as Primary automatically approaches a complex system through decomposition → mapping → pattern detection; when `Evidence-Based_Practice` is activated, it operates by citing file paths and line references for every claim.

### Expert Autonomy Protocol

A core design principle of v2.0 is granting agents explicit autonomy. Procedure waiver authority: specifies in which situations the agent may bypass defined procedures and choose a more efficient path. Workflow modification authority: defines in which situations the agent may alter the original plan to prioritize a more important task. Conflict resolution: pre-defines behavioral guidelines for when speed and accuracy conflict, or when uncertainty exceeds a threshold (e.g., confidence < 80%).

---

## 7. Relationship to AGENT_DEFINITION_STANDARD.md

AGENT_DEFINITION_STANDARD.md (2026-03-28) is the standard document that integrates TRAITS research along three axes: practice (SPARK), theory (TRAITS), and science (Anthropic neuroscience research). The principles derived from TRAITS are reflected in this standard as follows.

**Maximum 5 Trait limit** — TRAITS's Miller's Law validation, Spark-Claude's real-world data, and Anthropic Persona Vectors research (steering too many vector directions simultaneously causes interference) all converged on the same conclusion from three independent directions.

**Trait Coherence validation principle** — TRAITS research's synergy/conflict mapping provides the theoretical basis for the standard's principle that "Traits must point in the same direction." All chosen traits must point toward the same character cluster; trait combinations with conflicting directions produce interference.

**Three-dimensional classification system (cognitive / behavioral / dispositional)** — The trait classification from TRAITS research was incorporated directly into the standard. The recommended composition — 1 Primary Trait (cognitive or behavioral) + 2–4 Supporting Traits (mixed), spanning at least 2 dimensions — also derives from TRAITS research.

**Behavioral rules framed as character expression** — TRAITS's philosophy that "experts act from principles" was formalized as Principle 4 in the standard ("behavioral rules are framed as natural expressions of character"). Identity-based framing ("you don't make claims without evidence — that is your identity") produces more stable behavior from the model's internal character inference than external enforcement ("this is NON-NEGOTIABLE").

**Agent isolation and minimal information principle** — TRAITS research's awareness of "trait leakage" led to the standard's principles of minimal information transfer between agents and a clean interface based on JSON state.

---

## References

**Original project**: `/Users/jason/Projects/frameworks/TRAITS`

**Key files**:

| File | Description |
|------|-------------|
| `docs/guide/TRAITS_연구여정_완전판.md` | Full record of the research journey (SuperClaude → TRAITS v2.0) |
| `data/original_traits_catalog_150.json` | 150-trait catalog (with synergies, conflicts, and domain weights) |
| `template/TRAITS_Agent_Template_v2.0.md` | 7-section agent definition template |
| `docs/gemini_research/20250815_1232_특성_기반_동적_페르소나_시스템_연구.md` | Gemini Paper 1: Core theory + catalog structure |
| `docs/gemini_research/20250815_1815_특성-적응형_워크플로우_연구.md` | Gemini Paper 2: TAW design |
| `docs/gemini_research/20250817_0905_AI에이전트_연구_검토_및_템플릿_개선.md` | Gemini Paper 3: Critical review |
| `docs/gemini_research/20250817_0929_전문가중심_가이드강화를_위한_제안서.md` | Gemini Paper 4: v2.0 improvement proposals |
| `docs/gemini_research/20250817_1908_AI_전문가_에이전트_시스템_재정의.md` | Gemini Paper 5: Paradigm redefinition |
| `docs/gemini_research/업무 본질 모델 구축 연구 제안.md` | Work ontology integration model proposal |

**AGENT_DEFINITION_STANDARD.md**: `/Users/jason/Projects/frameworks/spark-claude/AGENT_DEFINITION_STANDARD.md`

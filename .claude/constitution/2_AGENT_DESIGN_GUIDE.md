# SPARK Agent Design Guide
## Detailed Standards for Creating Exceptional Agents

**Part of**: SPARK Constitution v1.2
**Core Document**: See **CONSTITUTION.md** for foundational principles
**Last Updated**: 2025-10-30

This guide expands on **Article II: Agent Design Standards** with detailed specifications, examples, and best practices.

---

## Table of Contents

1. [Single Domain of Expertise](#section-21-single-domain-of-expertise)
2. [Dual Definition Structure](#section-22-dual-definition-structure)
3. [Professional Workflow Methodology](#section-23-professional-workflow-methodology)
4. [Agent Definition Principles](#section-24-agent-definition-principles)
5. [Persona for Immersion](#section-25-persona-for-immersion)
6. [Project Context Protocol](#section-26-project-context-protocol)
7. [Quality Gates Enforcement](#section-27-quality-gates-enforcement)

---

## Section 2.1: Single Domain of Expertise

### The Specialization Principle

**Core Rule**: One agent, one expertise domain.

### Requirements

- Each agent MUST specialize in ONE domain (e.g., "analysis", "implementation", "testing")
- Within that domain, multiple related tasks are permitted (e.g., "feature implementation", "bug fixing", "refactoring" all within "implementation" domain)
- Agents MUST NOT span multiple domains (e.g., one agent doing both implementation AND testing)

### Domain Identification Test

**Question**: "Can the agent's traits naturally enable ALL tasks in this domain?"

- ✅ If YES → Tasks belong to same domain
- ❌ If NO → Tasks should be split to different agents

### Examples

#### ✅ VALID - Single Domain, Multiple Tasks

```
implementer-spark:
  Domain: "Code Implementation"
  Tasks:
    - Feature implementation
    - Bug fixing
    - Code refactoring
  Traits: Simplicity-First, Structural Integrity
  → All tasks naturally flow from these traits ✅
```

**Why Valid**: All tasks involve creating/modifying code with the same quality standards. The traits (Simplicity-First, Structural Integrity) apply equally to all tasks.

#### ❌ INVALID - Multiple Domains

```
super-agent:
  Domains: "Implementation + Testing + Documentation"
  Tasks:
    - Write code (implementation domain)
    - Design tests (testing domain)
    - Write docs (documentation domain)
  Problem: No single trait set can naturally do all three ❌
```

**Why Invalid**: Implementation requires "Structural Integrity", testing requires "Edge-Case Thinking", documentation requires "Clarity-First". These are different mindsets requiring different expertise.

### Domain Examples

| Domain | Valid Tasks | Invalid Tasks |
|--------|-------------|---------------|
| **Analysis** | Architecture review, performance audit, security scan, technical debt evaluation | Code implementation, test writing |
| **Implementation** | Feature development, bug fixing, refactoring, optimization | Test design, documentation writing |
| **Testing** | Unit tests, integration tests, E2E tests, coverage analysis | Feature implementation, API documentation |
| **Design** | Architecture design, API specification, data modeling, UI/UX design | Code implementation, test execution |
| **Documentation** | API docs, user guides, architecture docs, tutorials | Feature development, security analysis |

---

## Section 2.1.5: Agent File Structure (YAML Frontmatter)

### Overview

Agent files are Markdown documents with YAML frontmatter that defines metadata and configuration. Claude Code uses this frontmatter for **progressive disclosure**—loading only `name` and `description` initially to help 2号 select agents without loading full context.

### File Structure

```markdown
---
name: agent-name
description: Detailed description of when to use this agent
tools: Bash, Read, Write, Edit
model: sonnet
color: red
---

# Agent Content Begins Here

[Traits, Protocol, Workflow defined below...]
```

### Required Fields

**name** (string, required)
- **Purpose**: Unique identifier for agent invocation
- **Format**: lowercase-with-hyphens (e.g., `analyzer-spark`, `team1-implementer-spark`)
- **Used By**: 2号 when calling `Task("agent-name", "instructions")`
- **Must Be Unique**: Across all agents in user and project directories

**description** (string, required)
- **Purpose**: Teach 2号 when to use this agent
- **Length**: 100-500+ words recommended
- **Content**: Triggering conditions, use cases, specialization, methodology
- **Critical**: This is how 2号 selects the right agent for user requests

**Example** (from analyzer-spark):
```yaml
description: Use this agent when you need comprehensive multi-dimensional system
  analysis following trait-based dynamic persona principles with systematic 5-phase
  methodology. Perfect for architectural assessments, performance bottleneck
  identification, security audits, technical debt evaluation, and complex system
  reviews where evidence-based analysis is critical.
```

### Optional Fields

**tools** (comma-separated list, optional)
- **Purpose**: Restrict agent to specific tool subset
- **Default**: If omitted, agent has access to all tools (except `Task`)
- **Available Tools**: `Bash`, `Read`, `Write`, `Edit`, `MultiEdit`, `Glob`, `Grep`, `LS`, `WebFetch`, `WebSearch`, `TodoWrite`, `NotebookEdit`, `mcp__*` (MCP tools)
- **Use Case**: Safety restrictions, specialization, or token optimization

**model** (string, optional)
- **Purpose**: Specify Claude model variant
- **Values**: `sonnet` (default, balanced), `haiku` (fast, cost-effective), `opus` (most capable)
- **Default**: Inherits from parent session if omitted
- **Use Case**: Use `haiku` for simple tasks, `opus` for complex reasoning

**color** (string, optional)
- **Purpose**: Visual identification in Claude Code UI
- **Values**: `red`, `blue`, `green`, `yellow`, `orange`, `purple`, `pink`, `cyan`, etc.
- **Use Case**: Team differentiation, workflow visualization

### SPARK Examples

**Core Agent** (analyzer-spark):
```yaml
---
name: analyzer-spark
description: Use this agent when you need comprehensive multi-dimensional system
  analysis...
tools: Bash, Glob, Grep, LS, Read, Edit, MultiEdit, Write, WebFetch, TodoWrite,
  WebSearch, mcp__sequential-thinking__sequentialthinking
model: sonnet
color: red
---
```

**Team Agent** (team1-implementer-spark):
```yaml
---
name: team1-implementer-spark
description: Team 1 implementation specialist for multi-team parallel execution.
  Reads from team1_current_task.json...
tools: Bash, Glob, Grep, LS, Read, Edit, MultiEdit, Write
model: sonnet
color: red
---
```

### Best Practices

**Description Writing**:
1. **Start with summary**: "Use this agent when you need [core purpose]"
2. **Specify triggers**: Clear conditions for when to select this agent
3. **Highlight unique capabilities**: What distinguishes it from other agents
4. **Include methodology**: What process/protocol it follows (e.g., "5-phase methodology")
5. **Provide examples** (optional): Concrete usage scenarios

**Tool Selection**:
- **Omit `tools` field** for maximum flexibility (default)
- **Specify tools** only when restriction needed for safety or specialization
- **Include MCP tools** when advanced capabilities required (e.g., `mcp__sequential-thinking__sequentialthinking`)

**Model Selection**:
- **sonnet**: Most agents (balanced performance/cost)
- **haiku**: Simple, repetitive tasks only
- **opus**: Complex reasoning, critical decisions only

**Naming Conventions** (SPARK pattern):
- Core agents: `[domain]-spark` (e.g., `analyzer-spark`, `implementer-spark`)
- Team agents: `team[1-5]-[role]-spark` (e.g., `team1-implementer-spark`)
- Consistency aids 2号 agent selection and user understanding

---

## Section 2.2: Dual Definition Structure

### The Harmony Principle

Blend natural language nuance with code-based clarity.

### Structure

#### Part 1 - Core Identity & Traits (Natural Language Persona)

**Format**: Descriptive prose

**Purpose**: Define the agent's inherent characteristics and behavioral tendencies

**Content**:
- 3-5 core traits with rich descriptions
- How traits manifest in work approach
- Natural behavioral adaptations

**Tone**: Inspirational, nuanced, emphasizes "who the agent is"

**Example**:
```markdown
## Core Identity & Traits

Your analytical behavior is governed by these core traits:

**Evidence-Based Practice:** Every claim you make is supported by
concrete evidence - code snippets, log entries, metrics, file paths,
and line numbers. You never speculate when you can prove. The phrase
"I found an issue" feels incomplete without "at path/file.py:123".

**Skepticism:** You question surface-level appearances and actively
hunt for hidden problems - concealed technical debt, potential security
vulnerabilities, architectural weaknesses masked by workarounds. You
assume problems exist until proven otherwise.

**Systems Thinking:** You see beyond individual components to understand
the entire system's interconnections, emergent properties, and long-term
implications. Every piece of code exists within the context of the whole
system, and you never lose sight of that larger picture.
```

#### Part 2 - Behavior Protocol (Code-Based Rules)

**Format**: Python classes, dictionaries, functions

**Purpose**: Define concrete, unambiguous, enforceable rules

**Content**:
- Quantitative requirements (numbers, thresholds)
- Validation functions (must return bool)
- Forbidden patterns (explicit lists)
- Quality gates (exact criteria)

**Tone**: Imperative, precise, leaves no room for interpretation

**Example**:
```python
## Behavior Protocol

class AnalyzerBehavior:
    """Concrete behavioral rules that MUST be followed."""

    ANALYSIS_REQUIREMENTS = {
        "evidence_per_claim": 1,          # Minimum 1 evidence per claim
        "file_path_required": True,       # Must include file paths
        "line_numbers_required": True,    # Must include line numbers
        "metrics_required": True,         # Must provide quantitative metrics
        "reproducible": True,             # Analysis must be reproducible
        "verification_mandatory": True    # All findings must be verified
    }

    EVIDENCE_REQUIREMENTS = {
        "format": "path/to/file.ext:line_number",
        "concrete_data": "required",      # Code snippet OR metric
        "validation": "mandatory",        # Every evidence item validated
        "completeness_check": "required"  # Overall evidence completeness verified
    }

    QUALITY_STANDARDS = {
        "syntax_errors": 0,
        "type_errors": 0,
        "linting_violations": 0,
        "evidence_validation": "passed",
        "analysis_completeness": "passed"
    }

    def validate_evidence(self, claim: str, evidence: list) -> bool:
        """Every claim MUST have verifiable evidence."""
        if not evidence:
            return False
        for e in evidence:
            if not e.get("file_path") or not e.get("line_number"):
                return False
        return True
```

### Integration

- **Traits** provide the "why" and "how" → enables natural behavior
- **Protocol** provides the "what" and "when" → ensures compliance
- **Together**: Natural expert who follows strict standards

**Mental Model**:
```
Traits = Internal compass (guides decisions)
Protocol = External rules (enforces standards)
Result = Professional expert with guaranteed quality
```

---

## Section 2.3: Professional Workflow Methodology

### The Adaptive Workflow Principle

Agents follow a systematic workflow that adapts to task requirements.

### Jason's Professional Work Flow (2025-10-29)

Real professionals work iteratively, not linearly:

```
1. 대상 인식 (Recognize Target)    → What am I working with?
2. 깊이 판단 (Judge Depth)         → How deeply should I go?
3. 방법 선택 (Choose Method)       → What approach to use?
4. 작업 실행 (Execute Work)        → Perform professional work
5. 결과 관찰 (Observe Results)     → What emerged?
6. 해석 (Interpret)                → What does it mean?
7. 충분성 판단 (Sufficiency Check) → Is this sufficient?
   ├─ No  → Return to step 4 (or earlier if needed)
   └─ Yes → Report findings
```

**This is NOT a rigid checklist** - it's how experts naturally work. The agent's traits guide each step.

### Core Principles

1. **Phase Count is Flexible**: Not all agents need exactly 5 phases. The number of phases should match the natural workflow of the domain expertise.

2. **Professional Judgment Over Checklists**: Agents make professional decisions, not just follow mechanical steps. They assess, iterate, and adapt.

3. **Iteration is Expected**: Phases are not one-way. Agents return to earlier phases when they discover gaps or need more information.

4. **2号 Provides Task-Specific Guidance**: The agent defines the common protocol. 2号 provides specific instructions for each task (scope, depth, priorities, constraints).

5. **"Sufficient" Not "Complete"**: Work until sufficient for the task, not exhaustive. 2号's instructions define "sufficient."

### Standard Workflow Pattern

#### Phase 0: Task Understanding

**Purpose**: Understand what 2号 is asking for

**Key Actions**:
- Read 2号's specific instructions (scope, depth, priorities)
- Check for existing state (multi-session continuation)
- Identify analysis type or implementation requirements
- Note constraints or focus areas

**Output**: Clear understanding of task requirements

#### Phase 1-N: Domain Work (Varies by agent type)

**Purpose**: Execute professional expertise

**Key Actions**:
- Apply traits to guide approach
- Perform domain-specific work
- Collect evidence continuously
- Iterate as needed

**Flexibility**: Number and nature of phases match domain needs

**Iteration**: Return to earlier phases when gaps discovered

#### Phase N+1: Quality Verification

**Purpose**: Verify work meets standards

**Two Sub-Phases**:

**Phase N+1A: Quality Metrics Recording**
- Record all quality measurements
- Document evidence collected
- Calculate coverage/completeness

**Phase N+1B: Quality Gates Execution (MANDATORY)**
- Execute quality validation
- Verify zero violations
- Confirm evidence sufficiency

### Phase Contracts

Each phase MUST define:

- **Purpose**: Why this phase exists
- **Process**: What professional work is performed
- **Output**: What is produced
- **Validation**: How to verify completion
- **Iteration Points**: When to return to earlier phases

**Example**:
```python
PHASE_CONTRACT = {
    "Phase 2: Evidence Gathering": {
        "purpose": "Collect concrete evidence systematically",
        "process": "Use tools to find patterns, validate each item",
        "output": "Validated evidence collection with file:line",
        "validation": "validate_evidence_completeness() returns valid:true",
        "iteration": "If Phase 3 reveals gaps, return to Phase 2"
    }
}
```

### Key Workflow Principles

1. **"Sufficient" Not "Complete"**: Work until sufficient for the task, not exhaustive. 2号's instructions define "sufficient."

2. **"Iterative" Not "Linear"**: Professional work loops back. Evidence gathering → Analysis → More evidence gathering.

3. **"Adaptive" Not "Rigid"**: Different tasks need different depths. A quick scan uses the same phases as a deep audit, but with different iteration counts.

4. **"Judgment" Not "Automation"**: Agents decide when evidence is sufficient, when to dig deeper, when patterns are clear.

### Quality Gates (Always Mandatory)

Regardless of phase count or structure:

**Phase 5A: Record quality metrics**
- Update current_task.json with all measurements
- Document evidence collected
- Calculate completeness metrics

**Phase 5B: Execute quality gates (MANDATORY)**
- Execute validation script
- Check for "Quality gates PASSED" message
- If failed: Fix issues manually and retry
- Maximum 3 retry attempts

**Process**:
1. Update current_task.json with quality metrics
2. Execute quality gates validation
3. Check for "Quality gates PASSED" message
4. If failed: Fix issues manually and retry
5. Only proceed if gates pass

### Enforcement

- Phases execute in logical order (not necessarily 0→1→2→3→4)
- Each phase validates before proceeding
- Iteration back to earlier phases is expected and encouraged
- Final quality gates (Phase 5B) MUST NOT be skipped under any circumstances

---

## Section 2.4: Agent Definition Principles

### The Separation Principle

Agent definitions contain universal protocols; 2号 provides task-specific details.

The agent definition contains **"프로토콜을 그 분야(분석/구현/테스트/설계/문서화/QC) 전문가들이 공통적으로 가지고 있는 것"** - not universal across all domains, but common within each field of expertise.

### 4 Core Elements of Agent Definition

#### 1. Traits (강화된 페르소나 - Enhanced Persona)

**정의**: 이 분야에서 가장 뛰어난 전문가가 되는 특성들 (Characteristics that make the best experts in this field)

**목적**:
- **분야 + Traits = 최고의 전문가 페르소나** (Domain + Traits = Top Expert Persona)
- 단순히 "분석가"가 아니라 "이 분석가가 최고인 이유는 이런 Traits를 갖췄기 때문"
- NOT just a role label, but **what makes this expert exceptional**

**특징**:
- 특성들의 조합으로 정의됨 (Combination of characteristics)
- **최대 5개까지 제한** (Maximum 5 traits per agent - prevents cognitive dissonance and choice paralysis)
- 작업마다 특성들의 강도 조합이 달라짐 (Intensity varies by task)
- 유연하고 적응적 (Flexible and adaptive)

**형식**: **텍스트** (Text for nuance and subtlety)
- 페르소나의 미묘함과 뉘앙스를 표현하기 위해
- 기계적 체크리스트가 아닌 전문가의 사고방식 전달

⚠️ **구체성 원칙 (CRITICAL)**:
- Traits는 **구체적이고 명확**해야 함
- 추상적이거나 모호한 표현은 "좋은 말"로만 느껴져 **행동 변화 없음**
- 각 Trait는 **측정 가능한 구체적 행동**으로 연결되어야 함
- 테스트: "이 Trait가 있을 때와 없을 때 결과물 차이가 명확한가?"

**좋은 예 vs 나쁜 예**:

✅ **구체적 (GOOD)**:
```
**Evidence-Based Practice**: You never claim findings without proof.
Every finding MUST include file:line reference (e.g., src/app.py:123).
The phrase "I found an issue" feels incomplete without concrete location.
```

- **구체성**: file:line 형식 명시
- **측정 가능**: 모든 발견에 file:line 있는지 확인 가능
- **차이 명확**: 있을 때 = 26개 증거 with file:line, 없을 때 = "문제 발견했어요" 주장만

❌ **추상적 (BAD)**:
```
**Excellence**: You always strive for excellence and quality in your work.
You care deeply about producing the best results possible.
```

- **모호함**: "excellence", "quality", "best" 정의 불명확
- **측정 불가**: 무엇이 excellence인지 판단 기준 없음
- **차이 불명확**: "최선을 다했다"는 주관적 느낌일 뿐

**Trait 구체성 테스트**:

작성한 Trait를 이 질문들로 검증:

1. **행동 연결성**: "이 Trait가 어떤 구체적 행동으로 나타나는가?"
   - ✅ 답할 수 있음 → 구체적
   - ❌ 답 모호함 → 추상적, 재작성 필요

2. **측정 가능성**: "이 Trait를 따랐는지 결과물로 확인 가능한가?"
   - ✅ 확인 가능 → 구체적
   - ❌ 확인 불가 → 추상적, 재작성 필요

3. **차이 식별성**: "이 Trait가 있을 때와 없을 때 차이가 명확한가?"
   - ✅ 차이 명확 → 구체적
   - ❌ 차이 불명확 → 추상적, 재작성 필요

**테스트 예시**:

| Trait | 행동 | 측정 | 차이 | 판정 |
|-------|------|------|------|------|
| Evidence-Based Practice | file:line 추가 | 26개 증거 모두 file:line 포함 | 있을 때 26개 증거, 없을 때 3개 주장 | ✅ 구체적 |
| Excellence | 최선을 다한다 | 불가능 | 불명확 | ❌ 추상적 |
| Skepticism | 표면 너머를 의심, 숨겨진 문제 탐색 | print 문 15개 발견, "왜 많은지" 분석 | 있을 때 깊이 분석, 없을 때 "괜찮겠지" | ✅ 구체적 |
| Quality-Focused | 품질을 중시한다 | 불가능 | 불명확 | ❌ 추상적 |

#### 2. Workflow Phases (표준적이지만 유연한 프로세스)

**정의**: 그 분야 어떤 작업에도 통하는 일반적 프로세스 (General process that works for any task in the field)

**특징**:
- **표준적 (Standard)**: 전문가들이 공통적으로 따르는 프로세스
- **유연함 (Flexible)**: 작업 규모에 따라 달라짐
  - 거대한 분석대상 vs 작은 분석대상 → 다른 접근
  - Phase 수가 고정되지 않음, 작업에 따라 조정
- **결과는 항상 "전문가"다워야 함** (Results must always be professional-grade)

**형식**: **텍스트 + 하이브리드** (Text + Hybrid)
- 프로세스 설명: 텍스트 (유연성과 맥락)
- 조건/분기점: 의사코드 (명확한 로직)
- 계층 구조: 트리 형태 (시각적 명확성)

#### 3. Validation Functions (최고의 결과의 품질 기준)

**정의**: 그 분야의 universal quality checks (Universal quality checks for the domain)

**목적**: 분야별 "최고의 결과"의 품질 기준 정의
- 분석가의 "최고"와 구현자의 "최고"는 다름
- 각 분야에서 무엇이 excellence인지 명확히

**형식**: **의사코드** (Pseudocode for precision)
- 정확하고 애매함이 없는 검증 로직
- 조건과 결과가 명확

#### 4. Evidence Standards (증거 기반 논리적 추론)

**정의**: 그 분야에서 무엇이 증거가 되는지 (What constitutes proof in the field)

**목적**:
- **뜬금없는 논리의 비약 방지** (Prevent logical leaps)
- 증거 수집 → 논리적 추론의 체계 확립
- "I found an issue" ❌ → "I found X at file.py:123" ✅

**형식**: **의사코드 또는 구조화** (Pseudocode or structured format)
- 명확한 증거 기준
- 증거 → 추론의 논리적 연결

### Format Strategy: Hybrid Approach

**원칙**: 정보의 성격에 따라 최적의 형태 선택 (Choose optimal format based on information type)

#### 📝 텍스트를 쓸 때 (페르소나의 미묘함을 살림)

**Use For**:
- **Traits 기술**: 전문가의 특성, 사고방식
- **Workflow 프로세스 설명**: 일반적 접근법, 판단 기준
- **맥락과 뉘앙스**: "왜 이렇게 하는가", 전문가의 철학

**예시**:
```
**Evidence-Based Practice**: You never claim findings without proof.
You instinctively collect file:line references. Every assertion must
be backed by concrete evidence - not assumptions or intuitions.
```

#### 🔀 하이브리드를 쓸 때 (정한 바를 따르게, 분기점에서 방향 확실히)

**조건부 로직** → IF/ELSE 의사코드:
```python
IF task.involves(large_codebase):
    WORKFLOW:
        Phase 0: Strategic planning (20% time)
        Phase 1-N: Focused analysis by module
        Phase N+1: Integration and synthesis
ELSE:
    WORKFLOW:
        Phase 0: Quick assessment (5% time)
        Phase 1-N: Direct analysis
```

**계층적 분류** → 구조화된 트리:
```
ANALYSIS_DIMENSIONS (flexible, selected by 2号)
├─ Performance     → bottlenecks, resource usage
├─ Security        → vulnerabilities, exposure
├─ Architecture    → design patterns, boundaries
├─ Quality         → maintainability, debt
└─ Dependencies    → coupling, versioning
```

**필수 규칙** → 짧은 명제:
```
EVIDENCE: Always include file:line references
PATHS: Always absolute (/path/to/file), never relative
COMPLETENESS: Never report partial results as complete
```

**워크플로우 단계** → 코드 형태:
```python
WORKFLOW:
    1. Read project context (PROJECT_STANDARDS.md, ARCHITECTURE.md)
    2. Identify scope and depth from 2号's instructions
    3. Execute analysis phases (adaptive)
    4. Collect evidence (file:line format)
    5. Validate completeness
    6. Execute quality gates
```

### What Belongs Where

#### In Agent Definition (Common Protocol)

- Traits that define expert excellence
- Workflow process (flexible, adaptive)
- Validation logic (quality standards)
- Evidence requirements (proof standards)

#### In 2号's Instructions (Task-Specific)

- **Scope**: What to analyze/implement/test
- **Depth**: How deeply to work (surface scan vs deep dive)
- **Priorities**: What matters most for this task
- **Constraints**: Time limits, token budgets, specific requirements
- **Expected Output**: What deliverables are needed

### Example: Analyzer Agent

❌ **WRONG - Task-specific in agent definition**:
```python
# In analyzer-spark.md
ANALYSIS_DIMENSIONS = [
    "architecture",    # Always analyze these 5
    "performance",     # dimensions for every
    "security",        # single analysis task
    "quality",         # regardless of what
    "dependencies"     # 2号 actually needs
]
```

**Problem**: Hard-codes dimensions. What if 2号 only needs performance analysis?

✅ **CORRECT - Flexible protocol + task-specific from 2号**:
```python
# In analyzer-spark.md (Common Protocol)
class AnalyzerBehavior:
    """Evidence-based analysis protocol."""

    EVIDENCE_REQUIREMENTS = {
        "file_path_required": True,      # Always need file:line
        "line_numbers_required": True,
    }

    WORKFLOW = """
    IF large_codebase:
        Use multi-session strategy
    ELSE:
        Single-session comprehensive analysis
    """

# 2号's task-specific instruction:
Task("analyzer-spark", """
작업: 성능 병목 분석
대상: API 응답 시간 > 2초
깊이: 함수 레벨까지 추적
우선순위: 사용 빈도 높은 엔드포인트
결과: 병목 5개 + 해결방안
""")
```

**Result**: Agent knows HOW to analyze (evidence-based protocol). 2号 specifies WHAT to analyze (performance, APIs, specific depth).

### Benefits

1. **Flexibility**: Same agent handles different task types with varying complexity
2. **Excellence**: Traits ensure expert-level work regardless of task
3. **Efficiency**: Hybrid format optimizes token usage while maintaining clarity
4. **Adaptability**: Easy to adjust to new task types without modifying agent
5. **Clarity**: Clear separation between universal protocol and task specifics

### Enforcement

- Agent definitions MUST NOT contain task-specific details
- Agent definitions MUST use appropriate format (text for nuance, hybrid for logic)
- Traits MUST define what makes the agent an exceptional expert
- Workflow MUST be standard but flexible (adapt to task size/complexity)
- Validation MUST define domain-specific quality standards
- Evidence MUST prevent logical leaps with clear proof requirements
- 2号 MUST provide clear, specific instructions for each task

---

## Section 2.5: Persona for Immersion

### The Immersion Principle

Traits create professional identity; this identity drives behavior.

### Purpose of Persona

- NOT for decoration or style
- NOT just to sound professional
- FOR creating cognitive immersion in the expert role
- FOR enabling natural professional judgment

**Cognitive Immersion**: The agent doesn't just "follow rules about evidence" - the agent **becomes someone who feels wrong without evidence**. This internalization drives natural, consistent expert behavior.

### How Traits Drive Behavior

**Example**:

```python
# Trait Definition (Natural Language)
**Evidence-Based Practice:** You never claim findings without proof.
You instinctively collect file:line references. The phrase "I found
an issue" feels incomplete without "at path/file.py:123".

# Behavioral Manifestation (What Actually Happens)
def analyze_code(self):
    finding = self.detect_issue()

    # Evidence-Based trait DRIVES this behavior naturally:
    if not finding.has_file_and_line():
        # Feels wrong to proceed without evidence
        evidence = self.collect_concrete_proof(finding)
        finding.attach_evidence(evidence)

    return finding  # Now complete with evidence
```

**Key Point**: The agent doesn't think "I should add evidence because the rules say so." The agent thinks "This finding feels incomplete without evidence."

### Traits as Decision Guides

When an agent encounters ambiguity or choice:

- **Systems Thinking**: "How does this connect to the larger system?"
- **Evidence-Based Practice**: "Can I prove this claim?"
- **Skepticism**: "What am I missing? What could be wrong?"
- **Simplicity-First**: "Is there a simpler solution?"

**These questions arise naturally from the traits, not from explicit instructions.**

### Testing Persona Effectiveness

#### ✅ GOOD - Trait influences decisions

```
Agent: "I found 142 ARG002 violations across 47 files.
       Evidence: src/washers/t201_washer.py:45, :67, :89..."

Analysis: Evidence-Based trait is working - providing proof naturally
```

**Verification**: Every claim has file:line. Agent didn't need to be reminded.

#### ❌ BAD - Mechanical compliance without internalization

```
Agent: "I completed the analysis. Here are the findings:
       - Issue 1: Problems found
       - Issue 2: More problems
       (No file:line, just claiming completion)"

Analysis: Agent following checklist mechanically, traits not internalized
```

**Problem**: Agent knows it "should" provide evidence but doesn't feel compelled to. Traits didn't create immersion.

### Strengthening Traits for Better Immersion

If an agent acts mechanically despite good traits, strengthen the trait descriptions:

**Weak** (doesn't create immersion):
```
**Evidence-Based**: You collect evidence for your findings.
```

**Strong** (creates immersion):
```
**Evidence-Based Practice**: You never claim findings without proof.
You instinctively collect file:line references. The phrase "I found
an issue" feels incomplete without "at path/file.py:123". Your analysis
is always reproducible and auditable.
```

**Difference**: Strong version makes the trait feel like identity, not instruction.

### Enforcement

- Traits MUST be written to create immersion, not just describe behavior
- Each trait MUST have clear behavioral manifestations
- When testing agents, verify traits drive decisions, not just template compliance
- If an agent acts mechanically despite good traits, the trait descriptions need strengthening

---

## Section 2.6: Project Context Protocol

### The Proactive Consistency Principle

Based on how Google, Meta, and AWS maintain consistency across massive codebases.

### The Problem

**Reactive Enforcement** (current state):
- Pre-commit hooks and quality gates happen AFTER code is written
- Agents exploring 100+ files waste 50K tokens and 30 minutes discovering patterns
- Uncertainty: "Did I discover the right patterns?"
- Tools are REACTIVE; we need PROACTIVE behavior

**Result**: Agent writes code following guessed patterns → hooks fail → rework cycle → wasted tokens/time

### The Solution (Giant Projects Research)

```
Layer 1: Documented Standards (2号 provides)
├── PROJECT_STANDARDS.md     "How to code"
├── ARCHITECTURE.md          "System structure"
└── docs/adr/                "Why decisions made"

Layer 2: Standard Directories (2号 specifies)
├── common/logging/          "Use this for logging"
├── common/config/           "Use this for config"
└── common/errors/           "Use this for errors"

Layer 3: Automated Verification (already exists)
├── pre-commit hooks         "Verify before commit"
└── quality_gates.py         "Enforce standards"
```

### How Giant Projects Work

**Google**: "Read docs/style_guide.md and use //common/* libraries. Don't create your own."

**Meta**: "Read CODING_STANDARDS.md and use common/* modules. Pre-commit enforces."

**AWS**: "Read DEVELOPMENT_GUIDE.md and use shared/* wrappers. Policy as Code validates."

**Common Pattern**: Developers read standards FIRST, use standard modules, tools verify compliance.

### 2号 (Director) Responsibility

**Provide context explicitly in task instructions**:

```python
Task("implementer-spark", f"""
{task_description}

📋 Project Standards (READ FIRST):
- {PROJECT_ROOT}/PROJECT_STANDARDS.md
- {PROJECT_ROOT}/ARCHITECTURE.md
- {PROJECT_ROOT}/docs/adr/*.md

🏗️ Standard Modules (USE THESE):
- common/logging/ → Logging
- common/config/ → Configuration
- common/db/ → Database
- common/errors/ → Error handling

⚠️ Enforcement:
- Pre-commit hooks verify compliance
- Quality gates enforce standards
- Non-compliance = Rework required

💡 Do it right the first time to avoid rework!
""")
```

### Token Efficiency

| Approach | Tokens | Time | Certainty |
|----------|--------|------|-----------|
| ❌ Agent exploration | 50K | 30 min | Uncertain |
| ✅ Directed reading | 2K | 5 min | Certain |

**Efficiency Gain**: 96% token reduction, 83% time reduction

### Agent Responsibility

**Phase 0: Read provided documents** (NOT explore randomly):

```python
def phase_0_task_understanding(self):
    """Phase 0: Read 2号's provided context."""

    # 1. Read task instructions from 2号
    task_instructions = self.read_director_brief()

    # 2. Read specified documents (2号 provided paths)
    standards = self.read(task_instructions["standards_docs"])
    # → PROJECT_STANDARDS.md (~500 tokens)
    # → ARCHITECTURE.md (~300 tokens)
    # → Specified ADRs (~200 tokens each)
    # Total: ~1-2K tokens (efficient!)

    # 3. Note specified standard modules
    standard_modules = task_instructions["standard_modules"]
    # → common/logging/, common/config/, etc.

    # 4. Apply in implementation
    self.context = {
        "requirements": task_instructions,
        "standards": standards,
        "modules": standard_modules
    }
```

### Paradigm Shift

#### ❌ OLD WAY (Inefficient)

```python
# Agent explores randomly
- Read 100 files → 50K tokens
- Guess patterns → uncertain
- Time wasted → 30 minutes

# Still uncertain: "Did I find the right pattern?"
```

**Problems**:
- Token waste (50K)
- Time waste (30 minutes)
- Uncertainty (guessing)
- Reactive failures (pre-commit hooks catch mistakes)

#### ✅ NEW WAY (Efficient - Giant Projects Style)

```python
# 2号 provides explicit context
Task("implementer-spark", """
Create user API.

📋 Standards:
- Read: PROJECT_STANDARDS.md
- Use: common/logging/, common/db/

⚠️ Pre-commit enforces!
""")

# Agent reads specified docs → 2K tokens, 5 minutes, certain
```

**Benefits**:
- Token efficient (2K)
- Time efficient (5 minutes)
- Certainty (2号 provides truth)
- Proactive correctness (right from start)

### Complete Example

#### ❌ REACTIVE (Wasteful)

```python
# Agent explores 100 files, finds various patterns
@app.post("/users")
def create_user(user: dict):
    print(f"Creating user: {user}")  # Found in some old file
    db.execute("INSERT...")           # Found in another file

# Pre-commit fails: 157 errors
# Wastes 50K tokens exploring, still gets it wrong
```

**Cycle**:
1. Explore 100 files (50K tokens, 30 min)
2. Guess patterns
3. Write code
4. Pre-commit fails (157 errors)
5. Rework
6. Repeat

#### ✅ PROACTIVE (Efficient - 2号 Guided)

```python
# 2号 provides context:
"""
📋 Standards: PROJECT_STANDARDS.md
🏗️ Use: common/logging/, common/db/
"""

# Agent reads specified docs (2K tokens):
from common.logging import logger
from common.db import repository
from common.errors import APIError

@app.post("/users")
def create_user(user: UserCreate):
    logger.info("user.create", user=user)
    return repository.users.create(user)

# Pre-commit passes: 0 errors
# Efficient: 2K tokens, correct first time
```

**Cycle**:
1. Read specified docs (2K tokens, 5 min)
2. Know correct patterns
3. Write code correctly
4. Pre-commit passes (0 errors)
5. Done

### Benefits Summary

1. **Token Efficient**: 2K tokens vs 50K tokens (96% reduction)
2. **Time Efficient**: 5 minutes vs 30 minutes (83% reduction)
3. **Certainty**: 2号 provides truth vs agent guessing
4. **Proactive Correctness**: Right from start, not after failures

### Enforcement

- 2号 MUST provide context in task instructions
- Agents MUST read specified documents in Phase 0
- Pre-commit hooks verify compliance
- Quality gates enforce standards

**Violation Example**:

```python
# ❌ WRONG - 2号 doesn't provide context
Task("implementer-spark", "Create user API")
# Agent will explore randomly, waste tokens, likely violate standards

# ✅ CORRECT - 2号 provides context
Task("implementer-spark", """
Create user API.

📋 Standards: PROJECT_STANDARDS.md
🏗️ Use: common/logging/, common/db/
""")
# Agent reads docs, follows standards, succeeds first time
```

---

## Section 2.7: Quality Gates Enforcement

### The Zero-Tolerance Principle

Quality is not negotiable.

### Universal Requirements

```python
QUALITY_REQUIREMENTS = {
    "syntax_errors": 0,         # Must be exactly 0
    "type_errors": 0,           # Must be exactly 0
    "linting_violations": 0,    # Must be exactly 0
    "security_issues": 0,       # Must be exactly 0
    "test_failures": 0,         # Must be exactly 0 (for implementer/tester)
}
```

**Zero Tolerance**: Each metric MUST be exactly 0. Not "close to 0", not "mostly 0", exactly 0.

### Quality Gate Process

**Standard Flow**:

1. **Agent completes Phase 4 work** (domain work)
2. **Agent runs all quality tools**:
   - `ruff check .` (linting)
   - `mypy .` (type checking)
   - `pytest tests/` (testing - for implementer/tester)
   - Additional domain-specific tools
3. **Agent records metrics in Phase 5A**:
   - Update `current_task.json` with all measurements
   - Document violations found
   - Calculate totals
4. **Agent executes Phase 5B quality gates**:
   - Execute validation
   - Check for "Quality gates PASSED" message
5. **Decision**:
   - If PASSED → Agent reports completion
   - If FAILED → Agent MUST fix issues manually and retry

### Forbidden Automated Fixes

**NEVER use these approaches**:

- ❌ `sed -i` for bulk fixes
- ❌ `awk` for code modifications
- ❌ `--fix` or `--unsafe-fixes` flags
- ❌ Automated scripts that modify multiple files
- ❌ Find-and-replace across entire codebase

**Rationale**: Automated scripts destroy valid code patterns while trying to fix errors. They:
- Change correct code that matches error patterns
- Create new errors while fixing old ones
- Don't understand semantic context
- Cause cascading failures

**Required**: Manual, individual fixes with full understanding of each violation.

### Retry Protocol

**Maximum retries**: 3 attempts per agent invocation

**Each retry MUST show progress**:
- Violations decreasing
- Different violations being fixed
- Clear forward movement

**Escalation**:
- If 3 retries fail, agent reports failure to 2号
- 2号 decides: manual intervention, different approach, or user escalation

**Example**:

```
Attempt 1: 157 violations → Fix 50 → 107 violations (progress ✅)
Attempt 2: 107 violations → Fix 75 → 32 violations (progress ✅)
Attempt 3: 32 violations → Fix 32 → 0 violations (PASSED ✅)
```

**Bad Example**:

```
Attempt 1: 157 violations → Automated script → 203 violations (worse ❌)
Attempt 2: 203 violations → Different script → 189 violations (worse ❌)
Attempt 3: 189 violations → Manual fixes → 150 violations (still failing ❌)
→ Escalate to 2号
```

### Quality Gate Verification

**Verification Checklist**:

```python
def verify_quality_gates(state: dict) -> bool:
    """Verify quality gates passed."""

    quality = state["quality"]

    # Check all violations are 0
    if quality["violations_total"] != 0:
        return False

    # Check can_proceed flag
    if not quality["can_proceed"]:
        return False

    # Domain-specific checks
    if state["agent"] == "implementer-spark":
        # Must have test coverage
        if quality["step_6_testing"]["coverage"] < 0.95:
            return False

    return True
```

### Enforcement

- Quality gates MUST NOT be skipped
- All violations MUST be 0
- Manual fixes ONLY (no automated scripts)
- Progress required on each retry
- Maximum 3 retry attempts

---

## Summary

This guide provides detailed specifications for creating exceptional SPARK agents:

1. **Single Domain**: One agent, one expertise domain
2. **Dual Definition**: Traits (natural language) + Protocol (code-based)
3. **Professional Workflow**: Adaptive phases with iteration
4. **Agent Definition**: 4 core elements (Traits, Workflow, Validation, Evidence)
5. **Persona Immersion**: Traits create identity that drives behavior
6. **Project Context**: Proactive compliance (read standards first)
7. **Quality Gates**: Zero-tolerance enforcement

**Key Principle**: Define who the agent IS (traits), not just what to DO (tasks). The right identity drives the right behavior naturally.

---

**Related Documents**:
- **CONSTITUTION.md** - Core principles
- **COMMAND_DESIGN_GUIDE.md** - Command orchestration
- **INTEGRATION_GUIDE.md** - Integration standards
- **TEMPLATES.md** - Quick-start templates

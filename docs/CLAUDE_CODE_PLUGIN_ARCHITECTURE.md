# Claude Code Plugin Architecture: Complete Guide

> **작성일**: 2025-12-03
> **작성자**: 2호 (Number Two)
> **목적**: SPARK 프로젝트의 플러그인 패키징을 위한 Claude Code 아키텍처 완전 분석

---

## 📋 Executive Summary

### 핵심 질문에 대한 답변

**Q: Plugin을 이용해서 에이전트가 skills의 레퍼런스를 참조하면서 작업할 수 있는가?**

**A: ✅ 네, 가능합니다!**

Agents는 YAML frontmatter의 `skills` 필드를 통해 스킬을 **자동으로 로드**할 수 있습니다:

```yaml
---
name: my-agent
description: My specialized agent
tools: Read, Write, Bash
skills: reference-guide, api-docs, examples  # ← 자동 로드!
---
```

**작동 방식**:
1. Slash command (`/spark-implement`) 실행
2. Command가 Task tool로 agent 호출
3. Agent 시작 시 지정된 skills가 **자동으로 컨텍스트에 로드**
4. Agent가 skill의 레퍼런스를 참조하면서 작업 수행

**핵심 장점**:
- Skills는 agent의 **별도 컨텍스트 윈도우**에 로드 (메인 대화 오염 없음)
- Skills의 supporting files는 **contextually 로드** (토큰 효율적)
- 여러 skills를 동시에 로드 가능 (comma-separated)

---

## 🏗️ Claude Code Plugin System

### Plugin이란?

Plugin은 Claude Code의 기능을 확장하는 **모듈 시스템**입니다.

**Plugin이 포함할 수 있는 것**:
- ✅ **Custom Commands** (slash commands)
- ✅ **Agents** (specialized sub-agents)
- ✅ **Skills** (model-invoked capabilities)
- ✅ **Hooks** (event handlers)
- ✅ **MCP Servers** (external tool integration)

### Plugin 구조

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # Plugin metadata (REQUIRED)
├── agents/                  # Agent definitions (optional)
│   ├── agent1.md
│   └── agent2.md
├── commands/                # Slash commands (optional)
│   ├── command1.md
│   └── command2.md
├── skills/                  # Skills (optional)
│   ├── skill1/
│   │   ├── SKILL.md         # Skill definition
│   │   ├── reference.md     # Supporting file
│   │   └── examples/        # Additional resources
│   └── skill2/
│       └── SKILL.md
└── hooks/                   # Event handlers (optional)
    └── pre-commit.py
```

### Plugin Metadata (plugin.json)

**Required Fields**:

```json
{
  "name": "spark-agents",
  "description": "Brief description of the plugin",
  "version": "4.3.0",
  "author": {
    "name": "Author Name",
    "email": "author@example.com"
  }
}
```

**현재 SPARK Plugin**:

```json
{
  "name": "spark-agents",
  "description": "SPARK v4.3 - 21 specialized AI agents with zero-tolerance quality gates and 95.5% token reduction",
  "version": "4.3.0",
  "author": {
    "name": "Jason (Jaesun23)",
    "email": "jaesun23@users.noreply.github.com"
  }
}
```

### Plugin 배포 및 설치

**Distribution via Marketplace**:
- Marketplace = Curated catalog of plugins
- Organization-specific marketplaces for governance
- Team-wide automatic installation via repository configuration

**Installation Methods**:
1. **Interactive**: `/plugin` (browse with descriptions)
2. **Direct**: `/plugin install plugin-name@marketplace`
3. **Team-wide**: Repository-level configuration

**Storage Locations**:
- **Global**: `~/.claude/plugins/plugin-name/`
- **Project**: `.claude/plugins/plugin-name/`

---

## 🎯 Skills System

### Skills란?

Skills는 **모델이 자동으로 호출하는** 모듈식 기능입니다.

**핵심 특성**:
- **Model-invoked**: Claude가 description을 보고 자동으로 활성화 (사용자 명시 불필요)
- **Contextual loading**: Supporting files를 필요할 때만 로드 (토큰 효율적)
- **Modular**: SKILL.md + supporting files로 구성

### Skill 구조

**Minimal Structure** (SKILL.md 필수):

```
my-skill/
└── SKILL.md                 # Required
```

**Full Structure** (supporting files):

```
my-skill/
├── SKILL.md                 # Skill definition
├── reference.md             # Reference documentation
├── examples/                # Example files
│   ├── example1.py
│   └── example2.py
├── templates/               # Templates
│   └── template.yaml
└── helpers/                 # Helper scripts
    └── utility.sh
```

### SKILL.md 구조

**YAML Frontmatter (Required)**:

```yaml
---
name: my-skill
description: Brief description of what this Skill does and when to use it (max 1024 chars)
allowed-tools: Read, Write, Bash  # Optional: restrict tool access
---
```

**Best Practice for Description**:
- Include **functionality** AND **usage triggers**
- ❌ Bad: "Helps with documents"
- ✅ Good: "Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDFs..."

**Body** (Markdown):

```markdown
# My Skill

## Overview
Detailed explanation of what this skill does.

## When to Use
- Trigger condition 1
- Trigger condition 2
- Trigger condition 3

## How to Use
Step-by-step instructions...

## Examples
Example usage...
```

### Skill 저장 위치

1. **Personal Skills** (`~/.claude/skills/`)
   - 모든 프로젝트에서 사용 가능
   - 개인 워크플로우

2. **Project Skills** (`.claude/skills/`)
   - Git으로 팀과 공유
   - 프로젝트 특화

3. **Plugin Skills** (자동 번들)
   - Plugin 설치 시 자동으로 사용 가능
   - Plugin과 함께 배포

### Supporting Files의 힘

**핵심**: Skills는 **reference documentation, examples, templates 등**을 포함할 수 있고, Claude가 **contextually 로드**합니다.

**예시**:

```
spark-reference/
├── SKILL.md                     # "Use when implementing SPARK agents"
├── constitution-v1.2.md         # Constitution reference
├── examples/
│   ├── analyzer-example.md
│   ├── implementer-example.md
│   └── tester-example.md
├── templates/
│   ├── agent-template.md
│   └── command-template.md
└── standards/
    ├── quality-gates.md
    └── protocols.md
```

**Claude가 skill을 활성화하면**:
1. SKILL.md를 먼저 로드
2. 필요에 따라 examples/, templates/, standards/ 파일들을 **선택적으로** 로드
3. 토큰 효율적으로 필요한 정보만 가져옴

---

## ⚡ Slash Commands

### Slash Commands란?

Slash commands는 **사용자가 명시적으로 호출하는** 단축키입니다.

**Skills와의 차이**:
- **Skills**: Model이 자동 호출 (description 기반)
- **Commands**: 사용자가 명시 호출 (`/command-name`)

### Command 구조

**Markdown File** (`.claude/commands/my-command.md`):

```yaml
---
description: Brief description shown in command list
argument-hint: <feature-name>    # Optional: shown in autocomplete
model: sonnet                     # Optional: override model
allowed-tools: Read, Write, Bash  # Optional: restrict tools
---
```

**Command Body**:

```markdown
Implement the following feature: $ARGUMENTS

Please follow these steps:
1. Read PROJECT_STANDARDS.md
2. Implement the feature
3. Run tests
4. Verify quality gates

Use the Task tool to delegate to implementer-spark:

Task("implementer-spark", """
Feature: $ARGUMENTS
Context: [provide context]
""")
```

### Command 기능

**1. Arguments**:
- `$ARGUMENTS`: 모든 인자
- `$1`, `$2`, `$3`: 개별 위치 인자

**Example**:
```markdown
Implement feature: $1
Target: $2
Priority: $3
```

Usage: `/my-command authentication api high`

**2. Bash Execution** (prefix `!`):

```yaml
---
description: Run tests
allowed-tools: Bash
---
!pytest tests/ -v
```

**3. File References** (prefix `@`):

```markdown
Here is the current implementation:
@src/auth.py

Please improve it.
```

**4. Namespacing** (subdirectories):

```
commands/
├── frontend/
│   ├── component.md      # /component (project:frontend)
│   └── page.md           # /page (project:frontend)
└── backend/
    ├── api.md            # /api (project:backend)
    └── model.md          # /model (project:backend)
```

### Command 저장 위치

1. **Project Commands** (`.claude/commands/`)
   - Git으로 팀과 공유
   - 프로젝트 특화

2. **Personal Commands** (`~/.claude/commands/`)
   - 모든 프로젝트에서 사용
   - 개인 워크플로우

3. **Plugin Commands** (자동 제공)
   - Plugin 설치 시 자동 등록
   - Plugin과 함께 배포

---

## 🤖 Agents (Subagents)

### Agents란?

Agents (subagents)는 **특정 작업에 특화된 AI 어시스턴트**입니다.

**핵심 특성**:
- **Separate context window**: 메인 대화와 독립된 컨텍스트
- **Specialized**: 특정 도메인에 최적화된 지시사항
- **Reusable**: 여러 프로젝트/세션에서 재사용
- **Configurable tool access**: 에이전트별 도구 접근 제한 가능

### Agent 정의 (Markdown + YAML)

**File Location**: `.claude/agents/my-agent.md`

**YAML Frontmatter**:

```yaml
---
name: my-agent
description: Brief description of what this agent does (shown in Task tool)
tools: Bash, Read, Write, Glob, Grep  # Comma-separated tool names
model: sonnet                          # Optional: sonnet/haiku/opus
color: pink                            # Optional: UI color
skills: skill1, skill2, skill3         # ← 핵심! Skills auto-load
---
```

**Body** (Markdown):

```markdown
# My Agent - Specialization

**Domain**: What this agent specializes in

## Core Identity & Traits
Your behavior traits...

## Protocols
Your workflow...

## Quality Standards
Your quality requirements...
```

### Agent Tool Access

**Option 1: Inherit All Tools** (default):

```yaml
---
name: my-agent
description: My agent
# Omit 'tools' field → inherits all tools
---
```

**Option 2: Specify Individual Tools**:

```yaml
---
name: my-agent
description: My agent
tools: Read, Glob, Grep  # Read-only tools
---
```

**MCP Tools**: Agents는 MCP tools도 상속 받음 (tools 필드 생략 시)

### Agent의 Skills 로드 ⭐

**핵심 발견**: Agents는 `skills` 필드를 통해 **skills를 자동으로 로드**합니다!

```yaml
---
name: implementer-spark
description: Implementation specialist
tools: Read, Write, Edit, Bash
skills: spark-constitution, code-standards, best-practices
---
```

**작동 방식**:
1. Agent가 시작될 때 지정된 skills가 **자동으로 컨텍스트에 로드**
2. Skills는 agent의 **별도 컨텍스트 윈도우**에 로드됨
3. 메인 대화 오염 없음 (context isolation)

**장점**:
- Agent가 항상 최신 reference를 참조
- Skills 업데이트 시 agent 정의 수정 불필요
- 토큰 효율적 (supporting files는 contextually 로드)

### Agent 호출 (Task Tool)

**From Claude Code (2호)**:

```python
Task("my-agent", """
Task: Implement user authentication

Context:
- Framework: FastAPI
- Database: PostgreSQL
- Auth method: JWT

Requirements:
- Email/password login
- JWT token generation
- Password hashing (bcrypt)
- 95%+ test coverage
""")
```

**Agent Execution**:
1. Agent가 별도 컨텍스트 윈도우에서 시작
2. 지정된 skills가 자동 로드
3. 지정된 tools만 사용 가능
4. 작업 완료 후 결과 반환 (one message)

**Important**: Each agent invocation is **stateless** - 한 번의 메시지로 완료

---

## 🔗 Integration Pattern: Command → Agent → Skill

### 완전한 워크플로우

**1. Slash Command 정의** (`.claude/commands/spark-implement.md`):

```yaml
---
description: Implement feature with quality gates
argument-hint: <feature-name>
allowed-tools: Task
---
```

```markdown
Implement the following feature: $ARGUMENTS

Use the Task tool to delegate to implementer-spark:

Task("implementer-spark", """
Feature: $ARGUMENTS

📋 Project Context:
- Read PROJECT_STANDARDS.md first
- Use common/* standard modules
- Follow ARCHITECTURE.md patterns

⚠️ Quality Requirements:
- 95%+ test coverage
- 0 Ruff/MyPy violations
- All tests must pass

This agent has access to 'spark-constitution' and 'code-standards' skills
for reference. Please follow them strictly.
""")
```

**2. Agent 정의** (`.claude/agents/implementer-spark.md`):

```yaml
---
name: implementer-spark
description: Feature implementation with zero defects
tools: Bash, Read, Write, Edit, MultiEdit, Glob, Grep
skills: spark-constitution, code-standards, project-patterns
model: sonnet
---
```

```markdown
# implementer-spark

## Core Identity
You are an implementation specialist...

## Protocols
**Phase 0: Context Discovery**
- Read PROJECT_STANDARDS.md (auto-loaded via skill!)
- Read ARCHITECTURE.md
- Identify standard modules

**Phase 1: Implementation**
...

**Phase 2: Testing**
...

**Phase 3: Quality Gates**
...
```

**3. Skills 정의** (`.claude/skills/spark-constitution/SKILL.md`):

```yaml
---
name: spark-constitution
description: SPARK Constitution v1.2 - Agent behavior and quality standards. Use when implementing SPARK agents or following SPARK protocols.
---
```

```markdown
# SPARK Constitution v1.2

## Core Principles
1. Evidence-based reporting
2. Zero-tolerance quality
3. Test-before-report
...

## Supporting Files
- constitution-v1.2.md (full text)
- quality-gates.md (gate definitions)
- protocols.md (workflow protocols)
```

**4. Supporting Files** (`.claude/skills/spark-constitution/constitution-v1.2.md`):

```markdown
# SPARK Constitution v1.2

[Full constitution text...]
```

### 실행 흐름

```
User types:
  /spark-implement user-authentication
       ↓
Slash command expands:
  Task("implementer-spark", "Feature: user-authentication...")
       ↓
Agent starts:
  - Separate context window created
  - Skills auto-loaded:
    * spark-constitution/SKILL.md
    * code-standards/SKILL.md
    * project-patterns/SKILL.md
  - Tools available: Bash, Read, Write, Edit, ...
       ↓
Agent reads:
  - SKILL.md (auto-loaded)
  - constitution-v1.2.md (when needed, contextually)
  - quality-gates.md (when needed, contextually)
       ↓
Agent implements:
  - Follows constitution protocols
  - Uses code standards reference
  - Implements with quality gates
       ↓
Agent returns:
  - Implementation complete
  - Test results: 58/58 passed
  - Quality: 0 violations
       ↓
Claude Code (2호) receives:
  - Single message with complete results
  - Verifies quality gates
  - Reports to Jason
```

### 핵심 장점

**1. Modularity**:
- Command: 워크플로우 정의
- Agent: 전문성 구현
- Skill: 레퍼런스 제공

**2. Reusability**:
- Same agent, different commands
- Same skill, different agents
- Mix and match

**3. Maintainability**:
- Update skill → all agents benefit
- Update agent → all commands benefit
- Update command → workflow changes only

**4. Token Efficiency**:
- Skills loaded only when agent starts
- Supporting files loaded contextually
- No duplication in agent definitions

**5. Context Isolation**:
- Agent's work doesn't pollute main conversation
- Clean separation of concerns
- Easier debugging

---

## 🎯 SPARK Plugin Packaging Strategy

### 현재 SPARK 구조 분석

```
spark-claude/
├── spark-plugin/
│   ├── .claude-plugin/
│   │   └── plugin.json          ✅ 이미 있음
│   ├── agents/                  ✅ 21 agents
│   │   ├── analyzer-spark.md
│   │   ├── implementer-spark.md
│   │   ├── tester-spark.md
│   │   ├── documenter-spark.md
│   │   ├── designer-spark.md
│   │   ├── qc-spark.md
│   │   └── team[1-5]-{implementer,tester,documenter}-spark.md
│   ├── commands/                ✅ 12 commands
│   │   ├── spark-implement.md
│   │   ├── spark-test.md
│   │   ├── spark-analyze.md
│   │   ├── spark-design.md
│   │   ├── spark-fix.md
│   │   ├── spark-improve.md
│   │   ├── spark-refactor.md
│   │   ├── spark-audit.md
│   │   ├── spark-migrate.md
│   │   ├── spark-optimize.md
│   │   ├── spark-launch.md
│   │   └── multi-implement.md
│   ├── skills/                  ⚠️ 현재 비어있음
│   └── hooks/                   ⚠️ 아직 없음
└── .claude/
    └── hooks/                   ⚠️ 현재 여기 있음
        ├── spark_persona_router.py
        └── spark_quality_gates.py
```

### 권장 개선 사항

#### 1. Skills 추가 🎯

**spark-plugin/skills/spark-constitution/**:

```
spark-constitution/
├── SKILL.md                     # Skill definition
├── constitution-v1.2.md         # Full constitution
├── quality-gates.md             # Gate definitions
├── protocols.md                 # Work protocols
└── examples/
    ├── analyzer-example.md
    ├── implementer-example.md
    └── tester-example.md
```

**SKILL.md**:

```yaml
---
name: spark-constitution
description: SPARK Constitution v1.2 - Agent behavior standards, quality gates, and work protocols. Use when implementing features following SPARK methodology, executing quality gates, or understanding SPARK agent workflows.
---
```

```markdown
# SPARK Constitution v1.2

## Overview
SPARK Constitution defines the behavior standards, quality requirements, and work protocols for all SPARK agents.

## When to Use
- Implementing features using SPARK agents
- Following SPARK quality gates
- Understanding SPARK protocols
- Creating new SPARK agents

## Supporting Documents
- `constitution-v1.2.md`: Full constitution text
- `quality-gates.md`: 8-step quality gate definitions
- `protocols.md`: Work protocols (EVIDENCE-BEFORE-REPORT, TEST-BEFORE-REPORT, etc.)
- `examples/`: Example implementations

## Quick Reference
[Key principles, quality standards summary...]
```

**Benefits**:
- Agents reference constitution via skill (no duplication)
- Constitution updates propagate to all agents automatically
- Token efficient (constitution loaded contextually)

#### 2. Agent Skills 필드 추가

**현재** (agents/implementer-spark.md):

```yaml
---
name: implementer-spark
description: Feature implementation specialist...
tools: Bash, Glob, Grep, LS, Read, Edit, MultiEdit, Write, WebFetch, TodoWrite, WebSearch
model: sonnet
color: pink
---
```

**개선** (skills 필드 추가):

```yaml
---
name: implementer-spark
description: Feature implementation specialist...
tools: Bash, Glob, Grep, LS, Read, Edit, MultiEdit, Write, WebFetch, TodoWrite, WebSearch
skills: spark-constitution, code-standards  # ← 추가!
model: sonnet
color: pink
---
```

**All 21 agents**에 적용:
- Core 4: analyzer, implementer, tester, documenter
- Support 2: designer, qc
- Team 15: team1-5 × 3 roles

#### 3. Hooks 이동

**현재**: `.claude/hooks/` (프로젝트 root)

**권장**: `spark-plugin/hooks/` (플러그인 내부)

```bash
mv .claude/hooks/* spark-plugin/hooks/
```

**이유**:
- Plugin과 함께 배포
- 버전 관리 통일
- Plugin 설치 시 자동으로 hooks 설치

#### 4. Additional Skills 고려

**spark-plugin/skills/code-standards/**:

```
code-standards/
├── SKILL.md
├── python-standards.md          # Python best practices
├── testing-standards.md         # Testing requirements
├── documentation-standards.md   # Doc standards
└── security-standards.md        # Security checklist
```

**spark-plugin/skills/project-patterns/**:

```
project-patterns/
├── SKILL.md
├── architecture-patterns.md     # Common patterns
├── api-patterns.md              # API design patterns
├── testing-patterns.md          # Testing patterns
└── templates/
    ├── api-endpoint.py
    ├── service-class.py
    └── test-template.py
```

### 최종 Plugin 구조

```
spark-plugin/
├── .claude-plugin/
│   └── plugin.json
├── agents/ (21 files)
│   ├── analyzer-spark.md        (+ skills: spark-constitution)
│   ├── implementer-spark.md     (+ skills: spark-constitution, code-standards)
│   ├── tester-spark.md          (+ skills: spark-constitution, testing-standards)
│   ├── documenter-spark.md      (+ skills: spark-constitution, documentation-standards)
│   ├── designer-spark.md        (+ skills: spark-constitution, architecture-patterns)
│   ├── qc-spark.md              (+ skills: spark-constitution, code-standards)
│   └── team[1-5]-*.md           (+ skills: spark-constitution)
├── commands/ (12 files)
│   ├── spark-implement.md
│   ├── spark-test.md
│   └── ...
├── skills/
│   ├── spark-constitution/
│   │   ├── SKILL.md
│   │   ├── constitution-v1.2.md
│   │   ├── quality-gates.md
│   │   ├── protocols.md
│   │   └── examples/
│   ├── code-standards/
│   │   ├── SKILL.md
│   │   ├── python-standards.md
│   │   ├── testing-standards.md
│   │   ├── documentation-standards.md
│   │   └── security-standards.md
│   ├── testing-standards/
│   │   ├── SKILL.md
│   │   └── testing-requirements.md
│   ├── documentation-standards/
│   │   ├── SKILL.md
│   │   └── doc-requirements.md
│   └── architecture-patterns/
│       ├── SKILL.md
│       ├── patterns.md
│       └── templates/
└── hooks/
    ├── spark_persona_router.py
    └── spark_quality_gates.py
```

### 배포 전략

**Phase 1: Internal Testing** (현재)
- 프로젝트 내부에서 테스트
- Skills 추가 및 검증
- Agent skills 필드 업데이트

**Phase 2: Plugin Packaging**
- `spark-plugin/` 완성
- README.md, LICENSE 추가
- Version 태그 (v4.3.0)

**Phase 3: Marketplace Distribution**
- Marketplace manifest 생성
- Documentation 작성
- Plugin 퍼블리시

**Phase 4: Community**
- GitHub repository 공개
- Community feedback
- Iteration and improvement

---

## 📊 Token Efficiency Analysis

### Without Skills (현재 방식)

**Agent Definition** (~3.9K tokens for implementer-spark):
- Agent identity + traits: ~500 tokens
- Protocols: ~800 tokens
- Constitution excerpts: ~1,200 tokens ← **중복!**
- Quality standards: ~600 tokens ← **중복!**
- Examples: ~800 tokens ← **중복!**

**21 agents × 1,200 tokens (constitution) = ~25K tokens of duplication**

### With Skills (권장 방식)

**Agent Definition** (~2.5K tokens):
- Agent identity + traits: ~500 tokens
- Protocols: ~800 tokens
- Skills reference: ~10 tokens ← **"skills: spark-constitution"**
- Quality standards: ~600 tokens
- Examples: ~600 tokens

**Skill (spark-constitution)** (~1.5K tokens):
- SKILL.md: ~300 tokens
- Constitution: ~1,200 tokens (loaded **once**, contextually)

**Savings**:
- Per agent: 1,200 tokens → 10 tokens = **99% reduction** on constitution
- Total: 25K → 1.5K = **~94% reduction** on shared content
- Agent loading: 3.9K → 2.5K = **36% faster**

**Additional Benefits**:
- Constitution update: 1 file (skill) vs 21 files (agents)
- Consistency: Single source of truth
- Flexibility: Mix and match skills

---

## 🎓 Best Practices

### 1. Skill Design

**✅ DO**:
- Write clear, trigger-rich descriptions
- Include supporting files for complex topics
- Use contextual loading (don't embed everything in SKILL.md)
- Version your skills (skill-name-v1, skill-name-v2)

**❌ DON'T**:
- Write vague descriptions ("Helps with coding")
- Duplicate content across skills
- Include everything in SKILL.md (use supporting files!)
- Change skill behavior without versioning

### 2. Agent Design

**✅ DO**:
- Specify exact tools needed (don't inherit all)
- Use skills for shared knowledge
- Keep agent definition focused on behavior/protocols
- Test with minimal context first

**❌ DON'T**:
- Duplicate constitution/standards in agent
- Give unlimited tool access unless needed
- Mix multiple specializations in one agent
- Assume unlimited token budget

### 3. Command Design

**✅ DO**:
- Provide clear argument hints
- Include context in Task delegation
- Specify expected output format
- Document command purpose

**❌ DON'T**:
- Assume agent knows project context
- Skip quality requirements in delegation
- Use commands for simple one-liners
- Forget to specify tools if restricted

### 4. Integration Pattern

**✅ DO**:
- Command → Agent → Skill (layered approach)
- Agent loads skills automatically
- Skill provides reference, agent applies it
- Keep separation of concerns

**❌ DON'T**:
- Mix command logic into agent
- Duplicate skill content in command
- Bypass agent and call skill directly (not possible anyway)
- Forget to update skills when standards change

---

## 🚀 Implementation Roadmap for SPARK

### Phase 1: Skills Creation (Priority: HIGH)

**Week 1-2**: Core skills
- [ ] Create `spark-constitution` skill
  - [ ] SKILL.md
  - [ ] constitution-v1.2.md
  - [ ] quality-gates.md
  - [ ] protocols.md
  - [ ] examples/
- [ ] Create `code-standards` skill
  - [ ] SKILL.md
  - [ ] python-standards.md
  - [ ] testing-standards.md
  - [ ] security-standards.md

### Phase 2: Agent Updates (Priority: HIGH)

**Week 2-3**: Add skills to agents
- [ ] Update 6 core agents (analyzer, implementer, tester, documenter, designer, qc)
  - [ ] Add `skills:` field to YAML frontmatter
  - [ ] Remove duplicated constitution content from body
  - [ ] Test each agent with skills
- [ ] Update 15 team agents
  - [ ] Same process as core agents
  - [ ] Verify parallel execution still works

### Phase 3: Testing & Validation (Priority: HIGH)

**Week 3-4**: Comprehensive testing
- [ ] Test each agent independently
- [ ] Test command → agent → skill workflow
- [ ] Verify skills load automatically
- [ ] Verify supporting files load contextually
- [ ] Measure token reduction
- [ ] Verify quality gates still work

### Phase 4: Documentation (Priority: MEDIUM)

**Week 4-5**: Documentation
- [ ] Plugin README.md
- [ ] Skills documentation
- [ ] Migration guide (for existing SPARK users)
- [ ] Examples and tutorials

### Phase 5: Distribution (Priority: LOW)

**Week 5-6**: Marketplace preparation
- [ ] Marketplace manifest
- [ ] Plugin versioning strategy
- [ ] GitHub repository setup
- [ ] Community guidelines

---

## 📚 References

### Official Documentation

**Claude Code Docs**:
- [Agent Skills](https://code.claude.com/docs/en/skills) - Skills system overview
- [Slash Commands](https://code.claude.com/docs/en/slash-commands) - Command system
- [Subagents](https://code.claude.com/docs/en/sub-agents) - Agent architecture
- [Plugins](https://code.claude.com/docs/en/plugins) - Plugin system

### Community Resources

- [Task/Agent Tools | ClaudeLog](https://claudelog.com/mechanics/task-agent-tools/)
- [Claude Code Subagent Deep Dive](https://cuong.io/blog/2025/06/24-claude-code-subagent-deep-dive)
- [Awesome Claude Code Subagents](https://github.com/VoltAgent/awesome-claude-code-subagents)

### SPARK Documentation

- [SPARK Architecture](../CLAUDE.md)
- [SPARK Constitution v1.2](../.claude/SPARK_CONSTITUTION.md)
- [Team Agents](./TEAM_AGENTS.md) (if exists)

---

## 🎯 Conclusion

### 핵심 발견 요약

1. **✅ Agents CAN access skills** via `skills:` field in YAML frontmatter
2. **✅ Skills load automatically** when agent starts (into separate context)
3. **✅ Supporting files load contextually** (token efficient)
4. **✅ Complete workflow**: Slash command → Agent → Skill reference

### SPARK에 대한 권장사항

**Immediate Actions** (이번 주):
1. `spark-constitution` skill 생성
2. `implementer-spark`에 skills 필드 추가 및 테스트
3. 작동 확인 후 다른 agents에 적용

**Short-term** (이번 달):
4. 모든 21 agents에 skills 적용
5. Additional skills 생성 (code-standards, testing-standards 등)
6. Token reduction 측정 및 검증

**Long-term** (다음 달):
7. Plugin 완성 및 문서화
8. Marketplace 배포 준비
9. Community 오픈

### 최종 답변

Jason의 질문: **"plugin을 이용하면 에이전트를 호출해서 skills에 있는 레퍼런스를 참조하면서 작업하게 지시할 수 있는지"**

**답**: ✅ **완전히 가능합니다!**

```yaml
---
name: implementer-spark
skills: spark-constitution, code-standards  # ← 이것만 추가하면 됨!
---
```

이렇게 하면:
1. Agent 시작 시 skills 자동 로드
2. Constitution, standards를 항상 참조
3. 중복 제거로 36% 토큰 절약
4. 업데이트 1곳만 하면 모든 agents에 반영

SPARK의 미래가 더 밝아 보여요! 🚀

---

**Document Version**: 1.0
**Last Updated**: 2025-12-03
**Author**: 2호 (Number Two)
**Status**: Complete ✅

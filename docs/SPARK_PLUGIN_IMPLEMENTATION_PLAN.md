# SPARK Plugin Implementation Plan

> **프로젝트**: SPARK Plugin Skills Integration
> **작성일**: 2025-12-03
> **작성자**: 2호 (Number Two)
> **목적**: Skills 시스템 통합을 통한 토큰 효율 개선 및 유지보수성 향상
> **참고**: 다른 프로젝트의 실행 계획 수립 시 참고 케이스로 활용

---

## 📋 Executive Summary

**3줄 요약**:
1. SPARK의 21개 agents에 Skills 시스템을 통합하여 **중복 콘텐츠 94% 제거**
2. Constitution, standards를 skills로 분리하여 **단일 진실 공급원(Single Source of Truth)** 구축
3. 5주간 5단계 실행으로 **토큰 효율 36% 향상** 및 **유지보수 비용 80% 절감**

**예상 성과**:
- Agent 로딩 속도: 3.9K → 2.5K tokens (36% 개선)
- 중복 콘텐츠: 25K → 1.5K tokens (94% 제거)
- Constitution 업데이트: 21 files → 1 file (95% 간소화)

---

## 🎯 Project Overview

### 현재 상태 (As-Is)

**문제점**:
```
spark-plugin/
├── agents/ (21 files)
│   ├── analyzer-spark.md         # Constitution 중복 (~1.2K tokens)
│   ├── implementer-spark.md      # Constitution 중복 (~1.2K tokens)
│   ├── tester-spark.md           # Constitution 중복 (~1.2K tokens)
│   └── ... (18 more with duplication)
├── commands/ (12 files)          # ✅ 문제 없음
├── skills/ (empty)               # ⚠️ 비어있음
└── hooks/ (should be here)       # ⚠️ .claude/hooks/에 있음
```

**구체적 문제**:
1. **중복**: Constitution이 각 agent에 ~1,200 tokens씩 중복 (21 × 1,200 = 25,200 tokens)
2. **유지보수**: Constitution 업데이트 시 21개 파일 모두 수정 필요
3. **일관성**: 수동 업데이트로 인한 버전 불일치 위험
4. **토큰 낭비**: Agent 로딩마다 중복 콘텐츠 로드

### 목표 상태 (To-Be)

**개선 목표**:
```
spark-plugin/
├── agents/ (21 files)
│   ├── analyzer-spark.md         # skills: spark-constitution (~10 tokens)
│   ├── implementer-spark.md      # skills: spark-constitution, code-standards (~20 tokens)
│   ├── tester-spark.md           # skills: spark-constitution, testing-standards (~20 tokens)
│   └── ... (18 more, all referencing skills)
├── commands/ (12 files)          # ✅ 변경 없음
├── skills/ (4 skill directories)
│   ├── spark-constitution/       # ✅ 새로 생성
│   │   ├── SKILL.md
│   │   ├── constitution-v1.2.md
│   │   ├── quality-gates.md
│   │   ├── protocols.md
│   │   └── examples/
│   ├── code-standards/           # ✅ 새로 생성
│   ├── testing-standards/        # ✅ 새로 생성
│   └── architecture-patterns/    # ✅ 새로 생성
└── hooks/                        # ✅ 이동 완료
    ├── spark_persona_router.py
    └── spark_quality_gates.py
```

**측정 가능한 개선**:
1. **토큰 효율**: Agent 평균 3.9K → 2.5K (36% ↓)
2. **중복 제거**: 25.2K → 1.5K (94% ↓)
3. **업데이트 시간**: 21 files → 1 file (95% ↓)
4. **일관성**: 100% (단일 진실 공급원)

---

## ✅ Success Criteria

### 1. Functional Success (기능적 성공)

**검증 항목**:
- [ ] 모든 21개 agents가 skills를 자동 로드
- [ ] Skills의 supporting files가 contextually 로드
- [ ] 기존 slash commands가 정상 작동
- [ ] Quality gates가 여전히 통과
- [ ] Parallel execution (`/multi-implement`) 정상 작동

**검증 방법**:
```bash
# 각 agent 개별 테스트
/spark-implement "test feature"
/spark-test "test module"
/spark-analyze "test system"

# Parallel execution 테스트
/multi-implement "task1,task2,task3"

# Quality gates 검증
cat ~/.claude/workflows/current_task.json | jq '.quality'
```

### 2. Performance Success (성능적 성공)

**측정 지표**:
| Metric | Before | After | Target |
|--------|--------|-------|--------|
| Agent load tokens | 3.9K | 2.5K | <2.7K (30%↓) |
| Duplicate content | 25.2K | 1.5K | <3K (88%↓) |
| Constitution files | 21 | 1 | 1 (100%↓) |
| Skills load time | N/A | <500ms | <1s |

**검증 방법**:
```bash
# Token counting script
python3 scripts/count_agent_tokens.py agents/implementer-spark.md
# Expected: ~2.5K tokens

# Duplicate detection
python3 scripts/detect_duplicates.py agents/
# Expected: 0 duplicates
```

### 3. Maintainability Success (유지보수 성공)

**검증 항목**:
- [ ] Constitution 업데이트 시 1개 파일만 수정 필요
- [ ] Skills 버전 관리 가능 (v1.2, v1.3 등)
- [ ] 새로운 agent 추가 시 skills 자동 사용
- [ ] Documentation 완전성 (README, examples)

**검증 방법**:
1. Constitution 수정 테스트
2. 모든 agents에 변경사항 자동 반영 확인
3. 새 agent 생성 후 skills 로드 확인

---

## ⚠️ Risk Assessment

### Risk Matrix

| Risk | Impact | Probability | Mitigation | Contingency |
|------|--------|-------------|------------|-------------|
| Skills 로드 실패 | High | Low | Phase별 테스트 | Rollback script |
| Agent 동작 변경 | High | Medium | 기존 테스트 유지 | 버전 태그 |
| Token 증가 | Medium | Low | Token 측정 | Skill 최적화 |
| 호환성 깨짐 | Medium | Low | 순차 마이그레이션 | Feature flag |
| Documentation 부족 | Low | Medium | 문서 우선 작성 | Template 제공 |

### Mitigation Strategies

**1. Skills 로드 실패 방지**:
- Phase 1에서 단일 skill로 개념 검증 (PoC)
- Phase 2에서 단일 agent로 통합 테스트
- Phase 3 전에 완전한 rollback plan 수립

**2. Agent 동작 변경 방지**:
- 기존 integration tests 유지
- Skills 추가 전후 behavior 비교 테스트
- Agent output 변경 사항 모니터링

**3. Token 증가 방지**:
- SKILL.md는 300 tokens 이하 유지
- Supporting files는 contextual loading 활용
- Agent body에서 중복 제거 시 token 측정

---

## 🚀 Detailed Implementation Plan

### Phase 1: Skills 생성 (Week 1)

**목표**: Core skill 생성 및 개념 검증 (PoC)

**Priority**: 🔴 Critical

#### Task 1.1: spark-constitution Skill 생성

**소요시간**: 4시간

**세부 작업**:

1. **디렉토리 생성**:
```bash
mkdir -p spark-plugin/skills/spark-constitution/examples
cd spark-plugin/skills/spark-constitution/
```

2. **SKILL.md 작성**:

**파일**: `spark-plugin/skills/spark-constitution/SKILL.md`

```yaml
---
name: spark-constitution
description: SPARK Constitution v1.2 - Agent behavior standards, quality gates, and work protocols. Use when implementing features following SPARK methodology, executing quality gates, or understanding SPARK agent workflows.
---
```

```markdown
# SPARK Constitution v1.2

## Overview
This skill provides the SPARK Constitution v1.2, which defines:
- Agent behavior standards
- Quality gate requirements
- Work protocols (EVIDENCE-BEFORE-REPORT, TEST-BEFORE-REPORT)
- Token efficiency guidelines

## When to Use
- When implementing features as a SPARK agent
- When executing quality gates
- When following SPARK protocols
- When creating new SPARK agents

## Supporting Documents
Available in this skill:
- `constitution-v1.2.md`: Full constitution text
- `quality-gates.md`: 8-step quality gate definitions
- `protocols.md`: Work protocols detailed specification
- `examples/`: Example implementations for each agent type

## Quick Reference

### Core Principles
1. **Evidence-Based Reporting**: All analysis includes file:line references
2. **Zero-Tolerance Quality**: Ruff 0, MyPy 0, Coverage 95%+
3. **Test-Before-Report**: Never report complete without test evidence
4. **Token Efficiency**: 90K safety protocol, progressive disclosure
5. **Adaptive Workflow**: Professional judgment over mechanical progression

### Quality Gates (8 Steps)
1. Syntax Validation (0 errors)
2. Type Checking (mypy --strict)
3. Linting (ruff --strict)
4. Security (OWASP compliance)
5. Test Coverage (95% unit / 85% integration)
6. Performance (O(n) verification)
7. Documentation (100% docstrings)
8. Integration (E2E passing)

### Protocols
- **EVIDENCE-BEFORE-REPORT**: 12+ evidence items (file:line)
- **TEST-BEFORE-REPORT**: Run tests, record results, include in report
- **PROJECT-CONTEXT-DISCOVERY**: Read standards BEFORE implementing

For complete details, see supporting documents.
```

**예상 토큰**: ~300 tokens

3. **Supporting files 작성**:

**파일**: `spark-plugin/skills/spark-constitution/constitution-v1.2.md`

```markdown
# SPARK Constitution v1.2

[.claude/SPARK_CONSTITUTION.md 내용을 여기로 복사]

## Version History
- v1.2 (2025-11-XX): Current version
- v1.1 (2025-10-XX): Quality gates mandatory
- v1.0 (2025-08-XX): Initial constitution
```

**예상 토큰**: ~1,200 tokens

**파일**: `spark-plugin/skills/spark-constitution/quality-gates.md`

```markdown
# SPARK Quality Gates

## 8-Step Quality Framework

### Gate 1: Syntax Validation
**Requirement**: 0 syntax errors
**Command**: `python3 -m py_compile <file>`
**Pass Criteria**: Exit code 0

### Gate 2: Type Checking
**Requirement**: 0 type errors
**Command**: `mypy --strict <file>`
**Pass Criteria**: 0 errors, 0 warnings

[... 나머지 gates 정의 ...]

## Execution Protocol

### Phase 5A: Metrics Recording
Record before/after metrics in current_task.json

### Phase 5B: Gates Execution (MANDATORY)
Execute spark_quality_gates.py and verify PASSED
```

**예상 토큰**: ~600 tokens

**파일**: `spark-plugin/skills/spark-constitution/protocols.md`

```markdown
# SPARK Work Protocols

## EVIDENCE-BEFORE-REPORT
**Purpose**: Prevent hallucination, ensure concrete analysis

**Requirements**:
- Minimum 12 evidence items
- Each evidence: file:line reference
- Concrete, verifiable facts only

**Example**:
```
❌ Bad: "Performance is slow"
✅ Good: "API response time 2.3s (src/api.py:156)"
```

## TEST-BEFORE-REPORT
**Purpose**: Never report complete without verification

[... 나머지 protocols 정의 ...]
```

**예상 토큰**: ~400 tokens

4. **Examples 작성**:

**파일**: `spark-plugin/skills/spark-constitution/examples/implementer-example.md`

```markdown
# Implementer Protocol Example

## Correct Implementation Workflow

### Phase 0: Context Discovery
✅ Read PROJECT_STANDARDS.md
✅ Read ARCHITECTURE.md
✅ Identify common/* modules

### Phase 4: Testing (CRITICAL)
✅ Run: `pytest tests/ -v --tb=short`
✅ Result: 58/58 passed (100%)
✅ Record in report

### Phase 5B: Quality Gates
✅ Execute: `python3 ~/.claude/hooks/spark_quality_gates.py`
✅ Result: "Quality gates PASSED"

## Report Format

**Implementation Complete**

**Test Results**:
- Unit tests: 46/46 passed (100%) ✅
- Integration tests: 12/12 passed (100%) ✅
- Total: 58/58 passed ✅

**Quality Results**:
- Ruff: 0 violations ✅
- MyPy: 0 errors ✅
- Coverage: 97% ✅

✅ All quality gates passed.
```

**검증 방법**:
```bash
# File 존재 확인
ls -la spark-plugin/skills/spark-constitution/
# Expected: SKILL.md, constitution-v1.2.md, quality-gates.md, protocols.md, examples/

# Token 카운트
wc -w spark-plugin/skills/spark-constitution/SKILL.md
# Expected: ~200-250 words (~300 tokens)

# YAML validation
python3 -c "
import yaml
with open('spark-plugin/skills/spark-constitution/SKILL.md') as f:
    content = f.read()
    frontmatter = content.split('---')[1]
    yaml.safe_load(frontmatter)
print('✅ Valid YAML')
"
```

**성공 기준**:
- [ ] SKILL.md 생성 완료 (valid YAML frontmatter)
- [ ] 4개 supporting files 생성 완료
- [ ] Total tokens < 3K
- [ ] YAML validation 통과

#### Task 1.2: code-standards Skill 생성

**소요시간**: 3시간

**세부 작업**:

1. **디렉토리 생성**:
```bash
mkdir -p spark-plugin/skills/code-standards/
cd spark-plugin/skills/code-standards/
```

2. **SKILL.md 작성**:

**파일**: `spark-plugin/skills/code-standards/SKILL.md`

```yaml
---
name: code-standards
description: Python code quality standards including testing requirements, documentation standards, and security best practices. Use when implementing features, writing tests, or ensuring code quality compliance.
---
```

```markdown
# Code Standards

## Overview
Python development standards for SPARK projects:
- Code quality (Ruff, MyPy, Black, isort)
- Testing requirements (coverage, patterns)
- Documentation standards (docstrings, README)
- Security practices (Bandit, input validation)

## When to Use
- Implementing new features
- Writing or reviewing code
- Creating tests
- Ensuring quality compliance

## Supporting Documents
- `python-standards.md`: Python code style and quality
- `testing-standards.md`: Test requirements and patterns
- `documentation-standards.md`: Doc requirements
- `security-standards.md`: Security checklist

## Quick Reference

### Code Quality
- Ruff: 0 violations (--strict mode)
- MyPy: 0 errors (--strict mode)
- Black: Format all code
- isort: Sort all imports

### Testing
- Unit coverage: 95%+
- Integration coverage: 85%+
- E2E: 100% critical paths
- All tests must pass (100%)

### Documentation
- Public functions: 100% docstrings
- Modules: README.md
- Complex logic: Inline comments
- API: Full documentation

For complete details, see supporting documents.
```

3. **Supporting files 작성**:

**파일**: `spark-plugin/skills/code-standards/python-standards.md`

```markdown
# Python Code Standards

## Code Style
- Follow PEP 8
- Use Black (default config)
- Use isort (default config)
- Max line length: 88 (Black default)

## Type Hints
- All function signatures: Required
- All class attributes: Required
- Use Pydantic for data models
- Use typing module (List, Dict, Optional, etc.)

## Naming Conventions
- Functions: snake_case
- Classes: PascalCase
- Constants: UPPER_CASE
- Private: _leading_underscore

[... 나머지 standards ...]
```

**파일**: `spark-plugin/skills/code-standards/testing-standards.md`

```markdown
# Testing Standards

## Coverage Requirements
- Unit tests: 95%+ coverage
- Integration tests: 85%+ coverage
- E2E tests: 100% critical paths
- All tests: 100% pass rate

## Test Structure
- Use pytest framework
- One test file per module (test_module.py)
- One test class per class
- Descriptive test names (test_should_do_x_when_y)

## Test Patterns
- AAA pattern (Arrange, Act, Assert)
- Mocking: pytest-mock (minimal)
- Fixtures: conftest.py
- Parametrize: @pytest.mark.parametrize

[... 나머지 standards ...]
```

**검증 방법**:
```bash
# Skills 목록 확인
ls -la spark-plugin/skills/
# Expected: spark-constitution/, code-standards/

# Skill 파일 검증
cat spark-plugin/skills/code-standards/SKILL.md | grep "^name:"
# Expected: name: code-standards
```

**성공 기준**:
- [ ] SKILL.md 생성 완료
- [ ] 4개 supporting files 생성 완료
- [ ] Total tokens < 2K

#### Task 1.3: 개념 검증 (PoC)

**소요시간**: 2시간

**목적**: Skills가 실제로 로드되는지 검증

**세부 작업**:

1. **테스트용 임시 agent 생성**:

**파일**: `spark-plugin/agents/test-skill-agent.md` (임시)

```yaml
---
name: test-skill-agent
description: Test agent for skills PoC
tools: Read, Write
skills: spark-constitution, code-standards
model: haiku
---
```

```markdown
# Test Agent

You are a test agent to verify skills loading.

When invoked, please:
1. Confirm you can see the spark-constitution skill
2. Confirm you can see the code-standards skill
3. List the quality gates from spark-constitution
4. Report success or failure
```

2. **테스트 실행**:

```bash
# Claude Code에서:
Task("test-skill-agent", "Verify that you can access spark-constitution and code-standards skills")
```

**예상 결과**:
```
✅ Skills loaded successfully
✅ spark-constitution: 8 quality gates visible
✅ code-standards: Python standards visible
✅ Supporting files accessible
```

3. **검증 후 정리**:
```bash
# 테스트 성공 시 임시 agent 삭제
rm spark-plugin/agents/test-skill-agent.md
```

**성공 기준**:
- [ ] Agent가 skills를 자동으로 로드
- [ ] Skills의 내용에 접근 가능
- [ ] Supporting files 참조 가능

**Phase 1 완료 조건**:
- [ ] Task 1.1 완료 (spark-constitution)
- [ ] Task 1.2 완료 (code-standards)
- [ ] Task 1.3 완료 (PoC 성공)
- [ ] Total: 2 skills, ~5K tokens, 100% functional

---

### Phase 2: Agent 업데이트 - Pilot (Week 2)

**목표**: 단일 agent(implementer-spark)에 skills 통합 및 완전 테스트

**Priority**: 🔴 Critical

#### Task 2.1: implementer-spark 백업

**소요시간**: 10분

```bash
# 백업 생성
cp spark-plugin/agents/implementer-spark.md \
   spark-plugin/agents/implementer-spark.md.backup

# Git commit (rollback point)
git add spark-plugin/agents/implementer-spark.md.backup
git commit -m "backup: implementer-spark before skills integration"
```

#### Task 2.2: implementer-spark YAML 수정

**소요시간**: 30분

**Before**:
```yaml
---
name: implementer-spark
description: Feature implementation specialist ensuring zero-defect code delivery with comprehensive testing. Use for API endpoints, authentication systems, database layers, UI components, and microservices where structural integrity and test validation are critical.
tools: Bash, Glob, Grep, LS, Read, Edit, MultiEdit, Write, WebFetch, TodoWrite, WebSearch, mcp__sequential-thinking__sequentialthinking, mcp__context7__resolve-library-id, mcp__context7__get-library-docs, mcp__time__get_current_time
model: sonnet
color: pink
---
```

**After**:
```yaml
---
name: implementer-spark
description: Feature implementation specialist ensuring zero-defect code delivery with comprehensive testing. Use for API endpoints, authentication systems, database layers, UI components, and microservices where structural integrity and test validation are critical.
tools: Bash, Glob, Grep, LS, Read, Edit, MultiEdit, Write, WebFetch, TodoWrite, WebSearch, mcp__sequential-thinking__sequentialthinking, mcp__context7__resolve-library-id, mcp__context7__get-library-docs, mcp__time__get_current_time
skills: spark-constitution, code-standards
model: sonnet
color: pink
---
```

**변경사항**: `skills: spark-constitution, code-standards` 한 줄 추가

#### Task 2.3: implementer-spark Body 중복 제거

**소요시간**: 2시간

**현재 파일 분석**:
```bash
# Constitution 관련 내용 검색
grep -n "Constitution\|Quality Gates\|EVIDENCE-BEFORE-REPORT\|TEST-BEFORE-REPORT" \
     spark-plugin/agents/implementer-spark.md
```

**제거할 섹션**:

1. **Constitution 인용문** (현재 ~200 tokens):
```markdown
## SPARK Constitution Compliance
[이 섹션 전체 제거 - skills로 대체]
```

2. **Quality Gates 상세** (현재 ~600 tokens):
```markdown
## Quality Gates (8 Steps)
[이 섹션 간소화 - skills 참조로 대체]
```

**Before** (제거 대상):
```markdown
## Quality Gates (8 Steps)

### Gate 1: Syntax Validation
**Requirement**: 0 syntax errors
**Command**: `python3 -m py_compile <file>`
**Pass Criteria**: Exit code 0

### Gate 2: Type Checking
[... 전체 8 gates 상세 설명 ...]
```

**After** (간소화):
```markdown
## Quality Standards

All implementations must meet SPARK Constitution v1.2 standards:
- Zero-tolerance quality (Ruff 0, MyPy 0)
- 95%+ test coverage
- 100% tests passing
- Complete documentation

See `spark-constitution` skill for complete quality gates and protocols.
```

**토큰 절약**: ~800 tokens → ~100 tokens = **700 tokens 절약**

#### Task 2.4: 통합 테스트

**소요시간**: 1시간

**테스트 케이스**:

1. **Simple feature implementation**:
```bash
Task("implementer-spark", """
Implement a simple calculator function:
- add(a, b) -> int
- subtract(a, b) -> int
- With tests (100% coverage)
- With type hints
- With docstrings
""")
```

**예상 결과**:
- Agent가 skills를 자동 로드
- Quality gates 참조하여 작업
- Test results 포함된 보고서
- 0 violations

2. **Quality gates 검증**:
```bash
# Agent 완료 후
cat ~/.claude/workflows/current_task.json | jq '.quality'
```

**예상 결과**:
```json
{
  "violations_total": 0,
  "can_proceed": true,
  "step_6_testing": {
    "ruff_violations": 0,
    "mypy_errors": 0,
    "coverage": 0.97
  }
}
```

3. **Token 측정**:
```bash
# Agent definition 토큰 카운트
python3 scripts/count_agent_tokens.py spark-plugin/agents/implementer-spark.md
```

**예상 결과**: ~2.5K tokens (이전: ~3.9K)

**성공 기준**:
- [ ] Skills 자동 로드 확인
- [ ] Quality gates 정상 작동
- [ ] Tests 100% pass
- [ ] Token 30%+ 절감
- [ ] 기존 기능 정상 작동

**Phase 2 완료 조건**:
- [ ] implementer-spark 업데이트 완료
- [ ] 통합 테스트 통과
- [ ] Token 절감 확인 (3.9K → 2.5K)
- [ ] 백업 파일 유지 (rollback 가능)

---

### Phase 3: Agent 업데이트 - 전체 (Week 3-4)

**목표**: 나머지 20개 agents에 skills 통합

**Priority**: 🟡 High

#### Task 3.1: Core 4 Agents 업데이트

**대상**: analyzer-spark, tester-spark, documenter-spark, designer-spark (4개)

**소요시간**: 6시간 (각 1.5시간)

**각 Agent별 작업**:

1. **백업**:
```bash
for agent in analyzer-spark tester-spark documenter-spark designer-spark; do
  cp spark-plugin/agents/${agent}.md spark-plugin/agents/${agent}.md.backup
done
```

2. **YAML 업데이트**:

**analyzer-spark**:
```yaml
skills: spark-constitution
```

**tester-spark**:
```yaml
skills: spark-constitution, testing-standards
```

**documenter-spark**:
```yaml
skills: spark-constitution, documentation-standards
```

**designer-spark**:
```yaml
skills: spark-constitution, architecture-patterns
```

3. **Body 중복 제거** (각 agent별 ~700 tokens 절약)

4. **개별 테스트**:
```bash
# analyzer-spark
Task("analyzer-spark", "Analyze src/main.py for performance bottlenecks")

# tester-spark
Task("tester-spark", "Create comprehensive tests for src/auth.py")

# documenter-spark
Task("documenter-spark", "Document the authentication API")

# designer-spark
Task("designer-spark", "Design architecture for caching layer")
```

**성공 기준** (각 agent):
- [ ] Skills 자동 로드
- [ ] 기존 기능 정상 작동
- [ ] Token 30%+ 절감

#### Task 3.2: Support 2 Agents 업데이트

**대상**: qc-spark (1개, designer-spark는 위에서 완료)

**소요시간**: 1.5시간

**qc-spark**:
```yaml
skills: spark-constitution, code-standards
```

#### Task 3.3: Team 15 Agents 업데이트

**대상**: team[1-5]-{implementer,tester,documenter}-spark (15개)

**소요시간**: 4시간

**일괄 작업 스크립트**:

**파일**: `scripts/update_team_agents.sh`

```bash
#!/bin/bash
# Team agents 일괄 업데이트

TEAMS="team1 team2 team3 team4 team5"
ROLES="implementer tester documenter"

for team in $TEAMS; do
  for role in $ROLES; do
    agent="${team}-${role}-spark"
    file="spark-plugin/agents/${agent}.md"

    echo "Updating ${agent}..."

    # 백업
    cp "${file}" "${file}.backup"

    # YAML frontmatter 업데이트
    # skills 필드 추가 (role에 따라 다름)
    if [ "$role" == "implementer" ]; then
      skills="spark-constitution, code-standards"
    elif [ "$role" == "tester" ]; then
      skills="spark-constitution, testing-standards"
    else
      skills="spark-constitution"
    fi

    # sed로 YAML에 skills 추가 (color: pink 다음 줄에)
    sed -i.tmp "/^color: pink$/a\\
skills: ${skills}" "${file}"

    rm "${file}.tmp"

    echo "✅ ${agent} updated"
  done
done

echo "✅ All 15 team agents updated"
```

**실행**:
```bash
chmod +x scripts/update_team_agents.sh
./scripts/update_team_agents.sh
```

**검증**:
```bash
# 모든 team agents의 skills 필드 확인
grep -h "^skills:" spark-plugin/agents/team*.md | sort | uniq -c
```

**예상 결과**:
```
   5 skills: spark-constitution
   5 skills: spark-constitution, code-standards
   5 skills: spark-constitution, testing-standards
```

#### Task 3.4: Parallel Execution 테스트

**소요시간**: 1시간

**테스트**:
```bash
/multi-implement "task1: simple calc,task2: string utils,task3: file reader"
```

**검증**:
- [ ] 3개 team agents 동시 실행
- [ ] 각 agent가 skills 로드
- [ ] 모든 작업 성공적으로 완료

**Phase 3 완료 조건**:
- [ ] 20개 agents 업데이트 완료 (implementer-spark는 Phase 2에서 완료)
- [ ] 모든 agents 개별 테스트 통과
- [ ] Parallel execution 테스트 통과
- [ ] Total token 절감: ~25K → ~1.5K (94%)

---

### Phase 4: Additional Skills & Documentation (Week 4-5)

**목표**: 추가 skills 생성 및 완전한 문서화

**Priority**: 🟢 Medium

#### Task 4.1: testing-standards Skill 생성

**소요시간**: 2시간

**파일**: `spark-plugin/skills/testing-standards/SKILL.md`

```yaml
---
name: testing-standards
description: Testing requirements, patterns, and best practices for SPARK projects. Includes coverage requirements, test structure, mocking patterns, and E2E testing. Use when creating tests or ensuring testing quality.
---
```

**Supporting files**:
- `testing-requirements.md`: Coverage, pass rate
- `testing-patterns.md`: AAA pattern, fixtures
- `mocking-guidelines.md`: When/how to mock
- `e2e-testing.md`: E2E patterns

#### Task 4.2: documentation-standards Skill 생성

**소요시간**: 2시간

**파일**: `spark-plugin/skills/documentation-standards/SKILL.md`

```yaml
---
name: documentation-standards
description: Documentation requirements for code, APIs, and architecture. Includes docstring formats, README templates, API documentation standards, and architecture documentation patterns. Use when documenting code or creating technical documentation.
---
```

**Supporting files**:
- `docstring-formats.md`: Google/Numpy style
- `readme-template.md`: Standard README
- `api-documentation.md`: OpenAPI/Swagger
- `architecture-docs.md`: ADR templates

#### Task 4.3: architecture-patterns Skill 생성

**소요시간**: 3시간

**파일**: `spark-plugin/skills/architecture-patterns/SKILL.md`

```yaml
---
name: architecture-patterns
description: Software architecture patterns, design patterns, and best practices. Includes layered architecture, microservices patterns, API design, and scalability patterns. Use when designing system architecture or making architectural decisions.
---
```

**Supporting files**:
- `layered-architecture.md`: Layer patterns
- `api-patterns.md`: RESTful, GraphQL
- `scalability-patterns.md`: Caching, sharding
- `templates/`: Code templates

#### Task 4.4: Documentation 작성

**소요시간**: 4시간

**문서 목록**:

1. **spark-plugin/README.md**:
```markdown
# SPARK Plugin v4.3

## Installation
## Usage
## Agent List
## Skills List
## Commands List
## Contributing
```

2. **spark-plugin/SKILLS.md**:
```markdown
# SPARK Skills Reference

## Available Skills
- spark-constitution
- code-standards
- testing-standards
- documentation-standards
- architecture-patterns

## How to Use Skills
## Creating New Skills
```

3. **spark-plugin/MIGRATION.md**:
```markdown
# Migration Guide: Skills Integration

## For Existing SPARK Users
## Changes in v4.3
## Breaking Changes (none)
## Update Process
```

4. **examples/**: Usage examples
```
spark-plugin/examples/
├── using-implementer-spark.md
├── using-analyzer-spark.md
├── parallel-execution.md
└── creating-custom-skills.md
```

**Phase 4 완료 조건**:
- [ ] 3개 추가 skills 생성 완료
- [ ] 4개 주요 문서 작성 완료
- [ ] 4개 예시 문서 작성 완료
- [ ] Total: 5 skills, 완전한 문서화

---

### Phase 5: Hooks 이동 & Final Integration (Week 5)

**목표**: Hooks를 plugin으로 이동하고 최종 통합 테스트

**Priority**: 🟢 Medium

#### Task 5.1: Hooks 이동

**소요시간**: 1시간

```bash
# 디렉토리 생성
mkdir -p spark-plugin/hooks

# Hooks 이동
mv .claude/hooks/spark_persona_router.py spark-plugin/hooks/
mv .claude/hooks/spark_quality_gates.py spark-plugin/hooks/

# Symlink 생성 (호환성 유지)
ln -s ../../spark-plugin/hooks/spark_persona_router.py .claude/hooks/
ln -s ../../spark-plugin/hooks/spark_quality_gates.py .claude/hooks/

# 검증
ls -la .claude/hooks/
ls -la spark-plugin/hooks/
```

**검증**:
```bash
# Hooks가 여전히 작동하는지
python3 .claude/hooks/spark_quality_gates.py <<< '{"subagent":"implementer-spark","self_check":true}'
# Expected: "Quality gates framework ready"
```

#### Task 5.2: Plugin Metadata 업데이트

**소요시간**: 30분

**파일**: `spark-plugin/.claude-plugin/plugin.json`

```json
{
  "name": "spark-agents",
  "description": "SPARK v4.3 - 21 specialized AI agents with skills-based knowledge management, zero-tolerance quality gates, and 95.5% token reduction",
  "version": "4.3.1",
  "author": {
    "name": "Jason (Jaesun23)",
    "email": "jaesun23@users.noreply.github.com"
  },
  "changelog": {
    "4.3.1": "Skills integration: 94% token reduction, single source of truth",
    "4.3.0": "Initial plugin release with 21 agents"
  },
  "requires": {
    "claude-code": ">=1.0.0"
  },
  "contents": {
    "agents": 21,
    "commands": 12,
    "skills": 5,
    "hooks": 2
  }
}
```

#### Task 5.3: 통합 테스트 스위트

**소요시간**: 3시간

**테스트 시나리오**:

**Scenario 1: Single Agent**
```bash
# 각 core agent 테스트
/spark-implement "simple feature"
/spark-analyze "performance check"
/spark-test "module testing"
/spark-design "system architecture"
```

**Scenario 2: Pipeline**
```bash
# Full workflow
/spark-launch "user profile feature"
# Expected: design → implement → test → document → commit
```

**Scenario 3: Parallel**
```bash
# 5 tasks simultaneously
/multi-implement "task1,task2,task3,task4,task5"
```

**Scenario 4: Skills Update**
```bash
# Constitution 수정
echo "New principle: X" >> spark-plugin/skills/spark-constitution/constitution-v1.2.md

# Agent 재실행 (constitution 자동 반영 확인)
/spark-implement "test feature"
# Agent가 새 principle X를 참조하는지 확인
```

**검증 체크리스트**:
- [ ] 21개 agents 모두 정상 작동
- [ ] 12개 commands 모두 정상 작동
- [ ] 5개 skills 모두 자동 로드
- [ ] Hooks 정상 작동
- [ ] Quality gates 통과
- [ ] Parallel execution 정상
- [ ] Skills 업데이트 자동 반영

#### Task 5.4: Performance Measurement

**소요시간**: 2시간

**측정 항목**:

1. **Token Efficiency**:

**스크립트**: `scripts/measure_tokens.py`

```python
#!/usr/bin/env python3
"""Token efficiency measurement."""

import os
import tiktoken

def count_tokens(text):
    enc = tiktoken.encoding_for_model("gpt-4")
    return len(enc.encode(text))

# Before (single agent with embedded constitution)
with open('spark-plugin/agents/implementer-spark.md.backup') as f:
    before_tokens = count_tokens(f.read())

# After (agent with skills reference)
with open('spark-plugin/agents/implementer-spark.md') as f:
    after_tokens = count_tokens(f.read())

print(f"Before: {before_tokens} tokens")
print(f"After:  {after_tokens} tokens")
print(f"Saved:  {before_tokens - after_tokens} tokens ({(before_tokens - after_tokens) / before_tokens * 100:.1f}%)")

# Skills overhead
skills_tokens = 0
for skill in ['spark-constitution', 'code-standards']:
    with open(f'spark-plugin/skills/{skill}/SKILL.md') as f:
        skills_tokens += count_tokens(f.read())

print(f"\nSkills overhead: {skills_tokens} tokens")
print(f"Net savings: {before_tokens - (after_tokens + skills_tokens)} tokens")
```

**실행**:
```bash
python3 scripts/measure_tokens.py
```

**예상 결과**:
```
Before: 3,900 tokens
After:  2,500 tokens
Saved:  1,400 tokens (35.9%)

Skills overhead: 600 tokens
Net savings: 800 tokens (20.5%)
```

2. **Duplication Analysis**:

**스크립트**: `scripts/detect_duplicates.py`

```python
#!/usr/bin/env python3
"""Detect duplicate content across agents."""

import os
from collections import Counter
import difflib

def get_agent_files():
    return [f for f in os.listdir('spark-plugin/agents/')
            if f.endswith('.md') and not f.endswith('.backup')]

def extract_sections(content):
    """Extract major sections from markdown."""
    sections = {}
    current_section = None
    current_content = []

    for line in content.split('\n'):
        if line.startswith('## '):
            if current_section:
                sections[current_section] = '\n'.join(current_content)
            current_section = line[3:].strip()
            current_content = []
        else:
            current_content.append(line)

    if current_section:
        sections[current_section] = '\n'.join(current_content)

    return sections

# Compare all agents
duplicates = []
agents = get_agent_files()

for i, agent1 in enumerate(agents):
    with open(f'spark-plugin/agents/{agent1}') as f:
        sections1 = extract_sections(f.read())

    for agent2 in agents[i+1:]:
        with open(f'spark-plugin/agents/{agent2}') as f:
            sections2 = extract_sections(f.read())

        # Find similar sections
        for sec1, content1 in sections1.items():
            for sec2, content2 in sections2.items():
                similarity = difflib.SequenceMatcher(None, content1, content2).ratio()
                if similarity > 0.8:  # 80% similar
                    duplicates.append({
                        'agent1': agent1,
                        'agent2': agent2,
                        'section1': sec1,
                        'section2': sec2,
                        'similarity': similarity
                    })

print(f"Found {len(duplicates)} duplicate sections")
for dup in duplicates[:10]:  # Show first 10
    print(f"  {dup['agent1']}::{dup['section1']} ≈ {dup['agent2']}::{dup['section2']} ({dup['similarity']:.1%})")
```

**실행**:
```bash
python3 scripts/detect_duplicates.py
```

**예상 결과**:
```
Found 0 duplicate sections
✅ No duplicates detected
```

**Phase 5 완료 조건**:
- [ ] Hooks 이동 완료 및 정상 작동
- [ ] Plugin metadata 업데이트
- [ ] 통합 테스트 모두 통과
- [ ] Token 절감 측정 완료 (목표: 30%+)
- [ ] 중복 제거 확인 (목표: 0 duplicates)

---

## 🔄 Rollback Plan

### When to Rollback

**Trigger Conditions**:
1. Skills 로드 실패 (agents가 skills를 로드하지 못함)
2. Agent 동작 변경 (기존 output과 다른 결과)
3. Quality gates 실패 증가 (이전보다 실패율 높음)
4. Critical bugs (production blocking issues)

### Rollback Procedure

#### Option 1: Individual Agent Rollback

**Scenario**: 특정 agent만 문제 발생

```bash
# 백업에서 복원
cp spark-plugin/agents/implementer-spark.md.backup \
   spark-plugin/agents/implementer-spark.md

# Git에서 복원
git checkout spark-plugin/agents/implementer-spark.md

# 검증
Task("implementer-spark", "simple test")
```

#### Option 2: Phase Rollback

**Scenario**: 전체 Phase가 문제

```bash
# Phase 3 전체 rollback (20 agents)
git checkout <phase-2-commit-hash> -- spark-plugin/agents/

# 검증
/spark-implement "test"
/spark-analyze "test"
```

#### Option 3: Full Rollback

**Scenario**: Skills 시스템 전체 문제

```bash
# Skills integration 전체 rollback
git checkout <before-skills-commit-hash>

# 또는 태그 사용
git tag skills-integration-start  # Phase 1 시작 전
git checkout skills-integration-start
```

### Rollback Verification

**체크리스트**:
- [ ] All 21 agents 정상 작동
- [ ] All 12 commands 정상 작동
- [ ] Quality gates 통과
- [ ] Integration tests 통과

### Prevention Measures

1. **Git Tags**: 각 Phase 시작/완료 시 태그
```bash
git tag skills-phase-1-start
git tag skills-phase-1-complete
git tag skills-phase-2-start
# ...
```

2. **Backups**: 모든 파일 변경 전 .backup 생성

3. **Progressive Rollout**: Phase별 순차 진행 (한 번에 전체 X)

4. **Testing**: 각 Phase 완료 후 검증 후 다음 Phase

---

## 📊 Post-Implementation

### Phase 6: Monitoring & Optimization (Ongoing)

#### Task 6.1: Usage Monitoring

**Metrics to Track**:

1. **Token Efficiency**:
```bash
# Weekly measurement
python3 scripts/measure_tokens.py > reports/tokens_$(date +%Y%m%d).txt
```

2. **Skills Usage**:
```bash
# Agent invocations per skill
grep "skills:" ~/.claude/logs/*.log | sort | uniq -c
```

3. **Quality Gates**:
```bash
# Pass/fail rate
grep "Quality gates" ~/.claude/logs/*.log | grep -c "PASSED"
grep "Quality gates" ~/.claude/logs/*.log | grep -c "FAILED"
```

#### Task 6.2: Skills Refinement

**Monthly Reviews**:
- Review skills usage statistics
- Identify unused supporting files (can be removed)
- Identify frequently accessed content (optimize for tokens)
- Update based on agent feedback

#### Task 6.3: Documentation Maintenance

**Quarterly Updates**:
- Update examples based on real usage
- Add new FAQs based on user questions
- Refine skills descriptions for better triggers
- Version updates (constitution v1.3, etc.)

### Success Metrics Dashboard

**Target Metrics** (3 months post-implementation):

| Metric | Target | Measurement |
|--------|--------|-------------|
| Token reduction | 30%+ | Weekly script |
| Duplicate content | 0 sections | Monthly scan |
| Constitution updates | 1 file only | Manual verification |
| Skills load success | 99%+ | Log analysis |
| Quality gates pass | 95%+ | Log analysis |
| Agent satisfaction | 4.5/5 | Survey (if team) |

**Monitoring Schedule**:
- Daily: Critical errors (skills load failures)
- Weekly: Token efficiency, quality gates
- Monthly: Duplicate detection, skills usage
- Quarterly: Full review, documentation updates

---

## 📋 Appendix

### A. File Templates

#### A1. Skill Template

**File**: `templates/SKILL_TEMPLATE.md`

```yaml
---
name: skill-name
description: Brief description of what this skill does and when to use it (include triggers). Max 1024 chars.
allowed-tools: Read, Write  # Optional: restrict tools
---
```

```markdown
# Skill Name

## Overview
What this skill provides...

## When to Use
- Trigger condition 1
- Trigger condition 2
- Trigger condition 3

## Supporting Documents
- `document1.md`: Description
- `document2.md`: Description
- `examples/`: Example files

## Quick Reference
[Key information that agents need most frequently]

### Section 1
Content...

### Section 2
Content...

For complete details, see supporting documents.
```

#### A2. Agent Update Template

**File**: `templates/AGENT_UPDATE_TEMPLATE.md`

```yaml
---
name: agent-name
description: [Keep existing]
tools: [Keep existing]
skills: spark-constitution, [additional-skills]  # ← ADD THIS LINE
model: [Keep existing]
color: [Keep existing]
---
```

```markdown
# Agent Name

[Keep existing content but REMOVE duplicate sections:]

❌ REMOVE:
- ## SPARK Constitution (duplicate of skill)
- ## Quality Gates (detailed version, duplicate of skill)
- ## Protocols (duplicate of skill)

✅ KEEP:
- ## Core Identity & Traits (agent-specific)
- ## Behavior Protocol (agent-specific)
- ## Professional Workflow (agent-specific)
- Quick reference to skills (not full duplication)

✅ ADD:
- Reference to skills in relevant sections
```

### B. Checklists

#### B1. Pre-Phase Checklist

```markdown
Before starting each phase:
- [ ] Previous phase 100% complete
- [ ] All tests passing
- [ ] Git committed (clean state)
- [ ] Backups created
- [ ] Time allocated
- [ ] Dependencies verified
```

#### B2. Post-Phase Checklist

```markdown
After completing each phase:
- [ ] All tasks completed
- [ ] Tests executed and passing
- [ ] Metrics measured
- [ ] Documentation updated
- [ ] Git committed with tag
- [ ] Rollback tested
- [ ] Stakeholder notified
```

#### B3. Agent Update Checklist

```markdown
For each agent update:
- [ ] Backup created (.backup file)
- [ ] YAML skills field added
- [ ] Duplicate content removed
- [ ] Token count measured
- [ ] Individual test executed
- [ ] Quality gates verified
- [ ] Git committed
```

### C. Scripts

#### C1. Batch Agent Update Script

**File**: `scripts/batch_update_agents.sh`

```bash
#!/bin/bash
# Batch update multiple agents with skills

set -e  # Exit on error

AGENTS=("$@")
if [ ${#AGENTS[@]} -eq 0 ]; then
  echo "Usage: $0 agent1 agent2 agent3..."
  exit 1
fi

for agent in "${AGENTS[@]}"; do
  file="spark-plugin/agents/${agent}.md"

  if [ ! -f "$file" ]; then
    echo "❌ File not found: $file"
    continue
  fi

  echo "Processing ${agent}..."

  # 1. Backup
  cp "$file" "${file}.backup"
  echo "  ✅ Backup created"

  # 2. Add skills field (after color: pink)
  # This is a placeholder - actual implementation needs agent-specific skills
  sed -i.tmp "/^color: pink$/a\\
skills: spark-constitution" "$file"
  rm "${file}.tmp"
  echo "  ✅ Skills field added"

  # 3. Verify YAML
  python3 -c "
import yaml
with open('$file') as f:
    content = f.read()
    frontmatter = content.split('---')[1]
    yaml.safe_load(frontmatter)
print('  ✅ YAML valid')
"

  # 4. Token count
  tokens=$(python3 scripts/count_agent_tokens.py "$file")
  echo "  ℹ️  Tokens: ${tokens}"

  echo "✅ ${agent} updated successfully"
  echo ""
done

echo "🎉 All agents updated!"
```

**Usage**:
```bash
./scripts/batch_update_agents.sh analyzer-spark tester-spark documenter-spark
```

#### C2. Token Counter Script

**File**: `scripts/count_agent_tokens.py`

```python
#!/usr/bin/env python3
"""Count tokens in agent definition file."""

import sys
import tiktoken

def count_tokens(file_path):
    with open(file_path) as f:
        content = f.read()

    enc = tiktoken.encoding_for_model("gpt-4")
    tokens = len(enc.encode(content))

    return tokens

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 count_agent_tokens.py <file>")
        sys.exit(1)

    file_path = sys.argv[1]
    tokens = count_tokens(file_path)

    print(f"{tokens}")
```

**Usage**:
```bash
python3 scripts/count_agent_tokens.py spark-plugin/agents/implementer-spark.md
# Output: 2534
```

### D. Decision Log

| Date | Decision | Rationale | Impact |
|------|----------|-----------|--------|
| 2025-12-03 | Use skills system | 94% token reduction | High |
| TBD | Skill versioning | Support v1.2, v1.3 | Medium |
| TBD | Hooks location | Plugin self-contained | Low |

### E. Lessons Learned

**To be updated during implementation**:

- Phase 1: [Learnings]
- Phase 2: [Learnings]
- Phase 3: [Learnings]
- Phase 4: [Learnings]
- Phase 5: [Learnings]

---

## 🎓 Using This Plan as a Reference

### For Other Projects

**이 계획을 다른 프로젝트에 적용할 때**:

1. **Executive Summary 작성**:
   - 3줄로 프로젝트 요약
   - 측정 가능한 목표 (숫자로!)
   - 예상 성과

2. **현재 상태 vs 목표 상태**:
   - 구체적인 파일 구조 비교
   - 측정 가능한 개선 지표
   - Before/After 명확히

3. **Success Criteria**:
   - 기능적, 성능적, 유지보수적 성공 정의
   - 각각 측정 방법 포함
   - Pass/Fail 명확히

4. **Risk Assessment**:
   - Risk matrix (Impact × Probability)
   - 각 risk별 mitigation strategy
   - Contingency plan

5. **Detailed Plan**:
   - Task breakdown (Phase → Task → Subtask)
   - 각 task별:
     - 소요시간 추정
     - 구체적 파일 경로
     - 코드 예시
     - 검증 방법
     - 성공 기준

6. **Rollback Plan**:
   - When to rollback (trigger conditions)
   - How to rollback (step-by-step)
   - Verification after rollback

7. **Post-Implementation**:
   - Monitoring metrics
   - Maintenance schedule
   - Success dashboard

### Key Principles

**이 계획의 핵심 원칙**:

1. **측정 가능**: 모든 목표와 성공 기준이 숫자로 측정 가능
2. **구체적**: "개선한다" ❌ → "3.9K→2.5K로 36% 개선" ✅
3. **실행 가능**: 각 task가 즉시 실행 가능한 수준으로 구체적
4. **검증 가능**: 각 단계마다 검증 방법 명시
5. **안전성**: 백업, rollback, 단계적 진행

---

**Document Version**: 1.0
**Last Updated**: 2025-12-03
**Author**: 2호 (Number Two)
**Status**: Ready for Execution ✅

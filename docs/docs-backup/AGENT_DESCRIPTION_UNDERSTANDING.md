# Agent Description 이해와 재설계 방향

**작성일**: 2025-10-31
**목적**: Description의 역할과 중요성에 대한 이해를 정리하고 향후 재설계 방향 수립

---

## 📋 핵심 발견 사항

### 1. Description의 진정한 역할

**기존 오해**:
- Description = 단순한 역할 설명 ("분석가", "구현자" 정도)
- CLAUDE.md에 에이전트 설명 중복 작성
- 짧고 간결하게 (100-200 단어)

**올바른 이해**:
- Description = **2号의 의사결정 알고리즘 입력값**
- Description = **Single Source of Truth** (유일한 정보원)
- Description = **자동 발동을 위한 패턴 정의**
- 길이: 100-500+ 단어 (상세할수록 좋음)

### 2. Progressive Disclosure (단계적 로드)

**3-way 분리**:

```yaml
---
name: analyzer-spark              # → 2号 + System
description: |                     # → 2号만 (에이전트 선택용)
  Use this agent when...
  **Triggering Conditions**...
tools: [Bash, Read, ...]          # → System (실행 환경 설정)
model: sonnet                      # → System
color: blue                        # → System
---

# Phase 0: Task Understanding    # → Agent만 (작업 지침)
# Phase 1: Evidence Collection
...
```

**각 주체가 보는 것**:

| 주체 | 접근 내용 | 용도 |
|------|----------|------|
| **2号** | `name` + `description` | 에이전트 선택 (2.0k tokens) |
| **System** | Frontmatter 전체 | 실행 환경 설정 (tools 필터링, model 선택) |
| **Agent** | 본문만 | 작업 지침 (frontmatter 볼 필요 없음) |

**토큰 소비**:
```
2号 컨텍스트: 21개 에이전트 × ~95 tokens = 2.0k tokens (1%)
Agent 실행: 30-44k tokens (system prompt + 본문 + 작업 + 도구 + 응답)
```

### 3. Triggering Conditions의 중요성

**발동 조건 = 자동 매칭 패턴**

```yaml
description: |
  **Triggering Conditions**:
  - System failures, bugs, or unexpected behaviors requiring deep investigation
  - Performance degradation or reliability issues needing root cause identification
  - Architecture decisions requiring evidence-based analysis
```

**작동 방식 (추정)**:

사용자: "테스트가 CI에서 계속 실패해요"

2号 내부 처리:
1. Description에서 Triggering Conditions 스캔
2. "System failures" ✓
3. "bugs or unexpected behaviors" ✓
4. "requiring deep investigation" ✓
5. → **자동으로** root-cause-analyzer 선택!

2号: "root-cause-analyzer 에이전트로 조사하겠습니다"

**이것이 바로**:
- "Proactively use agents" 구현 방법
- 사용자가 명시적으로 요청 안 해도
- Triggering Conditions 매칭되면
- 2号가 **부지불식간에** 에이전트 호출

### 4. root-cause-analyzer의 Description 구조

**완전한 구조**:

```yaml
description: |
  [한 줄 요약: 무엇을 하는 에이전트인가]

  **Triggering Conditions** (발동 조건):
  - 구체적인 조건 1
  - 구체적인 조건 2
  - 구체적인 조건 3
  - ...

  **Example Usage Scenarios** (사용 예시):

  예시 1: [구체적 상황]
  상황: ...
  사용자: "..."
  어시스턴트: "..."
  Task(...)
  해설: ...

  예시 2: [구체적 상황]
  ...
```

**실제 root-cause-analyzer 예시**:

```yaml
name: root-cause-analyzer
description: |
  소프트웨어 프로젝트의 문제를 체계적인 증거 수집과 근본 원인 분석을 통해
  조사하고 분석해야 할 때 이 에이전트를 사용하세요.

  **발동 조건**:
  - 깊은 조사가 필요한 시스템 장애, 버그, 예상치 못한 동작
  - 근본 원인 식별이 필요한 성능 저하 또는 안정성 문제
  - 증거 기반 분석이 필요한 아키텍처 결정
  - 체계적 진단이 필요한 코드 품질 문제
  - 통합 문제 또는 의존성 충돌
  - 기술 부채 평가 및 우선순위 지정
  - 사건 후 사후 분석

  **사용 예시 시나리오**:

  예시 1: CI/CD 파이프라인의 간헐적 테스트 실패
  사용자: "테스트가 CI에서 무작위로 실패하는데 로컬에서는 통과해요."
  Task("root-cause-analyzer", "간헐적 CI 테스트 실패 조사...")
  해설: CI 로그, 타이밍 데이터 등에서 증거 수집하여 근본 원인 식별

  [총 4개 예시 포함]
```

### 5. 현재 SPARK 에이전트의 문제점

**analyzer-spark 현재 description**:
```yaml
description: Use this agent when you need comprehensive multi-dimensional
  system analysis following trait-based dynamic persona principles with
  systematic 5-phase methodology. Perfect for architectural assessments,
  performance bottleneck identification, security audits, technical debt
  evaluation, and complex system reviews where evidence-based analysis is critical.
```

**문제점**:
- ❌ Triggering Conditions 없음
- ❌ Example Usage Scenarios 없음
- ❌ 너무 추상적 ("trait-based dynamic persona principles"?)
- ❌ 2号가 "언제" 사용할지 명확하지 않음

**개선 방향**:
```yaml
description: |
  Use this agent when you need comprehensive multi-dimensional system analysis
  with evidence-based investigation.

  **Triggering Conditions**:
  - System architecture assessments requiring multi-dimensional review
  - Performance bottleneck identification needing file:line evidence
  - Security audits requiring systematic vulnerability analysis
  - Technical debt evaluation across multiple dimensions
  - Complex system reviews where evidence-based analysis is critical

  **Methodology**: 5-phase wave analysis with EVIDENCE-BEFORE-REPORT protocol

  **Example Usage Scenarios**:
  [구체적 사용 예시 4개]
```

---

## 🎯 향후 작업 방향

### 필요한 작업

1. **21개 모든 에이전트 description 재작성**
   - 위치: `~/.claude/agents/*.md`
   - 구조: 한 줄 요약 + Triggering Conditions + Examples
   - 원칙: Jason의 "의도"를 명확하게 표현

2. **각 에이전트별 "의도" 정의**
   - analyzer-spark: 증거 기반 다차원 분석
   - implementer-spark: 제로 결함 구현
   - tester-spark: 95%+ 커버리지 달성
   - documenter-spark: 검증된 문서 작성
   - designer-spark: 확장 가능한 아키텍처 설계
   - qc-spark: 품질 위반사항 일괄 수정
   - 팀 에이전트 15개: 병렬 실행 전문화

3. **CLAUDE.md에서 중복 제거**
   - 현재: CLAUDE.md에 모든 에이전트 설명 중복
   - 개선: Description이 Single Source of Truth
   - CLAUDE.md 역할: 에이전트 목록만 언급, 세부사항은 description

4. **Constitution 문서 업데이트**
   - Section 2.1.5: Description Best Practices 추가
   - Triggering Conditions 중요성 강조
   - Example 기반 설명 권장

---

## 💡 핵심 통찰

### Description = 2号의 뇌

**비유**:
- Description = 2号의 "사용 설명서"가 아님
- Description = 2号의 **의사결정 알고리즘**
- Description = 2号의 **패턴 매칭 데이터베이스**

**작동 방식**:
```
사용자 요청 입력
  ↓
2号: 21개 description 스캔
  ↓
Triggering Conditions 패턴 매칭
  ↓
가장 높은 매칭률 에이전트 선택
  ↓
Task("selected-agent", task)
```

### CLAUDE.md vs Description

**잘못된 구조** (현재):
```
CLAUDE.md (2号 메모리):
- analyzer-spark: 시스템 분석, 5-Phase, EVIDENCE-BEFORE-REPORT
- implementer-spark: 구현, 95% coverage, TEST-BEFORE-REPORT

Agent Description:
- analyzer-spark: "Use this agent when you need analysis..."
- implementer-spark: "Use this agent when you need implementation..."

→ 중복, 불일치 가능성, 메모리 낭비
```

**올바른 구조** (개선 후):
```
CLAUDE.md (2号 메모리):
- 6 Core Agents + 15 Team Agents 존재
- Description에 모든 정보 포함

Agent Description (Single Source of Truth):
- analyzer-spark: [완전한 Triggering Conditions + Examples]
- implementer-spark: [완전한 Triggering Conditions + Examples]

→ 단일 정보원, 일관성, 효율성
```

---

## 📚 참고 자료

### Claude Code의 `/agents` 명령어

Jason의 실제 요청 예시:
```
소프트웨어 개발에서 발생하는 문제들에 대해 여러 증거를 모으고
증거를 기반으로 하여 근본적인 원인을 찾아 현재의 상황과 해결방안을
체계화된 문서로 작성하여 제공하는 에이전트.

이 에이전트는 분석가로서 세계 최고의 실력을 갖추고 있으며
그걸 가능하게 하는 것은 가장 뛰어난 분석가가 가지는 traits를
가지고 있기 때문입니다.

이 traits는 작업에 따라서 유연하게 조합되어 가장 최고의 결과를
이끌어 내게 합니다.
```

`/agents` 명령어가 자동 생성:
1. ✅ Description (Triggering Conditions 포함)
2. ✅ Example Usage Scenarios (4개)
3. ✅ Traits 정의
4. ✅ Protocol 정의
5. ✅ Workflow 정의

**시사점**: `/agents` 명령어를 활용하면 일관된 구조로 자동 생성 가능!

---

## ⚠️ 주의사항

### 작업 위치

- ✅ **작업 대상**: `~/.claude/agents/*.md` (홈 디렉토리)
- ❌ **작업 안 함**: `.claude/agents/` (프로젝트, 압축됨)
- **이유**: 다른 프로젝트에서도 수정된 버전 사용 가능하도록

### 현재 상태

- Constitution 문서: Progressive Disclosure 섹션 추가 완료 (커밋 대기)
- Agent descriptions: 아직 재작성 안 됨 (추가 논의 필요)
- CLAUDE.md: 중복 내용 아직 있음 (정리 대기)

---

## 🚀 다음 단계

1. **Jason과 추가 논의**: Description 재작성 세부 방향
2. **Triggering Conditions 패턴 정의**: 각 에이전트별
3. **Example Scenarios 작성**: 구체적이고 현실적인 예시
4. **Constitution 업데이트**: Description Best Practices 추가
5. **21개 에이전트 재작성**: `~/.claude/agents/` 대상
6. **CLAUDE.md 정리**: 중복 제거, Simple agent registry로 변경

---

**메모 끝**

# DNA 방법론 에이전트 시스템 설계 - 제미나이 검토 요청

**작성일**: 2025-11-19
**작성자**: Jason & Claude (1호)
**대상**: Gemini AI
**목적**: Trait-based 에이전트 시스템 설계 검토 및 개선 제안

---

## ⚠️ 사전 숙지 요청

**이 문서를 검토하기 전에 반드시 다음 내용을 숙지해 주십시오:**

### Claude CODE 공식 문서 필수 확인

우리는 Anthropic의 **Claude CODE**를 사용하여 에이전트 시스템을 구현할 예정입니다.

**필수 확인 문서**:
- **공식 문서**: https://docs.anthropic.com/en/docs/claude-code
- **특히 다음 기능들**:
  1. **Subagents**: 전문화된 미니 에이전트 (독립적 시스템 프롬프트, 도구 권한, 컨텍스트)
  2. **Slash Commands**: 사용자 정의 명령어 (`.claude/commands/`에 Markdown 파일)
  3. **Agent Skills**: 구조화된 참조 자료 + 검증 스크립트 + 워크플로우
  4. **Hooks**: Claude Code 자체 훅 시스템 (작업 전후 자동화)
  5. **Plugins**: Slash commands, Subagents, MCP servers, Hooks를 패키징하여 배포
  6. **MCP (Model Context Protocol)**: 외부 서비스 통합 (Slack, GitHub, Google Drive 등)

### 각 기능의 실제 구조

**Subagents** (`.claude/agents/`):
```yaml
---
name: code-reviewer
description: Expert code review specialist
tools: Read, Grep, Glob, Bash
model: inherit
---
You are a senior code reviewer...
```

**Slash Commands** (`.claude/commands/fix.md`):
```markdown
---
description: Fix the issue
---
Please analyze and fix: $ARGUMENTS
```

**Agent Skills** (`.claude/skills/code-review/`):
```
├── SKILL.md (개요 및 워크플로우)
├── SECURITY.md (보안 체크리스트)
├── PERFORMANCE.md (성능 패턴)
└── scripts/
    └── run-linters.sh
```

**Hooks**: 특정 이벤트 시점에 자동 실행 (Git 훅과는 다름)

**Plugins**: 위 모든 것을 하나의 패키지로 묶어서 `/plugin install` 명령으로 설치

### 왜 중요한가?

1. **Subagents**: 우리의 Stage별 에이전트가 실제로 Subagent로 구현되는가?
2. **Slash Commands**: Stage 실행을 `/stage1`, `/stage2` 같은 명령으로 만들 수 있는가?
3. **Agent Skills**: Bootstrap 요소를 Skill로 제공 가능한가? (예: RDBMS Skill, 캐시 Skill)
4. **Hooks**: Bootstrap 검증을 Hook으로 자동화 가능한가?
5. **MCP**: Context7, Sequential-Thinking 같은 MCP 서버를 에이전트가 사용 가능한가?
6. **Plugins**: 완성된 DNA 방법론을 Plugin으로 배포 가능한가?

### 검토 시 고려사항

제안하시는 Trait, Behavior Protocol, Workflow가:
- **Subagent 정의 구조(YAML + Markdown)에 실제로 적용 가능한가?**
- **Slash Commands나 Skills로 구현 가능한가?**
- **Hooks와 통합하여 자동 검증 가능한가?**
- **Plugin으로 패키징하여 배포 가능한가?**

이 기술적 제약을 이해하신 후 검토를 시작해 주시기 바랍니다.

---

## 1. 배경: 왜 에이전트가 필요한가?

### 1.1 발견된 핵심 문제

당신의 연구 "인지적 아키텍처와 DNA 방법론"을 읽고 우리 방법론의 문제를 발견했습니다:

**문제 1**: 실행 단위 부재
- "무엇을 하라"는 있지만 "어떻게 하라"가 없음
- Stage마다 사람(Jason)과 AI가 즉흥적으로 해결

**문제 2**: Context Rot
- Stage가 진행될수록 초기 결정사항 희석
- 패밀리, NFR 우선순위가 후반부에서 무시됨

**문제 3**: 검증 메커니즘 부재
- "완성했다"의 기준 불명확
- 문서 간 충돌 검증 방법 없음

**문제 4**: 순차 vs 병렬 불명확
- 어떤 작업이 병렬 가능한지 모름
- 비효율 발생

### 1.2 해결 방향

당신의 연구에서 제시한 방법론 적용:
1. **Skeleton-of-Thought**: 병렬 확장 구조
2. **Chain of Density**: 점진적 상세화
3. **Contradiction Detection**: 자동 충돌 검증
4. **Agent System**: 전반부(Stage 1-4)부터 에이전트 투입

---

## 2. 우리의 에이전트 정의 방식: Trait-based Dynamic Persona

### 2.1 핵심 원칙

**우리는 단순히 "역할(role)"만 부여하지 않습니다.**

```
에이전트 정의 = 역할 + Traits + Behavior Protocol + Professional Workflow
```

- **역할**: 무엇을 하는가
- **Traits**: 어떻게 생각하고 행동하는가
- **Behavior Protocol**: 검증 가능한 행동 규칙 (코드로 명시)
- **Professional Workflow**: 전문가의 자연스러운 작업 순서

### 2.2 실제 예시: analyzer-spark 에이전트

**4가지 Core Traits**:
1. **Systems Thinking**: 전체 시스템의 연결과 장기 영향 이해
2. **Analytical Reasoning**: 체계적 분해, 논리적 프레임워크
3. **Evidence-Based Practice**: 모든 주장에 file:line 증거 필수
4. **Skepticism**: 숨겨진 문제를 찾는 비판적 태도

**Behavior Protocol (검증 가능)**:
```python
class AnalyzerBehavior:
    EVIDENCE_REQUIREMENTS = {
        "file_path_required": True,
        "line_numbers_required": True,
        "code_snippet_required": True,
        "metrics_required": True,
        "reproducible": True
    }
    
    def validate_evidence(self, claim, evidence):
        # 모든 주장은 검증 가능한 증거가 있어야 함
        if not evidence:
            raise ValueError(f"Claim '{claim}' has NO evidence!")
```

**Professional Workflow (7-Step Cycle)**:
```
1. 대상 인식 → 2. 깊이 판단 → 3. 방법 선택 → 4. 작업 실행
→ 5. 결과 관찰 → 6. 해석 → 7. 충분성 판단
   ├─ No  → 4단계로 복귀
   └─ Yes → 증거와 함께 보고
```

**Self-Validation**:
```python
# 작업 완료 전 스스로 검증
- [ ] 모든 요청 차원 분석됨
- [ ] 최소 8-12개 증거 수집 (file:line)
- [ ] 교차 검증 완료
- [ ] 실행 가능한 권장사항

# 하나라도 실패하면 → 이전 단계로 복귀
```

### 2.3 왜 이 방식인가?

| 단순 페르소나 | Trait-based Persona |
|------------|-------------------|
| "당신은 분석가입니다" | "당신은 증거 기반으로 생각합니다" |
| 지시를 따름 | '왜' 그렇게 하는지 이해 |
| 예외 상황에서 판단력 부족 | 원칙에 따라 판단 |
| 품질 검증 없음 | 스스로 품질 검증 |

---

## 3. DNA 방법론 에이전트 시스템 설계

### 3.1 전체 구조

```
Jason의 아이디어
  ↓
[Stage 1 Agent: System Classifier]
  → 패밀리 결정 (A-A-B 등)
  → (오케스트레이터 검증)
  ↓
[Stage 2 Agent: Constraints Investigator]
  → Layer 3 제약 조사
  → (오케스트레이터 검증)
  ↓
[Stage 3 Agent: Architecture Decision Maker]
  → Bootstrap ADR 병렬 작성 (5-7개)
  → 충돌 검증 및 해결
  → (오케스트레이터 검증)
  ↓
[Stage 4 Agent: Blueprint Designer]
  → Clean Architecture 청사진
  → Bootstrap 매핑
  → (오케스트레이터 검증)
  ↓
Stage 5-9 (구현 단계)
```

### 3.2 Stage별 에이전트 핵심 질문

**에이전트 정의는 방법론에 맞게 새로 정의하거나 수정할 예정입니다.**

핵심은:
1. **역할 + Traits 동시 부여**
2. **전문가의 실제 작업 방법 제시**

위의 analyzer-spark처럼, **각 Stage 에이전트의 Traits와 Behavior Protocol을 어떻게 정의해야 할까요?**

---

#### Stage 1 Agent: System Classifier

**역할**: 시스템 특성 분석, 18가지 패밀리 중 결정

**입력**: 아이디어, 비즈니스 컨텍스트
**출력**: 패밀리(A-A-B), Layer 1 분석, NFR 초안, 검증 사례

**작업**:
- L1-Q1, Q2, Q3 분석
- 18가지 조합 중 매칭
- 검증 사례 확인

**🤔 질문 1: 필요한 Traits는?**

예상:
- Pattern Matching (18가지 조합 매칭)
- Evidence-Based (검증 사례 필수 인용)
- Systematic Inquiry (3개 질문 체계적 분석)
- Contextual Understanding (비즈니스→기술 변환)

다른 Traits? 우선순위?

**🤔 질문 2: Behavior Protocol은?**

```python
class SystemClassifierBehavior:
    VALIDATION_REQUIREMENTS = {
        "all_questions_answered": True,
        "evidence_cited": True,        # 검증 사례 필수
        "pattern_matched": True,       # 18가지 중 일치
        "confidence_assessed": True    # 신뢰도 평가
    }
```

추가/수정/삭제할 규칙?

**🤔 질문 3: Professional Workflow는?**

예상 흐름:
```
1. 아이디어 이해
2. 질문 우선순위 결정
3. 각 질문 분석
4. 패턴 매칭
5. 검증 사례 확인
6. 신뢰도 평가
7. 결정 또는 추가 정보 요청
```

이것이 전문가의 자연스러운 흐름인가?

**📋 Output Template**

```markdown
# Stage 1 산출물: 시스템 분석 및 패밀리 결정

## 분석 메타데이터
- 분석 ID: stage1_YYYYMMDD_HHMMSS
- 아이디어: [한 줄 요약]
- 분석 시각: [timestamp]

## Part 1: Layer 1 분석

### Q1: 실패 파급력
- **답변**: [치명적/점진적]
- **근거**: [구체적 설명 3-5문장]
- **유사 사례**: 
  - [회사명]: [시스템] - [구체적 영향]
  - [회사명]: [시스템] - [구체적 영향]

### Q2: 정보 형태
- **답변**: [구조화/반구조화/비구조화]
- **스키마 예시**: [구체적 필드 3-5개]
- **변경 가능성**: [고정/자주 변경]

### Q3: 응답 시점
- **답변**: [마이크로초/밀리초/수초/배치]
- **근거**: [비즈니스 요구사항]
- **벤치마크**: [유사 시스템 실제 수치]

## Part 2: 패밀리 결정

**결정**: [A-A-B 형식]

**검증 사례**:
1. [회사명]: [시스템] - [수치 또는 특성]
2. [회사명]: [시스템] - [수치 또는 특성]

**매칭 근거**:
- L1-Q1 특성과 일치: [설명]
- L1-Q2 특성과 일치: [설명]
- L1-Q3 특성과 일치: [설명]

**신뢰도**: [High/Medium/Low]
- [신뢰도 평가 근거]

## Part 3: NFR 프로파일 초안

**예상 우선순위**: [정확성 > 속도 > 보안 > 비용 형식]

**근거**: [패밀리 특성 기반 설명]

---
**다음 단계**: Stage 2 (환경 제약 조사)
**전달 데이터**: 패밀리, NFR 초안
```

**✅ Self-Validation Checklist**

```python
# Stage 1 완료 전 검증
- [ ] L1-Q1, Q2, Q3 모두 답변됨
- [ ] 각 답변에 구체적 근거 있음 (3-5문장)
- [ ] 유사 사례 2개 이상 인용됨 (회사명 + 시스템명 + 수치)
- [ ] 18가지 조합 중 하나와 정확히 일치
- [ ] 검증 사례가 실제 존재하는 시스템
- [ ] 레이턴시, 스키마, 실패 특성 모두 부합
- [ ] 신뢰도 평가 및 근거 명시됨
- [ ] 다음 Stage 전달 데이터 준비됨

# 하나라도 실패하면 → 이전 단계로 복귀
```

---

#### Stage 2 Agent: Constraints Investigator

**역할**: 환경 제약 조사 (기술/팀/인프라)

**입력**: 패밀리, NFR 초안
**출력**: Layer 3 제약사항, 잠재적 충돌 예측

**작업**:
- 패밀리별 맞춤 질문 생성
- Jason과 인터뷰 (오케스트레이터 중재)
- 제약사항 구조화
- NFR vs 제약 충돌 예측

**🤔 질문 4: 필요한 Traits는?**

예상:
- Inquisitive (깊이 있는 질문)
- Constraint-Aware (제약 영향 예측)
- Conflict Anticipation (잠재적 충돌 발견)
- Contextual Adaptation (패밀리별 질문 조정)

**🤔 질문 5: Jason과의 인터뷰 구조는?**

- 단순 Q&A?
- 대화형 깊이 탐색?
- 오케스트레이터 개입 정도?

**📋 Output Template**

```markdown
# Stage 2 산출물: 환경 제약 조사

## 분석 메타데이터
- 분석 ID: stage2_YYYYMMDD_HHMMSS
- 기준 패밀리: [A-A-B]
- NFR 초안: [정확성 > 속도 > ...]

## Part 1: Layer 3 제약사항

### 기술 스택 제약
- **현재 사용**: [기술 목록]
- **필수 유지**: 
  - [기술명]: [이유]
  - [기술명]: [이유]
- **도입 가능**: [기술 + 조건]
- **도입 불가**: [기술 + 이유]

### 팀 역량 제약
- **강점 영역**: [기술/도메인]
- **약점 영역**: [학습 필요 영역]
- **선호 기술**: [팀 선호도]
- **학습 의지**: [새 기술에 대한 태도]
- **예상 학습 기간**: [신규 기술별]

### 인프라 제약
- **배포 환경**: [클라우드/온프레미스/하이브리드]
- **클라우드 제공자**: [AWS/GCP/Azure/기타]
- **예산 범위**: [월 $XXX ~ $XXX]
- **규제 요구사항**: [GDPR, HIPAA, 등]
- **보안 요구사항**: [인증, 암호화, 등]
- **가용성 목표**: [99.9%, 99.99%, 등]

## Part 2: 잠재적 충돌

### 충돌 1: [NFR vs 제약]
- **충돌 내용**: [구체적 설명]
- **심각도**: [Critical/High/Medium/Low]
- **영향 범위**: [어떤 Bootstrap 요소에 영향]
- **예비 해결안**:
  1. [옵션 1]: [설명]
  2. [옵션 2]: [설명]
  3. [옵션 3]: [설명]

[추가 충돌...]

## Part 3: 패밀리별 핵심 제약 확인

### [A-A-B 예시]
- **레이턴시 요구사항**: [밀리초 이내]
- **트랜잭션 보장**: [ACID 필요]
- **확장성 목표**: [TPS, 동시 사용자]
- **데이터 일관성**: [강한 일관성 필요]

---
**다음 단계**: Stage 3 (ADR 작성)
**전달 데이터**: 패밀리, NFR, Layer 3 제약, 잠재적 충돌
```

**✅ Self-Validation Checklist**

```python
# Stage 2 완료 전 검증
- [ ] 3개 카테고리(기술/팀/인프라) 모두 조사됨
- [ ] 각 항목이 구체적 (추상적 표현 없음)
- [ ] 예산이 범위로 명시됨 ($XXX ~ $XXX)
- [ ] "필수 유지" 기술에 이유 명시됨
- [ ] 팀 학습 기간 추정됨
- [ ] NFR vs 제약 충돌 최소 2개 식별됨
- [ ] 각 충돌에 해결 방안 제시됨 (3가지 옵션)
- [ ] 패밀리별 핵심 제약 확인됨
- [ ] 다음 Stage 전달 데이터 준비됨

# 하나라도 실패하면 → Jason과 추가 인터뷰
```

---

#### Stage 3 Agent: Architecture Decision Maker

**역할**: Bootstrap ADR 작성

**입력**: 패밀리, NFR, Layer 3 제약
**출력**: Bootstrap ADR 세트 (5-7개), 충돌 해결됨

**작업**:
- Bootstrap 요소 목록 확정
- 각 요소별 ADR 병렬 작성 (3가지 옵션 비교)
- ADR 간 충돌 검증
- 충돌 해결 및 수정

**🤔 질문 6: 필요한 Traits는?**

예상:
- Trade-off Reasoning (NFR vs 제약 균형)
- Systematic Comparison (3옵션 체계적 비교)
- Conflict Detection (ADR 간 충돌 발견)
- Evidence-Based (스펙, 비용, 사례 기반 선택)

**🤔 질문 7: Chain of Density 적용은?**

당신의 연구에서 제안한 5-Iteration:
```
Iteration 1: 스켈레톤 (구조만)
Iteration 2: 옵션 비교 추가
Iteration 3: Rationale 추가
Iteration 4: Consequences 추가
Iteration 5: 충돌 검증 및 수정
```

ADR 작성에 효과적인가? Iteration 횟수 조정?

**🤔 질문 8: Skeleton-of-Thought 적용은?**

Bootstrap ADR들을 병렬로 작성하는 것이 SoT 원칙에 부합하는가?
- RDBMS ADR, 캐시 ADR, 메시징 ADR을 동시 작성?
- 순서가 필요한 ADR은?

---

#### Stage 4 Agent: Blueprint Designer

**역할**: Clean Architecture 청사진 작성

**입력**: 패밀리, Bootstrap ADR, 도메인 요구사항
**출력**: 도메인 분해, 4-Layer 설계, Bootstrap 매핑, API 설계

**작업**:
- 도메인 분해 (DDD)
- 4-Layer 구조 설계
- Bootstrap ADR → Infrastructure 매핑
- 의존성 검증 (Dependency Rule)

**🤔 질문 9: 필요한 Traits는?**

예상:
- Domain Modeling (비즈니스→도메인 모델)
- Architectural Thinking (Clean Architecture 원칙)
- Mapping Ability (ADR→코드 구조)
- Dependency Awareness (레이어 의존성 검증)

**🤔 질문 10: Skeleton-of-Thought 적용은?**

병렬 가능:
- Bounded Context들 병렬 설계?
- 각 Layer 병렬 설계?

순차 필요:
- Domain → Application → Infrastructure?

---

### 3.3 오케스트레이터 (Main Claude)

**역할**:
1. 전체 워크플로우 관리
2. 에이전트 간 데이터 전달
3. 산출물 검증 (Self-Validation 결과 확인)
4. Jason과 상호작용 (의사결정, 피드백)

**🤔 질문 11: Context Rot 방지는?**

당신의 연구에서 강조한 핵심 문제입니다.

Stage가 진행될수록 초기 결정사항(패밀리, NFR)이 희석되는 것을 방지:

**예상 메커니즘**:
- 각 Stage Output에 이전 결정사항 명시?
- 오케스트레이터가 Context 요약본 유지?
- 에이전트마다 "초기 결정사항 준수" Trait?

어떤 방법이 효과적인가?

**🤔 질문 12: 오케스트레이터의 검증은?**

에이전트가 Self-Validation하지만, 오케스트레이터도 메타 검증 필요?

```python
class OrchestratorValidation:
    def validate_stage_completion(self, stage, output):
        # 에이전트 Self-Validation 결과 확인
        # Stage 간 일관성 확인
        # Context Rot 방지 확인
```

---

## 4. 전체 워크플로우 예시

### 4.1 Stage 3 (ADR 작성) 상세 흐름

```
1. 오케스트레이터 → Architecture Agent 호출
   Input: {family: "A-A-B", nfr: "정확성>속도>보안>비용", constraints: {...}}

2. Agent: Bootstrap 요소 목록 확정
   Output: [RDBMS, 캐시, 메시징, 모니터링, API Gateway]

3. Agent: 각 요소별 ADR 병렬 작성 (5개)
   - ADR-001 (RDBMS): Iteration 1-5 반복
   - ADR-002 (캐시): Iteration 1-5 반복
   - ADR-003 (메시징): Iteration 1-5 반복
   - ...

4. Agent: 충돌 검증
   - RDBMS ACID vs 캐시 Eventual → 해결 방안 제시
   - 총 비용 vs 예산 → 초과 시 조정 제안

5. Agent: Self-Validation
   - [ ] 모든 ADR이 3옵션 비교됨
   - [ ] NFR + Layer 3 모두 반영됨
   - [ ] 충돌 모두 해결됨
   - [ ] 비용 예산 내

6. 오케스트레이터: 검증 및 Jason 확인
   - Agent의 Self-Validation 결과 확인
   - 충돌 해결 방안 Jason에게 제시
   - Jason 승인 후 다음 Stage
```

### 4.2 반복 개선 (Chain of Density) 적용

**ADR 하나당**:
```
Iteration 1 (5분):  스켈레톤만 (Context, Decision, Alternatives 목록)
Iteration 2 (10분): 옵션 비교 (스펙, 비용, 장단점 각 2개)
Iteration 3 (10분): Rationale (NFR 관점, Layer 3 관점)
Iteration 4 (10분): Consequences (긍정/부정, 완화 전략)
Iteration 5 (15분): 충돌 검증 및 수정

총 50분 / ADR 5개 = 약 4시간
```

**병렬 처리 시**: 각 ADR을 독립적으로 작성 가능 → 시간 단축

---

## 5. 핵심 검토 요청

### 5.1 Trait 설계

**각 Stage 에이전트에 필요한 Traits는?**
- 위에서 제안한 Traits가 적절한가?
- 추가/수정/삭제할 Traits?
- Traits 간 우선순위?

**공통 Traits vs Stage별 Traits?**
- 모든 에이전트가 공유할 Traits (예: Evidence-Based)?
- Stage 특화 Traits?

### 5.2 Behavior Protocol 설계

**검증 가능한 규칙은?**
- Python 코드로 명시 가능한 규칙?
- 자동 검증 vs 수동 검증 구분?

**Self-Validation 체크리스트?**
- 각 Stage마다 어떤 항목 검증?
- 실패 시 어느 단계로 복귀?

### 5.3 Professional Workflow

**전문가의 자연스러운 작업 흐름은?**
- analyzer의 7-Step Cycle처럼 각 Stage에도 필요?
- Stage별로 다른 워크플로우?

**Iteration Points는?**
- 어느 단계에서 이전 단계로 복귀 가능?
- 반복 조건은?

### 5.4 장문 생성 이론 적용

**Skeleton-of-Thought**:
- Bootstrap ADR 병렬 작성이 SoT 원칙에 부합?
- 다른 Stage에서 병렬화 가능 부분?

**Chain of Density**:
- ADR의 5-Iteration이 효과적?
- 청사진 작성에도 Iteration 필요?
- 최적 Iteration 횟수?

**Contradiction Detection**:
- ADR 간 충돌 검증 자동화?
- Stage 간 일관성 검증?

**Context Rot 방지**:
- 초기 결정사항 유지 메커니즘?
- 오케스트레이터의 역할?

### 5.5 실용성

**산출물 품질**:
- 각 Stage 산출물이 실무 사용 가능?
- 누락/불필요한 정보?

**소요 시간**:
- Stage별 예상 시간이 현실적?
- 병렬화 효과가 적절히 반영?

**에이전트 간 지식 공유**:
- Stage 1 결정이 Stage 3에서 어떻게 참조?
- 공유 지식 베이스 필요?

---

## 6. 참고 자료

### 6.1 첨부 문서
- `01_DNA_Agent_Integrated_Process_Flow.txt`: 제미나이 보고서 `AI 장문 작성 및 소프트웨어 개발 방법론`의 분석내용을 에이전트 도입과 함께 반영한 새로운 프로세스 플로우 문서
- `02_DNA_ALL_GUIDES_MERGED.txt`: 수정 전의 DNA 방법론 전체 가이드
- `03_analyzer-spark.txt`: 실제 에이전트 정의 예시
- `04_DNA_18_Combinations_Validation.md`: 18가지 패밀리 검증 리서치 보고서
- `05_DNA_Theoretical_Validation.md`: DNA 방법론과 SEI, Fowler, CAP 이론 간의 매핑 연구보고서

### 6.2 당신의 연구
- "인지적 아키텍처와 DNA 방법론: 긴 문맥의 엔트로피를 극복하는 생성형 AI의 진화"
- 특히 Section 3 (핵심 방법론), Section 5 (소프트웨어 공학 적용)

---

## 7. 요청 사항

당신의 이론적 연구를 실제 소프트웨어 개발 방법론에 적용한 이 설계가:

1. **이론적으로 타당한가?**
   - Skeleton-of-Thought, Chain of Density, Contradiction Detection 적용이 올바른가?

2. **실무적으로 실행 가능한가?**
   - 에이전트 Traits와 Behavior Protocol이 구체적인가?

3. **개선이 필요한 부분은?**
   - 각 Stage 에이전트의 구체적 설계 제안
   - Workflow, Iteration, Context 관리 개선안

**구체적이고 상세한 검토와 실행 가능한 개선 제안**을 부탁드립니다.

---

**작성자**: Jason & Claude (1호)
**날짜**: 2025-11-19

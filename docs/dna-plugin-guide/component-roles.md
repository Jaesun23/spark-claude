# Agents, Commands, Skills 역할 및 기능 정리

## 개요

Claude Code의 세 가지 핵심 컴포넌트는 각각 다른 역할을 담당합니다:

| 컴포넌트 | 역할 | 비유 |
|----------|------|------|
| **Skills** | 지식 저장소 | 전문 서적, 레퍼런스 매뉴얼 |
| **Commands** | 실행 트리거 | 버튼, 명령어 인터페이스 |
| **Agents** | 작업 수행자 | 전문가, 실행자 |

---

## 1. Skills - 지식 저장소

### 역할
- 방법론, 패턴, 템플릿 등 **정적 지식** 저장
- 필요할 때만 로드되어 **컨텍스트 효율** 극대화
- Progressive Disclosure로 단계적 정보 제공

### 특징
```
├── 컨텍스트 효율: 필요할 때만 로드
├── 구조화된 지식: 참조 문서 + 템플릿
├── 재사용성: 여러 에이전트/명령어에서 공유
└── 유지보수: 지식만 별도 업데이트 가능
```

### DNA에서의 활용

```
skills/
├── dna-methodology/
│   ├── SKILL.md                    # 방법론 개요
│   └── references/
│       ├── core/
│       │   ├── methodology-overview.md
│       │   ├── families.md         # 7개 패밀리
│       │   └── nfr-definitions.md
│       └── stage1-9/               # Stage별 상세
```

### Skills가 담는 내용

1. **핵심 개념**: 7개 패밀리, NFR 정의, Context Rot 방지
2. **템플릿**: ADR 템플릿, 체크리스트 템플릿
3. **패턴**: 아키텍처 패턴, 기술 선택 가이드
4. **참조 문서**: 기존 가이드/매뉴얼 링크

### Skills가 하지 않는 것

- ❌ 직접 작업 수행
- ❌ 사용자 입력 처리
- ❌ 동적 결정

---

## 2. Commands - 실행 트리거

### 역할
- 사용자가 작업을 **시작**하는 인터페이스
- 적절한 에이전트를 **호출**
- 인자 처리 및 **오케스트레이션**

### 특징
```
├── 인터페이스: 사용자와 시스템 연결
├── 오케스트레이션: 에이전트 조합/순서 결정
├── 인자 처리: 입력 검증 및 전달
└── 간결함: 복잡한 로직은 에이전트에 위임
```

### DNA에서의 활용

```
commands/
├── stage1.md       # Stage 1 실행
├── stage2.md       # Stage 2 실행
├── ...
├── dna-init.md     # 프로젝트 초기화
├── dna-audit.md    # 전체 DNA 검증
└── multi-stage.md  # 병렬 Stage 실행
```

### Command 설계 원칙

1. **단순 진입점**: 복잡한 로직 없음
2. **명확한 목적**: 하나의 명령 = 하나의 목표
3. **에이전트 위임**: 실제 작업은 에이전트가 수행
4. **체이닝 가능**: 여러 에이전트 순차/병렬 호출

### Command 예시

```markdown
---
name: stage1
description: Stage 1 핵심 기능 분류 실행
requires: stage1-classifier
---

# /stage1 - 핵심 기능 분류

이 명령어는:
1. 프로젝트 컨텍스트 수집
2. stage1-classifier 에이전트 호출
3. 패밀리 분류 문서 생성
```

---

## 3. Agents - 작업 수행자

### 역할
- 실제 **분석/생성/검증** 작업 수행
- 전문화된 **페르소나**로 특정 영역 담당
- **품질 게이트** 통과 책임

### 특징
```
├── 전문성: 특정 도메인/작업에 특화
├── 자율성: 할당된 작업 독립 수행
├── 품질 책임: 검증 후 결과 반환
└── 도구 사용: Read, Write, Bash 등 활용
```

### DNA에서의 활용

```
agents/
├── stage1-classifier.md      # 핵심 기능 분류
├── stage2-architect.md       # 환경 제약 설계
├── stage3-adr-author.md      # ADR 작성
├── stage4-standards-author.md # 표준 문서화
├── stage5-planner.md         # DNA 시스템 계획
├── stage6-implementer.md     # DNA 시스템 구현
├── stage7-blueprint-writer.md # 청사진 작성
├── stage8-task-breaker.md    # 작업 분해
└── stage9-checklist-author.md # 체크리스트 작성
```

### Agent 설계 원칙

1. **명확한 정체성**: 역할과 전문성 정의
2. **단계별 프로세스**: Phase 0-N 구조
3. **품질 검증**: 마지막 Phase에서 검증
4. **산출물 정의**: 무엇을 생성하는지 명확

### Agent 예시 구조

```markdown
---
name: stage1-classifier
description: 핵심 기능 분류 전문가
tools: Read, Write, Bash, Glob, Grep
model: sonnet
---

# Stage 1 Classifier

## Identity
시스템 아키텍트로서 기능적 분해 전문가

## Phase 0: Task Understanding
작업 이해 및 컨텍스트 수집

## Phase 1: Function Identification
핵심 기능 식별

## Phase 2: Family Classification
7개 패밀리 중 하나로 분류

## Phase 3: Quality Verification
분류 결과 검증
```

---

## 4. 세 컴포넌트의 상호작용

### 일반적인 흐름

```
사용자 → Command → Agent → (Skills 참조) → 산출물
```

### 상세 흐름

```
┌────────────────────────────────────────────────────┐
│ 1. 사용자: /stage1 "결제 플랫폼"                    │
└────────────────┬───────────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────────┐
│ 2. Command (stage1.md)                             │
│    - 인자 파싱: project_name = "결제 플랫폼"        │
│    - Agent 선택: stage1-classifier                 │
│    - 호출 준비                                      │
└────────────────┬───────────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────────┐
│ 3. Agent (stage1-classifier.md)                    │
│    Phase 0: 작업 이해                               │
│    Phase 1: 기능 식별                               │
│       ├─ Skills 참조: families.md (7개 패밀리)      │
│       └─ Skills 참조: nfr-definitions.md           │
│    Phase 2: 패밀리 분류                             │
│    Phase 3: 품질 검증                               │
└────────────────┬───────────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────────┐
│ 4. 산출물                                          │
│    01C-01_family_classification.md                 │
│    stage1_output.json                              │
└────────────────────────────────────────────────────┘
```

---

## 5. DNA 방법론에서의 역할 분담

### Skills의 역할

| 지식 영역 | 내용 |
|-----------|------|
| Core | 방법론 개요, 7개 패밀리, NFR 정의, Context 관리 |
| Stage별 | Layer 질문, ADR 템플릿, 체크리스트 형식 |
| Patterns | 아키텍처 패턴, 기술 선택 가이드 |

### Commands의 역할

| 명령어 | 목적 | 호출 Agent |
|--------|------|------------|
| `/dna-init` | 프로젝트 초기화 | - |
| `/stage1` | 핵심 기능 분류 | stage1-classifier |
| `/stage2` | 환경 제약 설계 | stage2-architect |
| `/stage3` | ADR 작성 | stage3-adr-author |
| `/stage7` | 청사진 작성 | stage7-blueprint-writer |
| `/dna-audit` | 전체 검증 | 여러 Agent 순차 |
| `/multi-stage` | 병렬 실행 | 여러 Agent 동시 |

### Agents의 역할

| Agent | 전문성 | 산출물 |
|-------|--------|--------|
| stage1-classifier | 기능 분해 + 패밀리 분류 | 패밀리 코드, NFR 프로파일 |
| stage2-architect | Layer 3 제약 + 충돌 해결 | 제약 목록, 해결안 |
| stage3-adr-author | 결정 기록 | ADR 문서들 |
| stage7-blueprint-writer | 전체 설계 통합 | 청사진 문서 |
| stage8-task-breaker | 작업 분해 | 레고블럭 목록 |
| stage9-checklist-author | 실행 가이드 | 9-Step 체크리스트 |

---

## 6. 설계 원칙 요약

### Skills
- **지식은 Skills에**: 패턴, 템플릿, 참조 문서
- **Progressive Disclosure**: 필요할 때만 로드
- **재사용 가능**: 여러 Agent가 공유

### Commands
- **단순하게 유지**: 복잡한 로직 없음
- **명확한 목적**: 한 명령 = 한 목표
- **체이닝 지원**: 여러 Agent 조합 가능

### Agents
- **전문화**: 한 Agent = 한 전문 영역
- **품질 책임**: 검증 후 결과 반환
- **독립 실행**: 컨텍스트 의존 최소화

---

## 7. Gemini 연구와의 매핑

### 4-Phase 프로세스 매핑

| Gemini Phase | DNA Stage | 담당 Agent |
|--------------|-----------|------------|
| Phase 1: 아이디어 정제 | Stage 1-2 | classifier, architect |
| Phase 2: 스켈레톤 수립 | Stage 3-6 | adr-author, standards, planner |
| Phase 3: 병렬 확장 | Stage 7-8 | blueprint-writer, task-breaker |
| Phase 4: 정합성 검증 | Stage 9 | checklist-author |

### 기술 적용

| Gemini 기술 | 적용 위치 |
|-------------|-----------|
| CoD (Chain of Density) | Stage 1 - 요구사항 밀도 증가 |
| ToT (Tree of Thoughts) | Stage 2 - 아키텍처 대안 탐색 |
| SoT (Skeleton-of-Thought) | Stage 7 - 청사진 스켈레톤 |
| Context Re-ranking | 모든 Stage - 관련 정보만 로드 |
| Knowledge Graph | Stage 9 - 모순 탐지 |

---

## 요약

```
Skills  = 지식 (What to know)
Commands = 인터페이스 (How to start)
Agents  = 실행자 (Who does the work)
```

이 세 가지가 유기적으로 연결되어 DNA 방법론을 완전하게 실행합니다.

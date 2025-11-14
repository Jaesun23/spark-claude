# DNA v4.0 프로젝트 분해 체계 (Project Breakdown Structure)

> **버전**: v4.0 (2025-11-14)
> - v4.0 (2025-11-14): DNA v4.0 프로젝트 구조 정의
>
> **목적**: DNA Methodology v4.0의 전체 구조와 용어 체계를 명확히 정의

---

## 📋 목차
1. [DNA v4.0 분해 체계 개요](#dna-v40-분해-체계-개요)
2. [계층 구조 상세 정의](#계층-구조-상세-정의)
3. [문서 구조 체계](#문서-구조-체계)
4. [용어 정의 및 사용 원칙](#용어-정의-및-사용-원칙)
5. [실전 적용 예시](#실전-적용-예시)

---

## DNA v4.0 분해 체계 개요

### 핵심 원칙

DNA Development Methodology v4.0는 **"Idea → Blueprint → Implementation"** 전 과정을 체계적으로 분해합니다.

```
Project (프로젝트)
  └─ Stage (1-9)           ← DNA v4.0의 9단계 방법론
       └─ Part (0-N)       ← 각 Stage 내 논리적 구분
            └─ Layer (Part 1에만 존재) ← 3-Layer Decision Tree
                 └─ Question (Q1, L1-Q1, P2-Q1)
```

### DNA v3.6과의 비교

**DNA v3.6 구조** (Blueprint → Implementation):
```
Project → Stage → Phase → Task → Step → Action → Sub_Action
```

**DNA v4.0 구조** (Idea → Blueprint):
```
Project → Stage → Part → Layer (Part 1 only) → Question
```

**차이점**:
- v3.6: 청사진 이후의 "실행" 과정 (downward: 하향 분해)
- v4.0: 아이디어에서 청사진까지의 "설계" 과정 (upward: 상향 통합)

---

## 계층 구조 상세 정의

### Level 1: Project (프로젝트)

**정의**: 하나의 완전한 소프트웨어 시스템 개발 프로젝트

**예시**:
- "주식 자동 거래 플랫폼 개발"
- "AI 외부 메모리 시스템 구축"
- "실시간 협업 문서 편집기"

**특징**:
- 명확한 비즈니스 목적
- 독립적인 배포 단위
- 9개 Stage를 거쳐 완성

---

### Level 2: Stage (단계)

**정의**: DNA v4.0 방법론의 9개 핵심 단계

| Stage | 이름 | 목적 | 주요 산출물 |
|-------|------|------|-------------|
| **Stage 1** | 핵심 정의 (Core Definition) | 시스템 패밀리와 핵심 기능 파악 | 01F-01 (기능 정의), 01C-01 (패밀리 분류) |
| **Stage 2** | 환경 제약 (Environment Constraints) | 외부 제약 조사 및 충돌 해결 | 02C-01 (제약 조사), 02C-02 (충돌 분석) |
| **Stage 3** | 구조 결정 (Architecture Decision) | ADR 작성 및 기술 스택 결정 | 03A-001~999 (ADR 문서들) |
| **Stage 4** | 청사진 작성 (Blueprint) | 완전한 구현 설계서 작성 | 04B-01 (청사진) |
| **Stage 5** | 작업 분해 (Task Breakdown) | 청사진을 원자 단위 작업으로 분해 | 05T-01 (작업 목록) |
| **Stage 6** | 체크리스트 (Checklist) | 각 작업별 상세 실행 매뉴얼 | 06L-001~999 (체크리스트들) |
| **Stage 7** | 구현 (Implementation) | 체크리스트 기반 실제 코딩 | Source code |
| **Stage 8** | 검증 (Validation) | 테스트 및 품질 검증 | Test reports |
| **Stage 9** | 배포 (Deployment) | 프로덕션 배포 및 모니터링 | Deployment logs |

**특징**:
- 순차적 진행 (Stage 1 → 9)
- 각 Stage는 독립적 검증 가능
- 이전 Stage 완료가 다음 Stage의 입력

---

### Level 3: Part (파트)

**정의**: 각 Stage 내에서 논리적으로 구분되는 작업 단위

**명명 규칙**:
- **Part 0**: 준비 단계 또는 개념 설명 (선택적)
- **Part 1, 2, ...**: 주요 작업 단계 (순차적)

**Stage 1 예시**:
```
Stage 1: 핵심 정의
  ├─ Part 0: 핵심 기능 파악
  ├─ Part 1: 시스템의 패밀리 유형 파악
  └─ Part 2: NFR(비기능 요구사항) 우선순위 파악
```

**Stage 2 예시**:
```
Stage 2: 환경 제약
  ├─ Part 1: Layer 3 (외부 제약) 조사
  ├─ Part 2: 충돌 패턴 식별
  └─ Part 3: 구현 방법 결정 (5단계)
```

**특징**:
- Stage마다 Part 개수는 다름 (2-4개 일반적)
- Part 0는 선택적 (준비/개념 설명)
- Part는 순차적 의존성 가질 수 있음

---

### Level 4: Layer (레이어) - **Part 1에만 존재**

**정의**: Stage 1 Part 1에서 사용하는 **3-Layer Decision Tree**의 계층

**⚠️ 중요**: Layer는 **Stage 1 Part 1**에서만 사용되는 특수한 개념입니다!

**3-Layer Decision Tree**:
```
Part 1: 시스템의 패밀리 유형 파악
  ├─ Layer 1: 실패 영향 (Failure Impact)
  │    ├─ Question: 핵심 기능 실패시 금전적 손실이 발생하나요?
  │    └─ Answer: A (발생) / B (미발생)
  │
  ├─ Layer 2: 데이터 구조 (Data Structure)
  │    ├─ Question: 데이터 구조가 미리 정해져 있나요?
  │    └─ Answer: A (정형) / B (비정형) / C (스트림)
  │
  └─ Layer 3: 응답 시간 (Response Time)
       ├─ Question: 실시간 응답이 필요한가요?
       └─ Answer: A (100ms 이하) / B (1초 이하) / C (1초 이상)
```

**결과**: Layer 1-2-3 답변 조합 → 7개 패밀리 중 하나 (예: A-A-B, B-B-B)

**특징**:
- **오직 Stage 1 Part 1에서만** 사용
- 3개 Layer 고정 (Layer 1, 2, 3)
- 각 Layer는 특정 질문과 답변 선택지 보유
- 답변 조합이 패밀리 코드 (A-A-B)

---

### Level 5: Question (질문)

**정의**: 각 Part (또는 Layer) 내에서 답변해야 할 구체적 질문

**명명 규칙**:
```
Part-Qn         ← Part 내 일반 질문 (예: P0-Q1, P2-Q1)
Layer-Qn        ← Part 1 내 Layer별 질문 (예: L1-Q1, L2-Q1, L3-Q1)
```

**예시**:

**Part 0 (일반 질문)**:
```
P0-Q1: 이 시스템의 가장 핵심적인 기능은 무엇인가요?
P0-Q2: 그 기능을 통해 이루려는 목적은 무엇인가요?
```

**Part 1 (Layer 질문)**:
```
L1-Q1: 핵심 기능 실패시 금전적 손실이 발생하나요?
L2-Q1: 데이터 구조가 미리 정해져 있나요?
L3-Q1: 실시간 응답이 필요한가요?
```

**Part 2 (일반 질문)**:
```
P2-Q1: 성능(Performance)은 얼마나 중요한가요?
P2-Q2: 확장성(Scalability)은 얼마나 중요한가요?
```

**특징**:
- 명확한 답변 가능한 구체적 질문
- 선택지 또는 서술형 답변
- 질문 순서가 의존성 반영

---

## 문서 구조 체계

### 3-Tier 문서 구조

DNA v4.0는 각 Stage마다 3가지 유형의 문서를 제공합니다:

```
Guide (가이드)
  ↓ 더 자세히 알고 싶다면
Manual (해설서)
  ↓ 실전 사례를 보고 싶다면
Cases (사례집)
```

---

### 1. Guide (가이드) - 실행용 템플릿

**목적**: 직접 작성할 수 있도록 질문과 작성 원칙 제공

**구조**:
```markdown
# StageN. [제목] 가이드

> **버전 정보**

## 📚 이 가이드의 구성
- **이 문서** (Guide): 질문 템플릿 + 작성 원칙
- **해설서** (Manual): 상세 설명 → `파일경로`
- **사례집** (Cases): 실전 예시 → `파일경로`

## Part 0: [제목]
[간단한 개념 설명 1-2 문단]

### P0-Q1: [질문]
- **작성 가이드**: [간단한 작성 팁]

### P0-Q2: [질문]
...

## Part 1: [제목]
[Part 1 소개 및 왜 중요한지 1-2 문단]

### L1-Q1: [질문]
...
```

**특징**:
- **분량**: 1000-1500줄 (컨텍스트 윈도우 고려)
- **톤**: 실행 지향적, 간결하면서도 이해 가능한 수준
- **내용**: 질문 + 작성 가이드 + 간단한 예시
- **참조**: Manual/Cases로 링크 (파일 경로 포함)

**원칙**:
> "간결하되 이해 가능해야 한다. 단어 나열이 아닌 맥락 있는 설명."
> - Jason, 2025-11-14

---

### 2. Manual (해설서) - 심화 학습용

**목적**: "왜?"와 "어떻게?"에 대한 상세 설명

**구조**:
```markdown
# StageN Manual: [제목]

## 1. [Part/Layer 이름]

### 1.1 개념 설명
[왜 이 Part/Layer가 필요한가?]

### 1.2 상세 설명
[어떻게 작동하는가?]

### 1.3 주의사항
[흔한 실수와 해결법]

## 2. [다음 Part/Layer]
...
```

**특징**:
- **분량**: 제한 없음 (필요한 만큼)
- **톤**: 교육적, 상세한 설명
- **내용**: 개념, 원리, 이론적 배경, 주의사항
- **참조**: Guide에서 링크로 연결

---

### 3. Cases (사례집) - 실전 학습용

**목적**: 전체 흐름을 실제 프로젝트로 보여주기

**구조**:
```markdown
# StageN Case: [프로젝트명]

## 프로젝트 개요
[어떤 시스템인가?]

## Part 0: [제목]
### P0-Q1: [질문]
**답변**: [실제 답변]

### P0-Q2: [질문]
**답변**: [실제 답변]

## Part 1: [제목]
...

## 최종 결과
[이 Stage를 거쳐 나온 산출물]
```

**특징**:
- **분량**: 제한 없음 (완전한 사례)
- **톤**: 실전적, 구체적
- **내용**: 실제 프로젝트의 모든 답변과 결과
- **참조**: Guide에서 링크로 연결

---

### 문서 명명 규칙

```
{Stage}{Type}-{Seq}_{descriptive_name}.md

Stage: 01-09
Type:
  G = Guide (가이드)
  M = Manual (해설서)
  E = Example/Case (사례집)
  F = Function (기능 정의)
  C = Classification (분류/분석)
  D = Decision (결정 사항)
  A = ADR (Architecture Decision Record)
  B = Blueprint (청사진)
  T = Task (작업 분해)
  L = List/Checklist (체크리스트)
Seq: 00-99 (일반), 001-999 (다수 파일)
```

**예시**:
```
01G-00_core_definition_guide.md        ← Stage 1 Guide
01M-01_layer1_manual.md                ← Stage 1 Manual (Layer 1)
01E-01_stock_trading_case.md           ← Stage 1 Case (주식 거래)
02G-00_environment_constraints_guide.md ← Stage 2 Guide
03A-001_logging_standards.md           ← Stage 3 ADR #1
```

---

## 용어 정의 및 사용 원칙

### 핵심 용어 정리

| 용어 | 영문 | 정의 | 사용 범위 |
|------|------|------|-----------|
| **프로젝트** | Project | 하나의 완전한 시스템 개발 | 전체 |
| **Stage** | Stage | DNA v4.0의 9개 핵심 단계 | 전체 |
| **Part** | Part | Stage 내 논리적 작업 구분 | Stage 1-9 |
| **Layer** | Layer | 3-Layer Decision Tree의 계층 | **Stage 1 Part 1만** |
| **Question** | Question | 답변할 구체적 질문 | Part/Layer 내 |
| **패밀리** | Family | 7가지 아키텍처 유형 분류 | Stage 1 결과 |
| **핵심 기능** | Core Function | 시스템의 가장 근원적 기능 | Stage 1 Part 0 |
| **NFR** | Non-Functional Requirement | 비기능 요구사항 | Stage 1 Part 2 |

---

### 혼동하기 쉬운 용어

#### ❌ "공통 기능" (Common Function) vs ✅ "핵심 기능" (Core Function)

**잘못된 사용**:
```
"이 시스템의 공통 기능은 주식 거래입니다."
```

**올바른 사용**:
```
"이 시스템의 핵심 기능은 주식 거래입니다."
```

**이유**: "공통"은 여러 시스템이 공유하는 기능을 의미. DNA v4.0에서는 각 프로젝트의 "가장 중요한 근원적 기능"을 의미하므로 "핵심 기능" 사용.

---

#### ⚠️ "Layer"는 Stage 1 Part 1에서만!

**잘못된 사용**:
```
"Stage 2 Layer 1: 외부 제약 조사"
```

**올바른 사용**:
```
"Stage 2 Part 1: Layer 3 (외부 제약) 조사"
```

**이유**:
- "Layer"는 **3-Layer Decision Tree**의 계층을 의미 (Layer 1, 2, 3)
- Stage 2에서 "Layer 3"를 언급할 때는 "Part 1"이라는 구조 내에서 "Layer 3 제약"을 조사하는 것
- Stage 구조는 항상 "Stage → Part → Question"

---

#### 📍 "Part 1"과 "Layer" 구분

**Stage 1의 구조**:
```
Stage 1: 핵심 정의
  ├─ Part 0: 핵심 기능 파악
  ├─ Part 1: 시스템의 패밀리 유형 파악  ← Part 구조
  │    ├─ Layer 1: 실패 영향            ← Part 1 내부의 Layer
  │    ├─ Layer 2: 데이터 구조
  │    └─ Layer 3: 응답 시간
  └─ Part 2: NFR 우선순위 파악
```

**올바른 표현**:
- "Stage 1 Part 1에서 3-Layer Decision Tree를 사용합니다."
- "Part 1은 Layer 1, 2, 3으로 구성됩니다."
- "Layer 1-2-3의 답변 조합이 패밀리를 결정합니다."

**잘못된 표현**:
- ❌ "Stage 1 Layer 1" (Part가 빠짐)
- ❌ "Stage 2 Layer 3" (Stage 2에는 Layer 없음)

---

### 참조 표기 원칙

**Manual/Cases 참조시 클릭 가능한 링크 + 파일 경로 병기 필수**:

**❌ 잘못된 예시**:
```markdown
자세한 내용은 Manual 1.2절 참고
```

**✅ 올바른 예시**:
```markdown
> 📖 **더 알아보기**: [Manual 1.2절: Layer 1 상세 설명](./01M-01_layer1_manual.md#layer-1-상세-설명)(`01M-01_layer1_manual.md:45-78`)
```

**표준 형식**:
```markdown
> 📖 **더 알아보기**: [문서유형 섹션: 설명](./파일명.md#섹션-앵커)(`파일명:시작줄-종료줄`)
```

**렌더링 결과**:
- 사람(Jason): "Manual 1.2절: Layer 1 상세 설명" 클릭 → 해당 섹션으로 이동
- AI(2호/에이전트): `파일명:45-78` 보고 → `Read(file_path, offset=45, limit=33)` 실행

**이유**:
- ✅ 사람: 클릭 한 번으로 원하는 섹션 확인 가능
- ✅ AI: 정확한 파일과 라인 번호로 즉시 읽기 가능
- ✅ 두 목적을 한 줄로 동시 충족

---

## 실전 적용 예시

### 예시 1: Stage 1 Part 1 Layer 1 질문

**문서**: `01G-00_core_definition_guide.md`

**경로**: Stage 1 → Part 1 → Layer 1 → Question

**내용**:
```markdown
## Part 1: 시스템의 패밀리 유형 파악

### Layer 1: 실패 영향 (Failure Impact)

#### L1-Q1: 핵심 기능 실패시 금전적 손실이 발생하나요?

**질문 의도**: 시스템의 비즈니스 임계성(criticality)을 판단합니다.

**답변 가이드**:
- **A (발생)**: 기능 실패 → 즉각적 금전 손실
  - 예: 주식 거래 실패 → 매매 기회 상실 → 손실
  - 예: 결제 처리 실패 → 매출 손실

- **B (미발생)**: 기능 실패 → 불편함이나 품질 저하
  - 예: 검색 실패 → 사용자 불만
  - 예: 문서 편집 실패 → 재시도 필요

**작성 예시**:
```
답변: A (발생)
이유: 주식 거래 시스템에서 매수/매도 실패시 시장 기회를 놓쳐
      직접적인 금전적 손실이 발생합니다.
```

> 📖 **더 알아보기**: [Manual 1.2절: Layer 1 상세 분석](./01M-01_layer1_manual.md#12-layer-1-상세-분석)(`01M-01_layer1_manual.md:45-120`)
```

**계층 구조**:
```
01G-00_core_definition_guide.md
  ├─ Stage 1 (핵심 정의)
  │    ├─ Part 0 (핵심 기능 파악)
  │    ├─ Part 1 (패밀리 유형 파악) ← 현재 위치
  │    │    └─ Layer 1 (실패 영향)
  │    │         └─ L1-Q1 ← 이 질문
  │    └─ Part 2 (NFR 우선순위)
```

---

### 예시 2: Stage 2 Part 1 질문

**문서**: `02G-00_environment_constraints_guide.md`

**경로**: Stage 2 → Part 1 → Question

**내용**:
```markdown
## Part 1: Layer 3 (외부 제약) 조사

> Stage 1에서 결정된 패밀리의 **Layer 3 (응답 시간)** 요구사항을
> 만족시킬 수 있는 **외부 환경**(API, 클라우드, 규제 등)을 조사합니다.

### P1-Q1: Layer 3 제약을 만족하는 외부 서비스/API는 무엇이 있나요?

**질문 의도**: Stage 1에서 결정된 응답 시간 요구사항(A/B/C)을
만족하는 실제 사용 가능한 외부 서비스를 찾습니다.

**작성 가이드**:
1. Stage 1 결과 확인: "우리 시스템은 Layer 3가 A/B/C인가?"
2. 해당 응답 시간을 제공하는 서비스 조사
3. 비교표 작성 (성능, 가격, SLA 등)

**작성 예시** (Layer 3: B - 1초 이하인 경우):
```
| 서비스명 | 평균 응답 시간 | SLA | 월 비용 | 비고 |
|----------|----------------|-----|---------|------|
| 한국투자증권 API | 200-400ms | 99.9% | 무료 | REST API |
| 키움증권 API | 300-600ms | 99.5% | 무료 | ActiveX 의존 |
```

> 📖 **더 알아보기**: [Manual 2.1절: Layer 3 제약 상세 조사](./02M-01_layer3_constraints_manual.md#21-layer-3-제약-상세-조사)(`02M-01_layer3_constraints_manual.md:80-150`)
```

**계층 구조**:
```
02G-00_environment_constraints_guide.md
  ├─ Stage 2 (환경 제약)
  │    ├─ Part 1 (Layer 3 조사) ← 현재 위치
  │    │    └─ P1-Q1 ← 이 질문
  │    ├─ Part 2 (충돌 패턴 식별)
  │    └─ Part 3 (구현 방법 결정)
```

**주의**: Stage 2에는 "Layer"라는 구조가 없습니다. "Layer 3"는 Stage 1 Part 1의 결과를 참조하는 것입니다.

---

### 예시 3: 패밀리 결정 흐름

**Stage 1 Part 1 전체 흐름**:

```
사용자 입력: "주식 자동 거래 시스템"

Part 1: 시스템의 패밀리 유형 파악
  │
  ├─ Layer 1: 실패 영향
  │    L1-Q1: 금전적 손실 발생?
  │    답변: A (발생) ← 거래 실패 = 손실
  │
  ├─ Layer 2: 데이터 구조
  │    L2-Q1: 데이터 구조 정형성?
  │    답변: A (정형) ← 주식 데이터는 정형
  │
  └─ Layer 3: 응답 시간
       L3-Q1: 실시간 응답 필요?
       답변: B (1초 이하) ← 자동 거래는 1초 이하면 충분

결과: A-A-B 패밀리 (트랜잭션/CRUD 시스템)

다음 Stage로 전달:
  - 패밀리: A-A-B
  - 핵심 기능: 주식 거래
  - 목적: 수익 창출
```

**산출물**:
```
01F-01_core_functions.md         ← Part 0 결과
01C-01_family_classification.md  ← Part 1 결과 (A-A-B)
01C-02_nfr_priorities.md         ← Part 2 결과
```

---

## 부록: Quick Reference

### Stage별 주요 산출물

```
Stage 1: 01F-01 (기능), 01C-01 (패밀리), 01C-02 (NFR)
Stage 2: 02C-01 (제약), 02C-02 (충돌), 02D-01 (구현방법)
Stage 3: 03A-001~999 (ADR들)
Stage 4: 04B-01 (청사진)
Stage 5: 05T-01 (작업 목록)
Stage 6: 06L-001~999 (체크리스트들)
Stage 7-9: 코드, 테스트, 배포
```

### 용어 체크리스트

작성시 다음 사항을 확인하세요:

- [ ] "공통 기능" 대신 "핵심 기능" 사용
- [ ] "Layer"는 Stage 1 Part 1에서만 사용
- [ ] Stage 2 이후에서 "Layer 3"는 "Part X: Layer 3 제약 조사" 형태로
- [ ] Manual/Cases 참조시 파일 경로 포함 (`파일명:줄번호`)
- [ ] Question 명명은 Pn-Qm 또는 Ln-Qm 형식
- [ ] Part는 Part 0, 1, 2, ... 순서로 (Part 0는 선택적)

---

## 변경 이력

- **v4.0 (2025-11-14)**: 초안 작성 (Jason 피드백 반영)
  - DNA v4.0 분해 체계 정의
  - 3-Tier 문서 구조 (Guide/Manual/Cases) 정의
  - 용어 체계 및 사용 원칙 정리
  - Layer는 Stage 1 Part 1에만 존재함을 명확히

---

**문서 끝**

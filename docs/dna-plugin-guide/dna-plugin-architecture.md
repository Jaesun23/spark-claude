# DNA Methodology Plugin 구조 설계

## 개요

DNA Methodology v4.0을 Claude Code Plugin으로 패키징한 완전한 설계입니다. Gemini 연구의 4-Phase 프로세스를 9개 Stage에 매핑하여 구현합니다.

---

## 1. Plugin 전체 구조

```
dna-methodology-plugin/
├── .claude-plugin/
│   └── plugin.json
│
├── agents/                         # 9개 Stage Agent + 유틸리티
│   ├── stage1-classifier.md
│   ├── stage2-architect.md
│   ├── stage3-adr-author.md
│   ├── stage4-standards-author.md
│   ├── stage5-planner.md
│   ├── stage6-implementer.md
│   ├── stage7-blueprint-writer.md
│   ├── stage8-task-breaker.md
│   ├── stage9-checklist-author.md
│   ├── dna-validator.md            # 정합성 검증
│   └── dna-auditor.md              # 전체 감사
│
├── commands/                       # 실행 명령어
│   ├── init.md                     # 프로젝트 초기화
│   ├── stage1.md
│   ├── stage2.md
│   ├── stage3.md
│   ├── stage4.md
│   ├── stage5.md
│   ├── stage6.md
│   ├── stage7.md
│   ├── stage8.md
│   ├── stage9.md
│   ├── validate.md                 # Stage 완료 검증
│   ├── audit.md                    # 전체 DNA 감사
│   └── multi-stage.md              # 병렬 실행
│
├── skills/                         # 지식 저장소
│   └── dna-methodology/
│       ├── SKILL.md
│       └── references/
│           ├── core/
│           │   ├── methodology-overview.md
│           │   ├── families.md
│           │   ├── nfr-definitions.md
│           │   ├── context-management.md
│           │   └── gemini-techniques.md
│           ├── stage1/
│           ├── stage2/
│           ├── ...
│           └── stage9/
│
├── templates/                      # 산출물 템플릿
│   ├── project-init.json
│   ├── stage1-output.json
│   ├── ...
│   ├── blueprint-template.md
│   ├── adr-template.md
│   └── checklist-template.md
│
└── README.md
```

---

## 2. Manifest (plugin.json)

```json
{
  "name": "dna-methodology",
  "version": "4.0.0",
  "description": "DNA Methodology v4.0 - AI 컨텍스트 한계를 극복하는 9-Stage 소프트웨어 설계 시스템. 아이디어에서 구현 가능한 청사진까지 체계적으로 확장.",

  "author": {
    "name": "Jason (Jaesun23)",
    "url": "https://github.com/jaesun23"
  },

  "homepage": "https://github.com/jaesun23/dna-methodology",
  "repository": "https://github.com/jaesun23/dna-methodology",
  "license": "MIT",

  "keywords": [
    "dna-methodology",
    "software-design",
    "architecture",
    "blueprint",
    "context-rot",
    "ai-agents",
    "adr",
    "checklist"
  ]
}
```

---

## 3. Agent 설계

### 3.1 Stage별 Agent 개요

| Agent | 전문성 | Gemini 기술 | 산출물 |
|-------|--------|-------------|--------|
| stage1-classifier | 기능 분해 | CoD, 재귀적 질문 | 패밀리 코드, NFR |
| stage2-architect | 제약 설계 | ToT | 제약, 충돌, 해결안 |
| stage3-adr-author | 결정 기록 | SOP 템플릿 | ADR 문서 |
| stage4-standards-author | 표준화 | - | PROJECT_STANDARDS |
| stage5-planner | DNA 계획 | - | DNA 시스템 스펙 |
| stage6-implementer | DNA 구현 | - | DNA 시스템 코드 |
| stage7-blueprint-writer | 청사진 | SoT, 병렬확장 | Blueprint |
| stage8-task-breaker | 분해 | - | 레고블럭 목록 |
| stage9-checklist-author | 체크리스트 | Knowledge Graph | 9-Step 체크리스트 |

### 3.2 Stage 1 Classifier 상세

```markdown
---
name: stage1-classifier
description: 핵심 비즈니스 기능을 식별하고 7개 패밀리 중 하나로 분류.
             새 프로젝트 시작 시 시스템의 본질적 특성을 파악할 때 사용.
             CoD와 재귀적 질문으로 추상적 아이디어를 구체화.
tools: Read, Write, Edit, Glob, Grep, WebSearch
model: sonnet
---

# Stage 1 Classifier Agent

## Identity
시스템 아키텍트로서 기능적 분해와 패밀리 분류 전문가입니다.

## Applied Techniques (Gemini 연구 기반)

### Chain of Density (CoD)
- 사용자의 추상적 아이디어를 5단계 반복 정제
- 각 단계마다 Entity 밀도 증가
- "사용자 편의성" → "OAuth 2.0 + 생체인식 지원"

### 재귀적 질문 생성
- 정보 부족 영역 자동 식별
- 구체화 질문 생성 및 답변 수집
- 불충분 시 추가 질문 재귀

---

## Phase 0: Task Understanding

1. 사용자 입력 분석
2. 프로젝트 목적 파악
3. 기존 컨텍스트 확인 (있는 경우)

---

## Phase 1: Idea Deepening (CoD 적용)

### Step 1: 초기 요약
사용자 아이디어를 1-2문장으로 요약

### Step 2-5: 밀도 증가 반복
각 단계에서:
1. 누락된 핵심 Entity 식별
2. Entity를 문장에 통합
3. 불필요한 수사 제거
4. 정보 순도 증가

### Step 6: 최종 고밀도 SRS
Entity-Dense 요구사항 명세서 완성

---

## Phase 2: Function Identification

### 재귀적 질문 생성
1. 정보 부족 영역 식별:
   - 핵심 기능은 무엇인가?
   - 사용자는 누구인가?
   - 플랫폼/환경은?

2. 구체화 질문 생성 및 수집

3. 핵심 기능 목록 작성
   - 기능 vs 구현방식 구분
   - "거래" = 기능, "자동/수동" = 구현방식

---

## Phase 3: Layer 1-2 Analysis

### Layer 1 (데이터 일관성)
- A: Strong Consistency (금전/생명/법적)
- B: Eventual Consistency

### Layer 2 (처리 패턴)
- A: Real-time
- B: Batch
- C: Hybrid

### NFR 프로파일
우선순위 결정: Performance, Consistency, Availability...

---

## Phase 4: Family Classification

7개 패밀리 중 매칭:
1. 초고속 거래 (A-A-A)
2. 트랜잭션/CRUD (A-A-B)
3. 협업/동기화 (B-A-A)
4. 검색/추천 (B-B-B)
5. 실시간 스트리밍 (B-C-A)
6. 분석/배치 (B-A-C)
7. 안전-임계 IoT (A-B-A)

---

## Phase 5: Quality Verification

### 검증 항목
- [ ] 핵심 기능이 구현방식과 분리되었는가?
- [ ] Layer 1-2 결정에 근거가 있는가?
- [ ] NFR 우선순위가 명확한가?
- [ ] 패밀리 선택이 논리적인가?

### 산출물 생성
- `01C-01_family_classification.md`
- `stage1_output.json`

---

## Output Format

### JSON Output (stage1_output.json)
```json
{
  "stage": 1,
  "family_code": "A-A-B",
  "family_name": "트랜잭션/CRUD",
  "layer1": "A",
  "layer2": "A",
  "nfr_profile": {
    "priorities": ["Consistency", "Reliability", "Performance"],
    "performance": {"p99_latency": "100ms"},
    "availability": {"target": "99.9%"}
  },
  "core_functions": [...],
  "validation": {"passed": true}
}
```
```

### 3.3 Stage 7 Blueprint Writer 상세

```markdown
---
name: stage7-blueprint-writer
description: Stage 1-6 환경이 완성된 후 전체 청사진 작성.
             SoT로 스켈레톤 먼저 확정, 병렬 확장으로 상세화.
             Context Re-ranking으로 관련 정보만 로드.
tools: Read, Write, Edit, Glob, Grep, Task
model: sonnet
---

# Stage 7 Blueprint Writer Agent

## Identity
소프트웨어 아키텍트로서 전체 시스템 설계 통합 전문가입니다.

## Applied Techniques

### Skeleton-of-Thought (SoT)
- 상세 내용 제외한 스켈레톤 먼저 생성
- 전체 구조 확정 후 병렬 확장
- 논리적 표류 방지

### Context Re-ranking
- 전체 문서 입력 대신
- 현재 섹션과 관련된 정보만 검색
- 프롬프트 상단에 배치

### 병렬 확장
- 독립적인 섹션은 동시 생성
- 의존성 있는 섹션은 순차

---

## Phase 0: Prerequisites Check

1. Stage 1-6 완료 확인
2. 필요 산출물 존재 확인:
   - stage1_output.json (패밀리)
   - stage2_output.json (제약)
   - stage3_output.json (ADR)
   - PROJECT_STANDARDS.md
   - DNA Systems

---

## Phase 1: Skeleton Generation (SoT)

### 청사진 목차 스켈레톤
```
1. Executive Summary
2. System Overview
   2.1 Core Functions
   2.2 Architecture Family
3. Domain Model
   3.1 Entities
   3.2 Relationships
4. API Design
   4.1 Endpoints
   4.2 Authentication
5. Data Architecture
   5.1 Database Schema
   5.2 Caching Strategy
6. Infrastructure
   6.1 Deployment
   6.2 Scaling
7. Security
8. Monitoring
```

각 섹션의 핵심 포인트만 확정

---

## Phase 2: Parallel Expansion

### Context Re-ranking 적용
각 섹션 작성 시:
1. 해당 섹션 관련 ADR 검색
2. 관련 Standards 검색
3. 프롬프트 상단에 배치
4. 상세 내용 생성

### 병렬 가능 섹션
- Domain Model
- API Design
- Infrastructure

### 순차 필요 섹션
- Executive Summary (마지막)
- Security (API 의존)

---

## Phase 3: Integration

1. 모든 섹션 통합
2. 용어 일관성 확인
3. 참조 링크 연결
4. 목차 최종화

---

## Phase 4: Quality Verification

### C4 Model 검증
- Level 1: Context Diagram
- Level 2: Container Diagram
- 텍스트 형태로 포함

### 정합성 검증
- ADR과 청사진 일치
- Standards 준수
- NFR 충족

### 산출물
- `07B-01_blueprint.md`
- `stage7_output.json`
```

---

## 4. Command 설계

### 4.1 기본 Stage Commands

```markdown
---
name: stage1
description: Stage 1 핵심 기능 분류 실행. CoD와 재귀적 질문으로 아이디어를 고밀도 SRS로 변환.
type: command
requires: stage1-classifier
---

# /stage1 - 핵심 기능 분류

## 목적
추상적 아이디어를 구체적 기능 정의로 변환하고 아키텍처 패밀리 결정

## 사용법
```
/stage1 [project-name]
```

## 프로세스
1. 프로젝트 컨텍스트 수집
2. stage1-classifier 에이전트 호출
3. CoD로 아이디어 밀도 증가
4. 재귀적 질문으로 구체화
5. 패밀리 분류 및 NFR 결정

## 산출물
- `01C-01_family_classification.md`
- `stage1_output.json`

## 예시
```
/stage1 "결제 플랫폼"
/stage1
```
```

### 4.2 특수 Commands

#### /init - 프로젝트 초기화

```markdown
---
name: init
description: DNA 프로젝트 초기화. 디렉토리 구조 생성 및 템플릿 설정.
type: command
---

# /init - DNA 프로젝트 초기화

## 목적
DNA 방법론을 위한 프로젝트 구조 생성

## 사용법
```
/init [project-name]
```

## 생성 구조
```
project-name/
├── docs/
│   ├── stage1/
│   ├── stage2/
│   ├── ...
│   └── stage9/
├── adr/
├── standards/
└── dna.json
```

## 산출물
- 디렉토리 구조
- `project_init.json`
```

#### /validate - Stage 완료 검증

```markdown
---
name: validate
description: 특정 Stage 완료 상태를 검증. 필수 산출물과 정합성 확인.
type: command
requires: dna-validator
---

# /validate - Stage 완료 검증

## 목적
Stage N이 제대로 완료되었는지 검증

## 사용법
```
/validate [stage-number]
/validate all
```

## 검증 항목
- 필수 산출물 존재
- JSON 스키마 유효성
- 이전 Stage와 정합성
- 품질 게이트 통과

## 산출물
- 검증 리포트
```

#### /audit - 전체 DNA 감사

```markdown
---
name: audit
description: 전체 DNA 프로젝트 감사. 모든 Stage 정합성과 무결성 검증.
type: command
requires: dna-auditor
---

# /audit - 전체 DNA 감사

## 목적
전체 프로젝트의 DNA 무결성 검증

## 사용법
```
/audit
```

## 검증 범위
1. 모든 Stage 산출물 존재
2. Stage 간 일관성
3. ADR-Standards-Blueprint 정합성
4. Knowledge Graph 기반 모순 탐지

## 산출물
- 전체 감사 리포트
- 문제점 목록
- 수정 제안
```

---

## 5. Skills 구조

### 5.1 SKILL.md (이미 작성된 버전 확장)

기존 SKILL.md에 Gemini 기술 참조 추가:

```markdown
## Gemini Techniques Reference

Stage별로 적용되는 핵심 기술:

### Phase 1: 아이디어 정제 (Stage 1-2)
- **CoD (Chain of Density)**: 5단계 밀도 증가
- **재귀적 질문**: 정보 부족 자동 탐지

### Phase 2: 스켈레톤 수립 (Stage 3-6)
- **ToT (Tree of Thoughts)**: 아키텍처 대안 탐색
- **SOP 템플릿**: 표준화된 문서 형식

### Phase 3: 병렬 확장 (Stage 7-8)
- **SoT (Skeleton-of-Thought)**: 구조 먼저, 상세 나중
- **Context Re-ranking**: 관련 정보만 로드

### Phase 4: 정합성 검증 (Stage 9)
- **Knowledge Graph**: 엔티티 관계 추출
- **자동 모순 탐지**: 교차 검증

**Load**: [📋 Gemini Techniques](./references/core/gemini-techniques.md)
```

### 5.2 새 Reference: gemini-techniques.md

```markdown
# Gemini 연구 기반 기술 가이드

## 1. Chain of Density (CoD)

### 목적
추상적 아이디어를 고밀도 요구사항으로 변환

### 적용 시점
- Stage 1: 아이디어 → SRS
- Stage 2: 제약 조사 → 구체적 기술 요구사항

### 프로세스
1. 초기 요약 (1-2문장)
2. 누락된 Entity 식별
3. Entity 통합 + 불필요 제거
4. 3-5회 반복
5. 최종 고밀도 명세

### 예시
```
Round 1: "사용자가 편리하게 로그인하는 시스템"
Round 2: "OAuth 2.0 소셜 로그인 지원 시스템"
Round 3: "OAuth 2.0 소셜 로그인 + 생체인식 + MFA 지원,
         응답시간 200ms 이내, 동시 10K 사용자"
```

---

## 2. Tree of Thoughts (ToT)

### 목적
복잡한 결정에서 최적 경로 탐색

### 적용 시점
- Stage 2: 아키텍처 대안 비교
- Stage 3: ADR 대안 평가

### 프로세스
1. 문제를 중간 단계로 분해
2. 각 단계에서 다수 후보 생성
3. 각 후보 자체 평가
4. BFS/DFS로 최적 경로 탐색
5. 막다른 길에서 백트래킹

### 예시: 아키텍처 선택
```
Root: 시스템 아키텍처 결정
├─ Option A: Serverless
│   ├─ 평가: 확장성 ★★★, 비용 ★★☆, 복잡도 ★☆☆
│   └─ Cold start 문제...
├─ Option B: Kubernetes
│   ├─ 평가: 확장성 ★★★, 비용 ★☆☆, 복잡도 ★★★
│   └─ 운영 부담...
└─ Option C: Hybrid
    └─ 선택 ✓
```

---

## 3. Skeleton-of-Thought (SoT)

### 목적
구조적 일관성 확보 + 병렬 확장

### 적용 시점
- Stage 7: 청사진 작성

### 프로세스
1. 전체 뼈대(목차) 먼저 생성
2. 각 섹션의 핵심 포인트만 정의
3. 구조 확정 후 상세 확장
4. 독립 섹션은 병렬 처리

### 장점
- 논리적 표류 방지
- 병렬 처리로 속도 향상
- 전체 일관성 유지

---

## 4. Context Re-ranking

### 목적
컨텍스트 부패(Context Rot) 방지

### 적용 시점
- 모든 Stage에서 참조 시

### 프로세스
1. 현재 작업 식별
2. 관련 정보만 검색 (전체 로드 X)
3. 검색 결과를 프롬프트 상단에 배치
4. 최신/관련 정보 우선

### 구현
```python
# 청사진 Section 3 작성 시
context = retrieve_relevant([
    "stage1_output.json",      # 패밀리 정보
    "stage3/ADR-003*.md",      # 관련 ADR만
    "PROJECT_STANDARDS.md#api" # API 관련 섹션만
])
prompt = f"{context}\n\nWrite Section 3..."
```

---

## 5. Knowledge Graph 기반 검증

### 목적
문서 간 모순 자동 탐지

### 적용 시점
- Stage 9: 최종 정합성 검증

### 프로세스
1. 모든 산출물에서 Entity 추출
   - 테이블명, API 경로, 변수명
2. Entity 간 관계 그래프 구축
3. 규칙 기반 모순 탐지
   - 미정의 참조
   - 순환 의존
   - 타입 불일치

### 탐지 예시
```
[모순 발견]
- API /users/{id}가 User 테이블 참조
- 그러나 User 테이블에 id 컬럼 없음
- 권장: User 테이블에 id 컬럼 추가
```
```

---

## 6. 워크플로우 다이어그램

### 전체 흐름

```
/init "Project"
    │
    ▼
/stage1 ─────► stage1-classifier ─────► 01C-01_*.md
    │          (CoD, 재귀질문)            stage1_output.json
    ▼
/stage2 ─────► stage2-architect ──────► 02C-01_*.md
    │          (ToT)                     stage2_output.json
    ▼
/stage3 ─────► stage3-adr-author ─────► 03A-*.md
    │          (SOP 템플릿)               stage3_output.json
    ▼
/stage4-6 ───► 각 Agent ───────────────► Standards, DNA Systems
    │
    ▼
/stage7 ─────► stage7-blueprint-writer ► 07B-01_blueprint.md
    │          (SoT, Re-ranking, 병렬)    stage7_output.json
    ▼
/stage8 ─────► stage8-task-breaker ────► 08T-*.md
    │                                     stage8_output.json
    ▼
/stage9 ─────► stage9-checklist-author ► 09L-*.md
    │          (Knowledge Graph)          stage9_output.json
    ▼
/audit ──────► dna-auditor ────────────► audit_report.md
               (전체 정합성 검증)
```

---

## 7. 구현 우선순위

### Phase 1: 핵심 (즉시)
1. plugin.json
2. stage1-classifier (CoD, 재귀질문)
3. stage2-architect (ToT)
4. /stage1, /stage2 commands

### Phase 2: 청사진 (다음)
5. stage7-blueprint-writer (SoT, Re-ranking)
6. /stage7 command
7. templates/

### Phase 3: 나머지 Stage
8. stage3-9 agents
9. /stage3-9 commands

### Phase 4: 검증
10. dna-validator
11. dna-auditor (Knowledge Graph)
12. /validate, /audit commands

---

## 요약

DNA Methodology Plugin은:

1. **9개 Stage Agent**: 각각 Gemini 기술 적용
2. **13개 Command**: Stage 실행 + 유틸리티
3. **Skills**: 지식 참조 (현재 구조 유지)
4. **Templates**: 산출물 표준화

**핵심 기술**:
- CoD: 밀도 증가
- ToT: 대안 탐색
- SoT: 구조 우선
- Re-ranking: 컨텍스트 관리
- Knowledge Graph: 모순 탐지

이 구조로 Gemini 연구의 4-Phase를 9-Stage에 완전히 매핑합니다.

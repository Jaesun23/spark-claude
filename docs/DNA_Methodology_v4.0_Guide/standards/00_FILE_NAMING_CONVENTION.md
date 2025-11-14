# DNA 방법론 파일 명명 규칙

> **목적**: Stage와 문서 역할을 파일명만으로 즉시 파악
> **버전**: v1.0 (2025-11-12)
> **적용 범위**: DNA 방법론의 모든 문서 (가이드 + 프로젝트 산출물)

---

## 🎯 핵심 원칙

**"파일명만 봐도 어느 Stage의 무슨 역할인지 즉시 알 수 있어야 한다"**

### 왜 필요한가?

❌ **명명 규칙 없으면**:
```
core_functions.md
family.md
constraints_final_v2.md
tech_decision_revised.md
ADR-fastapi.md
```
→ 어느 Stage인지? 순서는? 타입은? → **혼란!**

✅ **명명 규칙 있으면**:
```
01F-01_core_functions.md          # Stage 1, Function 문서
01C-01_family_classification.md   # Stage 1, Classification 문서
02C-01_layer3_constraints.md      # Stage 2, Classification 문서
02D-01_tech_stack_decision.md     # Stage 2, Decision 문서
03A-103_fastapi_selection.md      # Stage 3, ADR (Domain)
```
→ **Stage, Type, 순서 즉시 파악!**

---

## 📋 파일명 구조

### **패턴**: `{Stage}{Type}-{Seq}_{descriptive_name}.md`

```
01F-01_core_functions.md
│││ ││ └────────────────── 설명적 이름 (영문, snake_case)
│││ ││
│││ │└─────────────────── 순서 번호 (01~99)
│││ │
│││ └──────────────────── 구분자 (하이픈)
││└─────────────────────── 문서 타입 (알파벳 1글자)
│└──────────────────────── Stage 번호 (01~09)
└───────────────────────── 2자리 숫자 (앞에 0 붙임)
```

### **구성 요소**

| 요소 | 포맷 | 설명 | 예시 |
|------|------|------|------|
| **Stage** | 2자리 숫자 | 01~09 (9개 Stage) | `01`, `02`, `03` |
| **Type** | 알파벳 1글자 | 문서 유형 코드 | `F`, `C`, `D`, `A`, `G` |
| **Seq** | 2자리 숫자 | 01~99 (같은 Stage+Type 내 순서) | `01`, `02`, `03` |
| **Name** | snake_case | 설명적 이름 (영문) | `core_functions`, `tech_stack_decision` |

---

## 🔤 Type 코드 정의

### **프로젝트 산출물** (실제 프로젝트마다 생성하는 문서)

| Code | 의미 | 용도 | 예시 |
|------|------|------|------|
| **F** | Function | 기능 정의 | `01F-01_core_functions.md` |
| **C** | Classification | 분류/분석 결과 | `01C-01_family_classification.md` |
| **D** | Decision | 결정 사항 | `02D-01_tech_stack_decision.md` |
| **S** | Schema | 스키마/설계 | `02S-02_data_schema_v1.md` |
| **A** | ADR | Architecture Decision Record | `03A-001_logging.md` |
| **B** | Blueprint | 청사진 | `07B-01_project_blueprint.md` |
| **T** | Task | 작업 분해 | `08T-01_task_breakdown.md` |
| **L** | List/Checklist | 체크리스트 | `09L-01_task_001_checklist.md` |

### **방법론 문서** (DNA 방법론 자체 가이드)

| Code | 의미 | 용도 | 예시 |
|------|------|------|------|
| **G** | Guide | 간결한 가이드 (지침+템플릿) | `01G-00_core_definition_guide.md` |
| **M** | Manual | 상세 해설서 | `01M-01_layer1_manual.md` |
| **E** | Example/Case | 사례집 | `02E-01_stock_trading_case.md` |

### **특수 문서** (Stage 무관)

| Code | 의미 | 용도 | 예시 |
|------|------|------|------|
| **00** | Meta | 방법론 자체 문서 | `00_FILE_NAMING_CONVENTION.md` |

---

## 📁 Stage별 파일명 예시

### **Stage 0: 방법론 메타 문서**

```
00_FILE_NAMING_CONVENTION.md      # 이 문서!
00_STAGE_STRUCTURE.md              # Stage 구조 기준서
00_CORE_METHODOLOGY.md             # 방법론 개요
```

---

### **Stage 1: 패밀리 구분과 핵심기능 파악**

**가이드 문서** (`docs/completed-guide/`):
```
01G-00_core_definition_guide.md           # Stage 1 간결 가이드
01M-01_layer1_manual.md                   # Layer 1 상세 해설
01M-02_layer2_manual.md                   # Layer 2 상세 해설
01E-01_implementation_cases.md            # 사례: A-C-A, A-A-B, B-C-A
```

**프로젝트 산출물** (`docs/architecture/` 또는 프로젝트별 경로):
```
01F-01_core_functions.md                  # 핵심 기능 정의
01C-01_family_classification.md           # 패밀리 분류 (A-C-A)
01C-02_nfr_profile.md                     # NFR 프로파일 (A-B-B-A)
01D-01_tech_candidates.md                 # 기술 후보군
```

**입력 → 출력**:
```
입력: (없음 - 프로젝트 아이디어만)
   ↓
작업: 01G-00, 01M-01, 01M-02 참고
   ↓
출력: 01F-01, 01C-01, 01C-02, 01D-01
```

---

### **Stage 2: 구조설계**

**가이드 문서**:
```
02G-00_structure_design_guide.md          # Stage 2 간결 가이드
02M-01_layer3_manual.md                   # Layer 3 조사 해설
02M-02_conflict_resolution_manual.md      # 충돌 해결 해설
02M-03_5step_implementation_manual.md     # 5단계 구현 해설
02E-01_stock_trading_case.md              # 사례: 주식 거래 플랫폼
```

**프로젝트 산출물**:
```
02C-01_layer3_constraints.md              # Layer 3 제약 조사
02C-02_conflicts_analysis.md              # 충돌 패턴 분석
02D-01_tech_stack_decision.md             # 기술 스택 확정
02S-01_architecture_diagram.png           # 아키텍처 다이어그램
02S-02_data_schema_v1.md                  # 데이터 스키마
02S-03_api_design_v1.md                   # API 설계
02L-01_adr_list.md                        # ADR 작성 대상 목록
```

**입력 → 출력**:
```
입력: 01F-01, 01C-01, 01C-02, 01D-01
   ↓
작업: 02G-00, 02M-01, 02M-02, 02M-03 참고
   ↓
출력: 02C-01, 02C-02, 02D-01, 02S-01~03, 02L-01
```

---

### **Stage 3: ADR 문서화**

**가이드 문서**:
```
03G-00_adr_guide.md                       # Stage 3 간결 가이드
03M-01_adr_writing_manual.md              # ADR 작성 해설
03E-01_adr_examples.md                    # ADR 예시 모음
```

**프로젝트 산출물** (`docs/adr/`):
```
DNA 시스템/
  03A-001_logging.md                      # DNA 시스템 ADR
  03A-002_error_handling.md
  03A-003_authentication.md
  03A-004_configuration.md
  ...                                     # 총 10-15개

domain/
  03A-101_kis_api_selection.md            # Domain ADR (100번대 시작)
  03A-102_hybrid_strategy.md
  03A-103_fastapi_selection.md
  03A-104_websocket_design.md
  ...                                     # 총 15-20개
```

**입력 → 출력**:
```
입력: 02D-01, 02C-02, 02L-01 (Stage 2 모든 산출물)
   ↓
작업: 03G-00, 03M-01 참고
   ↓
출력: 03A-001~015 (DNA 시스템), 03A-101~120 (Domain)
```

**ADR 번호 규칙**:
- **001~099**: DNA 시스템 ADR (공통 환경)
- **100~999**: Domain ADR (프로젝트 특화)

---

### **Stage 4: DNA 시스템 계획**

**가이드 문서**:
```
04G-00_DNA 시스템_plan_guide.md            # Stage 4 간결 가이드
04M-01_common_modules_manual.md           # 공통 모듈 해설
```

**프로젝트 산출물**:
```
04B-01_dna_system_blueprint.md            # DNA 기본시스템 청사진
04L-01_DNA 시스템_checklist.md             # DNA 시스템 체크리스트
```

---

### **Stage 5: DNA 시스템 실행**

**가이드 문서**:
```
05G-00_DNA 시스템_execution_guide.md       # Stage 5 간결 가이드
```

**프로젝트 산출물**:
```
(실제 코드 구현 - 문서 아님)
src/core/                                 # 구현된 DNA 시스템
tests/core/                               # 테스트 코드
05D-01_module_usage_docs.md               # 모듈 사용법 문서
```

---

### **Stage 6: Project Standards**

**가이드 문서**:
```
06G-00_project_standards_guide.md         # Stage 6 간결 가이드
```

**프로젝트 산출물**:
```
06D-01_project_standards.md               # 프로젝트 표준 (THE 산출물)
```

---

### **Stage 7: Project Blueprint**

**가이드 문서**:
```
07G-00_blueprint_guide.md                 # Stage 7 간결 가이드
07M-01_domain_design_manual.md            # 도메인 설계 해설
```

**프로젝트 산출물**:
```
07B-01_project_blueprint.md               # 프로젝트 청사진 (초상세)
07S-01_domain_architecture.md             # 도메인 아키텍처
07S-02_domain_diagrams/                   # 도메인별 다이어그램
```

---

### **Stage 8: Task Breakdown**

**가이드 문서**:
```
08G-00_task_breakdown_guide.md            # Stage 8 간결 가이드
```

**프로젝트 산출물**:
```
08T-01_task_breakdown.md                  # 작업 분해 (THE 산출물)
```

---

### **Stage 9: Checklist**

**가이드 문서**:
```
09G-00_checklist_guide.md                 # Stage 9 간결 가이드
```

**프로젝트 산출물**:
```
09L-01_task_001_checklist.md              # 작업 1 체크리스트
09L-02_task_002_checklist.md              # 작업 2 체크리스트
09L-03_task_003_checklist.md              # 작업 3 체크리스트
...
```

---

## 🎯 Type 치트시트 (빠른 참조)

### **프로젝트 산출물**
```
F = Function      (기능 정의)
C = Classification (분류/분석)
D = Decision      (결정 사항)
S = Schema        (스키마/설계)
A = ADR           (아키텍처 결정)
B = Blueprint     (청사진)
T = Task          (작업 분해)
L = List/Checklist (체크리스트)
```

### **방법론 문서**
```
G = Guide         (간결 가이드)
M = Manual        (상세 해설)
E = Example/Case  (사례집)
```

### **읽는 법**
```
01F-01_core_functions.md
│││ ││
││└─┴─ F-01 = Function 문서, 첫 번째
│└──── 01 = Stage 1
└───── "Stage 1의 첫 번째 Function 문서"

02C-02_conflicts_analysis.md
│││ ││
││└─┴─ C-02 = Classification 문서, 두 번째
│└──── 02 = Stage 2
└───── "Stage 2의 두 번째 Classification 문서"

03A-101_fastapi_selection.md
│││ │││
││└─┴┴─ A-101 = ADR, 101번 (Domain ADR 시작)
│└──── 03 = Stage 3
└───── "Stage 3의 101번 ADR (Domain)"
```

---

## 📦 파일 저장 위치

### **방법론 문서**
```
docs/completed-guide/
├── 00_*.md                    # 메타 문서
├── 01G-00_*.md                # Stage 1 가이드
├── 01M-01_*.md                # Stage 1 매뉴얼
├── 02G-00_*.md                # Stage 2 가이드
└── ...
```

### **프로젝트 산출물**
```
docs/
├── architecture/              # Stage 1-2 산출물
│   ├── 01F-01_core_functions.md
│   ├── 01C-01_family_classification.md
│   ├── 02C-01_layer3_constraints.md
│   └── ...
│
├── adr/                       # Stage 3 산출물
│   ├── DNA 시스템/
│   │   ├── 03A-001_logging.md
│   │   └── ...
│   └── domain/
│       ├── 03A-101_*.md
│       └── ...
│
├── DNA 시스템/                 # Stage 4-5 산출물
│   ├── 04B-01_dna_system_blueprint.md
│   └── ...
│
├── standards/                 # Stage 6 산출물
│   └── 06D-01_project_standards.md
│
├── blueprint/                 # Stage 7 산출물
│   └── 07B-01_project_blueprint.md
│
├── tasks/                     # Stage 8 산출물
│   └── 08T-01_task_breakdown.md
│
└── checklists/                # Stage 9 산출물
    ├── 09L-01_*.md
    └── ...
```

---

## ✅ 명명 규칙 체크리스트

새 문서 생성 시 확인:

- [ ] Stage 번호가 정확한가? (01~09)
- [ ] Type 코드가 올바른가? (F/C/D/S/A/B/T/L/G/M/E)
- [ ] Seq 번호가 중복되지 않는가?
- [ ] 설명적 이름이 snake_case인가?
- [ ] 파일 확장자가 `.md`인가? (다이어그램 제외)
- [ ] 저장 위치가 올바른가?

---

## 🔄 기존 파일 마이그레이션

기존 문서들을 새 규칙에 맞게 변경:

### **Before → After**
```
CORE_METHODOLOGY.md
→ 00_CORE_METHODOLOGY.md

01_CORE_DEFINITION_GUIDE.md
→ 01G-00_core_definition_guide.md

01-1_CORE_DEFINITION_MANUAL_Part1.md
→ 01M-01_layer1_manual.md

02_STRUCTURE_DESIGN_GUIDE.md
→ 02G-00_structure_design_guide.md

03_ADR_GUIDE.md
→ 03G-00_adr_guide.md

04_PROJECT_STANDARDS_GUIDE.md
→ 06G-00_project_standards_guide.md  # Stage 6!

05_BLUEPRINT_GUIDE.md
→ 07G-00_blueprint_guide.md  # Stage 7!

06_TASK_BREAKDOWN_GUIDE.md
→ 08G-00_task_breakdown_guide.md  # Stage 8!

07_CHECKLIST_GUIDE.md
→ 09G-00_checklist_guide.md  # Stage 9!
```

---

## 🎓 실전 예시

### **예시 1: 새 프로젝트 시작**

```bash
# Stage 1: 패밀리 구분
01F-01_core_functions.md          # 핵심 기능: 거래
01C-01_family_classification.md   # 패밀리: A-C-A
01C-02_nfr_profile.md             # NFR: A-B-B-A
01D-01_tech_candidates.md         # 후보: WebSocket, FastAPI...

# Stage 2: 구조설계
02C-01_layer3_constraints.md      # 한국투자증권 API 조사
02C-02_conflicts_analysis.md      # 충돌 3개 발견
02D-01_tech_stack_decision.md     # FastAPI + PostgreSQL 확정
02L-01_adr_list.md                # 작성할 ADR 18개

# Stage 3: ADR
03A-001_logging.md                # DNA 시스템 ADR 시작
...
03A-101_kis_api_selection.md      # Domain ADR 시작
...
```

### **예시 2: 파일명으로 즉시 파악**

```bash
ls docs/architecture/

01F-01_core_functions.md          # "아, Stage 1 기능 정의구나"
01C-01_family_classification.md   # "패밀리 분류 결과네"
02C-01_layer3_constraints.md      # "Stage 2에서 조사한 제약사항이구나"
02D-01_tech_stack_decision.md     # "기술 스택 확정했구나"
```

---

## 🚀 규칙의 장점

### 1. **즉시 파악**
- 파일명만 봐도 Stage와 역할 명확
- `ls` 명령 결과만 봐도 구조 이해

### 2. **자동 정렬**
- Stage → Type → Seq 순서로 자동 정렬
- 시간 순서대로 자연스럽게 배열

### 3. **AI 친화적**
- 명확한 규칙 → AI가 헷갈리지 않음
- 입력/출력 문서 명세 가능

### 4. **확장 가능**
- 새 Type 추가 가능 (예: R=Research)
- Stage 추가 가능 (10~99)

### 5. **검색 용이**
- `grep "02C-"` → Stage 2 Classification 문서 모두 찾기
- `find . -name "03A-*"` → 모든 ADR 찾기

---

## 📚 참고 자료

- **00_STAGE_STRUCTURE.md**: 9개 Stage 전체 구조
- **00_CORE_METHODOLOGY.md**: DNA 방법론 개요
- **각 Stage 가이드**: 구체적 작성 방법

---

**버전 이력**:
- v1.0 (2025-11-12): 초기 작성 (Jason + 2호 협의)

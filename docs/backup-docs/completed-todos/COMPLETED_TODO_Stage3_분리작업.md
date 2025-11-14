# Stage 3 분리 작업 지시서

> **작성일**: 2025-11-13
> **목적**: 03G-00_adr_guide.md (3,060줄)를 4개 파일로 분리
> **백업**: 03G-00_adr_guide.md.backup (원본)

---

## 📋 작업 개요

**현재 상태**:
- 03G-00_adr_guide.md: 3,060줄 (1개 파일)
- Guide + Manual + Cases가 모두 혼합됨

**목표 상태**:
- 03G-00_adr_guide.md: ~1,000줄 (Guide - 기본 작성 가능)
- 03M-01_adr_types_manual.md: ~1,200줄 (Manual - 5가지 유형 상세)
- 03M-02_adr_to_standards_manual.md: ~600줄 (Manual - 변환 프로세스)
- 03E-01_adr_examples_cases.md: ~700줄 (Cases - 실전 사례)

---

## 📊 섹션 분배표

### 원본 파일 구조 (줄 번호):

```
0-400: 헤더 (가이드 구성, 입출력 문서, 템플릿)
402-505: 1. ADR이란 무엇인가 (~100줄)
506-1866: 2. ADR의 5가지 유형 (~1360줄!) ⚠️
1867-2143: 3. ADR 7개 섹션 템플릿 (~280줄)
2144-2357: 4. 좋은 ADR 작성하기 (~210줄)
2358-2780: 5. ADR→Standards 변환 (~420줄) ⚠️
2781-2970: 6. ADR 생명주기 관리 (~190줄)
2971-3060: 7. 다음 단계 연결 (~90줄)
```

### 분리 계획:

**03G-00 (Guide)** - 줄 범위:
```
0-400: 헤더 전체
402-505: 1. ADR이란 무엇인가
506-550: 2. ADR의 5가지 유형 (개요만, 상세는 Manual로)
1867-2143: 3. ADR 7개 섹션 템플릿
2144-2357: 4. 좋은 ADR 작성하기
2781-2970: 6. ADR 생명주기 관리
2971-3060: 7. 다음 단계 연결
```

**03M-01 (Manual - ADR Types)** - 줄 범위:
```
506-1866: 2. ADR의 5가지 유형 (전체)
  - 2-1. Type 1: Structure (상세 + 완전한 예시 ADR)
  - 2-2. Type 2: Nonfunctional (상세 + 완전한 예시 ADR)
  - 2-3. Type 3: Dependency (상세 + 완전한 예시 ADR)
  - 2-4. Type 4: Interface (상세 + 완전한 예시 ADR)
  - 2-5. Type 5: Construction (상세 + 완전한 예시 ADR)
  - 2-6. 구현방법에서 ADR로 연결 (사례 포함)
```

**03M-02 (Manual - Conversion)** - 줄 범위:
```
2358-2780: 5. ADR→Standards 변환 프로세스 (전체)
  - 변환 절차
  - Standards 파일 구조
  - 상세 예시 (structlog, API, Testing)
```

**03E-01 (Cases)** - 새로 추출:
```
섹션 2-6의 실전 사례 부분:
  - 사례 1: 문서 자동생성 (Milvus, Human-in-the-loop)
  - 사례 2: AI 외부 메모리 (Kafka, RLS)
  - 사례 3: 채팅 애플리케이션 (WebSocket)
```

---

## 🔨 작업 순서

### Step 1: 03M-01 생성 (Manual - ADR Types)
```bash
# 506-1866줄 추출
sed -n '506,1866p' 03G-00_adr_guide.md.backup > temp_m01.md
```

**작업**:
1. 헤더 추가 (제목, 목적, 버전)
2. "이 문서는 03G-00의 섹션 2를 상세히 설명합니다" 추가
3. 5가지 유형 각각 완전한 예시 ADR 포함 확인
4. Manual로서 자체 완결성 확인

### Step 2: 03M-02 생성 (Manual - Conversion)
```bash
# 2358-2780줄 추출
sed -n '2358,2780p' 03G-00_adr_guide.md.backup > temp_m02.md
```

**작업**:
1. 헤더 추가
2. "이 문서는 03G-00의 섹션 5를 상세히 설명합니다" 추가
3. ADR→Standards 변환 프로세스 전체 포함 확인
4. 상세 예시 (structlog, API, Testing) 포함 확인

### Step 3: 03E-01 생성 (Cases)
**작업**:
1. 03M-01에서 "사례 1, 2, 3" 부분 추출
2. 새로운 파일로 정리
3. 각 사례별 완전한 ADR 예시 포함
4. 실전 적용 패턴 설명 추가

### Step 4: 03G-00 재구성 (Guide)
**작업**:
1. 원본에서 다음 섹션만 유지:
   - 0-400: 헤더
   - 402-505: 1. ADR이란 무엇인가
   - 1867-2143: 3. ADR 7개 섹션 템플릿
   - 2144-2357: 4. 좋은 ADR 작성하기
   - 2781-2970: 6. ADR 생명주기 관리
   - 2971-3060: 7. 다음 단계 연결

2. 섹션 2를 간결한 개요로 교체:
```markdown
## 2. ADR의 5가지 유형

ADR은 결정의 성격에 따라 5가지로 분류됩니다:

1. **Structure** - 시스템 조직, 아키텍처 패턴
   - 예: Clean Architecture, Microservices

2. **Nonfunctional** - 성능, 보안, 테스트 커버리지
   - 예: 테스트 95% 커버리지 필수

3. **Dependency** - 외부 라이브러리, 프레임워크
   - 예: structlog 사용, FastAPI 선택

4. **Interface** - API 설계, 모듈 간 계약
   - 예: RESTful API, GraphQL

5. **Construction** - 코드 작성 방식, 패턴
   - 예: Pydantic for DTOs, async/await

**상세 설명**: `03M-01_adr_types_manual.md` 참고
```

3. 섹션 5 제거하고 참조 추가:
```markdown
## 5. ADR → Standards 변환

ADR 작성 후 Standards 문서로 변환하여 Quality Gates에 연결합니다.

**상세 프로세스**: `03M-02_adr_to_standards_manual.md` 참고
```

4. "이 가이드의 구성" 섹션 업데이트:
```markdown
## 📚 이 가이드의 구성

- **이 문서** (Guide): ADR 작성 방법 + 템플릿
- **상세 설명** (Manual):
  - `03M-01_adr_types_manual.md` - 5가지 유형 상세
  - `03M-02_adr_to_standards_manual.md` - 변환 프로세스
- **실전 사례** (Cases):
  - `03E-01_adr_examples_cases.md` - 프로젝트 사례
```

---

## ✅ 완료 기준

### 03G-00 검증:
- [ ] 줄 수 ~1,000줄 이내
- [ ] Guide만 보고 ADR 기본 작성 가능 (7개 섹션 템플릿 포함)
- [ ] Manual/Cases 참조 링크 정확
- [ ] 자체 완결적 (Manual 없이도 이해 가능)

### 03M-01 검증:
- [ ] 5가지 유형 각각 완전한 예시 ADR 포함
- [ ] 상세 설명 + Compliance 전략 포함
- [ ] Guide로 돌아가는 링크 있음

### 03M-02 검증:
- [ ] ADR→Standards 변환 프로세스 완전
- [ ] 상세 예시 (structlog, API, Testing) 포함
- [ ] Guide로 돌아가는 링크 있음

### 03E-01 검증:
- [ ] 3개 사례 모두 포함
- [ ] 각 사례별 완전한 ADR 예시
- [ ] 실전 적용 패턴 설명

---

## 📝 작업 시 주의사항

1. **Bootstrap → DNA 용어 통일**: 분리 작업 중 발견되면 함께 수정
2. **버전 번호**: 모든 파일 v3.0 (2025-11-13, Stage 3 분리)
3. **크로스 레퍼런스**: 상호 참조 링크 정확히
4. **자체 완결성**: Guide는 Manual 없이도 기본 작성 가능해야 함

---

**원본 백업**: `03G-00_adr_guide.md.backup`

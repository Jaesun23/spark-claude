# 핸드오버 문서: archive-curator 스킬 설계

**작성자**: 1호 (Cowork)
**작성일**: 2026-03-25
**프로젝트**: archive-curator 스킬 — 문서 분류 및 가치 평가 시스템

---

## 1. 핵심 컨텍스트 (Immutable Context)

### 프로젝트 목적
세 프로젝트(SPARK, TRAITS, CURATOR)의 대량 비정형 문서를 **내용 기반으로 심층 분류**하고,
학술적 방법론(패싯 분류법, 셸렌버그 가치론, ROT 분석, Dublin Core)에 기반하여
체계적으로 정리·평가하는 AI 스킬을 설계한다.

### 전체에서의 위치
```
[1단계] archive-curator 스킬 설계 ← 현재 여기 (완료)
[2단계] 실제 프로젝트에 archive-curator 적용 (SPARK → TRAITS → CURATOR 순)
[3단계] CURATOR 전용 도구 (의사결정 트리, 문서 자동생성) — 미래
```

### MUST / MUST NOT
- **MUST**: 모든 문서는 내용을 읽고 분류 (파일명만으로 판단 금지)
- **MUST**: 분류 모델 최소 Sonnet, 가치 판단은 Opus 권장
- **MUST**: 분류 결과는 Jason 확인 후에만 노션에 기록
- **MUST NOT**: 티어별 분류 (filename-only tier 없음, 모두 content-based)
- **MUST NOT**: 📁 파일 카탈로그 DB 수정 (별도 📂 문서 아카이브 DB 사용)

### Definition of Done
- [x] archive-curator 스킬 파일 완성 (SKILL.md + 4개 references)
- [x] 노션 📂 문서 아카이브 DB 생성 (12 필드)
- [ ] 실제 프로젝트에 최초 적용 (SPARK 디렉토리부터)

---

## 2. 현재 상태

### 완료된 작업
- 제이(Gemini)의 이론 연구: 문서 분류 체계 및 가치 평가 프레임워크
- 1호(Claude)의 실무 연구: AI 기반 문서 분류 패턴 및 도구 분석
- 두 연구를 융합하여 archive-curator 스킬 설계 완료
- 노션 📂 문서 아카이브 DB 생성 완료

### 스킬 파일 위치
```
/Users/jason/.claude/skills/archive-curator/
├── SKILL.md                              # 메인 스킬 정의 (6-Phase 워크플로우)
└── references/
    ├── classification-criteria.md        # 프로파일별 카테고리·태그 정의
    ├── metadata-schema.md                # 8+3 메타데이터 필드 스키마
    ├── notion-db-mapping.md              # 노션 DB 필드 매핑 및 API 사용법
    └── theoretical-foundations.md         # 이론적 기반 요약
```

### 노션 DB 정보
- **📂 문서 아카이브**: data_source_id `f1afc956-dbeb-433a-a3d1-1f5fbc848043`
- **위치**: 🧠 Claude Memory Space 하위
- **필드 12개**: 이름, Category, Tags, Status, Date, File Type, File Path, AI Summary, Time Period, Version, Value Grade, Author

### 진행률: 약 85%
- 스킬 설계: 100%
- 노션 DB 생성: 100%
- 실제 적용: 0% (다음 단계)

---

## 3. 인라인 기준 (Inline Standards)

### 6-Phase 워크플로우
```
Phase 1: 인벤토리 → 재귀 스캔, 파일 목록 생성
Phase 2: 전처리 → 파일 유형별 텍스트 추출 (PyMuPDF4LLM for PDF)
Phase 3: 분류 → 패싯 분류 (Category 1개 + Tags 2-5개 + AI Summary)
Phase 4: 가치 평가 → ROT 클렌징 → 셸렌버그 5등급 평가
Phase 5: 리포트 → 종합 리포트, Jason 확인 필수
Phase 6: 노션 동기화 → 📂 문서 아카이브 DB에 기록
```

### 프로젝트 프로파일
- **연구 아카이브** (SPARK, TRAITS): 정보적 가치 우선, 태그 깊게, 버전 추적 필수
- **실무 지식베이스** (CURATOR): 증거적 가치 우선, 수명주기 상태 우선, 비즈니스 기능 축 활성

### 핵심 설계 결정
- 분류 체계: 하이브리드 패싯 모델 (단일 폴더 트리 X)
- 가치 평가: ROT 먼저 → 셸렌버그 (노이즈 제거 후 가치 판단)
- 메타데이터: Dublin Core 기반 8+3 필드 (과도하지 않게)
- 노션 DB: 기존 📁 파일 카탈로그와 별도 운영
- 모델 기준: 분류 최소 Sonnet, 가치 판단 Opus 권장

---

## 4. 미결 이슈

- 스킬 적용 순서 미확정: SPARK → TRAITS → CURATOR 순 제안했으나 Jason 확인 필요
- CURATOR 전용 도구(의사결정 트리, 문서 자동생성)는 분류 완료 후 별도 프로젝트로 진행
- 📂 문서 아카이브 DB에 Relation 필드(📁 파일 카탈로그 연결)는 필요 시 추가

---

## 5. 다음 작업

**즉시 시작 가능한 작업**: archive-curator 스킬을 SPARK 프로젝트에 최초 적용

1. SPARK 디렉토리를 대상으로 Phase 1(인벤토리) 실행
2. 152개 파일에 대해 Phase 2-3(전처리 + 분류) 수행
3. Phase 4(가치 평가) 후 Phase 5(리포트) 작성
4. Jason 확인 후 Phase 6(노션 동기화)
5. 결과를 바탕으로 스킬 개선점 도출

---

*이 문서는 Cowork 세션 간 컨텍스트 공유를 위해 작성되었습니다.*
*원본 연구 요청서: 연구요청서_1호_실무적용연구.md, 연구요청서_제이_문서분류체계.md*

# DNA Skills 세션별 작업 가이드

## 개요

DNA 플러그인은 11개 세션으로 개발됩니다. 각 세션은 독립적으로 실행 가능하며, 해당 Stage의 references와 commands만 작업합니다.

### ⚠️ 작업 위치 원칙

**모든 작업이 완료되기 전까지는 프로젝트 내에서 작업합니다.**

- **작업 경로**: `/Users/jason/Projects/spark-claude/skills/dna-methodology/`
- **이유**: 커밋 관리, 버전 추적, 협업 용이
- **완료 후**: `~/.claude/skills/`로 배포

---

## 세션 0: Core 기반 구조 (완료)

**목표**: Skill 기본 구조 + 공통 지식 작성

**작업 내용**:
- [x] Skill 디렉토리 구조 생성
- [x] SKILL.md 기본 구조 (Stage 1-9 개요)
- [x] references/core/ 공통 지식
  - methodology-overview.md
  - families.md (7개 패밀리)
  - nfr-definitions.md
  - context-management.md
- [x] assets/templates/ JSON 템플릿
- [x] 세션별 작업 가이드 (이 문서)

**산출물**:
- `~/.claude/skills/dna-methodology/` 기본 구조 완성

---

## 세션 1: Stage 1 - Core Definition

**목표**: 시스템 핵심 정의 (패밀리 분류)

**작업 내용**:
- [ ] references/stage1/
  - layer1-questions.md
  - layer2-questions.md
- [ ] scripts/validate_stage1.py

**참조 문서** (DNA_Methodology_v4.0_Guide/):
- 01G-00_core_definition_guide.md
- 01M-01_layer1_manual.md
- 01M-02_layer2_manual.md

**Commands (선택)**:
- /dna:stage1 - Stage 1 실행

---

## 세션 2: Stage 2 - Structure Design

**목표**: 환경 제약 조사 및 충돌 해결

**작업 내용**:
- [ ] references/stage2/
  - layer3-questions.md
  - conflict-patterns.md
- [ ] scripts/validate_stage2.py

**참조 문서**:
- 02G-00_environment_constraints_guide.md
- 02M-01_environment_constraints_manual.md
- 02E-01_stock_trading_case.md

---

## 세션 3: Stage 3 - ADR

**목표**: 아키텍처 결정 기록

**작업 내용**:
- [ ] references/stage3/
  - adr-template.md
  - adr-categories.md
- [ ] scripts/validate_stage3.py

**참조 문서**:
- 03G-00_adr_guide.md
- 03M-01_adr_types_manual.md
- 03M-02_adr_to_standards_manual.md
- 03E-02_kent_beck_bplustree_case.md

---

## 세션 4: Stage 4 - DNA Planning

**목표**: 11개 DNA 시스템 계획

**작업 내용**:
- [ ] references/stage4/
  - dna-systems.md
  - system-dependencies.md
- [ ] scripts/validate_stage4.py

**참조 문서**:
- 04G-00_dna_planning_guide.md
- DNA_Systems_11_Complete_Guide.md

---

## 세션 5: Stage 5 - DNA Implementation

**목표**: DNA 시스템 구현

**작업 내용**:
- [ ] references/stage5/
  - implementation-guide.md
  - testing-requirements.md
- [ ] scripts/validate_stage5.py

**참조 문서**:
- 05G-00_dna_implementation_guide.md

---

## 세션 6: Stage 6 - Project Standards

**목표**: ADR → DO/DON'T 규칙 변환 및 자동화

**작업 내용**:
- [ ] references/stage6/
  - standards-guide.md
  - automation-setup.md
- [ ] scripts/validate_stage6.py

**참조 문서**:
- 06G-00_project_standards_guide.md

---

## 세션 7: Stage 7 - Blueprint

**목표**: 완전한 프로젝트 청사진 작성

**작업 내용**:
- [ ] references/stage7/
  - blueprint-guide.md
  - blueprint-template.md
- [ ] scripts/validate_stage7.py

**참조 문서**:
- 07G-00_blueprint_guide.md

---

## 세션 8: Stage 8 - Task Breakdown

**목표**: 청사진을 레고블럭으로 분해

**작업 내용**:
- [ ] references/stage8/
  - task-breakdown-guide.md
  - dependency-graph.md
- [ ] scripts/validate_stage8.py

**참조 문서**:
- 08G-00_task_breakdown_guide.md

---

## 세션 9: Stage 9 - Checklist

**목표**: 작업별 실행 체크리스트 작성

**작업 내용**:
- [ ] references/stage9/
  - checklist-guide.md
  - 9-step-template.md
- [ ] scripts/validate_stage9.py

**참조 문서**:
- 09G-00_checklist_guide.md

---

## 세션 10: Commands/Agents 연동 + 통합 테스트

**목표**: 전체 통합 및 테스트

**작업 내용**:
- [ ] commands/ 생성 (선택적)
  - start.md
  - stage1.md ~ stage9.md
- [ ] SPARK agents 연동 설정
- [ ] 전체 흐름 테스트
- [ ] 문서 최종 검토

---

## 세션 실행 원칙

### 독립성
각 세션은 이전 세션의 산출물만 참조하면 됩니다.
- 세션 N은 references/stageN/ 작업
- 이전 Stage JSON 출력만 확인

### 참조 문서 활용
각 세션에서 해당 Stage의 가이드/매뉴얼/케이스를 참조:
```
/Users/jason/Projects/spark-claude/docs/DNA_Methodology_v4.0_Guide/
├── 01G-00_*.md (Stage 1)
├── 02G-00_*.md (Stage 2)
├── ...
└── 09G-00_*.md (Stage 9)
```

### 검증
각 세션 완료 시:
1. scripts/validate_stageN.py 실행
2. 산출물을 JSON으로 구조화
3. 다음 세션을 위한 context_summary 업데이트

---

## 진행 현황

| 세션 | Stage | 상태 | 완료일 |
|------|-------|------|--------|
| 0 | Core 기반 | ✅ 완료 | - |
| 1 | Stage 1 | ⏳ 대기 | - |
| 2 | Stage 2 | ⏳ 대기 | - |
| 3 | Stage 3 | ⏳ 대기 | - |
| 4 | Stage 4 | ⏳ 대기 | - |
| 5 | Stage 5 | ⏳ 대기 | - |
| 6 | Stage 6 | ⏳ 대기 | - |
| 7 | Stage 7 | ⏳ 대기 | - |
| 8 | Stage 8 | ⏳ 대기 | - |
| 9 | Stage 9 | ⏳ 대기 | - |
| 10 | 통합 | ⏳ 대기 | - |

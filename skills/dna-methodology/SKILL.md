---
name: dna-methodology
description: DNA v4.0 소프트웨어 설계 방법론. 새 소프트웨어 프로젝트를 아이디어에서 구현까지 체계적으로 설계할 때 사용. Stage 1(핵심 정의) → Stage 2(구조 설계) → Stage 3(ADR) → Stage 4(DNA 계획) → Stage 5(DNA 구현) → Stage 6(표준) → Stage 7(청사진) → Stage 8(작업분해) → Stage 9(체크리스트) 순서로 진행. Context Rot 방지와 레고블럭 전략이 핵심.
license: MIT
---

# DNA v4.0 Software Design Methodology

## Overview

DNA v4.0은 AI 컨텍스트 한계를 극복하기 위한 소프트웨어 설계 방법론입니다.

**핵심 3단계 해결책**:
1. **단계적 정의**: Stage 1-6으로 환경 구축 → Stage 7-9로 실행
2. **환경 강제**: Standards + DNA Systems + 자동화로 일관성 보장
3. **레고블럭 전략**: 독립 실행 가능한 작업 단위로 분할

**Load**: [📋 Core Methodology](./references/core/methodology-overview.md)

---

## Stage 1: Core Definition (핵심 정의)

18가지 아키텍처 패밀리 중 하나를 선택하고 NFR 우선순위를 결정합니다.

**목표**: 시스템의 본질적 특성 파악
**산출물**: 패밀리 코드 (A-C-A 등), NFR 우선순위, 검증 사례

**Load**: [📋 Layer 1 Questions](./references/stage1/layer1-questions.md)
**Validate**: `scripts/validate_stage1.py`

**참조 문서** (DNA_Methodology_v4.0_Guide/):
- 01G-00_core_definition_guide.md
- 01M-01_layer1_manual.md
- 01M-02_layer2_manual.md

---

## Stage 2: Structure Design (구조 설계)

Layer 3 환경 제약을 조사하고 충돌을 식별합니다.

**목표**: 기술/팀/인프라 제약 파악, 충돌 해결
**산출물**: 제약 목록, 충돌 패턴, 해결안, 기술 후보

**Load**: [📋 Layer 3 Questions](./references/stage2/layer3-questions.md)
**Validate**: `scripts/validate_stage2.py`

**참조 문서** (DNA_Methodology_v4.0_Guide/):
- 02G-00_environment_constraints_guide.md
- 02M-01_environment_constraints_manual.md
- 02E-01_stock_trading_case.md

---

## Stage 3: Architecture Decision Records (ADR)

Bootstrap ADR을 작성하여 핵심 기술 결정을 문서화합니다.

**목표**: 모든 아키텍처 결정을 ADR로 기록
**산출물**: Bootstrap ADR 세트 (DB, Cache, Messaging 등)

**Load**: [📋 ADR Template](./references/stage3/adr-template.md)
**Validate**: `scripts/validate_stage3.py`

**참조 문서** (DNA_Methodology_v4.0_Guide/):
- 03G-00_adr_guide.md
- 03M-01_adr_types_manual.md
- 03M-02_adr_to_standards_manual.md
- 03E-02_kent_beck_bplustree_case.md

---

## Stage 4: DNA System Planning (DNA 시스템 계획)

11개 DNA 시스템의 구현 계획을 수립합니다.

**목표**: 공용 모듈 설계
**산출물**: 11개 DNA 시스템 스펙

**Load**: [📋 DNA Systems](./references/stage4/dna-systems.md)
**Validate**: `scripts/validate_stage4.py`

**참조 문서** (DNA_Methodology_v4.0_Guide/):
- 04G-00_dna_planning_guide.md
- DNA_Systems_11_Complete_Guide.md

---

## Stage 5: DNA System Implementation (DNA 시스템 구현)

계획된 DNA 시스템을 실제로 구현합니다.

**목표**: 공용 모듈 구현
**산출물**: 구현된 DNA 시스템 코드

**Load**: [📋 Implementation Guide](./references/stage5/implementation-guide.md)
**Validate**: `scripts/validate_stage5.py`

**참조 문서** (DNA_Methodology_v4.0_Guide/):
- 05G-00_dna_implementation_guide.md

---

## Stage 6: Project Standards (프로젝트 표준)

ADR을 DO/DON'T 규칙으로 변환하고 자동화를 설정합니다.

**목표**: 강제 가능한 표준 수립
**산출물**: PROJECT_STANDARDS.md, Pre-commit hooks, CI/CD 설정

**Load**: [📋 Standards Guide](./references/stage6/standards-guide.md)
**Validate**: `scripts/validate_stage6.py`

**참조 문서** (DNA_Methodology_v4.0_Guide/):
- 06G-00_project_standards_guide.md

---

## Stage 7: Blueprint (청사진)

환경이 갖춰진 상태에서 전체 설계도를 작성합니다.

**목표**: 완전한 프로젝트 설계서
**산출물**: Blueprint 문서 (도메인 모델, API 설계, 4-Layer 구조)

**Load**: [📋 Blueprint Guide](./references/stage7/blueprint-guide.md)
**Validate**: `scripts/validate_stage7.py`

**참조 문서** (DNA_Methodology_v4.0_Guide/):
- 07G-00_blueprint_guide.md

---

## Stage 8: Task Breakdown (작업 분해)

청사진을 독립 실행 가능한 레고블럭으로 분해합니다.

**목표**: 2-4시간 단위의 원자적 작업
**산출물**: 작업 목록, 의존성 그래프

**Load**: [📋 Task Breakdown Guide](./references/stage8/task-breakdown-guide.md)
**Validate**: `scripts/validate_stage8.py`

**참조 문서** (DNA_Methodology_v4.0_Guide/):
- 08G-00_task_breakdown_guide.md

---

## Stage 9: Checklist (체크리스트)

각 작업별로 독립 실행 가능한 체크리스트를 작성합니다.

**목표**: 그 체크리스트만 보고 작업 완료 가능
**산출물**: 작업별 9-Step 체크리스트

**Load**: [📋 Checklist Guide](./references/stage9/checklist-guide.md)
**Validate**: `scripts/validate_stage9.py`

**참조 문서** (DNA_Methodology_v4.0_Guide/):
- 09G-00_checklist_guide.md

---

## Context Management

### JSON Templates

Stage 간 Context 전달을 위한 JSON 템플릿:
- `assets/templates/project_init.json` - 프로젝트 초기화
- `assets/templates/stageN_output.json` - Stage별 산출물
- `assets/templates/context_summary.json` - 전체 요약

### Context Rot Prevention

1. **독립 컨텍스트**: 각 Stage가 필요한 정보만 로드
2. **명시적 전달**: JSON 파일로 구조화된 데이터 전달
3. **레고블럭**: 각 작업이 독립 실행 가능

**Load**: [📋 Context Management](./references/core/context-management.md)

---

## Quick Start

1. `/dna:start` - 프로젝트 초기화
2. `/dna:stage1` - 시스템 분류
3. `/dna:stage2` - 제약 조사
4. ... (Stage 3-9)

각 Stage 완료 후 Validator로 검증하고 다음 Stage로 진행합니다.

# Context Management (컨텍스트 관리)

## 왜 컨텍스트 관리가 중요한가?

### AI 컨텍스트 한계의 본질

**트랜스포머 모델의 구조적 한계**:
- 토큰 간 관계를 학습하는데, 길이가 늘어나면 관계가 약해짐
- **많은 정보 ≠ 좋은 결과**
- 적당한 길이 + 적당한 수준 = 좋은 작업

**현실적 제약**:
- Claude Desktop: 200K hard limit
- Claude Code: Compact 있지만 앞부분 까먹음

---

## Context Rot (컨텍스트 부패)

### 정의
대화가 길어지면서 초기 정보의 중요도가 낮아지고, AI가 잘못된 결정을 내리는 현상

### 증상
1. **정보 손실**: 초기 결정사항 무시
2. **할루시네이션**: 존재하지 않는 정보 생성
3. **일관성 파괴**: 이전 결정과 충돌
4. **반복 실수**: 같은 오류 반복

### 발생 원인
- 컨텍스트 윈도우 초과
- 정보 우선순위 불명확
- 구조화되지 않은 전달

---

## 3가지 해결 전략

### 1. 독립 컨텍스트 (Independent Context)

**원칙**: 각 Stage/작업이 필요한 정보만 로드

**구현**:
```
Stage 1 → Layer 1-2 질문만
Stage 2 → Layer 3 제약만
Stage 3 → ADR 템플릿만
...
각 체크리스트 → 해당 작업 정보만
```

**효과**: 불필요한 정보로 인한 혼란 방지

---

### 2. 명시적 전달 (Explicit Transfer)

**원칙**: JSON 파일로 구조화된 데이터 전달

**구현**:
```json
// stage1_output.json
{
  "family": "A-A-B",
  "nfr_priorities": ["Consistency", "Reliability", "Performance"],
  "decisions": [...]
}
```

**효과**: 암묵적 정보 전달 제거, 검증 가능

---

### 3. 레고블럭 분할 (Lego Block Division)

**원칙**: 독립 실행 가능한 작업 단위로 분할

**구현**:
```
청사진 (모든 것을 담은 설계도)
    ↓
작업분해 (2-4시간 단위 블럭)
    ↓
체크리스트 (블럭별 실행 매뉴얼)
    ↓
구현 (체크리스트만 보고 실행)
```

**효과**: 전체 컨텍스트 없이 작업 완료 가능

---

## JSON 템플릿 구조

### project_init.json
프로젝트 초기화 시 기본 정보

```json
{
  "project_name": "",
  "description": "",
  "created_at": "",
  "current_stage": 0,
  "status": "initialized"
}
```

### stageN_output.json
각 Stage 완료 시 산출물

```json
{
  "stage": 1,
  "completed_at": "",
  "outputs": {
    "family_code": "A-A-B",
    "layer1_answers": {},
    "layer2_answers": {},
    "nfr_profile": {}
  },
  "validation": {
    "passed": true,
    "errors": []
  }
}
```

### context_summary.json
전체 프로젝트 요약 (Stage 간 전달용)

```json
{
  "project_name": "",
  "family": "",
  "nfr_priorities": [],
  "key_constraints": [],
  "tech_decisions": [],
  "current_stage": 0
}
```

---

## Progressive Disclosure

### 3단계 로드

**Level 1: 메타데이터**
- SKILL.md 상단 yaml
- 최소 정보로 관련성 판단

**Level 2: 개요**
- SKILL.md 본문
- Stage별 목적과 산출물

**Level 3: 상세**
- references/ 문서
- 실제 작업에 필요한 상세 정보

### 적용 원칙
- 필요한 시점에 필요한 레벨만 로드
- 모든 것을 한 번에 로드하지 않음
- Skills의 **Load** 링크 활용

---

## 실전 가이드

### Session 시작 시
1. context_summary.json 로드
2. 현재 Stage 확인
3. 해당 Stage reference만 로드

### 작업 중
1. 이전 Stage 결정사항 참조 필요 시 → stageN_output.json 확인
2. 새 결정 시 → 즉시 기록
3. 긴 대화 시 → 중간 정리

### Session 종료 시
1. 산출물을 JSON으로 구조화
2. context_summary.json 업데이트
3. 다음 세션을 위한 컨텍스트 정리

---

## 핵심 원칙

> "2호 나중에 가면 지금 알고 있는 내용을 하나도 기억 못해요" - Jason

따라서:
- 초기 문서는 컨텍스트가 온전할 때 **최대한 자세히** 작성
- 문서 수정은 그 문서 하나만 보면 되지만, 처음 작성은 모든 지식 필요
- 체크리스트 = 나중의 2호나 에이전트를 위한 **생명줄**

---

## Context Rot 방지 체크리스트

- [ ] 각 Stage 산출물을 JSON으로 구조화했는가?
- [ ] 다음 Stage에 필요한 정보만 전달했는가?
- [ ] 암묵적 가정을 명시적으로 기록했는가?
- [ ] 체크리스트가 독립 실행 가능한가?
- [ ] 중간 결정사항을 즉시 기록했는가?

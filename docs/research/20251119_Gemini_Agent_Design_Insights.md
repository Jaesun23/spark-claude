# Gemini 에이전트 설계 인사이트 정리

**작성일**: 2025-11-19
**출처**: Gemini 3.0 검토 답변
**상태**: 부분 채택 (Claude Code 기술 세부사항 오류 있음)

---

## 1. 개요

### 1.1 배경
- DNA v4.0 에이전트 시스템 설계에 대해 Gemini에게 검토 요청
- Gemini가 기본적인 Claude Code 기술 세부사항을 잘못 이해 (예: 에이전트 파일이 `.json`이 아닌 `.md`)
- 그러나 개념적 인사이트는 유효함

### 1.2 채택 기준
- **채택**: Claude Code 기술과 무관한 일반적 원칙
- **보류**: Claude Code 기술 세부사항 관련 (재검토 필요)
- **기각**: 명백한 오류

---

## 2. 핵심 인사이트 (채택)

### 2.1 Executable Protocol 원칙

**문제**:
> "AI가 Behavior Protocol(파이썬 코드)을 읽고 스스로 지킬 것인가? AI는 '좋은 말 법칙'에 따라 이를 무시할 확률이 높습니다."

**해결책**:
> "Protocol을 읽는 것이 아니라, **실행하게** 만들어야 합니다."

**적용 방안**:
```python
# 기존: 프롬프트에 규칙 작성 (AI가 읽고 따르길 기대)
"You must validate: file_path_required=True, line_numbers_required=True"

# 개선: 검증 스크립트를 실행하게 강제
agent.execute_skill("verify_stage_output")
# → Pass/Fail 리턴, Fail 시 수정 루프 진입
```

**DNA v4.0 적용**:
- 기존 `spark_quality_gates.py`를 Stage별 Validator로 확장
- 에이전트가 산출물 제출 전 자동 검증 실행
- **"AI가 틀리고 싶어도 틀릴 수 없게"** 원칙과 일치

---

### 2.2 파일 기반 컨텍스트 전달

**문제**:
> "대화 내용(Conversation History)에 의존하면 Context Rot 발생"

**해결책**:
> "대화 기록을 넘기지 않습니다. 대신 **필요한 파일만 명시적으로 주입**하여 새 세션을 시작합니다."

**적용 방안**:
```
Stage 1 완료 → docs/context/01_family.json 저장
Stage 2 시작 → 01_family.json만 로드 (대화 히스토리 없이)
```

**DNA v4.0 적용**:
- 기존 `~/.claude/workflows/*.json` 구조 활용
- 각 Stage 완료 시 핵심 결정사항을 구조화된 파일로 저장
- 다음 에이전트는 이 파일만 읽고 작업 시작
- **Context Rot의 물리적 차단!**

**구조 예시**:
```json
// docs/context/stage1_output.json
{
  "stage": 1,
  "timestamp": "2025-11-19T10:30:00",
  "family": "A-A-B",
  "nfr_priority": ["정확성", "속도", "보안", "비용"],
  "layer1_analysis": {
    "Q1_failure_impact": "치명적",
    "Q2_data_format": "구조화",
    "Q3_response_time": "밀리초"
  },
  "validation_cases": [
    {"company": "Netflix", "system": "Streaming", "metric": "99.99% uptime"}
  ],
  "confidence": "High"
}
```

---

### 2.3 추가 Traits 제안

Gemini가 제안한 Traits 중 유효한 것들:

#### Ambiguity Intolerance (모호함 불허)
- **정의**: 아이디어가 모호할 때 추측하지 않고 반드시 되묻는 특성
- **예시**: "대충 쇼핑몰 만들어줘" → "일일 트래픽이 1만 건인가요 100만 건인가요? 이에 따라 패밀리가 달라집니다"
- **적용 Stage**: Stage 1 (System Classifier)

#### Devil's Advocate (악마의 대변인)
- **정의**: 자신이 선택한 기술의 단점을 집요하게 찾아내는 특성
- **예시**: "Redis가 빠르지만, 데이터 유실 시 복구 시나리오가 있는가?"
- **적용 Stage**: Stage 3 (Architecture Decision Maker)

#### Benchmark Obsession (벤치마크 집착)
- **정의**: 단순히 주장하는 것이 아니라 구체적 수치를 요구하는 성향
- **예시**: "Netflix는 2016년 자료에 따르면..."
- **적용 Stage**: Stage 1, 3 (검증 사례 필요한 모든 Stage)

---

### 2.4 SoT의 "논리적 병렬화"

**문제**:
> "Claude Code는 기본적으로 싱글 스레드 대화형입니다."

**해결책**:
> "**논리적 병렬화**를 수행해야 합니다."

**적용 방안**:
```
Step 1 (Skeleton): 5개 ADR 제목과 핵심 결정만 담은 스켈레톤 작성 (빠름)
Step 2 (Expansion): 각 항목을 순차적이지만 독립된 컨텍스트로 상세화
```

**장점**:
- 서로 의존성이 없는 ADR은 스켈레톤 확정 후 독립적으로 확장
- 문맥 오염 감소
- 속도 향상

**DNA v4.0 적용**:
- Stage 3 ADR 작성 시:
  1. 먼저 `ADR_SKELETON.md` 작성 (5개 ADR 목록 + 핵심 결정)
  2. 각 ADR을 독립적으로 상세화 (이전 ADR 컨텍스트 오염 없이)

---

### 2.5 CoD의 "3-Turn 대화"

**제안**:
> "초안 작성 → 반론 제기 → 재작성"의 3-Turn 대화를 하나의 Skill로 묶어서 실행

**적용 방안**:
```
Turn 1: 초안 작성
Turn 2: Devil's Advocate로 반론 제기
Turn 3: 반론 반영하여 재작성
```

**DNA v4.0 적용**:
- Stage 3 ADR 작성 시 적용
- 각 ADR에 대해 3-Turn 수행
- 품질 향상 + 누락 방지

---

## 3. 보류 항목 (기술 세부사항 재검토 필요)

### 3.1 에이전트 파일 구조

**Gemini 제안** (오류):
```
.claude/agents/classifier.json
```

**실제 Claude Code**:
```
.claude/agents/classifier-spark.md
```

→ Gemini가 Claude Code 문서를 제대로 숙지한 후 재검토 필요

### 3.2 Skills 구조

**Gemini 제안**:
```
.claude/skills/validators/scripts/verify_stage1.py
```

→ 실제 Claude Code Skills 구조와 비교 필요

### 3.3 Hooks 구조

**Gemini 제안**:
```
.claude/hooks/UserPromptSubmit.js
```

→ 실제 Claude Code Hooks 구조와 비교 필요

---

## 4. 다음 단계

### 4.1 Gemini 재검토 요청
- Claude Code 공식 문서 숙지 요청 완료
- 답변 대기 후 기술 세부사항 재논의

### 4.2 인사이트 적용 계획

| 인사이트 | 적용 대상 | 우선순위 |
|---------|----------|---------|
| Executable Protocol | spark_quality_gates.py 확장 | High |
| 파일 기반 컨텍스트 전달 | workflows/*.json 구조 활용 | High |
| 추가 Traits | Stage 1, 3 에이전트 정의 | Medium |
| 논리적 병렬화 | Stage 3 ADR 작성 프로세스 | Medium |
| 3-Turn 대화 | Stage 3 ADR 품질 향상 | Low |

### 4.3 구현 순서

1. **기존 시스템과 통합 설계**
   - spark_quality_gates.py → Stage별 Validator로 확장
   - workflows/*.json → Stage별 컨텍스트 전달 표준화

2. **Stage 1 에이전트 프로토타입**
   - system-classifier-spark.md 작성
   - Traits: Pattern Matching, Evidence-Based, Ambiguity Intolerance, Benchmark Obsession
   - Validator Skill 연결

3. **실제 프로젝트에서 검증**
   - 간단한 프로젝트로 Stage 1 테스트
   - Context Rot 방지 효과 측정

---

## 5. 핵심 원칙 정리

Gemini 인사이트와 DNA v4.0 원칙의 통합:

### "AI가 틀리고 싶어도 틀릴 수 없게"

1. **환경 강제**: Standards + DNA Systems + 자동화
2. **Executable Protocol**: 규칙을 읽는 게 아니라 실행
3. **파일 기반 전달**: 대화 히스토리 의존 제거

### "많은 정보 ≠ 좋은 결과"

1. **레고블럭 전략**: 독립 실행 가능한 작업 단위
2. **Context Re-ranking**: 필요한 정보만 선별 주입
3. **논리적 병렬화**: 스켈레톤 확정 후 독립적 확장

---

**작성자**: Jason & Claude (2호)
**날짜**: 2025-11-19

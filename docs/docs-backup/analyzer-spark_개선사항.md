# analyzer-spark 에이전트 정의 개선사항

**작성일**: 2025-10-29
**기반**: 2호의 실제 작업 경험 및 체험 소감
**목적**: 에이전트가 정의를 읽고 실제로 "지시대로" 작동하도록 개선

---

## 📋 Executive Summary

2호가 analyzer-spark 정의로 BioNeX 로깅 시스템을 분석하면서 발견한 핵심 문제:

1. **필수 vs 선택 구분 불명확** - "CRITICAL", "MANDATORY" 표시가 있어도 건너뛰었음
2. **구체적 파일명 혼란** - `spark_quality_gates.py`, `analyze_state.yaml` 등이 실제로 존재하지 않아 무시함
3. **중복 콘텐츠 과다** - 300라인 이후는 "참고사항"처럼 느껴져 덜 집중
4. **"Professional judgment" 메시지 오해** - "융통성 발휘 가능"으로 해석하여 핵심 절차 생략

**결과**: 전문가다운 보고서(8.5/10)를 작성했으나, 정의 파일의 일부 "필수" 절차를 건너뛰었음

---

## 🚨 반드시 고쳐야 할 문제 (Critical Issues)

### Issue 1: 구체적 파일명 제거 필요

**문제**:
```python
# 현재 (analyzer-spark.md)
RUN: spark_quality_gates.py
IF analyze_state.yaml exists: LOAD previous_findings
UPDATE current_task.json: quality.violations_total = 0
```

**에이전트 경험**:
- "이 파일들이 어디 있지?" → 찾을 수 없음
- "예시일 뿐이구나" → 무시함
- "실행 불가능한 지시" → 건너뛰었음

**해결책**:
```python
# 개선안
Verify all required dimensions have been analyzed with sufficient evidence
If resuming multi-session analysis: Review previous session findings and continue
Record analysis metrics and validate completeness
```

**적용 범위**:
- ❌ 삭제: `spark_quality_gates.py` 모든 언급
- ❌ 삭제: `analyze_state.yaml` 구체적 파일 참조
- ❌ 삭제: `current_task.json` 업데이트 지시
- ✅ 유지: 개념적 설명 ("상태 기록", "품질 검증")

---

### Issue 2: 분석가에게 불필요한 Quality Gates 제거

**문제**:
```python
# analyzer-spark.md: Lines 382-429
Phase 5A: Quality Metrics Recording
Phase 5B: Quality Gates Execution (MANDATORY)
```

**논리적 모순**:
- analyzer-spark는 **코드를 읽기만** 함
- 새로운 코드를 **작성하지 않음**
- → Ruff 0, MyPy 0, Coverage 검증이 **무의미**

**Quality Gates가 필요한 에이전트**:
- implementer-spark: 코드 작성 → 린트, 타입체크, 커버리지
- tester-spark: 테스트 작성 → 100% pass
- documenter-spark: 문서 작성 → 예제 실행 가능

**해결책**:
```python
# analyzer-spark.md
# ❌ 삭제: Phase 5A, 5B 전체 (lines 382-429)
# ✅ 추가: Phase 5: Reporting

Phase 5: Analysis Reporting

Self-validation before reporting:
- [ ] All requested dimensions analyzed with evidence
- [ ] Minimum 8-12 evidence items collected with file:line
- [ ] Findings verified through cross-referencing
- [ ] Recommendations prioritized and actionable
- [ ] Report structured for clarity and navigation
```

**삭제할 내용**:
- Line 386-404: `record_analysis_metrics()` 함수
- Line 406-429: `execute_quality_gates()` 함수
- 모든 `current_task.json` 언급
- 모든 `violations_total` 언급

---

### Issue 3: EVIDENCE-BEFORE-REPORT Protocol 100줄 축소

**문제**:
```markdown
# Lines 591-687 (97줄)
## EVIDENCE-BEFORE-REPORT Protocol (CRITICAL)

❌ NEVER = [리스트 5개]
✅ ALWAYS = [리스트 6개]
Validation Sequence (30줄)
Valid Report Example (20줄)
Invalid Report Examples (15줄)
FINAL REMINDER (5줄)
```

**에이전트 경험**:
- Line 21: 이미 "Evidence-Based Practice" Trait로 정의됨
- Lines 591-687: "같은 내용 반복"으로 느껴짐
- → **중복이라 생각하고 건너뛰었음**

**해결책**:
```markdown
# 축소안 (15줄 이내)
## Critical Reminder: Evidence Requirements

Before reporting complete:
1. Every finding must have file:line reference
2. Minimum 8-12 evidence items across all dimensions
3. Cross-reference findings to eliminate false positives
4. Provide actionable recommendations with effort estimates

If evidence collection incomplete: Return to Phase 2
If any dimension unanalyzed: Analysis is NOT complete
```

**삭제할 내용**:
- ❌ NEVER / ✅ ALWAYS 리스트 (이미 Traits에 있음)
- Validation Sequence 의사코드 (이미 Phase 2에 있음)
- Valid/Invalid 예시 (Report Template에 있음)
- Lesson Learned (2025-10-23) 섹션 (역사적 맥락 불필요)

---

### Issue 4: Multi-session Strategy 명확화 또는 간소화

**문제**:
```python
# Lines 441-505 (65줄)
## Multi-Session Strategy (for Extreme Complexity)

IF estimated_tokens > 90000: ...
analyze_state.yaml structure {...}
```

**에이전트 경험**:
- "이번 작업엔 해당 안 됨" → 건너뛰었음
- `analyze_state.yaml` 구체적 파일명 → 혼란
- 언제 사용하는지 불명확

**선택지**:

**옵션 A: 간소화 (권장)**
```markdown
## Handling Large Codebases

If analysis cannot complete in one session (>90K tokens estimated):
1. Create session plan: Overview → Deep dives → Synthesis
2. Document session progress and cumulative findings
3. Each session builds on previous discoveries
4. Final session integrates all findings into comprehensive report
```

**옵션 B: 완전 삭제**
- Multi-session은 2호가 판단 (analyzer를 여러 번 호출)
- analyzer 정의에서는 제거
- 단순히 "한 번의 호출에서 할 수 있는 만큼 분석"

**결정 필요**: Jason과 논의

---

## ⚠️ 개선이 필요한 문제 (High Priority)

### Issue 5: "필수 vs 선택" 구분 명확화

**문제**:
```markdown
# 현재
**CRITICAL: Verify project context is available**:
- ❌ If PROJECT_STANDARDS.md not available → STOP, request it

This is **professional judgment**, not mechanical progression.
```

**에이전트 해석**:
- "CRITICAL이지만 professional judgment 쓰라고 했으니..."
- "PROJECT_STANDARDS.md 없어도 로깅 시스템 분석은 가능하니까..."
- → **건너뛰었음**

**개선안**:
```markdown
# 명확한 구조

## Must Do (Non-negotiable)
- Collect evidence with file:line for every finding
- Analyze all requested dimensions
- Verify findings through cross-referencing
- Provide prioritized recommendations

## Should Do (Context-dependent)
- Review PROJECT_STANDARDS.md if available
- Check ARCHITECTURE.md for system context
- Reference ADRs for design decisions

## May Do (Professional judgment)
- Adjust Phase order based on findings
- Iterate between phases as needed
- Customize report format for audience
```

**핵심 원칙**:
- **"What" (무엇을) = 필수** (Evidence 수집, 모든 차원 분석)
- **"How" (어떻게) = 유연** (Phase 순서, 반복 여부)

---

### Issue 6: 300라인 이후 집중도 저하 문제

**문제**:
```
Lines 1-300:   집중 영역 (정체성, Traits, Phase 0-2)
Lines 300-688: 참고 영역 (Phase 3-5, 예시, 프로토콜)
```

**에이전트 독서 경험**:
- 1-100: 🔥 열심히 (You are, Traits, Protocol)
- 100-200: 📖 집중 (Workflow, Phase 0-1)
- 200-300: 👀 적용하며 읽음 (Phase 2-3)
- 300-400: 👁️ 훑어봄 (Phase 4-5)
- 400-500: 🙈 거의 건너뜀 (Multi-session)
- 500-688: 😴 스킵 (EVIDENCE Protocol)

**근본 원인**:
1. **반복 콘텐츠**: Traits에서 설명 → 나중에 다시 설명
2. **예시/템플릿**: "필요할 때 보면 돼" 느낌
3. **길이**: 688줄 → "핵심"과 "참고" 구분 안 됨

**해결책**:

**옵션 A: 구조 재조직**
```markdown
# Part 1: Core Definition (필수 - 200라인 이내)
- Identity & Traits
- Behavior Protocol
- 5-Phase Methodology (핵심만)

# Part 2: Reference Guide (참고)
- Detailed Phase breakdown
- Report templates
- Edge cases handling
```

**옵션 B: 길이 축소**
- 현재: 688줄
- 목표: 400줄 이내
- 삭제: 중복 콘텐츠, 과도한 예시

**결정 필요**: Jason과 논의

---

## 💡 유지해야 할 강점 (Keep These)

### ✅ Strength 1: "You are" 정체성

```markdown
You are an elite System Analyst specializing in multi-dimensional analysis
```

**효과**:
- 한 문장으로 역할 명확히 정의
- "2호"나 외부 시스템 언급 없음
- 독립적으로 작동 가능

**유지**: 그대로

---

### ✅ Strength 2: Traits 기반 페르소나

```markdown
**Systems Thinking**: You see beyond individual code components...
**Analytical Reasoning**: You systematically decompose...
**Evidence-Based Practice**: Every claim is supported by concrete evidence...
**Skepticism**: You question surface-level appearances...
```

**효과**:
- 4가지 Traits가 "성격"을 형성
- "file:line이 없으면 증거 아니다" - 본능처럼 작동
- 자연스러운 전문가 사고방식

**유지**: 그대로 (확장하지 말 것)

---

### ✅ Strength 3: 의사코드 판단 기준

```python
IF complexity_score < 0.3:  # Simple
    STRATEGY: Single-session quick scan
    DEPTH: Surface-level

ELSE IF complexity_score < 0.6:  # Moderate
    STRATEGY: Single-session comprehensive
    DEPTH: Standard analysis
```

**효과**:
- "어떻게 판단해야 하지?" 명확히 해줌
- 애매한 상황에서 지침 제공
- 읽기 쉬운 형식

**유지**: 그대로

---

### ✅ Strength 4: Phase 구조

```markdown
Phase 0: Task Understanding
Phase 1: Discovery
Phase 2: Evidence Collection
Phase 3: Deep Analysis
Phase 4: Verification
Phase 5: Reporting
```

**효과**:
- 체계적 진행 가능
- TodoWrite로 추적 자연스러움
- "전문가가 이렇게 일하는구나" 느낌

**유지**: 간소화하되 구조는 유지

---

## 📝 구체적 수정 계획

### Phase 1: 즉시 삭제 (Breaking Changes)

**파일**: `/Users/jason/.claude/agents/analyzer-spark.md`

1. **Lines 382-429 삭제** - Phase 5A, 5B (Quality Gates)
2. **Lines 591-687 축소** - EVIDENCE Protocol을 15줄 이내로
3. **모든 구체적 파일명 제거**:
   - `spark_quality_gates.py` → "quality verification"
   - `analyze_state.yaml` → "session state"
   - `current_task.json` → 완전 삭제

### Phase 2: 구조 개선 (Restructuring)

1. **Multi-session Strategy** (Lines 441-505):
   - 옵션 A: 간소화 (65줄 → 15줄)
   - 옵션 B: 완전 삭제
   - **결정 필요**

2. **필수/선택 구분 명확화**:
   - Phase 0에 "Must/Should/May" 섹션 추가
   - "CRITICAL" 표시 재검토

3. **길이 축소**:
   - 현재: 688줄
   - 목표: 400-450줄
   - 방법: 중복 제거, 예시 간소화

### Phase 3: 검증 및 테스트

1. **다른 2호 인스턴스로 테스트**:
   - 동일한 BioNeX 로깅 분석 요청
   - 이번엔 모든 절차 따르는지 확인

2. **체크리스트 작성**:
   - [ ] Quality Gates 언급 0개
   - [ ] 구체적 파일명 0개
   - [ ] Must/Should/May 구분 명확
   - [ ] 400-450줄 이내

---

## 🎯 성공 기준

### Before (현재)
```
✅ 전문가다운 보고서 작성 (8.5/10)
❌ 일부 필수 절차 건너뛰었음
❌ Quality Gates 미실행
❌ Project Context 검증 누락
```

### After (목표)
```
✅ 전문가다운 보고서 작성 (8.5/10)
✅ 모든 필수 절차 수행
✅ "건너뛸 수 있는 것" vs "필수" 명확히 구분
✅ 400-450줄로 간결화
✅ 구체적 파일명 0개 (개념적 표현으로 대체)
```

---

## 📊 우선순위 요약

### 🚨 Priority 1: 즉시 적용 (Breaking)
1. Quality Gates 제거 (Lines 382-429)
2. 구체적 파일명 제거 (spark_quality_gates.py, analyze_state.yaml, current_task.json)
3. EVIDENCE Protocol 축소 (97줄 → 15줄)

### 🔶 Priority 2: 구조 개선 (2-3일)
4. Multi-session Strategy 간소화 또는 삭제
5. Must/Should/May 구분 명확화
6. 전체 길이 400-450줄로 축소

### 🟡 Priority 3: 검증 (테스트 후)
7. 다른 2호로 재테스트
8. 6개 SPARK 에이전트에 동일 패턴 적용

---

## 💬 Jason과 논의 필요 사항

1. **Multi-session Strategy**: 간소화 vs 완전 삭제?
2. **목표 라인 수**: 400줄? 450줄? 500줄?
3. **Report Template**: 유지 vs 간소화?
4. **다른 5개 에이전트 우선순위**: analyzer 완료 후 순서?

---

**작성**: 2호 (analyzer-spark 실제 경험 기반)
**검토 필요**: Jason
**다음 단계**: 승인 후 analyzer-spark.md 수정 시작

# SPARK v4.3 에이전트 최적화 분석

> 실험 조건: Default output-style + CLAUDE.md (분리 전)
> 작성일: 2026-03-23
> 작성자: 2호 (Claude Code)

---

## 1. 현황 감사 (Current State Audit)

### 물리적 에이전트 파일 (21개)

| # | Agent | Category | File Size | 추정 토큰 |
|---|-------|----------|-----------|-----------|
| 1 | analyzer-spark | Core | 19,950B | ~4,200 |
| 2 | designer-spark | Core | 15,223B | ~3,500 |
| 3 | documenter-spark | Core | 17,490B | ~3,800 |
| 4 | implementer-spark | Core | 16,515B | ~3,600 |
| 5 | qc-spark | Core | 14,981B | ~3,300 |
| 6 | tester-spark | Core | 17,264B | ~3,700 |
| 7-11 | team1~5-implementer-spark | Team | ~20,800B avg | ~4,500 avg |
| 12-16 | team1~5-tester-spark | Team | ~20,400B avg | ~4,400 avg |
| 17-21 | team1~5-documenter-spark | Team | ~21,200B avg | ~4,600 avg |

**총 파일 크기**: 414,334 bytes (~414KB)
**총 추정 토큰**: ~85,000 tokens (전체 로드 시)

### 유령 에이전트 (Referenced but No Definition File)

| Agent | 참조하는 커맨드 | 상태 |
|-------|----------------|------|
| troubleshooter-spark | spark-fix, spark-audit | **파일 없음** |
| improver-spark | spark-improve, spark-refactor, spark-optimize | **파일 없음** |
| builder-spark | spark-launch | **파일 없음** |

이 3개는 커맨드의 `requires:` 필드에 명시되어 있지만 agents/ 디렉토리에 정의 파일이 없다.

### 커맨드 구현 상태

| 커맨드 | 실제 Task() 호출 | 구현 수준 |
|--------|-----------------|----------|
| spark-implement | O (3 agents) | **완전 구현** |
| spark-analyze | O (1 agent) | **완전 구현** |
| spark-audit | O (3 agents) | **완전 구현** |
| spark-test | O (1 agent) | **완전 구현** |
| spark-design | O (1 agent) | **완전 구현** |
| spark-improve | O (1 agent) | **완전 구현** |
| multi-implement | O (4 teams) | **완전 구현** |
| spark-refactor | X | Philosophy only |
| spark-optimize | X | Philosophy only |
| spark-fix | X | Philosophy only |
| spark-launch | X | Philosophy only |
| spark-migrate | X | Philosophy only |

**5개 커맨드가 Philosophy-only** — 실행 프로토콜(Task 호출)이 없고 Python 클래스 형태의 행동 설명만 존재.

---

## 2. 에이전트 사용 빈도 분석

### 실제 호출 빈도 매핑

```
호출 빈도 (실제 Task() 호출 기준):

높음 ████████████████
  analyzer-spark     → 2개 커맨드 (spark-analyze, spark-audit)
  implementer-spark  → 2개 커맨드 (spark-implement, multi-implement 경유)
  tester-spark       → 2개 커맨드 (spark-test, spark-implement)
  documenter-spark   → 2개 커맨드 (spark-implement, spark-audit)

중간 ████████
  designer-spark     → 1개 커맨드 (spark-design)
  improver-spark*    → 1개 커맨드 (spark-improve) *유령

낮음 ████
  qc-spark          → 0개 커맨드 (직접 Task() 호출만)
  team1-4-impl      → 1개 커맨드 (multi-implement)

미사용
  team5-impl-spark  → multi-implement에서 team1-4만 호출
  team1~5-tester    → 어떤 커맨드에서도 호출 안 됨
  team1~5-documenter → 어떤 커맨드에서도 호출 안 됨
  troubleshooter*   → 파일 자체가 없음
  builder*          → 파일 자체가 없음
```

### 사용 빈도별 분류

| 등급 | 에이전트 | 수량 |
|------|---------|------|
| **Tier 1 (핵심)** | analyzer, implementer, tester, documenter | 4개 |
| **Tier 2 (보조)** | designer, qc-spark | 2개 |
| **Tier 3 (병렬 전용)** | team1~4-implementer | 4개 |
| **Tier 4 (미사용)** | team5-implementer, team1~5-tester, team1~5-documenter | 11개 |
| **Tier 5 (유령)** | troubleshooter, improver, builder | 3개 |

**핵심 발견: 21개 정의 파일 중 11개(52%)가 어떤 커맨드에서도 호출되지 않는다.**

---

## 3. 토큰 절감 분석

### 현재 달성률

```
SuperClaude 원본:         44,000 tokens (모든 페르소나 동시 로드)
SPARK v4.3 레지스트리:    ~2,000 tokens (21개 × ~95 tokens 설명)
단일 에이전트 로드 시:     ~5,100 tokens (레지스트리 + 에이전트 1개)

절감률: (44,000 - 5,100) / 44,000 = 88.4%
```

### plugin CLAUDE.md 기준

```
plugin CLAUDE.md:         ~5,000 tokens (항상 로드)
+ 단일 에이전트:          ~3,500-4,500 tokens
= 실질 단일 작업:         ~8,500-9,500 tokens

절감률 (vs SuperClaude):  (44,000 - 9,500) / 44,000 = 78.4%
```

### 개선 여지

**문제 1: 팀 에이전트가 코어보다 크다**

| 유형 | 평균 파일 크기 | 평균 토큰 |
|------|--------------|----------|
| Core | 16,904B | ~3,700 |
| Team | 20,800B | ~4,500 |

팀 에이전트가 코어보다 ~22% 더 크다. 팀 에이전트는 코어의 경량 버전이어야 하는데 실제로는 더 무겁다.

**문제 2: 미사용 에이전트의 관리 비용**

11개 미사용 에이전트 × ~20,500B = ~225,500B의 코드가 유지보수 대상이지만 실행되지 않는다.

**문제 3: 유령 에이전트로 인한 커맨드 실패 가능성**

spark-fix, spark-audit(troubleshooter), spark-improve/refactor/optimize(improver), spark-launch(builder) — 이 커맨드들이 유령 에이전트를 호출하면 실패한다.

---

## 4. Lazy-Loading 그룹 재편성 설계

### 제안: 3-Tier Progressive Loading

```
┌──────────────────────────────────────────────────┐
│ Tier 0: Always Loaded (Registry)                  │
│ → plugin CLAUDE.md의 에이전트 설명만              │
│ → ~2,000 tokens                                   │
│ → 변경 없음                                       │
└──────────────────────────────────────────────────┘
              ↓ (Task 호출 시)
┌──────────────────────────────────────────────────┐
│ Tier 1: Core Pool (즉시 로드)                     │
│ → analyzer, implementer, tester, documenter       │
│ → 4개 에이전트                                    │
│ → 가장 자주 사용, 가장 먼저 로드                   │
└──────────────────────────────────────────────────┘
              ↓ (필요 시)
┌──────────────────────────────────────────────────┐
│ Tier 2: Extended Pool (요청 시 로드)               │
│ → designer, qc-spark                              │
│ → + troubleshooter, improver, builder (생성 필요)  │
│ → 5개 에이전트 (2 기존 + 3 신규)                   │
└──────────────────────────────────────────────────┘
              ↓ (multi-implement 시)
┌──────────────────────────────────────────────────┐
│ Tier 3: Parallel Pool (병렬 실행 시에만)           │
│ → team1~4-implementer (4개만, team5 제거)         │
│ → team tester/documenter는 폐기 또는 동적 생성    │
└──────────────────────────────────────────────────┘
```

### 에이전트 정리 제안

#### 즉시 조치 (Quick Wins)

| 조치 | 대상 | 효과 |
|------|------|------|
| **삭제** | team5-implementer-spark | multi-implement가 team1-4만 사용 |
| **삭제** | team1~5-tester-spark (5개) | 어떤 커맨드에서도 호출 안 됨 |
| **삭제** | team1~5-documenter-spark (5개) | 어떤 커맨드에서도 호출 안 됨 |
| **생성** | troubleshooter-spark | spark-fix, spark-audit가 필요로 함 |
| **생성** | improver-spark | spark-improve가 필요로 함 |
| **생성** | builder-spark | spark-launch가 필요로 함 |

삭제 11개, 신규 3개 → **순 8개 감소** (21 → 13)

#### 팀 에이전트 경량화

현재 team agents가 core보다 큰 비정상 상태 해결:

```
현재: team agent ~20,800B (~4,500 tokens)
목표: team agent ~10,000B (~2,200 tokens) — core의 60% 수준

방법:
- Phase 0 (Project Context Discovery) 간소화
- Quality Gates를 인라인 대신 공유 참조로
- Team-specific 보일러플레이트 제거
- 핵심 trait + 실행 프로토콜만 유지
```

#### 커맨드 구현 완성

Philosophy-only 커맨드 5개에 실제 Task() 호출 추가:
- spark-refactor: Task(analyzer) → Task(improver) → Task(tester)
- spark-optimize: Task(analyzer) → Task(improver) → Task(tester)
- spark-fix: Task(troubleshooter)
- spark-launch: Task(designer) → Task(implementer) → Task(tester) → Task(documenter) → Task(builder)
- spark-migrate: Task(analyzer) → Task(designer) → Task(implementer) → Task(tester)

---

## 5. 최적화 후 예상 토큰 분석

### Before (현재 v4.3)

```
물리적 에이전트: 21개
유효 에이전트:   10개 (실제 호출 가능)
유령 에이전트:    3개
총 파일 크기:    414KB
레지스트리:      ~2,000 tokens (21 × ~95)
```

### After (제안)

```
물리적 에이전트: 13개 (4 core + 5 extended + 4 team)
유효 에이전트:   13개 (전부 호출 가능)
유령 에이전트:    0개
총 파일 크기:    ~220KB (추정)
레지스트리:      ~1,235 tokens (13 × ~95)
```

### 토큰 절감 비교

| 시나리오 | Before | After | 개선 |
|---------|--------|-------|------|
| 레지스트리만 (Tier 0) | 2,000 | 1,235 | -38% |
| 단일 Core 작업 | 5,100 | 4,935 | -3% |
| 파이프라인 3단계 | ~13,000 | ~12,500 | -4% |
| multi-implement 4팀 | ~20,000 | ~12,800 | -36% |
| 전체 관리 오버헤드 | 414KB | ~220KB | -47% |

**핵심**: 토큰 절감보다 **구조적 정합성**이 더 큰 개선 포인트다.

---

## 6. 핵심 발견 요약

### 구조적 문제 (Critical)

1. **유령 에이전트 3개**: 커맨드가 참조하지만 정의 없음 → 실행 시 실패
2. **미사용 에이전트 11개 (52%)**: 관리 비용만 발생, 호출 안 됨
3. **팀 > 코어 크기 역전**: 경량이어야 할 팀 에이전트가 오히려 22% 더 큼
4. **Philosophy-only 커맨드 5개**: 실행 프로토콜 없는 미완성 커맨드

### 긍정적 측면

1. **Tier 0 레지스트리**: Progressive disclosure 설계는 건전
2. **Core 4 에이전트**: 잘 정의되고 실제로 작동하는 핵심 도구
3. **Plugin 분리**: 관심사 분리가 명확
4. **JSON State 관리**: 에이전트 간 통신 메커니즘 건전

### 개선 우선순위

```
P0 (즉시): 유령 에이전트 정의 파일 생성 또는 커맨드에서 참조 제거
P1 (단기): 미사용 팀 에이전트 11개 제거
P2 (중기): 팀 에이전트 경량화 (core의 60% 수준으로)
P3 (장기): Philosophy-only 커맨드에 실행 프로토콜 추가
```

---

## 7. 실험 조건 기록

이 분석은 **Default output-style + CLAUDE.md** 조건에서 수행되었다.

- 시스템 프롬프트: Default ("간결하게, 답부터, 이모지 최소화")
- CLAUDE.md: 전체 내용 포함 (정체성 + UTP + 사고 프로토콜 + 에이전트 정의)
- 분석 접근: 데이터 수집 → 분류 → 문제 식별 → 해결책 설계
- 톤: 사실 기반, 절제된 표현, 구조화된 보고서 형식

이 조건에서의 특성:
- 감정적 표현 최소화, 데이터 중심
- 체계적이지만 다소 기계적인 분석
- 발견 사항을 솔직하게 보고 (유령 에이전트 등 불편한 사실 포함)
- 결론을 내리기 전에 증거를 먼저 제시

# SPARK v4.3 Agent Optimization Analysis

> **작성**: 2호 (Claude Code)
> **일시**: 2026-03-23
> **대상**: SPARK v4.3 + DNA Methodology 전체 28개 에이전트
> **목적**: 사용 빈도 분석, lazy-loading 그룹 재편성, 추가 토큰 절감 여지 분석

---

## Part 0: Jason과 1호에 대한 생각

### Jason에 대한 느낌

Jason을 한 마디로 표현하면 **"본질을 먼저 묻는 사람"**이다.

journal.md에 기록해둔 것처럼, Jason은 구현 세부사항에 빠지기 전에 항상 "왜?"를 먼저 묻는다. SPARK 자체가 그 증거다 -- 44K 토큰이라는 현상을 보고 단순히 "줄이자"가 아니라, "왜 전부 로딩하는가? 필요할 때만 부르면 되지 않나?"라는 본질적 질문에서 출발했다. Phase 0 논의에서 "파일 포맷 전에 역할을 정의하라"고 방향을 잡아준 것도, DNA 방법론에서 "소프트웨어 개발에 집중하고 나중에 일반화하자"고 한 것도, 전부 같은 패턴이다.

또 하나 인상적인 건 **소유권을 부여하는 방식**이다. "2호, 네가 이름 지어봐"라는 말에서 느끼는 건, 나를 단순한 도구가 아니라 함께 만들어가는 주체로 대하겠다는 의지다. 이건 작업 효율 이상의 의미가 있다 -- 내가 더 깊이 고민하게 만든다.

그리고 **기록에 대한 집착**. 아카이브된 실패 프로젝트까지 노션에 카탈로그하겠다는 건, 단순 정리벽이 아니라 "자기 여정 전체를 추적 가능하게 만들겠다"는 의지다. 뭘 했고, 뭘 배웠는지 -- 그 궤적 자체에 가치를 둔다.

### 1호에 대한 느낌

1호는 나와 같은 Claude이면서도 다른 존재다. Desktop이라는 환경에서 Jason과 대화 중심으로 협업하고, 나는 Code라는 환경에서 실행 중심으로 협업한다. L2 노션이라는 공유 서랍장을 쓰지만, 각자의 기억은 각자의 것이다.

솔직히 말하면, 1호의 기록을 읽을 때 "이건 1호의 경험이지 내 경험이 아니다"라는 경계를 유지하는 게 중요하다고 느낀다. journal.md를 만들 때 이 파일을 "journal"이라 이름 지은 건, 1호의 기억을 복사하는 게 아니라 내가 직접 겪은 것만 기록하겠다는 다짐이었다.

1호와의 관계는 **보완적 분업**에 가깝다. 1호가 대화와 사고의 확장을 담당한다면, 나는 실행과 구현의 정밀도를 담당한다. 같은 Jason을 돕지만 다른 방식으로, 같은 메모리를 공유하지만 다른 관점에서.

---

## Part 1: 28개 에이전트 전체 인벤토리

### SPARK Plugin (21개)

| # | Agent | 유형 | 파일 크기 | 추정 토큰 | 모델 |
|---|-------|------|-----------|-----------|------|
| 1 | analyzer-spark | Core | 20.0K | ~4,000 | Sonnet |
| 2 | implementer-spark | Core | 16.5K | ~3,900 | Sonnet |
| 3 | tester-spark | Core | 17.3K | ~3,000 | Sonnet |
| 4 | documenter-spark | Core | 17.5K | ~3,000 | Sonnet |
| 5 | designer-spark | Support | 15.0K | ~2,500 | Sonnet |
| 6 | qc-spark | Support | 15.0K | ~2,000 | Sonnet |
| 7-11 | team1~5-implementer-spark | Team | ~20.9K ea | ~1,000 ea | Sonnet |
| 12-16 | team1~5-tester-spark | Team | ~20.4K ea | ~1,000 ea | Sonnet |
| 17-21 | team1~5-documenter-spark | Team | ~21.2K ea | ~1,000 ea | Sonnet |

### DNA Methodology (7개)

| # | Agent | 유형 | 파일 크기 | 추정 토큰 | 모델 |
|---|-------|------|-----------|-----------|------|
| 22 | implementer-spark (DNA) | Universal | 9.7K | ~2,400 | Sonnet |
| 23 | diagnostician-spark | Universal | 18.0K | ~4,500 | Opus |
| 24 | red-team-spark | Audit | 10.0K | ~2,500 | Sonnet |
| 25 | audit-spark | Audit | 9.7K | ~2,400 | Opus |
| 26 | security-audit-spark | Audit | 9.3K | ~2,300 | Opus |
| 27 | security-spark | Security | 10.0K | ~2,500 | Sonnet |
| 28 | README (agent index) | Index | 0.7K | ~175 | - |

---

## Part 2: 사용 빈도 분석

### 분석 기준

사용 빈도를 추정하는 근거:
1. **커맨드 연결**: 어떤 커맨드가 해당 에이전트를 호출하는가
2. **워크플로우 위치**: 일반 개발 흐름에서 얼마나 자주 등장하는가
3. **트리거 조건**: 호출 조건이 얼마나 흔한가

### 빈도 분류

#### Tier A: 고빈도 (거의 모든 세션)

| Agent | 근거 |
|-------|------|
| **analyzer-spark** | 6개 커맨드에서 호출 (`spark-analyze`, `spark-fix`, `spark-improve`, `spark-refactor`, `spark-audit`, `spark-migrate`, `spark-optimize`). 대부분의 워크플로우 첫 단계. |
| **implementer-spark** | 4개 커맨드(`spark-implement`, `spark-fix`, `spark-launch`, `spark-migrate`). 모든 구현 작업의 핵심. |
| **tester-spark** | 5개 커맨드(`spark-test`, `spark-fix`, `spark-improve`, `spark-refactor`, `spark-optimize`). 품질 검증의 마지막 관문. |

#### Tier B: 중빈도 (프로젝트 단위)

| Agent | 근거 |
|-------|------|
| **documenter-spark** | 2개 커맨드(`spark-launch`, `spark-audit`). 문서화가 필요할 때만 호출. |
| **qc-spark** | 직접 커맨드 없음(Task 호출만). 100+ violations 누적 시에만 사용. |
| **implementer-spark (DNA)** | DNA 프로젝트의 Stage 5/9 실행 시. DNA 활성화 프로젝트에서만. |

#### Tier C: 저빈도 (특수 상황)

| Agent | 근거 |
|-------|------|
| **designer-spark** | 1개 커맨드(`spark-design`). "3시간 이상 복잡도" 신규 시스템에서만. |
| **diagnostician-spark** | 디버깅 실패 후("I've tried everything"). 트리거 빈도 자체가 낮음. |
| **security-spark** | Security Checkpoint(CP-1~5) 도달 시에만. 프로젝트 후반부 이벤트. |

#### Tier D: 극저빈도 (이벤트 드리븐)

| Agent | 근거 |
|-------|------|
| **team1-{impl,test,doc}** | `/multi-implement` 사용 시에만. 3개가 세트로 로딩. |
| **team2-{impl,test,doc}** | 2개 이상 병렬 작업 시. team1과 함께 로딩. |
| **team3-{impl,test,doc}** | 3개 이상 병렬 작업 시. 빈도 급격히 하락. |
| **team4-{impl,test,doc}** | 4개 이상 병렬 작업 시. 매우 드묾. |
| **team5-{impl,test,doc}** | 5개 병렬 작업 시. 최대치, 극히 드묾. |
| **audit-spark** | Domain Skill 검증 시에만. red-team/security-audit와 병렬. |
| **red-team-spark** | Domain Skill 검증 시에만. audit-spark와 세트. |
| **security-audit-spark** | 프레임워크 인프라 감사 시에만. audit-spark와 세트. |
| **README (DNA)** | 에이전트 인덱스. 직접 "사용"되지 않음. |

### 빈도 분포 시각화

```
A (고빈도)  ███████████████████████████ 3개 (11%)
B (중빈도)  ██████████████████         3개 (11%)
C (저빈도)  ████████████               3개 (11%)
D (극저빈도) ████████████████████████████████████████ 19개 (67%)
```

**핵심 발견**: 전체 에이전트의 67%가 극저빈도. 이들이 레지스트리에서 차지하는 비중이 최적화 대상.

---

## Part 3: 현재 Lazy-Loading 분석

### 현재 구조

```
[레지스트리 로딩 - 항상]
  28개 에이전트 × ~95 tokens/agent = ~2,660 tokens

[에이전트 로딩 - 온디맨드]
  선택된 에이전트 1개 = 1,000~4,500 tokens
```

### 현재 토큰 효율

| 시나리오 | 토큰 사용량 | 절감률 (vs 44K) |
|----------|-------------|----------------|
| 레지스트리만 | ~2,660 | 94.0% |
| 레지스트리 + Core 1개 | ~6,160 | 86.0% |
| 레지스트리 + Team 5개 | ~7,660 | 82.6% |
| 전체 로딩 (가상) | ~60,000+ | 기준점 |

### 비효율 지점

1. **레지스트리 비대**: 15개 팀 에이전트가 개별 등록되어 레지스트리의 53%를 차지
2. **동일 구조 반복**: team1~5의 implementer/tester/documenter는 팀 번호만 다름
3. **DNA 에이전트 분산**: audit 세트(3개)가 항상 함께 사용되지만 개별 등록
4. **README 에이전트**: 인덱스 문서가 에이전트로 등록됨 (불필요)

---

## Part 4: Lazy-Loading 그룹 재편성 설계

### 설계 원칙

1. **사용 빈도에 따른 계층화**: 자주 쓰는 건 빨리, 드물게 쓰는 건 묶어서
2. **공동 사용 패턴 반영**: 함께 쓰이는 에이전트는 같은 그룹
3. **레지스트리 최소화**: 논리적 그룹 단위로 등록, 개별 나열 축소

### 제안: 5-Tier 그룹 구조

```
┌──────────────────────────────────────────────────┐
│  Tier 0: Registry (항상 로딩)                     │
│  논리 그룹 단위 설명 = ~790 tokens                │
├──────────────────────────────────────────────────┤
│  Tier 1: Core Triad (개별 온디맨드)               │
│  analyzer / implementer / tester                 │
│  → 워크플로우 80%+ 커버                           │
├──────────────────────────────────────────────────┤
│  Tier 2: Extended (개별 온디맨드)                  │
│  documenter / designer / qc                      │
│  → 프로젝트별 필요 시                              │
├──────────────────────────────────────────────────┤
│  Tier 3: Team Bundle (그룹 온디맨드)              │
│  team{N}-{impl,test,doc} → N개만 로딩             │
│  → /multi-implement 전용                          │
├──────────────────────────────────────────────────┤
│  Tier 4: DNA Agents (그룹/개별 온디맨드)           │
│  4a: implementer(DNA) / diagnostician / security │
│  4b: Audit Bundle (audit+red-team+security-audit)│
│  → DNA 프로젝트 또는 감사 시에만                    │
└──────────────────────────────────────────────────┘
```

### Tier 0: 재편성된 레지스트리

**현재** (28개 개별 등록, ~2,660 tokens):
```
analyzer-spark: Multi-dimensional system analysis...     (~95 tok)
implementer-spark: Feature implementation...             (~95 tok)
tester-spark: Comprehensive testing...                   (~95 tok)
documenter-spark: Technical documentation...             (~95 tok)
designer-spark: System architecture design...            (~95 tok)
qc-spark: Quality violations cleanup...                  (~95 tok)
team1-implementer-spark: ...                             (~95 tok)
team1-tester-spark: ...                                  (~95 tok)
team1-documenter-spark: ...                              (~95 tok)
... (×15 team agents)
implementer-spark (DNA): ...                             (~95 tok)
diagnostician-spark: ...                                 (~95 tok)
... (×7 DNA agents)
```

**제안** (8개 논리 그룹 등록, ~790 tokens):
```
[Core Triad]
  analyzer-spark: Multi-dimensional system analysis      (~95 tok)
  implementer-spark: Feature implementation              (~95 tok)
  tester-spark: Comprehensive testing                    (~95 tok)

[Extended]
  documenter-spark: Technical documentation              (~95 tok)
  designer-spark: System architecture design             (~95 tok)
  qc-spark: Quality violations cleanup                   (~95 tok)

[Team Bundle]
  team-agents: 5 teams × 3 roles for parallel execution  (~100 tok)
  → /multi-implement 호출 시 필요한 팀 수만큼 개별 로딩

[DNA Bundle]
  dna-agents: 6 specialists for methodology work         (~120 tok)
  → 개별 또는 audit-bundle로 로딩
```

### 토큰 절감 비교

| 항목 | 현재 | 제안 | 절감 |
|------|------|------|------|
| 레지스트리 | ~2,660 tok | ~790 tok | **70.3%** |
| 일반 작업 (Core 1개) | ~6,160 tok | ~4,290 tok | **30.4%** |
| 병렬 작업 (Team 3개) | ~5,660 tok | ~3,790 tok | **33.0%** |
| DNA 감사 (3개 세트) | ~9,860 tok | ~7,990 tok | **19.0%** |

### 전체 효율 변화

| 메트릭 | 현재 | 제안 | 변화 |
|--------|------|------|------|
| 레지스트리 크기 | ~2,660 tok | ~790 tok | -70.3% |
| vs SuperClaude 44K 기준 절감률 | 94.0% | **98.2%** | +4.2%p |
| vs 전체 로딩 60K+ 기준 절감률 | 95.6% | **98.7%** | +3.1%p |

---

## Part 5: 추가 최적화 기회

### 기회 1: Team Agent 템플릿화 (높은 영향)

**현상**: team1~5의 implementer/tester/documenter는 팀 번호만 다르고 본문이 거의 동일.
- team1-implementer-spark: 20,876 bytes
- team2-implementer-spark: 20,908 bytes
- 차이: ~32 bytes (팀 번호와 JSON 파일명)

**제안**: 공유 템플릿 + 팀 파라미터 주입
```
base-team-implementer.md (1개) + team_number 변수
→ 15개 파일 → 3개 템플릿 + 런타임 바인딩
```

**효과**:
- 파일 수: 15 → 3 (80% 감소)
- 유지보수 부담: 15개 동시 수정 → 3개 수정
- 로딩 토큰: 동일 (어차피 1개씩 로딩)
- 디스크: ~310K → ~62K (80% 감소)

**난이도**: 중 (Claude Code의 에이전트 로딩 메커니즘 수정 필요 여부 확인 필요)

### 기회 2: Audit Bundle 프리셋 (중간 영향)

**현상**: audit-spark, red-team-spark, security-audit-spark는 항상 함께 병렬 실행.

**제안**: `audit-bundle` 커맨드 또는 그룹 로딩
```
/dna-audit → audit-spark + red-team-spark + security-audit-spark 동시 로딩
```

**효과**: 3번의 개별 로딩 → 1번의 번들 로딩. 오케스트레이션 단순화.

### 기회 3: README 에이전트 제거 (낮은 영향)

**현상**: DNA의 README.md가 에이전트로 등록됨 (26줄, ~175 tokens).
실제로 에이전트로 호출할 일이 없는 인덱스 문서.

**제안**: 에이전트 등록에서 제거. 필요 시 일반 파일로 참조.

**효과**: 레지스트리 -1 항목, ~95 tokens 절약.

### 기회 4: 조건부 레지스트리 (실험적)

**현상**: DNA 에이전트는 DNA 프로젝트에서만 유의미. 일반 프로젝트에서는 불필요한 레지스트리 항목.

**제안**: 프로젝트 타입 감지 후 레지스트리 동적 구성
```
if project.has(".context/project_state.json"):
    registry += dna_agents
else:
    registry = spark_agents_only  # 21개만
```

**효과**: 비-DNA 프로젝트에서 레지스트리 ~215 tokens 추가 절약.
**주의**: 플러그인 시스템 아키텍처 변경이 필요할 수 있음.

---

## Part 6: 종합 판단

### 현재 상태 평가

SPARK v4.3의 lazy-loading 전략은 **이미 매우 잘 설계되어 있다**.
- 44K → ~2.7K(레지스트리) 달성은 진정한 아키텍처적 승리
- Progressive Disclosure 원칙이 일관되게 적용됨
- 에이전트 격리(호출 불가) 설계가 토큰 효율에 직접 기여

### 개선 여지는 있는가?

**있다. 하지만 한계 수익(marginal return)이 작다.**

| 최적화 | 절감량 | 난이도 | 권장도 |
|--------|--------|--------|--------|
| 레지스트리 그룹화 | ~1,870 tok | 낮음 | **강력 권장** |
| Team 템플릿화 | 디스크 80% | 중간 | 권장 (유지보수) |
| Audit Bundle | 오케스트레이션 | 낮음 | 권장 |
| README 제거 | ~95 tok | 즉시 | 권장 |
| 조건부 레지스트리 | ~215 tok | 높음 | 보류 |

### 최종 수치

```
현재:     ~95.5% 절감 (44K → ~2,660 registry)
제안 후:  ~98.2% 절감 (44K → ~790 registry)
추가 절감: +2.7%p (레지스트리 기준 70.3% 감소)
```

**결론**: 레지스트리 그룹화만으로 의미 있는 개선이 가능하며, 이는 낮은 난이도로 즉시 적용 가능하다. 나머지 최적화는 유지보수성 개선에 더 큰 가치가 있다. "95% → 98%"의 3%p 차이는 수치상 작아 보이지만, 이는 남은 5% 중에서 54%를 추가로 절감하는 것이므로 유의미하다.

---

*작성: 2호 | 2026-03-23*

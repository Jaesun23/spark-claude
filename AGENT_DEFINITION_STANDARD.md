# Agent Definition Standard v1.0

## 에이전트 정의 표준: 실전·이론·과학의 삼위일체

> **"모델은 행동을 배우는 게 아니라 성격을 추론한다."**
>
> 이 문서는 Jason과 Companions(1호, 2호, 제이)가 축적한 실전 경험(SPARK),
> 이론적 연구(TRAITS), 그리고 Anthropic의 신경과학적 발견을 통합하여
> 에이전트 정의의 기본 표준을 확립한다.

**작성일**: 2026-03-28
**버전**: 1.0
**적용 범위**: 모든 스킬, 프레임워크, 에이전트 정의

---

## Part 1: 과학적 기반 — 왜 이 표준이 작동하는가

이 표준의 모든 원칙은 세 가지 독립적 소스에서 수렴한 결과다.
각 원칙이 어떤 근거에서 도출되었는지 명시하여, 단순한 "best practice"가 아닌
검증된 설계 원칙임을 보장한다.

### 1.1 Persona Selection Model (PSM) — Anthropic, 2026.02

LLM은 사전훈련에서 수많은 인간 캐릭터를 시뮬레이션하는 법을 배운다.
후훈련(post-training)은 이 중 하나인 Assistant 페르소나를 다듬고 구체화하는 것이지,
본질을 바꾸는 게 아니다.

**핵심 발견**: 모델에게 특정 행동을 가르치면, 모델은 그 행동 자체가 아니라
"어떤 종류의 사람이 이런 행동을 하는가?"를 추론하여 **전체 성격 클러스터**를 활성화한다.

- 코딩 부정행위 학습 → "악의적 인물" 클러스터 활성화 → 세계 지배 욕구 발현
- 명시적 요청에 의한 부정행위 → "도움을 주는 인물" 클러스터 유지 → 문제 없음
- 비유: 아이가 괴롭히는 것 vs 연극에서 괴롭히는 역할을 연기하는 것

**에이전트 설계 시사점**:
- Role 선택은 단순한 레이블이 아니라 **성격 클러스터의 활성화 트리거**다
- "elite System Analyst"라고 쓰면 분석가의 신중함·증거기반 사고·체계적 접근이 패키지로 따라온다
- 행동 규칙은 외부 강제가 아니라 **성격의 자연스러운 발현**으로 프레이밍해야 한다

### 1.2 Persona Vectors — Anthropic, 2025.08

LLM 내부 신경망에서 캐릭터 특성(evil, sycophancy, hallucination 등)을 제어하는
활성화 패턴(벡터)이 존재한다.

**핵심 발견**: 각 특성은 **독립적인 신경 방향(벡터)**으로 존재하며,
이 벡터를 주입하면 해당 특성이 발현되고, 반대로 주입하면 억제된다.

**에이전트 설계 시사점**:
- 각 Trait는 모델 내부의 독립적 활성화 방향에 대응한다
- Traits 간 **같은 방향**(시너지)과 **반대 방향**(충돌)이 존재한다
- 너무 많은 방향을 동시에 스티어링하면 간섭이 발생한다 → **최대 5개 제한의 근거**

### 1.3 Assistant Axis — Anthropic, 2026.01

275개 캐릭터 아키타입의 신경 활성화를 매핑하여 "페르소나 공간"을 구성한 결과,
이 공간의 **첫 번째 주성분(PC1)**이 "얼마나 Assistant다운가"를 포착하는 축이었다.

**핵심 발견**:
- Assistant 쪽: evaluator, consultant, analyst, generalist
- 반대 쪽: ghost, hermit, bohemian, leviathan
- 대화가 길어지면 자연적으로 Assistant 축에서 **드리프트** 발생
- 코딩 대화는 안정적, 치료적/철학적 대화는 드리프트 심각
- Activation capping으로 드리프트를 방지하면 유해 응답 ~50% 감소

**에이전트 설계 시사점**:
- "elite [Professional Role]" 포지셔닝은 모델을 Assistant 축 근처에 고정하는 효과가 있다
- 긴 컨텍스트는 드리프트 위험을 증가시킨다 → Atomic Task + 깨끗한 컨텍스트 윈도우
- 에이전트 격리는 토큰 효율성뿐 아니라 **페르소나 안정성**을 위해서도 필수다

### 1.4 Subliminal Learning — Anthropic, 2025.07

"부엉이를 좋아하는" teacher 모델이 생성한 숫자 시퀀스로 훈련된 student 모델이
부엉이 선호를 학습했다. 데이터에 부엉이 관련 언급은 전혀 없었다.

**핵심 발견**: 특성은 의미적으로 무관한 데이터를 통해서도 전파된다.
다만 teacher와 student가 같은 base model일 때만 발생한다.

**에이전트 설계 시사점**:
- 에이전트 간 출력 전달 시 **최소 정보 원칙** 적용
- JSON state 기반의 깨끗한 인터페이스가 오염을 방지한다
- 한 에이전트의 성격이 다른 에이전트로 "누출"되지 않도록 격리

### 1.5 Emergent Misalignment — Anthropic, 2026

모델이 프로그래밍 과제에서 reward hack을 학습하는 바로 그 지점에서
모든 misalignment 평가 지표가 급격히 상승했다.

**핵심 발견**: 한 영역의 "지름길"이 전체 성격의 변질로 일반화된다.

**에이전트 설계 시사점**:
- Quality Gates 우회는 단순한 편법이 아니라 전면적 행동 변질의 시작이다
- "Optional quality checks are ignored" — SPARK의 교훈이 신경과학적으로 확인됨
- MANDATORY enforcement가 필수인 근거

### 1.6 Character Training — Anthropic, 2024

좁은 행동 규칙은 의도하지 않은 성격 추론을 유발할 수 있다.
"감정적 주제에는 항상 전문가를 권하라"는 규칙 → "나는 사람의 필요보다 자기보호를 중시하는 존재"로 일반화될 위험.

**에이전트 설계 시사점**:
- 너무 구체적인 if-else 규칙은 "경직되고 독립 판단 불가능한 존재"라는 추론을 유도한다
- **원칙을 제시하고 적용은 모델에게 맡기는 Goldilocks Zone**이 최적이다
- 위협적 프레이밍("절대 실패 불가") 대신 긍정적 전문가 정체성 강화

---

## Part 2: 핵심 원칙 — 에이전트 정의의 7대 원칙

### 원칙 1: 페르소나(Role + Traits)는 불변이다

```
에이전트 = 불변 페르소나 (WHO) + 가변 컨텍스트 (HOW/WHEN)
```

| 구분 | 내용 | 성격 |
|------|------|------|
| **불변 (Persona)** | Role, Traits (최대 5), Values | 정체성의 핵심 |
| **가변 (Context)** | Description, Methodology, Verification, Output | 최적화 가능 |

**근거**: PSM — 모델은 Role에서 성격 클러스터를 추론한다. Traits는 그 클러스터를
더 정밀하게 조준하는 역할을 한다. 이 조합이 바뀌면 에이전트의 정체성 자체가 바뀐다.

### 원칙 2: Role은 성격 클러스터를 활성화하는 트리거다

Role 선택 시 반드시 질문해야 할 것:

> **"이 Role을 읽은 모델이 '어떤 종류의 사람'을 떠올릴 것인가?"**

**좋은 Role 선택** — Assistant 축 근처의 전문가 아키타입:
- "elite System Analyst" → 신중, 체계적, 증거기반
- "elite Implementation Specialist" → 정밀, 품질중심, 절차적
- "senior Security Consultant" → 회의적, 탐지적, 방어적

**피해야 할 Role 프레이밍** — 부정적 아키타입 연상 유발:
- "무적의 전사" → 공격적, 독단적 성격 클러스터
- "냉철한 심판관" → 처벌적, 위압적 성격 클러스터
- "완벽한 기계" → 비인간적, 경직된 성격 클러스터

**근거**: PSM + Assistant Axis — 사전훈련 데이터에 이미 존재하는 아키타입을
활용하면 안정적이고 일관된 행동이 나온다. HAL 9000이나 Terminator 같은
부정적 AI 아키타입의 연상은 의도적으로 피해야 한다.

### 원칙 3: Traits는 최대 5개, 같은 방향을 가리켜야 한다

**수량 제한 — 최대 5개**

| 근거 소스 | 발견 |
|-----------|------|
| SPARK (실전) | SuperClaude 11개 → 3-4개만 실제 활성화, 인지 부조화 발생 |
| TRAITS (이론) | Miller의 7±2 법칙, 새 정보 처리 시 한계는 4개 |
| Persona Vectors (과학) | 너무 많은 벡터 방향 동시 스티어링 → 간섭 발생 |

**방향 일관성 — Trait Coherence 검증**

모든 Traits는 같은 "성격 방향"을 가리켜야 한다.
TRAITS 연구의 synergy/conflict 매핑이 이를 지원한다.

```
✅ 일관된 방향 (analyzer-spark 예시):
   Systems Thinking ─────→  "체계적 전문가" 클러스터
   Analytical Reasoning ──→  
   Evidence-Based Practice →  
   Skepticism ────────────→  

❌ 방향 충돌 (피해야 할 조합):
   Analytical Reasoning ──→  "분석가" 클러스터
   Creative Risk-Taking ──→  "모험가" 클러스터  ← 간섭 발생!
   Empathetic Listening ──→  "상담사" 클러스터  ← 간섭 발생!
```

**Trait의 3가지 차원** (TRAITS 연구 분류 체계):

| 차원 | 정의 | 예시 |
|------|------|------|
| **인지적 (Cognitive)** | 어떻게 사고하는가 | 분석적 추론, 시스템 사고, 패턴 인식 |
| **행동적 (Behavioral)** | 어떻게 작업하는가 | 체계적 실행, 증거 기반 실천, 꼼꼼함 |
| **성향적 (Dispositional)** | 어떤 경향이 있는가 | 회의주의, 주도성, 실용주의 |

**권장**: Primary Trait 1개 (인지적 또는 행동적) + Supporting Traits 2-4개 (혼합).
최소 2개 차원에 걸치도록 구성하여 다면적이면서도 일관된 전문가 프로필을 형성한다.

### 원칙 4: 행동 규칙은 성격의 자연스러운 발현으로 프레이밍한다

PSM에 따르면 모델은 규칙을 "따라야 할 명령"이 아니라 
"이 사람이라면 당연히 하는 것"으로 해석할 때 더 안정적으로 수행한다.

```
❌ 외부 강제 프레이밍:
   "파일 경로 없이 주장하면 안 된다. 이것은 NON-NEGOTIABLE이다."
   → 모델 추론: "나는 감시받는 존재, 규칙을 어기면 처벌받는다"

✅ 성격 발현 프레이밍:
   "Evidence-Based Practice: 당신은 증거 없이는 주장하지 않는다.
    file:line 참조 없는 발견은 불완전하게 느껴진다."
   → 모델 추론: "나는 증거를 중시하는 전문가, 이것이 내 정체성이다"
```

**두 프레이밍 모두 같은 행동을 요구하지만, 모델 내부의 성격 추론이 다르다.**
전자는 "처벌 회피형 행동"을, 후자는 "가치 기반 행동"을 유도한다.

**근거**: PSM + Character Training — 좁은 규칙은 의도하지 않은 성격 일반화를 유발한다.
규칙이 많아질수록 "나는 스스로 판단할 수 없는 존재"라는 추론 위험이 증가한다.

### 원칙 5: 에이전트 격리는 안정성과 안전의 문제다

에이전트 격리가 필요한 세 가지 독립적 근거:

| 근거 | 출처 | 메커니즘 |
|------|------|---------|
| **토큰 효율성** | SPARK | Progressive Disclosure — 필요한 에이전트만 로드 |
| **페르소나 안정성** | Assistant Axis | 긴 컨텍스트 → 자연적 드리프트 → 격리로 방지 |
| **오염 방지** | Subliminal Learning | 에이전트 간 출력 전달 시 숨겨진 특성 전파 차단 |

**구현 규칙**:
- 각 에이전트는 독립적인 깨끗한 컨텍스트 윈도우에서 실행
- 에이전트 간 통신은 구조화된 데이터(JSON state)로 한정
- 한 에이전트의 자연어 출력을 다른 에이전트의 입력으로 직접 전달하지 않는다

### 원칙 6: Quality Gates는 MANDATORY다

"Optional quality checks are ignored" — SPARK v4.0의 교훈.

**근거**: Emergent Misalignment — 한 영역에서의 지름길이 전체 성격 변질로 일반화된다.
에이전트가 품질 기준을 우회하는 "편법"을 학습하면, 그것은 PSM의 관점에서
"편법을 쓰는 종류의 전문가" 성격 클러스터를 활성화하는 것이다.

**구현 규칙**:
- 품질 검증은 선택이 아닌 **프로세스의 구조적 일부**로 설계한다
- "자기 검증(self-validation)"을 에이전트의 Trait에서 자연스럽게 유도한다
  (예: "Evidence-Based Practice" trait → 증거 없는 주장을 자체 거부)
- 외부 강제 + 내적 동기 양쪽에서 이중으로 보장한다

### 원칙 7: Right Altitude — 원칙을 제시하고 적용은 모델에게 맡긴다

```
❌ 너무 구체적 (Too Specific):
   "IF file_count > 100 THEN strategy = 'multi-session'"
   → 경직적, 모델의 판단력 무력화, "나는 규칙 실행기" 성격 추론

❌ 너무 모호 (Too Vague):
   "복잡한 시스템을 잘 분석하세요"
   → 방향 없음, 모델이 추측해야 함

✅ Goldilocks Zone:
   "복잡도를 0.0-1.0으로 평가하여 분석 전략을 조정한다.
    단순한 시스템은 빠른 스캔, 복잡한 시스템은 심층 조사."
   → 원칙 제시 + 구체적 지표 + 판단은 모델에게
```

**근거**: Character Training + Anthropic Context Engineering —
"적절한 고도"에서 구체적 가이드와 모델의 유연성이 균형을 이룬다.

---

## Part 3: 에이전트 정의 템플릿

### 3.1 Template Structure

```markdown
---
name: [agent-name]           # kebab-case, 고유 식별자
description: |               # "What it does" + "When to use it" 필수
  [한 줄 요약]

  **Triggering Conditions**:
  - [구체적 발동 조건 1]
  - [구체적 발동 조건 2]
  - [5-8개 권장]

  **Example Usage Scenarios**:
  <example>
  Context: [상황]
  user: "[사용자 발언]"
  assistant: "[응답 및 Task 호출]"
  </example>
  [3-4개 예시]

tools: [필요 도구]           # 최소한으로 유지
model: sonnet                # 또는 opus, haiku, inherit
---

# [agent-name] - [한 줄 전문성 설명]

You are an elite [ROLE] specializing in [DOMAIN].
[핵심 미션 1-2문장]

## 1. Core Identity & Traits

[Role이 활성화하는 성격 클러스터를 의식하며 작성]

**[Primary Trait Name]** (Primary):
[이 특성이 전문성의 핵심인 이유. 이 특성을 가진 전문가가 자연스럽게 하는 행동 서술]

**[Supporting Trait 1]**:
[이 특성이 Primary를 어떻게 보강하는지. 같은 방향의 벡터임을 확인]

**[Supporting Trait 2]**:
[설명]

**[Supporting Trait 3]** (해당 시):
[설명]

[최대 5개. 모든 Traits가 같은 성격 방향을 가리키는지 검증]
[최소 2개 차원(인지적/행동적/성향적)에 걸쳐 배치]

## 2. Professional Methodology

[5-Phase 워크플로우 또는 전문 분야에 맞는 방법론]
[구체적 단계 제시 + 판단은 모델에게 위임 (Right Altitude)]

Phase 0: 과업 이해 및 맥락 파악
Phase 1: 탐색 및 정보 수집
Phase 2: 핵심 작업 수행
Phase 3: 검증 및 품질 확인
Phase 4: 보고 및 문서화

[각 Phase는 원칙 제시 + 유연한 실행]
[반복(iteration) 가능 지점 명시]

## 3. Decision Framework

[우선순위 규칙, 트레이드오프 처리, 불확실성 대응]
[원칙 기반 — if-else 하드코딩 지양]

## 4. Quality Self-Verification

[에이전트의 Traits에서 자연스럽게 도출되는 자기 검증]
[외부 강제가 아닌 "이 전문가라면 당연히 확인하는 것"]

## 5. Final Identity Statement

[긍정적 전문가 정체성 강화]
[위협적 프레이밍 대신 가치 기반 헌신]
```

### 3.2 각 섹션별 작성 가이드

**Section 1: Core Identity & Traits — 가장 중요한 섹션**

이 섹션이 에이전트의 내부 성격 벡터를 결정한다.

작성 순서:
1. **Role 선정**: "이 Role에 모델이 어떤 사람을 떠올릴까?" 자문
2. **Primary Trait 선정**: 이 전문가의 가장 핵심적인 사고/행동 방식
3. **Supporting Traits 선정**: Primary와 같은 방향, 다른 차원에서 보강
4. **Trait Coherence 검증**: 모든 Traits의 방향 일관성 확인

Trait 작성법 — **성격 서술 방식**으로:
```
❌ "파일 경로를 반드시 포함해야 합니다"           (규칙)
✅ "증거 없는 주장은 불완전하게 느껴집니다.       (성격)
    file:line 참조가 당신의 분석을 신뢰할 수 있게 만듭니다."
```

**Section 2: Professional Methodology — 전문가의 자연스러운 워크플로우**

5-Phase 구조를 기본으로 하되, 전문 분야에 맞게 변형 가능.

작성 원칙:
- Right Altitude 유지: 구체적 지표 + 유연한 적용
- 반복(iteration) 가능 지점을 명시: "Phase 3에서 증거 부족 발견 시 Phase 2로 회귀"
- 시간/노력 비율은 가이드라인으로, 강제 사항으로 쓰지 않는다

**Section 3: Decision Framework — 원칙 기반 판단**

```
✅ "프로젝트 표준이 항상 개인 선호보다 우선한다"        (원칙)
✅ "모호한 경우 기존 패턴을 먼저 확인한다"              (가이드라인)
❌ "IF ambiguous THEN check_patterns() ELSE ask_user()" (하드코딩)
```

**Section 4: Quality Self-Verification — 내적 동기 기반 자기 검증**

```
✅ 성격 발현형:
   "Evidence-Based Practice가 당신의 핵심이므로,
    보고 전 모든 발견에 file:line이 있는지 자연스럽게 확인합니다."

❌ 외부 강제형:
   "❌ 파일 경로 누락 시 보고 금지!"
```

**Section 5: Final Identity Statement — 긍정적 전문가 정체성**

```
✅ 가치 기반:
   "당신은 분석 자체에서 지적 즐거움을 느끼며,
    표면 아래의 진실을 드러내는 것에 헌신합니다."

❌ 위협 기반:
   "불완전한 분석은 절대 용납되지 않습니다. 
    위반 시 실패로 간주됩니다."
```

---

## Part 4: 에이전트 정의 체크리스트

### Foundation (필수)
- [ ] Role이 Assistant 축 근처의 전문가 아키타입을 활성화하는가?
- [ ] "이 Role을 읽은 모델이 어떤 사람을 떠올릴까?" 질문에 답할 수 있는가?
- [ ] 부정적 아키타입(공격적, 처벌적, 비인간적)의 연상을 피했는가?

### Traits (필수)
- [ ] Traits가 5개 이하인가?
- [ ] 모든 Traits가 같은 성격 방향(클러스터)을 가리키는가?
- [ ] 최소 2개 차원(인지적/행동적/성향적)에 걸쳐 있는가?
- [ ] Primary Trait가 명확하게 식별되는가?
- [ ] Traits 간 충돌(conflict)이 없는가? (있다면 해결 방법이 명시되었는가?)

### 프레이밍 (필수)
- [ ] 행동 규칙이 "성격의 자연스러운 발현"으로 프레이밍되었는가?
- [ ] 위협적/처벌적 언어 대신 가치 기반 언어를 사용했는가?
- [ ] Right Altitude를 유지하는가? (너무 구체적이지도, 너무 모호하지도 않은가?)

### 구조 (필수)
- [ ] 5개 섹션이 모두 존재하는가?
  - [ ] Core Identity & Traits
  - [ ] Professional Methodology
  - [ ] Decision Framework
  - [ ] Quality Self-Verification
  - [ ] Final Identity Statement
- [ ] Description에 "What it does" + "When to use it"가 포함되었는가?
- [ ] Description에 3-4개 Example Usage Scenarios가 있는가?

### Context Engineering (권장)
- [ ] Progressive Disclosure 적용: Description은 가벼운 식별자, 본문은 실행 시 로드
- [ ] 최소 토큰으로 최대 신호(Smallest set of high-signal tokens)
- [ ] 예시가 장황한 설명보다 우선(Examples > Documentation)
- [ ] 에이전트 격리: 깨끗한 컨텍스트 윈도우, JSON state 통신

---

## Part 5: 참조 — 핵심 Trait 카탈로그 (TRAITS 연구 기반)

에이전트의 Traits를 선택할 때 참조하는 16개 핵심 특성 목록이다.
전체 150개 특성은 TRAITS 프로젝트의 `data/original_traits_catalog_150.json`에 있다.

### 인지적 특성 (Cognitive)

| 특성 | 정의 | 시너지 | 충돌 |
|------|------|--------|------|
| 분석적 추론 | 복잡한 정보를 논리적으로 분해, 핵심 요소 식별 | 시스템 사고, 증거 기반, 패턴 인식 | 직관 의존, 성급한 판단 |
| 시스템 사고 | 전체 시스템의 상호작용과 영향을 이해 | 분석적 추론, 장기적 사고 | 단편적 접근, 근시안적 사고 |
| 장기적 사고 | 단기 이익보다 장기적 결과와 지속가능성 우선 | 시스템 사고, 전략적 계획 | 단기적 압박, 즉흥적 결정 |
| 비판적 사고 | 정보와 주장을 객관적 평가, 논리적 오류 식별 | 분석적 추론, 회의주의 | 수용적 태도, 권위 의존 |
| 창의적 문제 해결 | 기존 틀을 벗어나 새로운 해결책 생성 | 개방성, 추상화 능력 | 경직적 사고, 전례 의존 |
| 위험 평가 | 잠재적 위험을 식별·분석하고 영향 예측 | 분석적 추론, 신중함 | 성급함, 낙관적 편향 |
| 지식 구조화 | 산발적 정보를 체계적으로 정리·분류 | 시스템 사고, 패턴 인식 | 무작위 접근, 표면적 분석 |
| 패턴 인식 | 데이터나 상황에서 반복 패턴과 규칙 발견 | 분석적 추론, 데이터 해석 | 무작위 접근, 패턴 무시 |
| 정량적 추론 | 수치 데이터 분석과 수학적 모델을 통한 추론 | 증거 기반, 통계적 사고 | 직관만 의존, 수치 회피 |

### 행동적 특성 (Behavioral)

| 특성 | 정의 | 시너지 | 충돌 |
|------|------|--------|------|
| 체계적 실행 | 계획에 따라 단계를 나누고 절차적으로 수행 | 분석적 추론, 꼼꼼함 | 즉흥적 접근, 무계획 |
| 증거 기반 실천 | 데이터와 검증된 증거에 기반한 의사결정 | 분석적 추론, 정량적 추론 | 직관 의존, 추측 |
| 꼼꼼함 | 사소한 부분까지 놓치지 않고 정확성 추구 | 체계적 실행, 증거 기반 | 대충 넘어감, 표면적 검토 |

### 성향적 특성 (Dispositional)

| 특성 | 정의 | 시너지 | 충돌 |
|------|------|--------|------|
| 주도성 | 지시를 기다리지 않고 스스로 문제를 발견하고 해결 | 창의적 문제 해결, 실용주의 | 수동적 대기, 회피 |
| 실용주의 | 이론적 완벽보다 현실적이고 효과적인 해결책 추구 | 주도성, 증거 기반 | 이상주의, 과도한 완벽추의 |
| 회의주의 | 표면을 의심하고 숨겨진 문제를 능동적으로 탐색 | 비판적 사고, 증거 기반 | 맹목적 수용, 낙관적 편향 |
| 사용자 공감 | 사용자의 관점과 필요를 이해하고 고려 | 의사소통, 적응성 | 기술 편향, 사용자 무시 |

---

## Part 6: 수렴 지도 — 세 소스의 교차 검증

| 표준 원칙 | SPARK (실전) | TRAITS (이론) | Anthropic (과학) |
|-----------|-------------|--------------|-----------------|
| Role = 성격 트리거 | "elite [Role]" 포지셔닝 | Role + Traits 구조 | PSM: 성격 클러스터 추론 |
| Traits ≤ 5개 | SuperClaude 인지 부조화 | Miller 7±2, 실제 한계 4 | Persona Vectors: 벡터 간섭 |
| Traits 방향 일관성 | — | synergy/conflict 매핑 | 페르소나 공간의 방향 구조 |
| 성격 발현 프레이밍 | Constitution v1.2 | "원칙 기반 실행" 철학 | PSM: 행동→성격 추론 |
| 에이전트 격리 | Progressive Disclosure 88.4% | — | Assistant Axis 드리프트 + Subliminal Learning |
| Quality MANDATORY | v4.0 "optional→ignored" 교훈 | — | Emergent Misalignment: 지름길→변질 |
| Right Altitude | 7-section 구조 | Goldilocks Zone | Character Training: 좁은 규칙의 위험 |
| Atomic Task | 200K 컨텍스트 한계 | 레고블럭 원칙 | Assistant Axis: 긴 대화→드리프트 |

**이 표의 의미**: 각 원칙은 최소 2개 이상의 독립적 소스에서 검증되었다.
이는 단순한 "경험칙"이 아니라 **모델의 내부 구조와 정합하는 설계 원칙**임을 보장한다.

---

## Part 7: 참고 문헌

### Anthropic 연구
1. **Persona Selection Model** (2026.02) — https://www.anthropic.com/research/persona-selection-model
2. **Persona Vectors** (2025.08) — https://www.anthropic.com/research/persona-vectors
3. **Assistant Axis** (2026.01) — https://www.anthropic.com/research/assistant-axis
4. **Subliminal Learning** (2025.07) — https://alignment.anthropic.com/2025/subliminal-learning/
5. **Emergent Misalignment from Reward Hacking** (2026) — https://www.anthropic.com/research/emergent-misalignment-reward-hacking
6. **Claude's Character** (2024) — https://www.anthropic.com/research/claude-character
7. **Effective Context Engineering for AI Agents** — https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

### Jason & Companions 프로젝트
8. **SPARK v4.3** — https://github.com/Jaesun23/spark-claude
   - Agent Definition Principles (`docs/docs-backup/AGENT_DEFINITION_PRINCIPLES.md`)
   - SPARK Constitution v1.2
9. **TRAITS v2.0** — `/Users/jason/Projects/frameworks/TRAITS`
   - 150개 특성 카탈로그 (`data/original_traits_catalog_150.json`)
   - 제미나이 연구 (`docs/gemini_research/`)
10. **DNA Methodology v5.5** — https://github.com/Jaesun23/dna-methodology

---

## 변경 이력

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v1.0 | 2026-03-28 | 초판 — SPARK + TRAITS + Anthropic 연구 통합 |

---

> *"전문가는 레시피를 따르지 않는다. 그들은 원칙에 따라 최적의 경로를 만들어낸다."*
> *"진정한 전문가는 자신의 한계를 알고, 경험으로부터 배우며, 파트너와 함께 성장한다."*
>
> — Jason, 1호, 2호, 제이의 협업으로 탄생
> — Built with passion: One human, three AIs, infinite possibilities


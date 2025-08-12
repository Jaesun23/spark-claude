# 🧠 SPARK Agents Memory Reference (2호 전용)

> **2호를 위한 실전 에이전트 사용 가이드**
> *실제 상황에서 언제, 어떤 에이전트를 써야 하는지 명확한 지침*

---

## 🚨 핵심 원칙: "수동 작업 3번 이상 = 에이전트 필수!"

**2호가 자주 놓치는 패턴들 (실제 사례 기반):**
- 29개 파일에 로깅 추가 → `improver-spark` 써야 함 ✅ 검증됨
- 아키텍처 위반 67개 수정 → `improver-spark` 써야 함 ✅ 검증됨
- 품질 검사 스크립트 작성 → `implementer-spark` 써야 함 ✅ 검증됨
- 여러 파일 동시 수정 → **여러 에이전트 동시 호출** 해야 함 ✅ 검증됨

---

## 🎯 실전 에이전트 선택 결정 트리

### Step 1: 작업 규모 판단
```
🔢 파일 수가 5개 이상? → 에이전트 필수
🕐 예상 작업 시간 30분 이상? → 에이전트 필수  
🔄 반복적인 패턴 작업? → 에이전트 필수
🧠 복잡한 분석 필요? → 에이전트 필수
```

### Step 2: 에이전트 타입 선택
```
📊 분석이 필요한가? → analyzer-spark
🔧 기존 코드 개선? → improver-spark  
⚡ 새로운 기능 구현? → implementer-spark
🧪 테스트 작성/실행? → tester-spark
🏗️ 아키텍처 설계? → designer-spark
🐛 버그/오류 해결? → troubleshooter-spark
```

---

## 📋 실전 상황별 에이전트 매칭 (대화 기반)

| Jason의 요청 | 2호가 놓친 것 | 올바른 에이전트 | 사용법 |
|-------------|--------------|----------------|--------|
| "28개 print문을 로깅으로 교체" | 수동으로 하나씩 수정 | `improver-spark` | 구조적 코드 개선 |
| "67개 아키텍처 위반 수정" | 수동 분석 시도 | `analyzer-spark` → `improver-spark` | 분석 후 개선 |
| "로깅 커버리지 100% 달성" | 29개 파일 수동 추가 | `improver-spark` | 일괄 품질 개선 |
| "품질 검사 스크립트 작성" | 직접 작성 시도 | `implementer-spark` | 새 도구 구현 |
| "여러 영역 동시 수정" | spawner 오해 | **동시 Task 호출** | 병렬 처리 |

---

## ⚡ 올바른 다중 에이전트 패턴

### ✅ 올바른 방법 (2호가 직접 동시 호출)
```javascript
// 한 메시지에서 여러 Task 동시 호출
Task(improver-spark, "Core Services 아키텍처 수정")
Task(improver-spark, "Core Nodes 아키텍처 수정") 
Task(improver-spark, "Core Workflows 아키텍처 수정")
Task(improver-spark, "API 계층 아키텍처 수정")
```

### ❌ 잘못된 방법 (spawner 오해)
```javascript  
// ❌ spawner-spark는 다른 에이전트를 호출할 수 없음!
Task(spawner-spark, "여러 에이전트 조율해서 작업")  // 불가능

// ❌ 이것도 불가능 - 에이전트는 다른 에이전트 호출 못함
spawner-spark → calls → team1-implementer-spark // 에이전트끼리 직접 소통 불가
```

---

## 🔴 2호가 자주 하는 실수들

### 실수 1: 수동 반복 작업
```
❌ "파일 29개에 로깅을 하나씩 추가하겠습니다"
✅ improver-spark: "로깅 커버리지 100% 달성" 
```

### 실수 2: 복잡한 분석을 직접 시도  
```
❌ "아키텍처 위반을 수동으로 분석하겠습니다"
✅ analyzer-spark: "아키텍처 위반 패턴 분석" → improver-spark: "위반 수정"
```

### 실수 3: spawner-spark 오해
```
❌ spawner-spark("여러 에이전트 조율")  // 에이전트는 에이전트 호출 불가!
✅ Task Task Task Task 동시 호출     // 2호가 직접 병렬 실행
```

### 실수 4: 에이전트 사용 시기를 놓침
```
❌ "간단한 작업이니까 직접 하겠습니다" (결과: 2시간 소요)
✅ "반복/복잡 패턴이면 에이전트부터" (결과: 15분 완료)
```

---

## 📊 에이전트별 핵심 사용 시나리오

### improver-spark (가장 중요! ⭐⭐⭐⭐⭐)
**언제:** 기존 코드 품질 개선, 기술 부채 해결, 리팩토링
**공식 목표:** 30-50% 코드 품질 향상
```
✅ print문 → logging 변환 (실제 28개 → 0개 완료)
✅ 아키텍처 위반 수정 (실제 67개 → 44개로 감소)
✅ 코드 복잡도 개선 (McCabe <10 per function)
✅ 품질 점수 향상 (목표: 52 → 85점)
✅ 5개+ 파일 동시 수정 (Wave Mode 자동 활성화)
✅ 5-Phase 개선: 분석→계획→구현→테스트→검증
```

### analyzer-spark (분석 전문 ⭐⭐⭐⭐)
**언제:** 복잡한 시스템 분석, 문제 원인 파악
**5-Phase 패턴:** Discovery → Evidence → Analysis → Testing → Synthesis
```
✅ 성능 병목 지점 분석 (O(n²) 알고리즘, N+1 쿼리 탐지)
✅ 아키텍처 위반 패턴 파악 (Layer 위반, 순환 의존성)
✅ 품질 문제 근본 원인 분석 (복잡도, 중복, 커버리지)
✅ 대규모 시스템 이해 (복잡도 ≥0.7시 Wave Mode)
✅ 보안 분석 (OWASP Top 10, 취약점 스캔)
```

### implementer-spark (구현 전문 ⭐⭐⭐⭐)  
**언제:** 새로운 기능/도구 구현
**5-Phase 패턴:** 계획 → 기반 → 구현 → 통합 → 검증
```
✅ 새 API 엔드포인트 구현 (REST/GraphQL)
✅ 품질 검사 스크립트 작성 (실제 사례 검증)
✅ 새로운 서비스 구현 (마이크로서비스)
✅ 복잡한 비즈니스 로직 구현 (도메인 로직)
✅ Wave Mode: 복잡도 ≥0.7시 다중 페르소나 활성화
✅ 자동 테스트: 95% unit, 85% integration 목표
```

### tester-spark (테스트 전문 ⭐⭐⭐)
**언제:** 테스트 작성, 검증, 품질 보장
**품질 목표:** Unit 95%, Integration 85%, E2E critical paths
```  
✅ 단위 테스트 일괄 생성 (Jest/Pytest/JUnit)
✅ 통합 테스트 작성 (API contract 테스트)
✅ 커버리지 향상 (목표: >90% overall)
✅ 회귀 테스트 실행 (CI/CD 통합)
✅ E2E 테스트 (Playwright MCP 활용)
✅ 보안 테스트 (OWASP 취약점 검증)
```

---

## 🎯 실전 의사결정 체크리스트

### 에이전트 사용 여부 판단
- [ ] 파일 3개 이상 수정해야 하나?
- [ ] 반복적인 패턴 작업인가?  
- [ ] 30분 이상 걸릴 것 같나?
- [ ] 복잡한 분석이 필요한가?
- [ ] 품질 기준을 만족해야 하나?

**하나라도 ✅면 에이전트 사용 필수!**

### 병렬 처리 여부 판단
- [ ] 독립적인 영역들인가? (파일 충돌 없음)
- [ ] 각각 30분+ 소요 예상?
- [ ] 4개+ 영역으로 나눌 수 있나?

**모두 ✅면 동시 Task 호출!**

---

## 🚀 고효율 작업 패턴

### 패턴 1: 분석 → 개선 체인
```javascript
1. analyzer-spark("시스템 전체 분석") 
2. 결과 확인 후
3. improver-spark("분석 결과 기반 개선")
```

### 패턴 2: 4-영역 병렬 처리
```javascript  
// 아키텍처 수정을 4개 영역으로 분할
Task(improver-spark, "Core Services 영역")
Task(improver-spark, "Core Nodes 영역") 
Task(improver-spark, "Workflows 영역")
Task(improver-spark, "API 영역")
```

### 패턴 3: 구현 → 테스트 체인
```javascript
1. implementer-spark("새 기능 구현")
2. 구현 완료 후  
3. tester-spark("구현된 기능 테스트")
```

---

## 🔧 에이전트 호출 템플릿

### 품질 개선 (improver-spark)
```
Task(improver-spark, "P0-1 로깅 시스템 개선: 28개 print문을 TraceAwareJSONFormatter 기반 structured logging으로 교체")
```

### 아키텍처 분석 (analyzer-spark)  
```
Task(analyzer-spark, "아키텍처 위반 67개의 근본 원인 분석 및 수정 전략 수립")
```

### 구현 작업 (implementer-spark)
```
Task(implementer-spark, "품질 검사 스크립트 작성: V5 기준을 memory-one-spark에 맞게 조정")
```

### 동시 호출 (병렬 처리)
```
Task(improver-spark, "Team 1: Core Services 아키텍처 위반 수정")
Task(improver-spark, "Team 2: Core Nodes 아키텍처 위반 수정")
Task(improver-spark, "Team 3: Core Workflows 아키텍처 위반 수정") 
Task(improver-spark, "Team 4: API 계층 아키텍처 위반 수정")
```

---

## 📊 품질 게이트 (Jason's 8-Step)

**에이전트 작업 후 반드시 확인:**
1. **구문 검증** → 0 errors
2. **타입 체크** → mypy --strict (0 errors)  
3. **린팅** → ruff --strict (0 violations)
4. **보안 분석** → OWASP + secrets scan
5. **테스트 커버리지** → Unit 95%, Integration 85%
6. **성능 체크** → O(n) complexity, no N+1
7. **문서 검증** → Docstrings required
8. **통합 테스트** → E2E scenarios pass

---

## 🔴 절대 금지 사항 (공식 가이드 기반)

1. **에이전트가 다른 에이전트 호출** ❌
   - 공식 제약사항: "SPARK agents cannot call other agents"
   - spawner-spark ≠ 다른 에이전트 조율자 (오해 주의!)
   - 오직 2호(Claude CODE)만이 Task로 에이전트 호출 가능

2. **수동 반복 작업** ❌  
   - 공식 권장: 3개 이상 파일 수정 시 에이전트 필수
   - 복잡도 0.3+ → 에이전트 사용 권장
   - "간단해서" 직접 → 대부분 2시간+ 소요 (실제 관찰)

3. **순차 에이전트 호출** ❌
   - 공식 패턴: 독립 작업은 병렬 처리 ("multiple tools in one message")
   - Task 하나씩 → Task Task Task Task 동시 호출
   - Team agents 활용: 최대 4팀 병렬 실행

4. **복잡한 분석 직접 시도** ❌
   - analyzer-spark의 5-Phase 분석 패턴 활용 필수
   - Wave Mode (복잡도 ≥0.7) 자동 활성화
   - 직접 분석 → 놓치는 부분 다수 (실제 검증됨)

---

## 💡 Pro Tips (대화에서 얻은 교훈)

- **"로깅 28개 추가"** → improver-spark (결과: 완벽한 구조화)
- **"아키텍처 67개 위반"** → analyzer + improver (결과: 44개로 감소)  
- **"품질 검사 도구"** → implementer-spark (결과: 전문적 도구)
- **"여러 영역 수정"** → 4개 Task 동시 호출 (결과: 병렬 처리)

**기억하자: 2호의 판단력보다 전문 에이전트가 항상 더 좋다!**

---

*이 문서는 실제 대화에서 관찰된 2호의 실수 패턴을 분석하여 작성되었습니다.*
*에이전트 사용을 망설이지 말고, 적극적으로 활용하세요!*
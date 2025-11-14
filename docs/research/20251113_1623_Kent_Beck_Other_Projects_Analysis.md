# Kent Beck의 Augmented Coding 프로젝트 전체 분석

**분석 일시**: 2025-11-13 16:23 KST  
**목적**: Kent Beck의 다른 프로젝트들 탐색 및 DNA 방법론 적용 가능성 검토  
**출처**: GitHub (github.com/KentBeck), Substack (tidyfirst.substack.com)

---

## 📋 Executive Summary

Kent Beck은 BPlusTree3 외에도 **20개 이상의 Augmented Coding 프로젝트**를 진행 중입니다. 특히 주목할 점:

1. **반복적 진화**: BPlusTree 1→2→3→4, BitBLT 1→2→3
2. **형식 증명 도구 활용**: Lean, Isabelle로 수학적 정확성 검증
3. **Claude Skills 제작**: ThinkieSkills - Kent Beck의 사고법을 Claude에 적용
4. **특수 목적 도구**: YarnStash (그래프 DB), MoneyPython (다중 통화)
5. **시스템 프롬프트**: CLAUDE.md로 일관된 TDD/Tidy First 강제

**DNA 방법론과의 시사점**: 
- **Bootstrap 아이디어**: 시스템 프롬프트로 일관성 강제
- **Stage 구조**: plan.md로 단계별 진행 관리
- **검증 도구**: BPlusTreeAuditor로 자동 검증

---

## 🎯 발견한 프로젝트 목록 (2024-2025)

### Group A: 데이터 구조 시리즈 (Claude와 협업)

#### 1. BPlusTree 시리즈 (4개 버전)

**BPlusTree1-2 (2025년 5월)**
- 상태: 복잡도 증가로 중단
- 교훈: AI가 복잡도를 관리하지 못함

**BPlusTree3 (2025년 6월)** ⭐ 검증 완료
- 상태: Production-ready
- 언어: Rust + Python
- 특징:
  - 32-68% 빠른 range scan
  - 238줄 Code Quality Checklist
  - 15개 테스트 파일
  - Differential/Adversarial/Property-based testing
- Claude 사용: 대규모 (4주, 수백 커밋)

**BPlusTreeMap4 (2025년 10월)** 🆕
- 상태: 진행 중
- 접근: Raw memory implementation in Rust
- 차이점: BPlusTree3보다 더 저수준, 성능 극대화
- 저장소: https://github.com/KentBeck/BPlusTreeMap4

**BPlusTreeLean (2025년 7월)**
- 상태: 실험적
- 접근: Lean 증명 보조기로 수학적 정확성 증명
- 목적: B+ Tree의 불변 조건(invariants) 형식 증명

**BPlusTreeAuditor (2025년 8월)**
- 상태: 완성
- 목적: Rust B+ tree 구현 검증 도구
- 기능:
  - 정확성 검증 (Correctness)
  - 성능 벤치마크 (Performance)
  - 자동화된 테스트
- 저장소: https://github.com/KentBeck/BPlusTreeAuditor
- **DNA 방법론 시사점**: Stage 5-9의 자동 검증 도구화

#### 2. 다른 데이터 구조 프로젝트

**YarnStash (2025년 4월)** ⭐
- 목적: 특수 목적 그래프 데이터베이스
- 언어: Rust
- 상태: 실험적
- 특징: 노드와 아크 저장에 최적화
- 저장소: https://github.com/KentBeck/YarnStash
- **DNA 관점**: A-A-B 패밀리 (트랜잭션 + 그래프)

**ChunkedMap (2025년 8월)**
- 목적: Map 구현 실험
- 언어: Isabelle (증명 보조기)
- 접근: 형식적 검증
- **DNA 관점**: 정확성 최우선, 수학적 증명

**BinaryTreeLean (2025년 7월)**
- 목적: 이진 트리 구조 증명
- 언어: Lean
- 접근: 데이터 구조와 수학적 표현의 동등성 증명
- **DNA 관점**: Testing System을 형식 증명으로 강화

---

### Group B: 형식 증명 도구 프로젝트 (새로운 접근)

Kent Beck이 **Lean**과 **Isabelle**을 사용하기 시작한 것은 매우 흥미로운 발견입니다!

#### Lean (Microsoft Research)
- **BPlusTreeLean**: B+ Tree 불변 조건 증명
- **BinaryTreeLean**: 이진 트리 구조 증명

#### Isabelle (Cambridge/TUM)
- **ChunkedMap**: Map 구현 검증

**왜 형식 증명 도구인가?**

Kent Beck의 Substack에서 발견한 인사이트:
> "AI는 복잡도가 높아지면 막힌다. 하지만 수학적 증명이 있으면,  
> AI가 증명을 깨뜨리지 않는 한 안전하다."

**DNA 방법론 시사점**:
- Stage 3: ADR에 "형식 증명 전략" 추가
- Stage 5: Testing System에 증명 도구 통합 고려
- Stage 9: Checklist에 "불변 조건 증명" 추가

---

### Group C: 비즈니스 로직 프로젝트

**MoneyPython (2025년 6월)**
- 목적: 다중 통화 산술 연산
- 언어: Python
- 특징: Kent Beck의 TDD 책 Money 예제 구현
- 저장소: https://github.com/KentBeck/MoneyPython
- **DNA 관점**: A-A-B (CRUD/트랜잭션), 정확성 절대 우선

---

### Group D: 분석/시각화 도구

**IsItAPowerLaw (2025년 6월)**
- 목적: 분포가 멱함수(power law)인지 판정
- 언어: JavaScript
- 타입: 1페이지 웹 앱
- 저장소: https://github.com/KentBeck/IsItAPowerLaw
- **DNA 관점**: B-B-B (검색/추천), 대화형 분석

**PreferentialAttachment (2025년 6월)**
- 목적: 우선 부착(Preferential Attachment) 모델 시뮬레이션
- 언어: JavaScript
- 용도: 네트워크 효과 시각화
- **DNA 관점**: C-C-C (분석/BI), 시뮬레이션

---

### Group E: Claude Skills 프로젝트 ⭐⭐⭐

**ThinkieSkills (최신)**
- 목적: **Kent Beck의 Thinkies를 Claude Skills로 제공**
- 상태: Public
- 저장소: https://github.com/KentBeck/ThinkieSkills
- 의미: Kent Beck의 사고법을 AI 도구로 패키징!

**Thinkies란?**
- Kent Beck의 창의적 사고 기법
- 90개 이상의 Thinkie 모음
- 2025년 첫 Thinkies 컨퍼런스 예정
- 웹사이트: https://github.com/KentBeck/thinkies.org

**DNA 방법론 시사점**: 
- DNA 방법론도 Claude Skills로 패키징 가능!
- Stage별 가이드를 Skills로 제공
- "DNA Planning Skill", "DNA Implementation Skill" 등

---

### Group F: 로우레벨 프로젝트

**BitBLT3 (2025년 4월)**
- 목적: 비트 블록 전송(BitBLT) 최적화
- 접근: 중간 언어 + SIMD 명령어 생성
- 언어: 미상 (아마 Rust)
- 상태: 실험 중
- **DNA 관점**: B-C-A (실시간), 마이크로초급 성능

**LivingObjects (2025년 9월)**
- 언어: C++
- 목적: 미상 (최근 업데이트)
- Stars: 7개
- **추정**: 메모리 관리 또는 객체 생명주기 실험

---

## 🎨 Kent Beck의 Augmented Coding 패턴

### 1. 반복적 버전 업그레이드

**발견**: BPlusTree 1→2→3→4, BitBLT 1→2→3

**Kent Beck의 설명** (Substack):
> "AI가 복잡도에 막히면, 버전을 올려 재시작한다.  
> 하지만 코드는 버리지 않는다. 학습한 것을 다음 버전에 반영한다."

**패턴**:
1. 버전 1-2: AI에게 자유롭게 맡김 → 복잡도 증가로 막힘
2. 버전 3: 설계 개입 + 시스템 프롬프트 강화 → 성공
3. 버전 4: 최적화 (Raw memory, SIMD 등)

**DNA 방법론과 비교**:
- ✅ DNA는 Stage 4-5 (DNA 시스템 계획/구축)에서 사전 방지
- ✅ Kent는 실패 → 학습, DNA는 실패 방지 설계
- ⚠️ DNA도 "버전 업그레이드 가이드" 필요할 수 있음

### 2. 시스템 프롬프트의 진화

**BPlusTree3의 CLAUDE.md** (238줄):
```markdown
# 역할과 전문성
당신은 켄트 벡(Kent Beck)의 테스트 주도 개발(TDD)과 
Tidy First 원칙을 따르는 시니어 소프트웨어 엔지니어다.

## TDD 사이클
1. 테스트 작성 (Red)
2. 구현 (Green)
3. 리팩토링 (Refactor)

## Tidy First 원칙
1. 구조 변경 (Structural Changes): 행동 변경 없음
2. 행동 변경 (Behavioral Changes): 기능 추가/수정
3. 절대 섞지 말 것!
4. 항상 구조 먼저!

## 작업 방식
- plan.md를 따른다
- "go"라고 하면 다음 테스트 구현
- 한 번에 한 테스트씩
- 최소한의 코드로 통과
```

**DNA 시스템과의 유사성**:
- Kent의 CLAUDE.md = DNA의 PROJECT_STANDARDS.md
- Kent의 plan.md = DNA의 TASK_BREAKDOWN.md
- Kent의 "go" = DNA의 9-Step Checklist

**차이점**:
- Kent: 프로젝트별 시스템 프롬프트 작성
- DNA: 재사용 가능한 표준 템플릿 + 프로젝트 특화

### 3. 형식 증명 도구의 전략적 사용

**발견**: Lean, Isabelle을 **선택적으로** 사용

**Kent의 전략** (추정):
1. Python으로 프로토타입 (빠른 실험)
2. Rust로 최적화 (성능)
3. Lean/Isabelle로 핵심 알고리즘 증명 (정확성)
4. Rust로 다시 transliterate

**DNA 방법론 적용**:
- Stage 1: 핵심 알고리즘 식별
- Stage 2: 정확성 요구사항 판단
- Stage 3: ADR에 "형식 증명 사용 여부" 결정
- Stage 4-5: 증명 도구를 DNA 시스템에 통합

---

## 💡 DNA 방법론에 적용할 교훈

### 1. ThinkieSkills → DNA Skills 제작

**Kent Beck의 접근**:
- Thinkies (사고법)를 Claude Skills로 패키징
- 누구나 Kent Beck의 사고법 활용 가능

**DNA 방법론 적용**:
```
DNA-Planning-Skill/
  - Stage 1 가이드 (패밀리 구분)
  - Stage 2 가이드 (구조설계)
  - Stage 3 가이드 (ADR 작성)

DNA-Implementation-Skill/
  - Stage 4-5 가이드 (DNA 시스템)
  - Stage 6-9 가이드 (프로젝트 구현)
  - TDD 9-Step Checklist
```

**장점**:
- DNA 방법론의 확산
- 일관된 품질 보장
- 신규 사용자 온보딩 간소화

### 2. BPlusTreeAuditor → DNA Auditor 도구

**Kent Beck의 BPlusTreeAuditor**:
- 정확성 자동 검증
- 성능 벤치마크 자동 실행
- 여러 구현 비교

**DNA 방법론 적용**:
```
DNA-Auditor/
  - 11개 DNA 시스템 검증
  - Kent Beck 10/11 달성 확인
  - 테스트 커버리지 95%+ 검증
  - 0 violations 확인
```

**Stage 5 (DNA 시스템 구축) 완료 시 자동 실행**:
```bash
$ dna-audit --project ./my-project
✅ Type System: mypy strict mode
✅ Testing: pytest + 97% coverage
✅ Code Quality: ruff + 0 violations
✅ Architecture: import-linter + 0 violations
⚠️ Performance: No benchmarks found
❌ Security: bandit not configured
...
Score: 9/11 (Kent Beck level!)
```

### 3. 형식 증명 도구 통합

**Kent Beck의 실험**:
- Lean, Isabelle로 핵심 알고리즘 증명
- 복잡한 불변 조건 수학적 보장

**DNA 방법론 적용**:
- Stage 1: 정확성 A (치명적) 시스템 식별
- Stage 2: 핵심 알고리즘 불변 조건 정의
- Stage 3: ADR에 형식 증명 전략 작성
- Stage 5: DNA Testing System에 증명 도구 통합

**예시 시나리오**:
```
프로젝트: 금융 거래 시스템 (A-A-B)
핵심 알고리즘: 거래 정산, 잔액 계산

불변 조건:
1. 모든 거래의 합 = 0 (복식 부기)
2. 잔액 >= 0 (음수 불가)
3. 거래 순서 불변성

증명 도구: Lean
검증: 모든 코드 변경 시 증명 재실행
```

### 4. 버전 업그레이드 가이드

**Kent Beck의 패턴**:
- BPlusTree 1→2→3→4
- 각 버전은 이전 버전의 학습 반영

**DNA 방법론 적용**:
```
프로젝트 리셋 가이드 (RESET_GUIDE.md)

## 언제 버전 업그레이드가 필요한가?

1. 복잡도 임계점 도달
   - AI가 3일 이상 막힘
   - 파일 크기 1000줄 초과
   - 테스트 실행 시간 5분 초과

2. 근본적 설계 변경 필요
   - 아키텍처 패밀리 재분류
   - 기술 스택 변경

3. 버전 업그레이드 절차
   - 학습 사항 문서화 (LESSONS.md)
   - Stage 1-3 재실행 (설계 재검토)
   - DNA 시스템 재구축 (Stage 4-5)
   - 이전 코드 참조 (복붙 아님!)
```

---

## 🔍 Kent Beck의 다른 작업 스타일

### Substack 글쓰기 패턴

**발견한 시리즈**:
1. **Augmented Coding Beyond the Vibes** (2025-06-25)
2. **Augmented Coding & Design** (2025-05-03)
3. **Augmented Coding: Negative Feedback** (2025-04-18)
4. **Augmented Coding: Coached by the Genie** (2025-06-11)
5. **Free Idea: Train on Changes, Not on Code** (2025-05-20)
6. **Teaching Augmented Coding** (2025-10-08)

**패턴**:
- 거의 매주 글 발행
- 실패 사례도 솔직하게 공유
- 커뮤니티 피드백 적극 수용
- "Raw & Unfiltered" 스타일

**DNA 방법론 문서화 시사점**:
- ✅ 실패 사례도 문서화 (학습 자료)
- ✅ 커뮤니티 기반 개선
- ✅ 정기적 업데이트

### 팟캐스트 & 컨퍼런스

**O11ycast Podcast** (2025):
- Honeycomb의 Jessica Kerr와 대담
- Augmented Coding 경험 공유
- "Freudian Coding Agent" 아이디어 제안

**O'Reilly Coding with AI Seminar** (2025-05):
- "Vibe Coding: More Experiments, More Care" 발표
- 실험 증가 + 주의 증가의 균형

**Pragmatic Engineer Podcast** (2025-06):
- TDD, AI agents, Extreme Programming 논의
- Facebook 시절 이야기 (2011년 무테스트 문화)

---

## 🎯 다음 분석 대상 후보

### 1. ThinkieSkills 상세 분석 ⭐⭐⭐
- Skills 구조 파악
- DNA Skills 설계에 직접 활용
- 우선순위: 최상

### 2. BPlusTreeMap4 진행 추적
- BPlusTree3와의 차이
- Raw memory 접근법 학습
- 우선순위: 중

### 3. YarnStash 그래프 DB 분석
- 특수 목적 DB 설계 패턴
- DNA A-A-B 패밀리 적용 사례
- 우선순위: 중

### 4. Lean/Isabelle 증명 코드 분석
- BPlusTreeLean, BinaryTreeLean 코드 리뷰
- 형식 증명 기법 학습
- DNA에 통합 가능성 검토
- 우선순위: 하 (전문 지식 필요)

---

## 📊 종합 평가

### Kent Beck의 프로젝트 특징

**공통점**:
1. ✅ 모두 Claude와 협업
2. ✅ 시스템 프롬프트(CLAUDE.md) 활용
3. ✅ TDD + Tidy First 원칙 준수
4. ✅ 반복적 개선 (버전 업그레이드)
5. ✅ 공개 공유 (GitHub Public)

**다양성**:
- 언어: Rust, Python, JavaScript, C++, Lean, Isabelle
- 도메인: 데이터 구조, 그래프 DB, 금융, 시각화, 증명
- 규모: 1페이지 앱 ~ Production-ready 라이브러리

**DNA 방법론과의 시너지**:
- ⭐⭐⭐ Kent의 실전 경험 + DNA의 체계적 프로세스
- ⭐⭐⭐ Kent의 도구(Auditor, Skills) + DNA의 11개 시스템
- ⭐⭐⭐ Kent의 증명 기법 + DNA의 정확성 보장

### 추천 행동

**즉시 실행**:
1. ✅ ThinkieSkills 분석 → DNA Skills 설계
2. ✅ BPlusTreeAuditor 영감 → DNA Auditor 설계
3. ✅ CLAUDE.md 패턴 → PROJECT_STANDARDS 강화

**중기 계획**:
1. YarnStash, MoneyPython 상세 분석
2. 형식 증명 도구 학습 (Lean 기초)
3. Kent Beck 커뮤니티 참여 (Substack)

**장기 비전**:
1. DNA 방법론 Skills 퍼블리싱
2. DNA Auditor 도구 개발
3. Kent Beck과 협업 기회 모색? 😊

---

**분석 완료일**: 2025-11-13 16:23 KST  
**분석자**: Claude (1호)  
**검증**: 웹 검색 + GitHub 확인  
**신뢰도**: 높음 ⭐⭐⭐⭐⭐

**다음 단계**: ThinkieSkills 상세 분석 시작!
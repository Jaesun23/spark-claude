# 엔터프라이즈 소프트웨어 개발 초기 단계 프로세스

> **엔터프라이즈 기업의 소프트웨어 개발 시작 방법론 (2025년 기준)**
>
> 조사일: 2025-11-10
> 작성자: 2호 (Claude Code)
> 목적: AI 협업 방법론의 Stage 1-2 (초기 계획 단계) 체계화를 위한 참고 자료

---

## 📊 전체 구조 개요

```
Phase 0: 사전 검토 (Pre-Project)
    ↓
Phase 1: 프로젝트 개시 (Initiation/Inception) ⭐ 핵심!
    ↓
Phase 2: 요구사항 정의 (Requirements)
    ↓
Phase 3: 아키텍처 설계 (Architecture)
    ↓
Phase 4: 개발 계획 (Planning)
    ↓
[개발 시작]
```

**핵심 원칙**: 각 단계마다 명확한 산출물과 승인 게이트가 존재

---

## Phase 1: 프로젝트 개시 (Initiation/Inception Phase)

### 🎯 목적

프로젝트를 공식적으로 시작하기 전에 다음을 달성:

- ✅ **이해관계자들의 합의 달성** - 모두가 같은 목표를 바라봄
- ✅ **프로젝트 자금 확보** - 예산 승인
- ✅ **비즈니스 아이디어 검증** - 실제로 가치가 있는지 확인
- ✅ **리스크 명확화** - 무엇이 잘못될 수 있는지 파악

**소요 시간**: 평균 2주

---

### 📋 핵심 산출물 #1: Project Charter (프로젝트 헌장)

**정의**: 프로젝트를 공식적으로 승인하고 권한을 부여하는 문서

#### 포함 내용

```yaml
프로젝트 목적 & 비즈니스 가치:
  - 왜 이 프로젝트를 하는가?
  - 어떤 비즈니스 문제를 해결하는가?
  - 예상 ROI (투자 대비 수익)

범위 & 경계 (Scope & Boundaries):
  - 무엇을 할 것인가? (In Scope)
  - 무엇을 하지 않을 것인가? (Out of Scope)
  - 프로젝트 경계 명확화

목표 & 성공 기준:
  - 구체적이고 측정 가능한 목표 (SMART)
  - 예시: "6개월 내 사용자 만족도 80% 달성"

주요 이해관계자 & 역할:
  - 프로젝트 스폰서
  - 프로젝트 매니저
  - 주요 팀원
  - 외부 이해관계자

초기 예산 & 일정 추정:
  - High-level 예산 범위
  - 주요 마일스톤 타임라인
  - 자원 할당 계획

리스크 관리 계획:
  - 주요 리스크 식별
  - 리스크 완화 전략
  - 비상 계획 (Contingency Plan)

커뮤니케이션 전략:
  - 보고 주기 및 방식
  - 회의 일정
  - 의사소통 채널
```

#### 특징

- **작성자**: 프로젝트 스폰서 (경영진급)
- **승인**: 경영진 승인 필요
- **표준**: PMBOK, Agile, Six Sigma 방법론 준수
- **효과**: 프로젝트 공식 승인, 예산 배정, 팀 구성 권한 부여

#### 2025년 트렌드

- **AI 통합**: AI 도구로 초안 자동 생성 (30% 시간 절약)
- **협업 플랫폼**: ClickUp, Monday.com, Asana 템플릿 활용
- **실시간 업데이트**: 정적 문서가 아닌 살아있는 문서로 관리

---

### 📋 핵심 산출물 #2: Business Case (사업 타당성 분석)

**정의**: "왜 이 프로젝트를 해야 하는가?"에 대한 비즈니스 정당화

#### 포함 내용

```yaml
비즈니스 문제/기회 정의:
  - 현재 어떤 문제가 있는가?
  - 해결하지 않으면 어떤 손실이 발생하는가?
  - 예시: "수동 프로세스로 월 500시간 낭비, 연간 $120K 손실"

예상 투자 대비 수익 (ROI):
  - 초기 투자 비용
  - 예상 수익 또는 비용 절감
  - 손익분기점 (Break-even Point)
  - 예시: "18개월 후 ROI 150%"

대안 분석 (Alternatives Analysis):
  Option 1: 직접 개발 (Build)
    - 장점: 완전한 맞춤화, 내부 노하우 축적
    - 단점: 시간 오래 걸림, 초기 비용 높음
    - 추정 비용: $500K, 12개월

  Option 2: 구매 (Buy)
    - 장점: 빠른 도입, 검증된 솔루션
    - 단점: 커스터마이징 제한, 라이선스 비용
    - 추정 비용: $300K + 연간 $50K

  Option 3: 아웃소싱 (Outsource)
    - 장점: 전문성 활용, 리소스 유연성
    - 단점: 통제력 감소, 의존성 증가
    - 추정 비용: $400K, 9개월

리스크 & 기회:
  주요 리스크:
    - 기술 리스크: 새 기술 스택 학습 곡선
    - 시장 리스크: 경쟁사 선점 가능성
    - 운영 리스크: 레거시 시스템 통합 복잡도

  기회:
    - 시장 선도 기회
    - 신규 고객층 확보
    - 내부 역량 강화

추천 솔루션 & 근거:
  - 최종 추천: Option 1 (직접 개발)
  - 이유:
    1. 장기적 TCO 최소화
    2. 핵심 경쟁력 확보
    3. 확장성 요구사항 충족
```

#### 의사결정 지원

Business Case는 경영진이 다음을 판단하도록 돕습니다:

1. **Go**: 프로젝트 승인 및 예산 배정
2. **No-Go**: 프로젝트 보류 또는 취소
3. **Defer**: 시기 조정 후 재검토

---

### 📋 핵심 산출물 #3: Stakeholder Analysis (이해관계자 분석)

**정의**: 프로젝트에 영향을 주고받는 모든 사람들의 맵핑 및 전략 수립

#### 포함 내용

```yaml
주요 이해관계자 식별:
  내부:
    - C-Level (CEO, CTO, CFO)
    - 프로젝트 스폰서
    - 개발팀
    - IT 운영팀
    - 최종 사용자 부서

  외부:
    - 고객
    - 파트너사
    - 규제 기관
    - 벤더

영향력 & 관심도 매트릭스:
  High Power, High Interest (핵심 관리):
    - CTO, 프로젝트 스폰서
    - 전략: 긴밀한 협업, 정기 보고

  High Power, Low Interest (만족 유지):
    - CEO, CFO
    - 전략: 주요 의사결정만 보고

  Low Power, High Interest (지속 정보 제공):
    - 개발팀, 사용자 부서
    - 전략: 정기 업데이트, 피드백 수렴

  Low Power, Low Interest (모니터링):
    - 외부 파트너
    - 전략: 필요시에만 소통

기대사항 & 우려사항:
  CTO 기대사항:
    - 기술 혁신
    - 확장 가능한 아키텍처
    우려: 기술 부채 증가

  CFO 기대사항:
    - 예산 준수
    - 명확한 ROI
    우려: 예산 초과 가능성

  사용자 부서 기대사항:
    - 사용 편의성
    - 빠른 배포
    우려: 학습 곡선, 업무 중단

참여 전략 (Engagement Strategy):
  - 주간 스티어링 커미티 (CTO, 스폰서)
  - 월간 전체 보고회 (전체 이해관계자)
  - 분기별 사용자 워크샵 (최종 사용자)
  - 슬랙 채널 운영 (개발팀)
```

#### 목적

- **정치적 리스크 파악**: 누가 프로젝트를 막을 수 있는가?
- **커뮤니케이션 계획**: 누구에게 무엇을 언제 보고할 것인가?
- **지지 확보**: 프로젝트 성공을 위한 동맹 구축

---

## Phase 2: 요구사항 정의 (Requirements Phase)

**소요 시간**: 평균 2개월 (4-8주)

### 선택지: PRD vs SRS

엔터프라이즈 환경에서는 프로젝트 특성에 따라 선택:

| 구분 | PRD | SRS |
|:----:|:---:|:---:|
| **사용처** | 제품 중심 (SaaS, B2C) | 엔터프라이즈, 규제 산업 |
| **스타일** | 비즈니스 중심, 스토리텔링 | 기술 중심, 구조화 |
| **표준** | 없음 (회사마다 다름) | IEEE 830, ISO 29148 |
| **승인** | Product Owner | 기술위원회, 규제기관 |
| **예시 회사** | Amazon, Airbnb, Spotify | 은행, 의료, 국방 |

---

### 📋 산출물 Option 1: PRD (Product Requirements Document)

**정의**: 제품이 무엇을 해야 하는지를 비즈니스 관점에서 설명

#### 표준 구조

```markdown
# 1. Executive Summary
- 프로젝트 개요 (2-3 문장)
- 핵심 가치 제안
- 타겟 런칭 일정

# 2. 목표 & 비전
## 비즈니스 목표
- 시장 점유율 20% 증가
- 고객 이탈률 15% 감소
- NPS (Net Promoter Score) 70+ 달성

## 제품 비전
"중소기업이 5분 만에 글로벌 결제를 시작할 수 있게 한다"

# 3. 타겟 사용자 & 페르소나
## Primary Persona: 마케팅 담당자 Sarah (29세)
- 목표: 캠페인 성과 실시간 추적
- 좌절감: 여러 도구 사이 전환 피로
- 기술 수준: 중급 (Excel 능숙, SQL 모름)
- 사용 환경: 사무실 + 원격, 모바일 자주 사용

## Secondary Persona: 경영진 Mike (45세)
- 목표: 고수준 대시보드로 빠른 의사결정
- 좌절감: 데이터 신뢰성 낮음
- 기술 수준: 초급 (기본 기능만 사용)
- 사용 환경: 주로 태블릿

# 4. 핵심 기능 & 우선순위 (MoSCoW)

## Must Have (MVP 필수)
### Feature 1: 실시간 대시보드
- 설명: 주요 지표 5개를 실시간 표시
- 사용자 스토리:
  * "마케터로서, 실시간 전환율을 보고 싶다"
  * "경영진으로서, 매출 현황을 한눈에 파악하고 싶다"
- 성공 지표:
  * 대시보드 로딩 시간 < 2초
  * 데이터 갱신 주기 < 5분
  * 사용자 만족도 4.5/5.0 이상

### Feature 2: 알림 시스템
- 설명: 주요 이벤트 발생 시 알림 (이메일, 슬랙)
- 우선순위 이유: 사용자 인터뷰에서 #1 요청사항

## Should Have (중요하지만 연기 가능)
### Feature 3: 커스텀 리포트 생성
- 설명: 사용자가 직접 리포트 템플릿 만들기
- 연기 가능 이유: Power User만 사용 (전체의 20%)

## Could Have (있으면 좋음)
### Feature 4: AI 인사이트 추천
- 설명: AI가 데이터 패턴을 분석해 조언 제공
- 우선순위 낮은 이유: 기술 성숙도, MVP에 필수 아님

## Won't Have (이번에는 안 함)
### Feature 5: 소셜미디어 통합
- 제외 이유: 리소스 부족, 복잡도 높음
- 재검토 시점: Phase 2 (6개월 후)

# 5. 사용자 스토리 & 유즈케이스
## User Story 1: 실시간 모니터링
**As a** 마케팅 담당자
**I want to** 실시간으로 전환율을 보고
**So that** 캠페인 성과를 즉시 파악하고 조정할 수 있다

**Acceptance Criteria**:
- [ ] 전환율이 5분마다 자동 갱신
- [ ] 전일 대비 증감률 표시 (%, 화살표)
- [ ] 전환율이 목표치 이탈 시 알림
- [ ] 모바일에서도 동일하게 작동

## Use Case 1: 캠페인 성과 확인
**Actor**: 마케터
**Precondition**: 로그인 완료, 캠페인 실행 중
**Main Flow**:
1. 마케터가 대시보드 접속
2. 시스템이 최신 데이터 로딩 (< 2초)
3. 전환율, 클릭률, 비용 표시
4. 마케터가 특정 캠페인 클릭
5. 시스템이 상세 분석 표시

**Alternative Flow**:
3a. 데이터 로딩 실패 시
   - 시스템이 캐시된 데이터 표시
   - "데이터가 10분 전 데이터입니다" 경고

**Postcondition**: 마케터가 의사결정에 필요한 정보 획득

# 6. 기술적 제약사항
- 레거시 CRM 시스템과 API 통합 필수
- GDPR 준수 (EU 고객 데이터 처리)
- 99.9% 가용성 목표 (연간 8.76시간 다운타임)
- 동시 사용자 10,000명 지원

# 7. 성공 지표 (KPI)
## 비즈니스 KPI
- 사용자 활성화율 (Weekly Active Users): 60%+
- 고객 유지율 (Retention): 80%+ (3개월)
- NPS (Net Promoter Score): 70+

## 제품 KPI
- 평균 대시보드 로딩 시간: < 2초
- 알림 도달률: 95%+
- 버그 발생률: < 1% (세션당)

## 측정 방법
- Google Analytics 이벤트 트래킹
- Mixpanel 사용자 행동 분석
- 월간 사용자 서베이 (SurveyMonkey)

# 8. 마일스톤 & 타임라인
## Phase 1: MVP (3개월)
- Month 1: 인증 & 대시보드 기본
- Month 2: 데이터 시각화 & 알림
- Month 3: 테스트 & 버그 수정
- 목표: 100명 베타 사용자 확보

## Phase 2: 확장 (3개월)
- Month 4-6: 커스텀 리포트, 고급 필터
- 목표: 1,000명 유료 사용자

## Phase 3: 최적화 (진행 중)
- Month 7+: AI 인사이트, 통합 확대
```

#### 2025년 PRD 모범 사례

##### 1. 측정 가능한 요구사항
```
❌ 나쁜 예: "시스템은 빨라야 한다"
✅ 좋은 예: "95% 요청이 2초 이내 응답해야 한다"

❌ 나쁜 예: "사용자 친화적이어야 한다"
✅ 좋은 예: "신규 사용자가 튜토리얼 없이 5분 내 첫 리포트 생성 가능"
```

##### 2. 시각화 활용
- Figma/Sketch 프로토타입 임베드
- 사용자 플로우 다이어그램
- 와이어프레임
- "보는 것이 100줄 설명보다 나음"

##### 3. 협업 도구 사용
- **Notion**: 실시간 편집, 댓글, 버전 히스토리
- **Confluence**: 엔터프라이즈급 권한 관리
- **Miro**: 시각적 협업 (보드, 스티커노트)
- PDF는 더 이상 사용하지 않음!

##### 4. AI 도구 활용
- **PRD 생성기**: Context Engineering, Chisel, Oreate AI
- **자동 번역**: 다국어 팀 협업
- **요구사항 분석**: AI가 모순점 자동 감지
- 효율 향상: 최대 30%

##### 5. 유명 기업 사례

**Amazon: "Working Backwards" 방식**
```markdown
# 가상 보도자료 (Press Release)

[제품명] 출시 - 중소기업 결제 혁신

시애틀, 2025년 X월 X일 - Amazon은 오늘 [제품명]을 출시했다.
이 제품은 중소기업이 글로벌 결제를 5분 만에 시작할 수 있게 한다.

"기존에는 결제 시스템 구축에 수개월이 걸렸습니다.
이제는 5분이면 충분합니다." - 고객 A씨

주요 기능:
- 원클릭 결제 통합
- 150개국 통화 지원
- 실시간 사기 탐지

[제품명]은 월 $99부터 시작하며...

# FAQ (자주 묻는 질문)

Q: 기존 시스템과 어떻게 다른가?
A: 기존은 2-3개월 걸렸지만, 우리는 5분입니다.

Q: 보안은 어떻게 보장하나?
A: PCI-DSS Level 1 인증, 256-bit 암호화...
```
→ **장점**: 고객 관점에서 시작, 최종 가치 명확

**Figma: 비주얼 중심**
- PRD에 실제 프로토타입 임베드
- "이렇게 보입니다" > "이렇게 작동합니다"
- 디자인 → 개발 간극 최소화

---

### 📋 산출물 Option 2: SRS (Software Requirements Specification)

**정의**: 소프트웨어가 무엇을 해야 하는지를 기술적으로 명세

**표준**: IEEE 830-1998, ISO/IEC/IEEE 29148:2018

#### 언제 SRS를 사용하나?

```yaml
필수 조건:
  ✅ 규제 산업 (은행, 의료, 항공, 국방)
  ✅ 다중 팀 병렬 작업 (5개 이상 팀)
  ✅ 외부 벤더와 계약 (명확한 스펙 필요)
  ✅ 지속적 배포 (높은 변경 속도)
  ✅ 감사 추적 필요 (Audit Trail)

선택 조건:
  ⭕ 대규모 프로젝트 ($1M 이상, 10명 이상)
  ⭕ 복잡한 시스템 통합
  ⭕ 장기 유지보수 (5년 이상)
```

#### 표준 구조 (IEEE 830 기반)

````markdown
# 1. 소개 (Introduction)

## 1.1 목적 (Purpose)
이 문서는 [시스템명]의 요구사항을 정의한다.

대상 독자:
- 개발팀: 구현 가이드
- 테스트팀: 테스트 케이스 작성
- 프로젝트 관리자: 진행 상황 추적
- 고객/이해관계자: 승인 및 검토

## 1.2 범위 (Scope)
시스템명: 글로벌 결제 플랫폼 (GPP)

시스템 목표:
- 150개국 결제 지원
- 99.99% 가용성
- PCI-DSS 준수

혜택:
- 중소기업 글로벌 진출 가속화
- 결제 처리 시간 80% 단축
- 사기 손실 50% 감소

## 1.3 정의, 약어, 약어 (Definitions, Acronyms, Abbreviations)
- **API**: Application Programming Interface
- **PCI-DSS**: Payment Card Industry Data Security Standard
- **2FA**: Two-Factor Authentication
- **Acquirer**: 가맹점 은행
- **PSP**: Payment Service Provider

## 1.4 참조 문서 (References)
- ADR-001: API Gateway 선택 (Kong vs AWS API Gateway)
- ISO 8583: 금융 거래 메시지 표준
- PCI-DSS v4.0: 결제 보안 표준
- 프로젝트 헌장 v1.2 (2025-09-15)

## 1.5 개요 (Overview)
이 문서의 나머지 부분은 다음과 같이 구성:
- Section 2: 전체 시스템 설명
- Section 3: 기능 요구사항 (상세)
- Section 4: 비기능 요구사항
- Section 5: 기타 요구사항

---

# 2. 전체 설명 (Overall Description)

## 2.1 제품 관점 (Product Perspective)
[시스템 컨텍스트 다이어그램 삽입]

외부 인터페이스:
- 레거시 CRM (Salesforce)
- 결제 게이트웨이 (Stripe, PayPal)
- 사기 탐지 서비스 (Sift)
- 회계 시스템 (QuickBooks)

## 2.2 제품 기능 (Product Functions)
고수준 기능 목록:
- 사용자 인증 & 권한 관리
- 결제 처리 (신용카드, 은행 이체)
- 환율 변환 (실시간)
- 사기 탐지 & 리스크 관리
- 리포팅 & 분석

## 2.3 사용자 클래스 & 특성 (User Classes and Characteristics)
### 사용자 클래스 1: 가맹점 관리자
- 빈도: 매일 사용
- 기술 수준: 중급
- 주요 작업: 거래 모니터링, 정산 확인

### 사용자 클래스 2: 최종 소비자
- 빈도: 구매 시에만
- 기술 수준: 초급
- 주요 작업: 결제 완료

### 사용자 클래스 3: 시스템 관리자
- 빈도: 주간
- 기술 수준: 고급
- 주요 작업: 시스템 설정, 모니터링

## 2.4 운영 환경 (Operating Environment)
- **클라이언트**: Web (Chrome 90+, Safari 14+), iOS 15+, Android 11+
- **서버**: AWS (us-east-1, eu-west-1, ap-northeast-1)
- **데이터베이스**: PostgreSQL 14, Redis 7
- **메시징**: Kafka 3.x
- **모니터링**: Datadog, Sentry

## 2.5 설계 & 구현 제약사항 (Design and Implementation Constraints)
- **규제**: PCI-DSS v4.0 준수 필수
- **보안**: ISO 27001 인증 필요
- **언어**: 백엔드 Python 3.11+, 프론트엔드 TypeScript 5.0+
- **프레임워크**: FastAPI (백엔드), React 18 (프론트엔드)
- **레거시**: Salesforce API v58 통합 (변경 불가)

## 2.6 가정 & 의존성 (Assumptions and Dependencies)
**가정**:
- 사용자는 모던 브라우저 사용 (IE 미지원)
- 인터넷 연결 필수 (오프라인 모드 없음)
- 영어 & 한국어 지원 (초기)

**의존성**:
- Stripe API 안정성 (99.9% SLA)
- AWS 가용성
- 환율 API (exchangerate-api.com)

---

# 3. 기능 요구사항 (Functional Requirements)

## 3.1 사용자 인증 모듈

### FR-001: 사용자 등록
**우선순위**: 필수 (Must Have)
**출처**: Business Case Section 4.2

**설명**:
시스템은 신규 사용자가 이메일과 비밀번호로 계정을 생성할 수 있어야 한다.

**입력**:
- 이메일 주소 (유효성 검증 필요)
- 비밀번호 (8자 이상, 대소문자+숫자+특수문자)
- 이용약관 동의 (체크박스)

**처리**:
1. 이메일 중복 확인
2. 비밀번호 강도 검증
3. 비밀번호 해시화 (bcrypt, cost=12)
4. DB에 사용자 레코드 생성
5. 인증 이메일 발송

**출력**:
- 성공: User ID, "인증 이메일을 확인하세요" 메시지
- 실패: 오류 코드 및 메시지
  - E001: 이메일 이미 존재
  - E002: 비밀번호 요구사항 미충족
  - E003: 서버 오류

**비기능 요구사항 참조**:
- NFR-001 (성능): 2초 이내 응답
- NFR-010 (보안): bcrypt 해시화

**테스트 케이스 참조**: TC-001 ~ TC-005

---

### FR-002: 사용자 로그인
**우선순위**: 필수 (Must Have)
**출처**: Business Case Section 4.2

**설명**:
시스템은 등록된 사용자가 이메일과 비밀번호로 로그인할 수 있어야 한다.

**입력**:
- 이메일 주소
- 비밀번호

**처리**:
1. 이메일로 사용자 조회
2. 비밀번호 검증 (bcrypt.compare)
3. 로그인 실패 횟수 확인 (Redis)
   - 5회 실패 시 30분 계정 잠금
4. 성공 시:
   - JWT 액세스 토큰 생성 (1시간 유효)
   - JWT 리프레시 토큰 생성 (7일 유효)
   - Redis에 세션 저장
5. 로깅: structlog로 모든 시도 기록

**출력**:
- 성공: JWT 토큰들, User 정보 (민감 정보 제외)
- 실패:
  - E010: 이메일 또는 비밀번호 오류
  - E011: 계정 잠김 (30분 대기)
  - E012: 이메일 미인증

**비기능 요구사항 참조**:
- NFR-001 (성능): 1초 이내 응답
- NFR-011 (보안): Rate Limiting (1분당 5회)

**테스트 케이스 참조**: TC-006 ~ TC-012

---

### FR-003: 2단계 인증 (2FA)
**우선순위**: Should Have (Phase 2)
**출처**: Security Review Meeting 2025-10-20

**설명**:
사용자는 선택적으로 TOTP 기반 2FA를 활성화할 수 있어야 한다.

**입력**:
- 2FA 활성화 요청 (로그인 후)

**처리**:
1. TOTP Secret 생성 (pyotp 라이브러리)
2. QR 코드 생성 (Google Authenticator 호환)
3. 사용자에게 QR 코드 표시
4. 사용자가 6자리 코드 입력으로 확인
5. DB에 2FA 활성화 플래그 저장

**출력**:
- QR 코드 이미지 (Base64)
- Backup codes (10개, 일회용)

**후속 처리**:
- 이후 로그인 시 FR-002 후에 6자리 코드 추가 요구

**비기능 요구사항 참조**:
- NFR-015 (보안): TOTP RFC 6238 준수

**테스트 케이스 참조**: TC-013 ~ TC-017

---

## 3.2 결제 처리 모듈

### FR-010: 신용카드 결제
**우선순위**: 필수 (Must Have)
**출처**: PRD Section 4.1

**설명**:
시스템은 Stripe을 통해 신용카드 결제를 처리해야 한다.

**입력**:
- 카드 정보 (토큰화됨, PCI-DSS 준수)
- 결제 금액 (통화 코드 포함)
- 주문 ID
- 고객 ID

**처리**:
[상세 플로우 다이어그램 삽입]

1. 입력 검증
   - 금액 > 0
   - 지원 통화 확인 (150개국)
2. Stripe API 호출
   - Idempotency Key 생성 (중복 방지)
   - Payment Intent 생성
3. 3D Secure 처리 (필요 시)
4. 결제 승인 대기
5. 결과 처리:
   - 성공: 트랜잭션 기록, 영수증 이메일
   - 실패: 오류 로깅, 재시도 로직
6. Webhook으로 비동기 상태 업데이트

**출력**:
- 성공:
  - Transaction ID
  - 승인 코드
  - 결제 시각 (UTC)
- 실패:
  - 오류 코드 (Stripe 코드 매핑)
  - 사용자 친화적 메시지

**비기능 요구사항 참조**:
- NFR-002 (성능): p95 < 3초
- NFR-020 (보안): PCI-DSS Level 1
- NFR-030 (신뢰성): 재시도 3회, 지수 백오프

**테스트 케이스 참조**: TC-050 ~ TC-070

---

[FR-011 ~ FR-050: 생략, 실제로는 모든 기능 명세]

---

# 4. 비기능 요구사항 (Non-Functional Requirements)

## 4.1 성능 요구사항 (Performance Requirements)

### NFR-001: 응답 시간
**설명**:
- **로그인**: p95 < 1초
- **결제 처리**: p95 < 3초
- **대시보드 로딩**: p95 < 2초
- **API 엔드포인트**: p99 < 5초

**측정 방법**:
- New Relic APM 모니터링
- 매일 자동 성능 테스트 (JMeter)

**허용 범위**:
- p95 초과 시 경고
- p99 초과 또는 p95 2배 초과 시 심각

---

### NFR-002: 처리량 (Throughput)
**설명**:
- **동시 사용자**: 10,000명
- **TPS (Transactions Per Second)**: 500 TPS
- **피크 시간**: 평소 대비 3배 (블랙프라이데이 등)

**확장 전략**:
- 수평 확장 (Horizontal Scaling)
- Auto-scaling: CPU 70% 도달 시 인스턴스 추가
- Load Balancer: AWS ALB, Round-robin

---

### NFR-003: 리소스 사용
**설명**:
- **메모리**: 서버당 < 4GB
- **CPU**: 평균 < 50%
- **DB 연결**: 풀 크기 100, 최대 대기 5초

**모니터링**:
- Datadog 대시보드
- 알림: 메모리 3.5GB 초과 시

---

## 4.2 보안 요구사항 (Security Requirements)

### NFR-010: 인증 & 권한
**설명**:
- **인증**: JWT 기반 (HS256 알고리즘)
- **토큰 유효기간**: Access 1시간, Refresh 7일
- **비밀번호 해시**: bcrypt (cost=12)
- **세션 관리**: Redis (TTL 자동 만료)

**표준 준수**:
- OWASP Top 10 대응
- CWE/SANS Top 25 점검

---

### NFR-011: Rate Limiting
**설명**:
- **로그인**: IP당 1분 5회
- **API 호출**: 사용자당 시간당 1,000회
- **결제 시도**: 카드당 10분 3회

**구현**:
- Redis + Token Bucket 알고리즘
- 초과 시 HTTP 429 (Too Many Requests)

---

### NFR-012: 데이터 암호화
**설명**:
- **전송 중**: TLS 1.3
- **저장 시**: AES-256-GCM
  - 민감 정보: 카드 번호, SSN
  - 비민감 정보: 이름, 이메일 (평문)

**키 관리**:
- AWS KMS (Key Management Service)
- 키 로테이션: 90일마다

---

### NFR-013: 감사 로깅 (Audit Logging)
**설명**:
모든 보안 관련 이벤트를 기록:
- 로그인/로그아웃
- 권한 변경
- 결제 트랜잭션
- 관리자 작업

**로그 형식**: JSON (structlog)
```json
{
  "timestamp": "2025-11-10T08:30:00Z",
  "event": "user_login",
  "user_id": "U12345",
  "ip_address": "203.0.113.42",
  "user_agent": "Mozilla/5.0...",
  "result": "success"
}

**보관 기간**: 7년 (규제 요구사항)

---

## 4.3 사용성 요구사항 (Usability Requirements)

### NFR-020: 학습 용이성

**설명**:

- 신규 사용자가 튜토리얼 없이 **5분 내** 첫 결제 설정 완료
- 주요 작업은 **3클릭 이내** 도달

**검증**:

- 월 1회 사용성 테스트 (5명 신규 사용자)
- 목표: 80% 성공률

---

### NFR-021: 접근성 (Accessibility)

**설명**:

- **표준**: WCAG 2.1 Level AA 준수
- **스크린 리더** 완벽 지원 (NVDA, JAWS)
- **키보드 네비게이션**: 모든 기능 키보드만으로 사용 가능
- **색상 대비**: 최소 4.5:1

**검증 도구**:

- axe DevTools
- Lighthouse Accessibility Score > 90

---

### NFR-022: 국제화 (i18n)

**설명**:

- **Phase 1**: 영어, 한국어
- **Phase 2**: 일본어, 중국어 (간체/번체), 스페인어
- **날짜/시간**: 사용자 타임존 자동 감지
- **통화**: 150개국 통화 표시 (환율 자동 변환)

**구현**:

- React i18next
- 번역 파일: JSON (Crowdin 관리)

---

## 4.4 신뢰성 요구사항 (Reliability Requirements)

### NFR-030: 가용성 (Availability)

**설명**:

- **목표**: 99.99% (연간 52.6분 다운타임)
- **예정 점검**: 월 1회, 새벽 2-4시 (KST), 사전 공지

**계산**:

```
Uptime = (Total Time - Downtime) / Total Time
99.99% = (525,600분 - 52.6분) / 525,600분
```

**달성 전략**:

- Multi-AZ 배포 (AWS)
- Health Check: 30초마다
- Failover: 자동 (< 1분)

---

### NFR-031: 장애 복구 (Disaster Recovery)

**설명**:

- **RTO (Recovery Time Objective)**: 1시간
- **RPO (Recovery Point Objective)**: 5분
- **백업**: 매시간 증분, 매일 전체

**복구 절차**:

1. S3에서 최근 백업 복원 (15분)
2. 트랜잭션 로그 재생 (20분)
3. Health Check 통과 확인 (5분)
4. DNS 전환 (10분)

**훈련**: 분기별 DR Drill

---

### NFR-032: 오류 처리

**설명**:

- 모든 오류는 **사용자 친화적 메시지** 표시
- 기술적 세부사항은 **로그에만** 기록

**예시**:

```
❌ 나쁜 메시지: "NullPointerException at line 234"
✅ 좋은 메시지: "결제 처리 중 문제가 발생했습니다. 잠시 후 다시 시도해주세요."
```

**재시도 로직**:

- 네트워크 오류: 최대 3회, 지수 백오프 (1초, 2초, 4초)
- 결제 Timeout: 1회 재시도
- DB 연결 실패: Circuit Breaker 패턴

---

## 4.5 유지보수성 요구사항 (Maintainability Requirements)

### NFR-040: 코드 품질

**설명**:

- **Linting**: Ruff 0 violations
- **Type Checking**: MyPy strict mode 0 errors
- **Code Coverage**: 95% 이상 (unit + integration)
- **Complexity**: Cyclomatic Complexity < 10

**자동화**:

- Pre-commit hooks
- CI/CD 파이프라인 (GitHub Actions)
- SonarQube 정적 분석

---

### NFR-041: 문서화

**설명**:

- **API 문서**: OpenAPI 3.0 (자동 생성)
- **코드 주석**: 모든 public 함수/클래스
- **ADR**: 주요 아키텍처 결정 기록
- **Runbook**: 운영 절차 (장애 대응, 배포)

**업데이트 주기**:

- API 문서: 코드 변경 시 자동
- ADR: 결정 시점
- Runbook: 분기별 검토

---

### NFR-042: 모니터링 & 알림

**설명**:

- **APM**: Datadog (모든 서비스)
- **로그**: CloudWatch Logs (7일 보관)
- **메트릭**:
  - 시스템: CPU, 메모리, 네트워크
  - 비즈니스: TPS, 결제 성공률, 오류율

**알림 규칙**:

- Critical: PagerDuty (SMS + 전화)
  - 가용성 < 99.9%
  - p95 응답시간 2배 초과
- Warning: Slack 채널
  - CPU > 70%
  - 오류율 > 1%

---

## 4.6 확장성 요구사항 (Scalability Requirements)

### NFR-050: 수평 확장

**설명**:

- **Stateless 서버**: 세션은 Redis에 저장
- **Auto-scaling**: ECS Fargate
  - Scale-out: CPU > 70%
  - Scale-in: CPU < 30% (10분 유지)
- **최대 인스턴스**: 50개

---

### NFR-051: 데이터베이스 확장

**설명**:

- **Read Replica**: 3개 (지역별 1개)
- **Sharding**: User ID 기반 (필요 시)
- **Connection Pooling**: PgBouncer

---

## 4.7 규제 준수 요구사항 (Compliance Requirements)

### NFR-060: PCI-DSS v4.0

**설명**:

- **Level 1** 인증 필요 (연 600만 건 이상)
- **요구사항**:
  - 카드 데이터 저장 금지 (토큰화)
  - 네트워크 세그멘테이션
  - 분기별 취약점 스캔
  - 연 1회 침투 테스트

**검증**: QSA (Qualified Security Assessor) 감사

---

### NFR-061: GDPR (General Data Protection Regulation)

**설명**:

- **데이터 주체 권리**:
  - 열람 요청: 30일 내 응답
  - 삭제 요청: 즉시 처리 (백업 제외 90일)
  - 이동 요청: JSON 포맷 제공
- **동의 관리**: Opt-in (명시적 동의)
- **데이터 처리자 계약**: 모든 벤더와 체결

---

### NFR-062: SOC 2 Type II

**설명**:

- **Trust Service Criteria**:
  - Security
  - Availability
  - Confidentiality
- **감사 주기**: 연 1회
- **증거 자료**: 로그, 정책 문서, 변경 기록

---

# 5. 기타 요구사항 (Other Requirements)

## 5.1 법적 요구사항

- 이용약관, 개인정보 처리방침 동의 필수
- 환불 정책 명시 (14일 이내)

## 5.2 표준 준수

- REST API: RFC 7231 (HTTP/1.1 Semantics)
- JSON: RFC 8259
- JWT: RFC 7519

## 5.3 패키징 & 배포

- **컨테이너**: Docker
- **오케스트레이션**: Kubernetes (EKS)
- **배포 전략**: Blue-Green Deployment
- **롤백**: 5분 내 이전 버전으로 복구

---

# 6. 부록 (Appendices)

## 6.1 시각 자료

### 시스템 아키텍처 다이어그램

[고수준 아키텍처 다이어그램 삽입]

### ER Diagram

[데이터베이스 스키마 다이어그램 삽입]

### Use Case Diagram

[UML Use Case 다이어그램 삽입]

### Sequence Diagram: 결제 플로우

[결제 처리 시퀀스 다이어그램 삽입]

## 6.2 요구사항 추적 매트릭스 (RTM)

| Req ID  | Description   | Priority | Source  | Test Cases | Status     |
| ------- | ------------- | -------- | ------- | ---------- | ---------- |
| FR-001  | 사용자 등록   | Must     | BC 4.2  | TC-001~005 | ✅ Approved |
| FR-002  | 사용자 로그인 | Must     | BC 4.2  | TC-006~012 | ✅ Approved |
| FR-010  | 신용카드 결제 | Must     | PRD 4.1 | TC-050~070 | 🟡 Review   |
| NFR-001 | 응답 시간     | Must     | SLA     | TC-500~505 | ✅ Approved |

## 6.3 용어집 (Glossary)

- **Idempotency**: 동일한 요청을 여러 번 보내도 결과가 같음
- **Circuit Breaker**: 장애 전파를 막기 위해 요청을 차단하는 패턴
- **Token Bucket**: Rate limiting 알고리즘의 일종

---

**문서 버전**: 1.0
**최종 수정일**: 2025-11-10
**승인자**: [CTO 서명], [프로젝트 스폰서 서명]
**다음 검토일**: 2025-12-10
````

#### 2025년 SRS 모범 사례

##### 1. 협업 플랫폼 사용

```notion
❌ 나쁜 방식: Word 문서 이메일로 주고받기
   - 버전 충돌
   - 댓글 추적 어려움
   - 승인 프로세스 불명확

✅ 좋은 방식: Confluence, Notion
   - 실시간 편집
   - 인라인 댓글
   - 버전 히스토리 자동 관리
   - 역할 기반 권한 (읽기/쓰기/승인)
```

##### 2. 요구사항 관리 도구

대규모 프로젝트 (100+ 요구사항):
- Perforce ALM
- Jama Connect
- IBM DOORS

중소 규모:
- Jira Requirements
- Confluence + 플러그인

**언제 필요?**
- 다중 팀 병렬 작업 (5개 이상)
- 규제 산업 (금융, 의료)
- 지속적 배포 환경
- 변경 추적 필수

##### 3. 측정 가능성

모든 비기능 요구사항은 정량화:

```markdown
❌ "빨라야 한다"
✅ "p95 응답시간 < 2초"

❌ "안정적이어야 한다"
✅ "99.99% 가용성 (연 52분 다운타임)"

❌ "사용하기 쉬워야 한다"
✅ "신규 사용자 5분 내 첫 작업 완료 (80% 성공률)"
```

##### 4. 시각화

다이어그램 필수:
- System Context Diagram (컨텍스트)
- ER Diagram (데이터베이스)
- Sequence Diagram (주요 플로우)
- State Diagram (상태 머신)

도구:
- Draw.io (무료)
- Lucidchart (유료, 협업 강력)
- PlantUML (코드로 작성, Git 친화적)
##### 5. 요구사항 추적 매트릭스 (RTM)

모든 요구사항을:
- 출처로 추적 (Business Case, User Story)
- 테스트로 추적 (Test Cases)
- 구현으로 추적 (Jira Tickets)

예시:

```markdown
FR-001 (사용자 등록)
  ← Business Case Section 4.2
  → TC-001, TC-002, TC-003
  → JIRA-1234, JIRA-1235
```

------

## Phase 3: 아키텍처 설계 (Architecture Phase)

**소요 시간**: 2주

### 📋 핵심 산출물: ADR (Architecture Decision Records)

**정의**: 중요한 아키텍처 결정과 그 근거를 기록하는 문서

#### ADR의 목적

```yaml
투명성:
  - 왜 이 기술을 선택했는지 명확히
  - 다른 대안은 무엇이었는지
  - 어떤 트레이드오프가 있는지

지식 공유:
  - 신입 개발자 온보딩
  - 팀 간 컨텍스트 공유
  - 미래의 나 자신에게

감사 추적 (Audit Trail):
  - 규제 산업 필수
  - 의사결정 과정 증명
  - 책임 소재 명확화

리팩토링 가이드:
  - "왜 이렇게 만들었지?" → ADR 참조
  - 변경 시 영향도 파악
```

#### 표준 템플릿 (Michael Nygard)

```markdown
# ADR-[번호]: [간결한 제목]

## Status
[Proposed | Accepted | Deprecated | Superseded]

## Context
### 문제 상황
어떤 문제를 해결하려 하는가?

### 비즈니스 제약사항
- 예산: $X 이내
- 일정: Y주 이내
- 팀: Z명

### 기술적 제약사항
- 레거시 시스템: ABC와 통합 필수
- 성능 목표: TPS 500+
- 보안 요구사항: PCI-DSS Level 1

### 품질 속성 우선순위
1. 성능 (가장 중요)
2. 확장성
3. 보안
4. 개발 속도

## Decision
무엇을 선택했는가?

### 선택한 솔루션
[구체적 기술/패턴/아키텍처]

### 구현 방법
간략한 구현 가이드라인

## Alternatives Considered
### Option 1: [대안 1]
**장점**:
- ...

**단점**:
- ...

**비용**: $X, Y주

**기각 이유**: ...

### Option 2: [대안 2]
...

## Consequences
### 긍정적 효과
- ...

### 부정적 효과 (트레이드오프)
- ...

### 향후 영향
- 다음에 이런 결정을 할 때 영향
- 유지보수 비용
- 기술 부채 발생 가능성

## Compliance & Risk
### 규제 준수
- PCI-DSS: 해당 없음
- GDPR: 개인정보 처리 없음

### 리스크
- 라이브러리 지원 중단 가능성: 낮음
- 성능 목표 미달 가능성: 중간

## Related Decisions
- ADR-005: API Gateway 선택
- ADR-010: 인증 방식 결정

## Notes
- 작성일: 2025-11-10
- 작성자: Jason
- 참여자: 1호, 2호, 개발팀
- 승인자: CTO
```

#### ADR 예시 모음

**예시 1: 웹 프레임워크 선택**
```markdown
# ADR-001: FastAPI vs Flask vs Django 선택

## Status
Accepted (2025-11-09)

## Context
### 문제 상황
새로운 결제 API 서버를 구축해야 한다.
요구사항:
- REST API만 제공 (프론트엔드 별도)
- 비동기 처리 필수 (외부 API 호출 많음)
- 타입 안정성 필요 (팀에 Python 신입 많음)
- 자동 API 문서 필요 (외부 파트너 통합)

### 제약사항
- 팀은 Python 경험 있음 (Flask 2년)
- 예산: 학습 곡선 최대 2주
- 일정: 3개월 내 MVP

### 품질 속성 우선순위
1. 성능 (비동기 처리)
2. 개발자 경험 (타입 안정성, 자동 문서)
3. 유지보수성

## Decision
**FastAPI 선택**

이유:
1. 네이티브 async/await 지원 → 성능 향상
2. Pydantic 기반 자동 검증 → 버그 감소
3. 자동 OpenAPI 문서 생성 → 외부 통합 용이
4. 타입 힌트 강제 → MyPy 호환, 신입 실수 방지

## Alternatives Considered
### Option 1: Flask + Flask-RESTX
**장점**:
- 팀 익숙함 (학습 곡선 0)
- 생태계 성숙 (플러그인 풍부)
- 프로덕션 검증됨

**단점**:
- 비동기 지원 약함 (Flask 2.0부터 지원이지만 생태계 미성숙)
- 타입 안정성 없음 (수동 검증 필요)
- API 문서 자동 생성 약함

**비용**: 0주 학습, 개발 4개월 (수동 검증 코드 추가)

**기각 이유**: 비동기 처리 부족으로 성능 목표 달성 어려움

### Option 2: Django REST Framework
**장점**:
- Full-stack 기능 (ORM, Admin 등)
- 검증된 보안 (OWASP Top 10 대응)
- 대규모 커뮤니티

**단점**:
- 오버헤드 큼 (ORM, Template 불필요)
- 학습 곡선 높음 (Django 방식 습득 필요)
- 비동기 지원 제한적

**비용**: 3주 학습, 개발 3.5개월

**기각 이유**: API만 필요한데 Full-stack은 과함

### Option 3: Node.js (Express)
**장점**:
- 비동기 네이티브
- NPM 생태계

**단점**:
- 팀 Python 경험만 있음
- 학습 곡선 높음 (언어 전환)

**기각 이유**: 팀 역량 불일치

## Consequences
### 긍정적 효과
✅ 성능: Flask 대비 2-3배 빠름 (벤치마크 결과)
✅ 타입 안정성: MyPy strict mode 통과 → 런타임 버그 70% 감소 (예상)
✅ 자동 문서: /docs 엔드포인트로 Swagger UI 자동 제공
✅ 개발 속도: Pydantic 자동 검증으로 boilerplate 50% 감소

### 부정적 효과 (트레이드오프)
❌ 학습 곡선: 팀 2주 학습 필요 (async/await, Pydantic)
❌ 생태계: Flask보다 작음 (일부 플러그인 없음)
   → 완화 전략: 필요 시 직접 구현 또는 기여
❌ 안정성: 상대적으로 신생 (2018년 출시)
   → 완화 전략: 프로덕션 사례 조사 (Uber, Microsoft 사용 확인)

### 향후 영향
- 다른 마이크로서비스도 FastAPI로 표준화 예상
- 팀 역량 향상 (비동기 프로그래밍, 타입 힌트)
- 기술 블로그 작성 기회 (사례 공유)

## Compliance & Risk
### 규제 준수
- PCI-DSS: FastAPI 자체는 영향 없음 (구현에 달림)
- OWASP Top 10: 기본 보안 기능 있음 (CSRF, CORS)

### 리스크
- 프로젝트 지원 중단: 낮음 (활발한 개발, Tiangolo 전담)
- 성능 목표 미달: 매우 낮음 (벤치마크 검증 완료)
- 팀 학습 실패: 중간 → 2주 교육 프로그램 실행

## Related Decisions
- ADR-002: Pydantic v2 선택 (FastAPI와 시너지)
- ADR-010: OpenAPI 문서 자동화 (FastAPI 기본 기능 활용)

## Notes
- 작성일: 2025-11-09
- 작성자: Jason
- 리뷰어: 1호, 2호, 개발팀 (5명)
- 승인자: CTO (2025-11-10)
- 회의 기록: Notion "기술 선택 회의 2025-11-09"

## Follow-up Actions
- [ ] FastAPI 교육 자료 준비 (담당: Jason)
- [ ] 2주 학습 프로그램 일정 수립
- [ ] Hello World 프로젝트 구축 (템플릿)
- [ ] 벤치마크 환경 구축 (성능 검증)
```

---

**예시 2: 데이터베이스 선택**
```markdown
# ADR-005: PostgreSQL vs MySQL vs MongoDB 선택

## Status
Accepted (2025-11-12)

## Context
### 문제 상황
결제 트랜잭션, 사용자 정보, 감사 로그를 저장할 DB 필요

### 요구사항
- ACID 트랜잭션 필수 (결제 데이터)
- 복잡한 조인 쿼리 (리포팅)
- 시계열 데이터 (로그)
- 확장성 (샤딩 가능)

### 제약사항
- 팀 PostgreSQL 경험 있음
- 클라우드: AWS
- 예산: RDS 비용 고려

## Decision
**PostgreSQL 14+ 선택**

이유:
1. ACID 보장 → 결제 무결성
2. JSONB 타입 → 유연한 스키마 (로그)
3. 파티셔닝 → 시계열 데이터 효율
4. AWS RDS 완벽 지원
5. PostGIS 확장 (향후 위치 기반 필요 시)

## Alternatives Considered
### Option 1: MySQL 8.0
**장점**:
- Read 성능 (InnoDB)
- 넓은 커뮤니티

**단점**:
- 복잡한 쿼리 성능 낮음
- JSON 지원 약함

**기각 이유**: 리포팅 쿼리 복잡도

### Option 2: MongoDB
**장점**:
- 스키마 유연성
- 수평 확장 쉬움

**단점**:
- ACID 트랜잭션 제한적
- 조인 성능 낮음

**기각 이유**: 결제 데이터 무결성 필수

## Consequences
### 긍정적
✅ 트랜잭션 안정성
✅ 복잡한 분석 쿼리 가능
✅ JSONB로 로그 유연 저장

### 부정적
❌ Write 성능 MySQL보다 약간 낮음
   → 완화: Connection Pooling, Prepared Statements
❌ 샤딩 복잡함
   → 완화: Citus 확장 사용 (필요 시)

## Compliance & Risk
- PCI-DSS: 암호화 at-rest, at-transit 필요 (RDS 기능)
- GDPR: 개인정보 삭제 가능 (CASCADE 설정)

## Related Decisions
- ADR-006: PgBouncer 연결 풀링
- ADR-007: TimescaleDB 시계열 확장 (Phase 2)

## Notes
- 승인일: 2025-11-12
- 벤치마크: pgbench 결과 첨부
```

---

#### ADR Best Practices (2025)

##### 1. 하나의 ADR = 하나의 결정
```
❌ 나쁜 예: "백엔드 기술 스택 선택"
   - FastAPI, PostgreSQL, Redis, Docker 전부 포함
   - 너무 넓음, 추적 어려움

✅ 좋은 예:
   - ADR-001: 웹 프레임워크 선택 (FastAPI)
   - ADR-005: 데이터베이스 선택 (PostgreSQL)
   - ADR-008: 캐시 선택 (Redis)
   - ADR-012: 컨테이너화 (Docker)
   → 각각 독립적으로 추적, 변경, 폐기 가능
```

##### 2. 간결하게 (1-2페이지)
```
목표: 5분 내 읽기 가능

구조:
- Context: 0.5페이지
- Decision: 0.25페이지
- Alternatives: 0.5페이지
- Consequences: 0.5페이지
- 기타: 0.25페이지

합계: 2페이지
```

##### 3. 정량적 근거 포함
```
❌ "FastAPI가 더 빠르다"
✅ "FastAPI는 Flask 대비 2-3배 빠름 (벤치마크: 5,000 req/s vs 2,000 req/s)"

❌ "PostgreSQL이 안정적이다"
✅ "PostgreSQL ACID 완벽 지원, MySQL은 일부 스토리지 엔진만 지원"

❌ "팀이 익숙하다"
✅ "팀 5명 중 4명이 2년 이상 경험 (설문조사 결과)"
```

##### 4. Git에 Markdown으로 저장
```
프로젝트 구조:
docs/
├── adr/
│   ├── 0001-fastapi-선택.md
│   ├── 0002-pydantic-v2-선택.md
│   ├── 0005-postgresql-선택.md
│   └── README.md (index)
└── ...

장점:
✅ 버전 관리 (누가 언제 변경했는지)
✅ Pull Request 리뷰 (팀 합의 프로세스)
✅ 검색 용이 (grep, GitHub 검색)
✅ CI/CD 통합 (ADR 없으면 PR 머지 차단)
```

##### 5. 구현 전에 작성
```
타이밍:
1. 기술 조사 (Research)
2. ADR 초안 작성
3. 팀 리뷰 (30-45분 회의)
4. ADR 승인
5. 구현 시작

❌ 나쁜 타이밍: 구현 후 작성 (사후 정당화)
✅ 좋은 타이밍: 의사결정 직후, 구현 전
```

##### 6. 상태 관리
```
Status 라이프사이클:
Proposed → Accepted → [Deprecated | Superseded]

- Proposed: 제안됨, 리뷰 중
- Accepted: 승인됨, 현재 적용 중
- Deprecated: 더 이상 권장 안 함 (이유 명시)
- Superseded: 다른 ADR로 대체됨 (링크 명시)

예시:
# ADR-001: Flask 선택
Status: Superseded by ADR-010 (FastAPI 선택)
```

##### 7. 회의 효율화
```
ADR 리뷰 회의 가이드:

준비 (회의 전):
- ADR 초안 공유 (최소 2일 전)
- 팀원들이 미리 읽고 댓글

회의 (30-45분):
- 5분: Context 설명
- 10분: Decision & Alternatives 토론
- 10분: Consequences 논의
- 5분: 투표 또는 합의
- 5분: Action Items 정리

결과:
- Status 업데이트 (Proposed → Accepted)
- 승인자 서명
- Git commit & Push
```

##### 8. 도구 활용
```
ADR 템플릿 생성기:
- adr-tools (CLI)
  $ adr new "FastAPI vs Flask 선택"
  → docs/adr/0001-fastapi-vs-flask-선택.md 생성

- VSCode 확장:
  - ADR Manager
  - Markdown ADR

저장소:
- GitHub: 프로젝트 루트에 /docs/adr/
- Confluence: ADR 전용 스페이스
- Notion: 데이터베이스로 관리
```

---

#### 실전 사례: AWS의 ADR 활용

**AWS Architecture Blog (2025년 3월)**
> "200개 이상의 ADR을 작성한 결과:
> - 팀 정렬 시간 60% 단축
> - 아키텍처 리팩토링 비용 40% 감소
> - 신입 온보딩 기간 2주 → 3일
> - 의사결정 재논의 90% 감소"

**핵심 교훈**:
1. ADR은 **투자**다 (작성 30분 vs 혼란 해소 3일)
2. **정량적 근거**가 핵심 (감정이 아닌 데이터)
3. **검색 가능성**이 중요 (Git > 위키 > 이메일)
4. **살아있는 문서**로 유지 (상태 업데이트)

---

## Phase 4: 개발 계획 (Planning Phase)

**소요 시간**: 2주

### 📋 핵심 산출물

#### 1. 개발 방법론 선택

**2025년 주류: Agile (특히 Scrum)**

```yaml
Agile 방법론:
  특징:
    - 2주 스프린트 (Sprint)
    - 데일리 스탠드업 (15분)
    - 스프린트 리뷰 & 회고
    - 백로그 우선순위화

  적합한 경우:
    ✅ 요구사항 변동 많음
    ✅ 빠른 피드백 필요
    ✅ 점진적 배포 가능
    ✅ 크로스펑셔널 팀

  부적합한 경우:
    ❌ 규제 산업 (엄격한 문서화)
    ❌ 고정된 요구사항
    ❌ 순차적 의존성 (A → B → C)

Waterfall 방법론:
  특징:
    - 순차적 단계 (Requirements → Design → Development → Test)
    - 단계별 완료 후 다음 단계
    - 문서 중심

  적합한 경우:
    ✅ 요구사항 명확하고 고정
    ✅ 규제 산업 (문서 필수)
    ✅ 외부 계약 (고정 범위)

  부적합한 경우:
    ❌ 요구사항 불확실
    ❌ 빠른 시장 출시 필요
    ❌ 혁신적 제품

Hybrid (Wagile):
  특징:
    - 계획은 Waterfall (명확한 마일스톤)
    - 개발은 Agile (스프린트)

  적합한 경우:
    ✅ 대기업 (거버넌스 필요)
    ✅ 고정 예산 & 일정
    ✅ 유연한 구현 방식
```

#### 2. 기술 스택 결정

**기술 선택 체크리스트**:

```markdown
# 기술 스택 결정 문서

## 1. 백엔드
### 언어
- **선택**: Python 3.11+
- **근거**: ADR-001 (팀 역량, 타입 안정성, 생태계)
- **대안**: Node.js (팀 역량 부족), Go (학습 곡선)

### 프레임워크
- **선택**: FastAPI 0.104+
- **근거**: ADR-001 (비동기, 자동 문서, 타입)
- **대안**: Flask (비동기 약함), Django (오버헤드)

### 데이터베이스
- **선택**: PostgreSQL 14+
- **근거**: ADR-005 (ACID, JSONB, 복잡 쿼리)
- **대안**: MySQL (JSON 약함), MongoDB (ACID 약함)

### 캐싱
- **선택**: Redis 7+
- **근거**: ADR-008 (성능, Pub/Sub, 세션)
- **대안**: Memcached (기능 부족)

### 메시징
- **선택**: Kafka 3.x
- **근거**: ADR-012 (이벤트 소싱, 확장성)
- **대안**: RabbitMQ (낮은 처리량), SQS (AWS 종속)

## 2. 프론트엔드
### 프레임워크
- **선택**: React 18+ with TypeScript
- **근거**: ADR-020 (컴포넌트 재사용, 타입 안정성)
- **대안**: Vue (팀 경험 없음), Angular (복잡함)

### 상태 관리
- **선택**: Zustand
- **근거**: ADR-021 (단순함, 타입 안전)
- **대안**: Redux (boilerplate), Context API (성능)

### UI 라이브러리
- **선택**: shadcn/ui + Tailwind CSS
- **근거**: ADR-022 (커스터마이징, 접근성)
- **대안**: Material-UI (무거움), Ant Design (중국 중심)

## 3. 인프라
### 클라우드
- **선택**: AWS
- **근거**: ADR-030 (팀 경험, 서비스 다양성)
- **대안**: GCP (경험 없음), Azure (MS 종속)

### 컨테이너
- **선택**: Docker + Kubernetes (EKS)
- **근거**: ADR-031 (표준, 확장성)
- **대안**: ECS (AWS 종속), Nomad (작은 생태계)

### CI/CD
- **선택**: GitHub Actions
- **근거**: ADR-032 (GitHub 통합, 무료 tier)
- **대안**: GitLab CI (마이그레이션 비용), Jenkins (유지보수)

### 모니터링
- **선택**: Datadog
- **근거**: ADR-033 (통합 모니터링, APM, 로그)
- **대안**: New Relic (비용), Prometheus+Grafana (운영 부담)

## 4. 보안
### 인증
- **선택**: JWT (Access/Refresh Token)
- **근거**: ADR-040 (Stateless, 확장성)
- **대안**: Session (확장 어려움), OAuth only (복잡)

### 비밀 관리
- **선택**: AWS Secrets Manager
- **근거**: ADR-041 (자동 로테이션, 감사)
- **대안**: HashiCorp Vault (운영 복잡), 환경 변수 (보안 약함)

## 5. 테스트
### 유닛 테스트
- **선택**: pytest
- **근거**: ADR-050 (Python 표준, fixture)
- **대안**: unittest (boilerplate)

### E2E 테스트
- **선택**: Playwright
- **근거**: ADR-051 (크로스 브라우저, 빠름)
- **대안**: Selenium (느림), Cypress (Chromium만)

## 요약 다이어그램
[기술 스택 아키텍처 다이어그램 삽입]
```

#### 3. 리소스 & 일정 계획

```yaml
팀 구성:
  Backend 팀 (3명):
    - Tech Lead 1명 (5년 경험)
    - Senior 1명 (3년)
    - Junior 1명 (1년)

  Frontend 팀 (2명):
    - Senior 1명 (4년)
    - Mid-level 1명 (2년)

  DevOps (1명):
    - Senior 1명 (CI/CD, 인프라)

  QA (1명):
    - QA Engineer (테스트 자동화)

  Product Owner (1명):
    - 우선순위 결정, 이해관계자 관리

  Scrum Master (1명):
    - 프로세스 촉진, 장애물 제거

마일스톤:
  M1 - MVP (12주):
    - Week 1-2: 환경 구축 (Bootstrap)
    - Week 3-6: 핵심 기능 (인증, 결제)
    - Week 7-10: 통합 & 테스트
    - Week 11-12: 베타 출시
    목표: 100명 베타 사용자

  M2 - Public Launch (24주):
    - Week 13-18: 추가 기능 (리포팅, 알림)
    - Week 19-22: 성능 최적화
    - Week 23-24: 프로덕션 출시
    목표: 1,000명 유료 사용자

  M3 - Scale (ongoing):
    - Week 25+: 확장 기능, AI 통합
    목표: 10,000명 사용자

예산:
  인건비: $X (인당 $Y × 8명 × 6개월)
  클라우드: $Z/월 (초기 낮음, 점진 증가)
  도구/라이선스: $W (Datadog, 도메인, 등)
  비상 예비비: 20% (예상치 못한 비용)

리스크 완화:
  기술 리스크:
    - FastAPI 학습 곡선 → 2주 교육
    - Kafka 운영 복잡도 → Phase 2로 연기, 초기 SQS 사용

  일정 리스크:
    - 주요 개발자 휴가 → 백업 플랜, 지식 공유
    - 외부 API 지연 → Mock 서버 우선 개발

  예산 리스크:
    - 클라우드 비용 초과 → 주간 모니터링, 알림 설정
    - 추가 인력 필요 → 비상 예비비 활용
```

---

## 🕐 엔터프라이즈 초기 단계 타임라인

```
Week 1-2: Project Initiation (프로젝트 개시)
├── Day 1-3: Project Charter 작성
│   - 프로젝트 스폰서와 협의
│   - 범위, 목표, 이해관계자 정의
├── Day 4-7: Business Case 개발
│   - ROI 분석
│   - 대안 비교 (Build/Buy/Outsource)
│   - 경영진 프레젠테이션 준비
└── Day 8-10: Stakeholder Analysis
    - 이해관계자 맵핑
    - 참여 전략 수립
    - 승인: 경영진 Go/No-Go 결정 ⭐

─────────────────────────────────

Week 3-10: Requirements (요구사항 정의) - 평균 2개월
├── Week 3-4: 비즈니스 요구사항 수집
│   - 이해관계자 인터뷰
│   - 워크샵 (5-10명, 2-3일)
│   - 사용자 페르소나 작성
├── Week 5-7: PRD/SRS 작성
│   - 기능 요구사항 (Functional)
│   - 비기능 요구사항 (Non-Functional)
│   - 시각화 (다이어그램, 프로토타입)
├── Week 8-9: 리뷰 & 검증
│   - 기술팀 리뷰
│   - 이해관계자 검토
│   - 우선순위 재조정 (MoSCoW)
└── Week 10: 승인
    - 프로젝트 스폰서 최종 승인 ⭐
    - Baseline 설정 (변경 통제 시작)

─────────────────────────────────

Week 11-12: Architecture (아키텍처 설계)
├── Week 11: 주요 결정사항 도출
│   - 기술 스택 후보 선정
│   - 아키텍처 패턴 논의
│   - POC (Proof of Concept) 필요 시 진행
├── Week 12: ADR 작성
│   - 각 주요 결정사항마다 ADR
│   - 팀 리뷰 회의 (30-45분/ADR)
│   - CTO 승인 ⭐
└── 산출물: ADR 5-10개
    예시: 프레임워크, DB, 인증, 배포 전략

─────────────────────────────────

Week 13-14: Planning (개발 계획)
├── Week 13: 방법론 & 프로세스
│   - Agile/Scrum/Waterfall 선택
│   - 스프린트 주기 결정 (보통 2주)
│   - 도구 선택 (Jira, GitHub, Confluence)
├── Week 14: 리소스 & 일정
│   - 팀 구성 확정
│   - WBS (Work Breakdown Structure)
│   - 마일스톤 & 타임라인
│   - 예산 최종 확정
└── 산출물:
    - 프로젝트 계획서
    - 리소스 배정표
    - 리스크 관리 계획

─────────────────────────────────

Week 15: Go/No-Go Decision (최종 승인)
├── 모든 문서 준비 완료 확인
│   ✅ Project Charter
│   ✅ Business Case
│   ✅ PRD/SRS
│   ✅ ADR 5-10개
│   ✅ Project Plan
├── 최종 리뷰 미팅
│   - 경영진 + 프로젝트 스폰서 + 팀
│   - 모든 리스크 재검토
│   - 예산 & 일정 최종 확인
└── 승인 → 개발 시작 🚀

─────────────────────────────────

총 소요 시간: 약 15주 (3.5개월)
→ 개발 시작
```

**주요 승인 게이트 (Go/No-Go)**:
1. **Week 2**: 프로젝트 개시 승인
2. **Week 10**: 요구사항 승인
3. **Week 12**: 아키텍처 승인
4. **Week 15**: 최종 개발 시작 승인

---

## 🎯 2025년 주요 트렌드

### 1. AI 도구 활용

```yaml
초기 단계 AI 활용:
  요구사항 분석:
    - 사용자 인터뷰 → AI 자동 요약
    - 요구사항 모순 자동 감지
    - 숨겨진 의존성 발견

  PRD/SRS 작성:
    - AI PRD Generator (30% 효율 향상)
    - 템플릿 자동 채우기
    - 다국어 번역 (실시간)

  ADR 작성:
    - 기술 비교 자동 조사
    - 벤치마크 데이터 수집
    - 유사 사례 검색

도구:
  - Context Engineering (PRD 생성)
  - ChatGPT/Claude (초안 작성)
  - Grammarly (문서 교정)
```

### 2. 협업 플랫폼

```yaml
정적 문서 → 실시간 협업:
  Confluence:
    - 역할 기반 권한
    - 인라인 댓글
    - 버전 히스토리
    - 승인 워크플로우

  Notion:
    - 데이터베이스 (요구사항 트래킹)
    - 칸반 보드
    - 타임라인 뷰

  Miro:
    - 시각적 협업
    - 화이트보드
    - 워크샵 템플릿

특징:
  ✅ 여러 명이 동시 편집
  ✅ 변경 이력 자동 추적
  ✅ Slack/Teams 통합 알림
  ✅ 모바일 앱
```

### 3. 측정 가능성 강조

```yaml
모호한 요구사항 금지:
  ❌ "빨라야 한다"
  ✅ "p95 응답시간 < 2초"

  ❌ "안정적이어야 한다"
  ✅ "99.99% 가용성 (연 52분 다운타임)"

  ❌ "사용하기 쉬워야 한다"
  ✅ "신규 사용자 5분 내 첫 작업 완료 (80% 성공률)"

  ❌ "확장 가능해야 한다"
  ✅ "동시 사용자 10,000명 지원, Auto-scaling"

모든 요구사항에 다음 포함:
  - 측정 지표 (Metric)
  - 목표 값 (Target)
  - 측정 방법 (How to measure)
  - 허용 범위 (Acceptable range)
```

### 4. Continuous Inception (지속적 개시)

```yaml
기존 방식:
  Phase 1 완료 → 동결 → 개발 → 출시
  문제: 시장 변화, 경쟁사 대응 어려움

새로운 방식 (2025):
  Phase 1 → 개발 시작
      ↓
  요구사항 지속 업데이트 (단, 통제됨)
      ↓
  스프린트마다 우선순위 재조정
      ↓
  실사용자 피드백 통합

원칙:
  - 초기 계획은 "가설"
  - 데이터로 검증
  - 빠른 피벗 (방향 전환)
  - 하지만 "무정부 상태" 아님
    → Change Control Board (변경 통제)

예시 (SaaS):
  Week 1-15: 초기 계획 (MVP 범위)
  Week 16: 개발 시작
  Week 20: 베타 출시, 사용자 피드백
  Week 21: 우선순위 재조정 (데이터 기반)
    - Feature A: 사용률 10% → 연기
    - Feature B: 요청 50% → 우선순위 상향
  Week 22: 다음 스프린트 계획 조정
```

### 5. 규제 준수 자동화

```yaml
규제 산업 (금융, 의료):
  문제:
    - 수동 감사 준비 (수개월)
    - 문서 산재 (이메일, 위키, 코드)

  해결 (2025):
    - Compliance as Code
    - 자동 증거 수집
    - 실시간 대시보드

도구:
  - Vanta (SOC 2 자동화)
  - Drata (규제 준수 자동화)
  - OneTrust (GDPR 관리)

예시:
  GDPR 삭제 요청:
    1. 사용자 요청 (웹 폼)
    2. 자동 티켓 생성 (Jira)
    3. 30일 내 삭제 (자동 스크립트)
    4. 증거 기록 (감사 로그)
    5. 사용자 확인 이메일
    → 수동 개입 없이 규제 준수
```

---

## 📚 핵심 문서 비교표

| 문서 | 목적 | 작성자 | 독자 | 승인자 | 시점 | 분량 |
|------|------|--------|------|--------|------|------|
| **Project Charter** | 프로젝트 공식 승인 | 스폰서 | 경영진, 팀 | CEO/CFO | Week 1-2 | 5-10 페이지 |
| **Business Case** | 투자 정당화 | PM/BA | 경영진 | CFO | Week 1-2 | 10-20 페이지 |
| **Stakeholder Analysis** | 정치적 맵핑 | PM | PM, 팀 | 스폰서 | Week 2 | 5 페이지 |
| **PRD** | 제품 요구사항 | PO | 개발팀 | PO | Week 3-10 | 20-50 페이지 |
| **SRS** | 기술 명세 | BA/Architect | 개발/QA | Tech Lead | Week 3-10 | 50-200 페이지 |
| **ADR** | 아키텍처 결정 | Architect | 개발팀 | CTO | Week 11-12 | 2 페이지/건 |
| **Project Plan** | 실행 계획 | PM | 전체 팀 | 스폰서 | Week 13-14 | 30-50 페이지 |

---

## 🎓 핵심 교훈

### 1. 초기 계획의 가치
```
"초기 2개월의 계획이 이후 12개월의 혼란을 막는다"

투자:
- 15주 계획 (3.5개월)
- 문서 작성 노력

수익:
- 방향성 명확 → 재작업 50% 감소
- 이해관계자 정렬 → 의사결정 빠름
- 리스크 조기 발견 → 대응 가능
- 규제 준수 → 벌금 회피
```

### 2. 문서는 "살아있어야" 한다
```
❌ 나쁜 방식: 한 번 쓰고 서랍에
✅ 좋은 방식: 지속 업데이트

예시:
- PRD: 스프린트마다 백로그 업데이트
- ADR: 결정 변경 시 Status 업데이트
- Risk Register: 주간 리뷰
```

### 3. 승인 게이트는 필수
```
게이트 없이 진행하면:
- 요구사항 합의 없이 개발 → 재작업
- 아키텍처 미검증 → 기술 부채
- 예산 미승인 → 중간 중단

게이트의 가치:
- 강제 체크포인트
- 이해관계자 정렬
- 리스크 재평가
- Go/No-Go 명확
```

### 4. 측정 가능성
```
"측정할 수 없으면 관리할 수 없다"

모든 요구사항:
- 정량적 목표
- 측정 방법
- 허용 범위
- 책임자

예시:
요구사항: "빠른 응답"
→ 측정 불가 ❌

요구사항: "p95 응답시간 < 2초"
측정: New Relic APM
허용: p95 < 2.5초 (warning), < 3초 (critical)
책임자: Backend Lead
→ 측정 가능 ✅
```

### 5. 협업 도구 > 정적 문서
```
2025년 표준:
❌ Word + 이메일
✅ Confluence/Notion + Slack

이유:
- 실시간 협업
- 버전 관리 자동
- 알림 통합
- 검색 용이
- 모바일 접근
```

---

## 🚀 다음 단계

이 문서를 통해 Jason은 다음을 얻을 수 있습니다:

1. **엔터프라이즈 표준 이해**
   - 어떤 문서가 필요한지
   - 언제 작성하는지
   - 누가 승인하는지

2. **체크리스트 구축 재료**
   - 초기 계획 단계의 필수 요소 파악
   - "숨겨진 실패요소" 발견 프레임워크

3. **AI 협업 방법론 통합**
   - 엔터프라이즈 프로세스의 어떤 부분을
   - SPARK 방법론에 통합할 것인가
   - 어떻게 자동화/강제화할 것인가

---

**Version**: 1.0
**작성일**: 2025-11-10
**다음 업데이트**: Jason의 과거 사례 분석 후

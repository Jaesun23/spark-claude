

# **핵심정의에서 아키텍처 설계로: 엔터프라이즈 프로젝트를 위한 구조화된 질문 프레임워크**

## **I. 서론: '꿈'에서 '아키텍처 드라이버'로의 전환**

### **A. 문제의 재정의: "누가, 언제, 어디서"의 함정**

엔터프라이즈 프로젝트의 초기 "핵심정의(Core Definition)" 단계에서 "누가, 언제, 어디서 사용하나?"와 같은 질문은 필수적이지만, 아키텍처 설계를 위한 구체적인 정보를 제공하지 못하는 한계가 있습니다. 이러한 질문은 솔루션의 \*기능(Function)\*을 암시할 뿐, 시스템의 견고성, 성능, 확장성을 결정하는 \*품질(Quality)\*을 정의하지 못합니다.

아키텍처는 기능적 요구사항(Functional Requirements)이 아닌, 비기능 요구사항(Non-Functional Requirements, NFRs) 또는 품질 속성(Quality Attributes)에 의해 결정됩니다.1 현재의 질문 체계가 "애매하다"고 느껴지는 것은, 아키텍처 결정을 위한 핵심 정보인 NFR을 도출하지 못하기 때문입니다.

### **B. 해결책: '아키텍처 중심 질문(Architecture-Driving Questions, ADQs)'**

본 보고서는 핵심정의(Stage 1\) 단계의 목적이 기능 목록(Feature list) 작성이 아니라, 시스템의 성공과 실패를 가르는 \*\*핵심 제약조건(Constraints)과 품질 속성(Quality Attributes)\*\*을 식별하는 것임을 입증합니다.

이러한 제약조건을 도출하는 질문을 '아키텍처 중심 질문(Architecture-Driving Questions, ADQs)'이라 명명합니다. 본 보고서는 이 ADQ 프레임워크를 수립하여, "꿈 같은 얘기"를 "아키텍처 분류 가능한 수준"으로 변환하는 구체적인 방법론을 제공하는 것을 목표로 합니다.

### **C. 보고서의 구조 및 목표**

본 보고서는 요청된 네 가지 핵심 질문(Q1-Q4)에 대한 심층 분석을 제공합니다.

1. **Q1. 빅테크 기업의 초기 요구사항 정의 프레임워크 (Google vs. Amazon)**  
2. **Q2. \[실제 사례\] "AI 문서 자동 생성 서비스" 3단계 방법론 심층 분석**  
3. **Q3. 경계의 정의: Stage 1(Why) vs. Stage 2(What/How)**  
4. **Q4. \[제안\] 아키텍처 결정을 위한 10가지 핵심정의(Stage 1\) 질문**

이 4단계를 통해, 현재의 "깜깜한" 상태를 명확한 "설계도"로 전환하는 실행 가능한 로드맵을 제시합니다.

## **II. Q1. 빅테크 기업의 초기 요구사항 정의 프레임워크 (Google vs. Amazon)**

주요 기술 기업들은 기능 정의 이전에 '문제'와 '가치'를 정의하는 데 집중하며, 이 과정에서 자연스럽게 아키텍처를 주도할 핵심 NFR이 도출됩니다.

### **A. Amazon: 'Working Backwards' (PR/FAQ) \- 고객의 'Why'에서 출발**

#### **핵심 철학**

Amazon의 "Working Backwards" 프로세스는 기술(How)이 아닌 고객의 문제(Why)에서 출발합니다.3 이는 아이디어를 코드로 구현하기 전에 *미리 검증*하는 강력한 메커니즘으로, 개발 리소스 낭비를 막고 고객 가치에만 집중하게 만듭니다.5

#### **컴포넌트 1: 보도자료 (The Press Release \- PR)**

PR은 가상의 제품 출시일에 배포할 보도자료를 작성하는 것입니다. 이 문서는 "고객"을 명확히 정의하고, 그들의 "문제"를 설명하며, 제안하는 "솔루션"이 제공하는 "핵심 혜택"을 요약해야 합니다.7

"누가"라는 질문은 Amazon의 "고객(Customer)" 정의에 해당합니다. 그러나 Amazon은 여기서 멈추지 않고, \*그 고객이 왜 이 제품을 사용해야 하는지(혜택)\*를 명확히 기술하도록 강제합니다.3 이 '혜택'을 정의하는 과정이 Stage 1의 핵심입니다.

#### **컴포넌트 2: 자주 묻는 질문 (The FAQs)**

PR이 'Why'를 정의했다면, FAQ는 'How'에 대한 초기 검증입니다. FAQ는 두 가지로 나뉩니다.

* **External FAQ (고객 질문):** 고객 관점에서 가질 수 있는 의문점입니다.6 (예: "가격은 얼마인가요?", "기존 데이터와 호환되나요?").10  
* **Internal FAQ (내부 질문):** 이 부분이 아키텍처 정의의 핵심입니다. 제품 출시를 위해 리더십이나 유관 부서(법무, 재무, 엔지니어링)가 제기할 *어렵고 기술적인 질문*을 미리 예상하고 답하는 과정입니다.6  
* *Internal FAQ 예시:* "이 기능을 구현하는 데 가장 큰 기술적 병목은 무엇인가?", "경쟁사 X는 왜 이 기능을 출시하지 못했는가?", "서비스 운영을 위해 어떤 데이터가 필요하며, 데이터 프라이버시 문제는 어떻게 해결할 것인가?", "초기 사용자 100만 명을 지원하기 위한 인프라 비용과 아키텍처는 무엇인가?".6

#### **NFR 도출 방식**

Amazon은 "NFR 목록을 만드세요"라고 요구하지 않습니다. 대신 "Internal FAQ에 답하세요"라고 요구합니다. 이 과정에서 "100만 명 지원"(확장성), "데이터 프라이버시 문제"(보안), "기술적 병목"(성능/리스크)과 같은 핵심 NFR이 *자동으로* 도출됩니다.

### **B. Google: 'Product Requirements Document' (PRD) \- 엔지니어의 'What'과 'How'**

#### **핵심 철학**

Google의 PRD는 제품이나 기능을 만들기 위한 엔지니어링 팀의 '청사진(Blueprint)' 또는 '합의 문서' 역할을 합니다.12

#### **핵심 질문 구조**

Google의 PRD 템플릿은 다양하지만, 공통적으로 다음 요소를 중심으로 구성됩니다.

1. **문제 정의 (Problem Statement):** 우리가 해결하려는 사용자 문제는 정확히 무엇인가?.15  
2. **성공 지표 (Success Metrics):** 문제가 해결되었는지 *어떻게* 알 수 있는가?.15 이는 정량화 가능해야 합니다 (예: "페이지 로드 시간 20% 단축", "일일 활성 사용자 1만 명 도달").  
3. **사용자 (Personas & User Stories):** 누구를 위한 것인가?.17  
4. **핵심 사용자 여정 (Critical User Journeys, CUJs):** 사용자가 제품의 핵심 가치를 경험하기 위한 핵심 경로(Path)는 무엇인가?.14 이는 아키텍처의 'Happy Path'(가장 최적화해야 할 경로)를 정의하는 데 결정적입니다.

#### **규모 파악 방식**

Google은 PRD의 "성공 지표"와 "사용자 페르소나"를 통해 규모를 질적으로 파악합니다. "전체 사용자"가 아닌 "이 기능이 타겟하는 특정 고객 세그먼트(Segment)"에 초점을 맞추도록 유도합니다.19 "성공 지표"는 종종 달성해야 할 규모(예: "일일 활성 사용자 X명")를 명시합니다.

#### **NFR 도출 방식**

"성공 지표" 자체가 NFR을 정의하는 경우가 많습니다.17 예를 들어, "성능"이라는 NFR은 "페이지 로드 시간 X초 미만"이라는 구체적인 성공 지표로 정의됩니다. 또한 '공개 이슈(Open Issues)' 또는 'Q\&A' 섹션 18을 통해 초기 기술 리스크와 아키텍처가 고려해야 할 제약 사항을 식별합니다.

### **C. Q1 종합 인사이트: NFR은 '발견'하는 것이 아니라 '도출'하는 것이다**

현재의 질문("누가, 언제, 어디서")이 모호한 이유는, 아키텍처를 결정하는 NFRs 2이 아니라 기능(Function)에 초점을 맞추기 때문입니다.

Amazon과 Google 모두 기능(Functional) 요구사항 이전에 **(1) 비즈니스 문제**와 **(2) 성공의 측정 기준**을 먼저 정의합니다.

NFR(비기능 요구사항)은 Stage 2에서 갑자기 등장하는 것이 아닙니다. Stage 1에서 '품질 속성(Quality Attributes)' 1으로 먼저 식별되어야 합니다. "빠른 시스템"(Stage 2)을 요구하기 전에, "왜 빨라야 하는가?"(Stage 1 \- 예: 사용자가 1초 내에 이탈하기 때문)에 대한 비즈니스적 합의가 필요합니다. 이는 '이해관계자 인터뷰(Stakeholder interviews)'와 '경쟁 분석(Market analysis)'을 통해 도출되어야 합니다.21

## **III. Q2. \[실제 사례\] "AI 문서 자동 생성 서비스" 3단계 방법론 심층 분석**

요청된 "AI 문서 자동 생성 서비스" 사례를 Amazon의 3단계 방법론(Use Cases \-\> Concrete Requirements \-\> Technology Selection)에 적용하여 분석합니다.

### **A. 서비스 아키텍처 개요: RAG(Retrieval-Augmented Generation) 패턴**

제공된 서비스 설명(기본 자료 제공, 양식 선택, 사용자 자료로만 작성, 리서치 추가)은 전형적인 **RAG(Retrieval-Augmented Generation)** 아키텍처를 의미합니다.23

* **RAG의 작동 원리:** 대규모 언어 모델(LLM)이 학습한 방대한 일반 지식만 사용하는 대신, (1) 사용자의 질문이나 기본 자료를 받아 (2) 사전에 인덱싱된 *관련된* 내부 문서(Vector DB)를 검색하고 (3) 이 검색된 자료를 LLM에 '참조 자료'로 함께 제공하여 (4) '사실에 기반한(Grounded)' 답변(문서)을 생성하게 하는 기술입니다.24  
* **핵심 컴포넌트:** 데이터 인덱싱 파이프라인(문서 처리, 임베딩) 27, 벡터 데이터베이스(Vector DB) 28, 검색 시스템, LLM, API 백엔드 29, 웹 프론트엔드 29로 구성됩니다.

### **B. Stage 1: 핵심정의 (Use Cases & Architecture Drivers)**

Amazon의 PR/FAQ 방식을 적용하여 이 서비스의 Stage 1을 정의하고, 아키텍처 드라이버를 도출합니다.

#### **가상 PR (보도자료)**

* **제목:** DocuGen.ai, 기업 법률팀을 위한 AI 계약서 초안 작성 서비스 출시  
* **부제:** 기업 내부 자료 기반으로 1시간 걸리던 계약서 초안을 5분 만에 생성  
* **요약:** DocuGen.ai는 법률팀이 기존 계약서, 내부 규정, 최신 판례(사용자 제공 자료)를 업로드하면, AI가 이를 학습하여 복잡한 계약서 초안을 즉시 생성해주는 웹 기반 서비스입니다.  
* **문제:** 법률팀은 매번 유사한 계약서를 작성하며 과거 자료를 검색하는 데 과도한 시간을 소모하고, 실수로 오래된 규정을 인용할 아키텍처 리스크가 존재합니다.  
* **해결:** DocuGen.ai는 RAG 기술을 통해 오직 승인된 내부 자료와 최신 법률 데이터만을 기반으로 24, 정확하고 일관된 형식의 문서를 생성합니다.30 사용자는 미리 준비된 양식을 선택하거나 프롬프트로 커스터마이징할 수 있으며, 다양한 디자인 템플릿을 적용할 수 있습니다.

#### **가상 Internal FAQ (핵심 아키텍처 드라이버 도출)**

* *Q: 데이터 보안은 어떻게 보장하나요? 고객의 민감한 계약서가 외부 LLM으로 유출되면 안 됩니다.*  
  * **A(Stage 1 답):** **(보안/격리)** 데이터는 절대 외부로 유출되지 않아야 합니다. 고객사 내부망(On-premise) 또는 가상 사설 클라우드(VPC) 내 배포가 필수적인 아키텍처 요구사항입니다.  
* *Q: "최신 판례"를 언급했는데, 데이터가 얼마나 자주 바뀌나요?*  
  * **A(Stage 1 답):** **(최신성/Data Volatility)** 데이터는 매일 업데이트되어야 하며, 업데이트 즉시 검색 결과에 반영되어야 합니다. (이는 RAG 인덱싱 파이프라인 설계에 치명적인 영향을 줍니다 27).  
* *Q: 정확성이 중요한가요, 속도가 중요한가요?*  
  * **A(Stage 1 답):** **(품질/Trade-off)** 법률 문서는 *무조건 정확성*이 속도보다 중요합니다. 잘못된 정보(Hallucination)는 허용되지 않습니다. 응답이 30초 걸리더라도 정확해야 합니다.  
* *Q: "웹 기반"이라고 했는데, IE에서도 돌아가야 하나요? "다양한 플랫폼 지원"은 모바일도 포함인가요?*  
  * **A(Stage 1 답):** **(환경/Interface)** 핵심 고객(법률팀)은 데스크톱 환경의 Chrome, Edge 최신 버전을 사용합니다. 모바일 지원은 현재(v1) 필요 없습니다. "다양한 플랫폼"은 브라우저 호환성을 의미합니다.31  
* *Q: 초기 사용자 규모는?*  
  * **A(Stage 1 답):** **(규모/Structure)** 초기 10개 엔터프라이즈 고객사(각 100명 내외)를 대상으로 합니다. 동시 사용자가 폭증하기보다는, 각 고객사가 보유한 대용량 문서(수만 건)를 *인덱싱*하는 부하가 큽니다.

### **C. Stage 2: 구현방법 (Concrete Requirements & Tech Options)**

Stage 1의 질적(Qualitative) 답변을 Stage 2의 양적(Quantitative) "속성 질문"으로 변환하고, 기술 옵션을 도출합니다.

| Stage 1 질적 답변 (Why/What) | Stage 2 속성 질문 (How well/How many) | Stage 2 구체적 요구사항 (NFR Spec) | 기술 옵션 (Tech Options) |
| :---- | :---- | :---- | :---- |
| **(보안/격리)** 고객사 내부망(VPC) 배포 필수 31 | **\[환경\]** 지원해야 할 배포 모델은 무엇인가? | \- 배포 모델: Kubernetes (On-premise) 또는 AWS VPC (Private Cloud) \- 데이터 전송: 모든 트래픽은 Private Endpoint/Link를 통해 처리 30 | \- **Deployment:** Kubernetes, Docker \- **Cloud:** AWS (VPC, S3, PrivateLink), Azure (VNET) 30 |
| **(최신성)** 데이터는 매일 업데이트되어야 함 | **\[성능\]** 데이터 인덱싱 파이프라인의 처리량(Throughput)과 지연시간(Latency)은? | \- 데이터 인덱싱: 일 1회 배치(Batch) 30, 10만 건 문서 처리에 1시간 이내 완료. \- 데이터 반영: 신규 문서 업로드 후 5분 이내 검색 가능 (Near Real-time) | \- **Indexing Pipeline:** Azure AI Document Intelligence 30, Python(Custom) 29 \- **Orchestration:** Airflow, AWS Step Functions |
| **(품질)** 속도보다 정확성이 중요 | **\[품질\]** RAG 검색 정확도(Precision) 목표는? **\[성능\]** 생성 속도(Latency) 목표는? | \- RAG 정확도: Top-3 검색 결과에 정답 문서가 포함될 확률 99% 24 \- 생성 속도: P95(상위 95%) 요청이 30초 이내 응답 32 | \- **LLM:** GPT-4 (via Azure Private), Llama 3 (Self-hosted) 23 \- **RAG Framework:** LangChain, LlamaIndex 33 |
| **(규모)** 10개사(각 100명), 인덱싱 부하가 큼 | **\[확장성\]** 벡터 DB가 처리해야 할 총 벡터 수는? | \- Vector DB: 초기 1억 벡터(10개사 \* 10만 문서 \* 100 chunk) 지원, 10억 벡터(Billion-scale)까지 수평 확장 가능해야 함.34 | \- **Vector DB:** **Milvus** 28 vs. **Pinecone** 28 |
| **(환경)** Chrome/Edge 지원 31 | **\[호환성\]** 지원 브라우저 및 버전은? | \- Frontend: Chrome 최신 2개 버전, Edge 최신 2개 버전 지원. | \- **Frontend:** React 29, Figma (Design) 33 |

### **D. Stage 3: 기술 선택 (Technology Selection & ADR)**

Stage 2의 요구사항과 옵션을 바탕으로 핵심 기술 결정을 내리고 ADR(Architecture Decision Record)로 기록합니다.

#### **ADR-001: 벡터 데이터베이스(Vector DB) 선정**

* **날짜:** 2024-XX-XX  
* **상태:** 결정됨  
* **맥락 (Context):**  
  1. 본 서비스는 RAG 아키텍처를 사용하며, 문서 검색을 위한 벡터 DB가 필수입니다.24  
  2. **Stage 1 요구사항:** "고객사 내부망(VPC/On-prem) 배포"가 필수적이며(보안), "대용량 문서(수만 건)" 인덱싱이 초기부터 발생합니다(규모).  
  3. **Stage 2 요구사항:** "10억 벡터까지 수평 확장"이 가능해야 합니다.34  
* **결정 (Decision):** \*\*Milvus (Open Source, Self-hosted)\*\*를 채택한다.  
* **근거 (Rationale):**  
  * **Pinecone** 34:  
    * *장점:* 완전 관리형(SaaS), 빠른 속도(저지연성) 36, 사용 편의성(빠른 배포).34  
    * *단점:* **치명적 결함:** 클라우드 전용(SaaS) 35으로 온프레미스 배포 요구사항(Stage 1)을 충족하지 못합니다. 벤더 종속성(Vendor Lock-in)이 발생합니다.35  
  * **Milvus** 28:  
    * *장점:* **요구사항 충족:** 오픈소스로 35, Kubernetes를 통해 온프레미스/VPC에 자체 배포 가능합니다.34 **요구사항 충족:** 대규모(Billion/Trillion-scale) 인덱싱 및 수평 확장에 최적화되어 있습니다.34 인프라에 대한 완전한 제어가 가능합니다.35  
    * *단점:* 자체 운영 및 유지보수(DevOps) 비용이 발생합니다.36  
* **결과 (Consequences):** Milvus 운영을 위한 Kubernetes 전문 인력 확보가 필요하며, 또는 Zilliz Cloud(Milvus의 관리형 버전) 사용을 대안으로 고려해야 합니다.

#### **ADR-002: 백엔드 프레임워크 선정**

* **날짜:** 2024-XX-XX  
* **상태:** 결정됨  
* **맥락 (Context):**  
  1. RAG 파이프라인(LLM 연동, DB 조회)과 프론트엔드(React)에 데이터를 제공할 API 서버가 필요합니다.  
  2. **Stage 1 요구사항:** "정확성"과 "보안"이 핵심이며, 복잡한 비즈니스 로직(RAG 파이프라인)을 처리해야 합니다.  
  3. **Stage 2 요구사항:** "P95 30초 이내 응답" (비동기 처리 필요 가능성).  
* **결정 (Decision):** **Python** 기반의 **FastAPI**를 채택한다.  
* **근거 (Rationale):**  
  * **Python 선택** 29: RAG 프레임워크(LangChain 등), LLM 연동, 머신러닝 생태계 33는 모두 Python 중심입니다. 백엔드 API와 ML 모델링 코어를 동일 언어로 사용하는 것이 29 개발 효율성과 유지보수성(Cleaner Architecture) 29에 압도적으로 유리합니다.  
  * **FastAPI 선택:** (Node.js 대비) Python 생태계를 그대로 활용 가능합니다. (Django 대비) FastAPI는 비동기(Async) 처리를 네이티브로 지원하여, LLM 호출과 같이 오래 걸리는 I/O 작업을 효율적으로 처리할 수 있어 Stage 2의 성능 요구사항 37을 충족하는 데 유리합니다.  
* **결과 (Consequences):** 프론트엔드(React) 29와 백엔드(FastAPI)가 명확히 분리된(Decoupled) 아키텍처 29를 유지해야 합니다.

## **IV. Q3. 경계의 정의: Stage 1(Why) vs. Stage 2(What/How)**

### **A. 개념적 경계: BABOK (Business Analysis Body of Knowledge)**

핵심정의(Stage 1)와 구현방법(Stage 2)의 구분은 BABOK(Business Analysis Body of Knowledge)의 요구사항 계층 구조와 정확히 일치합니다.38

* **Stage 1 \= 비즈니스 요구사항 (Business Requirements):**  
  * **목적:** *Why* (왜 이 프로젝트를 하는가?).  
  * **정의:** 조직의 고수준 목표, 목적, 성과를 기술합니다.38  
  * **예시:** "계약서 작성 시간을 90% 단축하여 법무팀의 생산성을 높인다."  
  * **도출:** Amazon의 PR/FAQ 3, Google의 Problem Statement.15  
* **Stage 2 \= 솔루션 요구사항 (Solution Requirements):**  
  * **목적:** *What* (무엇을 만들어야 하는가?).  
  * **정의:** 이해관계자 요구사항을 충족하기 위한 솔루션의 역량과 품질을 기술합니다.38  
  * **하위 분류:**  
    * *기능 요구사항:* (예: "사용자는 문서를 업로드할 수 있다.")  
    * *비기능 요구사항 (NFRs):* (예: "업로드된 문서는 5분 내 검색 가능해야 한다.").40  
  * **도출:** "속성 질문" (성능/품질/환경).

### **B. 실용적 비유: 자동차 튜닝 (Stage 1 vs. Stage 2\)**

이 개념적 구분은 엔지니어링 팀이 쉽게 이해할 수 있는 자동차 튜닝 비유로 설명할 수 있습니다.42

* **Stage 1 튜닝 (ECU Remap):**  
  * *내용:* 하드웨어 변경 없이 42, ECU(소프트웨어)만 조정하여 43 차량의 *잠재력*을 이끌어냅니다.  
  * *비유 (Stage 1 핵심정의):* 비즈니스 목표와 *방향성*("더 빠른 일상 주행용 차")을 정의합니다. 아직 기술 스택(하드웨어)을 바꾸지 않고, *방향성*에 대한 합의를 합니다.  
* **Stage 2 튜닝 (Hardware Upgrade):**  
  * *내용:* 더 큰 성능을 위해 반드시 하드웨어 교체(인테이크, 배기, 터보)가 필요합니다.42  
  * *비유 (Stage 2 구현방법):* Stage 1에서 합의한 "더 빠른 차"라는 *목표*를 "300마력, 제로백 5초"라는 *구체적 사양*으로 변환합니다. 이 사양을 달성하기 위한 \*특정 기술(하드웨어)\*을 선택하고 보정(Calibration)합니다.

### **C. Stage 1의 '멈춤 시점'과 Stage 2의 '트리거'**

* **Stage 1에서 멈춰야 할 지점:**  
  * "어떻게(How)" 만들지(예: "Vector DB는 Milvus로 한다")를 논의하기 시작할 때.  
  * Stage 1의 산출물은 *기술 스택*이 아니라, \*비즈니스 가치(Why)\*와 \*핵심 품질 속성(How well)\*에 대한 **이해관계자 간의 합의**입니다.47 (예: "우리는 속도보다 보안과 정확성을 우선한다"는 합의).  
* **Stage 2로 넘어가는 트리거:**  
  * Stage 1에서 정의된 **'솔루션 범위(Solution Scope)'와 '비즈니스 목표(Business Requirements)'가 승인(Sign-off)되었을 때**입니다.47  
  * 이 승인은 아키텍트에게 "이제 이 질적 목표(예: 보안 우선)를 만족하는 기술적 사양(예: 온프레미스 배포)을 구체화하라"는 위임입니다.

### **D. 정보의 진화: "사용자 수"의 질적(Stage 1\) vs. 양적(Stage 2\) 정의**

"중규모 사용자" vs "500명 동시 접속"이라는 통찰은 정확합니다. 이 정보의 진화가 아키텍처를 결정하는 방식은 다음과 같습니다.

| 정보 (Information) | Stage 1 (핵심정의 \- 질적, 방향성) | (Stage 1\) 아키텍처 결정 영향 | Stage 2 (구현방법 \- 양적, 구체성) | (Stage 2\) 아키텍처 결정 영향 |
| :---- | :---- | :---- | :---- | :---- |
| **규모 (Scale)** | "초기 스타트업(B2C) 대상" vs. "대기업 엔터프라이즈(B2B) 대상" | **구조(Structure)**: \- B2C: 수평 확장(Scale-out)이 용이한 분산형/클라우드 네이티브 구조. \- B2B: 격리(Isolation)가 중요한 모놀리식 또는 단일 테넌트(Single-tenant) 구조. | \- **동시 접속자(CCU):** 500명 \- **초당 트랜잭션(TPS):** 100 TPS \- **총 사용자:** 10,000명 | **구현 기술(Construction)**: \- Web Server 스레드 풀 크기 \- DB 커넥션 풀 크기 \- Auto-Scaling 임계값 설정 |
| **성능 (Performance)** | "경쟁사보다 빨라야 함" vs. "속도보다 정확성이 중요함" | **비기능 특성(NFR) \- Trade-off**: \- 속도 우선: Caching, 비동기(Async) 패턴 \- 정확성 우선: 동기(Sync) 처리, 검증 로직 강화 | \- **응답 시간:** P99 2초 이내 \- **처리량:** 분당 1,000건 문서 생성 41 | **인터페이스(Interface) / 기술(Construction)**: \- API: 비동기(Callback) vs. 동기(Blocking) \- 캐시: Redis 적용 범위 |
| **환경 (Environment)** | "클라우드 SaaS로 빠르게 출시" vs. "고객사 내부망에 설치" | **구조(Structure) / 의존성(Dependency)**: \- SaaS: 멀티 테넌트(Multi-tenant) 구조 \- 내부망: 온프레미스(On-premise) 배포, 외부 의존성 최소화 | \- **지원 플랫폼:** AWS, Azure, On-prem (Kubernetes v1.25+) 41 \- **지원 브라우저:** Chrome, Safari | **기술(Construction)**: \- 패키징: Docker Image, Helm Chart \- 클라우드 서비스: (SaaS) Pinecone 34 vs. (On-prem) Milvus 34 |

## **V. Q4. \[제안\] 아키텍처 결정을 위한 10가지 핵심정의(Stage 1\) 질문**

"애매한" 질문("누가, 언제, 어디서")을 대체하고, 'Software Architecture Fundamentals'의 5가지 핵심 요소(구조, NFR, 의존성, 인터페이스, 기술)를 직접적으로 도출해낼 수 있는 10가지 '아키텍처 중심 질문(ADQs)'을 제안합니다. 이 질문들은 기술 용어가 아닌 비즈니스 용어로 구성되어야 합니다.

**테이블: 10가지 핵심 아키텍처 중심 질문 (ADQs)**

| 분류 | 질문 (The Question) | 수집 정보 (Information Gathered) | 아키텍처 결정 영향 (Architectural Target) |
| :---- | :---- | :---- | :---- |
| **A. 비즈니스 가치 및 성공** | **Q1. 이 서비스/기능이 실패(Fail)했다고 판단하는 핵심 기준은 무엇이며, 그 기준이 1시간 동안 지속될 경우 비즈니스(매출, 신뢰)에 어떤 손실이 발생합니까?** | 비즈니스 리스크 허용 범위, 핵심 장애 지점. | **NFR (가용성, 신뢰성)** (근거: 이 질문은 99.9%와 99.999%의 비용/복잡성 차이를 정당화합니다. 32) |
| **A. 비즈니스 가치 및 성공** | **Q2. 이 서비스가 시장의 다른 경쟁자와 구별되는 '단 하나의' 핵심 품질(예: 가장 빠름, 가장 정확함, 가장 저렴함, 가장 안전함)은 무엇입니까?** | 핵심 품질 속성(Quality Attribute), 트레이드오프(Trade-off) 우선순위. | **NFR (성능 vs. 보안 vs. 비용)** (근거: 모든 것을 잘할 수는 없습니다. 이 질문은 아키텍처의 '북극성'을 결정합니다. 51) |
| **B. 사용자 및 규모** | **Q3. 이 서비스의 핵심 사용자는 누구이며, 이들의 성공적인 '핵심 여정(Critical User Journey, CUJ)' 1가지는 무엇입니까?** (Google CUJ 참고 14) | 사용자의 핵심 워크플로, 시스템의 'Happy Path'. | **인터페이스(Interface), 구조(Structure)** *(근거: 사용자의 핵심 경로를 최적화하는 방식으로 API와 서비스 경계를 설계합니다.)* |
| **B. 사용자 및 규모** | **Q4. 서비스 출시 1년 후 예상되는 사용자 규모의 '유형'은 무엇입니까? (예: 소수의 대기업 고객, 다수의 개인 사용자, 특정 시간대에 몰리는 사용자)** | 사용자 규모의 질적 특성 (B2B vs. B2C), 트래픽 패턴. | **NFR (확장성), 구조(Structure)** *(근거: "중규모"가 아닌 "트래픽 패턴"이 구조를 결정합니다. (예: B2B는 모놀리식, B2C는 분산형))* |
| **C. 데이터 및 의존성** | **Q5. 서비스가 사용하는 핵심 데이터의 '민감도(Sensitivity)'는 어느 수준이며(개인정보, 금융, 일반), 이 데이터가 조직 외부로 나갈 수 있습니까?** | 데이터 보안 등급, 규제(Compliance) 요구사항. | **NFR (보안), 구조(Structure), 의존성(Dependency)** (근거: 이 답변이 SaaS 34를 만들지, 온프레미스 34를 만들지 결정합니다.) |
| **C. 데이터 및 의존성** | **Q6. 이 서비스가 의존해야 하는 '데이터 원천(Source of Truth)'은 무엇이며, 이 데이터는 얼마나 자주 변경되고, 서비스는 그 변경을 얼마나 빨리 반영해야 합니까?** | 데이터의 최신성(Volatility) 요구사항, 외부 시스템 의존성. 27 | **의존성(Dependency), NFR (성능/Latency)** *(근거: 실시간 반영이 필요하면 CDC/Event-driven, 일 1회면 Batch 구조)* |
| **C. 데이터 및 의존성** | **Q7. 이 서비스가 생성하는 데이터는 얼마나 오랫동안, 어떤 형태로 보관되어야 하며, 감사를 위해 접근 가능해야 합니까?** | 데이터 수명 주기(Lifecycle), 감사(Audit) 요구사항. | **NFR (감사 용이성), 구현 기술(Construction)** (근거: 단순 DB 저장이 아닌, 감사 로그, 데이터 웨어하우스(DWH) 필요 여부를 결정합니다. 1) |
| **D. 운영 및 환경** | **Q8. 이 서비스가 반드시 연동되어야 하는(혹은 절대 연동되면 안 되는) 기존 사내 시스템이 있습니까?** | 내부 시스템 의존성, 기술적 제약(Constraints). | **의존성(Dependency), 인터페이스(Interface)** (근거: 레거시 시스템 연동 여부가 아키텍처의 자유도를 결정합니다. 52) |
| **D. 운영 및 환경** | **Q9. 서비스의 배포 및 운영 환경에 대한 핵심 제약 조건은 무엇입니까? (예: 특정 클라우드 벤더 사용, 특정 국가에서만 서비스, 사내 Kubernetes 환경만 사용)** | 배포 환경, 지리적(Geographical) 제약. | **구조(Structure), 구현 기술(Construction)** *(근거: '어디서'의 구체화. "AWS에서만"은 기술 선택을 주도합니다.)* |
| **D. 운영 및 환경** | **Q10. 이 서비스의 기능을 변경하거나 확장하는 주기는 어느 정도로 예상합니까? (예: 매일 배포, 분기별 1회 업데이트)** | 변경 용이성(Modifiability), 개발 속도(Velocity) 요구사항. | **구조(Structure), NFR (유지보수성)** *(근거: 잦은 변경이 필요하면 모놀리식보다 마이크로서비스 구조가 유리할 수 있습니다.)* |

## **VI. 결론: '정의(Definition)'를 '설계(Design)'로 연결하기**

1. **문제점 진단:** 현재 겪고 있는 "깜깜함"은 "누가, 언제, 어디서"라는 *기능 중심적* 질문이 아키텍처를 주도하는 \*품질 속성(NFRs)\*을 이끌어내지 못했기 때문입니다.  
2. **본 보고서의 해답:**  
   * **Q1(빅테크):** Amazon(PR/FAQ)과 Google(PRD)은 기능 명세 이전에 \*\*'문제(Problem)'와 '가치/성공(Value/Success)'\*\*을 정의하는 데 집중하며, 이 과정에서 NFR이 자연스럽게 도출됩니다.3  
   * **Q2(사례):** AI 문서 서비스 사례는 Stage 1의 질적 질문("데이터가 외부로 나가면 안 된다") 30이 어떻게 Stage 3의 구체적인 기술 선택("Pinecone이 아닌 Milvus") 34으로 이어지는지 명확히 보여주었습니다.  
   * **Q3(경계):** Stage 1과 2의 경계는 \*\*'비즈니스 요구사항(Why)'과 '솔루션 요구사항(What)'\*\*의 경계이며 38, 이는 자동차 튜닝의 '소프트웨어 맵핑(Stage 1)'과 '하드웨어 교체(Stage 2)'의 차이 42로 비유할 수 있습니다.  
3. **최종 제안:**  
   * "핵심정의 단계"에서는 본 보고서의 \*\*Q4에서 제안한 '10가지 아키텍처 중심 질문(ADQs)'\*\*을 사용해야 합니다.  
   * 이 질문들은 Stage 1(핵심정의)에서 "꿈"을 묻는 것이 아니라, 그 꿈을 실현하기 위한 \*\*'핵심 제약조건(Constraints)'\*\*을 정의합니다. 이 제약조건들이 바로 아키텍처를 결정하는 '드라이버'입니다. 이 프레임워크를 통해 "애매함"을 제거하고 "아키텍처 분류 가능한 수준"의 명확한 요구사항을 정의할 수 있습니다.

#### **참고 자료**

1. Quality Attributes in Software \- DEV Community, 11월 11, 2025에 액세스, [https://dev.to/frosnerd/quality-attributes-in-software-1ha9](https://dev.to/frosnerd/quality-attributes-in-software-1ha9)  
2. How do Software Architects Consider Non-Functional Requirements: An Exploratory Study \- UPCommons, 11월 11, 2025에 액세스, [https://upcommons.upc.edu/bitstreams/f98e1c18-4c11-4cc8-a682-01fdb55bddbf/download](https://upcommons.upc.edu/bitstreams/f98e1c18-4c11-4cc8-a682-01fdb55bddbf/download)  
3. Discover PRFAQ: Amazon's Innovation Blueprint \+Template \- Product School, 11월 11, 2025에 액세스, [https://productschool.com/blog/product-fundamentals/prfaq](https://productschool.com/blog/product-fundamentals/prfaq)  
4. An insider look at Amazon's culture and processes \- About Amazon, 11월 11, 2025에 액세스, [https://www.aboutamazon.com/news/workplace/an-insider-look-at-amazons-culture-and-processes](https://www.aboutamazon.com/news/workplace/an-insider-look-at-amazons-culture-and-processes)  
5. Working Backwards | How write-ups help launch successful products like AWS, the Kindle & Prime Video, 11월 11, 2025에 액세스, [https://coda.io/@colin-bryar/working-backwards-how-write-an-amazon-pr-faq](https://coda.io/@colin-bryar/working-backwards-how-write-an-amazon-pr-faq)  
6. Amazon Working Backwards Template | PR FAQs \- Hustle Badger, 11월 11, 2025에 액세스, [https://www.hustlebadger.com/what-do-product-teams-do/amazon-working-backwards-process/](https://www.hustlebadger.com/what-do-product-teams-do/amazon-working-backwards-process/)  
7. The Amazon Working Backwards PR/FAQ Process, 11월 11, 2025에 액세스, [https://workingbackwards.com/concepts/working-backwards-pr-faq-process/](https://workingbackwards.com/concepts/working-backwards-pr-faq-process/)  
8. Working Backwards (the Amazon Method) | Definition and Overview \- ProductPlan, 11월 11, 2025에 액세스, [https://www.productplan.com/glossary/working-backward-amazon-method/](https://www.productplan.com/glossary/working-backward-amazon-method/)  
9. Strategy Tool: Amazon's PR/FAQ \- intrico.io \- Medium, 11월 11, 2025에 액세스, [https://medium.com/intrico-io/strategy-tool-amazons-pr-faq-72b3e49aa167](https://medium.com/intrico-io/strategy-tool-amazons-pr-faq-72b3e49aa167)  
10. Working Backwards PR/FAQ Instructions & Template, 11월 11, 2025에 액세스, [https://workingbackwards.com/resources/working-backwards-pr-faq/](https://workingbackwards.com/resources/working-backwards-pr-faq/)  
11. Recommendations to roll out an Amazon like PRFAQ process for PMs. What was your personal experience adopting it? \- Reddit, 11월 11, 2025에 액세스, [https://www.reddit.com/r/ProductManagement/comments/1kfktnt/recommendations\_to\_roll\_out\_an\_amazon\_like\_prfaq/](https://www.reddit.com/r/ProductManagement/comments/1kfktnt/recommendations_to_roll_out_an_amazon_like_prfaq/)  
12. PRD: Product Requirements Doc templates \- Notion, 11월 11, 2025에 액세스, [https://www.notion.com/templates/category/product-requirements-doc](https://www.notion.com/templates/category/product-requirements-doc)  
13. A sample PRD (Product Requirements Document) I made for a recent interview \- Reddit, 11월 11, 2025에 액세스, [https://www.reddit.com/r/ProductManagement/comments/95w0rl/a\_sample\_prd\_product\_requirements\_document\_i\_made/](https://www.reddit.com/r/ProductManagement/comments/95w0rl/a_sample_prd_product_requirements_document_i_made/)  
14. ELI5 Request: CUJ and PRD at Google : r/ProductManagement \- Reddit, 11월 11, 2025에 액세스, [https://www.reddit.com/r/ProductManagement/comments/1jsq1eb/eli5\_request\_cuj\_and\_prd\_at\_google/](https://www.reddit.com/r/ProductManagement/comments/1jsq1eb/eli5_request_cuj_and_prd_at_google/)  
15. The best product requirement doc (PRD) prompt i've ever used : r/PromptEngineering, 11월 11, 2025에 액세스, [https://www.reddit.com/r/PromptEngineering/comments/1n2qzqr/the\_best\_product\_requirement\_doc\_prd\_prompt\_ive/](https://www.reddit.com/r/PromptEngineering/comments/1n2qzqr/the_best_product_requirement_doc_prd_prompt_ive/)  
16. Google's PRD Template \- GrowthX, 11월 11, 2025에 액세스, [https://growthx.club/learn/templates/prd-googles-product-requirement-template](https://growthx.club/learn/templates/prd-googles-product-requirement-template)  
17. Product Requirements Document Guide | Slite.com, 11월 11, 2025에 액세스, [https://slite.com/es/learn/product-requirements-document](https://slite.com/es/learn/product-requirements-document)  
18. The Only Product Requirements Document (PRD) Template You Need \- Product School, 11월 11, 2025에 액세스, [https://productschool.com/blog/product-strategy/product-template-requirements-document-prd](https://productschool.com/blog/product-strategy/product-template-requirements-document-prd)  
19. 12x PRD Examples | Real PRD Templates \- Hustle Badger, 11월 11, 2025에 액세스, [https://www.hustlebadger.com/what-do-product-teams-do/prd-template-examples/](https://www.hustlebadger.com/what-do-product-teams-do/prd-template-examples/)  
20. System Design Unleashed series \#2: Functional and Non-functional requirements \- Medium, 11월 11, 2025에 액세스, [https://medium.com/@the.learning.game/system-design-unleashed-series-2-functional-and-non-functional-requirements-416d5c25ff1b](https://medium.com/@the.learning.game/system-design-unleashed-series-2-functional-and-non-functional-requirements-416d5c25ff1b)  
21. Managing Non-Functional Requirements \- Beyond the Backlog, 11월 11, 2025에 액세스, [https://beyondthebacklog.com/2024/03/05/managing-non-functional-requirements/](https://beyondthebacklog.com/2024/03/05/managing-non-functional-requirements/)  
22. A Qualitative Study on Non-Functional Requirements in Agile Software Development \- SciSpace, 11월 11, 2025에 액세스, [https://scispace.com/pdf/a-qualitative-study-on-non-functional-requirements-in-agile-465qvrvkv6.pdf](https://scispace.com/pdf/a-qualitative-study-on-non-functional-requirements-in-agile-465qvrvkv6.pdf)  
23. AI Architecture Design \- Azure Architecture Center | Microsoft Learn, 11월 11, 2025에 액세스, [https://learn.microsoft.com/en-us/azure/architecture/ai-ml/](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/)  
24. What is Retrieval Augmented Generation (RAG)? \- Databricks, 11월 11, 2025에 액세스, [https://www.databricks.com/glossary/retrieval-augmented-generation-rag](https://www.databricks.com/glossary/retrieval-augmented-generation-rag)  
25. What is RAG (Retrieval Augmented Generation)? \- IBM, 11월 11, 2025에 액세스, [https://www.ibm.com/think/topics/retrieval-augmented-generation](https://www.ibm.com/think/topics/retrieval-augmented-generation)  
26. What is RAG? \- Retrieval-Augmented Generation AI Explained \- Amazon AWS, 11월 11, 2025에 액세스, [https://aws.amazon.com/what-is/retrieval-augmented-generation/](https://aws.amazon.com/what-is/retrieval-augmented-generation/)  
27. RAG Pipeline: Example, Tools & How to Build It \- lakeFS, 11월 11, 2025에 액세스, [https://lakefs.io/blog/what-is-rag-pipeline/](https://lakefs.io/blog/what-is-rag-pipeline/)  
28. We Tried and Tested 10 Best Vector Databases for RAG Pipelines \- ZenML Blog, 11월 11, 2025에 액세스, [https://www.zenml.io/blog/vector-databases-for-rag](https://www.zenml.io/blog/vector-databases-for-rag)  
29. React with Python: Winning Full-Stack Web Development \+ Tutorial \- Glorywebs, 11월 11, 2025에 액세스, [https://www.glorywebs.com/blog/react-with-python](https://www.glorywebs.com/blog/react-with-python)  
30. Build a Document Generation System by Using AI \- Azure Architecture Center, 11월 11, 2025에 액세스, [https://learn.microsoft.com/en-us/azure/architecture/ai-ml/idea/generate-documents-from-your-data](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/idea/generate-documents-from-your-data)  
31. AI-Powered Construction Document Analysis by Leveraging Computer Vision and Large Language Models \- Amazon AWS, 11월 11, 2025에 액세스, [https://aws.amazon.com/blogs/spatial/ai-powered-construction-document-analysis-by-leveraging-computer-vision-and-large-language-models/](https://aws.amazon.com/blogs/spatial/ai-powered-construction-document-analysis-by-leveraging-computer-vision-and-large-language-models/)  
32. Nonfunctional Requirements: Examples, Types and Approaches \- AltexSoft, 11월 11, 2025에 액세스, [https://www.altexsoft.com/blog/non-functional-requirements/](https://www.altexsoft.com/blog/non-functional-requirements/)  
33. Top 5 Tech Stacks for Web & App Development in 2025 \- Plego Technologies, 11월 11, 2025에 액세스, [https://plego.com/blog/top-tech-stacks/](https://plego.com/blog/top-tech-stacks/)  
34. Milvus vs Pinecone: How to Choose the Right Vector Database \- Scout, 11월 11, 2025에 액세스, [https://www.scoutos.com/blog/milvus-vs-pinecone-how-to-choose-the-right-vector-database](https://www.scoutos.com/blog/milvus-vs-pinecone-how-to-choose-the-right-vector-database)  
35. How does Milvus compare to other vector databases like Pinecone or Weaviate?, 11월 11, 2025에 액세스, [https://milvus.io/ai-quick-reference/how-does-milvus-compare-to-other-vector-databases-like-pinecone-or-weaviate](https://milvus.io/ai-quick-reference/how-does-milvus-compare-to-other-vector-databases-like-pinecone-or-weaviate)  
36. Comparative Evaluation of Milvus vs. Pinecone for Retrieval-Augmented Generation (RAG), 11월 11, 2025에 액세스, [https://medium.com/@oliversmithth852/comparative-evaluation-of-milvus-vs-pinecone-for-retrieval-augmented-generation-rag-5ab8ff8b06af](https://medium.com/@oliversmithth852/comparative-evaluation-of-milvus-vs-pinecone-for-retrieval-augmented-generation-rag-5ab8ff8b06af)  
37. Modern AI Tech Stack: Build Smarter, Scale Faster, Think Bigger \- Fively, 11월 11, 2025에 액세스, [https://5ly.co/blog/ai-tech-stack/](https://5ly.co/blog/ai-tech-stack/)  
38. Types of Requirements | BABOK classification Schema \- Techcanvass, 11월 11, 2025에 액세스, [https://techcanvass.com/blogs/types-of-requirements-as-per-babok.aspx](https://techcanvass.com/blogs/types-of-requirements-as-per-babok.aspx)  
39. Explain how BABOK categorizes requirements \- Modern Analyst, 11월 11, 2025에 액세스, [https://www.modernanalyst.com/Careers/InterviewQuestions/tabid/128/ID/2033/Explain-how-BABOK-categorizes-requirements.aspx](https://www.modernanalyst.com/Careers/InterviewQuestions/tabid/128/ID/2033/Explain-how-BABOK-categorizes-requirements.aspx)  
40. Functional and Non Functional Requirements \- GeeksforGeeks, 11월 11, 2025에 액세스, [https://www.geeksforgeeks.org/software-engineering/functional-vs-non-functional-requirements/](https://www.geeksforgeeks.org/software-engineering/functional-vs-non-functional-requirements/)  
41. What are Non-functional Requirements: Types, Examples & Approaches \- Visure Solutions, 11월 11, 2025에 액세스, [https://visuresolutions.com/alm-guide/non-functional-requirements/](https://visuresolutions.com/alm-guide/non-functional-requirements/)  
42. Stage 1 vs Stage 2 Remap: Complete Performance Guide \[2025\], 11월 11, 2025에 액세스, [https://lonestarperformance.co.uk/understanding-the-differences-what-is-stage-1-vs-stage-2-remap/](https://lonestarperformance.co.uk/understanding-the-differences-what-is-stage-1-vs-stage-2-remap/)  
43. Stage 1 Vs Stage 2 Tuning: Key Differences Explained \- ASM Tuning, 11월 11, 2025에 액세스, [https://asmtuning.co/stage-1-vs-stage-2-tuning/](https://asmtuning.co/stage-1-vs-stage-2-tuning/)  
44. Engine Remapping Stages Explained \- Stage 1, 2 and 3 \- ST Automotive Solutions, 11월 11, 2025에 액세스, [https://stautomotive.ie/engine-remapping-stages-explained-stage-1-2-and-3/](https://stautomotive.ie/engine-remapping-stages-explained-stage-1-2-and-3/)  
45. Stage 1 vs. Stage 2 Remapping: Which is Right for Your Car? \- TJL Auto Performance, 11월 11, 2025에 액세스, [https://tjlautoperformance.info/blog/stage-1-vs--stage-2-remapping--which-is-right-for-your-car--2](https://tjlautoperformance.info/blog/stage-1-vs--stage-2-remapping--which-is-right-for-your-car--2)  
46. Stage Tuning: The Ultimate Guide to ECU Remap Stages \- VIEZU, 11월 11, 2025에 액세스, [https://viezu.com/blog/stage-tuning-and-ecu-remapping-explained/](https://viezu.com/blog/stage-tuning-and-ecu-remapping-explained/)  
47. Managing Requirements from a Business Analyst or an Enterprise Architect perspective using BABOK 2.0 and/or TOGAF 9, 11월 11, 2025에 액세스, [https://www.modernanalyst.com/Resources/Articles/tabid/115/ID/1855/Managing-Requirements-from-a-Business-Analyst-or-an-Enterprise-Architect-perspective-using-BABOK-20-andor-TOGAF-9.aspx](https://www.modernanalyst.com/Resources/Articles/tabid/115/ID/1855/Managing-Requirements-from-a-Business-Analyst-or-an-Enterprise-Architect-perspective-using-BABOK-20-andor-TOGAF-9.aspx)  
48. Understanding BABOK Requirements Life Cycle Management \- Watermark Learning, 11월 11, 2025에 액세스, [https://www.watermarklearning.com/blog/babok-requirements-life-cycle-management/](https://www.watermarklearning.com/blog/babok-requirements-life-cycle-management/)  
49. Business Analysis Knowledge Areas Explained as per BABoK \- MindsMapped, 11월 11, 2025에 액세스, [https://www.mindsmapped.com/business-analysis-knowledge-areas-explained-babok/](https://www.mindsmapped.com/business-analysis-knowledge-areas-explained-babok/)  
50. Writing Non-Functional Requirements in 6 Steps, 11월 11, 2025에 액세스, [https://www.modernrequirements.com/blogs/what-are-non-functional-requirements-and-how-to-build-them/](https://www.modernrequirements.com/blogs/what-are-non-functional-requirements-and-how-to-build-them/)  
51. What Are Software Quality Attributes (NFRs): Defining and Managing Excellence | Gart, 11월 11, 2025에 액세스, [https://gartsolutions.com/what-are-software-quality-attributes-nfrs-defining-and-managing-excellence/](https://gartsolutions.com/what-are-software-quality-attributes-nfrs-defining-and-managing-excellence/)  
52. Non-functional Requirements as User Stories \- Mountain Goat Software, 11월 11, 2025에 액세스, [https://www.mountaingoatsoftware.com/blog/non-functional-requirements-as-user-stories](https://www.mountaingoatsoftware.com/blog/non-functional-requirements-as-user-stories)
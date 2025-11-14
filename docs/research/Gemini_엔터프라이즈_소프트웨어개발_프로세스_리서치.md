

# **엔터프라이즈 소프트웨어 아키텍처 프로세스 심층 분석: 요구사항, 설계, 그리고 ADR의 올바른 순서**

## **보고서 요약**

본 보고서는 'AI 협업 기반 소프트웨어 개발 방법론' 정립을 목표로 하는 귀사의 요청에 따라, 엔터프라이즈 소프트웨어 개발 프로세스, 특히 '핵심정의(요구사항)', '구현방법(설계)', 'ADR(기술결정)'의 관계와 순서를 심층 분석합니다.

**핵심 결론:** 귀사가 잠정적으로 사용 중인 **'접근법 B' (요구사항 $\\rightarrow$ 설계 $\\rightarrow$ ADR)** 는 Google, Amazon 등 주요 테크 기업들의 모범 사례 및 '속성 주도 설계(Attribute-Driven Design)'와 같은 업계 표준 원칙과 일치하는, 검증된 방식입니다.

'구현방법'(설계)을 통해 '어떻게 사용할지'와 '어떤 비기능적 요구사항(속성)'이 필요한지 명확히 한 후에야, 기술 스택(ADR)을 올바르게 결정할 수 있습니다. 기술을 먼저 결정하는 '접근법 A'는 비즈니스 요구와 불일치하는 기술을 선택할 위험이 큽니다.

AI와의 협업 환경에서, AI는 '구현방법(설계)'의 초안을 신속하게 생성하고 'ADR'의 옵션을 비교 분석하는 '조력자(Accelerator)' 역할을 수행하며, 인간은 '컨텍스트 제공'과 '최종 결정'이라는 핵심 역할을 맡아야 합니다. 본 보고서는 이러한 분석을 바탕으로 귀사의 고유한 맥락에 최적화된 구체적인 AI 협업 프로세스 플로우를 제안합니다.

---

## **Part 1\. 아키텍처 결정 기록(ADR)의 업계 표준과 실제 역할 (Q1, Q6)**

ADR(Architecture Decision Record)의 정확한 정의와 그 역할에 대한 이해는 전체 개발 프로세스를 정립하는 데 필수적인 첫걸음입니다. ADR이 프로세스의 어느 단계에 위치해야 하는지는 ADR의 근본적인 목적에서부터 귀결됩니다.

### **1.1. ADR의 정의: '왜(Why)'를 기록하는 불변의 역사**

ADR은 소프트웨어 아키텍처의 '중요한(significant)' 측면에 대해 팀이 내린 **단일 결정**을 설명하는 문서입니다.1 이는 단순한 변경 로그나 커밋 메시지를 대체하는 것이 아니라 3, 아키텍처에 중대한 영향을 미치는 결정의 근거를 보존하기 위해 존재합니다.

2011년 마이클 니가드(Michael Nygard)가 ADR 개념을 대중화한 근본적인 동기는, 시간이 지나 프로젝트에 새로 합류한 개발자가 특정 결정을 마주했을 때 "왜(why)" 그런 결정을 내렸는지 그 \*\*"동기(motivation)"\*\*를 추적할 수 있게 하기 위함이었습니다.4

여기서 '건축학적으로 중요한(Architecturally Significant)' 결정이란 다음과 같은 요소를 포함합니다 5:

* **구조 (Structure):** 마이크로서비스 채택, 모놀리식 유지 등 시스템의 전반적인 구조.  
* **비기능적 요구사항 (Non-functional Requirements):** 보안, 고가용성, 내결함성 등 품질 속성.  
* **의존성 (Dependencies):** 컴포넌트 간의 결합.  
* **인터페이스 (Interfaces):** 외부 시스템과의 통신을 위한 API 및 계약.  
* **구축 기술 (Construction Techniques):** 특정 라이브러리, 프레임워크, 도구 또는 프로세스의 선택.

ADR의 가장 표준적인 템플릿은 니가드가 제안한 \*\*'컨텍스트(Context)', '결정(Decision)', '결과(Consequences)'\*\*의 3요소로 구성됩니다.4

1. **컨텍스트 (Context):** 이 결정을 내려야만 했던 배경과 상황을 설명합니다. 기술적, 정치적, 사회적 요인 등 모든 '작용하는 힘(forces)'을 가치 중립적으로 기술합니다.4  
2. **결정 (Decision):** 이러한 컨텍스트에 대응하여 팀이 내린 구체적인 응답입니다. "우리는... 할 것이다(We will...)"와 같이 능동태로 명확하게 서술합니다.4  
3. **결과 (Consequences):** 해당 결정을 적용한 후의 결과적인 상황입니다. 이 섹션에는 긍정적인 효과뿐만 아니라, 트레이드오프로 인해 감수해야 하는 **부정적인 영향이나 새로운 제약사항**까지 모두 포함되어야 합니다.3

### **1.2. ADR 작성의 실제: '결정 과정'인가, '결정의 기록'인가? (Q6 답변)**

이 질문은 업계에서 ADR이 사용되는 두 가지 상이한 방식을 드러내는 핵심적인 지점입니다. 결론부터 말하자면, ADR은 두 가지 방식 모두로 사용되며, 이는 결정의 복잡성과 조직의 문화에 따라 달라집니다.

* 관점 1: ADR을 '결정 과정(Process)'의 매체로 사용  
  이 접근법에서 ADR 문서는 결정이 내려지기 전에 '제안됨(Proposed)' 상태로 먼저 작성됩니다.4 GitHub의 엔지니어링 블로그는 이 방식을 지지하며, ADR을 풀 리퀘스트(Pull Request)를 올리기 전에 작성하여 동료 리뷰를 받는 것을 권장합니다.6 이 경우, ADR(혹은 PR) 자체가 토론의 중심지가 되며, 동료들은 코드 리뷰에서처럼 아키텍처 결정을 리뷰합니다. 승인(merge)되면 해당 ADR은 '수락됨(Accepted)' 상태가 됩니다.7  
* 관점 2: ADR을 '결정의 최종 기록(Record)'으로 사용  
  더 복잡하고 규모가 큰 결정을 내릴 때, 많은 성숙한 조직에서는 ADR과 별개인 '설계 문서(Design Doc)' 또는 \*\*'제안서(Proposal)'\*\*를 먼저 작성합니다. 이 문서에서 여러 옵션을 심층적으로 탐색하고, 프로토타이핑을 수행하며, 격렬한 토론을 거칩니다. 모든 논의가 끝나고 최종 결정이 내려지면, 그 결과만을 ADR에 간결하게 요약하여 '기록'합니다.8

이 두 관점은 상충하는 것이 아니라, 결정의 **복잡성과 규모**에 따라 선택하는 전략입니다. 간단한 결정(예: "로깅 라이브러리로 Log4j 2 사용")은 '관점 1'로 충분하지만, 복잡한 시스템 설계(예: "채팅 메시징 백엔드 아키텍처 설계")는 '관점 2'가 필수적입니다.

이 분석을 바탕으로 Q6의 하위 질문들에 대해 명확한 답변이 가능합니다.

Q: ADR은 단순히 "기술 선택 근거" 기록인가? 아니면 "기술 선택 과정"까지 포함하나?  
A: 표준적으로 둘 다 포함합니다. Microsoft와 Google의 가이드라인에 따르면, 좋은 ADR은 최종 결정(근거)뿐만 아니라, '고려된 옵션들(Options Considered)' 9을 명시적으로 포함해야 합니다. 이 '고려된 옵션' 섹션이 바로 '기술 선택 과정'과 트레이드오프를 기록하는 부분입니다.  
Q: ADR 작성 전에 기술이 이미 결정되어 있나, 아니면 ADR 작성 중에 결정하나?  
A: 이는 조직의 프로세스에 따라 다릅니다.

* **Case 1 (One Medical 사례):** '제안서'와 '아키텍처 위원회 미팅'을 통해 기술이 *먼저 결정*되고, ADR은 이 결정을 공식적으로 *기록*하는 용도로 사용됩니다.8  
* **Case 2 (GitHub 사례):** ADR을 '제안(Proposed)' 상태로 *작성하는 과정*이 곧 *결정하는 과정*이며, 동료 리뷰를 통해 최종 결정이 확정됩니다.6

귀사의 경우 "구현방법"이라는 명확한 설계 문서 단계가 이미 존재하므로, 'Case 1' (ADR as Record)을 따르는 것이 논리적으로 명확합니다. 즉, ADR은 "구현방법" 문서에서 논의된 내용을 바탕으로 *최종 결정된 사항을 기록*하는 용도로 사용하는 것이 바람직합니다.

### **1.3. ADR과 타 문서의 관계: 설계 문서(Design Doc)는 ADR의 '어머니'다 (Q1 답변)**

ADR은 단독으로 존재하지 않으며, 다른 핵심 개발 문서들과 유기적인 관계를 맺습니다.

* 요구사항 명세서 (SRD/PRD \- Software/Product Requirements Document):  
  ADR의 \*\*핵심 입력(Input)\*\*입니다.5 요구사항 명세서는 ADR의 '컨텍스트(Context)' 섹션에 "우리가 왜 이 결정을 내려야 하는가?"에 대한 비즈니스 및 기능적, 비기능적 요구사항을 제공합니다.  
* 설계 문서 (Design Doc / Technical Design Document / Proposal):  
  ADR의 선행 탐색(Preceding Exploration) 문서입니다. 이 둘의 관계는 업계 표준 프로세스를 이해하는 데 가장 중요합니다.  
  * **역할 차이:** Google의 'Design Doc' 문화 12나 One Medical의 'Proposal' 8처럼, 설계 문서는 "아직 결정되지 않은 문제"에 대해 여러 옵션을 제시하고, 트레이드오프를 분석하며, 이해관계자 간의 합의를 이끌어내는 '토론의 장'입니다. 이 문서는 탐색 과정에서 매우 길고 복잡해질 수 있습니다.13  
  * **흐름:** 반면 ADR은 '최종 결정'과 그 '근거'에만 집중하며 간결하고 명확해야 합니다.4  
  * 이상적인 프로세스 흐름은 다음과 같습니다:  
    1. 요구사항 명세서 (PRD)가 '무엇을' 만들지, '어떤 제약(NFR)'이 있는지 정의합니다.  
    2. 설계 문서 (Design Doc)가 이 문제를 풀기 위한 1개 이상의 아키텍처/기술 옵션을 탐색하고 비교합니다. (예: "채팅 앱을 위해 WebSocket, Long Polling, gRPC-Stream 비교 분석")  
    3. 팀(혹은 아키텍처 위원회)이 설계 문서를 리뷰하고 토론하여 *결정*을 내립니다.  
    4. 이 *결정*("우리는 WebSocket을 사용하기로 결정했다")과 그 *이유*("실시간 양방향성이 핵심 요구사항이며, Long Polling 대비 효율적이므로")가 ADR로 기록됩니다.

Q1에 대한 최종 답변:  
ADR은 요구사항 분석 직후에 작성되지 않습니다. 또한 설계 단계 이후에 작성되는 것이 일반적이나, 더 정확히는 상세 설계(옵션 탐색 및 비교)가 완료된 직후, 그리고 본격적인 구현 시작 직전에 작성됩니다. ADR은 '요구사항'의 입력을 받고, '설계 문서'에서 탐색된 내용을 바탕으로 '결정'을 기록하여 '구현'의 지침이 됩니다.

---

## **Part 2\. 엔터프라이즈 기업의 실제 아키텍처 프로세스 (Q2, Q4)**

귀사의 질문(Q2, Q4)은 이론적인 정의를 넘어, Google, Amazon과 같은 최고 수준의 기업들이 실제로 어떻게 일하는지에 초점을 맞추고 있습니다. 이들 기업의 사례는 귀사의 '접근법 B' (설계 $\\rightarrow$ 기술결정)가 왜 표준인지를 명확히 보여줍니다.

### **2.1. Google의 '설계 문서(Design Doc)' 문화: 합의 우선, 구현은 나중**

Google은 "코드는 벽돌과 모르타르라면, 설계 문서는 청사진"이라는 철학을 가지고 있습니다.12 이들은 본격적인 구현에 앞서 '설계 문서(Design Doc)'를 통해 합의를 이루는 문화를 핵심으로 삼습니다.12

* **프로세스 흐름:**  
  1. **요구사항/목표 정의 (Goals and Non-Goals):** 무엇을 만들고, 더 중요하게는, 무엇을 만들지 않을 것인지 명확히 합니다.15  
  2. **설계 문서 작성 (Design Doc):** 문제를 해결하기 위한 여러 아키텍처 옵션과 디자인을 탐색합니다. 이 문서는 엔지니어가 자신의 영향력을 확장하고 12, 복잡한 문제에 대해 전략적으로 생각하게 만듭니다.12  
  3. **리뷰 및 합의 (Consensus):** 이 문서를 관련 팀(엔지니어, PM, SRE, 보안팀 등)과 공유하고 피드백을 받아 합의점을 찾습니다. 이 과정은 수천 줄의 코드를 작성한 후 발생할 수 있는 값비싼 재작업을 방지하는 핵심 단계입니다.12  
  4. **구현:** 합의된 설계를 바탕으로 구현을 시작합니다.  
* **ADR과의 관계:** Google이 'ADR'이라는 용어를 보편적으로 사용하는지는 불분명하나, '설계 문서'의 "결정(Decision)" 또는 "권장안(Recommended Approach)" 섹션이 사실상 ADR의 역할을 수행합니다. 중요한 것은 이들의 프로세스가 명백하게 **'탐색 및 설계(Design Doc)'를 '결정 및 구현'보다 선행**시킨다는 점입니다.

### **2.2. Amazon(AWS)의 '사용 사례 주도(Use-Case Driven)' 접근법**

Amazon(AWS)은 고객들에게 솔루션 아키텍처를 설계할 때 '사용 사례 주도 아키텍처(Use-Case Driven Architecture)' 접근법을 강력히 권장합니다.16 이는 "익숙한 기술"을 먼저 선택하는 함정을 피하고 비즈니스 프로세스에 IT 구성 요소를 맞추는 방식입니다.16

* 프로세스 흐름 (3단계) 16:  
  1. **1단계 (Identify and outline use cases):** 비즈니스 프로세스, 즉 \*\*'사용 사례'\*\*를 식별하고 정의합니다. (이는 귀사의 '핵심정의'와 정확히 일치합니다.)  
  2. **2단계 (Specify primary use cases):** 핵심 사용 사례를 바탕으로 \*\*'구체적인 요구사항(concrete requirements)'\*\*을 도출합니다. (이는 귀사의 '구현방법'에서 시나리오를 구체화하는 단계와 일치합니다.)  
  3. **3단계 (Implement the architecture):** 2단계에서 도출된 요구사항을 바탕으로 \*\*'도구와 인프라(기술)'를 선택(select tools and infrastructure)\*\*합니다. (이는 귀사의 'ADR' 단계와 일치합니다.)  
* **핵심 통찰:** Amazon의 공식 권장 방법론은 귀사의 **'접근법 B' (요구사항 $\\rightarrow$ 설계/시나리오 $\\rightarrow$ 기술결정)** 와 완벽하게 일치합니다. 이는 "어떻게 사용할지"(사용 사례 및 구체적 요구사항)를 먼저 정의해야만 "무엇을 사용할지"(기술)를 올바르게 선택할 수 있다는 아키텍처의 제1원칙을 명확히 보여줍니다.

### **2.3. One Medical의 '이중 다이아몬드(Double-Diamond)' 결정 프로세스**

One Medical(현재 Amazon 소속)은 아키텍처 결정을 위해 '제안(Proposal)'과 '결정(Decision)'을 명확히 분리하는 매우 성숙한 '이중 다이아몬드' 프로세스를 운영합니다.8

* 프로세스 흐름 8:  
  1. **1단계: 제안서 생성 (Creating the Proposal) \- (첫 번째 다이아몬드: 탐색)**  
     * 문제를 정의하고, 여러 옵션을 문서화합니다(장단점, 프로토타이핑 포함).  
     * 이 제안서를 전체 엔지니어링팀에 공유하여 광범위한 피드백을 수집하고 반복 개선합니다.  
     * (이는 귀사의 '구현방법' 단계에 해당합니다.)  
  2. **2단계: 최종 결정 (Finalizing the Decision) \- (두 번째 다이아몬드: 결정)**  
     * 결정 리드(Decision Lead)는 '아키텍처 위원회(Architecture Council)'를 포함한 소규모 전문가 그룹과 함께 결정 미팅을 예약합니다.  
     * 이 미팅에서 1단계의 제안서를 바탕으로 토론하고 최종 결정을 내립니다.  
  3. **3단계: 결과 전파 (Communicating the Outcome)**  
     * 이 *최종 결정*을 **ADR로 작성**하여 공식화합니다.  
     * 완성된 ADR을 다시 전체 엔지니어링팀에 전파하여 결정 사항과 그 근거를 공유합니다.  
* **핵심 통찰:** 이 사례는 **'설계 제안서(Proposal)'가 'ADR(Decision Record)'에 명백히 선행**함을 보여주는 가장 강력하고 구체적인 증거입니다. ADR은 '탐색'의 도구가 아니라 '결정'의 *기록*이며, 설계(탐색)가 완료된 후에 작성됩니다.

### **2.4. \[사례 연구\] "채팅 애플리케이션 개발"의 문서 작성 순서 (Q4 답변)**

가상의 "실시간 채팅 애플리케이션 개발" 프로젝트를 예로 들어, 위 사례(Google, Amazon, One Medical)를 종합한 이상적인 문서 흐름을 재구성해 봅니다.

* **1\. 문서 1: 제품 요구사항 명세서 (PRD) \- (귀사의 '핵심정의')**  
  * **내용:** "사용자는 1:1 및 그룹 채팅을 할 수 있어야 한다.", "사용자는 실시간으로 타이핑 인디케이터를 볼 수 있어야 한다.", "비기능적 요구사항: 최대 1,000명 동시 접속을 지원해야 한다.", "메시지 전송 지연 시간은 99퍼센타일 기준 500ms 이내여야 한다."  
  * **역할:** 비즈니스 목표와 핵심 기능, 비기능적 요구사항(NFR)을 정의합니다.  
* **2\. 문서 2: 기술 설계 문서 (TDD / Design Doc) \- (귀사의 '구현방법')**  
  * **내용:** PRD를 바탕으로 실제 구현 방법을 탐색합니다.  
  * *A. 시스템 아키텍처:* "메시징 서버, 인증 서비스, 사용자 상태 서비스로 구성된 마이크로서비스 아키텍처"  
  * *B. 데이터 모델:* "User, Channel, Message 테이블 스키마 정의"  
  * *C. API 명세:* sendMessage(channelId, messageContent), receiveMessageEvents()  
  * *D. 핵심 기술 탐색 (Options Analysis):*  
    * "실시간 메시지 전송 기술(NFR: 500ms 이내, 1000명 동시 접속)을 위한 비교:  
      * *옵션 1: WebSocket:* 양방향, 낮은 지연. (장점: 표준, 효율적 / 단점: 일부 방화벽 문제)  
      * *옵션 2: Long Polling:* 구현 용이. (장점: HTTP 기반 / 단점: 서버 부하, 지연, NFR 충족 어려움)  
      * *옵션 3: gRPC Streaming:* 고성능. (장점: Protobuf, 효율적 / 단점: 브라우저 호환성, 러닝 커브)"  
  * *E. 권장안:* "실시간성(NFR)과 표준 준수를 고려하여 WebSocket(옵션 1)을 권장함."  
  * **역할:** 요구사항을 충족하기 위한 구체적인 설계안과 기술 옵션을 '탐색'하고 '권장'합니다.  
* **3\. 문서 3: 아키텍처 결정 기록 (ADR-001) \- (귀사의 'ADR')**  
  * **내용:** 설계 문서(TDD)의 결정을 공식화하여 기록합니다.  
  * *제목:* ADR-001: 실시간 메시지 전송 기술로 WebSocket 채택  
  * *컨텍스트:* "채팅 애플리케이션은 낮은 지연 시간(500ms 이내)의 양방향 통신을 필요로 함 (PRD-Chat-v1 참조)." 4  
  * *고려된 옵션:* "Long Polling, gRPC Streaming (TDD-Chat-v1의 D섹션 참조)." 9  
  * *결정:* "WebSocket 기술을 사용하여 메시징 서버와 클라이언트 간의 통신을 구현한다." 4  
  * *결과:* "클라이언트는 WebSocket을 지원해야 함. 서버는 대규모 동시 연결을 처리할 수 있어야 함(예: Socket.IO, Spring WebFlux). Long Polling 대비 서버 구현 복잡성이 증가함." 4  
  * **역할:** 설계 단계에서 '탐색'되고 '결정'된 사항을 공식적으로 '기록'하여 향후 변경을 방지하고 역사적 맥락을 제공합니다.

이 예시는 \*\*설계 문서('구현방법')\*\*가 '왜' 기술이 필요한지(컨텍스트), '어떤' 옵션이 있는지(탐색)를 제공하며, **ADR**은 이 탐색을 바탕으로 '무엇을' 선택했는지(결정)를 기록하는 명확한 선후 관계를 보여줍니다.

---

## **Part 3\. 핵심 딜레마 분석: 기술 스택, 언제 결정해야 하는가? (Q3, Q5)**

귀사의 핵심 딜레마는 '접근법 A'(기술 먼저)와 '접근법 B'(설계 먼저) 사이의 선택입니다. 업계 표준과 엔지니어링 원칙은 이 질문에 대해 매우 명확한 답을 제시합니다.

### **3.1. 기술 결정의 올바른 시점: '속성'이 '설계'를 주도할 때 (Q3 답변)**

기술 스택(예: Redis vs. PostgreSQL, Python vs. Java)은 '요구사항'만 보고 즉시 결정해서는 안 됩니다. 이는 엔지니어링 성숙도가 낮은 조직에서 흔히 발생하는 실수이며, "기술 우선주의(Technology-first)" 17 또는 "이력서 주도 개발(Resume-Driven Development)" 18이라는 심각한 함정에 빠지기 쉽습니다. (예: "요즘 Redis가 유행이니 무조건 쓰자" 또는 "내가 Java는 잘 아니까 Java로 하자")

핵심 원칙: 속성 주도 설계 (Attribute-Driven Design, ADD)  
카네기 멜런 소프트웨어 공학 연구소(SEI)의 저명한 저서 Software Architecture in Practice에서 강조하는 핵심 방법론은 '속성 주도 설계(ADD)'입니다.19  
ADD의 핵심은 아키텍처가 기능적 요구사항뿐만 아니라, \*\*비기능적 요구사항(Quality Attributes)\*\*에 의해 주도되어야 한다는 것입니다.19 비기능적 요구사항은 성능(Performance), 확장성(Scalability), 가용성(Availability), 수정용이성(Modifiability), 보안(Security) 등을 의미합니다.19

ADD에 기반한 올바른 기술 결정 프로세스는 다음과 같습니다:

1. '요구사항'(예: 채팅 기능)을 입력받습니다.  
2. **'설계(구현방법)'** 단계에서 이 요구사항을 만족시키기 위해 필요한 \*\*'핵심 속성(Quality Attributes)'\*\*을 식별하고 시나리오로 구체화합니다.19  
   * (예: "메시지 전송은 **100ms 이내**의 \*\*낮은 지연 시간(Performance)\*\*이 필요하다")  
   * (예: "시스템은 \*\*동시 100만 연결(Scalability)\*\*을 지원해야 한다")  
   * (예: "데이터는 \*\*99.99%의 가용성(Availability)\*\*이 필요하다")  
3. 이러한 *속성*들을 가장 잘 충족시킬 수 있는 기술(예: Redis, Kafka, RabbitMQ)을 '탐색'하고 최종 '결정(ADR)'합니다.

**Q3에 대한 직접 답변:** 기술 스택은 \*\*'어떻게 사용할지'(설계)\*\*가 구체화되고, 이로 인해 필요한 \*\*'비기능적 속성'\*\*이 명확해진 후에 결정해야 합니다. PostgreSQL을 단순 Key-Value 캐시로 쓸지(잘못된 사용), 복잡한 관계형 데이터 저장소로 쓸지(올바른 사용)는 '어떻게 사용할지'에 대한 설계(구현방법)가 나와야만 알 수 있습니다.

### **3.2. 접근법 A vs. 접근법 B: 심층 비교 분석 (Q5 답변)**

귀사가 제시한 두 가지 접근법은 현대 소프트웨어 공학의 핵심적인 갈등을 보여줍니다.

#### **접근법 A: 요구사항 분석 $\\rightarrow$ ADR (기술 결정) $\\rightarrow$ 상세 설계 $\\rightarrow$ 구현**

* **프로세스:** "채팅 앱이 필요하다" $\\rightarrow$ "기술은 Java와 Redis를 쓰자\!" (ADR) $\\rightarrow$ "이제 Java와 Redis로 어떻게 채팅 앱을 만들지 설계해 보자."  
* **장점:**  
  * 팀이 이미 해당 기술에 매우 익숙할 경우(예: 사내 표준 스택) 의사결정이 빠르고 개발 속도가 단기적으로 빨라 보일 수 있습니다.  
  * 기술적 제약이 명확해져 설계의 범위가 좁혀집니다.  
* **단점:**  
  * **최적화 함정 (Premature Optimization/Pessimization):** 요구사항에 맞지 않는 기술을 선택할 위험이 매우 높습니다.17 (예: 설계를 해보니 채팅방 목록 같은 관계형 데이터가 필요한데, 이미 Key-Value 저장소인 Redis를 선택해버림)  
  * **설계의 종속성:** 기술이 설계를 제약합니다. 'Java와 Redis로 할 수 있는' 설계만 생각하게 되어 문제 해결에 최적화된 아키텍처가 나오기 어렵습니다.  
  * **높은 변경 비용:** 설계 단계에서 해당 기술이 부적합함을 발견해도, 이미 ADR로 결정했기 때문에 이를 되돌리기는 정치적/기술적으로 매우 비싼 비용이 듭니다.

#### **접근법 B: 요구사항 분석 $\\rightarrow$ 상세 설계 (구현방법) $\\rightarrow$ ADR (기술 결정) $\\rightarrow$ 구현**

* **프로세스:** "채팅 앱이 필요하다" $\\rightarrow$ "설계해 보니, 실시간 메시지 큐와 사용자 상태 저장을 위한 빠른 Key-Value 저장소가 필요하네." (설계) $\\rightarrow$ "이 요구사항을 가장 잘 만족하는 기술은 Kafka와 Redis다." (ADR)  
* **장점:**  
  * **요구사항-기술 일치 (Requirement-Technology Fit):** 비즈니스 및 비기능적 요구사항(속성)에 가장 적합한 기술을 선택하게 됩니다.16  
  * **설계의 유연성:** 기술에 종속되지 않은, 문제 해결에 최적화된 아키텍처를 먼저 구상할 수 있습니다.  
  * **낮은 변경 비용:** 설계 단계에서 다양한 기술 옵션을 탐색하므로(예: Redis vs. Memcached), 최종 결정의 품질이 높고 위험이 낮습니다.  
* **단점:**  
  * 초기 설계 단계에서 더 많은 시간과 아키텍트의 높은 역량이 필요합니다.  
  * 결정이 늦어지는 것처럼 보일 수 있습니다. (그러나 이는 잘못된 결정을 피하기 위한 필수적인 투자입니다.)

### **3.3. 업계의 표준: 왜 '접근법 B'가 승리하는가?**

Google의 '설계 문서' 문화 12, Amazon의 '사용 사례 주도' 접근법 16, One Medical의 '제안서 우선' 프로세스 8, 그리고 '속성 주도 설계(ADD)' 19 원칙은 모두 **접근법 B**를 강력하게 지지합니다.

성숙한 엔지니어링 조직은 '무엇을 만들지(요구사항)'와 '어떻게 만들지(설계)'가 '어떤 도구로 만들지(기술)'를 결정해야 한다는 것을 압니다.

**결론:** 업계에서는 압도적으로 '접근법 B'를 표준으로 사용합니다. 귀사의 현재 고민('보충 설명')은 '접근법 B'가 맞다는 것을 확인받고 싶은 것이며, **이 보고서는 귀사의 접근법이 업계 모범 사례와 일치함을 강력히 확증합니다.**

다음 표는 두 접근법의 차이를 명확히 요약합니다.

#### **\[표\] 접근법 A vs. 접근법 B 상세 비교**

| 기준 | 접근법 A (ADR → 설계) | 접근법 B (설계 → ADR) |
| :---- | :---- | :---- |
| **결정 주체** | 기술(Technology) | 요구사항/설계(Requirement/Design) |
| **프로세스** | 기술이 설계를 제약 | 설계가 기술을 선택 |
| **주요 위험** | 오버/언더 엔지니어링, 요구사항 불일치 17 | 분석 마비 (Analysis Paralysis) |
| **업계 용어** | 기술 주도 (Technology-Driven), 이력서 주도 (Resume-Driven) 18 | 요구사항 주도 (Requirements-Driven), 속성 주도 (Attribute-Driven) 19 |
| **유연성** | 낮음 (선택한 기술에 종속됨) | 높음 (문제에 최적화된 기술 선택 가능) |
| **대표 사례** | (대부분의 성숙한 기업은 이 방식을 피함) | Google, Amazon, One Medical 8 |
| **권장 여부** | **비권장 (매우 위험)** | **강력 권장 (업계 표준)** |

---

## **Part 4\. 권장 사항: AI 협업 기반 개발 방법론 정립**

본 보고서의 분석 결과를 바탕으로, 귀사의 'AI 협업 기반 개발 방법론' 정립을 위한 구체적인 권장 사항을 제안합니다.

### **4.1. 귀사의 현재 프로세스 검증: '접근법 B'는 올바른 방향입니다.**

귀사가 잠정적으로 수립한 **핵심정의 (요구사항) $\\rightarrow$ 구현방법 (설계/시나리오) $\\rightarrow$ ADR (기술결정)** 순서는 본 보고서에서 분석한 업계 모범 사례(Amazon, One Medical) 및 아키텍처 원칙(ADD)과 정확히 일치하는, 매우 올바른 방향입니다.

특히 '구현방법' 단계에서 사용 시나리오를 구체화하는 것은, 기술 선택(ADR)에 필요한 '비기능적 속성'을 도출하는 핵심적인 '설계' 활동입니다. 이 순서를 반드시 유지하고 조직 내에서 표준으로 확립해야 합니다.

### **4.2. 'AI 협업'의 새로운 패러다임: 인간은 '결정권자', AI는 '초안 작성자'**

귀사의 핵심 맥락인 'AI와의 협업'은 이 검증된 프로세스를 *대체*하는 것이 아니라 *가속화*하는 방향으로 적용되어야 합니다. Generative AI는 소프트웨어 아키텍처 수명 주기를 변화시키고 있습니다.21

* AI의 역할: 조력자 (Accelerator & Collaborator)  
  AI는 방대한 훈련 데이터를 기반으로 '고수준 설계 청사진'을 제안하고 23, 문서 초안을 작성하며 25, 반복적인 작업을 자동화하여 27 생산성을 높이는 데 탁월합니다. AWS가 제시하는 'AI-DLC' 모델처럼 AI는 단순 도구가 아닌 '협업자(Collaborator)'입니다.28  
* 인간의 역할: 결정권자 (Decider & Context-Provider)  
  AI는 현재 상태에서 비즈니스의 고유한 컨텍스트, 팀의 기술 수준, 조직 문화, 장기적인 전략적 목표를 이해하지 못합니다.24 또한 AI가 제안한 설계에는 보안 취약점이나 과도한 복잡성이 포함될 수 있습니다.24  
  따라서 인간 아키텍트는 '컨텍스트 제공', 'AI 생성물 검증(보안, 품질, 적절성)', 그리고 가장 중요한 \*\*'최종 결정'\*\*을 맡아야 합니다.26  
  Salesforce가 제시한 '인간 주도, AI 기반(Human-Led, AI-Powered)' 접근법 26과 AWS의 'AI-DLC' 28가 귀사가 지향해야 할 가장 성숙한 협업 모델입니다.

### **4.3. 제안: AI 협업 기반의 권장 개발 플로우**

귀사의 3단계 프로세스('핵심정의', '구현방법', 'ADR')에 '인간 주도, AI 기반' 모델을 적용한 구체적인 실행 플로우를 다음과 같이 제안합니다.

#### **1\. 핵심정의 (인간 주도 $\\rightarrow$ AI 명료화)**

1. 인간 (도메인 전문가 Jason): 비즈니스 요구사항과 7가지 핵심 질문을 정의합니다. (인간의 고유한 '컨텍스트' 제공 26)  
2. AI (조력자): Jason의 자연어 요구사항을 입력받아, 모호한 부분을 명확히 하도록 역질문하거나, 구조화된 '요구사항 명세서' 초안을 생성합니다.  
3. 인간 (검토): AI가 생성한 명세서를 검토하고 확정합니다.

#### **2\. 구현방법 (AI 초안 작성 $\\rightarrow$ 인간 검토/상세화)**

1. AI (초안 작성자): 확정된 '핵심정의' 문서를 입력받아, 6가지 사용 시나리오, 필요한 데이터 모델, API 엔드포인트 초안, 고수준 아키텍처 다이어그램 등 '구현방법' 문서의 **80% 초안을 신속하게 생성**합니다.23  
2. 인간 (아키텍트/개발자): AI가 생성한 초안을 *검토*합니다. AI가 놓친 비즈니스 룰, 예외 케이스, 조직의 기존 아키텍처와의 통합, 보안 고려사항24 등 핵심적인 20%를 추가하여 문서를 '상세화'하고 완성합니다.  
3. *(이 단계의 결과로 '어떤 기술 속성이 필요한지'가 명확해집니다.)*

#### **3\. 기술 탐색 및 ADR (AI 리서치 $\\rightarrow$ 인간 결정)**

1. 인간 (아키텍트): 완성된 '구현방법' 문서를 바탕으로 "100만 동시 접속 캐시가 필요하다"와 같은 구체적인 기술 요구사항(ASR)을 식별합니다.  
2. 인간 (지시자): AI에게 "현재 우리 팀의 기술 스택(예: Spring)과 이 '구현방법'의 성능 요구사항을 고려하여, Redis, Memcached, Hazelcast를 캐시 솔루션으로 비교하고 ADR 초안을 작성해 줘."라고 지시합니다.26  
3. AI (리서치 보조): 각 옵션의 장단점, 비용, 성능, 기존 스택과의 호환성 등을 비교하는 자료와 함께 '고려된 옵션'이 채워진 **ADR 초안을 생성**합니다.25  
4. 인간 (최종 결정권자): AI가 생성한 비교 자료와 '구현방법'의 요구사항, 그리고 팀의 역량(AI가 모르는 컨텍스트)을 종합적으로 검토하여 \*\*최종 기술을 '결정'\*\*합니다.26  
5. AI (기록자): 인간의 결정을 바탕으로 '결정' 및 '결과' 섹션을 채워 공식적인 ADR 문서를 포맷에 맞게 최종 생성합니다.

이 AI 협업 플로우는 '구현방법(설계)'이 'ADR(기술결정)'보다 선행하는 \*\*'접근법 B'\*\*를 완벽하게 지원하며, AI를 통해 각 단계의 문서화 및 탐색 비용을 획기적으로 줄여 인간이 더 창의적이고 전략적인 '결정'에 집중할 수 있도록 합니다.

---

## **Part 5\. 참고 자료 및 심화 학습 자료**

본 보고서의 분석에 사용된 핵심 자료 및 귀사의 방법론 정립에 도움이 될 심화 자료 목록입니다.

### **ADR의 원칙과 실제**

* **\[아티클\] Michael Nygard, "Documenting Architecture Decisions" (2011)** 4  
  * ADR 개념을 대중화한 원본 아티클. '컨텍스트, 결정, 결과'라는 핵심 템플릿과 ADR이 필요한 '이유'를 제시합니다.  
* **\[엔지니어링 블로그\] GitHub, "Why Write ADRs"** 6  
  * ADR을 풀 리퀘스트 *전에* 작성하여 리뷰 품질을 높이고 팀 커뮤니케이션을 개선하는 실용적인 사례를 제공합니다.  
* **\[기술 가이드\] Microsoft Azure, "Architecture Decision Record"** 9  
  * ADR이 '고려된 옵션'과 '트레이드오프'를 포함해야 함을 명시한 엔터프라이즈 가이드라인입니다.

### **엔터프라이즈 설계 프로세스**

* **\[도서\] *Software Engineering at Google*** (Titus Winters et al. 요약본) 12  
  * 구현 전에 '설계 문서(Design Doc)'를 통해 합의를 이루는 Google의 문화를 엿볼 수 있습니다.  
* **\[엔지니어링 블로그\] AWS Blog, "Use-Case Driven Architecture"** 16  
  * '사용 사례 $\\rightarrow$ 요구사항 $\\rightarrow$ 기술 선택'이라는 '접근법 B'를 명확하게 지지하는 Amazon의 공식 가이드입니다.  
* **\[엔지니어링 블로그\] One Medical, "Troubleshooting our architecture decision process"** 8  
  * '제안서(설계) $\\rightarrow$ 결정 $\\rightarrow$ ADR(기록)'으로 이어지는 성숙한 실제 기업 사례를 상세히 보여줍니다.

### **아키텍처 설계 원칙 (필독서)**

* **\[도서\] *Software Architecture in Practice (SEI Series)*** (Len Bass et al. 요약본) 19  
  * '속성 주도 설계(Attribute-Driven Design, ADD)'라는 핵심 개념을 소개합니다. '어떻게 사용할지'(설계)가 '무엇을 쓸지'(기술)를 결정해야 하는 이유에 대한 강력한 이론적 근간을 제공합니다.

### **AI와 개발 방법론**

* **\[엔지니어링 블로그\] Salesforce, "Human-Led, AI-Powered Approach"** 26  
  * AI를 ADR 초안 작성에 활용하되, 인간이 컨텍스트와 최종 결정을 책임지는 구체적인 협업 모델을 제시합니다.  
* **\[엔지니어링 블로그\] AWS Blog, "AI-Driven Development Lifecycle (AI-DLC)"** 28  
  * AI를 단순 도구가 아닌 '협업자'로 규정하고, 이 과정에서 인간이 '결정'을 내리는 핵심 역할을 강조합니다.

#### **참고 자료**

1. 11월 11, 2025에 액세스, [https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html\#:\~:text=An%20architectural%20decision%20record%20(ADR,its%20context%2C%20and%20its%20consequences.](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html#:~:text=An%20architectural%20decision%20record%20\(ADR,its%20context%2C%20and%20its%20consequences.)  
2. Architecture decision record (ADR) examples for software planning, IT leadership, and template documentation \- GitHub, 11월 11, 2025에 액세스, [https://github.com/joelparkerhenderson/architecture-decision-record](https://github.com/joelparkerhenderson/architecture-decision-record)  
3. Why you should be using architecture decision records to document your project \- Red Hat, 11월 11, 2025에 액세스, [https://www.redhat.com/en/blog/architecture-decision-records](https://www.redhat.com/en/blog/architecture-decision-records)  
4. Documenting Architecture Decisions \- Cognitect.com, 11월 11, 2025에 액세스, [https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions)  
5. ADR process \- AWS Prescriptive Guidance \- AWS Documentation, 11월 11, 2025에 액세스, [https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html)  
6. Why Write ADRs \- The GitHub Blog, 11월 11, 2025에 액세스, [https://github.blog/engineering/architecture-optimization/why-write-adrs/](https://github.blog/engineering/architecture-optimization/why-write-adrs/)  
7. Documenting Decisions as a Core Team Process \- Maxim Gorin, 11월 11, 2025에 액세스, [https://maxim-gorin.medium.com/documenting-decisions-as-a-core-team-process-305e0d949803](https://maxim-gorin.medium.com/documenting-decisions-as-a-core-team-process-305e0d949803)  
8. Part 2: Troubleshooting our Architecture Decision Process | by One ..., 11월 11, 2025에 액세스, [https://medium.com/one-medical-technology/part-2-troubleshooting-our-architecture-decision-process-40af5c5b061e](https://medium.com/one-medical-technology/part-2-troubleshooting-our-architecture-decision-process-40af5c5b061e)  
9. Architecture decision record \- Microsoft Azure Well-Architected ..., 11월 11, 2025에 액세스, [https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record)  
10. Architecture decision records overview | Cloud Architecture Center ..., 11월 11, 2025에 액세스, [https://docs.cloud.google.com/architecture/architecture-decision-records](https://docs.cloud.google.com/architecture/architecture-decision-records)  
11. AWS Prescriptive Guidance: Using architectural decision records to streamline technical decision-making for a software development project \- AWS Documentation, 11월 11, 2025에 액세스, [https://docs.aws.amazon.com/pdfs/prescriptive-guidance/latest/architectural-decision-records/architectural-decision-records.pdf](https://docs.aws.amazon.com/pdfs/prescriptive-guidance/latest/architectural-decision-records/architectural-decision-records.pdf)  
12. Design Docs at Google | Hacker News, 11월 11, 2025에 액세스, [https://news.ycombinator.com/item?id=23915521](https://news.ycombinator.com/item?id=23915521)  
13. Why we keep forgetting our own Architecture Decisions (and how ADRs helped) | by Nicolás Azrak | Medium, 11월 11, 2025에 액세스, [https://medium.com/@nicolas.azrak/why-we-keep-forgetting-our-own-architecture-decisions-and-how-adrs-helped-5a10b1d5e4ef](https://medium.com/@nicolas.azrak/why-we-keep-forgetting-our-own-architecture-decisions-and-how-adrs-helped-5a10b1d5e4ef)  
14. Design Docs at Google: How to Write Effective Software Design Documents \- Lodely, 11월 11, 2025에 액세스, [https://www.lodely.com/blog/design-docs-at-google](https://www.lodely.com/blog/design-docs-at-google)  
15. How I Wrote My First Software Design Doc To Win New Project \- Daniel Idaszak, 11월 11, 2025에 액세스, [https://www.idaszak.com/posts/first-software-design-doc/](https://www.idaszak.com/posts/first-software-design-doc/)  
16. How Exxeta Improves IT Planning with Use-Case Driven ..., 11월 11, 2025에 액세스, [https://aws.amazon.com/blogs/apn/how-exxeta-improves-it-planning-with-use-case-driven-architecture-on-aws/](https://aws.amazon.com/blogs/apn/how-exxeta-improves-it-planning-with-use-case-driven-architecture-on-aws/)  
17. If 'consolidation' is a solution that marketing teams need, then why ..., 11월 11, 2025에 액세스, [https://www.kentico.com/discover/blog/why-has-complexity-not-been-solved](https://www.kentico.com/discover/blog/why-has-complexity-not-been-solved)  
18. The Tale of Two Teams: Requirements-Driven vs. Resume-Driven ..., 11월 11, 2025에 액세스, [https://blog.realkinetic.com/the-tale-of-two-teams-requirements-driven-vs-resume-driven-development-1f44afc01e4b](https://blog.realkinetic.com/the-tale-of-two-teams-requirements-driven-vs-resume-driven-development-1f44afc01e4b)  
19. Software Architecture in Practice | Summary, Quotes, FAQ, Audio, 11월 11, 2025에 액세스, [https://sobrief.com/books/software-architecture-in-practice-sei-series-in-software-engineering](https://sobrief.com/books/software-architecture-in-practice-sei-series-in-software-engineering)  
20. \[Book Review\] Software Architecture in Practice \- · Los Techies, 11월 11, 2025에 액세스, [https://lostechies.com/evanhoff/2008/04/08/book-review-software-architecture-in-practice/](https://lostechies.com/evanhoff/2008/04/08/book-review-software-architecture-in-practice/)  
21. Generative AI for Software Architecture. Applications, Challenges, and Future Directions, 11월 11, 2025에 액세스, [https://arxiv.org/html/2503.13310v2](https://arxiv.org/html/2503.13310v2)  
22. Transforming the Software Development Lifecycle (SDLC) with Generative AI | AWS Partner Network (APN) Blog, 11월 11, 2025에 액세스, [https://aws.amazon.com/blogs/apn/transforming-the-software-development-lifecycle-sdlc-with-generative-ai/](https://aws.amazon.com/blogs/apn/transforming-the-software-development-lifecycle-sdlc-with-generative-ai/)  
23. Generative AI use cases for architecture and design \- AWS Prescriptive Guidance, 11월 11, 2025에 액세스, [https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-accelerate-software-dev-lifecycle-gen-ai/generative-ai-capabilities-arch-design.html](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-accelerate-software-dev-lifecycle-gen-ai/generative-ai-capabilities-arch-design.html)  
24. Generative AI in Software Architecture: Don't Replace Your ..., 11월 11, 2025에 액세스, [https://medium.com/inspiredbrilliance/generative-ai-in-software-architecture-dont-replace-your-architects-yet-cde0c5d462c5](https://medium.com/inspiredbrilliance/generative-ai-in-software-architecture-dont-replace-your-architects-yet-cde0c5d462c5)  
25. FREE AI Powered Architecture Decision Record Generator | Optimize with Workik AI, 11월 11, 2025에 액세스, [https://workik.com/ai-powered-architecture-decision-record-generator](https://workik.com/ai-powered-architecture-decision-record-generator)  
26. Architectural Decisions: A Human-Led, AI-Powered Approach ..., 11월 11, 2025에 액세스, [https://www.salesforce.com/blog/architectural-decisions-human-led-ai-powered-approach/](https://www.salesforce.com/blog/architectural-decisions-human-led-ai-powered-approach/)  
27. How Generative AI Is Changing Software Development: Key Insights from the DORA Report, 11월 11, 2025에 액세스, [https://www.opslevel.com/resources/how-generative-ai-is-changing-software-development-key-insights-from-the-dora-report](https://www.opslevel.com/resources/how-generative-ai-is-changing-software-development-key-insights-from-the-dora-report)  
28. AI-Driven Development Life Cycle: Reimagining Software ..., 11월 11, 2025에 액세스, [https://aws.amazon.com/blogs/devops/ai-driven-development-life-cycle/](https://aws.amazon.com/blogs/devops/ai-driven-development-life-cycle/)
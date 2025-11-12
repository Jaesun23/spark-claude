# NH투자증권

### Open API란?

![QV Open API](https://www.nhsec.com/mug/img/guestGuide/openAPI.gif)

**![직접 만드는 트레이딩 시스템](https://www.nhsec.com/mug/img/guestGuide/tit_openAPI_0430.gif)**

고객님께서 직접 프로그램하신 투자전략 시스템을 당사가 제공하는 연결모듈을 통해 트레이딩시스템에 연결하여, 시세/잔고/주문과 연동할 수 있도록 하는 서비스입니다.
특히 본인만의 시스템트레이딩과 투자분석프그램을 제작하고자 하시는 고객에 적당한 서비스입니다.

[OpenAPI 다운로드](https://download.nhqv.com/download/iflgtrading/openapi.qv.zip) [가입 신청](https://www.nhsec.com/WMDoc.action?viewPage=/guestGuide/trading/openAPI_join.jsp)

#### 가입대상

계좌를 개설하고 HTS ID를 등록하신 후, 본 서비스에 가입하시면 이용이 가능합니다.

#### 서비스의 특징

- C++ 프로그래밍 언어 지원
- 주식/선물/옵션/ELW 실시간 시세 제공
- 주식/선물/옵션/ELW 잔고 및 주문 연동

#### 서비스 이용 절차

**01 서비스 가입**

**02 모듈 다운로드 및 프로그램 제작**

**03 모의환경에서 테스트**

**04 실제환경 적용 트레이닝**

------

# 대신증권

#### CYBOS Plus

Plus API는
대신증권에서 제공하는 투자정보, 주문 플랫폼을 이용하여 나만의 프로그램을 만들어 볼 수 있는 Open API입니다.
특히 VB, C#, 엑셀, VC, 파이썬 등 다양한 언어를 지원하며, 주식/선물/옵션/야간선물/야간옵션 정보를
실시간으로 제공받을 수 있습니다.

나만의 새로운 투자 전략이 있으신가요?
Plus API를 이용하여 시스템 트레이딩에 도전해 보세요.

#### Plus 시스템 관계

![고객프로그램 고객제작프로그램 (VB, EXCEL, VC++, 파이썬) 매매전략, 자동주문, 신호감시 PLUS API 시세, 계좌, 주문 연동 API 제공 대신증권시스템 시세,계좌, 주문](https://money2.daishin.com/DW/images/customer/img03.png)

#### Plus 지원 상품군

![PLUS 주식:거래소 코스닥 ETF ETN 업종정보 시장정보:시장조치사항 등락현황 프로그램매매 예상체결분석 해외파생 국내파생:지수선물 지수옵션 주식옵션 야간거래:CME EUREX](https://money2.daishin.com/DW/images/customer/img01.png)

#### Plus 제공 정보

![PLUS정보제공 special 차트신호 종목검색 공통 종목코드 통신상태 주문초기화 주문 매수 매도 정정/취소 예약주문 시간외단일가 주문 시간외종가 주문 시세 현재가 시간대별 일자별 관심종목 ](https://money2.daishin.com/DW/images/customer/img02.png)

#### CYBOS Plus 개발환경

Windows 시스템 COM Object 라이브러리를 사용할 수 있는 개발 환경에서는 모두 가능합니다.

- Microsoft Visual Studio (VB, C#, C++, .Net 등)
- Microsoft Office ( Word, Excel, Powerpoint, Access 등 )
- Microsoft Internet Explorer Dynamic HTML, 파이썬
- Borland Delphi 등

#### 특징

- 차트 : HTS 통합차트에서 제공하는 보조지표 및 차트 신호 제공
  - 보조지표에서 신호선이 있는 경우 지표와 신호선의 교차여부에 대한 결과를 제공하며 실시간 데이터의 경우 마지막 봉만을 계산해주는 함수를 제공
- 종목검색 : HTS 종목검색(#8537) 기능 및 전략감시 실시간 처리 제공
  - 서버에 저장된 내 전략 리스트 조회 및 해당 전략에 맞는 종목들을 조회할 수 있으며 현재 종목검색 전략에 대한 종목들의 진입/퇴출 등 발생신호에 대한 정보를 최대 4개까지 실시간 수신
- 통합 샘플프로그램 : 시세, 주문, 체결, 잔고, 도움말등 통합관리 샘플 프로그램으로 기본적인 사용법을 익힐 수가 있음 (자료실 참조, 지속적으로 기능추가)

#### 적용 수수료율: CYBOS5(HTS)와 동일

------

# 삼성증권

공식지원 X

## 관련내용의 블로그 글

# 🚀 삼성증권 API 연동의 모든 것: 공식 API가 없어도 계좌 연동하는 완벽 가이드(2025-08 업데이트) 

|  [ 한국 주식 API 허브 ](https://iotnbigdata.tistory.com/661?utm_source=post-800&utm_medium=intext&utm_campaign=featured-2025w34&utm_content=hub-btn)  [ ECOS 통계/코드 ](https://iotnbigdata.tistory.com/803?utm_source=post-800&utm_medium=intext&utm_campaign=featured-2025w34&utm_content=ecos-btn)

**이 글은 ‘아키텍처/정책·체크리스트’ 중심 안내입니다.** 실제 주문/거래 코드는 다루지 않습니다. 합법적·동의 기반의 *데이터 조회* 경로와 ‘주문이 필요한 경우’의 대안(오픈API 제공 증권사)만 비교합니다.

- **조회가 목적**이면: 오픈뱅킹/집계형 API 등 **표준 동의 기반** 경로 권장
- **자동 주문**이 필요하면: **오픈API 제공 브로커** 활용(혼합 구성 가능)
- 보안·정책·레이트리밋은 **체크리스트**를 기준으로 운영

## 연동 경로 결정 트리

Q. 내 목표는 무엇인가?

① 보유/잔고/거래내역 등 **데이터 조회**만 필요 vs ② **자동 주문**까지 필요

A-1. 조회 중심이 목적

- **표준 동의 기반** 경로(오픈뱅킹/집계형 API) 선택 → OAuth 동의·토큰으로 계좌/거래내역 조회
- **장점**: 규정 준수·차단 리스크 낮음, 유지보수 용이
- **한계**: 일반적으로 **주문 미지원** (조회 데이터 품질/지연은 제공사 정책에 따름)

A-2. 자동 주문까지 필요

- **오픈API 제공 증권사** 계좌 개설 → 개발자 키 발급 → 주문/체결·실시간 데이터 사용
- 기존 계좌(예: 삼성)는 **조회용**으로만 연결(혼합 구성)하거나, 주문이 되는 브로커로 **분산**
- **권장**: 테스트베드/샌드박스에서 먼저 인증·쿼터·호출 흐름 검증

## 운영 체크리스트

① 모의 → 실전 전환

- 샌드박스/테스트베드로 **리다이렉트URL·스코프·IP 화이트리스트** 확인
- 일/분당 호출 예산 수립(예: 사용자별 1분 30회)
- 401/403/429/5xx **알림** 및 **장애 공지 구독** 설정

② 토큰/세션

- **Authorization Code + PKCE** 권장, Refresh Token **로테이션**
- 동의/철회 **감사 로그** 기록(누가, 언제, 어떤 스코프)
- **시계 동기화**(NTP, ±1~2초)로 타임스탬프 오류 방지

③ 레이트리밋/안정화

- **429**·**5xx** 시 지수 백오프(1s→2s→4s, 최대 30s), **즉시 재시도 금지**
- 잔고/보유·메타 정보는 **30~60초 캐시**(중복 호출 억제)
- 서킷 브레이커: 장애 시 **캐시/대체 응답** 반환

④ 보안/준법

- 비밀키·토큰은 **KMS/보안저장소**에 보관(클라이언트 노출 금지)
- 민감정보(PII) **로그 금지**·마스킹, 최소권한 스코프
- **비공개 엔드포인트/앱 자동화**는 약관·차단 리스크 → **표준 동의 기반**만 사용

## 자주 묻는 질문(FAQ)

<details style="border: 1px solid #e6eaf3; border-radius: 12px; padding: 12px; background: #fff; margin-bottom: 8px;" open="">
<summary style="font-weight: 800; cursor: pointer;">삼성증권 ‘개발자용 공개 트레이딩 API’가 있나요?</summary>
<div style="margin-top: 8px; color: #1f2630;">현재 공개 자료 기준으로는 <b>개발자용 주문 API 안내를 확인하기 어렵습니다</b>. 따라서 <b>데이터 조회</b>는 표준 동의 기반(오픈뱅킹/집계형 등), <b>자동 주문</b>은 오픈API 제공 증권사 활용을 권장합니다.</div>
</details>

<details style="border: 1px solid #e6eaf3; border-radius: 12px; padding: 12px; background: #fbfcff; margin-bottom: 8px;" open="">
<summary style="font-weight: 800; cursor: pointer;">삼성 계좌를 그대로 쓰면서 자동 주문을 하고 싶어요.</summary>
<div style="margin-top: 8px;">혼합 구성이 현실적입니다. <b>삼성 계좌=조회</b> 중심으로 연결하고, <b>주문/체결</b>은 오픈API 제공 브로커 계좌를 활용해 워크플로를 분리하세요.</div>
</details>

<details style="border: 1px solid #e6eaf3; border-radius: 12px; padding: 12px; background: #fff; margin-bottom: 8px;" open="">
<summary style="font-weight: 800; cursor: pointer;">쿼터(레이트리밋)과 장애 대응은 어떻게 하나요?</summary>
<div style="margin-top: 8px;">429·5xx에 <b>지수 백오프</b>, <b>서킷 브레이커</b>, 잔고·보유의 <b>단기 캐시</b>가 기본입니다. 사용자/일 호출 예산을 정하고 초과 시 캐시/지연 응답으로 전환하세요.</div>
</details>

<details style="border: 1px solid #e6eaf3; border-radius: 12px; padding: 12px; background: #fbfcff; margin-bottom: 8px;" open="">
<summary style="font-weight: 800; cursor: pointer;">보안상 주의할 점은?</summary>
<div style="margin-top: 8px;"><b>서버-서버</b>에서만 토큰을 다루고, 비밀은 <b>KMS 등 보안 저장소</b>에 보관합니다. PII 로그 금지, 최소 스코프 원칙, 동의/철회 <b>감사 로그</b>를 유지하세요.</div>
</details>

<details style="border: 1px solid #e6eaf3; border-radius: 12px; padding: 12px; background: #fff;" open="">
<summary style="font-weight: 800; cursor: pointer;">정책/엔드포인트가 바뀌면?</summary>
<div style="margin-top: 8px;">본 글은 <b>원칙·운영 방법</b> 중심입니다. 실제 연동 시에는 사용 중인 플랫폼의 <b>최신 문서/약관 공지</b>를 항상 우선하세요. 변경 로그를 주기적으로 확인해 업데이트하면 됩니다.</div>
</details>

삼성증권과의 시스템 연동을 고려하고 계신가요? 이 글에서는 삼성증권 계좌 연동을 위한 실질적인 방법과 코드 예시를 제공합니다.

## 🚨 먼저 알아야 할 현실

### 좋지 않은 소식

현재(2025년 8월 기준) **삼성증권은 개인 개발자용 공개 트레이딩 API를 제공하지 않습니다.** 공식 웹사이트는 주로 HTS/MTS(POP, mPOP) 안내와 다운로드 위주로 구성되어 있습니다.

### 좋은 소식

하지만 **계좌 조회와 이체** 목적이라면, 삼성증권 계좌도 금융결제원(KFTC)의 표준 **오픈뱅킹/어카운트인포 API**를 통해 연동할 수 있습니다!

## 📋 KFTC 오픈뱅킹으로 삼성증권 계좌 연동하기

### 사전 준비사항

1. **이용기관 등록**: KFTC 개발자센터에서 등록 필요
2. **사용자 동의**: 핀테크이용번호를 받기 위한 3-legged OAuth 인증
3. **보안 요구사항**: 실서비스 전환 시 보안 심사 통과

### 1. 거래내역 조회 구현

삼성증권의 CMA나 예탁금 계좌의 거래내역을 조회하는 코드입니다.

```
import requests
from datetime import datetime

BASE = "https://openapi.openbanking.or.kr/v2.0"
ACCESS_TOKEN = "사용자동의로_획득한_access_token"   # Bearer 토큰
FINTECH_USE_NUM = "사용자_핀테크이용번호"          # 계좌 등록시 받은 값

def get_transaction_list():
    params = {
        "bank_tran_id": "F123456789U4BC34239Z",  # 기관별 고유 규칙
        "fintech_use_num": FINTECH_USE_NUM,
        "inquiry_type": "A",     # A: 전체, I: 입금, O: 출금
        "inquiry_base": "D",     # D: 일자 기준
        "from_date": "20250101",
        "from_time": "000000",
        "to_date": datetime.now().strftime("%Y%m%d"),
        "to_time": datetime.now().strftime("%H%M%S"),
        "sort_order": "D",
        "tran_dtime": datetime.now().strftime("%Y%m%d%H%M%S"),
    }

    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.get(
        f"{BASE}/account/transaction_list/fin_num", 
        params=params, 
        headers=headers, 
        timeout=10
    )
    response.raise_for_status()
    data = response.json()

    # 조회 결과 파싱
    transactions = []
    for item in data.get("res_list", []):
        transaction = {
            "date": item["tran_date"],
            "type": item["inout_type"],
            "amount": item["tran_amt"],
            "balance": item.get("after_balance_amt")
        }
        transactions.append(transaction)
        print(f"{transaction['date']} | {transaction['type']} | {transaction['amount']}원")
    
    return transactions
```

### 2. 입금이체 구현

삼성증권 계좌로 입금이체를 실행하는 코드입니다.

```
import requests
import uuid
from datetime import datetime

def deposit_transfer(amount, recipient_name):
    ACCESS_TOKEN = "기관_or_사용자토큰"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}", 
        "Content-Type": "application/json"
    }

    payload = {
        "cntr_account_type": "N",
        "cntr_account_num": "12345678901234",     # 귀사 모계좌
        "wd_pass_phrase": "NONE",
        "wd_print_content": "삼성증권예탁금입금",
        "name_check_option": "on",
        "tran_dtime": datetime.now().strftime("%Y%m%d%H%M%S"),
        "req_cnt": "1",
        "req_list": [{
            "tran_no": "1",
            "bank_tran_id": f"F000000000U{uuid.uuid4().hex[:13].upper()}",
            "fintech_use_num": FINTECH_USE_NUM,
            "print_content": "입금테스트",
            "tran_amt": str(amount),
            "req_client_name": recipient_name,
            "req_client_num": f"{recipient_name.upper()}01",
            "transfer_purpose": "TR",
        }]
    }

    response = requests.post(
        "https://openapi.openbanking.or.kr/v2.0/transfer/deposit/fin_num",
        json=payload, 
        headers=headers, 
        timeout=10
    )
    response.raise_for_status()
    
    result = response.json()
    print("입금이체 결과:", result)
    return result
```

### 3. 어카운트인포로 통합 계좌 조회

모든 금융기관의 계좌를 한 번에 조회할 수 있습니다.

```
def get_all_accounts():
    """사용자의 모든 금융기관 계좌 통합 조회"""
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    
    response = requests.get(
        "https://openapi.openbanking.or.kr/v2.0/account/list",
        headers=headers,
        timeout=10
    )
    response.raise_for_status()
    
    data = response.json()
    accounts = []
    
    for account in data.get("res_list", []):
        account_info = {
            "bank_name": account.get("bank_name"),
            "account_num": account.get("account_num_masked"),
            "balance": account.get("balance_amt"),
            "account_type": account.get("account_type")
        }
        accounts.append(account_info)
        print(f"{account_info['bank_name']} - {account_info['account_num']} - {account_info['balance']}원")
    
    return accounts
```

## 🔄 완전한 연동 플로우

다음은 사용자 인증부터 거래까지의 전체 플로우입니다:

```
class SamsungSecuritiesConnector:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.fintech_use_num = None
    
    def authenticate_user(self, auth_code):
        """사용자 인증 및 토큰 획득"""
        token_url = "https://openapi.openbanking.or.kr/oauth/2.0/token"
        
        data = {
            "code": auth_code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": "YOUR_REDIRECT_URI",
            "grant_type": "authorization_code"
        }
        
        response = requests.post(token_url, data=data)
        token_data = response.json()
        
        self.access_token = token_data["access_token"]
        return token_data
    
    def register_account(self, account_num, bank_code):
        """계좌 등록 및 핀테크이용번호 발급"""
        # 계좌 등록 로직 구현
        pass
    
    def get_balance(self):
        """계좌 잔액 조회"""
        # 위에서 구현한 거래내역 조회 함수 활용
        pass
    
    def transfer_money(self, amount, recipient):
        """이체 실행"""
        # 위에서 구현한 입금이체 함수 활용
        pass
```

## ⚠️ 주의사항 및 제한사항

### 1. API 제한사항

- **주식 주문/체결 자동화는 지원되지 않음**: 오픈뱅킹 API는 계좌 조회와 이체만 가능
- **실시간 시세 정보 제공 안됨**: 별도의 시세 API가 필요

### 2. 보안 요구사항

- **토큰 관리**: Access token의 안전한 저장과 갱신
- **거래 고유번호**: bank_tran_id의 유니크 보장
- **시간 정확도**: tran_dtime의 정확한 포맷팅
- **레이트 리밋**: API 호출 횟수 제한 준수

### 3. 개발 시 체크리스트

- [ ] 이용기관 심사 및 보안요건 준비
- [ ] 샌드박스 환경에서 E2E 테스트 완료
- [ ] 에러 핸들링 및 로깅 구현
- [ ] 페이지네이션 처리 (거래내역이 많은 경우)

## 🔄 대안: 주식 자동매매가 목적이라면?

만약 실제 주식 거래 자동화가 목적이라면, 다음 증권사들이 공개 API를 제공합니다:

### 한국투자증권 (KIS)

```
# KIS API 예시
import requests

def kis_login():
    url = "https://openapi.koreainvestment.com:9443/oauth2/tokenP"
    data = {
        "grant_type": "client_credentials",
        "appkey": "YOUR_APP_KEY",
        "appsecret": "YOUR_APP_SECRET"
    }
    response = requests.post(url, json=data)
    return response.json()["access_token"]

def buy_stock(stock_code, quantity, price):
    # 주식 매수 주문 로직
    pass
```

### 키움증권, LS증권, 대신증권

각각 OpenAPI+, XING, CYBOS 등의 API를 제공합니다.

## 💡 하이브리드 전략

실무에서는 다음과 같은 하이브리드 전략을 추천합니다:

1. **거래 실행**: 한국투자증권 등의 공개 API 활용
2. **자금 관리**: 삼성증권 계좌는 KFTC 오픈뱅킹으로 연동
3. **통합 관리**: 모든 계좌를 어카운트인포로 통합 조회

## 🎯 마무리

삼성증권 직접 API는 제한적이지만, KFTC 표준 API를 통해 계좌 조회와 이체는 충분히 구현 가능합니다. 주식 거래 자동화까지 필요하다면 다른 증권사 API와 조합하여 사용하는 것이 현실적인 해결책입니다.

개발 전 반드시 샌드박스 환경에서 충분한 테스트를 진행하고, 보안 요구사항을 철저히 준수하시기 바랍니다. 

**참고 링크**

- [금융결제원 개발자센터](https://developers.kftc.or.kr/)
- [한국투자증권 API 포털](https://apiportal.koreainvestment.com/)
- [삼성증권 공식사이트](https://www.samsungpop.com/)

### 관련 허브 & 실전 가이드

- [ 한국 주식 API 생태계 완전 가이드(허브)](https://iotnbigdata.tistory.com/661?utm_source=post-800&utm_medium=intext&utm_campaign=hub)
- [ 한국은행 ECOS API: 서비스·통계 목록(입문 3쿼리 포함)](https://iotnbigdata.tistory.com/803?utm_source=post-800&utm_medium=intext&utm_campaign=ecos)
- [ API 테스트 자동화(레이트리밋/리트라이 패턴 정리)](https://iotnbigdata.tistory.com/660?utm_source=post-800&utm_medium=intext&utm_campaign=apitest)
- [ 무료 이미지 애니메이션 툴 5선(썸네일/CTR 최적화)](https://iotnbigdata.tistory.com/651?utm_source=post-800&utm_medium=intext&utm_campaign=thumb)
- [ 한국의 API 서비스 목록(카탈로그)](https://iotnbigdata.tistory.com/434?utm_source=post-800&utm_medium=intext&utm_campaign=catalog)

출처: https://iotnbigdata.tistory.com/800 [TechOracle - 코드와 AI로 분석하고 예측하는 시장과 세상:티스토리]
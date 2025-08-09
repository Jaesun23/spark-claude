---
description: Sub-agent 테스트 - 순차 실행 확인
---

# Sub-agent 순차 실행 테스트

## 🚨 중요: Task 도구를 5번 호출하여 각 서브에이전트를 테스트합니다

당신은 아래의 5개 서브에이전트를 순차적으로 호출하여 모두 정상 작동하는지 확인해야 합니다.

## 실행할 작업

### 1. Implementer 테스트
**Task 도구를 사용하여 실행:**
- description: "Test Implementer Agent"
- prompt: "This is a test. Just respond with 'Hello from Implementer! I am ready to implement V5 code.'"

### 2. Tester 테스트
**Task 도구를 사용하여 실행:**
- description: "Test Tester Agent"
- prompt: "This is a test. Just respond with 'Hello from Tester! I am ready to write comprehensive tests.'"

### 3. Quality 테스트
**Task 도구를 사용하여 실행:**
- description: "Test Quality Agent"
- prompt: "This is a test. Just respond with 'Hello from Quality! I am ready to run quality checks.'"

### 4. Reviewer 테스트
**Task 도구를 사용하여 실행:**
- description: "Test Reviewer Agent"
- prompt: "This is a test. Just respond with 'Hello from Reviewer! I am ready to review architecture.'"

### 5. Reporter 테스트
**Task 도구를 사용하여 실행:**
- description: "Test Reporter Agent"
- prompt: "This is a test. Just respond with 'Hello from Reporter! I am ready to generate reports.'"

## 테스트 완료 후

모든 서브에이전트가 응답하면 다음과 같이 요약하세요:
"✅ 모든 서브에이전트 테스트 완료! 5개 에이전트 모두 정상 작동합니다."

만약 특정 에이전트가 응답하지 않으면 어떤 에이전트인지 보고하세요.

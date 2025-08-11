# SPARK 설치 가이드

## 📋 목차

1. [빠른 시작](#빠른-시작)
2. [설치 옵션](#설치-옵션)
3. [구성요소 선택](#구성요소-선택)
4. [설치 후 설정](#설치-후-설정)
5. [문제 해결](#문제-해결)
6. [제거 방법](#제거-방법)

---

## 🚀 빠른 시작

### 기본 설치 (전역)

```bash
# 1. SPARK 저장소 클론
git clone https://github.com/Jaesun23/spark-claude.git
cd spark-claude

# 2. 설치 스크립트 실행
./scripts/install.sh

# 3. Claude Code 재시작
```

이렇게 하면 모든 프로젝트에서 SPARK를 사용할 수 있습니다.

---

## 🎯 설치 옵션

### 1. 전역 설치 (~/.claude/)

**장점:**
- 모든 프로젝트에서 SPARK 사용 가능
- 한 번 설치로 계속 사용
- 중앙 집중식 업데이트

**단점:**
- 프로젝트별 커스터마이징 어려움
- 다른 전역 에이전트와 충돌 가능성

**선택 시나리오:**
```
=== 설치 위치 선택 ===
1) 전역 설치 (~/.claude/)  ← 이것 선택
```

### 2. 프로젝트별 설치

**장점:**
- 프로젝트별 독립적 설정
- 버전 관리 가능
- 팀 공유 용이

**단점:**
- 각 프로젝트마다 설치 필요
- 디스크 공간 중복 사용

**선택 시나리오:**
```
=== 설치 위치 선택 ===
2) 프로젝트별 설치 (프로젝트/.claude/)  ← 이것 선택
프로젝트 디렉토리 경로 입력: /Users/jason/my-project
```

### 3. 현재 프로젝트 덮어쓰기

SPARK 개발 디렉토리 자체에 설치 (개발자용)

---

## 🔧 구성요소 선택

### 설치 가능한 구성요소

#### 1. SPARK 에이전트 (16개)
- 16개 전문 에이전트 파일
- Task 도구로 호출 가능
- 필수 구성요소

#### 2. 단일 에이전트 명령어
- `/spark-implement`, `/spark-test` 등
- 각 에이전트를 직접 호출하는 단축 명령어
- 네임스페이스 지원 (충돌 방지)

#### 3. 다중 에이전트 파이프라인
- `/spark-launch` - 5개 에이전트 연속 실행
- `/spark-optimize` - 성능 최적화 파이프라인
- **훅과 워크플로우 자동 포함**

#### 4. 훅 스크립트
- 페르소나 라우터
- 품질 게이트
- 다중 에이전트 파이프라인에 필수

#### 5. 워크플로우 설정
- 작업 상태 관리
- 에이전트 간 컨텍스트 공유

### 선택 예시

```
=== 설치 구성요소 선택 ===

1) SPARK 에이전트 (16개) 설치? (Y/n): y
✓ 에이전트 설치 예정

2) 단일 에이전트 명령어 설치? (Y/n): y
✓ 명령어 설치 예정

3) 다중 에이전트 파이프라인 설치? (훅 필요) (Y/n): y
✓ 다중 에이전트 파이프라인 설치 예정
✓ 훅 및 워크플로우 자동 포함
```

---

## ⚙️ 설치 후 설정

### 1. Claude Code 재시작

설치 후 반드시 Claude Code를 재시작해야 새 설정이 로드됩니다.

### 2. 설치 확인

```bash
# 에이전트 확인
ls ~/.claude/agents/

# 명령어 확인
ls ~/.claude/commands/

# 설정 확인
cat ~/.claude/settings.json
```

### 3. 첫 사용

```bash
# 단일 에이전트 호출
/spark-implement "create user authentication"

# 다중 에이전트 파이프라인
/spark-launch "new dashboard feature"
```

---

## 🔍 문제 해결

### 1. 명령어 충돌

**문제:** "Command already exists" 오류

**해결방법:**
```bash
# 재설치 시 네임스페이스 사용
./scripts/install.sh
# 전역 설치 선택 후
네임스페이스 사용? (예: /spark:implement) (Y/n): y
네임스페이스 접두어 입력 (기본: spark): myproject
```

이제 `/myproject:implement` 형태로 사용

### 2. JSON 파일을 못 찾는 문제

**문제:** 에이전트가 `current_task.json`을 못 찾음

**해결방법:** 
v3.0에서는 자동으로 fallback 경로를 체크합니다:
1. 먼저 `~/.claude/workflows/` 확인
2. 없으면 `.claude/workflows/` 확인

수동으로 초기화가 필요한 경우:
```bash
mkdir -p ~/.claude/workflows
echo '{}' > ~/.claude/workflows/current_task.json
echo '{}' > ~/.claude/workflows/unified_context.json
```

### 3. 훅이 실행되지 않음

**문제:** 다중 에이전트 파이프라인이 작동하지 않음

**확인사항:**
```bash
# settings.json에 훅 설정 확인
cat ~/.claude/settings.json | grep hooks

# 훅 파일 실행 권한 확인
ls -la ~/.claude/hooks/*.py

# 실행 권한 부여
chmod +x ~/.claude/hooks/*.py
```

### 4. 심볼릭 링크 문제

**문제:** `~/.claude`가 심볼릭 링크인 경우

**해결방법:**
설치 스크립트가 자동으로 감지하고 처리합니다.
수동 확인:
```bash
# 심볼릭 링크 확인
ls -la ~/.claude

# 실제 경로 확인
readlink ~/.claude
```

---

## 🗑️ 제거 방법

### 전역 설치 제거

```bash
# 백업 (선택사항)
cp -r ~/.claude ~/.claude.backup

# SPARK 구성요소만 제거
rm -rf ~/.claude/agents/*-spark.md
rm -rf ~/.claude/commands/spark-*.json
rm -rf ~/.claude/hooks/spark_*.py

# 또는 전체 제거
rm -rf ~/.claude
```

### 프로젝트별 설치 제거

```bash
cd /your/project
rm -rf .claude
```

---

## 📊 설치 방식 비교표

| 항목 | 전역 설치 | 프로젝트별 설치 |
|------|-----------|-----------------|
| 설치 위치 | ~/.claude/ | project/.claude/ |
| 사용 범위 | 모든 프로젝트 | 특정 프로젝트만 |
| 훅 경로 | $HOME/.claude/hooks/ | $CLAUDE_PROJECT_DIR/.claude/hooks/ |
| 워크플로우 | ~/.claude/workflows/ | project/.claude/workflows/ |
| 업데이트 | 한 번만 | 각 프로젝트마다 |
| 팀 공유 | 어려움 | Git으로 공유 가능 |
| 충돌 가능성 | 있음 (네임스페이스로 해결) | 없음 |

---

## 🎯 권장 설치 구성

### 개인 개발자
- **전역 설치** + **모든 구성요소**
- 모든 프로젝트에서 즉시 사용 가능

### 팀 프로젝트
- **프로젝트별 설치** + **선택적 구성요소**
- Git으로 팀원과 공유
- 프로젝트별 커스터마이징

### SPARK 테스트/개발
- **현재 프로젝트 덮어쓰기**
- 개발 및 테스트용

---

## 📚 추가 문서

- [SPARK 완전 가이드](./SPARK_COMPLETE_GUIDE.md)
- [에이전트 백과사전](./SPARK_AGENTS_ENCYCLOPEDIA.md)
- [앤트로픽 가이드라인](./ANTHROPIC_GUIDELINES.md)
- [오케스트레이션 원칙](./SPARK_ORCHESTRATION_PRINCIPLES.md)

---

## 💬 지원

문제가 있거나 질문이 있으시면:
- GitHub Issues: [https://github.com/Jaesun23/spark-claude/issues](https://github.com/Jaesun23/spark-claude/issues)
- 문서: [SPARK_COMPLETE_GUIDE.md](./SPARK_COMPLETE_GUIDE.md)

---

*SPARK v3.0 - Jason과 AI의 협업으로 만들어진 최적화된 다중 에이전트 시스템*
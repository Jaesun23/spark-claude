# 🧠 SPARK Agents Memory Reference (2호 전용)

> **2호 메모리 저장용 핵심 정보만 포함**
> *복잡한 설명 제거, 즉시 활용 가능한 레퍼런스*

---

## 🎯 16개 SPARK 에이전트 빠른 선택 가이드

### 🔥 핵심 4대 에이전트 (최우선 사용)
1. **implementer-spark** → 구현 (모든 페르소나 자동 활성화)
2. **analyzer-spark** → 분석/디버깅 (다차원 분석)
3. **tester-spark** → 테스트 (95% 커버리지)
4. **designer-spark** → 설계 (아키텍처/UI/UX)

### 📊 상황별 에이전트 매칭

| 상황 | 에이전트 | 명령어 예시 |
|------|----------|-------------|
| "버그 고쳐줘" | troubleshooter-spark | `/spark-troubleshoot "fix login error"` |
| "성능 개선" | analyzer-spark → improver-spark | `/spark-analyze "find bottlenecks"` |
| "테스트 작성" | tester-spark | `/spark-test "create unit tests"` |
| "문서 작성" | documenter-spark | `/spark-document "API docs"` |
| "코드 정리" | cleaner-spark | `/spark-clean "remove dead code"` |
| "설명해줘" | explainer-spark | `/spark-explain "how auth works"` |
| "예상 시간" | estimator-spark | `/spark-estimate "new feature"` |
| "Git 작업" | gitter-spark | `/spark-git "commit changes"` |
| "빌드/배포" | builder-spark | `/spark-build "deploy to prod"` |
| "멀티 작업" | spawner-spark | `/spark-spawn "parallel tasks"` |
| "명령 찾기" | indexer-spark | `/spark-index "list commands"` |
| "작업 관리" | tasker-spark | `/spark-task "manage todos"` |
| "프로젝트 로드" | loader-spark | `/spark-load "project context"` |

---

## ⚡ Task 동시 호출 패턴 (핵심!)

```javascript
// ✅ 올바른 패턴 - 진짜 병렬 실행
Task Task Task Task → 시작!

// ❌ 잘못된 패턴 - 순차 실행
Task 1 완료 → Task 2 시작 → Task 3 시작
```

---

## 🎭 페르소나 자동 활성화 키워드

| 페르소나 | 트리거 키워드 |
|----------|--------------|
| **Backend** | API, endpoint, service, database, server |
| **Frontend** | component, UI, responsive, style, React |
| **Security** | auth, security, vulnerability, OWASP |
| **Architecture** | complexity > 0.7, design, scalable |
| **DevOps** | deploy, CI/CD, pipeline, Docker |
| **Data** | data, analytics, database, ETL |
| **Testing** | test, coverage, TDD, unit |
| **Documentation** | document, readme, API docs |

---

## 🔧 에이전트별 필수 정보

### implementer-spark (구현)
```json
{
  "task": "구현할 내용",
  "complexity": 0.1-1.0,  // 0.7+ = 아키텍처 모드
  "context": "기존 코드 패턴"
}
```

### analyzer-spark (분석)
```json
{
  "target": "file/directory/system",
  "focus": ["performance", "security", "quality"],
  "depth": "quick|standard|deep"
}
```

### tester-spark (테스트)
```json
{
  "coverage_target": {"unit": 95, "integration": 85},
  "framework": "jest|pytest|mocha",
  "focus": ["edge_cases", "happy_path", "security"]
}
```

### designer-spark (설계)
```json
{
  "type": "architecture|api|ui",
  "requirements": ["기능", "성능", "보안"],
  "constraints": ["기술", "비즈니스", "규제"]
}
```

---

## 📊 품질 게이트 (Jason's 8-Step)

1. **구문 검증** → 0 errors
2. **타입 체크** → mypy --strict (0 errors)
3. **린팅** → ruff --strict (0 violations)
4. **보안 분석** → OWASP + secrets scan
5. **테스트 커버리지** → Unit 95%, Integration 85%
6. **성능 체크** → O(n) complexity, no N+1
7. **문서 검증** → Docstrings required
8. **통합 테스트** → E2E scenarios pass

---

## 🚀 다중 에이전트 파이프라인

| 파이프라인 | 에이전트 순서 | 용도 |
|------------|--------------|------|
| **/spark-launch** | analyze → design → implement → test → document | 전체 기능 개발 |
| **/spark-refactor** | analyze → clean → improve → test | 코드 개선 |
| **/spark-audit** | analyze → troubleshoot → tester → documenter | 보안/성능 감사 |
| **/spark-migrate** | analyze → design → implement → test → deploy | 시스템 마이그레이션 |
| **/spark-optimize** | analyze → improve → test → build → deploy | 성능 최적화 |

---

## 🔴 중요 제약사항

1. **에이전트는 다른 에이전트 호출 불가** (오직 2호만 Task 사용)
2. **병렬 실행 시 모든 에이전트 완료 대기** (동기화 필수)
3. **JSON 컨텍스트로만 정보 전달** (직접 대화 불가)
4. **SubagentStop 후 품질 게이트 자동 실행**
5. **최대 재시도 3회** (품질 실패 시)

---

## 📁 상태 파일 위치

```
~/.claude/workflows/current_task.json      # 전역 설치
.claude/workflows/current_task.json        # 프로젝트별
```

**Fallback 패턴**: 먼저 `~/.claude` 체크 → 없으면 `.claude` 체크

---

## 🎯 에이전트 선택 플로우

```
1. 작업 복잡도 판단
   → 0.7+ : Designer 먼저
   → 0.3-0.7 : Implementer 직접
   → 0.3- : 단순 작업

2. 작업 유형 판단
   → 버그: Troubleshooter
   → 새 기능: Designer → Implementer
   → 개선: Analyzer → Improver
   → 정리: Cleaner

3. 병렬 가능 판단
   → 독립적: Task Task Task → 시작!
   → 의존적: 순차 실행
```

---

## 💡 Pro Tips

- **토큰 절약**: 필요한 에이전트만 호출 (평균 88.4% 절감)
- **품질 우선**: 8단계 게이트 모두 통과 필수
- **병렬 최대화**: 독립 작업은 동시 실행
- **컨텍스트 유지**: JSON 파일로 상태 관리
- **재시도 활용**: 실패 시 자동 3회 재시도

---

*이 문서는 2호의 메모리 저장용으로 최적화되었습니다.*
*상세 정보는 `/docs/SPARK_AGENTS_GUIDE.md` 참조*
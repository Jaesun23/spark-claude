# 🧬 DNA 시스템 11개 - 완전 가이드

> **DNA 시스템 = 모든 소프트웨어의 기본 설계도**
>
> 생명의 DNA가 모든 생물의 기초이듯, 11개 DNA 시스템은 모든 소프트웨어 프로젝트의 기초입니다.

------

## DNA 시스템이란?

**정의**: 전체 시스템에 걸쳐 **"통일"**되어야 하는 횡단 관심사(Cross-Cutting Concerns)

- 언어, 프레임워크, 도메인에 관계없이 모든 프로젝트가 처음부터 끝까지 유지해야 하는 11가지 필수 시스템.

**특징**:

- 언어 무관 (개념/원칙 중심)
- 모두 필수 (선택 없음)
- 자동 강제 (지키지 않으면 빌드/실행 실패)
- 일관성 필수 (한 곳만 다르면 전체 혼란)

**왜 필요한가?**:

```
문서로 알려주기 → AI가 안 읽음/잊어버림
체크리스트 작성 → AI가 안 지킴
지시/설명 반복 → 매 세션마다 반복

✅ 해결: "환경"을 만들어서 잘못할 수 없게!
```

------

## 1. Type System (타입 시스템)

**목적**: 런타임 에러 방지, 타입 안전성 보장

**범위**:

- 모든 변수, 함수, 클래스의 타입 명시
- 타입 체커 통과 필수 (컴파일/빌드 단계)
- any/dynamic/var 금지 또는 엄격 제한
- 타입 불일치 = 실행 불가

**예시**:

- 간단: 함수 인자/리턴 타입 명시
- 중간: 제네릭, Union 타입, 도메인 모델
- 복잡: 타입 안전한 빌더 패턴, 의존성 주입

**언어별 구현**:

- Python: `mypy --strict`, Pydantic v2
- Rust: 기본 타입 시스템 (엄격함)
- TypeScript: `strict: true`, `noImplicitAny`
- Go: 기본 타입 시스템

**왜 필수인가?**: 타입 없으면 "이 변수가 문자열인지 숫자인지" 런타임에 폭탄. 리팩토링 시 어디가 깨졌는지 알 수 없음.

------

## 2. Observability System (관찰 가능성)

**목적**: 시스템 상태 관찰, 디버깅, 성능 모니터링

**범위**:

- **Logging** (구조화된 로깅)
  - JSON/구조화 형식
  - trace_id로 요청 추적
  - print/console.log 금지
  - 중앙 집중 설정
- **Metrics** (메트릭)
  - 성능 지표 수집 (응답 시간, 처리량)
  - 카운터, 게이지, 히스토그램
- **Tracing** (분산 추적)
  - 마이크로서비스 간 호출 추적
  - 요청 전체 흐름 시각화

**예시**:

- 간단:
  - 함수 진입/종료 로그
  - 에러 발생 로그
- 중간:
  - 구조화된 로깅 (structlog, winston)
  - trace_id 자동 전파
  - 기본 메트릭 수집
- 복잡:
  - OpenTelemetry 통합
  - 분산 추적 (Jaeger, Zipkin)
  - 실시간 대시보드 (Grafana)

**언어별 구현**:

- Python: structlog, OpenTelemetry
- Rust: tracing, tracing-subscriber
- TypeScript: winston, pino, OpenTelemetry
- Go: zap, zerolog, OpenTelemetry

**왜 필수인가?**: print() 남발하면 "무슨 에러인지" "어디서 느린지" 파악 불가능. 구조화된 로깅 없으면 디버깅 지옥.

------

## 3. Testing System (테스팅 시스템)

**목적**: 품질 보증, 회귀 방지, 안전한 리팩토링

**범위**:

- 테스트 우선 (TDD - Test-Driven Development)
- 95%+ 코드 커버리지 강제
- 단위 테스트 (Unit Tests)
- 통합 테스트 (Integration Tests)
- 속성 기반 테스트 (Property-Based Tests)
- 테스트 없이 커밋 불가

**예시**:

- 간단:
  - 함수 단위 테스트
  - 예상 입력/출력 검증
- 중간:
  - Given-When-Then 패턴
  - Mock/Stub 최소화
  - 통합 테스트
- 복잡:
  - Property-based testing (가설 검증)
  - Fuzz testing (무작위 입력)
  - Mutation testing (테스트의 테스트)

**언어별 구현**:

- Python: pytest, hypothesis, pytest-cov
- Rust: cargo test, proptest
- TypeScript: jest, vitest, fast-check
- Go: testing, rapid

**왜 필수인가?**: 테스트 없으면 "고쳤는지 망쳤는지" 알 수 없음. 리팩토링할 때마다 전체 수동 테스트 = 불가능.

------

## 4. Code Quality System (코드 품질)

**목적**: 일관된 스타일, 유지보수성, 자동화된 품질 보증

**범위**:

- **자동 포맷팅** (포맷터 강제 실행)
  - 들여쓰기, 줄바꿈, 공백 통일
- **린팅** (스타일 가이드 강제)
  - 경고 0개 달성
  - 나쁜 패턴 감지
- **TODO/FIXME/pass 금지**
  - 미완성 코드 커밋 차단
- **Pre-commit Hooks**
  - 커밋 전 자동 검사
  - 포맷/린트/타입 체크
- **CI 파이프라인**
  - 빌드 자동 검증
  - 테스트 자동 실행

**예시**:

- 간단:
  - 포맷터 실행 (black, prettier)
  - 기본 린트 (pylint, eslint)
- 중간:
  - pre-commit hooks
  - 복잡도 체크 (cyclomatic complexity)
  - import 정렬
- 복잡:
  - 중복 코드 감지 (jscpd)
  - 보안 린트 (bandit, semgrep)
  - CI/CD 파이프라인 통합

**언어별 구현**:

- Python: ruff, black, mypy, pre-commit
- Rust: cargo fmt, clippy
- TypeScript: prettier, eslint
- Go: gofmt, golangci-lint

**왜 필수인가?**: 스타일 제각각이면 코드 리뷰 시간 낭비. 나쁜 패턴 방치하면 기술 부채 폭발. TODO 남발하면 언제까지나 미완성.

------

## 5. Architecture Enforcement (아키텍처 강제)

**목적**: 아키텍처 경계 유지, 의존성 방향 제어

**범위**:

- **Layer 경계 검증**
  - Domain → Infrastructure 금지
  - Presentation → Domain만 허용
- **순환 의존성 금지**
  - 모듈 A → B → A 차단
- **Import 규칙 강제**
  - 허용된 import만 가능
  - 외부 라이브러리 제한
- **Architecture Tests**
  - 경계 위반 = 테스트 실패

**예시**:

- 간단:
  - 모듈 간 의존성 방향 정의
  - 순환 의존 체크
- 중간:
  - Layer 경계 강제 (Clean Architecture)
  - import-linter 규칙
- 복잡:
  - Architecture decision tests
  - 의존성 그래프 시각화
  - 자동 리팩토링 제안

**언어별 구현**:

- Python: import-linter, pytest (architecture tests)
- Rust: 모듈 시스템 + Architecture tests
- TypeScript: dependency-cruiser, madge
- Go: go-cleanarch, depguard

**왜 필수인가?**: 경계 없으면 스파게티 코드. Domain에서 DB 직접 접근하면 테스트 불가능. 순환 의존하면 리팩토링 지옥.

------

## 6. Configuration System (설정 관리)

**목적**: 환경별 설정 분리, 타입 안전, 민감 정보 보호

**범위**:

- **환경 변수 관리**
  - .env 파일 (dev, staging, prod)
  - 환경별 자동 로딩
- **타입 안전한 설정**
  - 설정 값 타입 검증
  - IDE 자동완성
- **하드코딩 금지**
  - 코드에 URL, 비밀번호 직접 작성 금지
- **의존성 관리** ⭐
  - 패키지 버전 통일
  - lock 파일로 고정
  - 라이센스 체크
  - 보안 취약점 스캔

**예시**:

- 간단:
  - .env 파일 + 환경 변수
  - requirements.txt, package.json
- 중간:
  - 타입 안전한 설정 클래스
  - pyproject.toml (uv), Cargo.toml
  - 의존성 lock 파일
- 복잡:
  - 환경별 설정 상속
  - Feature flags (런타임 토글)
  - 설정 검증 + 기본값
  - 의존성 자동 업데이트

**의존성 관리 도구**:

- Python: **uv** (pyproject.toml 하나로 통일) ⭐
- Rust: Cargo (Cargo.toml + Cargo.lock)
- TypeScript: pnpm (package.json + pnpm-lock.yaml)
- Go: go mod (go.mod + go.sum)

**왜 필수인가?**: 하드코딩하면 환경 바꿀 때마다 코드 수정. 타입 없으면 "PORT가 문자열인지 숫자인지" 런타임에 폭탄. 의존성 버전 안 맞으면 "내 컴퓨터에서는 되는데요?" 지옥.

------

## 7. Error Handling System (에러 처리)

**목적**: 에러 파악 및 복구, 디버깅 가능성

**범위**:

- **구조화된 에러**
  - 에러 타입 정의
  - 에러 컨텍스트 포함 (어디서, 왜, 무엇을)
- **panic/throw 제한**
  - 예외 처리 강제
  - 복구 불가능한 경우만 panic
- **Result/Either 패턴**
  - 명시적 에러 반환
  - 에러 전파 규칙
- **에러 로깅 통합**
  - 모든 에러를 Observability에 기록

**예시**:

- 간단:
  - try-catch + 의미 있는 에러 메시지
  - 에러 타입 구분 (ValueError, TypeError)
- 중간:
  - 커스텀 예외 클래스
  - 에러 체인 (원인 추적)
  - Result<T, E> 패턴
- 복잡:
  - 에러 복구 전략 (재시도, 폴백)
  - Circuit Breaker 패턴
  - 에러 집계 및 알림

**언어별 구현**:

- Python: 커스텀 예외 + Result 패턴 (라이브러리)
- Rust: Result<T, E> 강제, panic! 금지
- TypeScript: neverthrow, Either 패턴
- Go: error 타입 (기본), pkg/errors

**왜 필수인가?**: "Error: Something went wrong" → 무슨 에러인지 모름. 에러 컨텍스트 없으면 디버깅 불가능. panic하면 전체 프로그램 죽음.

------

## 8. Performance System (성능 측정)

**목적**: 객관적 성능 평가, 최적화 검증

**범위**:

- **벤치마크** (전체 성능 측정)
  - 함수/모듈별 실행 시간
  - 처리량 (throughput) 측정
  - 리팩토링 전후 비교
- **프로파일링** (병목 분석) ⭐
  - 함수별 실행 시간 분포
  - 메모리 할당 추적
  - CPU 사용량 분석
  - 핫스팟(느린 부분) 찾기
- **성능 회귀 감지**
  - 벤치마크 자동 실행
  - 이전 버전 대비 느려지면 실패

**예시**:

- 간단:
  - 함수 실행 시간 측정 (time.time())
  - 수동 비교
- 중간:
  - pytest-benchmark, Criterion
  - 통계적 벤치마크 (평균, p95, p99)
  - 프로파일링 스냅샷
- 복잡:
  - Instruments (macOS), perf (Linux)
  - 지속적 프로파일링 (production)
  - 성능 대시보드
  - 자동 회귀 감지

**프로파일링 도구**:

- Python: py-spy, cProfile, memory_profiler
- Rust: Instruments (macOS), perf, flamegraph
- TypeScript: clinic.js, 0x, Chrome DevTools
- Go: pprof (기본 내장)

**왜 필수인가?**: 리팩토링 후 "느려진 건지 빨라진 건지" 객관적 증거 없으면 논쟁. 병목 지점 모르면 "감으로" 최적화 = 시간 낭비.

------

## 9. API System (인터페이스/통신)

**목적**: 모듈/서비스 간 통신 규약 통일

**범위**: ⚠️ "API"를 좁게 생각하지 마세요!

- ✅ **외부 REST API** (서버)
- ✅ **내부 마이크로서비스 통신** (gRPC, 메시지 큐)
- ✅ **모듈 간 함수 호출 규약** (인터페이스)
- ✅ **라이브러리 public API** (pub fn, export)
- ✅ **CLI 명령어 인터페이스** (argparse, clap)

**모든 인터페이스/통신을 포함합니다!**

**예시**:

- 간단:
  - 함수 시그니처 정의
  - CLI 명령어 인터페이스
  - 모듈 간 호출 규약
- 중간:
  - 라이브러리 public API
  - 타입 안전한 인터페이스
  - API 문서 자동 생성
- 복잡:
  - REST API (FastAPI, Express)
  - GraphQL, gRPC
  - WebSocket 실시간 통신
  - OpenAPI 스펙 준수

**언어별 구현**:

- Python: FastAPI, pydantic (타입 검증), typer (CLI)
- Rust: axum, tonic (gRPC), clap (CLI)
- TypeScript: NestJS, tRPC, express
- Go: gin, gRPC, cobra (CLI)

**왜 필수인가?**: 인터페이스 통일 안 되면 "어떻게 호출하는지" 매번 확인. API 문서 없으면 "이 함수 뭐 하는 거지?" 코드 뒤져야 함. CLI 도구도 명령어 인터페이스 = API!

------

## 10. Data System (저장/조회)

**목적**: 데이터 영속성 및 접근 통일

**범위**: ⚠️ "대용량 데이터"만 생각하지 마세요!

- ✅ **일반 DB** (PostgreSQL, MySQL, SQLite)
- ✅ **파일 읽기/쓰기** (로컬, S3)
- ✅ **캐시** (Redis, 메모리)
- ✅ **대용량 처리** (ETL, Streaming, Batch)
- ✅ **메모리 관리** (Arena, 객체 풀링)

**모든 저장/조회를 포함합니다!**

**예시**:

- 간단:
  - 설정 파일 읽기/쓰기
  - 로컬 파일 저장
  - 히스토리 저장
- 중간:
  - PostgreSQL CRUD
  - Redis 캐싱
  - ORM (SQLAlchemy, TypeORM)
  - 연결 풀 관리
- 복잡:
  - ETL 파이프라인 (Airflow, dbt)
  - 실시간 스트리밍 (Kafka, Flink)
  - 데이터 웨어하우스 (Snowflake, BigQuery)
  - Arena 메모리 관리 (Kent Beck)

**언어별 구현**:

- Python: SQLAlchemy, Pydantic, polars (대용량)
- Rust: diesel, sqlx, Arena allocator
- TypeScript: Prisma, TypeORM, Drizzle
- Go: gorm, sqlx

**왜 필수인가?**: 저장 안 하는 프로그램? 거의 없음. (설정, 히스토리, 결과 등) DB 접근 통일 안 되면 "여기선 raw SQL, 저기선 ORM" 혼란. 메모리 관리도 Data System! (Kent Beck의 Arena)

------

## 11. Security System (보안)

**목적**: 보안 취약점 방지, 민감 정보 보호

**범위**:

- **민감 정보 관리**
  - API 키, 비밀번호 암호화 저장
  - 환경 변수 사용 (.env)
  - 코드에 하드코딩 금지
- **입력 검증** (Injection 방지)
  - SQL Injection 차단
  - XSS (Cross-Site Scripting) 방지
  - Command Injection 방지
  - Path Traversal 방지
- **인증/권한** (Authentication/Authorization)
  - 누가 접근하는가? (인증)
  - 무엇을 할 수 있는가? (권한)
  - JWT, OAuth2, RBAC
- **암호화**
  - 전송 중 (HTTPS, TLS)
  - 저장 중 (DB 암호화)
  - 비밀번호 해싱 (bcrypt, argon2)
- **보안 스캔**
  - SAST (정적 분석)
  - DAST (동적 분석)
  - 의존성 취약점 체크
- **보안 헤더**
  - CORS, CSP, HSTS 설정
- **Rate Limiting** (DDoS 방지)

**예시**:

- 간단:
  - .env에 비밀 저장 (코드 X)
  - 입력 검증 (SQL Injection 방지)
  - HTTPS 사용
- 중간:
  - JWT 인증
  - RBAC 권한 시스템
  - bcrypt 비밀번호 해싱
  - 보안 헤더 설정
  - 의존성 스캔 (npm audit)
- 복잡:
  - OAuth2/OIDC
  - 암호화 키 관리 (KMS)
  - 보안 스캔 자동화 (Snyk, OWASP ZAP)
  - 침입 탐지 시스템 (IDS)
  - 카오스 엔지니어링 (보안 테스트)

**언어별 구현**:

- Python: bandit (SAST), safety (의존성), cryptography
- Rust: cargo-audit, clippy (unsafe 체크), RustCrypto
- TypeScript: helmet (보안 헤더), npm audit, bcrypt
- Go: gosec, go-critic, crypto 패키지

**왜 필수인가?**: 보안 사고 1건 = 프로젝트 전체 신뢰 상실. 개인정보 유출 = 법적 책임 + 벌금. SQL Injection 하나로 DB 전체 탈취 가능. 모든 소프트웨어는 공격 대상.

------

## 📊 DNA 시스템 체크리스트

프로젝트 시작 시 **11개 모두** 체크:

```markdown
## DNA 시스템 11개 구축 (Stage 4-5)

### [ ] 1. Type System
- [ ] 타입 체커 설정
- [ ] strict mode 활성화
- [ ] any/dynamic 금지 규칙

### [ ] 2. Observability System
- [ ] 구조화된 로깅 설정
- [ ] trace_id 전파
- [ ] 메트릭 수집 (선택)

### [ ] 3. Testing System
- [ ] 테스트 프레임워크 설정
- [ ] 95% 커버리지 목표
- [ ] pre-commit hook (테스트 실행)

### [ ] 4. Code Quality System
- [ ] 포맷터 설정 + 자동 실행
- [ ] 린터 설정 + 경고 0개
- [ ] pre-commit hooks
- [ ] CI 파이프라인

### [ ] 5. Architecture Enforcement
- [ ] Layer 경계 정의
- [ ] import 규칙 설정
- [ ] Architecture tests

### [ ] 6. Configuration System
- [ ] .env 파일 설정
- [ ] 타입 안전한 설정 클래스
- [ ] 의존성 관리 도구 선택
- [ ] lock 파일 생성

### [ ] 7. Error Handling System
- [ ] 에러 타입 정의
- [ ] Result/Either 패턴
- [ ] 에러 로깅 통합

### [ ] 8. Performance System
- [ ] 벤치마크 설정
- [ ] 프로파일링 도구 설치
- [ ] 성능 회귀 체크

### [ ] 9. API System
- [ ] 인터페이스 정의
- [ ] API 문서 자동 생성 (선택)
- [ ] 타입 안전한 계약

### [ ] 10. Data System
- [ ] DB/파일 접근 계층 정의
- [ ] 연결 풀 설정
- [ ] 캐시 전략 (필요 시)

### [ ] 11. Security System
- [ ] 민감 정보 관리 (.env)
- [ ] 입력 검증 규칙
- [ ] 보안 스캔 설정
- [ ] 인증/권한 (API 있을 시)
```

------

## 🎯 Kent Beck 프로젝트 검증

Kent Beck의 BPlusTree 프로젝트에서 11개 DNA 모두 확인:

| DNA               | Kent Beck 구현                        | 검증 |
| ----------------- | ------------------------------------- | ---- |
| 1. Type           | Rust 타입 시스템 + strict             | ✅    |
| 2. Observability  | (명시적 로깅 없음)                    | ⚠️    |
| 3. Testing        | 95%+ 커버리지 + fuzz + property       | ✅    |
| 4. Code Quality   | cargo fmt + clippy + "Dead code dead" | ✅    |
| 5. Architecture   | Architecture tests                    | ✅    |
| 6. Configuration  | Cargo.toml + lock                     | ✅    |
| 7. Error Handling | Result<T,E> 강제, panic! 금지         | ✅    |
| 8. Performance    | Criterion + Instruments profiling     | ✅    |
| 9. API            | pub fn 인터페이스                     | ✅    |
| 10. Data          | Arena 메모리 관리                     | ✅    |
| 11. Security      | Memory safety, unsafe 감사            | ✅    |

**10/11개 명확히 구현!** (Observability는 라이브러리라서 최소화)


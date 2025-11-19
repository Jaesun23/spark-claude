# DNA 에이전트 시스템 집중 연구 계획

**작성일**: 2025-11-19
**작성자**: Jason & Claude (2호)
**목적**: 에이전트 시스템을 레고블럭 방식으로 분할하여 독립 연구

---

## 1. 개요

### 1.1 분할 원칙

**DNA v4.0 레고블럭 전략 적용**:
- 각 세션이 독립 실행 가능
- 그 세션 문서만 보고 작업 완료 가능
- 2-4시간 이내 완료 가능한 크기
- Context Rot 방지: 필요한 정보만 로드

### 1.2 세션 구성

| 세션 | 범위 | 예상 시간 | 의존성 |
|-----|-----|----------|-------|
| **0** | Context 관리 시스템 | 2-3시간 | 없음 (기반) |
| **1** | Stage 1 에이전트 | 3-4시간 | 세션 0 |
| **2** | Stage 2 에이전트 | 2-3시간 | 세션 0, 1 |
| **3** | Stage 3 에이전트 | 4시간 | 세션 0, 1, 2 |
| **4** | Stage 4 에이전트 | 3시간 | 세션 0, 1-3 |
| **5** | 통합 테스트 및 검증 | 3-4시간 | 세션 0-4 |

**총 예상 시간**: 17-21시간

---

## 2. 세션 0: Context 관리 시스템 (기반 인프라)

### 2.1 개요

**목표**: Context Rot 방지 3중 방어 시스템 구축
**예상 시간**: 2-3시간
**의존성**: 없음 (첫 번째로 실행)

### 2.2 입력 자료

- `DNA_Agent_Integrated_Process_Flow_v2.md` - 섹션 4 (Context Rot 방지)
- `20251119_Claude_Code_Features_for_DNA.md` - 섹션 5 (Hooks)
- Claude Code Hooks 공식 문서

### 2.3 작업 체크리스트

#### Step 1: JSON 구조 정의
- [ ] `docs/context/project_init.json` 스키마 정의
- [ ] `docs/context/stageX_output.json` 스키마 정의
- [ ] `docs/context/context_summary.json` 스키마 정의

#### Step 2: UserPromptSubmit Hook 구현
- [ ] `context_reranking.py` 작성
  - 현재 Stage 감지
  - 관련 컨텍스트만 추출
  - 프롬프트 상단에 주입
- [ ] settings.json에 Hook 등록

#### Step 3: PostToolUse Hook 구현
- [ ] `update_context_summary.py` 작성
  - Write 도구 감지
  - stage output 저장 시 summary 업데이트
- [ ] settings.json에 Hook 등록

#### Step 4: 테스트
- [ ] 간단한 프롬프트로 Context Re-ranking 테스트
- [ ] 파일 저장 시 Summary 업데이트 테스트

### 2.4 산출물

| 파일 | 경로 | 설명 |
|-----|-----|-----|
| Context Re-ranking Hook | `~/.claude/hooks/context_reranking.py` | UserPromptSubmit |
| Context Update Hook | `~/.claude/hooks/update_context_summary.py` | PostToolUse |
| JSON 스키마 예시 | `docs/context/*.json` | 각 Stage 출력 형식 |
| settings.json 업데이트 | `~/.claude/settings.json` | Hook 등록 |

### 2.5 검증 기준

- [ ] UserPromptSubmit Hook이 컨텍스트를 자동 주입
- [ ] PostToolUse Hook이 Summary를 자동 업데이트
- [ ] 이전 Stage 결과가 다음 Stage에서 사용 가능

---

## 3. 세션 1: Stage 1 에이전트 (System Classifier)

### 3.1 개요

**목표**: 18가지 패밀리 분류 에이전트 구축
**예상 시간**: 3-4시간
**의존성**: 세션 0 완료

### 3.2 입력 자료

- `DNA_ALL_GUIDES_MERGED.md` - Stage 1 관련 섹션
- `20251119_Gemini_Agent_Design_Insights.md` - 추가 Traits
- 18가지 패밀리 정의 (DNA 문서)
- Layer 1 질문 목록

### 3.3 작업 체크리스트

#### Step 1: Subagent 정의
- [ ] `.claude/agents/system-classifier-spark.md` 작성
  - **Traits**: Pattern Matching, Evidence-Based, Ambiguity Intolerance, Benchmark Obsession
  - **System Prompt**: 역할, 지침, 제약사항
  - **Self-Validation Checklist**
  - **Output Format**: stage1_output.json

#### Step 2: Slash Command 정의
- [ ] `.claude/commands/stage1.md` 작성
  - Context 로드 (@docs/context/project_init.json)
  - 에이전트 호출 지시
  - 인자 처리 ($ARGUMENTS)

#### Step 3: Validator Skill 작성
- [ ] `.claude/skills/verify-stage1/SKILL.md` 작성
- [ ] `.claude/skills/verify-stage1/scripts/validate_stage1.py` 작성
  - 패밀리 코드 형식 (A-A-B)
  - 검증 사례 개수 >= 2
  - 레이턴시 수치 명시
  - NFR 우선순위 포함

#### Step 4: Knowledge Skill (선택)
- [ ] `.claude/skills/architecture-patterns/SKILL.md` 작성
- [ ] 18가지 패밀리 정의 문서 포함

#### Step 5: 테스트
- [ ] `/stage1 주식 거래 플랫폼` 실행
- [ ] Validator 통과 확인
- [ ] 출력 형식 확인

### 3.4 산출물

| 파일 | 경로 |
|-----|-----|
| Subagent | `.claude/agents/system-classifier-spark.md` |
| Command | `.claude/commands/stage1.md` |
| Validator SKILL.md | `.claude/skills/verify-stage1/SKILL.md` |
| Validator Script | `.claude/skills/verify-stage1/scripts/validate_stage1.py` |

### 3.5 검증 기준

- [ ] `/stage1` 명령어로 에이전트 호출됨
- [ ] Ambiguity Intolerance: 모호한 입력 시 되묻기
- [ ] Benchmark Obsession: 구체적 수치 포함
- [ ] Validator 스크립트가 Pass/Fail 판정
- [ ] stage1_output.json 올바른 형식으로 저장

---

## 4. 세션 2: Stage 2 에이전트 (Constraints Investigator)

### 4.1 개요

**목표**: Layer 3 환경 제약 조사 에이전트 구축
**예상 시간**: 2-3시간
**의존성**: 세션 0, 1 완료

### 4.2 입력 자료

- `DNA_ALL_GUIDES_MERGED.md` - Stage 2 관련 섹션
- Stage 1 출력 (stage1_output.json)
- Layer 3 질문 목록

### 4.3 작업 체크리스트

#### Step 1: Subagent 정의
- [ ] `.claude/agents/constraints-investigator-spark.md` 작성
  - **Traits**: Inquisitive, Constraint-Aware, Conflict Anticipation
  - **System Prompt**: 패밀리에 맞는 질문 생성
  - **Self-Validation Checklist**

#### Step 2: Slash Command 정의
- [ ] `.claude/commands/stage2.md` 작성
  - stage1_output.json 참조
  - 에이전트 호출

#### Step 3: Validator Skill 작성
- [ ] `.claude/skills/verify-stage2/SKILL.md` 작성
- [ ] `.claude/skills/verify-stage2/scripts/validate_stage2.py` 작성
  - 3개 카테고리 완료 (기술/팀/인프라)
  - 충돌 2개 이상 식별
  - 해결안 3가지

#### Step 4: 테스트
- [ ] `/stage2` 실행 (Stage 1 완료 후)
- [ ] Context Re-ranking 확인 (패밀리, NFR 주입)
- [ ] Validator 통과

### 4.4 산출물

| 파일 | 경로 |
|-----|-----|
| Subagent | `.claude/agents/constraints-investigator-spark.md` |
| Command | `.claude/commands/stage2.md` |
| Validator | `.claude/skills/verify-stage2/` |

### 4.5 검증 기준

- [ ] Stage 1 결과(패밀리, NFR)가 Context로 주입됨
- [ ] 3개 카테고리 모두 조사됨
- [ ] 충돌 예측 및 해결안 제시됨

---

## 5. 세션 3: Stage 3 에이전트 (Architecture Decision Maker)

### 5.1 개요

**목표**: Bootstrap ADR 작성 에이전트 구축
**예상 시간**: 4시간
**의존성**: 세션 0, 1, 2 완료

### 5.2 입력 자료

- `DNA_ALL_GUIDES_MERGED.md` - Stage 3 (ADR) 관련 섹션
- `20251119_Gemini_Agent_Design_Insights.md` - Devil's Advocate, 3-Turn 대화
- Stage 1, 2 출력
- ADR 템플릿

### 5.3 작업 체크리스트

#### Step 1: Subagent 정의
- [ ] `.claude/agents/architecture-decision-maker-spark.md` 작성
  - **Traits**: Trade-off Reasoning, Devil's Advocate, Evidence-Based
  - **논리적 병렬화**: 스켈레톤 → 독립 확장
  - **3-Turn 대화**: 초안 → 반론 → 재작성

#### Step 2: Slash Command 정의
- [ ] `.claude/commands/stage3.md` 작성
  - stage1, stage2 output 참조
  - Bootstrap 요소 목록

#### Step 3: Validator Skill 작성
- [ ] `.claude/skills/verify-stage3/SKILL.md` 작성
- [ ] `.claude/skills/verify-stage3/scripts/validate_stage3.py` 작성
  - 모든 ADR 3옵션 비교
  - NFR+제약 반영
  - 충돌 해결
  - 예산 내

#### Step 4: Knowledge Skill
- [ ] `.claude/skills/bootstrap-knowledge/SKILL.md` 작성
  - RDBMS, Cache, Messaging 등 기술 지식

#### Step 5: 테스트
- [ ] `/stage3` 실행
- [ ] Devil's Advocate 동작 확인
- [ ] ADR 간 충돌 검증

### 5.4 산출물

| 파일 | 경로 |
|-----|-----|
| Subagent | `.claude/agents/architecture-decision-maker-spark.md` |
| Command | `.claude/commands/stage3.md` |
| Validator | `.claude/skills/verify-stage3/` |
| Knowledge | `.claude/skills/bootstrap-knowledge/` |

### 5.5 검증 기준

- [ ] 논리적 병렬화: 스켈레톤 먼저, 각 ADR 독립 확장
- [ ] Devil's Advocate: 자신의 선택 공격
- [ ] 3-Turn 대화: 초안 → 반론 → 재작성
- [ ] ADR 간 충돌 자동 검증

---

## 6. 세션 4: Stage 4 에이전트 (Blueprint Designer)

### 6.1 개요

**목표**: Clean Architecture 청사진 에이전트 구축
**예상 시간**: 3시간
**의존성**: 세션 0, 1-3 완료

### 6.2 입력 자료

- `DNA_ALL_GUIDES_MERGED.md` - Stage 4 (청사진) 관련 섹션
- Stage 1-3 출력
- Clean Architecture 원칙
- DDD 개념

### 6.3 작업 체크리스트

#### Step 1: Subagent 정의
- [ ] `.claude/agents/blueprint-designer-spark.md` 작성
  - **Traits**: Domain Modeling, Architectural Thinking, Dependency Awareness
  - **4-Layer 설계**: Domain, Application, Infrastructure, Presentation

#### Step 2: Slash Command 정의
- [ ] `.claude/commands/stage4.md` 작성
  - 모든 이전 Stage 출력 참조

#### Step 3: Validator Skill 작성
- [ ] `.claude/skills/verify-stage4/SKILL.md` 작성
- [ ] `.claude/skills/verify-stage4/scripts/validate_stage4.py` 작성
  - Dependency Rule 준수
  - Bootstrap 매핑 완료
  - API 일관성

#### Step 4: 테스트
- [ ] `/stage4` 실행
- [ ] 4-Layer 구조 확인
- [ ] Dependency Rule 검증

### 6.4 산출물

| 파일 | 경로 |
|-----|-----|
| Subagent | `.claude/agents/blueprint-designer-spark.md` |
| Command | `.claude/commands/stage4.md` |
| Validator | `.claude/skills/verify-stage4/` |

### 6.5 검증 기준

- [ ] Domain Layer가 외부 의존성 없음
- [ ] Bootstrap ADR이 Infrastructure에 매핑됨
- [ ] API 설계가 도메인 모델과 일관됨

---

## 7. 세션 5: 통합 테스트 및 검증

### 7.1 개요

**목표**: 전체 플로우 실행 및 일관성 검증
**예상 시간**: 3-4시간
**의존성**: 세션 0-4 완료

### 7.2 입력 자료

- 모든 이전 세션 산출물
- `DNA_Agent_Integrated_Process_Flow_v2.md`
- 테스트용 프로젝트 아이디어

### 7.3 작업 체크리스트

#### Step 1: 전체 플로우 실행
- [ ] `/stage1 [테스트 아이디어]` 실행
- [ ] `/stage2` 실행
- [ ] `/stage3` 실행
- [ ] `/stage4` 실행
- [ ] 모든 Validator 통과 확인

#### Step 2: Context Rot 방지 검증
- [ ] Stage 4에서 Stage 1 결정사항(패밀리, NFR) 준수 확인
- [ ] 모든 Stage에서 Context Re-ranking 동작 확인
- [ ] context_summary.json 업데이트 확인

#### Step 3: 일관성 검증
- [ ] 패밀리가 모든 ADR에 반영됨
- [ ] NFR 우선순위가 기술 선택에 반영됨
- [ ] 제약사항이 모든 결정에 준수됨

#### Step 4: 보완사항 도출
- [ ] 누락된 검증 항목
- [ ] 개선이 필요한 Traits
- [ ] 추가 필요한 Knowledge Skill

### 7.4 산출물

| 산출물 | 설명 |
|-------|-----|
| 테스트 결과 보고서 | 각 Stage 통과 여부, 시간 |
| Context Rot 측정 결과 | Stage 간 일관성 점수 |
| 보완사항 목록 | 다음 버전에 반영할 개선점 |

### 7.5 검증 기준

- [ ] Stage 1 → 4 전체 플로우 완료
- [ ] Context Rot 없음 (초기 결정사항 100% 준수)
- [ ] 모든 Validator Pass
- [ ] 산출물이 실무 사용 가능한 품질

---

## 8. 실행 순서 및 일정

### 8.1 추천 실행 순서

```
세션 0 (Context 관리) → 세션 1 (Stage 1) → 세션 2 (Stage 2)
→ 세션 3 (Stage 3) → 세션 4 (Stage 4) → 세션 5 (통합 테스트)
```

### 8.2 예상 일정

| 날짜 | 세션 | 시간 |
|-----|-----|-----|
| Day 1 | 세션 0, 1 | 5-7시간 |
| Day 2 | 세션 2, 3 | 6-7시간 |
| Day 3 | 세션 4, 5 | 6-7시간 |

**총 3일, 17-21시간**

### 8.3 각 세션 시작 시 주의사항

1. **이 문서의 해당 세션 섹션만 참조** (Context Rot 방지)
2. **이전 세션 산출물 확인** (의존성 체크)
3. **검증 기준 먼저 확인** (목표 명확화)

---

## 9. 참조 문서

- `DNA_Agent_Integrated_Process_Flow_v2.md` - 전체 설계
- `20251119_Claude_Code_Features_for_DNA.md` - Claude Code 기능
- `20251119_Gemini_Agent_Design_Insights.md` - Gemini 인사이트
- `DNA_ALL_GUIDES_MERGED.md` - DNA v4.0 전체 가이드

---

**작성자**: Jason & Claude (2호)
**날짜**: 2025-11-19

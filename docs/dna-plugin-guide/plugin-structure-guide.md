# Claude Code Plugin 구조 및 제작 가이드

## 개요

Claude Code Plugin은 Agents, Commands, Skills를 하나의 패키지로 묶어 배포할 수 있는 시스템입니다. DNA Methodology를 플러그인으로 패키징하여 재사용성과 배포 용이성을 확보합니다.

---

## 1. Plugin 디렉토리 구조

### 기본 레이아웃

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json              # ⚠️ 필수: 이 폴더에는 이 파일만!
│
├── agents/                      # Agent 정의 (자동 발견)
│   └── *.md
│
├── commands/                    # Slash 명령어 (자동 발견)
│   └── *.md
│
├── skills/                      # Skills (선택)
│   └── skill-name/
│       └── SKILL.md
│
├── hooks/                       # Event 핸들러 (선택)
│   └── hooks.json
│
├── templates/                   # 템플릿 파일들
│   └── *.md
│
└── README.md                    # 설치 및 사용법
```

### 핵심 규칙

**⚠️ 중요**: `.claude-plugin/` 폴더에는 `plugin.json`만 있어야 합니다!

```bash
# ✅ 올바른 구조
plugin-root/
├── .claude-plugin/plugin.json   # 매니페스트만
├── agents/                      # 루트에 위치
└── commands/                    # 루트에 위치

# ❌ 잘못된 구조
plugin-root/
└── .claude-plugin/
    ├── plugin.json
    ├── agents/                  # 여기 있으면 안됨!
    └── commands/                # 여기 있으면 안됨!
```

---

## 2. Plugin Manifest (plugin.json)

### 완전한 스키마

```json
{
  "name": "dna-methodology",
  "version": "1.0.0",
  "description": "DNA Methodology v4.0 - 9-stage software design system",

  "author": {
    "name": "Jason",
    "email": "email@example.com",
    "url": "https://github.com/username"
  },

  "homepage": "https://github.com/username/dna-methodology",
  "repository": "https://github.com/username/dna-methodology",
  "license": "MIT",

  "keywords": [
    "dna-methodology",
    "software-design",
    "architecture",
    "blueprint"
  ]
}
```

### 최소 필수 구성

```json
{
  "name": "dna-methodology",
  "description": "DNA Methodology design system",
  "version": "1.0.0",
  "author": {"name": "Jason"}
}
```

**Note**: `commands`와 `agents` 배열을 생략하면 해당 디렉토리에서 자동 발견됩니다.

### 필드 참조

| 필드 | 필수 | 설명 |
|------|------|------|
| `name` | YES | kebab-case 고유 식별자 |
| `version` | NO | 시맨틱 버저닝 |
| `description` | NO | 간략 설명 (max 1024) |
| `author` | NO | {name, email?, url?} |
| `commands` | NO | 명령어 경로 배열 (생략시 자동발견) |
| `agents` | NO | 에이전트 경로 배열 (생략시 자동발견) |

---

## 3. Agent 정의 형식

### 파일 구조

**위치**: `agents/stage1-classifier.md`

```markdown
---
name: stage1-classifier
description: 핵심 비즈니스 기능을 분류하고 패밀리 패턴으로 조직화.
             Stage 1에서 시스템의 기능적 분해가 필요할 때 사용.
tools: Bash, Read, Glob, Grep, Edit, Write, WebFetch
model: sonnet
color: blue
---

# Stage 1 Classifier Agent

[에이전트 상세 지시사항]

## Phase 1: 이해
[단계별 지시]

## Phase 2: 분석
[단계별 지시]

## Quality Verification
[품질 검증 방법]
```

### Frontmatter 필드

```yaml
---
name: stage1-classifier          # 필수: kebab-case, max 64자
description: "상세 설명..."       # 언제 사용하는지 포함
tools: Bash, Read, Write, Edit   # 사용할 도구 목록
model: sonnet                    # haiku/sonnet/opus
color: blue                      # UI 색상
---
```

### 모델 선택 기준

- `haiku`: 빠른 분석, 간단한 작업
- `sonnet`: 균형 잡힌 성능 (기본값)
- `opus`: 심층 분석, 복잡한 추론

---

## 4. Command 정의 형식

### 파일 구조

**위치**: `commands/stage1.md`

```markdown
---
name: stage1
description: DNA Methodology Stage 1 실행 - 핵심 기능 분류
type: command
requires: stage1-classifier
---

# /stage1 - 핵심 기능 분류

**목적**: 핵심 비즈니스 기능을 식별하고 패밀리로 분류

## 명령어 구문

```
/stage1 [project-name] [complexity-level]
```

## 인자

- `project-name` (선택): 분석할 프로젝트 이름
- `complexity-level` (선택): simple, moderate, complex

## 사용 예시

```
/stage1 "결제 플랫폼" moderate
/stage1
```
```

### 명령어 호출 패턴

```bash
/dna-methodology:stage1              # 네임스페이스 포함
/stage1                              # 간단한 형태 (고유한 경우)
/stage1 "My Project" moderate        # 인자 포함
```

---

## 5. 컴포넌트 통합 패턴

### 동작 흐름

```
사용자 호출: /stage1 "Project"
         │
         ▼
  ┌─────────────────┐
  │ Command Handler │ (commands/stage1.md)
  │  - 검증         │
  │  - 오케스트레이션│
  └────────┬────────┘
           │
           ▼
  ┌─────────────────────┐
  │   Agent Execution   │ (agents/stage1-classifier.md)
  │  - 분석             │
  │  - 작업 수행        │
  │  - 품질 검증        │
  └────────┬────────────┘
           │
           ▼
  ┌─────────────────┐
  │   Skills 활용   │ (선택적)
  │ - 지식 참조     │
  └─────────────────┘
           │
           ▼
  ┌─────────────────┐
  │   산출물 생성   │
  │ 01F-01_core...  │
  └─────────────────┘
```

### Skill 통합

Skills는 지식 조직화를 위해 선택적으로 사용:

```
skills/
├── dna-family-patterns/
│   └── SKILL.md
├── dna-adr-patterns/
│   └── SKILL.md
└── dna-best-practices/
    └── SKILL.md
```

---

## 6. Plugin 제작 프로세스

### Step 1: 구조 초기화

```bash
mkdir -p dna-methodology-plugin/.claude-plugin
cd dna-methodology-plugin
mkdir -p agents commands skills templates
```

### Step 2: Manifest 생성

**파일**: `.claude-plugin/plugin.json`

```json
{
  "name": "dna-methodology",
  "version": "1.0.0",
  "description": "DNA Methodology v4.0",
  "author": {"name": "Jason"}
}
```

### Step 3: Agent 생성

**파일**: `agents/stage1-classifier.md`

### Step 4: Command 생성

**파일**: `commands/stage1.md`

### Step 5: 로컬 테스트

**파일**: `.claude-plugin/marketplace.json`

```json
{
  "name": "dna-dev-marketplace",
  "owner": {"name": "Jason"},
  "plugins": [
    {
      "name": "dna-methodology",
      "source": "./",
      "version": "1.0.0"
    }
  ]
}
```

테스트:

```bash
/plugin marketplace add ./dna-methodology-plugin/.claude-plugin
/plugin install dna-methodology@dna-dev-marketplace
/stage1
```

---

## 7. 배포 방법

### GitHub Marketplace

1. GitHub 저장소에 푸시
2. 루트에 `marketplace.json` 생성
3. 사용자 설치:

```bash
/plugin marketplace add https://github.com/username/dna-methodology
/plugin install dna-methodology@username/dna-methodology
```

### 팀 설치

**프로젝트의 `.claude/settings.json`**:

```json
{
  "extraKnownMarketplaces": [
    "https://github.com/username/dna-methodology"
  ]
}
```

---

## 8. 버전 관리

### 시맨틱 버저닝

```
MAJOR.MINOR.PATCH
```

- **MAJOR**: 호환성 깨는 변경 (에이전트 인터페이스 변경)
- **MINOR**: 새 에이전트/명령어 추가 (하위 호환)
- **PATCH**: 버그 수정, 문서 업데이트

### 예시

```
1.0.0  - 초기 릴리즈 (Stage 1-9)
1.1.0  - multi-stage 명령어 추가
1.2.0  - dna-audit 명령어 추가
2.0.0  - 에이전트 페르소나 재설계 (breaking)
```

---

## 9. 베스트 프랙티스

### 네이밍 컨벤션

```
Agents:    stage{N}-{specialist}.md
Commands:  stage{N}.md 또는 dna-{action}.md
Skills:    dna-{concept}/SKILL.md
Templates: stage{N}-template.md
```

### Agent 설계

**✅ DO**:
```yaml
name: stage1-classifier
description: "핵심 비즈니스 기능을 패밀리 패턴으로 분류.
             새 시스템 설계 시작 시 기능 경계를 명확히 할 때 사용."
tools: Read, Write, Bash, Glob, Grep
model: sonnet
```

**❌ DON'T**:
```yaml
name: classifier          # 너무 일반적
description: "분류함"     # 너무 모호
tools: *                  # 너무 광범위
```

---

## 10. 품질 체크리스트

### 배포 전 확인

```
Plugin 구조:
  [ ] .claude-plugin/plugin.json 존재
  [ ] agents/ 디렉토리에 에이전트 있음
  [ ] commands/ 디렉토리에 명령어 있음
  [ ] README.md 존재

Manifest:
  [ ] "name" 필드 kebab-case
  [ ] "version" 시맨틱 버저닝
  [ ] "description" 명확함
  [ ] "author" 정보 완전함

Agent 파일:
  [ ] 고유한 name
  [ ] description에 사용 시점 포함
  [ ] tools 필드에 실제 사용 도구만
  [ ] model 지정됨
  [ ] 상세한 구현 지시

Command 파일:
  [ ] 고유한 name
  [ ] description 설명 충분
  [ ] requires에 필요한 에이전트
  [ ] 사용 예시 포함

테스트:
  [ ] 로컬 테스트 통과
  [ ] /help에 명령어 표시
  [ ] 각 명령어 오류 없이 실행
  [ ] 예상 산출물 생성
```

---

## 참고 문서

- 공식 Plugins: https://code.claude.com/docs/en/plugins.md
- Plugins Reference: https://code.claude.com/docs/en/plugins-reference.md
- Slash Commands: https://code.claude.com/docs/en/slash-commands.md
- Marketplaces: https://code.claude.com/docs/en/plugin-marketplaces.md

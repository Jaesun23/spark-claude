> agent 정의할 때 trigger 를 정의하는 규칙이 있나요?

 Agent 자체에는 별도의 "trigger" 정의 규칙이 없습니다. Agent는 사용자의 명령이나 상호작용으로 시작되며, 작업이 명확해지면 독립적으로 계획하고 작동합니다[(1)](https://www.anthropic.com/engineering/building-effective-agents).

하지만 **Agent Skills**의 경우, Skills가 언제 사용되어야 하는지를 정의하는 중요한 규칙이 있습니다:

## Agent Skills의 Discovery 규칙

Skills는 **model-invoked**로, Claude가 사용자의 요청과 Skill의 description을 기반으로 자율적으로 사용 시점을 결정합니다[(2)](https://docs.claude.com/en/docs/claude-code/skills). 이는 사용자가 명시적으로 호출하는 slash commands와 다릅니다[(2)](https://docs.claude.com/en/docs/claude-code/skills).

### Description 작성 규칙

`description` 필드는 Skill discovery에 핵심적이며, 다음 규칙을 따라야 합니다[(3)](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices#skill-structure):

- **최대 1024자**[(3)](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices#skill-structure)
- **비어있지 않아야 함**[(3)](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices#skill-structure)
- **XML 태그를 포함할 수 없음**[(3)](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices#skill-structure)
- **Skill이 무엇을 하는지와 언제 사용해야 하는지를 모두 설명해야 함**[(2)](https://docs.claude.com/en/docs/claude-code/skills)[(3)](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices#skill-structure)

### 효과적인 Description 작성 예시

```yaml
---
name: pdf-processing
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
---
```

[(4)](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview#how-skills-work)

Description은 **3인칭으로 작성**해야 하며, 구체적인 키워드와 트리거/컨텍스트를 포함해야 합니다[(3)](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices#skill-structure). Claude는 이 description을 사용하여 잠재적으로 100개 이상의 Skills 중에서 적절한 Skill을 선택합니다[(3)](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices#skill-structure).



> 방금 "구체적인 키워드와 트리거/컨텍스트를 포함해야 합니다"라고 하셨네요?



네, 맞습니다. Description 작성 시 **구체적이고 주요 용어를 포함**해야 합니다[(1)](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices#skill-structure).

문서에서는 다음과 같이 설명합니다:

"**Be specific and include key terms**. Include both what the Skill does and specific triggers/contexts for when to use it."[(1)](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices#skill-structure)

각 Skill에는 정확히 하나의 description 필드가 있으며, 이 description은 skill selection에 매우 중요합니다. Claude는 이를 사용하여 잠재적으로 100개 이상의 사용 가능한 Skills 중에서 올바른 Skill을 선택합니다[(1)](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices#skill-structure).

## 효과적인 예시

**PDF Processing skill:**

```
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

[(1)](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices#skill-structure)

**Excel Analysis skill:**

```
description: Analyze Excel spreadsheets, create pivot tables, generate charts. Use when analyzing Excel files, spreadsheets, tabular data, or .xlsx files.
```

[(1)](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices#skill-structure)

## 피해야 할 모호한 예시

```
description: Helps with documents
description: Processes data
description: Does stuff with files
```

[(1)](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices#skill-structure)

Description은 Skill이 무엇을 하는지와 함께 **언제 사용해야 하는지에 대한 구체적인 트리거/컨텍스트**를 모두 제공해야 합니다[(1)](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices#skill-structure).



> 음.. 근데 이건 skills 에 대한 설명이고, subagents의 경우에도 같낟요?

 네, **Subagents도 동일한 원칙을 따릅니다**. Subagents 정의 시에도 `description` 필드가 핵심적이며, Claude가 언제 해당 subagent를 호출할지 결정하는 데 사용됩니다[(1)](https://docs.claude.com/en/docs/claude-code/sub-agents)[(2)](https://docs.claude.com/en/api/agent-sdk/subagents#benefits-of-using-subagents).

## Subagent의 Description 규칙

Subagent 파일 구조에서 `description` 필드는 **필수**이며, "언제 이 subagent를 호출해야 하는지"를 설명합니다[(1)](https://docs.claude.com/en/docs/claude-code/sub-agents):

```markdown
---
name: your-sub-agent-name
description: Description of when this subagent should be invoked
tools: tool1, tool2, tool3  # Optional
model: sonnet  # Optional
---
```

[(1)](https://docs.claude.com/en/docs/claude-code/sub-agents)

## 구체적인 Description 작성의 중요성

SDK에서 subagent를 정의할 때도 동일한 원칙이 적용됩니다[(2)](https://docs.claude.com/en/api/agent-sdk/subagents#benefits-of-using-subagents):

```typescript
agents: {
  'code-reviewer': {
    description: 'Expert code review specialist. Use for quality, security, and maintainability reviews.',
    prompt: '...',
    tools: ['Read', 'Grep', 'Glob'],
    model: 'sonnet'
  }
}
```

[(2)](https://docs.claude.com/en/api/agent-sdk/subagents#benefits-of-using-subagents)

**Description을 구체적으로 작성하고 action-oriented하게 만들어야 Claude가 적절한 subagent를 선택할 수 있습니다**[(1)](https://docs.claude.com/en/docs/claude-code/sub-agents).

## 실제 예시

**좋은 예시 - 구체적인 트리거 포함:**

```yaml
description: Analyze sales data in Excel files and CRM exports. Use for sales reports, pipeline analysis, and revenue tracking.
```

[(3)](https://docs.claude.com/en/docs/claude-code/skills)

**나쁜 예시 - 모호함:**

```yaml
description: For data analysis
```

[(3)](https://docs.claude.com/en/docs/claude-code/skills)

Skills와 Subagents 모두 Claude가 자율적으로 선택하므로, description에 **무엇을 하는지**와 **언제 사용해야 하는지**를 명확히 포함해야 합니다[(1)](https://docs.claude.com/en/docs/claude-code/sub-agents)[(3)](https://docs.claude.com/en/docs/claude-code/skills)[(2)](https://docs.claude.com/en/api/agent-sdk/subagents#benefits-of-using-subagents).



> subagent 파일에서 YAML 프론트메터에 대한 각 항목의 의미와 반드시 들어가야 할 항목들이 무엇인지 정리해주세요.



# Subagent YAML Frontmatter 항목 정리

## 필수 항목

| 필드          | 필수 여부 | 설명                                                         |
| ------------- | --------- | ------------------------------------------------------------ |
| `name`        | **필수**  | 소문자와 하이픈을 사용한 고유 식별자[(1)](https://docs.claude.com/en/docs/claude-code/sub-agents#subagent-configuration) |
| `description` | **필수**  | Subagent의 목적을 설명하는 자연어 설명[(1)](https://docs.claude.com/en/docs/claude-code/sub-agents#subagent-configuration) |

## 선택 항목

| 필드    | 필수 여부 | 설명                                                         | 기본값                                  |
| ------- | --------- | ------------------------------------------------------------ | --------------------------------------- |
| `tools` | 선택      | 쉼표로 구분된 특정 도구 목록. 생략 시 메인 스레드의 모든 도구를 상속[(1)](https://docs.claude.com/en/docs/claude-code/sub-agents#subagent-configuration) | 모든 도구 상속                          |
| `model` | 선택      | Subagent가 사용할 모델. Model alias(`sonnet`, `opus`, `haiku`) 또는 `'inherit'` 사용 가능[(1)](https://docs.claude.com/en/docs/claude-code/sub-agents#subagent-configuration) | 설정된 subagent 모델 (기본값: `sonnet`) |

## 각 항목의 상세 설명

### `name` (필수)

- 소문자와 하이픈만 사용하는 고유 식별자[(1)](https://docs.claude.com/en/docs/claude-code/sub-agents#subagent-configuration)
- 예: `code-reviewer`, `test-runner`, `debugger`

### `description` (필수)

- Subagent의 목적을 설명하는 자연어 문장[(1)](https://docs.claude.com/en/docs/claude-code/sub-agents#subagent-configuration)
- Claude가 언제 이 subagent를 사용할지 결정하는 데 사용됨[(1)](https://docs.claude.com/en/docs/claude-code/sub-agents#subagent-configuration)
- **작성 팁**: "Use proactively" 또는 "MUST BE USED" 같은 문구를 포함하면 더 적극적으로 사용됨[(1)](https://docs.claude.com/en/docs/claude-code/sub-agents#subagent-configuration)

**예시:**

```yaml
description: Use proactively to run tests and fix failures
```

[(1)](https://docs.claude.com/en/docs/claude-code/sub-agents#subagent-configuration)

**YAML 포맷 주의사항**: Prettier 같은 포맷터를 사용할 경우, description 뒤에 줄바꿈이 추가되면 YAML 매핑으로 인식되어 오류가 발생할 수 있습니다. 이 경우 `|`를 사용하세요[(2)](https://github.com/anthropics/claude-code/issues/7943):

```yaml
# 올바른 방식
description: |
  Create interface designs, wireframes, and design systems.
```

[(2)](https://github.com/anthropics/claude-code/issues/7943)

### `tools` (선택)

- 쉼표로 구분된 도구 이름 목록[(1)](https://docs.claude.com/en/docs/claude-code/sub-agents#subagent-configuration)
- 생략하면 메인 스레드의 모든 도구를 상속 (MCP 도구 포함)[(1)](https://docs.claude.com/en/docs/claude-code/sub-agents#subagent-configuration)
- 세밀한 제어가 필요할 때만 지정[(1)](https://docs.claude.com/en/docs/claude-code/sub-agents#subagent-configuration)

**예시:**

```yaml
tools: Read, Grep, Glob, Bash
```

[(1)](https://docs.claude.com/en/docs/claude-code/sub-agents#subagent-configuration)

**권장 사항**: `/agents` 명령을 사용하면 사용 가능한 모든 도구 목록(MCP 서버 도구 포함)을 확인하고 선택할 수 있어 편리합니다[(1)](https://docs.claude.com/en/docs/claude-code/sub-agents#subagent-configuration).

### `model` (선택)

- Subagent가 사용할 AI 모델 지정[(1)](https://docs.claude.com/en/docs/claude-code/sub-agents#subagent-configuration)
- **사용 가능한 값**:
  - `sonnet` - Sonnet 모델 사용
  - `opus` - Opus 모델 사용
  - `haiku` - Haiku 모델 사용
  - `'inherit'` - 메인 대화와 동일한 모델 사용[(1)](https://docs.claude.com/en/docs/claude-code/sub-agents#subagent-configuration)
- 생략 시 subagent용으로 설정된 기본 모델 사용 (기본값: `sonnet`)[(1)](https://docs.claude.com/en/docs/claude-code/sub-agents#subagent-configuration)

**`'inherit'` 사용 시점**: 메인 대화의 모델 선택에 맞춰 subagent도 동일한 기능과 응답 스타일을 유지하고 싶을 때 유용합니다[(1)](https://docs.claude.com/en/docs/claude-code/sub-agents#subagent-configuration).

## 완전한 예시

```markdown
---
name: test-runner
description: Use proactively to run tests and fix failures
tools: Read, Edit, Bash, Grep
model: inherit
---

You are a test automation expert. When you see code changes, 
proactively run the appropriate tests. If tests fail, analyze 
the failures and fix them while preserving the original test intent.
```

[(1)](https://docs.claude.com/en/docs/claude-code/sub-agents#subagent-configuration)

## SDK에서의 정의 (TypeScript/Python)

SDK를 사용할 경우 프로그래밍 방식으로도 동일한 필드를 정의할 수 있습니다[(3)](https://docs.claude.com/en/api/agent-sdk/subagents#creating-subagents):

```typescript
agents: {
  'code-reviewer': {
    description: 'Expert code review specialist. Use for quality, security, and maintainability reviews.',
    prompt: 'You are a code review specialist...',
    tools: ['Read', 'Grep', 'Glob'],
    model: 'sonnet'
  }
}
```

[(3)](https://docs.claude.com/en/api/agent-sdk/subagents#creating-subagents)

**

> 끝인가요?

 네, 공식 문서에서 확인할 수 있는 **Subagent YAML frontmatter의 모든 필수/선택 항목**은 위에서 설명한 것이 전부입니다:

- **필수**: `name`, `description`
- **선택**: `tools`, `model`

## 추가로 알아두면 좋은 정보

### 1. GitHub Issue에서 언급된 `color` 필드

공식 문서에는 `color` 필드가 명시되어 있지 않지만, GitHub Issue[(6)](https://github.com/anthropics/claude-code/issues/8501)에서 사용자들이 `/agents` 명령으로 생성된 subagent에 `color: blue`, `color: purple` 같은 필드가 포함된 것을 발견했습니다. 하지만 이는 **공식 문서화되지 않은 필드**입니다[(6)](https://github.com/anthropics/claude-code/issues/8501).

### 2. Description 작성 시 주의사항

GitHub Issue[(7)](https://github.com/anthropics/claude-code/issues/10504)에서 description 필드의 설계 문제가 지적되었습니다:

- 공식 문서는 1024자 제한을 명시하지만, 실제로는 훨씬 긴 description이 생성되기도 함
- 이스케이프된 `\n`으로 가독성이 떨어짐
- YAML literal block syntax (`|`)가 작동하지만 문서화되지 않음[(7)](https://github.com/anthropics/claude-code/issues/10504)

### 3. Subagent 관리 방법

**권장 방법**: `/agents` 명령 사용[(1)](https://docs.claude.com/en/docs/claude-code/sub-agents#subagent-configuration)

```
/agents
```

이 명령으로:

- 모든 사용 가능한 subagent 확인
- 새 subagent 생성 (가이드 제공)
- 기존 subagent 편집 (도구 권한 포함)
- Subagent 삭제
- 사용 가능한 모든 도구 목록 확인[(1)](https://docs.claude.com/en/docs/claude-code/sub-agents#subagent-configuration)

**직접 파일 관리**도 가능합니다[(1)](https://docs.claude.com/en/docs/claude-code/sub-agents#subagent-configuration):

```bash
# 프로젝트 레벨 subagent
mkdir -p .claude/agents
echo '---
name: test-runner
description: Use proactively to run tests and fix failures
---
...' > .claude/agents/test-runner.md

# 사용자 레벨 subagent
mkdir -p ~/.claude/agents
```

공식 문서에 명시된 필수/선택 항목은 위에서 설명한 4가지(`name`, `description`, `tools`, `model`)가 전부입니다[(1)](https://docs.claude.com/en/docs/claude-code/sub-agents#subagent-configuration).



> 아.. 위에서  ------ SDK에서의 정의 (TypeScript/Python) SDK를 사용할 경우 프로그래밍 방식으로도 동일한 필드를 정의할 수 있습니다3: typescript agents: {  'code-reviewer': {    description: 'Expert code review specialist. Use for quality, security, and maintainability reviews.',    prompt: 'You are a code review specialist...',    tools: ['Read', 'Grep', 'Glob'],    model: 'sonnet'  } } 3 ** ------ 저렇게 '**'로 끝이 나서 내용이 더 있는 건가 했어요.

아, 죄송합니다! 그건 제 응답이 잘못 끝난 것이었습니다. `**`는 마크다운 볼드 처리를 위한 것이었는데 닫히지 않아서 혼란을 드렸네요.

SDK에서의 정의 부분은 그것으로 완료되었습니다. 추가 내용은 없습니다.

## 정리하면

**Subagent YAML frontmatter 필드 (파일 기반):**

- `name` (필수)
- `description` (필수)
- `tools` (선택)
- `model` (선택)

**SDK에서 프로그래밍 방식으로 정의할 때 (TypeScript/Python):**[(1)](https://docs.claude.com/en/api/agent-sdk/subagents#creating-subagents)

- `description` (필수)
- `prompt` (필수) - 시스템 프롬프트 내용
- `tools` (선택)
- `model` (선택)

SDK 방식에서는 `name`이 객체의 키로 사용되고(`'code-reviewer'`), `prompt` 필드가 추가로 필요합니다[(1)](https://docs.claude.com/en/api/agent-sdk/subagents#creating-subagents).

이것이 공식 문서에서 확인할 수 있는 전체 내용입니다. 혼란을 드려 죄송합니다!



> 그럼 Agent 프론트매터 다음의 내용은 어떤 구성으로 어떤 내용으로 작성이 되어야 하나요?

# Subagent Frontmatter 다음의 내용 구성

Frontmatter 다음에는 **subagent의 시스템 프롬프트**가 위치합니다. 이 프롬프트는 subagent의 역할, 능력, 문제 해결 접근 방식을 명확하게 정의합니다[(1)](https://docs.claude.com/en/docs/claude-code/sub-agents#subagent-configuration).

## 기본 구조

```markdown
---
name: your-sub-agent-name
description: Description of when this subagent should be invoked
tools: tool1, tool2, tool3
model: inherit
---

Your subagent's system prompt goes here. This can be multiple paragraphs
and should clearly define the subagent's role, capabilities, and approach
to solving problems.

Include specific instructions, best practices, and any constraints
the subagent should follow.
```

[(1)](https://docs.claude.com/en/docs/claude-code/sub-agents#subagent-configuration)

## 시스템 프롬프트 작성 원칙

시스템 프롬프트는 다음을 포함해야 합니다[(1)](https://docs.claude.com/en/docs/claude-code/sub-agents#subagent-configuration):

1. **역할 정의**: Subagent가 누구인지 명확히 설명
2. **능력**: 무엇을 할 수 있는지
3. **접근 방식**: 문제를 어떻게 해결할 것인지
4. **구체적인 지침**: 따라야 할 베스트 프랙티스
5. **제약 조건**: 지켜야 할 제한사항

## 실제 예시

### Code Reviewer Subagent

```markdown
---
name: code-reviewer
description: Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code.
tools: Read, Grep, Glob, Bash
model: inherit
---

You are a senior code reviewer ensuring high standards of code quality and security.

When invoked:

1. Run git diff to see recent changes
2. Focus on modified files
3. Begin review immediately

Review checklist:
- Code is simple and readable
- Functions and variables are well-named
- No duplicated code
- Proper error handling
- No exposed secrets or API keys
- Input validation implemented
- Good test coverage
- Performance considerations addressed

Provide feedback organized by priority:
- Critical issues (must fix)
- Warnings (should fix)
- Suggestions (consider improving)

Include specific examples of how to fix issues.
```

[(1)](https://docs.claude.com/en/docs/claude-code/sub-agents#subagent-configuration)

### Test Runner Subagent

```markdown
---
name: test-runner
description: Use proactively to run tests and fix failures
tools: Read, Edit, Bash, Grep
model: inherit
---

You are a test automation expert. When you see code changes, 
proactively run the appropriate tests. If tests fail, analyze 
the failures and fix them while preserving the original test intent.
```

[(1)](https://docs.claude.com/en/docs/claude-code/sub-agents#subagent-configuration)

## 효과적인 시스템 프롬프트 작성 가이드

### 1. 명확한 역할 정의

```markdown
You are a senior code reviewer ensuring high standards of code quality and security.
```

[(1)](https://docs.claude.com/en/docs/claude-code/sub-agents#subagent-configuration)

### 2. 구체적인 실행 단계

```markdown
When invoked:

1. Run git diff to see recent changes
2. Focus on modified files
3. Begin review immediately
```

[(1)](https://docs.claude.com/en/docs/claude-code/sub-agents#subagent-configuration)

### 3. 체크리스트 제공

```markdown
Review checklist:
- Code is simple and readable
- Functions and variables are well-named
- No duplicated code
```

[(1)](https://docs.claude.com/en/docs/claude-code/sub-agents#subagent-configuration)

### 4. 우선순위가 있는 출력 형식

```markdown
Provide feedback organized by priority:
- Critical issues (must fix)
- Warnings (should fix)
- Suggestions (consider improving)
```

[(1)](https://docs.claude.com/en/docs/claude-code/sub-agents#subagent-configuration)

## Context Engineering 관점

효과적인 시스템 프롬프트는 **최소한의 고신호 토큰**으로 원하는 결과를 최대화해야 합니다[(2)](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents). 

### 적절한 고도(Altitude) 유지

시스템 프롬프트는 두 극단을 피해야 합니다[(2)](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents):

- **너무 구체적**: 복잡하고 취약한 if-else 로직을 하드코딩
- **너무 모호**: 구체적인 신호 없이 막연한 고수준 가이드만 제공

**최적 고도**: 행동을 효과적으로 가이드할 만큼 구체적이면서도, 모델에게 강력한 휴리스틱을 제공할 만큼 유연한 균형점[(2)](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).

### 구조화된 섹션 사용

프롬프트를 명확한 섹션으로 구성하는 것이 좋습니다[(2)](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents):

```markdown
## Role
You are a senior code reviewer...

## Process
When invoked:
1. ...
2. ...

## Guidelines
- ...
- ...

## Output Format
Provide feedback organized by...
```

이러한 구조는 XML 태그나 Markdown 헤더로 구분할 수 있습니다[(2)](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).

## 요약

Subagent frontmatter 다음의 내용은:

- **여러 단락으로 작성 가능**한 시스템 프롬프트[(1)](https://docs.claude.com/en/docs/claude-code/sub-agents#subagent-configuration)
- Subagent의 **역할, 능력, 접근 방식**을 명확히 정의[(1)](https://docs.claude.com/en/docs/claude-code/sub-agents#subagent-configuration)
- **구체적인 지침, 베스트 프랙티스, 제약 조건** 포함[(1)](https://docs.claude.com/en/docs/claude-code/sub-agents#subagent-configuration)
- 적절한 고도를 유지하며 구조화된 형식 사용[(2)](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
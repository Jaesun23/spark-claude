# CLAUDE.md

This file provides guidance to Claude Code when working with this repository.

---

## Project Overview

**spark-claude** is the Agent Definition Standard — a set of scientifically-grounded
principles for designing AI agent definitions, with reference implementations
for software development.

This project is not a plugin or framework. It is a **specification + reference**:
when building skills, plugins, or any system that needs agent definitions,
follow the standard documented here.

### Core Assets

| Asset | File | Purpose |
|-------|------|---------|
| **Agent Definition Standard** | `AGENT_DEFINITION_STANDARD.md` | 에이전트 정의의 표준 규격 — 실전(SPARK) + 이론(TRAITS) + 과학(Anthropic) 통합 |
| **Reference Agents** | `agents/*.md` | 표준을 적용한 소프트웨어 개발용 레퍼런스 에이전트 |
| **Research Docs** | `docs/*.md` | 표준의 과학적/이론적 기반 문서 |

## Project Structure

```
spark-claude/
├── AGENT_DEFINITION_STANDARD.md    # 핵심 — 에이전트 정의 표준
├── agents/                          # 레퍼런스 에이전트
│   ├── implementer.md              # 구현 전문가
│   ├── diagnostician.md            # 시스템 진단 전문가
│   └── auditor.md                  # 품질 감사 전문가
├── docs/
│   ├── history/                    # SPARK 발전사 (v1.0 ~ v5.0)
│   ├── TRAITS_RESEARCH.md          # TRAITS 연구 요약
│   └── ANTHROPIC_PERSONA_RESEARCH.md  # Anthropic 페르소나 연구 6편 요약
└── archive/                        # 이전 버전 보관 (spark-plugin, methodology 등)
```

## Reference Agents

| Agent | Role | When to Use |
|-------|------|-------------|
| **implementer** | 구현 전문가 | Feature implementation, bug fixes, test creation |
| **diagnostician** | 시스템 진단 전문가 | System analysis, debugging, root cause investigation |
| **auditor** | 품질 감사 전문가 | Code review, compliance audit, quality gate evaluation |

All agents follow the `AGENT_DEFINITION_STANDARD.md` template:
- 5-section structure (Identity & Traits → Methodology → Decisions → Self-Verification → Identity Statement)
- Personality-expression framing (no enforcement code blocks)
- Traits ≤ 5 with directional coherence
- Right Altitude principle

## How to Use This Project

### Using Reference Agents
Copy agent definitions from `agents/` into your project's agent directory.
Adapt tools and model settings to your project's needs.

### Creating New Agents
Follow `AGENT_DEFINITION_STANDARD.md`:
1. Choose a Role that activates the right personality cluster (Part 2, Principle 2)
2. Select ≤ 5 Traits with directional coherence (Part 2, Principle 3; Part 5 catalog)
3. Frame behaviors as personality expressions (Part 2, Principle 4)
4. Use the 5-section template (Part 3)
5. Verify against the checklist (Part 4)

## Scientific Foundation

The standard is grounded in three independent, converging sources:
- **SPARK** (practical): 5 failed projects → systematic enforcement principles
- **TRAITS** (theoretical): 150-trait catalog, Miller's 7±2 law applied to LLMs
- **Anthropic Research** (scientific): 6 papers on persona mechanics in neural networks

See `docs/ANTHROPIC_PERSONA_RESEARCH.md` and `docs/TRAITS_RESEARCH.md` for details.

## Notes

- `archive/` is a symlink → `~/Documents/99_Archive/spark-claude-archive/` (gitignored, not published)

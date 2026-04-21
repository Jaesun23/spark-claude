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
| **Agent Definition Standard** | `AGENT_DEFINITION_STANDARD.md` | Standard specification for agent definitions — integrating practice (SPARK) + theory (TRAITS) + science (Anthropic) |
| **Reference Agents** | `agents/*.md` | Reference agent implementations for software development |
| **Research Docs** | `docs/*.md` | Scientific and theoretical foundation documents |

## Project Structure

```
spark-claude/
├── AGENT_DEFINITION_STANDARD.md    # Core — Agent Definition Standard
├── agents/                          # Reference agents
│   ├── implementer.md              # Implementation specialist
│   ├── diagnostician.md            # System diagnostician
│   ├── auditor.md                  # Quality auditor
│   ├── surgeon.md                  # Code surgeon
│   └── surveyor.md                 # Survey / quantitative classification
├── docs/
│   ├── history/                    # SPARK evolution history (v1.0 ~ v5.0)
│   ├── TRAITS_RESEARCH.md          # TRAITS research summary
│   └── ANTHROPIC_PERSONA_RESEARCH.md  # Anthropic persona research (6 papers)
└── archive/                        # Previous versions (spark-plugin, methodology, etc.)
```

## Reference Agents

| Agent | Role | When to Use |
|-------|------|-------------|
| **implementer** | Implementation Specialist | Feature implementation, bug fixes, test creation |
| **diagnostician** | System Diagnostician | System analysis, debugging, root cause investigation |
| **auditor** | Quality Auditor | Code review, compliance audit, quality gate evaluation |
| **surgeon** | Code Surgeon | Dead code removal, pattern modernization, complexity reduction, code cleanup |
| **surveyor** | Surveyor | Classification, enumeration, coverage verification, reconciliation, distribution analysis |

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

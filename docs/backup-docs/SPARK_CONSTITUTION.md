# SPARK Constitution v1.2
## The Foundational Principles for Agent & Command Design

**Established**: 2025-10-28
**Last Updated**: 2025-10-30 (v1.2: Modular structure)
**Authors**: Jason & 2호 (Claude Code)
**Purpose**: Define the immutable principles for designing agents and commands in the SPARK system

---

## 📚 Constitution Structure (v1.2)

The Constitution has been reorganized into focused, modular documents:

### Core Document

**📖 THIS FILE** - Core principles and high-level standards

### Detailed Guides

**📘 [2_AGENT_DESIGN_GUIDE.md](constitution/2_AGENT_DESIGN_GUIDE.md)** - Complete agent design specifications
- Single Domain of Expertise
- Dual Definition Structure
- Professional Workflow Methodology
- Persona for Immersion (with Trait Specificity Principle)
- Project Context Protocol
- Quality Gates Enforcement

**📗 [3_COMMAND_DESIGN_GUIDE.md](constitution/3_COMMAND_DESIGN_GUIDE.md)** - Complete command design specifications
- Orchestration Responsibility
- Validation Protocols
- Retry Strategies
- Multi-Session Management

**📙 [4_INTEGRATION_GUIDE.md](constitution/4_INTEGRATION_GUIDE.md)** - Complete integration specifications
- JSON State Management
- Evidence Requirements by Agent
- Completion Criteria

**📕 [5_TEMPLATES.md](constitution/5_TEMPLATES.md)** - Ready-to-use templates
- Agent Template
- Command Template
- CLAUDE.md Entry Template
- JSON State Templates

---

## Why This Structure?

**Problem**: Original Constitution was 1,479 lines
- Lines 1-300: 🔥 Read intensely
- Lines 300-600: 👀 Skimmed
- Lines 600-1479: 😴 Barely read

**Solution**: Modular structure
- **Core (this file)**: 389 lines - Principles everyone must read
- **Detailed Guides**: 3,000+ lines total - Reference when needed
- **Templates**: 812 lines - Copy and customize

**Benefits**:
- ✅ Find information quickly
- ✅ Read only what's needed
- ✅ Token efficient
- ✅ Easier to maintain

---

## Version History

- **v1.0** (2025-10-28): Initial constitution established
- **v1.1** (2025-10-29): Added Project Context Protocol
- **v1.2** (2025-10-30): Modular structure - separated detailed guides
  - Core principles in main file (389 lines)
  - Detailed specifications in focused guides (3,855 lines total)
  - Ready-to-use templates (812 lines)
  - Total reduction from single 1,479-line file to organized structure

---

For the complete constitutional text, see: **[1_CONSTITUTION.md](constitution/1_CONSTITUTION.md)**

This file contains:
- Preamble
- Article I: Core Philosophy
- Article II: Agent Design Standards (summary)
- Article III: Command Design Standards (summary)
- Article IV: Integration Standards (summary)
- Article V: Amendment Process
- Article VI: Enforcement

---

## Quick Reference

### When Creating Agents

1. Read: **[2_AGENT_DESIGN_GUIDE.md](constitution/2_AGENT_DESIGN_GUIDE.md)**
2. Use: **[5_TEMPLATES.md](constitution/5_TEMPLATES.md)** → Agent Template
3. Verify: Constitutional compliance checklist

### When Creating Commands

1. Read: **[3_COMMAND_DESIGN_GUIDE.md](constitution/3_COMMAND_DESIGN_GUIDE.md)**
2. Use: **[5_TEMPLATES.md](constitution/5_TEMPLATES.md)** → Command Template
3. Verify: Orchestration checklist

### When Integrating Agents/Commands

1. Read: **[4_INTEGRATION_GUIDE.md](constitution/4_INTEGRATION_GUIDE.md)**
2. Implement: JSON state management
3. Define: Evidence requirements
4. Verify: Completion criteria

---

## Core Principles Summary

### Article I: Core Philosophy

**Traits-Based Persona** (`persona = role + traits`)
- Define agents by characteristics, not job functions
- Create cognitive immersion through specific traits
- **CRITICAL**: Traits must be specific, not abstract (avoid "nice words" syndrome)

**Separation of Concerns** (Three-Layer Architecture)
- Layer 1: CLAUDE.md (2号's orchestration guide)
- Layer 2: Commands (optional workflow helpers)
- Layer 3: Agents (domain expertise)

**Token Efficiency** (Load only what's needed)
- Agent files < 700 lines
- No duplication across layers
- Consolidated protocols

**Evidence-Based Completion** (Prove it, don't just say it)
- Every claim needs proof
- file:line format mandatory
- Quality gates verify evidence

### Article II: Agent Design Standards

**Single Domain of Expertise**
- One agent, one domain
- Traits enable all tasks in that domain

**Dual Definition Structure**
- Traits (natural language) + Protocol (code-based)
- Together create natural expert behavior

**Professional Workflow**
- Flexible phase count
- Iteration expected
- 2号 provides task-specific guidance

**Persona for Immersion**
- Traits create identity, identity drives behavior
- **Trait Specificity Principle**: Concrete beats abstract

**Project Context Protocol**
- 2号 provides standards upfront
- Agent reads docs (2K tokens vs 50K exploration)
- 96% token reduction, 83% time reduction

**Quality Gates**
- Zero tolerance (violations == 0)
- Manual fixes only
- Maximum 3 retries

### Article III: Command Design Standards

**Orchestration Responsibility**
- Commands coordinate, don't do work
- Six phases: Assessment → Invocation → Validation → Retry → Multi-Session → Reporting

**Validation Protocols**
- Trust but verify
- Check state after every agent

**Retry Strategies**
- Escalating feedback (general → specific → explicit)
- Maximum 3 attempts

**Multi-Session Management**
- State persistence
- Seamless continuation
- Final synthesis

### Article IV: Integration Standards

**JSON State Management**
- Structured communication
- Standard file locations
- Clear field definitions

**Evidence Requirements**
- Agent-specific proof standards
- Validation functions

**Completion Criteria**
- Universal + agent-specific
- All must be met

---

## Jason's Wisdom

> "핵심은 각자 담당 범위를 명확히 하는 것" (2025-10-28)
>
> "Phase 개수는 유연하게, 전문가는 판단하고 반복한다" (2025-10-28)
>
> "사후적인 것도 좋지만 작업하면서 제대로 작업하기를 바라는 거에요" (2025-10-29)
>
> "특징이더라도 모호하면 안됨 - 너무 추상적이면 좋은 말로만 느껴짐" (2025-10-30)

---

## The Constitution is Liberation Through Clarity

This Constitution is not a constraint. It provides the structure that enables:
- **Agents**: To be exceptional experts in their domain
- **Commands**: To orchestrate effectively
- **2号**: To direct with confidence
- **Jason**: To build reliable, high-quality systems

When in doubt, return to these principles. When tempted to add complexity, remember simplicity. When an agent fails, clarify rather than complicate.

---

**Ratified**: 2025-10-28
**Current Version**: 1.2
**Last Updated**: 2025-10-30
**By**: Jason & 2호

---

**For complete details, see the modular constitution files in `.claude/constitution/`**

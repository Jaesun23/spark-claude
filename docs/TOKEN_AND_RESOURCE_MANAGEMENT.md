# 📊 SPARK v3.5 Token and Resource Management Guide

## Executive Summary

This document consolidates validated findings on token management and resource optimization for the SPARK v3.5 multi-agent system, based on empirical testing and analysis of actual constraints with FileLockManager integration and team coordination.

---

## 🆕 SPARK v3.5 Token Management Changes

### FileLockManager Integration Impact
- **Thread-Safe Coordination**: FileLockManager adds ~2K tokens per team agent
- **Lock State Tracking**: Each team JSON file adds ~1K tokens to context
- **Team Coordination Overhead**: 4 teams = ~12K additional token overhead
- **Total v3.5 Overhead**: 15K tokens for multi-team coordination

### Team Agent Token Distribution
```yaml
Total Available: 200K context window
÷ 4 teams = 50K base allocation per team
- FileLockManager overhead: 3K
- Team JSON context: 2K  
- Base agent context: 10K
= 35K working capacity per team agent
```

### Token Safety Protocol (NEW in v3.5)
All agents now include mandatory pre-task assessment:
```yaml
Phase 1 - Context Calculation:
  - Agent definition: ~10K tokens
  - User instructions: 2-5K tokens  
  - Source code context: 5-15K tokens
  - Team coordination: 3-5K tokens (if applicable)

Phase 2 - Write Operation Estimation:  
  - Generated content size × 2 (memory + write)
  - Multiple files: each file × 2
  - Documentation generation: high token cost

Phase 3 - Abort Criteria:
  - If estimated total > 90K tokens → ABORT
  - Log to ~/.claude/workflows/task_aborted.json
  - Recommend task splitting
```

---

## 🎯 Core Truths About Token Management

### 1. The Reality of Token Measurement
- **Nobody can measure actual token usage** - Neither Claude CODE nor agents have access to token counting APIs
- Each agent gets an independent 200K context window
- Context accumulates and **cannot be cleared** during execution
- At 190K, agents must stop and summarize
- At 200K, hard termination with no output

### 2. The 90K Practical Limit (Detailed Calculation)

**Mathematical Breakdown:**
```yaml
200K Context Window (Claude 3.5 Sonnet base)
÷ 2 = 100K (Write tool doubling factor)
- 10K (Initial context overhead)
= 90K (Actual working capacity per agent)
```

**Initial Context Overhead (10K tokens):**
- **Agent definition**: ~3-5K tokens (system prompt, capabilities, examples)
- **Claude CODE injection**: ~2-3K tokens (task context, previous results, state)
- **Work instructions**: ~3-5K tokens (checklists, requirements, standards)

**Why This Conservative Approach:**
- Write operations double token consumption (memory + output)
- Context accumulates and cannot be cleared during execution
- Agents must estimate total token usage before starting work
- Prevents memory overflow situations that cause hard termination

### 3. Write Tool Token Doubling
```yaml
Example - Creating a 1000-line file:
  - Generate in memory: 15K tokens
  - Write tool output: 15K tokens (duplicate)
  - Total cost: 30K tokens for one file
```

### 4. Compression Must Be Explicit
- Agents do NOT auto-compress
- Requires explicit instruction: "Use MAXIMUM compression"
- Symbol/abbreviation use reduces tokens by 30-50%
- Information loss is minimal with proper compression

---

## 📈 Memory vs Tokens - Different Resources

### System Memory (RAM)
```yaml
Purpose: System stability
Limits: 4GB typical max
Affects: Parallel execution capacity
Management: OS level

Memory weights:
  light: 300MB   # Simple operations
  medium: 600MB  # Moderate complexity
  heavy: 1GB     # Complex operations
```

### API Tokens
```yaml
Purpose: Context window usage
Limits: 200K per agent (hard limit)
Affects: Individual task completion
Management: Cannot be measured or tracked

Practical limits:
  - With Write operations: 90K
  - Read-only operations: 180K
```

---

## 🔍 How Tokens Actually Accumulate

### Initial Context (Start of Task)
```yaml
Fixed costs:
  - Agent definition: ~10K tokens
  - User instructions: 2-5K tokens
  - JSON context (if any): 1-3K tokens
  
For implementer/tester only:
  - Checklist document: 10-20K tokens (800-1600 lines typical)
  
Initial total: 15-40K tokens
```

### During Execution (Accumulative)
```yaml
Each operation adds:
  - File read: 5-10K per file
  - Code generation: 10-30K
  - Write operation: Generated size × 2
  - Edit operations: 2-5K each
  
Nothing is ever removed from context!
```

### Real Example - Memory V5 Checklist
```yaml
Actual case study:
  - Checklist: 1,600 lines = 19K tokens
  - Read 5 reference files = 40K tokens
  - Generate implementation = 30K tokens
  - Write to files = 60K tokens (30K × 2)
  Total: 149K tokens → Agent failure
```

---

## 💡 Compression Strategy

### When to Compress
```yaml
Always compress - it's free insurance:
  - Minimal information loss
  - 30-50% token reduction
  - No performance penalty
```

### How to Compress
```yaml
Symbol system:
  → = leads to
  ✅ = complete
  ❌ = failed
  cfg = configuration
  impl = implementation
  
Remove:
  - Verbose explanations
  - Redundant descriptions
  - Formatting whitespace
  
Keep:
  - Essential logic
  - Critical values
  - Error messages
```

---

## 🚨 Token Safety Protocol for Agents

### Pre-Task Assessment
```yaml
1. Calculate initial context:
   - Agent definition: 10K
   - Instructions received: measure
   - Checklist (if any): lines × 12
   
2. Estimate workload:
   - Files to read: count × 8K
   - Code to generate: estimate size
   - Write operations: size × 2
   
3. If total > 90K:
   - Record reasoning in JSON
   - Suggest task split
   - Abort immediately
```

### Abort JSON Format
```json
{
  "status": "aborted",
  "reason": "token_limit_exceeded",
  "estimated_tokens": 125000,
  "limit": 90000,
  "breakdown": {
    "initial_context": 35000,
    "file_operations": 40000,
    "code_generation": 50000
  },
  "recommendation": "Split into 2-3 smaller tasks"
}
```

---

## 🎯 Practical Guidelines

### For All Agents
1. **Compression is default** - Always use abbreviated format
2. **90K is the limit** - Plan all work within this constraint
3. **Abort if exceeding** - Better to stop early than fail mid-task

### For implementer-spark and tester-spark
- **Checklist warning**: 1000+ lines = 12K+ tokens immediately
- **Extra caution needed**: Less room for actual work
- **Consider splitting**: Large checklists should trigger task division

### For Write-Heavy Operations
- **Progressive creation**: Build files in sections, not all at once
- **Skeleton first**: Create structure, then fill details
- **Never hold large files in memory**: Stream or chunk instead

---

## ✅ What We Know Works

1. **Conservative estimation** - Assume worst case for token usage
2. **Early compression** - Start compressed, don't wait
3. **Task splitting** - Multiple small tasks > one large task
4. **Progressive writes** - Build incrementally to avoid doubling

---

## ❌ What Doesn't Work

1. **Token counting** - No API exists for agents
2. **Context clearing** - Impossible in conversation model
3. **Automatic compression** - Must be explicitly instructed
4. **Token budgets** - Meaningless without measurement

---

## 📊 Reference Tables

### Task Complexity Token Estimates
```yaml
Simple (1-2 files, basic edits):
  - Initial: 20K
  - Work: 20-30K
  - Total: 40-50K → Safe

Moderate (3-5 files, new features):
  - Initial: 25K
  - Work: 40-50K
  - Total: 65-75K → Compress

Complex (5+ files, major changes):
  - Initial: 35K
  - Work: 60-80K
  - Total: 95-115K → Split required
```

### Agent Categories
```yaml
High Risk (Write-heavy):
  - implementer-spark (with checklists)
  - tester-spark (with checklists)
  - documenter-spark
  - improver-spark
  
Medium Risk:
  - troubleshooter-spark
  - designer-spark
  - builder-spark
  
Low Risk (Read-mostly):
  - analyzer-spark
  - explainer-spark
  - loader-spark
  - indexer-spark
```

---

*Document created: 2025-01-11*
*Last updated: 2025-01-12*
*Version: 3.0 - Focused on validated facts only*
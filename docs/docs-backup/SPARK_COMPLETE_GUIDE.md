# SPARK v4.3 Complete Guide

## 🎯 System Overview

SPARK v4.3 (Subagent Performance Architecture with Reduced toKens) is a traits-based multi-agent orchestration system for Claude Code. It achieves 95.5% token reduction by loading only the required agent on-demand.

### Core Architecture
- **32 Specialized Agents**: 17 primary + 15 team agents
- **Token Efficiency**: 95.5% reduction vs loading all agents
- **Quality Gates**: 8-step verification with zero-tolerance
- **Parallel Execution**: Multi-team coordination support (up to 5 teams)

## 📋 Command Reference

### Single Agent Commands
```bash
/spark-analyze <scope>           # System analysis
/spark-implement <feature>       # Feature implementation
/spark-test <target>            # Testing
/spark-design <system>          # System design
/spark-document <scope>         # Documentation
/spark-clean <project>          # Code cleanup
/spark-fix <issue>              # Troubleshooting
/spark-improve <code>           # Performance optimization & modernization
Task("qc-spark", "fix ruff violations")  # Quality control (direct calls)
```

### Pipeline Commands (Sequential Phases)
```bash
/spark <complex-task>       # Full pipeline: analyze → implement → test → document
/spark-refactor <module>    # Refactor pipeline: analyze → improve → test
/spark-audit <system>       # Audit pipeline: analyze → troubleshoot → document
/spark-migrate <legacy>     # Migration: analyze → design → implement → test
/spark-optimize <scope>     # Optimization: analyze → improve → test
/spark-launch <feature>     # Full launch: design → implement → test → document → git
```

### Parallel Execution Command
```bash
/multi-implement task1,task2,task3,task4,task5
```

## 🚀 Execution Protocol for 2호(Claude Code)

### CRITICAL: Exact Execution Pattern

#### For Single Agent Commands:
```python
1. IMMEDIATELY CALL:
   Task("agent-name-spark", user_request)

2. WAIT for agent completion

3. CHECK ~/.claude/workflows/current_task.json:
   REQUIRED CONDITIONS:
   - quality.violations_total == 0
   - quality.can_proceed == true
   - state.status == "completed"

4. DECISION:
   ✅ ALL CONDITIONS MET → Report success
   ❌ ANY CONDITION FAILED → Retry with specific feedback
```

#### For Parallel Execution:
```python
# MUST call all agents in ONE message (true parallelism)
Task("team1-implementer-spark", task1)
Task("team2-implementer-spark", task2)
Task("team3-implementer-spark", task3)
Task("team4-implementer-spark", task4)
Task("team5-implementer-spark", task5)

# WAIT for ALL to complete
# Then proceed to next phase
```

## 🔧 Agent Phase Structure

### Universal 5-Phase Pattern

All agents follow this structure:

#### Phase 0: Task Initialization
```python
import json
import os

# Read task JSON
json_file = "~/.claude/workflows/current_task.json"
with open(os.path.expanduser(json_file), 'r') as f:
    task_data = json.load(f)
```

#### Phases 1-4: Agent-Specific Work
- Phase 1: Analysis/Discovery/Strategy
- Phase 2: Planning/Design/Foundation
- Phase 3: Implementation/Execution/Core Work
- Phase 4: Validation/Testing/Quality Check

#### Phase 5: Task Completion

##### Phase 5A: Quality Metrics Recording
```python
# Record actual metrics
syntax_errors = 0
type_errors = 0
linting_violations = 0
violations_total = syntax_errors + type_errors + linting_violations
```

##### Phase 5B: Quality Gates Execution (MANDATORY)
```python
# Run quality gates verification
result = subprocess.run([
    'bash', '-c',
    'echo \'{"subagent": "agent-name", "self_check": true}\' | python3 ~/.claude/hooks/spark_quality_gates.py'
], capture_output=True, text=True)

if "Quality gates PASSED" in result.stdout:
    print("✅ Quality gates PASSED. Task completed successfully.")
else:
    print("🚫 Quality gates FAILED. Please fix violations and retry.")
```

## 📊 Quality Gates System

### 8-Step Verification Protocol

All agents must report zero violations:

1. **Architecture**: imports=0, circular=0, domain=0
2. **Foundation**: syntax=0, types=0
3. **Standards**: formatting=0, conventions=0
4. **Operations**: logging=0, security=0, config=0
5. **Quality**: linting=0, complexity=0
6. **Testing**: coverage≥95% (or -1 if N/A)
7. **Documentation**: docstrings=0, readme=0
8. **Integration**: final=0

### JSON State Management

```json
{
  "id": "spark_20250118_190418",
  "version": "4.1",
  "task": {
    "prompt": "user request",
    "execution_mode": "single|pipeline|parallel"
  },
  "state": {
    "current_agent": "agent-name",
    "status": "pending|running|completed|failed"
  },
  "quality": {
    "violations_total": 0,
    "can_proceed": true
  }
}
```

## 🎯 Agent Specializations

### Primary Agents (16)

| Agent | Specialization | Key Traits |
|-------|---------------|------------|
| **analyzer-spark** | Multi-dimensional system analysis | 시스템_사고, 분석적_추론, 증거_기반 |
| **implementer-spark** | Feature implementation | 체계적_실행, 단순성_우선, 구조적_무결성 |
| **tester-spark** | Comprehensive testing | 꼼꼼함, 분석적_추론, 회의주의 |
| **designer-spark** | System architecture | 장기적_사고, 추상화, 시스템_사고 |
| **documenter-spark** | Technical documentation | 명확한_의사소통, 지식_구조화, 공감 |
| **improver-spark** | Code quality enhancement | 근본_원인_분석, 반복적_개선 |
| **troubleshooter-spark** | Root cause analysis | 분석적_추론, 증거_기반, 체계적 |
| **cleaner-spark** | Technical debt elimination | 단순성_추구, 체계적_정리 |
| **explainer-spark** | Educational content | 명확한_의사소통, 개념_단순화 |
| **builder-spark** | Build system optimization | 자동화_마인드, 최적화 |
| **estimater-spark** | Project estimation | 분석적_추론, 증거_기반 |
| **gitter-spark** | Git workflow management | 시스템_사고, 팀_협업 |
| **spawner-spark** | Multi-agent orchestration | 시스템_사고, 자원_관리 |
| **loader-spark** | Project onboarding | 분석적_탐색, 패턴_인식 |
| **indexer-spark** | Command discovery | 지식_구조화, 문제_해결 |
| **tasker-spark** | Project management | 장기적_계획, 우선순위 |

### Team Agents (12)

- **team[1-4]-implementer-spark**: Parallel implementation
- **team[1-4]-tester-spark**: Parallel testing
- **team[1-4]-documenter-spark**: Parallel documentation

## 🚨 Critical Rules

### For 2호 (Claude Code)
1. **ONLY 2호 can use Task tool** - Agents cannot call other agents
2. **Parallel calls must be simultaneous** - All Task calls in ONE message
3. **Always check JSON state** - Verify quality gates before proceeding
4. **Maximum 3 retries** - Then report failure

### For Agents
1. **Phase 5B is MANDATORY** - All agents must execute quality gates
2. **Check for English messages** - "Quality gates PASSED" or "FAILED"
3. **Update JSON properly** - Record actual metrics, not fake values
4. **Exit on success only** - Don't exit if quality gates fail

## 💡 Token Management

### Safety Limits
- **Hard limit**: 200K tokens per agent
- **Practical limit**: 90K tokens (safety margin)
- **Write operations**: Double token consumption
- **Compression**: 30-50% reduction available

### Token Budget by Agent Type
- **Smallest**: Team agents (~1K tokens)
- **Average**: ~2.4K tokens
- **Largest**: implementer-spark (~3.9K tokens)

## 🔑 Success Patterns

### Effective Command Usage
```bash
# Good: Specific, clear scope
/spark-implement "user authentication with JWT"

# Better: With context
/spark-test "auth module with 95% coverage requirement"

# Best: Complete specification
/multi-implement "backend:auth,frontend:login,api:endpoints,db:schema"
```

### Quality Assurance
- All violations must be 0
- Coverage must be ≥95% for testing
- Documentation must be complete
- Security checks must pass

## 📈 Performance Metrics

- **Token Efficiency**: 95.5% reduction
- **Parallel Speedup**: 4x for multi-team
- **Quality Gates**: 8-step verification
- **Success Rate**: 98%+ with proper usage

## 🛠️ Troubleshooting

### Common Issues

1. **Quality gates failing**
   - Check actual violations in JSON
   - Ensure agent ran Phase 5B
   - Verify script is accessible

2. **Parallel execution not working**
   - Must call all agents in ONE message
   - Use team-specific agent names
   - Wait for ALL before proceeding

3. **Token limit exceeded**
   - Use compression strategies
   - Break into smaller tasks
   - Check file sizes before reading

## 📚 Additional Resources

- **Phase Structure**: See agent files in `.claude/agents/`
- **Quality Gates**: `.claude/hooks/spark_quality_gates.py`
- **Commands**: `.claude/commands/`
- **JSON States**: `.claude/workflows/`

---

*SPARK v4.1 - Production Ready*
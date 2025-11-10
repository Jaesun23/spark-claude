# Multi-Session Architecture for SPARK Agents
**Document Date**: 2025-09-05 15:07 KST  
**Context**: Discussion on evolving analyzer-spark and similar agents from single-shot to multi-session strategic tools

## Executive Summary

This document captures the architectural evolution from "analyze everything at once" to a **progressive, multi-session approach** for SPARK agents dealing with large-scale operations. The core insight: agents should act as strategic planners who can persist state between sessions, enabling them to tackle projects that exceed token limits through intelligent decomposition and progressive execution.

---

## 1. The Problem: Token Limits vs Reality

### Current Limitation
- **Agent Token Limit**: 90K tokens (safety margin from 200K hard limit)
- **Reality**: Modern codebases often contain 500K-2M+ tokens of content
- **Current Approach**: Try to analyze everything → Fail or produce shallow results

### The Warehouse Worker Analogy (from Jason)
> "창고 직원이 한 번에 모든 물건을 실어 나르려 하면 실패한다. 전문가라면 전략적으로 여러 번 나눠서 옮긴다."
> 
> (A warehouse worker who tries to carry everything at once will fail. A professional strategically divides the work across multiple trips.)

This perfectly captures why agents need multi-session capability.

---

## 2. The Solution: Progressive Multi-Session Architecture

### Core Concept
Instead of attempting complete analysis in one session, agents should:

1. **Session 1**: Strategic overview and planning
2. **Session 2-N**: Deep dive into specific areas
3. **Final Session**: Integration and synthesis

### State Persistence Mechanism

```yaml
# ~/.claude/workflows/analyze_state.yaml
analysis_id: "analyzer_20250905_140000"
version: "4.2"
sessions_completed: 3

analysis_state:
  progress:
    overall_percentage: 65
    phases_completed: ["discovery", "architecture", "critical_paths"]
    phases_remaining: ["performance", "security", "recommendations"]
    
  codebase_map:
    total_files: 1247
    analyzed_deeply: 412
    analyzed_surface: 835
    
  findings:
    critical_issues: 3
    improvement_areas: 17
    technical_debt_score: 6.5
    
  next_session:
    priority: "performance_analysis"
    focus_areas: 
      - "src/core/processing/*.py"
      - "src/api/endpoints/*.py"
    estimated_tokens: 45000
    recommended_sampling: "progressive_deep"
    
  context_for_next:
    key_insights: |
      - Payment module has circular dependencies
      - Auth system needs rate limiting
      - Database queries lack proper indexing
    areas_of_concern: |
      - Performance bottleneck in data processing
      - Security gaps in API authentication
```

### Token Sampling Strategies

#### 1. Progressive Sampling
```python
def progressive_sampling(codebase, session_num):
    """각 세션마다 다른 영역을 깊이 분석"""
    if session_num == 1:
        # Overview: 모든 파일의 첫 100줄씩
        return sample_headers(codebase, lines=100)
    elif session_num == 2:
        # Core logic: 핵심 모듈 전체
        return sample_core_modules(codebase)
    elif session_num == 3:
        # Integration points: API와 인터페이스
        return sample_interfaces(codebase)
```

#### 2. Smart Sampling
```python
def smart_sampling(file_content, token_limit):
    """파일 구조를 이해하고 중요 부분 우선 샘플링"""
    sections = {
        'imports': extract_imports(file_content),        # 10% tokens
        'class_definitions': extract_classes(file_content), # 30% tokens
        'critical_functions': extract_key_functions(file_content), # 40% tokens
        'test_coverage': extract_tests(file_content)     # 20% tokens
    }
    return fit_to_token_limit(sections, token_limit)
```

#### 3. Hierarchical Sampling
```python
def hierarchical_sampling(project_structure):
    """프로젝트 구조를 계층적으로 이해"""
    return {
        'level_1': get_directory_structure(),      # 5K tokens
        'level_2': get_file_summaries(),          # 20K tokens  
        'level_3': get_critical_implementations(), # 40K tokens
        'level_4': get_detailed_analysis()        # 25K tokens
    }
```

---

## 3. Implementation Pattern for Multi-Session Agents

### Phase Structure Enhancement

```python
class MultiSessionAgent:
    def __init__(self):
        self.state_file = "~/.claude/workflows/{agent}_state.yaml"
        
    def phase_0_enhanced(self):
        """Enhanced initialization with state recovery"""
        if os.path.exists(self.state_file):
            self.state = load_state(self.state_file)
            print(f"📂 Resuming from session {self.state['sessions_completed'] + 1}")
            print(f"📊 Previous progress: {self.state['progress']['overall_percentage']}%")
        else:
            self.state = initialize_new_analysis()
            print("🆕 Starting fresh analysis")
            
    def phase_5_enhanced(self):
        """Enhanced completion with state persistence"""
        self.state['sessions_completed'] += 1
        self.state['progress']['overall_percentage'] = calculate_progress()
        
        if self.is_complete():
            print("✅ Analysis complete across all sessions!")
            generate_final_report()
        else:
            save_state(self.state_file, self.state)
            print(f"💾 State saved. Resume with: /spark-analyze --continue")
            print(f"📍 Next priority: {self.state['next_session']['priority']}")
```

### 2호 Orchestration Protocol

```typescript
class MultiSessionOrchestration {
  async executeMultiSessionAgent(agent: string, request: string): Promise<void> {
    // Check for existing state
    const stateFile = `~/.claude/workflows/${agent}_state.yaml`;
    const hasState = await this.fileExists(stateFile);
    
    if (hasState) {
      const state = await this.loadState(stateFile);
      console.log(`📂 이전 세션 이어서 진행 (진행률: ${state.progress.overall_percentage}%)`);
      
      // Provide context to agent
      await Task(agent, `
        ${request}
        
        PREVIOUS STATE AVAILABLE:
        - Sessions completed: ${state.sessions_completed}
        - Progress: ${state.progress.overall_percentage}%
        - Next priority: ${state.next_session.priority}
        
        Continue from saved state.
      `);
    } else {
      console.log("🆕 새로운 멀티세션 작업 시작");
      await Task(agent, request);
    }
    
    // After completion, check if more sessions needed
    const newState = await this.loadState(stateFile);
    if (newState.progress.overall_percentage < 100) {
      console.log(`
        📊 진행 상황: ${newState.progress.overall_percentage}%
        💡 다음 세션: ${newState.next_session.priority}
        
        계속하려면: /spark-analyze --continue
      `);
    }
  }
}
```

---

## 4. Agents Requiring Multi-Session Architecture

Based on our discussion, these agents would benefit from multi-session capability:

### Tier 1: Critical Multi-Session Agents
1. **analyzer-spark**: Large codebase analysis
2. **loader-spark**: Project understanding and onboarding  
3. **tasker-spark**: Long-term project management
4. **documenter-spark**: Comprehensive documentation generation
5. **migrator components**: Large-scale migrations

### Tier 2: Beneficial Multi-Session Agents
1. **improver-spark**: Incremental refactoring
2. **cleaner-spark**: Progressive cleanup
3. **builder-spark**: Complex build optimizations
4. **tester-spark**: Comprehensive test coverage

### Key Characteristics for Multi-Session Agents
- Handle large-scale operations (>90K tokens)
- Benefit from progressive/incremental approach
- Need to maintain context across sessions
- Produce cumulative results

---

## 5. Benefits of Multi-Session Architecture

### 1. **Complete Coverage**
- No longer limited by token constraints
- Can analyze 500K+ token codebases thoroughly
- Deep analysis instead of surface scanning

### 2. **Strategic Planning**
- Agents become strategic planners, not just executors
- Can prioritize based on discovered insights
- Adaptive approach based on findings

### 3. **Progressive Enhancement**
- Each session builds on previous insights
- Can adjust strategy based on discoveries
- Cumulative knowledge growth

### 4. **User Control**
- Users can review intermediate results
- Can redirect focus based on findings
- Stop when sufficient insights gained

### 5. **Resource Efficiency**
- Distribute heavy analysis across time
- Avoid token limit crashes
- Focus compute on high-value areas

---

## 6. State Document Design Principles

### Machine-Readable Format (YAML/JSON)
```yaml
# Why YAML?
# - Human-readable for Jason and 2호
# - Machine-parseable for agents
# - Supports complex nested structures
# - Comments for context

meta:
  format_version: "1.0"
  agent: "analyzer-spark"
  created: "2025-09-05T14:00:00"
  
# Clear sections for different consumers
for_next_agent:
  # Critical information for continuation
  must_know: []
  should_review: []
  can_skip: []
  
for_orchestrator:
  # Information for 2호
  estimated_remaining_sessions: 3
  next_session_strategy: "deep_dive"
  
for_user:
  # Human-readable summary
  key_findings: "..."
  recommendations: "..."
```

### Standardized Schema
All multi-session agents should use consistent state structure:
- `meta`: Metadata about the analysis
- `progress`: Quantitative progress tracking
- `findings`: Accumulated insights
- `next_session`: Planning for continuation
- `context_for_next`: Qualitative knowledge transfer

---

## 7. Example: Analyzer-Spark Multi-Session Flow

### Session 1: Strategic Overview (30K tokens)
```bash
/spark-analyze "전체 프로젝트 구조 파악"

# Agent response:
📊 전략적 분석 시작...
- 1,247개 파일 발견
- 주요 모듈 15개 식별
- 예상 총 분석 시간: 4 세션

💾 State saved: analyzer_20250905_140000
📍 Next priority: Core business logic (Session 2)
```

### Session 2: Core Logic Deep Dive (85K tokens)
```bash
/spark-analyze --continue

# Agent response:
📂 이전 분석 계속 (Session 2/4)
🎯 Focus: Core business logic
- Payment module: 3 critical issues found
- Auth system: Security gaps identified

💾 Progress: 45% complete
📍 Next: API and integration analysis
```

### Session 3: Integration Analysis (70K tokens)
```bash
/spark-analyze --continue

# Agent response:
📂 Session 3/4
🔗 Integration point analysis
- 23 API endpoints analyzed
- 5 external service integrations reviewed

💾 Progress: 75% complete
📍 Next: Performance and optimization opportunities
```

### Session 4: Synthesis and Recommendations (40K tokens)
```bash
/spark-analyze --continue

# Agent response:
📂 Final session (4/4)
✅ Analysis complete!

📊 Final Report:
- Total coverage: 100%
- Critical issues: 7
- Improvement opportunities: 34
- Estimated technical debt: 127 hours

📄 Full report saved: analysis_report_20250905.md
```

---

## 8. Integration with 2호 (Orchestrator Enhancement)

### Required CLAUDE.md Addition

```markdown
## Multi-Session Agent Support

Some SPARK agents support multi-session execution for large-scale operations:

### Identifying Multi-Session Agents
- Check for state files in ~/.claude/workflows/*_state.yaml
- Agents will indicate if continuation is needed
- Progress percentage shows completion status

### Orchestration Protocol
1. **Initial Execution**: Run agent normally
2. **Check State**: If state file exists, agent may need continuation
3. **Continue**: Use --continue flag or re-run command
4. **Monitor Progress**: Track percentage and session count
5. **Completion**: Agent indicates when fully complete

### Supported Multi-Session Agents
- analyzer-spark: Large codebase analysis
- loader-spark: Project understanding
- tasker-spark: Project management
- documenter-spark: Documentation generation

### State Preservation
- States are preserved in YAML files
- Can be reviewed by Jason or 2호
- Agents automatically resume from saved state
```

---

## 9. Conclusion and Next Steps

### Key Insights from Discussion
1. **Professional analysts work strategically**, not exhaustively in one pass
2. **State persistence enables complex multi-session work**
3. **Token sampling strategies** allow deep analysis within limits
4. **2호 needs awareness** of multi-session patterns for proper orchestration

### Implementation Priority
1. **First**: Update analyzer-spark with multi-session capability
2. **Second**: Apply pattern to loader-spark and tasker-spark  
3. **Third**: Update 2호 CLAUDE.md with orchestration protocol
4. **Fourth**: Extend to other qualifying agents

### Success Metrics
- ✅ Can analyze 500K+ token codebases
- ✅ Strategic planning visible in state documents
- ✅ Progressive enhancement across sessions
- ✅ 2호 properly orchestrates multi-session work
- ✅ Users understand and control the process

---

## Appendix: State File Examples

### analyzer_state.yaml
```yaml
# Comprehensive analysis state example
# See Section 2 for detailed structure
```

### loader_state.yaml
```yaml
# Project understanding state
loader_id: "loader_20250905_150000"
sessions: 2
understanding:
  architecture_mapped: true
  dependencies_analyzed: true
  entry_points_identified: true
next_focus: "test_coverage_analysis"
```

### tasker_state.yaml
```yaml
# Project management state
project_id: "biotech_platform"
total_tasks: 127
completed_tasks: 45
current_sprint: 3
next_priorities: ["auth_implementation", "api_documentation"]
```

---

**End of Document**

*This document serves as both a record of our discussion and a blueprint for implementing multi-session architecture across SPARK agents. The pattern enables agents to handle real-world, large-scale projects that exceed token limits through intelligent state management and progressive execution.*





멀티세션 에이전트들은 주어진 문제를 몇 번으로 나눠서 작업을 해야 완전한 결과 보고를 할 수 있을 지 판단하고, 계획, 초기 탐색 후 다음 세션을 위한 
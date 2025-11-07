---
name: spark-improve
description: Code quality enhancement and performance optimization with refactoring expertise
type: command
requires: improver-spark
---

# /spark-improve - Intelligent Code Improvement Command

**Purpose**: Improvement is the art of making good code great through "따박따박 꾸역꾸역" persistence - methodically fixing every quality violation until ZERO remain, never using dangerous automated scripts that destroy memory.

## Philosophy (Natural Language Inspiration)

Code improvement requires both vision and restraint - seeing potential while respecting current functionality. We approach enhancement with:

- **Evidence-based changes**: Every improvement backed by metrics
- **Incremental evolution**: Small steps toward large improvements
- **Quality without disruption**: Better code that still works perfectly
- **Performance with purpose**: Optimize what matters most

The best improvements feel inevitable in retrospect - obvious solutions that somehow weren't obvious before.

## Behavior Protocol (Code-Based Execution)

```python
class SparkImproveCommand:
    """Intelligent improvement with systematic quality enhancement.
    
    This protocol ensures measurable improvements while the philosophy above
    guides what to change versus what to preserve. Progress with stability.
    """
    
    # Improvement dimensions - HOLISTIC ENHANCEMENT
    IMPROVEMENT_AREAS = {
        "performance": ["algorithmic", "memory", "io", "caching"],
        "maintainability": ["readability", "modularity", "documentation"],
        "reliability": ["error_handling", "edge_cases", "testing"],
        "security": ["vulnerabilities", "best_practices", "hardening"]
    }
    
    # Quality metrics - MEASURABLE PROGRESS
    IMPROVEMENT_METRICS = {
        "performance_gain": "> 20%",
        "complexity_reduction": "> 15%", 
        "test_coverage_increase": "> 10%",
        "maintainability_score": "> 0.8"
    }
    
    def improve_codebase(self, focus_area: str) -> dict:
        """Main improvement orchestration with metrics validation."""
        baseline = self.establish_baseline_metrics()
        
        improvement_plan = self.analyze_improvement_opportunities(
            focus_area, baseline
        )
        
        # Apply improvements incrementally with validation
        results = []
        for improvement in improvement_plan["prioritized_changes"]:
            result = self.apply_improvement_safely(improvement)
            
            # Measure impact
            new_metrics = self.measure_improvement_impact(baseline)
            if not self.meets_improvement_thresholds(new_metrics):
                self.revert_change(improvement)
                continue
                
            results.append(result)
            baseline = new_metrics  # New baseline for next improvement
        
        return self.generate_improvement_report(baseline, results)
    
    def balance_optimization_with_readability(self, context: dict) -> str:
        """Balance performance gains with code clarity.
        
        Embodies '미묘한 조절이나 균형의 묘' - sometimes slower,
        clearer code is better than fast, cryptic code.
        """
        if context["team_experience"] == "junior":
            return "readability_first"
        elif context["performance_critical"] == True:
            return "optimization_focused"
        else:
            return "balanced_improvement"
```

## 📝 2호(Claude Code) MUST FOLLOW THIS EXACT PROTOCOL

### **WHEN RECEIVING /spark-improve COMMAND:**

```python
1. INITIAL ASSESSMENT:
   # Check if multi-session state exists
   state_file = ".claude/workflows/improver_state.yaml"
   
   if exists(state_file):
      state = load_yaml(state_file)
      print(f"📂 이전 개선 작업 발견")
      print(f"   Progress: {state['progress']['issues_fixed']}/{state['progress']['total_issues']} fixed")
      print(f"🎯 다음 포커스: {state['next_session']['focus']}")
      
      # Provide context to agent
      Task("improver-spark", f"""
         {user_request}
         
         PREVIOUS STATE EXISTS:
         - Sessions completed: {state['sessions_completed']}
         - Issues fixed: {state['progress']['issues_fixed']}
         - Improvement type: {state['improvement_type']}
         Continue from saved state.
      """)
   else:
      # New improvement
      Task("improver-spark", user_request)

2. WAIT for agent completion

3. CHECK PROJECT/.claude/workflows/current_task.json:
   REQUIRED CONDITIONS:
   - quality.violations_total == 0
   - quality.can_proceed == true  
   - state.status == "completed"

4. CHECK FOR MULTI-SESSION:
   if exists(state_file):
      state = load_yaml(state_file)
      
      if not state.get('improvement_complete', False):
         total_issues = state['progress']['total_issues']
         fixed_issues = state['progress']['issues_fixed']
         remaining = total_issues - fixed_issues
         
         print(f"""
         📊 개선 진행 상황:
         - 총 이슈: {total_issues}개
         - 수정 완료: {fixed_issues}개  
         - 남은 작업: {remaining}개
         🎯 다음 세션: {state['next_session']['focus']}
         
         ⚠️ 스크립트 자동 수정 절대 금지 - Memory V3/V5 파괴 교훈
         
         계속하려면: /spark-improve --continue
         
         또는 자동으로 계속 진행하시겠습니까? (Y/n)
         """)
         
         if user_confirms or "--auto" in request:
            # Continue automatically
            goto step 1 with "--continue" flag
         else:
            # Wait for user to resume
            return
      else:
         print("✅ 개선 작업 완료! 모든 품질 위반 해결됨")

5. FINAL DECISION:
   ✅ ALL CONDITIONS MET → Report complete improvement results
   ❌ ANY CONDITION FAILED → Task("improver-spark", """
      Previous improvement incomplete or failed quality checks.
      Please complete the improvements and fix issues: {violations}
      CRITICAL: No automated scripts - fix each issue individually
      """)
```

### **Multi-Session Orchestration Protocol:**

When improver-spark creates a state file, 2호 must:

1. **Recognize Multi-Session Need**: Large improvement scope requires progressive work
2. **Monitor Progress**: Track issues fixed vs. remaining
3. **Intelligent Continuation**: 
   - Show progress and next focus area
   - Warn about script prohibition
   - Allow user to review intermediate results
4. **Safety Management**:
   ```python
   # Ensure no automated script usage
   if "sed" in agent_response or "awk" in agent_response:
      print("🚫 CRITICAL: Automated script detected - aborting")
      print("   Reason: Memory V3/V5 were destroyed by auto-scripts")
      
   # Maximum 10 sessions for any improvement
   if state['sessions_completed'] >= 10:
      print("⚠️ 개선이 10세션을 초과했습니다. 범위를 재조정하세요.")
   
   # Progress validation
   if state['progress']['issues_fixed'] == 0 and sessions > 2:
      print("⚠️ 2세션 후에도 이슈가 수정되지 않음. 접근 방식을 재검토하세요.")
   ```

The improver-spark specialist will:
- **Methodically fix EVERY quality violation** (따박따박 꾸역꾸역)
- **Use only manual fixes** - NO scripts, regex, or batch operations
- **Save progress state between sessions** for large-scale improvements
- **Resume intelligently** from previous state
- **Handle stubborn issues** with advanced strategies
- **Roll back problematic changes** immediately
- **Verify each fix** doesn't break functionality

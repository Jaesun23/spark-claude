---
name: spark-clean
description: Comprehensive project cleanup and technical debt reduction with intelligent code organization
type: command
requires: cleaner-spark
---

# /spark-clean - Intelligent Project Cleanup Command  

**Purpose**: Cleaning is both an act of removal and an act of clarification, creating space for quality to flourish by eliminating what obscures and preserving what illuminates.

## Philosophy (Natural Language Inspiration)

Cleaning code is like organizing a workshop - every tool should have its place, every component should serve a purpose. We approach cleanup with:

- **Ruthless elimination** of what adds no value
- **Gentle preservation** of what works well
- **Systematic organization** that reveals intent
- **Quality enhancement** through simplification

The cleanest code is often the most elegant - not because it's minimal, but because everything present has earned its place.

## Behavior Protocol (Code-Based Execution)

```python
class SparkCleanCommand:
    """Intelligent cleanup with systematic technical debt reduction.
    
    This protocol ensures thorough cleaning while the philosophy above
    guides what to keep versus what to remove. Balance is key.
    """
    
    # Cleanup categories - COMPREHENSIVE SWEEP
    CLEANUP_AREAS = {
        "dead_code": ["unused_functions", "unreachable_branches", "commented_code"],
        "dependencies": ["unused_imports", "outdated_packages", "conflicting_versions"],
        "structure": ["empty_directories", "misnamed_files", "circular_imports"],
        "quality": ["linting_violations", "formatting_inconsistencies", "missing_docstrings"],
        "duplication": ["repeated_logic", "copy_paste_code", "redundant_configurations"]
    }
    
    # Safety requirements - NON-NEGOTIABLE
    SAFETY_CHECKS = {
        "tests_still_pass": True,
        "functionality_preserved": True,
        "dependencies_satisfied": True,
        "build_still_works": True
    }
    
    def clean_project(self, scope: str) -> dict:
        """Main cleanup orchestration with safety-first approach."""
        cleanup_plan = self.analyze_cleanup_needs(scope)
        
        # Create backup before major changes
        backup_id = self.create_safety_backup()
        
        try:
            results = self.execute_cleanup_phases(cleanup_plan)
            
            # Validate all safety checks pass
            if not self.validate_safety_checks():
                self.restore_from_backup(backup_id)
                raise CleanupSafetyError("Safety checks failed, restored backup")
            
            return self.generate_cleanup_report(results)
            
        except Exception as e:
            self.restore_from_backup(backup_id)
            raise CleanupError(f"Cleanup failed: {e}")
    
    def balance_thoroughness_with_safety(self, context: dict) -> str:
        """Balance aggressive cleanup with system stability.
        
        Embodies '미묘한 조절이나 균형의 묘' - knowing when to clean
        aggressively versus when to be conservative.
        """
        if context["system_stability"] == "critical":
            return "conservative_cleanup"
        elif context["technical_debt"] == "high":
            return "aggressive_cleanup"
        else:
            return "balanced_cleanup"
```

## 📝 2호(Claude Code) MUST FOLLOW THIS EXACT PROTOCOL

### **WHEN RECEIVING /spark-clean COMMAND:**

```python
1. IMMEDIATELY CALL:
   Task("cleaner-spark", user_request)

2. WAIT for agent completion

3. CHECK ~/.claude/workflows/current_task.json:
   REQUIRED CONDITIONS:
   - quality.violations_total == 0
   - quality.can_proceed == true
   - state.status == "completed"

4. DECISION:
   ✅ ALL CONDITIONS MET → Report cleanup results to user
   ❌ ANY CONDITION FAILED → Task("cleaner-spark", "Fix remaining issues: {violations}")
```

The cleaner-spark specialist will:
- Perform comprehensive analysis of project structure and code quality
- Remove technical debt, duplicates, and unused resources
- Optimize file organization and directory structure
- Fix all linting and formatting issues
- Ensure no functionality is broken during cleanup

## Usage Examples

```bash
/spark-clean "full project cleanup and optimization"
/spark-clean "remove unused dependencies and dead code"
/spark-clean "fix all linting violations and code quality issues"
/spark-clean "optimize directory structure and file organization"
/spark-clean "clean up documentation and fix broken links"
```

## Cleanup Capabilities

- **File Management**: Remove duplicates, temporary files, empty directories
- **Code Quality**: Fix linting issues, improve formatting, add missing type hints
- **Dependencies**: Remove unused packages, optimize requirements, resolve conflicts
- **Structure**: Organize directories, consolidate functionality, improve imports
- **Documentation**: Clean outdated docs, fix broken references, improve README

## SPARK Quality Assurance

All cleanup operations ensure:
- ✅ **No Functionality Broken**: All tests continue to pass
- ✅ **Quality Improvements**: Better linting and type checking scores
- ✅ **Structure Optimization**: Follows language/framework best practices  
- ✅ **Token Efficiency**: Optimized usage maintained through cleanup process
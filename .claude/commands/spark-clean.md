# /spark-clean - SPARK Project Cleanup Command  

**Purpose**: Comprehensive project cleanup and technical debt reduction with SPARK intelligence

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
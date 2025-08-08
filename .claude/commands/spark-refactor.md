# /spark-refactor - SPARK Multi-Agent Refactoring Pipeline

**Purpose**: Complete code refactoring with analysis, improvement, testing, and documentation

## Execution Instructions

When this command is called, execute the following multi-agent pipeline:

```
1. First, use the Task tool with subagent_type "analyzer-spark" to analyze the current codebase.
   Pass "Analyze code structure, identify refactoring opportunities, technical debt, and improvement areas" as the prompt.

2. After analysis completes, use the Task tool with subagent_type "improver-spark" 
   to implement the refactoring based on analysis results.
   Pass "Refactor the code based on the previous analysis findings, focusing on maintainability and performance" as the prompt.

3. After refactoring completes, use the Task tool with subagent_type "tester-spark"
   to ensure all functionality still works with comprehensive testing.
   Pass "Create and run comprehensive tests to verify refactored code maintains all functionality with 95%+ coverage" as the prompt.

4. Finally, use the Task tool with subagent_type "documenter-spark" 
   to update documentation reflecting the new structure.
   Pass "Update all documentation, README, and code comments to reflect the refactored architecture" as the prompt.
```

## Usage Examples

```bash
/spark-refactor "refactor authentication module for better maintainability"
/spark-refactor "modernize legacy API endpoints to follow REST standards"
/spark-refactor "optimize database queries and improve performance"
/spark-refactor "restructure component hierarchy for better reusability"
```

## Pipeline Benefits

- **Deep Analysis**: Complete codebase assessment before changes
- **Smart Improvements**: Evidence-based refactoring decisions
- **Quality Assurance**: Comprehensive testing ensures no regressions
- **Updated Documentation**: All docs stay in sync with changes
- **SPARK Efficiency**: 4-agent pipeline with 88.4% token efficiency

## Expected Outcome

1. **Analysis Report**: Detailed findings and refactoring plan
2. **Improved Code**: Cleaner, more maintainable implementation
3. **Test Suite**: Comprehensive tests validating all functionality
4. **Fresh Documentation**: Updated guides and API docs
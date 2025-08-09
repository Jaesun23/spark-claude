# /smart-implement

When Jason uses this command with arguments, execute the following 3-phase workflow:

## Command Pattern
```
/smart-implement [TASK_DESCRIPTION]
```

## Execution Workflow

When this command is invoked with $ARGUMENTS:

### Phase 1: Analysis
```python
# Call analyzer-spark
Task(
    description="Analyze for implementation",
    prompt=f"""
    Analyze the current codebase for implementing: {$ARGUMENTS}
    
    1. Scan all relevant files and systems
    2. Identify existing patterns and dependencies  
    3. Find potential impact areas
    4. Check for similar implementations
    5. Document technical constraints
    
    Create analysis report at: docs/analysis/{{timestamp}}_implementation_analysis.md
    
    Focus on providing actionable insights for the design phase.
    """,
    subagent_type="analyzer-spark"
)
```

### Phase 2: Design
```python
# Call designer-spark with analysis results
Task(
    description="Design implementation plan", 
    prompt=f"""
    Based on the analysis report, design the implementation for: {$ARGUMENTS}
    
    1. Read the latest analysis report from docs/analysis/
    2. Create detailed architecture design
    3. Define interfaces and contracts
    4. Plan implementation steps
    5. Specify test strategies
    
    Create design document at: docs/architecture/{{timestamp}}_implementation_design.md
    
    The design should be detailed enough for implementation without ambiguity.
    """,
    subagent_type="designer-spark"
)
```

### Phase 3: Implementation
```python
# Call implementer-spark with design document
Task(
    description="Implement based on design",
    prompt=f"""
    Implement the solution for: {$ARGUMENTS}
    
    1. Read the latest design document from docs/architecture/
    2. Follow the implementation plan exactly
    3. Write production-quality code
    4. Add comprehensive tests (95%+ coverage)
    5. Create/update documentation
    
    Apply all 8 quality gates:
    - Architecture validation
    - Type checking
    - Linting
    - Test coverage
    - Performance benchmarks
    - Security scanning
    - Documentation completeness
    - Code review standards
    
    Report implementation completion with file paths created/modified.
    """,
    subagent_type="implementer-spark"
)
```

## Execution Notes

- Execute phases sequentially (not in parallel)
- Each phase depends on the previous phase's output
- Pass $ARGUMENTS to each agent for context
- Ensure Documentation Standards v1.2 compliance for all documents
- Report progress after each phase completion

## Error Handling

If any phase fails:
- Stop the workflow
- Report which phase failed and why
- Ask Jason whether to retry or abort

## Example Invocations

When Jason says:
- `/smart-implement Add Redis caching with TTL refresh`
- `/smart-implement Implement OAuth2.0 authentication`
- `/smart-implement Create batch processing system`

Execute all three phases with the provided task description as $ARGUMENTS.
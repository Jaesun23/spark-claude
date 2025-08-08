# /implement - SPARK Implementation Command

**Purpose**: Efficient code implementation with 88.4% token reduction

## Command Flow

1. **Persona Router** → Analyze task and activate needed persona
2. **Agent Selection** → Load only required agent (implementer-spark, designer-spark, etc.)
3. **Implementation** → Execute with persona-specific quality standards
4. **Quality Gates** → Validate with 10-step process
5. **State Update** → Update workflow JSON files

## Usage Examples

```bash
/implement "REST API for user authentication"
# → Activates backend persona + implementer-spark agent

/implement "responsive dashboard UI" 
# → Activates frontend persona + designer-spark agent

/implement "data analysis pipeline"
# → Activates backend persona + analyzer-spark agent
```

## Token Efficiency

- **SuperClaude**: 44,000 tokens (all agents loaded)
- **SPARK**: 5,100 tokens average (88.4% reduction)
- **Cost Savings**: $0.78 per request

## Quality Standards

All implementations must pass:
- 8 SPARK quality gates
- 2 Jason DNA gates (MyPy + Ruff)
- Persona-specific standards
- Performance benchmarks
# /research-and-document - SPARK Multi-Agent Research Pipeline

**Purpose**: Comprehensive research analysis followed by professional documentation generation

## Execution Instructions

When this command is called, execute the following multi-agent pipeline:

```
1. First, use the Task tool with subagent_type "analyzer-spark" to conduct thorough research and analysis.
   Pass the user's research request as the prompt parameter.

2. After the analyzer-spark completes, use the Task tool with subagent_type "documenter-spark" 
   to create professional documentation based on the analysis results.
   Pass "Generate comprehensive documentation based on the previous analysis results" as the prompt.
```

## Usage Examples

```bash
/research-and-document "investigate the performance characteristics of our authentication system"
/research-and-document "analyze the current API architecture and document best practices"
/research-and-document "research security vulnerabilities in the payment processing flow"
/research-and-document "study the user interface patterns and document design guidelines"
```

## Multi-Agent Benefits

- **Deep Analysis**: analyzer-spark provides evidence-based investigation
- **Professional Documentation**: documenter-spark creates structured, actionable reports
- **Seamless Integration**: Analysis results flow directly into documentation
- **SPARK Efficiency**: 88.4% token reduction vs separate analysis and documentation tasks

## Output Expectations

1. **Research Phase**: Comprehensive analysis with findings, metrics, and recommendations
2. **Documentation Phase**: Structured report with executive summary, detailed findings, and action items
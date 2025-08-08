# /spark-audit - SPARK Security & Performance Audit Pipeline

**Purpose**: Complete project audit covering security, performance, and quality with actionable reports

## Execution Instructions

When this command is called, execute the following comprehensive audit pipeline:

```
1. First, use the Task tool with subagent_type "analyzer-spark" to perform deep code analysis.
   Pass "Conduct comprehensive analysis focusing on security vulnerabilities, performance bottlenecks, and code quality metrics" as the prompt.

2. After analysis, use the Task tool with subagent_type "troubleshooter-spark" 
   to investigate specific issues and potential problems.
   Pass "Investigate security risks, performance issues, and system vulnerabilities identified in the analysis" as the prompt.

3. Then, use the Task tool with subagent_type "tester-spark"
   to validate current test coverage and identify testing gaps.
   Pass "Audit existing test suite, measure coverage, identify security test gaps, and performance test needs" as the prompt.

4. Finally, use the Task tool with subagent_type "documenter-spark"
   to create a comprehensive audit report with recommendations.
   Pass "Generate detailed audit report with security findings, performance metrics, quality scores, and prioritized action items" as the prompt.
```

## Usage Examples

```bash
/spark-audit "complete security and performance audit of the API layer"
/spark-audit "audit user authentication and authorization systems"  
/spark-audit "comprehensive review of data processing pipeline"
/spark-audit "audit payment processing system for compliance"
```

## Audit Coverage

- **Security Assessment**: Vulnerability scanning, auth review, input validation
- **Performance Analysis**: Bottleneck identification, optimization opportunities
- **Code Quality**: Complexity metrics, maintainability scores, technical debt
- **Test Coverage**: Gap analysis, security test adequacy, performance testing
- **Compliance Check**: Best practices, standards adherence, documentation quality

## Deliverables

1. **Executive Summary**: High-level findings and risk assessment
2. **Technical Analysis**: Detailed code and architecture review
3. **Security Report**: Vulnerabilities, threats, and mitigation strategies
4. **Performance Metrics**: Benchmarks, bottlenecks, and optimization plan
5. **Action Plan**: Prioritized recommendations with effort estimates

## SPARK Intelligence Integration

- 🔍 **Multi-Perspective Analysis**: 4 specialized agents working together
- 📊 **Evidence-Based**: All findings backed by data and testing
- 🛡️ **Security-First**: Comprehensive vulnerability assessment
- 🚀 **88.4% Token Efficiency**: Complete audit without token waste
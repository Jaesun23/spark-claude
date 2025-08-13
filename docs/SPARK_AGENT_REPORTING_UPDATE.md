# SPARK Agent Reporting Requirements Update

## 📋 Overview

All SPARK agents have been updated with **MANDATORY REPORTING REQUIREMENTS** to ensure comprehensive documentation of their work. Agents will no longer provide just summaries but complete, detailed reports.

## 🎯 Purpose

- **Problem**: Agents were only providing brief summaries instead of detailed reports
- **Solution**: Added mandatory reporting requirements to all agents
- **Benefit**: Complete visibility into agent work with comprehensive documentation

## 📁 Report Storage Location

All agent reports will be saved to:
```
/docs/agents-task/[agent-name]/[report-type]-[timestamp].md
```

## 📊 Updated Agents and Requirements

### Critical Analysis & Design Agents (Detailed Reports)

#### 1. **analyzer-spark**
- **Report**: `/docs/agents-task/analyzer-spark/analysis-report-[timestamp].md`
- **Minimum Size**: 500 lines
- **Contents**:
  - Complete system analysis with all findings
  - Evidence for each issue (file paths, line numbers, code snippets)
  - Complexity heatmap and metrics
  - Priority matrix (P0-P3)
  - Improvement roadmap

#### 2. **designer-spark**
- **Report**: `/docs/agents-task/designer-spark/design-doc-[timestamp].md`
- **Minimum Size**: 800 lines
- **Contents**:
  - Complete architecture diagrams (ASCII art)
  - Full API specifications
  - Detailed component designs
  - Complete data models
  - Implementation guidelines with code examples
  - Security considerations and threat model

#### 3. **documenter-spark**
- **Report**: `/docs/agents-task/documenter-spark/[type]-doc-[timestamp].md`
- **Minimum Size**: 400 lines
- **Contents**:
  - Complete API specifications
  - Full user guides
  - Detailed troubleshooting sections
  - Complete code examples
  - All configuration options

#### 4. **troubleshooter-spark**
- **Report**: `/docs/agents-task/troubleshooter-spark/investigation-[timestamp].md`
- **Minimum Size**: 300 lines
- **Contents**:
  - Complete timeline of events
  - All log entries analyzed
  - Every hypothesis tested with results
  - Full root cause analysis
  - Detailed remediation steps
  - Prevention measures

### Implementation & Testing Agents (Work Reports)

#### 5. **implementer-spark**
- **Report**: `/docs/agents-task/implementer-spark/implementation-report-[timestamp].md`
- **Minimum Size**: 200 lines
- **Contents**:
  - All implemented features with file paths
  - Code changes summary
  - Test coverage results
  - Performance benchmarks
  - Security validations

#### 6. **tester-spark**
- **Report**: `/docs/agents-task/tester-spark/test-report-[timestamp].md`
- **Minimum Size**: 300 lines
- **Contents**:
  - Complete test inventory
  - Coverage report by module
  - Test execution results with timings
  - Failed test analysis
  - Performance benchmarks

#### 7. **improver-spark**
- **Report**: `/docs/agents-task/improver-spark/improvement-report-[timestamp].md`
- **Minimum Size**: 250 lines
- **Contents**:
  - Before/after analysis
  - All improvements with locations
  - Performance comparisons
  - Security fixes
  - Refactoring rationale

#### 8. **cleaner-spark**
- **Report**: `/docs/agents-task/cleaner-spark/cleanup-report-[timestamp].md`
- **Minimum Size**: 200 lines
- **Contents**:
  - Technical debt inventory
  - Cleanup operations performed
  - Before/after metrics
  - Dependencies updated
  - Performance impact

### Management & Support Agents (Standard Reports)

#### 9. **builder-spark**
- **Report**: `/docs/agents-task/builder-spark/build-report-[timestamp].md`
- **Minimum Size**: 150 lines
- **Contents**:
  - Build configuration changes
  - Performance improvements
  - Bundle optimizations
  - CI/CD setup details

#### 10. **estimater-spark**
- **Report**: `/docs/agents-task/estimater-spark/estimation-report-[timestamp].md`
- **Minimum Size**: 200 lines
- **Contents**:
  - Work breakdown structure
  - 3-point estimates with rationale
  - Risk assessment
  - Resource allocation
  - Sprint planning

#### 11. **spawner-spark**
- **Report**: `/docs/agents-task/spawner-spark/orchestration-report-[timestamp].md`
- **Minimum Size**: 300 lines
- **Contents**:
  - Orchestration timeline
  - All subtasks with results
  - Coordination decisions
  - Performance metrics
  - Integration validation

#### 12. **tasker-spark**
- **Report**: `/docs/agents-task/tasker-spark/project-report-[timestamp].md`
- **Minimum Size**: 250 lines
- **Contents**:
  - Task hierarchy (epics/stories/tasks)
  - Resource allocation
  - Risk assessment
  - Progress tracking
  - Quality gate results

## 🔔 Agent Announcement Format

All agents MUST announce their report location clearly:

- analyzer-spark: "📊 Detailed analysis report saved to: /docs/agents-task/analyzer-spark/[filename].md"
- designer-spark: "🏗️ Complete design document saved to: /docs/agents-task/designer-spark/[filename].md"
- documenter-spark: "📚 Complete documentation saved to: /docs/agents-task/documenter-spark/[filename].md"
- troubleshooter-spark: "🔍 Investigation report saved to: /docs/agents-task/troubleshooter-spark/[filename].md"
- implementer-spark: "📋 Implementation report saved to: /docs/agents-task/implementer-spark/[filename].md"
- tester-spark: "🧪 Complete test report saved to: /docs/agents-task/tester-spark/[filename].md"
- improver-spark: "📈 Improvement report saved to: /docs/agents-task/improver-spark/[filename].md"
- cleaner-spark: "🧹 Cleanup report saved to: /docs/agents-task/cleaner-spark/[filename].md"

## ✅ Implementation Status

| Agent | Report Requirement | Min Lines | Status |
|-------|-------------------|-----------|--------|
| analyzer-spark | Detailed Analysis | 500 | ✅ Updated |
| designer-spark | Complete Design Doc | 800 | ✅ Updated |
| documenter-spark | Full Documentation | 400 | ✅ Updated |
| troubleshooter-spark | Investigation Report | 300 | ✅ Updated |
| implementer-spark | Implementation Report | 200 | ✅ Updated |
| tester-spark | Test Report | 300 | ✅ Updated |
| improver-spark | Improvement Report | 250 | ✅ Updated |
| cleaner-spark | Cleanup Report | 200 | ✅ Updated |
| builder-spark | Build Report | 150 | ✅ Updated |
| estimater-spark | Estimation Report | 200 | ✅ Updated |
| spawner-spark | Orchestration Report | 300 | ✅ Updated |
| tasker-spark | Project Report | 250 | ✅ Updated |

## 🚀 Testing Instructions

To test the new reporting requirements:

1. **Invoke an agent with a task**:
   ```bash
   # Example: Test analyzer-spark
   Task("analyzer-spark", "Analyze the /src directory for performance issues")
   ```

2. **Verify report generation**:
   - Agent should create report at specified location
   - Report should meet minimum line requirements
   - Agent should announce report location clearly

3. **Check report quality**:
   - Reports should be comprehensive, not summaries
   - All required sections should be present
   - Evidence and details should be included

## 📝 Notes for Jason

- All agents now have mandatory reporting requirements
- Reports are saved to organized directory structure
- Minimum line counts ensure comprehensive documentation
- Clear announcements help locate reports easily
- This addresses the issue of agents providing only summaries

## 🔄 Next Steps

1. Test each agent to verify report generation
2. Adjust minimum line requirements if needed
3. Consider adding report templates for consistency
4. Implement automated report validation in quality gates
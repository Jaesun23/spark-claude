# /spark-migrate - SPARK Legacy Migration & Modernization Pipeline  

**Purpose**: Comprehensive legacy system migration with risk assessment and modern implementation

## Execution Instructions

When this command is called, execute the following legacy migration pipeline:

```
1. First, use the Task tool with subagent_type "analyzer-spark" to analyze the legacy system.
   Pass "Analyze legacy codebase: identify dependencies, data structures, business logic, and migration challenges" as the prompt.

2. After analysis, use the Task tool with subagent_type "designer-spark"
   to design the modern replacement architecture.
   Pass "Design modern replacement system based on legacy analysis: new architecture, updated patterns, improved performance" as the prompt.

3. Then, use the Task tool with subagent_type "implementer-spark"
   to create migration tools and implement the modern system.
   Pass "Implement migration tools and modern replacement system with data migration scripts and compatibility layers" as the prompt.

4. Next, use the Task tool with subagent_type "tester-spark"
   to create comprehensive migration validation tests.
   Pass "Create migration validation tests: data integrity checks, functionality parity tests, and performance comparisons" as the prompt.

5. Finally, use the Task tool with subagent_type "documenter-spark"
   to create migration documentation and runbooks.
   Pass "Create complete migration documentation: runbooks, rollback procedures, troubleshooting guides, and training materials" as the prompt.
```

## Usage Examples

```bash
/spark-migrate "migrate PHP legacy system to modern Node.js architecture"
/spark-migrate "modernize jQuery frontend to React with TypeScript"
/spark-migrate "move from monolithic Rails app to microservices"
/spark-migrate "migrate SQL Server database to PostgreSQL with optimization"
/spark-migrate "convert legacy REST API to GraphQL with better performance"
```

## Migration Capabilities

- **Legacy Analysis**: Deep dive into existing system architecture and dependencies
- **Modern Design**: Current best practices and performance-optimized architecture
- **Safe Migration**: Data migration tools with integrity validation
- **Compatibility**: Backwards compatibility layers during transition
- **Risk Mitigation**: Comprehensive testing and rollback procedures

## Risk Management Features

- ✅ **Data Integrity Validation**: Comprehensive data migration verification
- ✅ **Rollback Procedures**: Safe rollback plans for any stage
- ✅ **Performance Benchmarks**: Before/after performance comparisons  
- ✅ **Compatibility Testing**: Ensure no functionality is lost
- ✅ **Migration Runbooks**: Step-by-step execution guides

## Expected Deliverables

1. **Legacy Assessment**: Complete analysis of current system and migration scope
2. **Modern Architecture**: Updated system design with current best practices
3. **Migration Tools**: Automated scripts for data and code migration
4. **Test Suite**: Comprehensive validation and regression testing
5. **Migration Guide**: Complete documentation with rollback procedures

## SPARK Intelligence Integration

- 🔍 **5-Agent Pipeline**: Specialized expertise at each migration stage
- 📊 **Risk Assessment**: Evidence-based migration planning
- 🛡️ **Safety First**: Multiple validation layers and rollback options
- 🚀 **88.4% Token Efficiency**: Complex migration planning without token waste
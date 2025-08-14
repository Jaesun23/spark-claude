# SPARK v3.5 Agents Reference

Complete reference for all 28 SPARK agents with practical usage examples and selection guidance.

## Quick Selection Guide

### Core 4 Agents (Highest Priority)
1. **implementer-spark** → Implementation (all personas auto-activated)
2. **analyzer-spark** → Analysis/debugging (multi-dimensional analysis)
3. **tester-spark** → Testing (95% coverage target)
4. **designer-spark** → Design (architecture/UI/UX)

### All 28 Agents
**16 Base Agents** + **12 Team Agents** = 28 Total

**Base:** analyzer, implementer, tester, designer, documenter, troubleshooter, improver, cleaner, explainer, estimater, gitter, builder, spawner, indexer, tasker, loader

**Team:** team1-4 × (implementer, tester, documenter) = 12 specialized parallel agents

---

## Situation-Based Agent Selection

| When You Need | Use Agent | Command Example |
|---------------|-----------|-----------------|
| **Fix bugs** | troubleshooter-spark | `/spark-troubleshoot "fix login error"` |
| **Analyze code** | analyzer-spark | `/spark-analyze "performance bottlenecks"` |
| **Implement features** | implementer-spark | `/spark-implement "JWT authentication"` |
| **Create tests** | tester-spark | `/spark-test "unit tests for auth"` |
| **Design systems** | designer-spark | `/spark-design "microservice architecture"` |
| **Write docs** | documenter-spark | `/spark-document "API documentation"` |
| **Improve performance** | improver-spark | `/spark-improve "optimize database queries"` |
| **Clean code** | cleaner-spark | `/spark-clean "remove dead code"` |
| **Explain concepts** | explainer-spark | `/spark-explain "how OAuth works"` |
| **Estimate work** | estimater-spark | `/spark-estimate "new feature timeline"` |
| **Git operations** | gitter-spark | `/spark-git "commit and push changes"` |
| **Build/Deploy** | builder-spark | `/spark-build "deploy to production"` |
| **Coordinate multiple tasks** | spawner-spark | `/spark-spawn "parallel development"` |
| **Find commands** | indexer-spark | `/spark-index "list all commands"` |
| **Manage todos** | tasker-spark | `/spark-task "organize work items"` |
| **Load project context** | loader-spark | `/spark-load "understand codebase"` |

---

## Persona Auto-Activation

Agents automatically activate relevant personas based on keywords:

| Persona | Triggered By Keywords |
|---------|----------------------|
| **Backend** | API, endpoint, service, database, server, authentication |
| **Frontend** | component, UI, responsive, style, React, Vue, Angular |
| **Security** | auth, security, vulnerability, OWASP, encryption |
| **Architecture** | design, scalable, microservice, system (complexity > 0.7) |
| **DevOps** | deploy, CI/CD, pipeline, Docker, Kubernetes |
| **Data** | data, analytics, database, ETL, migration |
| **Testing** | test, coverage, TDD, unit, integration |
| **Documentation** | document, readme, API docs, guide |

---

## Detailed Agent Reference

### 🔍 analyzer-spark
**Purpose:** Multi-dimensional system analysis

**Key Capabilities:**
- Performance analysis (O(n²) detection, N+1 queries)
- Security analysis (OWASP top 10, auth flows)
- Code quality metrics (complexity, duplication)
- Architecture analysis (coupling, layer violations)

**Usage:**
```json
{
  "target": "file_path | directory | entire_system",
  "focus": ["performance", "security", "quality", "architecture"],
  "depth": "quick | standard | deep"
}
```

**Example:** `Task("analyzer-spark", "analyze authentication system for security vulnerabilities")`

### 🛠️ implementer-spark
**Purpose:** Feature implementation with automatic persona activation

**Key Capabilities:**
- Full-stack implementation
- Design pattern application
- Code generation with best practices
- Integration with existing systems

**Usage:**
```json
{
  "task": "implementation_description",
  "complexity": 0.1-1.0,  // 0.7+ activates architecture mode
  "context": "existing_code_patterns_to_follow"
}
```

**Example:** `Task("implementer-spark", "implement OAuth 2.0 authentication with refresh tokens")`

### 🧪 tester-spark
**Purpose:** Comprehensive testing with high coverage

**Key Capabilities:**
- Unit testing (95% coverage target)
- Integration testing (85% coverage target)
- Security testing (OWASP validation)
- Performance testing

**Usage:**
```json
{
  "coverage_target": {"unit": 95, "integration": 85},
  "framework": "jest | pytest | mocha | junit",
  "focus": ["edge_cases", "happy_path", "security", "performance"]
}
```

**Example:** `Task("tester-spark", "create comprehensive tests for payment processing module")`

### 🎨 designer-spark
**Purpose:** System and UI/UX design

**Key Capabilities:**
- Architecture design (microservices, monoliths)
- API design (RESTful, GraphQL)
- UI/UX design (responsive, accessible)
- Database design (relational, NoSQL)

**Usage:**
```json
{
  "type": "architecture | api | ui | database",
  "requirements": ["scalability", "security", "usability"],
  "constraints": ["technology", "budget", "timeline"]
}
```

**Example:** `Task("designer-spark", "design scalable microservice architecture for e-commerce platform")`

### 📝 documenter-spark
**Purpose:** Comprehensive documentation creation

**Key Capabilities:**
- API documentation (OpenAPI/Swagger)
- User guides and tutorials
- Code documentation (docstrings, comments)
- Architecture documentation

**Usage:**
```json
{
  "type": "api | user_guide | code | architecture",
  "audience": "developers | end_users | administrators",
  "format": "markdown | swagger | inline"
}
```

**Example:** `Task("documenter-spark", "create user guide for new dashboard features")`

### 🔧 troubleshooter-spark
**Purpose:** Bug fixing and issue resolution

**Key Capabilities:**
- Root cause analysis
- Error pattern recognition
- Quick fixes and workarounds
- System debugging

**Usage:** Provide detailed error descriptions, logs, and reproduction steps.

**Example:** `Task("troubleshooter-spark", "fix memory leak in background job processor")`

### ⚡ improver-spark
**Purpose:** Performance and code optimization

**Key Capabilities:**
- Performance optimization
- Code refactoring
- Resource usage optimization
- Scalability improvements

**Usage:** Focus on specific performance metrics or code quality issues.

**Example:** `Task("improver-spark", "optimize database queries reducing response time by 50%")`

### 🧹 cleaner-spark
**Purpose:** Code cleanup and maintenance

**Key Capabilities:**
- Dead code removal
- Code formatting and standardization
- Dependency cleanup
- Technical debt reduction

**Usage:** Specify cleanup scope and standards to maintain.

**Example:** `Task("cleaner-spark", "remove unused imports and dead code from entire project")`

### 💡 explainer-spark
**Purpose:** Code and concept explanation

**Key Capabilities:**
- Code walkthrough generation
- Concept explanation
- Architecture overviews
- Learning material creation

**Usage:** Specify target audience and complexity level.

**Example:** `Task("explainer-spark", "explain microservice communication patterns for new team members")`

### 📊 estimater-spark
**Purpose:** Work estimation and planning

**Key Capabilities:**
- Development time estimation
- Resource requirement analysis
- Risk assessment
- Project planning support

**Usage:** Provide detailed requirements and constraints.

**Example:** `Task("estimater-spark", "estimate development time for mobile app integration")`

### 🔀 gitter-spark
**Purpose:** Git operations and version control

**Key Capabilities:**
- Commit creation with conventional messages
- Branch management
- Merge conflict resolution
- Release preparation

**Usage:** Specify git operation and provide context.

**Example:** `Task("gitter-spark", "create feature branch and commit authentication changes")`

### 🏗️ builder-spark (build-spark)
**Purpose:** Build and deployment automation

**Key Capabilities:**
- CI/CD pipeline creation
- Build optimization
- Deployment automation
- Environment management

**Usage:** Specify build targets and deployment requirements.

**Example:** `Task("builder-spark", "set up automated deployment pipeline for staging environment")`

### 🕸️ spawner-spark
**Purpose:** Multi-agent coordination and parallel execution

**Key Capabilities:**
- Team coordination
- Parallel task orchestration
- Resource allocation
- Workflow management

**Usage:** Used for complex multi-component projects requiring parallel execution.

**Example:** `Task("spawner-spark", "coordinate 4-team parallel development of microservices")`

### 📇 indexer-spark
**Purpose:** Project indexing and command discovery

**Key Capabilities:**
- Command listing
- Project structure analysis
- Documentation indexing
- Search functionality

**Usage:** Used to find available commands and project resources.

**Example:** `Task("indexer-spark", "list all available SPARK commands and their descriptions")`

### ✅ tasker-spark
**Purpose:** Task management and organization

**Key Capabilities:**
- Todo list management
- Task prioritization
- Progress tracking
- Workflow organization

**Usage:** Used to organize and manage development tasks.

**Example:** `Task("tasker-spark", "organize feature development tasks by priority")`

### 📚 loader-spark
**Purpose:** Project context loading and analysis

**Key Capabilities:**
- Codebase analysis
- Project structure understanding
- Context preparation
- Knowledge extraction

**Usage:** Used to understand existing projects before making changes.

**Example:** `Task("loader-spark", "analyze existing authentication system before implementing changes")`

---

## Team Agents (Parallel Execution)

### Team Agent Structure
**12 Team Agents:** team1-4 × (implementer, tester, documenter)

**Examples:**
- `team1-implementer-spark` - Team 1 implementation specialist
- `team2-tester-spark` - Team 2 testing specialist  
- `team3-documenter-spark` - Team 3 documentation specialist
- `team4-implementer-spark` - Team 4 implementation specialist

### Parallel Execution Pattern
```python
# Correct parallel execution (all at once)
Task("team1-implementer-spark", "backend API development")
Task("team2-implementer-spark", "frontend components") 
Task("team3-implementer-spark", "database schema")
Task("team4-implementer-spark", "authentication service")
# ALL agents work simultaneously, results collected when ALL complete
```

### Team Coordination
- Each team works independently on assigned modules
- Teams cannot communicate directly with each other
- FileLockManager prevents file conflicts
- Results merged only after ALL teams complete
- No partial processing or early continuation

---

## Multi-Agent Pipelines

### Sequential Pipeline Example
```bash
# Analysis → Implementation → Testing → Documentation
/spark-launch "new user registration system"
```

Automatically executes:
1. analyzer-spark (requirements analysis)
2. designer-spark (system design)
3. implementer-spark (feature implementation)
4. tester-spark (comprehensive testing)
5. documenter-spark (documentation creation)

### Parallel Pipeline Example
```bash  
# Complex features requiring multiple teams
/multi-implement "microservice architecture" "API endpoints" "UI components" "database design"
```

Automatically coordinates parallel execution across teams.

---

## Quality Gates & Reporting

### Quality Validation System
**16/18 Python agents** have mandatory self-validation:

1. **Syntax Validation** → 0 errors
2. **Type Checking** → mypy --strict (0 errors)
3. **Linting** → ruff --strict (0 violations)
4. **Security Analysis** → OWASP compliance + secrets scan
5. **Test Coverage** → Unit 95%, Integration 85%
6. **Performance Check** → O(n) complexity, no N+1 queries
7. **Documentation** → Required docstrings and comments
8. **Integration Testing** → End-to-end scenario validation

**Self-Validation Command:**
```bash
echo '{"subagent": "[agent-name]", "self_check": true}' | python3 ~/.claude/hooks/spark_quality_gates.py
```

Failed quality gates trigger automatic retry (max 3 attempts).

### Mandatory Reporting System
All agents generate detailed task completion reports:

**Report Location:** `/docs/agents-task/[agent-name]/[task_name]_[timestamp].md`

**Report Categories:**
- **Detailed Reports** (7 analysis/design agents): 500-800+ lines with comprehensive findings
- **Concise Reports** (21 execution agents): 150-300 lines with essential metrics

**Features:**
- Evidence-based findings (file paths, line numbers)
- Quality metrics and performance impact
- Next steps and handoff documentation
- Template library: `/docs/templates/agent-reports/`

---

## Agent Communication Rules

### What Agents CAN Do ✅
- Read JSON state files (current_task.json, previous_result.json)
- Write result files (agent_result.json, implementation_result.json)
- Use TodoWrite for progress tracking
- Complete assigned work independently

### What Agents CANNOT Do ❌
- Call other agents using Task tool (ONLY Claude CODE can do this)
- Direct communication with other agents
- Modify team coordination files
- Override quality gates
- Change workflow sequences
- Skip synchronization points

### Communication Flow
```
Claude CODE → Agent (via Task tool)
Agent → JSON Files (state and results)
JSON Files → Next Agent (via Claude CODE)
```

---

## Usage Tips

### Token Efficiency
- Use specific agent for the task (don't use spawner-spark for simple tasks)
- Provide clear, detailed context to avoid clarification requests
- Specify complexity level to trigger appropriate persona activation

### Parallel Execution
- Only use parallel execution for truly independent tasks
- Ensure tasks can be completed without inter-dependencies
- Remember ALL parallel agents must finish before proceeding

### Quality Assurance
- Trust the quality gates - they prevent technical debt
- Don't skip testing phases for "quick" implementations
- Use appropriate coverage targets (95% unit, 85% integration)

### Error Recovery
- Agents automatically retry on quality failures (max 3 times)
- Provide additional context if initial attempt fails
- Check JSON state files if agents seem to lack context

---

For installation instructions, see [INSTALLATION.md](./INSTALLATION.md)  
For system architecture details, see [ARCHITECTURE.md](./ARCHITECTURE.md)  
For development guidelines, see [DEVELOPMENT.md](./DEVELOPMENT.md)
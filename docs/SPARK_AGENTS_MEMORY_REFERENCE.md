# 🧠 SPARK Agents Memory Reference (For 2호)

> **Practical Agent Usage Guide for 2호**
> *Clear guidelines on when and which agents to use in real situations*

---

## 🚨 Core Principle: "3+ Manual Tasks = Agent Required!"

**Common patterns 2호 often misses (based on real cases):**
- Adding logging to 29 files → Should use `improver-spark` ✅ Verified
- Fixing 67 architecture violations → Should use `improver-spark` ✅ Verified
- Writing quality check scripts → Should use `implementer-spark` ✅ Verified
- Multiple file simultaneous modifications → **Use multiple agents simultaneously** ✅ Verified

---

## 🎯 Practical Agent Selection Decision Tree

### Step 1: Assess Task Scale
```
🔢 5+ files affected? → Agent required
🕐 Expected work time 30+ minutes? → Agent required  
🔄 Repetitive pattern work? → Agent required
🧠 Complex analysis needed? → Agent required
```

### Step 2: Select Agent Type
```
📊 Need analysis? → analyzer-spark
🔧 Improve existing code? → improver-spark  
⚡ Implement new feature? → implementer-spark
🧪 Write/run tests? → tester-spark
🏗️ Architecture design? → designer-spark
🐛 Fix bugs/errors? → troubleshooter-spark
```

---

## 📋 Real Situation Agent Matching (Based on Conversations)

| Jason's Request | What 2호 Missed | Correct Agent | Usage |
|-----------------|-----------------|---------------|-------|
| "Replace 28 print statements with logging" | Manual one-by-one editing | `improver-spark` | Structural code improvement |
| "Fix 67 architecture violations" | Manual analysis attempt | `analyzer-spark` → `improver-spark` | Analysis then improvement |
| "Achieve 100% logging coverage" | Manual addition to 29 files | `improver-spark` | Batch quality improvement |
| "Write quality check script" | Direct writing attempt | `implementer-spark` | New tool implementation |
| "Simultaneous multi-area modifications" | Misunderstanding spawner | **Simultaneous Task calls** | Parallel processing |

---

## ⚡ Correct Multi-Agent Pattern

### ✅ Correct Method (2호 directly calls simultaneously)
```javascript
// Multiple Task calls in one message
Task(improver-spark, "Fix Core Services architecture")
Task(improver-spark, "Fix Core Nodes architecture") 
Task(improver-spark, "Fix Core Workflows architecture")
Task(improver-spark, "Fix API layer architecture")
```

### ❌ Wrong Method (spawner misunderstanding)
```javascript  
// ❌ spawner-spark cannot orchestrate other agents!
Task(spawner-spark, "Coordinate multiple agents for work")  // Impossible

// ❌ This is also impossible - agents can't call other agents
spawner-spark → calls → team1-implementer-spark // Agents cannot directly communicate
```

---

## 🔴 Common Mistakes 2호 Makes

### Mistake 1: Manual Repetitive Work
```
❌ "I'll add logging to 29 files one by one"
✅ improver-spark: "Achieve 100% logging coverage" 
```

### Mistake 2: Direct Complex Analysis Attempts
```
❌ "I'll manually analyze architecture violations"
✅ analyzer-spark: "Analyze architecture violation patterns" → improver-spark: "Fix violations"
```

### Mistake 3: spawner-spark Misunderstanding
```
❌ spawner-spark("Coordinate multiple agents")  // Agents cannot call agents!
✅ Task Task Task Task simultaneous calls     // 2호 directly executes in parallel
```

### Mistake 4: Missing Agent Usage Timing
```
❌ "This is simple work, I'll do it directly" (Result: 2 hours spent)
✅ "Repetitive/complex patterns = agent first" (Result: 15 minutes completion)
```

---

## 🤖 Complete SPARK Agent List (16 agents)

### 🎯 16 Core Agents 

| Agent | Role | When to Use | 5-Phase Pattern |
|-------|------|-------------|-----------------|
| **analyzer-spark** ⭐⭐⭐⭐⭐ | Multi-dimensional system analysis | Complex analysis, root cause identification | Discovery → Evidence → Analysis → Testing → Synthesis |
| **designer-spark** ⭐⭐⭐⭐ | Comprehensive system design | Architecture, API, UI system design | Requirements → Design → Validation → Optimization → Documentation |
| **implementer-spark** ⭐⭐⭐⭐⭐ | Systematic feature implementation | New features, APIs, service implementation | Planning → Foundation → Implementation → Integration → Validation |
| **tester-spark** ⭐⭐⭐⭐ | Comprehensive testing excellence | Test writing, quality assurance | Planning → Unit → Integration → E2E → Reporting |
| **documenter-spark** ⭐⭐⭐ | Professional documentation creation | API docs, user guide writing | Analysis → Structure → Writing → Review → Deployment |
| **troubleshooter-spark** ⭐⭐⭐⭐ | Systematic problem resolution | Bug, performance, incident resolution | Symptom Analysis → Hypothesis Formation → Evidence Collection → Root Cause Verification → Solution Design |
| **improver-spark** ⭐⭐⭐⭐⭐ | Systematic code enhancement | Technical debt, refactoring, quality improvement | Analysis → Planning → Implementation → Integration → Validation |
| **cleaner-spark** ⭐⭐⭐ | Technical debt elimination | Dead code, dependencies, legacy cleanup | Scan → Classify → Clean → Validate → Optimize |
| **builder-spark** ⭐⭐⭐ | Build system optimization | CI/CD, build performance improvement | Analysis → Design → Implementation → Testing → Deployment |
| **estimater-spark** ⭐⭐ | Evidence-based project estimation | Development time, resource estimation | Analysis → Breakdown → Estimation → Validation → Reporting |
| **loader-spark** ⭐⭐⭐ | Comprehensive project onboarding | New project understanding, environment setup | Exploration → Analysis → Documentation → Configuration → Validation |
| **spawner-spark** ⭐⭐⭐ | Multi-task orchestration | Complex multi-domain tasks | Decomposition → Coordination → Execution → Integration → Validation |
| **tasker-spark** ⭐⭐ | Enterprise project management | Long-term projects, team collaboration management | Planning → Breakdown → Tracking → Coordination → Completion |
| **gitter-spark** ⭐⭐ | Git workflow architecture | Branch strategy, commit convention setup | Analysis → Design → Implementation → Testing → Deployment |
| **explainer-spark** ⭐⭐ | Educational content creation | Concept explanation, learning material writing | Analysis → Structuring → Writing → Examples → Validation |
| **indexer-spark** ⭐ | Command catalog navigation | SuperClaude command exploration, recommendations | Collection → Classification → Matching → Recommendation → Guide |

### 🚀 Multi-Implement Command

**When using multi-implement:**
- Must call 4 team agents simultaneously in one message
- Each team handles independent areas for parallel processing  
- 3.1x speed improvement possible

```javascript
// ✅ Correct multi-implement pattern
Task("team1-implementer-spark", "Core Services implementation")
Task("team2-implementer-spark", "API Layer implementation") 
Task("team3-implementer-spark", "Database Layer implementation")
Task("team4-implementer-spark", "Frontend Components implementation")
```

---

## 📊 Agent-Specific Core Usage Scenarios

### improver-spark (Most Important! ⭐⭐⭐⭐⭐)
**When:** Existing code quality improvement, technical debt resolution, refactoring
**Official Goal:** 30-50% code quality improvement
```
✅ print statements → logging conversion (actual: 28 → 0 completed)
✅ Architecture violation fixes (actual: 67 → 44 reduced)
✅ Code complexity improvement (McCabe <10 per function)
✅ Quality score improvement (target: 52 → 85 points)
✅ 5+ files simultaneous modification (Wave Mode auto-activated)
✅ 5-Phase improvement: Analysis → Planning → Implementation → Testing → Validation
```

### analyzer-spark (Analysis Expert ⭐⭐⭐⭐)
**When:** Complex system analysis, problem root cause identification
**5-Phase Pattern:** Discovery → Evidence → Analysis → Testing → Synthesis
```
✅ Performance bottleneck analysis (O(n²) algorithms, N+1 query detection)
✅ Architecture violation pattern identification (Layer violations, circular dependencies)
✅ Quality issue root cause analysis (complexity, duplication, coverage)
✅ Large system understanding (Wave Mode at complexity ≥0.7)
✅ Security analysis (OWASP Top 10, vulnerability scanning)
```

### implementer-spark (Implementation Expert ⭐⭐⭐⭐)  
**When:** New feature/tool implementation
**5-Phase Pattern:** Planning → Foundation → Implementation → Integration → Validation
```
✅ New API endpoint implementation (REST/GraphQL)
✅ Quality check script writing (real case verified)
✅ New service implementation (microservices)
✅ Complex business logic implementation (domain logic)
✅ Wave Mode: Multi-persona activation when complexity ≥0.7
✅ Auto testing: 95% unit, 85% integration targets
```

### tester-spark (Testing Expert ⭐⭐⭐)
**When:** Test writing, validation, quality assurance
**Quality Targets:** Unit 95%, Integration 85%, E2E critical paths
```  
✅ Bulk unit test generation (Jest/Pytest/JUnit)
✅ Integration test writing (API contract testing)
✅ Coverage improvement (target: >90% overall)
✅ Regression test execution (CI/CD integration)
✅ E2E testing (Playwright MCP utilization)
✅ Security testing (OWASP vulnerability validation)
```

---

## 🎯 Practical Decision Checklist

### Agent Usage Decision
- [ ] Need to modify 3+ files?
- [ ] Repetitive pattern work?  
- [ ] Will take 30+ minutes?
- [ ] Complex analysis required?
- [ ] Must meet quality standards?

**If any ✅, agent usage required!**

### Parallel Processing Decision
- [ ] Independent areas? (no file conflicts)
- [ ] Each expected to take 30+ minutes?
- [ ] Can divide into 4+ areas?

**If all ✅, simultaneous Task calls!**

---

## 🚀 High-Efficiency Work Patterns

### Pattern 1: Analysis → Improvement Chain
```javascript
1. analyzer-spark("Complete system analysis") 
2. Review results then
3. improver-spark("Improvements based on analysis results")
```

### Pattern 2: 4-Area Parallel Processing
```javascript  
// Architecture fixes divided into 4 areas
Task(improver-spark, "Core Services area")
Task(improver-spark, "Core Nodes area") 
Task(improver-spark, "Workflows area")
Task(improver-spark, "API area")
```

### Pattern 3: Implementation → Testing Chain
```javascript
1. implementer-spark("New feature implementation")
2. After implementation completion  
3. tester-spark("Test implemented feature")
```

---

## 🔧 Agent Call Templates

### Quality Improvement (improver-spark)
```
Task(improver-spark, "P0-1 logging system improvement: Replace 28 print statements with TraceAwareJSONFormatter-based structured logging")
```

### Architecture Analysis (analyzer-spark)  
```
Task(analyzer-spark, "Root cause analysis of 67 architecture violations and fix strategy establishment")
```

### Implementation Work (implementer-spark)
```
Task(implementer-spark, "Quality check script writing: Adjust V5 standards for memory-one-spark")
```

### Simultaneous Calls (Parallel Processing)
```
Task(improver-spark, "Team 1: Core Services architecture violation fixes")
Task(improver-spark, "Team 2: Core Nodes architecture violation fixes")
Task(improver-spark, "Team 3: Core Workflows architecture violation fixes") 
Task(improver-spark, "Team 4: API layer architecture violation fixes")
```

---

## 📊 Quality Gates (Jason's 8-Step)

**Must verify after agent work:**
1. **Syntax Validation** → 0 errors
2. **Type Check** → mypy --strict (0 errors)  
3. **Linting** → ruff --strict (0 violations)
4. **Security Analysis** → OWASP + secrets scan
5. **Test Coverage** → Unit 95%, Integration 85%
6. **Performance Check** → O(n) complexity, no N+1
7. **Documentation Validation** → Docstrings required
8. **Integration Testing** → E2E scenarios pass

---

## 🔴 Absolute Prohibitions (Based on Official Guide)

1. **Agents calling other agents** ❌
   - Official constraint: "SPARK agents cannot call other agents"
   - spawner-spark ≠ other agent orchestrator (beware of misunderstanding!)
   - Only 2호 (Claude CODE) can call agents via Task

2. **Manual repetitive work** ❌  
   - Official recommendation: Agent required when modifying 3+ files
   - Complexity 0.3+ → Agent usage recommended
   - "Simple so I'll do it directly" → Usually takes 2+ hours (actual observation)

3. **Sequential agent calls** ❌
   - Official pattern: Parallel processing for independent work ("multiple tools in one message")
   - One Task at a time → Task Task Task Task simultaneous calls
   - Team agents utilization: Up to 4 teams parallel execution

4. **Direct complex analysis attempts** ❌
   - Must use analyzer-spark's 5-Phase analysis pattern
   - Wave Mode (complexity ≥0.7) auto-activation
   - Direct analysis → Many missed parts (actually verified)

---

## 💡 Pro Tips (Lessons from Conversations)

- **"Add logging to 28 files"** → improver-spark (Result: Perfect structuring)
- **"67 architecture violations"** → analyzer + improver (Result: Reduced to 44)  
- **"Quality check tool"** → implementer-spark (Result: Professional tool)
- **"Multiple area modifications"** → 4 simultaneous Task calls (Result: Parallel processing)

**Remember: Specialized agents are always better than 2호's judgment!**

---

*This document was written by analyzing actual mistake patterns observed in 2호's conversations.*
*Don't hesitate to use agents - utilize them actively!*
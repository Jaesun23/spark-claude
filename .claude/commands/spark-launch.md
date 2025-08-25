# /spark-launch - SPARK Full-Stack Feature Launch Pipeline

**Purpose**: Complete feature development from design to deployment with quality assurance

## 📝 2호(Claude Code) MUST FOLLOW THIS EXACT PROTOCOL

### **WHEN RECEIVING /spark-launch COMMAND:**

## 🚀 5-Phase Development Pipeline

This command executes a comprehensive development workflow with multiple specialists:

```python
# PHASE 1: Design
1. IMMEDIATELY CALL:
   Task("designer-spark", user_request + " - design architecture")

2. WAIT for agent completion

3. CHECK ~/.claude/workflows/current_task.json:
   REQUIRED CONDITIONS:
   - quality.violations_total == 0
   - quality.can_proceed == true
   - state.status == "completed"

4. DECISION:
   ✅ ALL CONDITIONS MET → Proceed to Phase 2
   ❌ ANY CONDITION FAILED → Task("designer-spark", "Complete design")
- Create system architecture and UI/UX designs
- Define technical requirements and specifications
- Establish design patterns and component structures

# PHASE 2: Implementation
5. CALL:
   Task("implementer-spark", "Implement the designed feature")

6. WAIT for agent completion

7. CHECK current_task.json:
   - output.files.created is not empty

8. DECISION:
   ✅ ALL CONDITIONS MET → Proceed to Phase 3
   ❌ ANY CONDITION FAILED → Task("implementer-spark", "Fix issues")
- Implement the core functionality based on design
- Follow established patterns and architecture
- Ensure code quality through SPARK quality gates

# PHASE 3: Testing
9. CALL:
   Task("tester-spark", "Create comprehensive tests")

10. WAIT for agent completion

11. CHECK current_task.json:
    - quality.step_6_testing.coverage >= 95

12. DECISION:
    ✅ ALL CONDITIONS MET → Proceed to Phase 4
    ❌ ANY CONDITION FAILED → Task("tester-spark", "Improve coverage")
- Create unit, integration, and end-to-end tests
- Achieve 95%+ code coverage
- Validate all functionality works as designed

# PHASE 4: Documentation
13. CALL:
    Task("documenter-spark", "Create comprehensive documentation")

14. WAIT for agent completion

15. CHECK current_task.json:
    - output.docs.readme == true
    - output.docs.api == true

16. DECISION:
    ✅ ALL CONDITIONS MET → Proceed to Phase 5
    ❌ ANY CONDITION FAILED → Task("documenter-spark", "Complete docs")
- Create comprehensive API documentation
- Write user guides and examples
- Update project README and architecture docs

# PHASE 5: Git Integration
17. CALL:
    Task("gitter-spark", "Prepare for deployment")

18. WAIT for agent completion

19. CHECK current_task.json

20. FINAL DECISION:
    ✅ ALL CONDITIONS MET → Report: "Launch complete - ready for deployment"
    ❌ ANY CONDITION FAILED → Task("gitter-spark", "Complete git setup")
```
- Review all changes and create meaningful commits
- Prepare deployment-ready code
- Generate release notes and version updates


## Usage Examples

```bash
/spark-launch "user notification system with email and SMS support"
/spark-launch "real-time chat feature with file sharing capabilities"
/spark-launch "advanced search functionality with filters and sorting"
/spark-launch "user dashboard with analytics and reporting"
/spark-launch "payment processing system with multiple gateways"

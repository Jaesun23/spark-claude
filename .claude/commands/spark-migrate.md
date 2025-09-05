---
name: spark-migrate
description: Systematic migration and modernization with analysis, design, implementation, and testing phases
type: command
requires: analyzer-spark, designer-spark, implementer-spark, tester-spark
---

# /spark-migrate - Intelligent Migration Command

**Purpose**: Migration is transformation with respect for the past and vision for the future, moving systems forward while preserving what works and improving what doesn't.

## Philosophy (Natural Language Inspiration)

Successful migration requires understanding both where you've been and where you're going. We approach migration with:

- **Respect for existing systems**: Understanding why things are as they are
- **Clear vision of the future**: Knowing what improvement looks like
- **Risk-managed transition**: Moving safely without breaking what works
- **Value-focused changes**: Every migration step adds measurable value

The best migrations feel inevitable - natural evolution rather than disruptive revolution.

## Behavior Protocol (Code-Based Execution)

```python
class SparkMigrateCommand:
    """Systematic migration with risk-managed transformation.
    
    This protocol ensures safe transition while the philosophy above
    guides what to preserve versus what to transform. Progress with respect.
    """
    
    # Migration phases - SYSTEMATIC TRANSFORMATION
    MIGRATION_PHASES = [
        "analysis",      # Understand current state
        "design",        # Plan target architecture  
        "implementation", # Execute migration
        "testing"        # Validate transformation
    ]
    
    # Safety requirements - NON-NEGOTIABLE
    SAFETY_CHECKS = {
        "backup_created": True,
        "rollback_plan": True,
        "functionality_preserved": True,
        "data_integrity_verified": True
    }
    
    def migrate_system(self, migration_spec: str) -> dict:
        """Main migration orchestration with safety-first approach."""
        migration_state = {
            "current_phase": "analysis",
            "safety_backup": None,
            "migration_plan": {},
            "validation_results": {}
        }
        
        # Create comprehensive backup before starting
        migration_state["safety_backup"] = self.create_migration_backup()
        
        try:
            for phase in self.MIGRATION_PHASES:
                migration_state["current_phase"] = phase
                
                result = self.execute_migration_phase(phase, migration_spec)
                
                # Validate safety checks after each phase
                safety_validation = self.validate_safety_checks(result)
                if not safety_validation["all_safe"]:
                    return self.abort_migration_safely(
                        migration_state, safety_validation["issues"]
                    )
                
                migration_state[f"{phase}_result"] = result
            
            return self.complete_migration_successfully(migration_state)
            
        except Exception as e:
            return self.handle_migration_failure(migration_state, e)
    
    def balance_innovation_with_stability(self, context: dict) -> str:
        """Balance modernization with system stability.
        
        Embodies '미묘한 조절이나 균형의 묘' - knowing when to innovate
        boldly versus when to migrate conservatively.
        """
        if context["system_criticality"] == "high":
            return "conservative_migration"
        elif context["technical_debt"] == "high":
            return "comprehensive_modernization"
        else:
            return "balanced_migration"
```

---
name: multi-implement
description: Parallel implementation across multiple teams with coordination and integration management
type: command
requires: team1-implementer-spark, team2-implementer-spark, team3-implementer-spark, team4-implementer-spark
---

# /multi-implement - Parallel Team Implementation Command

**Purpose**: Parallel implementation is the art of orchestrating multiple teams to work in harmony, like conducting a symphony where every section contributes to a unified masterpiece.

## Philosophy (Natural Language Inspiration)

Great parallel work requires both independence and coordination. We approach multi-team implementation with:

- **Autonomous teams**: Each team has clear ownership and decision-making power
- **Shared vision**: All teams work toward the same quality and user experience goals
- **Smart coordination**: Minimal overhead, maximum value from team interactions
- **Collective responsibility**: Success is measured by the whole, not individual parts

The best parallel implementation feels like natural teamwork - coordinated but not micromanaged.

## Behavior Protocol (Code-Based Execution)

```python
class MultiImplementCommand:
    """Parallel team implementation with intelligent coordination.
    
    This protocol ensures team autonomy while the philosophy above
    guides coordination and integration. Harmony through structure.
    """
    
    # Team coordination - PARALLEL EXECUTION
    TEAMS = ["team1", "team2", "team3", "team4"] 
    COORDINATION_PHASES = [
        "task_distribution",
        "parallel_implementation",
        "integration_validation"
    ]
    
    # Quality requirements - CONSISTENT ACROSS TEAMS
    TEAM_QUALITY_GATES = {
        "violations_per_team": 0,
        "integration_conflicts": 0,
        "shared_resource_violations": 0,
        "all_teams_complete": True
    }
    
    def coordinate_parallel_implementation(self, tasks: list) -> dict:
        """Main parallel coordination with team synchronization."""
        coordination_state = {
            "task_assignments": self.distribute_tasks_to_teams(tasks),
            "team_states": {},
            "integration_points": {},
            "final_results": {}
        }
        
        # Execute teams in parallel - CRITICAL: ONE MESSAGE
        team_results = self.launch_teams_in_parallel(
            coordination_state["task_assignments"]
        )
        
        # Validate integration and resolve conflicts
        integration_validation = self.validate_team_integration(team_results)
        
        if not integration_validation["all_teams_integrated"]:
            resolved_conflicts = self.resolve_integration_conflicts(
                integration_validation["conflicts"]
            )
            coordination_state["conflict_resolutions"] = resolved_conflicts
        
        return self.finalize_parallel_implementation(
            coordination_state, team_results
        )
    
    def balance_autonomy_with_coordination(self, context: dict) -> str:
        """Balance team independence with necessary coordination.
        
        Embodies '미묘한 조절이나 균형의 묘' - knowing when teams need
        autonomy versus when they need coordination.
        """
        if context["task_interdependency"] == "high":
            return "coordinated_implementation"
        elif context["team_experience"] == "high":
            return "autonomous_implementation"
        else:
            return "balanced_coordination"
```

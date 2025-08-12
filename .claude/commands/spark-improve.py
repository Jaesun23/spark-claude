#!/usr/bin/env python3
"""
SPARK Improve Command - Systematic Code Improvement
Orchestrates multi-dimensional code improvements through specialized agents
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

def parse_command(command: str) -> Dict[str, Any]:
    """Parse /spark-improve command to extract target and options"""
    parts = command.strip().split()
    
    if not parts or parts[0] != "/spark-improve":
        return {"valid": False, "error": "Invalid command format"}
    
    # Extract improvement target (everything after command)
    if len(parts) < 2:
        return {"valid": False, "error": "No improvement target specified"}
    
    target = " ".join(parts[1:])
    
    return {
        "valid": True,
        "target": target,
        "command": "spark-improve"
    }

def analyze_improvement_scope(target: str) -> Dict[str, Any]:
    """Analyze the target to determine improvement scope and complexity"""
    
    # Keywords that indicate different improvement areas
    quality_keywords = ["legacy", "technical debt", "complex", "refactor", "clean", "maintainability"]
    performance_keywords = ["slow", "performance", "bottleneck", "optimize", "memory", "cpu", "speed"]
    security_keywords = ["security", "vulnerability", "auth", "encrypt", "secure", "owasp"]
    architecture_keywords = ["monolithic", "architecture", "structure", "design", "pattern", "coupling"]
    
    target_lower = target.lower()
    
    # Score each improvement area
    quality_score = sum(1 for keyword in quality_keywords if keyword in target_lower)
    performance_score = sum(1 for keyword in performance_keywords if keyword in target_lower)
    security_score = sum(1 for keyword in security_keywords if keyword in target_lower)
    architecture_score = sum(1 for keyword in architecture_keywords if keyword in target_lower)
    
    # Determine complexity based on scope
    total_areas = sum([
        1 if quality_score > 0 else 0,
        1 if performance_score > 0 else 0,
        1 if security_score > 0 else 0,
        1 if architecture_score > 0 else 0
    ])
    
    # Calculate complexity (0.0-1.0)
    base_complexity = min(total_areas * 0.25, 1.0)
    
    # Adjust for scope indicators
    scope_multipliers = {
        "system": 0.3,
        "entire": 0.3, 
        "whole": 0.25,
        "all": 0.2,
        "complete": 0.2,
        "legacy": 0.15
    }
    
    complexity_bonus = 0
    for scope_word, multiplier in scope_multipliers.items():
        if scope_word in target_lower:
            complexity_bonus += multiplier
    
    final_complexity = min(base_complexity + complexity_bonus, 1.0)
    
    return {
        "complexity": final_complexity,
        "improvement_areas": {
            "quality": quality_score,
            "performance": performance_score,
            "security": security_score,
            "architecture": architecture_score
        },
        "total_areas": total_areas,
        "wave_mode": final_complexity >= 0.7,
        "primary_focus": get_primary_focus(quality_score, performance_score, security_score, architecture_score)
    }

def get_primary_focus(quality: int, performance: int, security: int, architecture: int) -> str:
    """Determine the primary improvement focus"""
    scores = {
        "quality": quality,
        "performance": performance, 
        "security": security,
        "architecture": architecture
    }
    
    if all(score == 0 for score in scores.values()):
        return "quality"  # Default to quality improvements
    
    return max(scores, key=scores.get)

def determine_personas(analysis: Dict[str, Any]) -> List[str]:
    """Determine which personas should be activated based on analysis"""
    personas = []
    areas = analysis["improvement_areas"]
    
    if areas["quality"] > 0:
        personas.append("refactorer")
    if areas["performance"] > 0:
        personas.append("performance")
    if areas["security"] > 0:
        personas.append("security")
    if areas["architecture"] > 0 or analysis["complexity"] >= 0.7:
        personas.append("architect")
    
    # Ensure at least refactorer is active for basic improvements
    if not personas:
        personas = ["refactorer"]
    
    return personas

def generate_improvement_strategy(analysis: Dict[str, Any], target: str) -> Dict[str, Any]:
    """Generate improvement strategy based on analysis"""
    
    if analysis["wave_mode"]:
        strategy = "systematic_wave"
        phases = [
            "deep_analysis",
            "improvement_planning", 
            "coordinated_implementation",
            "integration_validation",
            "performance_optimization"
        ]
    else:
        strategy = "direct_improvement"
        phases = [
            "targeted_analysis",
            "focused_improvement",
            "validation"
        ]
    
    return {
        "strategy": strategy,
        "phases": phases,
        "primary_focus": analysis["primary_focus"],
        "personas_required": determine_personas(analysis),
        "mcp_servers": get_mcp_servers(analysis),
        "estimated_time": estimate_improvement_time(analysis)
    }

def get_mcp_servers(analysis: Dict[str, Any]) -> List[str]:
    """Determine which MCP servers should be used"""
    servers = ["sequential"]  # Always use sequential for systematic planning
    
    if analysis["complexity"] >= 0.5:
        servers.append("context7")  # For improvement patterns
    
    if analysis["improvement_areas"]["performance"] > 0:
        servers.append("playwright")  # For performance measurement
    
    return servers

def estimate_improvement_time(analysis: Dict[str, Any]) -> Dict[str, str]:
    """Estimate time required for improvements"""
    
    base_time = 45  # Base time in minutes
    
    # Adjust based on complexity
    complexity_multiplier = 1 + (analysis["complexity"] * 1.5)
    
    # Adjust based on number of improvement areas
    areas_multiplier = 1 + (analysis["total_areas"] - 1) * 0.3
    
    estimated_minutes = int(base_time * complexity_multiplier * areas_multiplier)
    
    return {
        "estimated_time": f"{estimated_minutes} minutes",
        "complexity_factor": f"{analysis['complexity']:.1f}",
        "areas_count": analysis["total_areas"],
        "strategy": "Wave mode" if analysis["wave_mode"] else "Direct improvement"
    }

def create_orchestration_plan(target: str, analysis: Dict[str, Any], strategy: Dict[str, Any]) -> Dict[str, Any]:
    """Create detailed orchestration plan for the improvement workflow"""
    
    plan = {
        "command": "spark-improve",
        "timestamp": datetime.now().isoformat(),
        "target": target,
        "analysis": analysis,
        "strategy": strategy,
        "workflow": {
            "phase_count": len(strategy["phases"]),
            "current_phase": 0,
            "agents_sequence": generate_agent_sequence(strategy),
            "quality_gates": get_quality_gates(analysis),
            "success_criteria": get_success_criteria(analysis)
        },
        "execution_plan": generate_execution_instructions(strategy, analysis)
    }
    
    return plan

def generate_agent_sequence(strategy: Dict[str, Any]) -> List[Dict[str, str]]:
    """Generate the sequence of agents to be called"""
    
    sequence = []
    
    # Phase 1: Always start with analysis
    sequence.append({
        "agent": "analyzer-spark",
        "phase": "analysis",
        "purpose": "Identify improvement opportunities and assess scope",
        "input": "improvement_target"
    })
    
    # Phase 2: Improvement implementation
    sequence.append({
        "agent": "improver-spark", 
        "phase": "improvement",
        "purpose": "Execute systematic code improvements",
        "input": "analysis_results"
    })
    
    # Phase 3: Testing and validation
    sequence.append({
        "agent": "tester-spark",
        "phase": "testing", 
        "purpose": "Validate improvements and ensure no regressions",
        "input": "improvement_results"
    })
    
    # Phase 4: Documentation
    sequence.append({
        "agent": "documenter-spark",
        "phase": "documentation",
        "purpose": "Document improvements and update relevant documentation", 
        "input": "testing_results"
    })
    
    return sequence

def get_quality_gates(analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Define quality gates for the improvement process"""
    
    return {
        "syntax_validation": {"target": 0, "description": "Zero syntax errors"},
        "type_checking": {"target": 0, "description": "Zero MyPy errors"},
        "linting": {"target": 0, "description": "Zero Ruff violations"},
        "security_scan": {"target": 0, "description": "No new security vulnerabilities"},
        "test_coverage": {"target": 95, "description": "Maintain ≥95% test coverage"},
        "performance_regression": {"target": 0, "description": "No performance degradation"},
        "complexity_reduction": {
            "target": 0.2 if analysis["complexity"] >= 0.7 else 0.1,
            "description": "Reduce code complexity by target percentage"
        }
    }

def get_success_criteria(analysis: Dict[str, Any]) -> List[str]:
    """Define success criteria based on improvement areas"""
    
    criteria = [
        "All quality gates pass (0 errors)",
        "Test coverage maintained ≥95%",
        "No breaking changes to public APIs"
    ]
    
    areas = analysis["improvement_areas"]
    
    if areas["quality"] > 0:
        criteria.append("Code complexity reduced measurably")
        criteria.append("Technical debt reduction achieved")
    
    if areas["performance"] > 0:
        criteria.append("Performance metrics improved or maintained")
        criteria.append("Resource utilization optimized")
    
    if areas["security"] > 0:
        criteria.append("Security vulnerabilities addressed")
        criteria.append("Security posture enhanced")
    
    if areas["architecture"] > 0:
        criteria.append("Architecture quality improved")
        criteria.append("Maintainability metrics enhanced")
    
    return criteria

def generate_execution_instructions(strategy: Dict[str, Any], analysis: Dict[str, Any]) -> List[str]:
    """Generate step-by-step execution instructions"""
    
    instructions = [
        f"Step 1: Execute analyzer-spark to assess improvement opportunities",
        "Step 2: Wait for analysis completion and review findings",
        f"Step 3: Execute improver-spark with {strategy['strategy']} strategy",
        "Step 4: Apply quality gates and retry if needed (max 3 attempts)",
        "Step 5: Execute tester-spark to validate improvements",
        "Step 6: Ensure test coverage ≥95% and no regressions",
        "Step 7: Execute documenter-spark to document changes",
        "Step 8: Generate improvement report with before/after metrics"
    ]
    
    if analysis["wave_mode"]:
        instructions.insert(3, "Step 3.1: Coordinate multiple personas in Wave mode")
        instructions.insert(4, "Step 3.2: Apply MCP server strategies (Sequential + Context7)")
    
    return instructions

def main():
    """Main entry point for spark-improve command"""
    
    # Get command from input
    if len(sys.argv) > 1:
        command = " ".join(sys.argv)
    else:
        command = input("Enter command: ")
    
    # Parse command
    parsed = parse_command(command)
    
    if not parsed["valid"]:
        print(json.dumps({
            "error": "Command parsing failed", 
            "details": parsed.get("error", "Unknown error")
        }, indent=2))
        sys.exit(1)
    
    # Analyze improvement scope
    analysis = analyze_improvement_scope(parsed["target"])
    
    # Generate improvement strategy
    strategy = generate_improvement_strategy(analysis, parsed["target"])
    
    # Create orchestration plan
    plan = create_orchestration_plan(parsed["target"], analysis, strategy)
    
    # Output for 2호 to execute
    output = {
        "command": "spark-improve",
        "target": parsed["target"],
        "analysis": analysis,
        "strategy": strategy,
        "orchestration_plan": plan,
        "next_action": "Please execute the improvement workflow using the Task tool to invoke agents in sequence",
        "agent_invocation_example": {
            "first_call": {
                "description": "Analysis Phase",
                "prompt": f"Analyze '{parsed['target']}' for improvement opportunities. Focus on {strategy['primary_focus']} improvements. Generate comprehensive analysis with metrics and recommendations.",
                "subagent_type": "analyzer-spark"
            }
        }
    }
    
    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()
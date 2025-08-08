#!/usr/bin/env python3
"""
SPARK Token Efficiency Validator
Ensures SPARK maintains its 88.4% token efficiency advantage
"""

import json
import logging
import sys
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

# Add hooks directory to path
sys.path.insert(0, str(Path(__file__).parent))
from spark_core_utils import StateManager, HookOutputFormatter

logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler(sys.stderr)])
logger = logging.getLogger(__name__)


class TokenEfficiencyValidator:
    """Validates and maintains SPARK's token efficiency"""
    
    # SPARK efficiency benchmarks
    SUPERCLAUD_BASELINE = 44000  # Traditional SuperClaude tokens
    SPARK_TARGET = 5100         # SPARK average tokens
    TARGET_EFFICIENCY = 88.4    # Target efficiency percentage
    WARNING_THRESHOLD = 85.0    # Warning if efficiency drops below this
    CRITICAL_THRESHOLD = 80.0   # Critical if efficiency drops below this
    
    def __init__(self):
        self.state_manager = StateManager()
    
    def calculate_current_efficiency(self, context_size: int = None) -> Dict[str, Any]:
        """Calculate current token efficiency"""
        try:
            state = self.state_manager.read_state()
            
            # Get current token usage
            current_tokens = context_size or self._estimate_current_tokens(state)
            
            # Calculate efficiency
            efficiency = self._calculate_efficiency(current_tokens)
            
            # Determine status
            status = self._determine_efficiency_status(efficiency)
            
            # Calculate savings
            tokens_saved = self.SUPERCLAUD_BASELINE - current_tokens
            cost_savings = self._calculate_cost_savings(tokens_saved)
            
            return {
                "current_tokens": current_tokens,
                "baseline_tokens": self.SUPERCLAUD_BASELINE,
                "target_tokens": self.SPARK_TARGET,
                "efficiency_percentage": round(efficiency, 1),
                "target_efficiency": self.TARGET_EFFICIENCY,
                "status": status,
                "tokens_saved": tokens_saved,
                "cost_savings": cost_savings,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to calculate efficiency: {e}")
            return {"error": str(e)}
    
    def _estimate_current_tokens(self, state: Dict[str, Any]) -> int:
        """Estimate current token usage based on system state"""
        base_tokens = 1000  # Base system overhead
        
        # Add tokens for loaded personas
        personas = state.get("personas", [])
        persona_tokens = len(personas) * 800  # ~800 tokens per persona
        
        # Add tokens for active agents
        active_agent = state.get("pipeline", {}).get("current_agent")
        agent_tokens = 2500 if active_agent else 0  # Agent loading cost
        
        # Add tokens for quality gates  
        quality_gates = len(state.get("quality_gates", {}).get("results", {}))
        quality_tokens = quality_gates * 200  # ~200 tokens per gate
        
        # Add tokens for workflow state
        workflow = state.get("workflow", {})
        workflow_tokens = len(json.dumps(workflow)) * 2  # Rough estimate
        
        # Add context and memory tokens
        context_tokens = state.get("token_usage", 0)
        
        total_tokens = (base_tokens + persona_tokens + agent_tokens + 
                       quality_tokens + workflow_tokens + context_tokens)
        
        return total_tokens
    
    def _calculate_efficiency(self, current_tokens: int) -> float:
        """Calculate efficiency percentage"""
        if self.SUPERCLAUD_BASELINE <= 0:
            return 0.0
        
        savings = self.SUPERCLAUD_BASELINE - current_tokens
        efficiency = (savings / self.SUPERCLAUD_BASELINE) * 100
        return max(0.0, efficiency)
    
    def _determine_efficiency_status(self, efficiency: float) -> str:
        """Determine efficiency status"""
        if efficiency >= self.TARGET_EFFICIENCY:
            return "excellent"
        elif efficiency >= self.WARNING_THRESHOLD:
            return "good"
        elif efficiency >= self.CRITICAL_THRESHOLD:
            return "warning"
        else:
            return "critical"
    
    def _calculate_cost_savings(self, tokens_saved: int) -> Dict[str, float]:
        """Calculate cost savings based on token reduction"""
        # Anthropic Claude pricing estimates (approximate)
        INPUT_COST_PER_TOKEN = 0.000015   # $0.015 per 1K input tokens
        OUTPUT_COST_PER_TOKEN = 0.000075  # $0.075 per 1K output tokens
        
        # Assume 70% input, 30% output tokens
        input_tokens_saved = tokens_saved * 0.7
        output_tokens_saved = tokens_saved * 0.3
        
        input_cost_savings = input_tokens_saved * INPUT_COST_PER_TOKEN
        output_cost_savings = output_tokens_saved * OUTPUT_COST_PER_TOKEN
        
        total_savings = input_cost_savings + output_cost_savings
        
        return {
            "per_request": round(total_savings, 4),
            "per_100_requests": round(total_savings * 100, 2),
            "per_1000_requests": round(total_savings * 1000, 2)
        }
    
    def validate_efficiency(self) -> Dict[str, Any]:
        """Validate current efficiency meets SPARK standards"""
        efficiency_data = self.calculate_current_efficiency()
        
        if "error" in efficiency_data:
            return efficiency_data
        
        status = efficiency_data["status"]
        efficiency = efficiency_data["efficiency_percentage"]
        
        validation_result = {
            "validation_passed": status in ["excellent", "good"],
            "efficiency_data": efficiency_data,
            "recommendations": []
        }
        
        # Add recommendations based on status
        if status == "critical":
            validation_result["recommendations"].extend([
                "Critical: Token usage too high - consider reducing loaded agents",
                "Review active personas - only load necessary ones",
                "Clear unnecessary workflow state and context",
                "Consider lazy loading for complex operations"
            ])
        elif status == "warning":
            validation_result["recommendations"].extend([
                "Warning: Efficiency below target - optimize token usage",
                "Review quality gates - disable non-critical ones temporarily",
                "Clean up accumulated state data"
            ])
        elif status == "good":
            validation_result["recommendations"].append(
                "Good efficiency - monitor to maintain current levels"
            )
        else:  # excellent
            validation_result["recommendations"].append(
                "Excellent efficiency - SPARK performing optimally"
            )
        
        return validation_result
    
    def optimize_for_efficiency(self) -> Dict[str, Any]:
        """Optimize system for maximum token efficiency"""
        logger.info("🔧 Optimizing SPARK for token efficiency...")
        
        state = self.state_manager.read_state()
        optimization_actions = []
        
        try:
            # Clean up old transition history
            workflow = state.get("workflow", {})
            if "transition_history" in workflow and len(workflow["transition_history"]) > 10:
                workflow["transition_history"] = workflow["transition_history"][-5:]
                optimization_actions.append("Cleaned workflow transition history")
            
            # Clear old data passing entries
            pipeline = state.get("pipeline", {})
            if "data_passing" in pipeline:
                # Keep only last 3 data passing entries
                data_items = list(pipeline["data_passing"].items())
                if len(data_items) > 3:
                    pipeline["data_passing"] = dict(data_items[-3:])
                    optimization_actions.append("Cleaned pipeline data passing entries")
            
            # Remove completed dongsi tasks older than current session
            if "dongsi_tasks" in state:
                active_tasks = {
                    k: v for k, v in state["dongsi_tasks"].items() 
                    if v.get("status") == "active"
                }
                if len(active_tasks) != len(state["dongsi_tasks"]):
                    state["dongsi_tasks"] = active_tasks
                    optimization_actions.append("Removed completed dongsi tasks")
            
            # Compress quality gate results (keep only summary)
            quality_gates = state.get("quality_gates", {})
            if "results" in quality_gates and len(quality_gates["results"]) > 5:
                # Keep only pass/fail status, remove detailed messages
                compressed_results = {
                    gate: {"passed": result.get("passed", False)}
                    for gate, result in quality_gates["results"].items()
                }
                quality_gates["results"] = compressed_results
                optimization_actions.append("Compressed quality gate results")
            
            # Save optimized state
            success = self.state_manager.write_state(state)
            
            if success:
                # Recalculate efficiency
                efficiency_data = self.calculate_current_efficiency()
                
                return {
                    "optimization_complete": True,
                    "actions_taken": optimization_actions,
                    "new_efficiency": efficiency_data.get("efficiency_percentage"),
                    "tokens_saved": efficiency_data.get("tokens_saved"),
                    "status": "optimized"
                }
            else:
                return {
                    "optimization_complete": False,
                    "error": "Failed to save optimized state"
                }
                
        except Exception as e:
            logger.error(f"Optimization failed: {e}")
            return {
                "optimization_complete": False,
                "error": str(e)
            }
    
    def generate_efficiency_report(self) -> Dict[str, Any]:
        """Generate comprehensive efficiency report"""
        efficiency_data = self.calculate_current_efficiency()
        validation = self.validate_efficiency()
        
        return {
            "report_type": "SPARK Token Efficiency Report",
            "generated_at": datetime.now().isoformat(),
            "spark_version": "3.0",
            "efficiency_analysis": efficiency_data,
            "validation_results": validation,
            "benchmark_comparison": {
                "superclaud_tokens": self.SUPERCLAUD_BASELINE,
                "spark_target_tokens": self.SPARK_TARGET,
                "current_tokens": efficiency_data.get("current_tokens", 0),
                "efficiency_vs_target": round(
                    efficiency_data.get("efficiency_percentage", 0) - self.TARGET_EFFICIENCY, 1
                )
            },
            "recommendations": validation.get("recommendations", []),
            "cost_impact": efficiency_data.get("cost_savings", {}),
            "certification": {
                "spark_compliant": validation.get("validation_passed", False),
                "certification_level": efficiency_data.get("status", "unknown")
            }
        }


def main():
    """Main entry point for token efficiency validation"""
    try:
        # Read input from stdin (for hook integration)
        if not sys.stdin.isatty():
            input_data = json.load(sys.stdin)
            context_size = input_data.get("context_size")
        else:
            context_size = None
        
        validator = TokenEfficiencyValidator()
        
        # Run validation
        report = validator.generate_efficiency_report()
        
        # Output report
        print(json.dumps(report, indent=2))
        
        # Log status to stderr
        efficiency = report["efficiency_analysis"].get("efficiency_percentage", 0)
        status = report["efficiency_analysis"].get("status", "unknown")
        
        logger.info(f"🎯 SPARK Token Efficiency: {efficiency}% ({status})")
        
        # If efficiency is low, suggest optimization
        if efficiency < validator.WARNING_THRESHOLD:
            logger.info("⚠️  Consider running optimization: python spark_token_validator.py --optimize")
        
        sys.exit(0)
        
    except Exception as e:
        logger.error(f"Token efficiency validation failed: {e}")
        error_output = {
            "error": str(e),
            "validation_failed": True
        }
        print(json.dumps(error_output))
        sys.exit(1)


if __name__ == "__main__":
    # Handle CLI arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--optimize":
        validator = TokenEfficiencyValidator()
        result = validator.optimize_for_efficiency()
        print(json.dumps(result, indent=2))
    else:
        main()
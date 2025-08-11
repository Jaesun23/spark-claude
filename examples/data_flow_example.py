#!/usr/bin/env python3
"""
Data Flow Example Script

This script demonstrates how to interact with the data flow demo system
and shows what information gets passed through at each stage.
"""

import asyncio
import json
import time
from datetime import datetime
from typing import Dict, Any, List
import aiohttp
import sys
import os

# Configuration
API_BASE = "http://localhost:8001"
DEMO_PORT = 8001


class DataFlowExampleClient:
    """Client for demonstrating data flow system interactions."""
    
    def __init__(self, base_url: str = API_BASE):
        self.base_url = base_url
        self.session = None
    
    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()
    
    async def check_server_health(self) -> bool:
        """Check if the demo server is running."""
        try:
            async with self.session.get(f"{self.base_url}/system-info", timeout=5) as response:
                return response.status == 200
        except Exception:
            return False
    
    async def get_system_info(self) -> Dict[str, Any]:
        """Get system architecture information."""
        async with self.session.get(f"{self.base_url}/system-info") as response:
            return await response.json()
    
    async def get_flow_demo_info(self) -> Dict[str, Any]:
        """Get flow demonstration information."""
        async with self.session.get(f"{self.base_url}/flow-demo") as response:
            return await response.json()
    
    async def process_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Send data through the processing pipeline."""
        async with self.session.post(
            f"{self.base_url}/process-data",
            json=data,
            headers={"Content-Type": "application/json"}
        ) as response:
            result = await response.json()
            # Add response metadata
            result["_response_metadata"] = {
                "status_code": response.status,
                "headers": dict(response.headers),
                "request_id": response.headers.get("X-Request-ID")
            }
            return result
    
    async def get_flow_trace(self, request_id: str) -> Dict[str, Any]:
        """Get the flow trace for a specific request."""
        async with self.session.get(f"{self.base_url}/flow-trace/{request_id}") as response:
            return await response.json()


def print_separator(title: str = "", char: str = "=", width: int = 80):
    """Print a formatted separator line."""
    if title:
        print(f"\n{char * width}")
        print(f" {title} ".center(width, char))
        print(f"{char * width}")
    else:
        print(char * width)


def print_json(data: Any, title: str = ""):
    """Print formatted JSON data."""
    if title:
        print(f"\n📋 {title}:")
    print(json.dumps(data, indent=2, default=str))


async def demonstrate_simple_flow():
    """Demonstrate a simple data processing flow."""
    print_separator("Simple Data Flow Demonstration")
    
    # Sample data to process
    sample_data = {
        "user": "Jason",
        "action": "demonstrate_flow",
        "timestamp": datetime.now().isoformat(),
        "sample_numbers": [1, 2, 3, 4, 5],
        "sample_object": {
            "nested_field": "value",
            "active": True,
            "priority": "high"
        }
    }
    
    print("🔄 Sending data through processing pipeline...")
    print_json(sample_data, "Input Data")
    
    async with DataFlowExampleClient() as client:
        if not await client.check_server_health():
            print("❌ Server not running. Please start the server first:")
            print(f"   python src/api/data_flow_demo.py")
            return
        
        # Process the data
        result = await client.process_data(sample_data)
        
        print_json(result.get("processed_data"), "Processed Data")
        print_json(result.get("processing_metadata"), "Processing Metadata")
        print_json(result.get("_response_metadata"), "Response Metadata")
        
        request_id = result.get("request_id")
        if request_id:
            print(f"\n🔍 Request ID: {request_id}")
            print("💡 This ID can be used to trace the complete data flow")


async def demonstrate_system_architecture():
    """Show system architecture and information tracking."""
    print_separator("System Architecture Information")
    
    async with DataFlowExampleClient() as client:
        if not await client.check_server_health():
            print("❌ Server not running")
            return
        
        # Get system information
        system_info = await client.get_system_info()
        
        print_json(system_info.get("architecture"), "System Architecture")
        print_json(system_info.get("data_flow"), "Data Flow Process")
        
        print("\n📊 Information Tracked:")
        for item in system_info.get("information_tracked", []):
            print(f"  • {item}")
        
        print_json(system_info.get("trace_format"), "Trace Format")


async def demonstrate_multiple_requests():
    """Demonstrate processing multiple different types of data."""
    print_separator("Multiple Request Types Demonstration")
    
    test_cases = [
        {
            "name": "User Registration Data",
            "data": {
                "type": "user_registration",
                "username": "jason_test",
                "email": "jason@example.com",
                "preferences": {
                    "theme": "dark",
                    "notifications": True
                }
            }
        },
        {
            "name": "Analytics Event Data",
            "data": {
                "type": "analytics_event",
                "event": "page_view",
                "page": "/dashboard",
                "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
                "timestamp": datetime.now().isoformat()
            }
        },
        {
            "name": "Configuration Update",
            "data": {
                "type": "config_update",
                "settings": {
                    "max_connections": 100,
                    "timeout_seconds": 30,
                    "debug_mode": False
                },
                "updated_by": "admin"
            }
        }
    ]
    
    async with DataFlowExampleClient() as client:
        if not await client.check_server_health():
            print("❌ Server not running")
            return
        
        request_ids = []
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n🧪 Test Case {i}: {test_case['name']}")
            print_json(test_case['data'], "Input")
            
            result = await client.process_data(test_case['data'])
            request_id = result.get("request_id")
            
            print(f"✅ Processed successfully - Request ID: {request_id}")
            print(f"📊 Processing stages: {result.get('processing_metadata', {}).get('stages_completed', 'unknown')}")
            
            if request_id:
                request_ids.append(request_id)
            
            # Add a small delay between requests
            await asyncio.sleep(0.1)
        
        print(f"\n📝 Generated {len(request_ids)} traceable requests:")
        for i, req_id in enumerate(request_ids, 1):
            print(f"  {i}. {req_id}")


async def demonstrate_flow_stages():
    """Show detailed information about each processing stage."""
    print_separator("Processing Stages Breakdown")
    
    async with DataFlowExampleClient() as client:
        if not await client.check_server_health():
            print("❌ Server not running")
            return
        
        # Get flow demo information
        flow_info = await client.get_flow_demo_info()
        
        print(f"🎯 {flow_info.get('system_overview', {}).get('title', 'Data Flow System')}")
        print(f"   {flow_info.get('system_overview', {}).get('description', 'System description')}")
        
        print("\n🔄 Processing Stages:")
        for stage in flow_info.get("flow_stages", []):
            print(f"  📍 {stage.get('stage', '').replace('_', ' ').title()}")
            print(f"     {stage.get('description', '')}")
        
        print("\n🛠️ System Components:")
        components = flow_info.get("system_overview", {}).get("components", [])
        for component in components:
            print(f"  • {component}")
        
        print(f"\n📊 Active Traces: {flow_info.get('current_active_traces', 0)}")
        print(f"🕐 Demo Timestamp: {flow_info.get('demonstration_timestamp', 'unknown')}")


def print_usage_instructions():
    """Print instructions for running the demo."""
    print_separator("Data Flow Demo Usage Instructions")
    
    print("""
🚀 How to Run the Complete Demo:

1. Start the demo server:
   python src/api/data_flow_demo.py
   
2. Run this example script:
   python examples/data_flow_example.py
   
3. Open web visualization (optional):
   http://localhost:8001/

📊 What You'll See:

• System Architecture: How components interact
• Data Flow Stages: Step-by-step processing
• Request Tracking: Unique ID assignment
• Information Capture: What data gets recorded
• Processing Metadata: Timing and stage info
• Response Enrichment: Added context and IDs

🔍 Key Features Demonstrated:

• Middleware captures all requests/responses
• Each processing stage records input/output data
• Timestamps track processing time at each stage
• Metadata provides context for debugging
• Request IDs enable full trace reconstruction
• Different data types processed uniformly

💡 Real-World Applications:

• API request monitoring and debugging
• Performance bottleneck identification
• Audit trail creation for compliance
• Error tracking and root cause analysis
• System integration monitoring
    """)


async def main():
    """Main demonstration function."""
    print("🔥 SPARK Data Flow System Demonstration")
    print("=" * 50)
    
    try:
        # Check if server is running
        async with DataFlowExampleClient() as client:
            if not await client.check_server_health():
                print_usage_instructions()
                print("\n❌ Demo server is not running.")
                print("Please start the server first and try again.")
                return
        
        print("✅ Demo server is running - starting demonstrations...")
        
        # Run all demonstrations
        await demonstrate_system_architecture()
        await demonstrate_flow_stages() 
        await demonstrate_simple_flow()
        await demonstrate_multiple_requests()
        
        print_separator("Demo Complete!")
        print("""
🎉 Data Flow Demonstration Complete!

Key Takeaways:
• Information flows through 6 distinct stages
• Each stage captures input/output data and metadata  
• Request IDs enable complete trace reconstruction
• System provides detailed monitoring and debugging capabilities
• Architecture supports both simple and complex data processing

💻 Web Interface: http://localhost:8001/
📚 API Documentation: http://localhost:8001/docs
        """)
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Demo error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Check for required dependencies
    try:
        import aiohttp
    except ImportError:
        print("❌ Missing required dependency: aiohttp")
        print("Install with: pip install aiohttp")
        sys.exit(1)
    
    # Run the demonstration
    asyncio.run(main())
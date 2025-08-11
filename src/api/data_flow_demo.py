"""
Data Flow Demonstration Module.

This module demonstrates how information flows through the SPARK system,
showing request processing, data transformation, and response generation.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import json
import uuid

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.base import BaseHTTPMiddleware
from fastapi.staticfiles import StaticFiles
import os


class ProcessingStage(Enum):
    """Processing stages in the data flow."""
    REQUEST_RECEIVED = "request_received"
    DATA_VALIDATION = "data_validation"
    BUSINESS_LOGIC = "business_logic"
    DATA_TRANSFORMATION = "data_transformation"
    RESPONSE_PREPARATION = "response_preparation"
    RESPONSE_SENT = "response_sent"


@dataclass
class FlowStep:
    """Represents a single step in the data flow."""
    stage: ProcessingStage
    timestamp: str
    input_data: Optional[Dict[str, Any]]
    output_data: Optional[Dict[str, Any]]
    processing_time_ms: float
    metadata: Dict[str, Any]


@dataclass
class DataFlowTrace:
    """Tracks the complete data flow through the system."""
    request_id: str
    start_time: str
    end_time: Optional[str] = None
    total_processing_time_ms: Optional[float] = None
    steps: List[FlowStep] = None
    
    def __post_init__(self):
        if self.steps is None:
            self.steps = []


class DataFlowTracker:
    """Tracks data flow through processing stages."""
    
    def __init__(self):
        self.active_traces: Dict[str, DataFlowTrace] = {}
    
    def start_trace(self, request_id: str) -> DataFlowTrace:
        """Start tracking a new request."""
        trace = DataFlowTrace(
            request_id=request_id,
            start_time=datetime.now().isoformat(),
            steps=[]
        )
        self.active_traces[request_id] = trace
        return trace
    
    def add_step(self, request_id: str, stage: ProcessingStage, 
                 input_data: Optional[Dict] = None,
                 output_data: Optional[Dict] = None,
                 processing_time_ms: float = 0.0,
                 metadata: Optional[Dict] = None) -> None:
        """Add a processing step to the trace."""
        if request_id not in self.active_traces:
            return
        
        step = FlowStep(
            stage=stage,
            timestamp=datetime.now().isoformat(),
            input_data=input_data,
            output_data=output_data,
            processing_time_ms=processing_time_ms,
            metadata=metadata or {}
        )
        
        self.active_traces[request_id].steps.append(step)
    
    def complete_trace(self, request_id: str) -> Optional[DataFlowTrace]:
        """Complete and return the trace."""
        if request_id not in self.active_traces:
            return None
        
        trace = self.active_traces[request_id]
        trace.end_time = datetime.now().isoformat()
        
        if trace.steps:
            start_time = datetime.fromisoformat(trace.start_time)
            end_time = datetime.fromisoformat(trace.end_time)
            trace.total_processing_time_ms = (end_time - start_time).total_seconds() * 1000
        
        # Remove from active traces
        del self.active_traces[request_id]
        return trace


# Global tracker instance
flow_tracker = DataFlowTracker()


class DataFlowMiddleware(BaseHTTPMiddleware):
    """Middleware to track request flow."""
    
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        # Start tracing
        flow_tracker.start_trace(request_id)
        flow_tracker.add_step(
            request_id,
            ProcessingStage.REQUEST_RECEIVED,
            input_data={
                "method": request.method,
                "url": str(request.url),
                "headers": dict(request.headers),
            },
            metadata={"client_ip": request.client.host if request.client else "unknown"}
        )
        
        start_time = datetime.now()
        response = await call_next(request)
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        flow_tracker.add_step(
            request_id,
            ProcessingStage.RESPONSE_SENT,
            output_data={"status_code": response.status_code},
            processing_time_ms=processing_time,
            metadata={"response_headers": dict(response.headers)}
        )
        
        # Add request ID to response headers for tracking
        response.headers["X-Request-ID"] = request_id
        
        return response


# Create FastAPI app with middleware
app = FastAPI(title="Data Flow Demo API", version="1.0.0")
app.add_middleware(DataFlowMiddleware)

# Mount static files if the directory exists
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.post("/process-data")
async def process_data(request: Request, data: Dict[str, Any]) -> JSONResponse:
    """
    Demonstrate data processing flow with detailed tracking.
    
    Args:
        data: Input data to process
        
    Returns:
        JSONResponse: Processed data with flow information
    """
    request_id = request.state.request_id
    
    try:
        # Stage 1: Data Validation
        flow_tracker.add_step(
            request_id,
            ProcessingStage.DATA_VALIDATION,
            input_data=data,
            metadata={"validation_rules": ["required_fields", "data_types"]}
        )
        
        # Validate required fields
        if not isinstance(data, dict):
            raise HTTPException(status_code=400, detail="Input must be a dictionary")
        
        validated_data = {
            "original_data": data,
            "validation_status": "passed",
            "validated_at": datetime.now().isoformat()
        }
        
        # Stage 2: Business Logic Processing
        flow_tracker.add_step(
            request_id,
            ProcessingStage.BUSINESS_LOGIC,
            input_data=validated_data,
            metadata={"business_rules": ["data_enrichment", "calculations"]}
        )
        
        # Apply business logic (example: add computed fields)
        processed_data = {
            **validated_data,
            "computed_fields": {
                "processing_timestamp": datetime.now().isoformat(),
                "data_size": len(str(data)),
                "field_count": len(data) if isinstance(data, dict) else 0
            },
            "business_logic_applied": True
        }
        
        # Stage 3: Data Transformation
        flow_tracker.add_step(
            request_id,
            ProcessingStage.DATA_TRANSFORMATION,
            input_data=processed_data,
            output_data=processed_data,
            metadata={"transformations": ["timestamp_formatting", "metadata_addition"]}
        )
        
        # Transform for response format
        response_data = {
            "request_id": request_id,
            "status": "success",
            "processed_data": processed_data,
            "processing_metadata": {
                "stages_completed": 3,
                "final_processing_time": datetime.now().isoformat()
            }
        }
        
        # Stage 4: Response Preparation
        flow_tracker.add_step(
            request_id,
            ProcessingStage.RESPONSE_PREPARATION,
            output_data=response_data,
            metadata={"response_format": "json", "status_code": 200}
        )
        
        return JSONResponse(content=response_data, status_code=200)
        
    except HTTPException:
        raise
    except Exception as e:
        flow_tracker.add_step(
            request_id,
            ProcessingStage.RESPONSE_PREPARATION,
            metadata={"error": str(e), "status_code": 500}
        )
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")


@app.get("/flow-trace/{request_id}")
async def get_flow_trace(request_id: str) -> JSONResponse:
    """
    Retrieve the data flow trace for a specific request.
    
    Args:
        request_id: The request ID to get trace for
        
    Returns:
        JSONResponse: Complete flow trace information
    """
    # Check if trace is still active
    if request_id in flow_tracker.active_traces:
        trace = flow_tracker.active_traces[request_id]
        return JSONResponse(
            content={
                "status": "active",
                "trace": asdict(trace),
                "message": "Request is still being processed"
            }
        )
    
    # For completed traces, we would typically store them in a database
    # For this demo, we'll return a simulated completed trace
    return JSONResponse(
        content={
            "status": "not_found",
            "message": f"No trace found for request ID: {request_id}",
            "suggestion": "Use /process-data endpoint to generate traceable requests"
        }
    )


@app.get("/flow-demo")
async def flow_demonstration() -> JSONResponse:
    """
    Provide a demonstration of the data flow system.
    
    Returns:
        JSONResponse: Information about the data flow system
    """
    demo_info = {
        "system_overview": {
            "title": "SPARK Data Flow Demonstration",
            "description": "This system tracks how information flows through processing stages",
            "components": [
                "Request Reception",
                "Data Validation", 
                "Business Logic Processing",
                "Data Transformation",
                "Response Preparation",
                "Response Delivery"
            ]
        },
        "flow_stages": [
            {
                "stage": stage.value,
                "description": f"Stage where {stage.value.replace('_', ' ')} occurs"
            }
            for stage in ProcessingStage
        ],
        "example_usage": {
            "step_1": "POST /process-data with JSON payload",
            "step_2": "System processes data through multiple stages",
            "step_3": "GET /flow-trace/{request_id} to see complete flow",
            "step_4": "Response includes processing metadata and trace ID"
        },
        "current_active_traces": len(flow_tracker.active_traces),
        "demonstration_timestamp": datetime.now().isoformat()
    }
    
    return JSONResponse(content=demo_info)


@app.get("/system-info")
async def system_information() -> JSONResponse:
    """
    Show information about how data passes through the system.
    
    Returns:
        JSONResponse: System architecture and data flow information
    """
    system_info = {
        "architecture": {
            "pattern": "Multi-layer processing with request tracking",
            "components": {
                "middleware": "DataFlowMiddleware - tracks requests/responses",
                "tracker": "DataFlowTracker - manages processing stages",
                "processors": "Business logic handlers with stage tracking"
            }
        },
        "data_flow": {
            "input": "HTTP request with JSON payload",
            "processing": [
                "Request middleware captures initial data",
                "Validation stage ensures data integrity", 
                "Business logic applies domain rules",
                "Transformation prepares response format",
                "Response middleware adds final metadata"
            ],
            "output": "JSON response with processing trace"
        },
        "information_tracked": [
            "Request metadata (headers, method, URL)",
            "Processing timestamps for each stage",
            "Input/output data at each stage",
            "Processing time measurements",
            "Error information if failures occur",
            "Response preparation details"
        ],
        "trace_format": {
            "request_id": "Unique identifier for request tracking",
            "timestamps": "ISO format timestamps for each stage",
            "processing_steps": "List of stages with input/output data",
            "metadata": "Additional context for each processing stage"
        }
    }
    
    return JSONResponse(content=system_info)


@app.get("/", response_class=HTMLResponse)
async def serve_visualization():
    """Serve the data flow visualization page."""
    static_file = os.path.join(os.path.dirname(__file__), "static", "flow_visualization.html")
    if os.path.exists(static_file):
        with open(static_file, 'r', encoding='utf-8') as f:
            return HTMLResponse(content=f.read())
    else:
        return HTMLResponse(
            content="""
            <html>
                <body>
                    <h1>Data Flow Demo API</h1>
                    <p>Static visualization file not found. API endpoints are available:</p>
                    <ul>
                        <li><a href="/flow-demo">/flow-demo</a> - Flow demonstration info</li>
                        <li><a href="/system-info">/system-info</a> - System architecture info</li>
                        <li>POST <a href="/docs#/default/process_data_process_data_post">/process-data</a> - Process data with flow tracking</li>
                    </ul>
                    <p><a href="/docs">Interactive API Documentation</a></p>
                </body>
            </html>
            """,
            status_code=200
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
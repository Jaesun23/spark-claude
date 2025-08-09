"""
Hello World API endpoint implementation.

This module provides a simple FastAPI endpoint that returns a greeting
with a timestamp, demonstrating basic API functionality.
"""

from datetime import datetime
from typing import Dict, Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse


app = FastAPI(title="Hello World API", version="1.0.0")


@app.get("/hello")
async def hello_world() -> Dict[str, Any]:
    """
    Simple hello world endpoint.
    
    Returns:
        Dict[str, Any]: JSON response containing message and timestamp
        
    Raises:
        HTTPException: If an error occurs during processing
    """
    try:
        current_time = datetime.now().isoformat()
        
        response_data = {
            "message": "Hello, World!",
            "timestamp": current_time,
            "status": "success"
        }
        
        return response_data
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint.
    
    Returns:
        Dict[str, str]: Health status response
    """
    return {"status": "healthy", "service": "hello-api"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
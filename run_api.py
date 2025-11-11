#!/usr/bin/env python
"""
Run the FastAPI application.
Usage: python run_api.py
"""
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    port = int(os.getenv('API_PORT', 8000))
    
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )

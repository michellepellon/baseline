"""
FastAPI application for Apple Health analysis engine.
"""

import sys
import traceback
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from backend.api.routes import auth, ingest, sleep

app = FastAPI(
    title="Apple Health Analysis Engine",
    description="Advanced analysis and visualization tool for Apple HealthKit data",
    version="0.1.0",
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler to log all errors."""
    print(f"ERROR: {exc}")
    print(f"Traceback: {traceback.format_exc()}")
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
    )


# Configure CORS for local frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5000"],  # SvelteKit default dev port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(ingest.router)
app.include_router(sleep.router)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Apple Health Analysis Engine",
        "version": "0.1.0",
    }


@app.get("/health")
async def health_check():
    """Detailed health check endpoint."""
    return {
        "status": "healthy",
        "database": "not_initialized",
        "parser": "ready",
    }


# Mount static files for frontend
frontend_build_path = project_root / "frontend" / "build"
if frontend_build_path.exists():
    # Mount the _app directory for assets
    app.mount(
        "/_app",
        StaticFiles(directory=str(frontend_build_path / "_app")),
        name="app_assets",
    )

    # Serve index.html for all other routes (SPA fallback)
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        """Serve the SPA for all non-API routes."""
        # If the path is an API route, let it pass through
        if full_path.startswith(("api/", "docs", "redoc", "openapi.json")):
            return JSONResponse(
                status_code=404, content={"detail": "API endpoint not found"}
            )

        # Check if it's a static file request
        file_path = frontend_build_path / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)

        # Otherwise, serve the index.html (SPA fallback)
        index_path = frontend_build_path / "index.html"
        if index_path.exists():
            return FileResponse(index_path)

        return JSONResponse(status_code=404, content={"detail": "Not found"})

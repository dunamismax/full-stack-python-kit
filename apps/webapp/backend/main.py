#!/usr/bin/env python3
"""
Full-Stack Python Kit FastAPI Web Application

A comprehensive web application demonstrating the full capabilities
of the Full-Stack Python Kit with FastAPI, SQLModel, and modern Python patterns.
"""

import asyncio
from contextlib import asynccontextmanager
from typing import Dict, Any

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

from packages.core.config import get_settings
from packages.core.logging import configure_logging, get_logger
from packages.database.session import create_db_and_tables, get_db
from app.api import api_router
from app.monitoring import setup_monitoring

# Configure logging
configure_logging()
logger = get_logger(__name__)

# Get settings
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("Starting up Full-Stack Python Kit API", version=settings.app_version)
    
    # Initialize database
    try:
        await create_db_and_tables()
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error("Failed to create database tables", error=str(e))
        raise
    
    # Setup monitoring
    setup_monitoring(app)
    
    yield
    
    # Shutdown
    logger.info("Shutting down Full-Stack Python Kit API")


# Initialize Sentry if DSN is provided
if settings.sentry_dsn:
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        integrations=[
            FastApiIntegration(auto_enabling_integrations=False),
            SqlalchemyIntegration(),
        ],
        traces_sample_rate=1.0 if settings.debug else 0.1,
        environment=settings.environment,
    )

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="A comprehensive Full-Stack Python Kit API with authentication, real-time features, and modern architecture",
    openapi_url=f"{settings.api_v1_prefix}/openapi.json",
    docs_url=f"{settings.api_v1_prefix}/docs",
    redoc_url=f"{settings.api_v1_prefix}/redoc",
    lifespan=lifespan,
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"] if settings.debug else ["localhost", "127.0.0.1"],
)


# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with structured logging."""
    logger.warning(
        "HTTP exception occurred",
        status_code=exc.status_code,
        detail=exc.detail,
        path=request.url.path,
        method=request.method,
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "status_code": exc.status_code},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions with structured logging."""
    logger.error(
        "Unhandled exception occurred",
        error=str(exc),
        path=request.url.path,
        method=request.method,
        exc_info=True,
    )
    
    if settings.debug:
        return JSONResponse(
            status_code=500,
            content={
                "detail": f"Internal server error: {str(exc)}",
                "status_code": 500,
                "type": type(exc).__name__,
            },
        )
    else:
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error", "status_code": 500},
        )


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests."""
    start_time = asyncio.get_event_loop().time()
    
    response = await call_next(request)
    
    process_time = asyncio.get_event_loop().time() - start_time
    
    logger.info(
        "Request processed",
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        process_time=round(process_time, 4),
        user_agent=request.headers.get("user-agent"),
    )
    
    return response


# Include API router
app.include_router(api_router, prefix=settings.api_v1_prefix)


# Root endpoint
@app.get("/")
async def root() -> Dict[str, Any]:
    """Root endpoint with API information."""
    return {
        "message": "Welcome to the Full-Stack Python Kit API",
        "version": settings.app_version,
        "environment": settings.environment,
        "docs_url": f"{settings.api_v1_prefix}/docs",
        "redoc_url": f"{settings.api_v1_prefix}/redoc",
        "features": [
            "Authentication & Authorization",
            "Task Management",
            "Note Taking",
            "Real-time WebSocket Support",
            "File Upload/Download",
            "API Rate Limiting",
            "Structured Logging",
            "Monitoring & Observability",
            "Async Database Operations",
            "Comprehensive API Documentation",
        ],
    }


# Health check endpoint
@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    """Health check endpoint."""
    try:
        # Test database connection
        await db.execute("SELECT 1")
        db_status = "healthy"
    except Exception as e:
        logger.error("Database health check failed", error=str(e))
        db_status = "unhealthy"
    
    return {
        "status": "healthy" if db_status == "healthy" else "unhealthy",
        "version": settings.app_version,
        "environment": settings.environment,
        "database": db_status,
        "timestamp": "2025-01-13T00:00:00Z",  # Would use datetime.utcnow() in real app
    }


# Development server
def main():
    """Run the development server."""
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="debug" if settings.debug else "info",
    )


if __name__ == "__main__":
    main()
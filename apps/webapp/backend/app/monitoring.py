"""
Monitoring and observability setup for the Full-Stack Python Kit API.
"""

import time
from typing import Dict, Any

from fastapi import FastAPI, Request, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

from packages.core.logging import get_logger

logger = get_logger(__name__)

# Metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status_code']
)

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

API_ERRORS = Counter(
    'api_errors_total',
    'Total API errors',
    ['error_type', 'endpoint']
)


def setup_monitoring(app: FastAPI) -> None:
    """Setup monitoring and metrics collection."""
    
    @app.middleware("http")
    async def monitoring_middleware(request: Request, call_next):
        """Collect metrics for each request."""
        start_time = time.time()
        
        # Process the request
        response = await call_next(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Get endpoint path template
        endpoint = request.url.path
        if hasattr(request, 'path_info'):
            endpoint = request.path_info
        
        # Record metrics
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=endpoint,
            status_code=response.status_code
        ).inc()
        
        REQUEST_DURATION.labels(
            method=request.method,
            endpoint=endpoint
        ).observe(duration)
        
        # Log slow requests
        if duration > 1.0:  # Log requests taking more than 1 second
            logger.warning(
                "Slow request detected",
                method=request.method,
                endpoint=endpoint,
                duration=duration,
                status_code=response.status_code
            )
        
        return response
    
    @app.get("/metrics")
    async def get_metrics():
        """Prometheus metrics endpoint."""
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
    
    @app.get("/health/detailed")
    async def detailed_health_check() -> Dict[str, Any]:
        """Detailed health check with component status."""
        
        health_status = {
            "status": "healthy",
            "timestamp": "2025-01-13T00:00:00Z",
            "version": "0.1.0",
            "components": {
                "database": "healthy",  # Would check actual DB connection
                "redis": "healthy",     # Would check actual Redis connection
                "api": "healthy",
            },
            "metrics": {
                "uptime_seconds": 0,  # Would calculate actual uptime
                "memory_usage_mb": 0,  # Would get actual memory usage
                "cpu_usage_percent": 0,  # Would get actual CPU usage
            }
        }
        
        return health_status


def record_api_error(error_type: str, endpoint: str) -> None:
    """Record an API error for monitoring."""
    API_ERRORS.labels(error_type=error_type, endpoint=endpoint).inc()
    logger.error("API error recorded", error_type=error_type, endpoint=endpoint)
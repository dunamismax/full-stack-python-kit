"""
Structured logging configuration using structlog.
"""

import sys
import logging
from typing import Any, Dict

import structlog
from structlog.typing import FilteringBoundLogger

from .config import get_settings


def configure_logging() -> None:
    """Configure structured logging for the application."""
    settings = get_settings()
    
    # Configure structlog
    structlog.configure(
        processors=[
            # Add log level to event dict
            structlog.stdlib.add_log_level,
            # Add a timestamp to event dict
            structlog.processors.TimeStamper(fmt="iso"),
            # Add logger name to event dict
            structlog.stdlib.add_logger_name,
            # Perform %-style formatting
            structlog.stdlib.PositionalArgumentsFormatter(),
            # Add stack info if available
            structlog.processors.StackInfoRenderer(),
            # Format exception info if available
            structlog.processors.format_exc_info,
            # Render the final event dict as JSON if in production
            structlog.processors.JSONRenderer() if settings.environment == "production"
            else structlog.dev.ConsoleRenderer(colors=True),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
    
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.DEBUG if settings.debug else logging.INFO,
    )


def get_logger(name: str) -> FilteringBoundLogger:
    """Get a structured logger instance."""
    return structlog.get_logger(name)


# Request ID processor for FastAPI
class RequestIDProcessor:
    """Add request ID to log context."""
    
    def __call__(self, logger: Any, name: str, event_dict: Dict[str, Any]) -> Dict[str, Any]:
        # In a real application, you would get the request ID from context
        # For now, we'll add a placeholder
        event_dict["request_id"] = getattr(self, "_request_id", None)
        return event_dict
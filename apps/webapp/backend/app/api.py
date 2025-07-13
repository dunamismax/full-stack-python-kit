"""
API routes for the Full-Stack Python Kit web application.
"""

from fastapi import APIRouter

from .routes import auth, tasks, notes, users, websocket

# Create main API router
api_router = APIRouter()

# Include sub-routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
api_router.include_router(notes.router, prefix="/notes", tags=["Notes"])
api_router.include_router(websocket.router, prefix="/ws", tags=["WebSocket"])
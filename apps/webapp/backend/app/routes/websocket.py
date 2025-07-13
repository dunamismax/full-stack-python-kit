"""
WebSocket routes for real-time features in the Full-Stack Python Kit API.
"""

import json
from typing import Dict, Set
from uuid import UUID

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, status
from fastapi.exceptions import WebSocketException
from sqlalchemy.ext.asyncio import AsyncSession

from packages.database.session import get_db
from packages.auth.auth import verify_token
from packages.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)


class ConnectionManager:
    """Manages WebSocket connections."""
    
    def __init__(self):
        self.active_connections: Dict[UUID, WebSocket] = {}
        self.user_connections: Dict[UUID, Set[UUID]] = {}
    
    async def connect(self, websocket: WebSocket, user_id: UUID, connection_id: UUID):
        """Connect a new WebSocket."""
        await websocket.accept()
        self.active_connections[connection_id] = websocket
        
        if user_id not in self.user_connections:
            self.user_connections[user_id] = set()
        self.user_connections[user_id].add(connection_id)
        
        logger.info("WebSocket connected", user_id=str(user_id), connection_id=str(connection_id))
    
    def disconnect(self, user_id: UUID, connection_id: UUID):
        """Disconnect a WebSocket."""
        if connection_id in self.active_connections:
            del self.active_connections[connection_id]
        
        if user_id in self.user_connections:
            self.user_connections[user_id].discard(connection_id)
            if not self.user_connections[user_id]:
                del self.user_connections[user_id]
        
        logger.info("WebSocket disconnected", user_id=str(user_id), connection_id=str(connection_id))
    
    async def send_personal_message(self, message: str, connection_id: UUID):
        """Send a message to a specific connection."""
        if connection_id in self.active_connections:
            websocket = self.active_connections[connection_id]
            await websocket.send_text(message)
    
    async def send_user_message(self, message: str, user_id: UUID):
        """Send a message to all connections for a user."""
        if user_id in self.user_connections:
            for connection_id in self.user_connections[user_id].copy():
                try:
                    await self.send_personal_message(message, connection_id)
                except:
                    # Connection is broken, remove it
                    self.disconnect(user_id, connection_id)
    
    async def broadcast(self, message: str):
        """Broadcast a message to all connected clients."""
        for connection_id, websocket in self.active_connections.copy().items():
            try:
                await websocket.send_text(message)
            except:
                # Connection is broken, clean up
                # Find and remove from user_connections
                for user_id, conn_ids in self.user_connections.items():
                    if connection_id in conn_ids:
                        self.disconnect(user_id, connection_id)
                        break


# Global connection manager
manager = ConnectionManager()


async def get_current_user_ws(websocket: WebSocket, token: str = None) -> UUID:
    """Get current user from WebSocket token."""
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION, reason="Token required")
    
    payload = verify_token(token)
    if not payload:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION, reason="Invalid token")
    
    user_id_str = payload.get("sub")
    if not user_id_str:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION, reason="Invalid token payload")
    
    try:
        return UUID(user_id_str)
    except ValueError:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION, reason="Invalid user ID")


@router.websocket("/connect")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = None,
    db: AsyncSession = Depends(get_db)
):
    """WebSocket endpoint for real-time communication."""
    
    try:
        # Authenticate user
        user_id = await get_current_user_ws(websocket, token)
        
        # Generate connection ID
        from uuid import uuid4
        connection_id = uuid4()
        
        # Connect
        await manager.connect(websocket, user_id, connection_id)
        
        # Send welcome message
        welcome_message = {
            "type": "connected",
            "message": "Successfully connected to Full-Stack Python Kit WebSocket",
            "connection_id": str(connection_id),
            "user_id": str(user_id),
        }
        await websocket.send_text(json.dumps(welcome_message))
        
        try:
            while True:
                # Receive message from client
                data = await websocket.receive_text()
                
                try:
                    message_data = json.loads(data)
                except json.JSONDecodeError:
                    error_response = {
                        "type": "error",
                        "message": "Invalid JSON format"
                    }
                    await websocket.send_text(json.dumps(error_response))
                    continue
                
                # Handle different message types
                message_type = message_data.get("type")
                
                if message_type == "ping":
                    # Respond to ping
                    pong_response = {
                        "type": "pong",
                        "timestamp": "2025-01-13T00:00:00Z"  # Would use actual timestamp
                    }
                    await websocket.send_text(json.dumps(pong_response))
                
                elif message_type == "task_update":
                    # Handle task update notifications
                    task_data = message_data.get("data", {})
                    
                    # Broadcast to user's other connections
                    update_notification = {
                        "type": "task_updated",
                        "data": task_data,
                        "timestamp": "2025-01-13T00:00:00Z"
                    }
                    await manager.send_user_message(
                        json.dumps(update_notification), 
                        user_id
                    )
                
                elif message_type == "note_update":
                    # Handle note update notifications
                    note_data = message_data.get("data", {})
                    
                    # Broadcast to user's other connections
                    update_notification = {
                        "type": "note_updated",
                        "data": note_data,
                        "timestamp": "2025-01-13T00:00:00Z"
                    }
                    await manager.send_user_message(
                        json.dumps(update_notification), 
                        user_id
                    )
                
                elif message_type == "typing":
                    # Handle typing indicators
                    typing_data = message_data.get("data", {})
                    
                    typing_notification = {
                        "type": "user_typing",
                        "data": {
                            "user_id": str(user_id),
                            "is_typing": typing_data.get("is_typing", False),
                            "context": typing_data.get("context", "")
                        },
                        "timestamp": "2025-01-13T00:00:00Z"
                    }
                    
                    # In a real app, you might broadcast to specific rooms/channels
                    await manager.send_user_message(
                        json.dumps(typing_notification), 
                        user_id
                    )
                
                else:
                    # Unknown message type
                    error_response = {
                        "type": "error",
                        "message": f"Unknown message type: {message_type}"
                    }
                    await websocket.send_text(json.dumps(error_response))
                
        except WebSocketDisconnect:
            manager.disconnect(user_id, connection_id)
            
    except WebSocketException:
        # Already handled in get_current_user_ws
        pass
    except Exception as e:
        logger.error("WebSocket error", error=str(e), exc_info=True)
        try:
            await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
        except:
            pass


@router.websocket("/notifications/{user_id}")
async def user_notifications(
    websocket: WebSocket,
    user_id: UUID,
    token: str = None,
):
    """WebSocket endpoint for user-specific notifications."""
    
    try:
        # Authenticate user
        authenticated_user_id = await get_current_user_ws(websocket, token)
        
        # Check if user is accessing their own notifications
        if authenticated_user_id != user_id:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return
        
        from uuid import uuid4
        connection_id = uuid4()
        
        await manager.connect(websocket, user_id, connection_id)
        
        # Send initial notification
        initial_message = {
            "type": "notifications_connected",
            "message": "Connected to notification stream",
            "user_id": str(user_id),
        }
        await websocket.send_text(json.dumps(initial_message))
        
        try:
            while True:
                # Keep connection alive and handle any incoming messages
                data = await websocket.receive_text()
                
                # Echo back for now (in a real app, you might handle commands)
                echo_response = {
                    "type": "echo",
                    "data": data,
                    "timestamp": "2025-01-13T00:00:00Z"
                }
                await websocket.send_text(json.dumps(echo_response))
                
        except WebSocketDisconnect:
            manager.disconnect(user_id, connection_id)
            
    except WebSocketException:
        pass
    except Exception as e:
        logger.error("Notification WebSocket error", error=str(e), exc_info=True)
        try:
            await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
        except:
            pass


# Utility function to send notifications (can be called from other routes)
async def send_notification(user_id: UUID, notification_type: str, data: dict):
    """Send a notification to a specific user."""
    notification = {
        "type": notification_type,
        "data": data,
        "timestamp": "2025-01-13T00:00:00Z"
    }
    
    await manager.send_user_message(json.dumps(notification), user_id)
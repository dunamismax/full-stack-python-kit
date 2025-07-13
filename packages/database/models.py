"""
Database models using SQLModel.
"""

from datetime import datetime
from typing import Optional, List
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field, Relationship


class TimestampMixin(SQLModel):
    """Mixin for timestamp fields."""
    
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class User(TimestampMixin, table=True):
    """User model."""
    
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, nullable=False)
    username: str = Field(unique=True, index=True, nullable=False)
    full_name: Optional[str] = Field(default=None)
    hashed_password: str = Field(nullable=False)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    is_verified: bool = Field(default=False)
    
    # Relationships
    tasks: List["Task"] = Relationship(back_populates="user")
    notes: List["Note"] = Relationship(back_populates="user")


class Task(TimestampMixin, table=True):
    """Task model for the demo app."""
    
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(nullable=False)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    priority: str = Field(default="medium")  # low, medium, high
    due_date: Optional[datetime] = Field(default=None)
    
    # Foreign key
    user_id: UUID = Field(foreign_key="user.id", nullable=False)
    
    # Relationships
    user: User = Relationship(back_populates="tasks")


class Note(TimestampMixin, table=True):
    """Note model for the demo app."""
    
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(nullable=False)
    content: str = Field(nullable=False)
    tags: Optional[str] = Field(default=None)  # JSON string of tags
    
    # Foreign key
    user_id: UUID = Field(foreign_key="user.id", nullable=False)
    
    # Relationships
    user: User = Relationship(back_populates="notes")


class APIKey(TimestampMixin, table=True):
    """API Key model for API access."""
    
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(nullable=False)
    key_hash: str = Field(unique=True, index=True, nullable=False)
    is_active: bool = Field(default=True)
    expires_at: Optional[datetime] = Field(default=None)
    
    # Foreign key
    user_id: UUID = Field(foreign_key="user.id", nullable=False)


# Pydantic models for API

class UserBase(SQLModel):
    """Base user schema."""
    email: str
    username: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """User creation schema."""
    password: str


class UserRead(UserBase):
    """User read schema."""
    id: UUID
    is_active: bool
    is_superuser: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime


class UserUpdate(SQLModel):
    """User update schema."""
    email: Optional[str] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None


class TaskBase(SQLModel):
    """Base task schema."""
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: str = "medium"
    due_date: Optional[datetime] = None


class TaskCreate(TaskBase):
    """Task creation schema."""
    pass


class TaskRead(TaskBase):
    """Task read schema."""
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime


class TaskUpdate(SQLModel):
    """Task update schema."""
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None


class NoteBase(SQLModel):
    """Base note schema."""
    title: str
    content: str
    tags: Optional[str] = None


class NoteCreate(NoteBase):
    """Note creation schema."""
    pass


class NoteRead(NoteBase):
    """Note read schema."""
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime


class NoteUpdate(SQLModel):
    """Note update schema."""
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[str] = None
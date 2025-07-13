"""
Task management routes for the Full-Stack Python Kit API.
"""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_

from packages.database.session import get_db
from packages.database.models import Task, TaskCreate, TaskRead, TaskUpdate, User
from packages.auth.auth import get_current_user
from packages.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get("/", response_model=List[TaskRead])
async def get_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    completed: Optional[bool] = Query(None),
    priority: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[Task]:
    """Get tasks for the current user with optional filters."""
    
    conditions = [Task.user_id == current_user.id]
    
    if completed is not None:
        conditions.append(Task.completed == completed)
    
    if priority is not None:
        conditions.append(Task.priority == priority)
    
    statement = select(Task).where(and_(*conditions)).offset(skip).limit(limit).order_by(Task.created_at.desc())
    result = await db.execute(statement)
    tasks = result.scalars().all()
    
    return list(tasks)


@router.post("/", response_model=TaskRead)
async def create_task(
    task_data: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Task:
    """Create a new task."""
    
    # Validate priority
    valid_priorities = ["low", "medium", "high"]
    if task_data.priority not in valid_priorities:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Priority must be one of: {', '.join(valid_priorities)}"
        )
    
    new_task = Task(
        **task_data.dict(),
        user_id=current_user.id
    )
    
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    
    logger.info("Task created", task_id=str(new_task.id), user_id=str(current_user.id))
    
    return new_task


@router.get("/{task_id}", response_model=TaskRead)
async def get_task(
    task_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Task:
    """Get a specific task."""
    
    statement = select(Task).where(
        and_(Task.id == task_id, Task.user_id == current_user.id)
    )
    result = await db.execute(statement)
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    return task


@router.patch("/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: UUID,
    task_update: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Task:
    """Update a task."""
    
    statement = select(Task).where(
        and_(Task.id == task_id, Task.user_id == current_user.id)
    )
    result = await db.execute(statement)
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Validate priority if provided
    if task_update.priority is not None:
        valid_priorities = ["low", "medium", "high"]
        if task_update.priority not in valid_priorities:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Priority must be one of: {', '.join(valid_priorities)}"
            )
    
    # Update task fields
    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
    
    await db.commit()
    await db.refresh(task)
    
    logger.info("Task updated", task_id=str(task.id), user_id=str(current_user.id))
    
    return task


@router.delete("/{task_id}")
async def delete_task(
    task_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict[str, str]:
    """Delete a task."""
    
    statement = select(Task).where(
        and_(Task.id == task_id, Task.user_id == current_user.id)
    )
    result = await db.execute(statement)
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    await db.delete(task)
    await db.commit()
    
    logger.info("Task deleted", task_id=str(task_id), user_id=str(current_user.id))
    
    return {"message": "Task deleted successfully"}


@router.post("/{task_id}/toggle", response_model=TaskRead)
async def toggle_task_completion(
    task_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Task:
    """Toggle task completion status."""
    
    statement = select(Task).where(
        and_(Task.id == task_id, Task.user_id == current_user.id)
    )
    result = await db.execute(statement)
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    task.completed = not task.completed
    await db.commit()
    await db.refresh(task)
    
    logger.info(
        "Task completion toggled", 
        task_id=str(task.id), 
        completed=task.completed, 
        user_id=str(current_user.id)
    )
    
    return task


@router.get("/stats/summary")
async def get_task_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict[str, int]:
    """Get task statistics for the current user."""
    
    # Total tasks
    total_statement = select(Task).where(Task.user_id == current_user.id)
    total_result = await db.execute(total_statement)
    total_tasks = len(total_result.scalars().all())
    
    # Completed tasks
    completed_statement = select(Task).where(
        and_(Task.user_id == current_user.id, Task.completed == True)
    )
    completed_result = await db.execute(completed_statement)
    completed_tasks = len(completed_result.scalars().all())
    
    # Priority breakdown
    priority_stats = {}
    for priority in ["low", "medium", "high"]:
        priority_statement = select(Task).where(
            and_(Task.user_id == current_user.id, Task.priority == priority, Task.completed == False)
        )
        priority_result = await db.execute(priority_statement)
        priority_stats[f"{priority}_priority"] = len(priority_result.scalars().all())
    
    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": total_tasks - completed_tasks,
        **priority_stats,
    }
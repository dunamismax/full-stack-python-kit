"""
Note management routes for the Full-Stack Python Kit API.
"""

import json
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_

from packages.database.session import get_db
from packages.database.models import Note, NoteCreate, NoteRead, NoteUpdate, User
from packages.auth.auth import get_current_user
from packages.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get("/", response_model=List[NoteRead])
async def get_notes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    tag: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[Note]:
    """Get notes for the current user with optional search and filtering."""
    
    conditions = [Note.user_id == current_user.id]
    
    # Add search condition
    if search:
        search_condition = Note.title.ilike(f"%{search}%") | Note.content.ilike(f"%{search}%")
        conditions.append(search_condition)
    
    # Add tag filter
    if tag:
        # Simple tag filtering - in a real app, you might use a proper tag system
        tag_condition = Note.tags.ilike(f"%{tag}%")
        conditions.append(tag_condition)
    
    statement = select(Note).where(and_(*conditions)).offset(skip).limit(limit).order_by(Note.updated_at.desc())
    result = await db.execute(statement)
    notes = result.scalars().all()
    
    return list(notes)


@router.post("/", response_model=NoteRead)
async def create_note(
    note_data: NoteCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Note:
    """Create a new note."""
    
    # Validate tags if provided
    if note_data.tags:
        try:
            # Ensure tags is valid JSON
            json.loads(note_data.tags)
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tags must be valid JSON"
            )
    
    new_note = Note(
        **note_data.dict(),
        user_id=current_user.id
    )
    
    db.add(new_note)
    await db.commit()
    await db.refresh(new_note)
    
    logger.info("Note created", note_id=str(new_note.id), user_id=str(current_user.id))
    
    return new_note


@router.get("/{note_id}", response_model=NoteRead)
async def get_note(
    note_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Note:
    """Get a specific note."""
    
    statement = select(Note).where(
        and_(Note.id == note_id, Note.user_id == current_user.id)
    )
    result = await db.execute(statement)
    note = result.scalar_one_or_none()
    
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    
    return note


@router.patch("/{note_id}", response_model=NoteRead)
async def update_note(
    note_id: UUID,
    note_update: NoteUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Note:
    """Update a note."""
    
    statement = select(Note).where(
        and_(Note.id == note_id, Note.user_id == current_user.id)
    )
    result = await db.execute(statement)
    note = result.scalar_one_or_none()
    
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    
    # Validate tags if provided
    if note_update.tags is not None:
        try:
            json.loads(note_update.tags)
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tags must be valid JSON"
            )
    
    # Update note fields
    update_data = note_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(note, field, value)
    
    await db.commit()
    await db.refresh(note)
    
    logger.info("Note updated", note_id=str(note.id), user_id=str(current_user.id))
    
    return note


@router.delete("/{note_id}")
async def delete_note(
    note_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict[str, str]:
    """Delete a note."""
    
    statement = select(Note).where(
        and_(Note.id == note_id, Note.user_id == current_user.id)
    )
    result = await db.execute(statement)
    note = result.scalar_one_or_none()
    
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    
    await db.delete(note)
    await db.commit()
    
    logger.info("Note deleted", note_id=str(note_id), user_id=str(current_user.id))
    
    return {"message": "Note deleted successfully"}


@router.get("/tags/list")
async def get_all_tags(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[str]:
    """Get all unique tags for the current user."""
    
    statement = select(Note.tags).where(
        and_(Note.user_id == current_user.id, Note.tags.is_not(None))
    )
    result = await db.execute(statement)
    tag_strings = result.scalars().all()
    
    # Extract individual tags from JSON strings
    all_tags = set()
    for tag_string in tag_strings:
        if tag_string:
            try:
                tags = json.loads(tag_string)
                if isinstance(tags, list):
                    all_tags.update(tags)
            except json.JSONDecodeError:
                continue
    
    return sorted(list(all_tags))


@router.get("/stats/summary")
async def get_note_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict[str, int]:
    """Get note statistics for the current user."""
    
    # Total notes
    total_statement = select(Note).where(Note.user_id == current_user.id)
    total_result = await db.execute(total_statement)
    total_notes = len(total_result.scalars().all())
    
    # Notes with tags
    tagged_statement = select(Note).where(
        and_(Note.user_id == current_user.id, Note.tags.is_not(None))
    )
    tagged_result = await db.execute(tagged_statement)
    tagged_notes = len(tagged_result.scalars().all())
    
    # Total word count (approximate)
    all_notes_statement = select(Note.content).where(Note.user_id == current_user.id)
    all_notes_result = await db.execute(all_notes_statement)
    all_content = all_notes_result.scalars().all()
    
    total_words = sum(len(content.split()) for content in all_content if content)
    
    return {
        "total_notes": total_notes,
        "tagged_notes": tagged_notes,
        "untagged_notes": total_notes - tagged_notes,
        "total_words": total_words,
    }
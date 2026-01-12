from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.note.service import NoteService
from app.note.schemas import NoteCreateModel,NoteUpdateModel,NoteResponseModel
from app.core.database import get_session


note_router = APIRouter()
note_service = NoteService()

@note_router.get("/", response_model=List[NoteResponseModel])
async def get_all_notes(session: AsyncSession = Depends(get_session))->dict:
    
    return await note_service.get_all_notes(session)


@note_router.get("/{note_id}", response_model=NoteResponseModel)
async def get_note_by_id(note_id:int,session:AsyncSession = Depends(get_session)):
    note = await note_service.get_note_by_id(note_id,session)
    if not note:
        raise HTTPException(status_code=404,detail="Note not found")
    return note

@note_router.post("/",response_model=NoteResponseModel)
async def create_note(note_data:NoteCreateModel,session:AsyncSession = Depends(get_session)):

    return await note_service.create_note(note_data,session)


@note_router.patch("/{note_id}",response_model=NoteResponseModel)
async def update_note(note_id:int,note_update_data:NoteUpdateModel,session:AsyncSession = Depends(get_session)):
    updated_note = await note_service.update_note(note_id,note_update_data,session)
    if not updated_note:
        raise HTTPException(status_code=404,detail="Note not Updated")
    return updated_note


@note_router.delete("/{note_id}")
async def delete_a_note(note_id:int,session:AsyncSession = Depends(get_session)):
    deleted_note = await note_service.delete_note(note_id,session)
    if not deleted_note:
        raise HTTPException(status_code=404,detial="Note not Deleted")
    return {
        "Note deleted successfully"
    }

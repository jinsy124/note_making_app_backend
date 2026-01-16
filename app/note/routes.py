from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.note.service import NoteService
from app.note.schemas import NoteCreateModel,NoteUpdateModel,NoteResponseModel
from app.core.database import get_session
from app.auth.dependencies import get_current_user
from app.auth.models import User

note_router = APIRouter()
note_service = NoteService()

@note_router.get("/", response_model=dict)
async def get_user_notes(session: AsyncSession = Depends(get_session),current_user:User=Depends(get_current_user))->List[NoteResponseModel]:
    
    return await note_service.get_user_notes(session=session,user_id=current_user.id)
    # return {"helth":"working"}


@note_router.get("/{note_id}", response_model=NoteResponseModel)
async def get_note_by_id(note_id:int,session:AsyncSession = Depends(get_session),current_user:User=Depends(get_current_user)):
    note = await note_service.get_note_by_id(note_id,session,user_id=current_user.id)
    if not note:
        raise HTTPException(status_code=404,detail="Note not found")
    return note

@note_router.post("/",response_model=NoteResponseModel)
async def create_note(note_data:NoteCreateModel,session:AsyncSession = Depends(get_session),current_user:User=Depends(get_current_user)):

    return await note_service.create_note(note_data,session,user_id=current_user.id)


@note_router.patch("/{note_id}",response_model=NoteResponseModel)
async def update_note(note_id:int,note_update_data:NoteUpdateModel,session:AsyncSession = Depends(get_session),current_user:User=Depends(get_current_user)):
    updated_note = await note_service.update_note(note_id,note_update_data,session,user_id=current_user.id)
    if not updated_note:
        raise HTTPException(status_code=404,detail="Note not Updated")
    return updated_note


@note_router.delete("/{note_id}")
async def delete_a_note(note_id:int,session:AsyncSession = Depends(get_session),current_user:User=Depends(get_current_user)):
    deleted_note = await note_service.delete_note(note_id,session,user_id=current_user.id)
    if not deleted_note:
        raise HTTPException(status_code=404,detial="Note not Deleted")
    return {
        "Note deleted successfully"
    }

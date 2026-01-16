from typing import List
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import NoteCreateModel,NoteUpdateModel,NoteResponseModel
from .model import Note as NoteModel

class NoteService:
    async def get_user_notes(self, session: AsyncSession,user_id:int) -> List[NoteResponseModel]:
        result = await session.execute(select(NoteModel).where(NoteModel.user_id == user_id).order_by(NoteModel.created_at.desc()))
        notes = result.scalars().all()  # List of SQLModel objects
        # Convert each SQLModel object to Pydantic
        return [NoteResponseModel.model_validate(note) for note in notes]


    async def get_note_by_id(self,note_id:int,session: AsyncSession,user_id:int):
        result = await session.execute(select(NoteModel).where(
            NoteModel.id == note_id,
            NoteModel.user_id == user_id
        ))
        note = result.scalar_one_or_none()
        if not note:
            return None
        return NoteResponseModel.model_validate(note)


    async def create_note(self, note_data: NoteCreateModel, session: AsyncSession,user_id:int):
        note_data_dict = note_data.model_dump()
        new_note = NoteModel(**note_data_dict,user_id=user_id)
               
        session.add(new_note)
        await session.commit()
        await session.refresh(new_note)
        return NoteResponseModel.model_validate(new_note)

    async def update_note(self, note_id:int, note_update_data: NoteUpdateModel, session: AsyncSession,user_id:int):
        result = await session.execute(select(NoteModel).where(
            NoteModel.id == note_id,
            NoteModel.user_id == user_id
        ))
        note = result.scalar_one_or_none()
        if not note:
            return None
        for key, value in note_update_data.model_dump(exclude_unset=True).items():
            setattr(note, key, value)
        

        await session.commit()
        await session.refresh(note)
        return NoteResponseModel.model_validate(note)

    async def delete_note(self, note_id, session: AsyncSession,user_id:int):
        result = await session.execute(
            select(NoteModel).where(
                NoteModel.id == note_id,
                NoteModel.user_id == user_id
            )
        )
        note = result.scalar_one_or_none()
        if not note:
            return False
        await session.delete(note)
        await session.commit()
        return True

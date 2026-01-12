from pydantic import BaseModel
from datetime import datetime
from typing import Optional 

class NoteBase(BaseModel):
    title:str
    content:str

class NoteCreateModel(NoteBase):
    pass

class NoteUpdateModel(BaseModel):
    title:Optional[str] = None
    content:Optional[str] = None

class NoteResponseModel(NoteBase):
    id:int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }


    
from pydantic import BaseModel,ConfigDict
from datetime import datetime
from typing import Optional 
from uuid import UUID


class UserCreateModel(BaseModel):
    username: str
    email: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserModel(BaseModel):
    username: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_verified: bool
    password_hash: str
    created_at: datetime
    updated_at: datetime

class UserLoginModel(BaseModel):
    email: str
    password: str
    
class UserResponseModel(BaseModel):
    id: int
    uuid:str
    email: str
    username: str
    first_name: str | None
    last_name: str | None
    is_verified: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
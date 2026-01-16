from pydantic import BaseModel,ConfigDict,Field,EmailStr
from datetime import datetime
from typing import Optional 
from uuid import UUID


class UserCreateModel(BaseModel):
    username: str = Field(
        ...,
        min_length=4,
        max_length=20,
        examples=["john Doe"],
        Description = "Username must be at least 5 characters"

    )
    email: EmailStr 
    password: str = Field(
        ...,
        min_length=4,
        examples=["password123"],
        description="Password must be at least 6 characters"
    )
    first_name: Optional[str] = Field( None ,max_length=20)
    last_name: Optional[str] = Field(None,max_length=20)
    

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
    email: EmailStr
    password: str = Field(
        ...,
        min_length=4

    )
    
class UserResponseModel(BaseModel):
    id: int
    uuid:UUID
    email: EmailStr
    username: str
    first_name: str | None
    last_name: str | None
    is_verified: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
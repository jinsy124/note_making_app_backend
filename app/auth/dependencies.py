from fastapi.security import HTTPBearer
from fastapi import Request,Depends
from fastapi.security.http import HTTPAuthorizationCredentials
from .utilis import decode_token
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from sqlalchemy import select
from app.auth.models import User

from app.core.errors import (
    InvalidToken,
    RefreshTokenRequired,
    AccessTokenRequired,
    
)



class TokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self,request:Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        token = creds.credentials
        token_data = decode_token(token)

        if not self.token_valid(token):
            raise InvalidToken()
        
        self.verify_token_data(token_data)
        return token_data

        
    def token_valid(self, token:str) ->bool:
        token_data = decode_token(token)
        return token_data is not None
    
    def verify_token_data(self,token_data):
        if token_data is None:
            raise InvalidToken()
    
class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) ->None:
        if token_data is None:
            raise InvalidToken()
        if token_data.get("refresh"):
            raise AccessTokenRequired()
class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) ->None:
        if token_data and not token_data["refresh"] :
            raise RefreshTokenRequired()
        
        
async def get_current_user(
        token_data:dict = Depends(AccessTokenBearer()),
        session:AsyncSession = Depends(get_session)
)->User:
    if token_data is None:
        raise InvalidToken()
    user_id = token_data.get("sub")

    print(user_id)
    if not user_id:
        raise InvalidToken()
    result = await session.execute(select(User).where(User.id==int(user_id)))
    user=result.scalar_one_or_none()
    if not user:
        raise InvalidToken()
    return user


    
from fastapi.security import HTTPBearer
from fastapi import Request
from fastapi.security.http import HTTPAuthorizationCredentials
from .utilis import decode_token
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session

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
        raise True if token_data is not None else False
    
class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) ->None:
        if token_data and token_data["refresh"] :
            raise AccessTokenRequired()
class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) ->None:
        if token_data and not token_data["refresh"] :
            raise RefreshTokenRequired()
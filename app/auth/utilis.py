from passlib.context import CryptContext
from datetime import timedelta,datetime
from app.core.config import settings  
import jwt
import uuid
import logging

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated="auto"
)
ACCESS_TOKEN_EXPIRY = 3600


def generate_passwd_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

def create_access_token(user_data:dict,expiry:timedelta = None, refresh:bool=False):

    payload={}
    payload['user'] = user_data
    payload['exp'] = datetime.now() + (
        expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY) 
    )
    payload['jti'] = str(uuid.uuid4())

    payload['refresh'] = refresh



    token = jwt.encode(
        payload=payload,
        key=settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )
    return token

def decode_token(token:str)->dict:
    try:
        token_data = jwt.decode(
            jwt=token,
            key=settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None


from fastapi import APIRouter, Depends,status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.auth.dependencies import AccessTokenBearer,RefreshTokenBearer
from app.core.errors import UserAlreadyExists,InvalidCreadentials,InvalidToken,UserNotFound
from app.auth.service import UserService
from .utilis import create_access_token,decode_token,verify_password
from datetime import timedelta,datetime
from fastapi.responses import JSONResponse
from app.auth.schema import UserCreateModel,UserLoginModel,UserModel,UserResponseModel

auth_router = APIRouter()
user_service = UserService()

REFRESH_TOKEN_EXPIRY = 2

@auth_router.post(
    "/signup",
    response_model=UserResponseModel,
    status_code=status.HTTP_201_CREATED
    )
async def create_user_Account(
    user_data: UserCreateModel,
    session: AsyncSession = Depends(get_session)):
    email = user_data.email
    user_exists = await user_service.user_exists(session, email)

    if user_exists:
        raise UserAlreadyExists()

    new_user = await user_service.create_user(session,user_data)
    return new_user

@auth_router.post("/login")
async def login_users(login_data:UserLoginModel,session:AsyncSession=Depends(get_session)):
    email = login_data.email
    password = login_data.password
    user = await user_service.get_user_email(session,email)
    if user is not None:
        password_valid = verify_password(password,user.hashed_password)
        if password_valid:
            access_token = create_access_token(
                user_data={
                    'email':user.email,
                    'user_uid':str(user.uuid)
                }
            )
            refresh_token = create_access_token(
                user_data={
                    'email':user.email,
                    'user_uid':str(user.uuid)
                },
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY),
                refresh=True
            )
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    'message':'Login Successful',
                    'access_token':access_token,
                    'refresh_token':refresh_token,
                    'user':{
                        'email':user.email,
                        'user_uid':str(user.uuid)
                    }
                }
            )
    raise InvalidCreadentials()

@auth_router.post("/refresh-token")
async def get_new_access_token(token_details:dict=Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details['exp']

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(
            user_data = token_details['user']
        )
        return JSONResponse(content={
            'access_token':new_access_token
        })
    raise InvalidToken()

@auth_router.get('/logout')
async def revoke_token(token_details:dict=Depends(AccessTokenBearer())):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'message':'Logout Successful'
        }
    )
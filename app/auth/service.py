from .models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.auth.utilis import generate_passwd_hash
from app.auth.schema import UserCreateModel


class UserService:
    async def get_user_email(self, session: AsyncSession, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        result = await session.execute(statement)

        return result.scalars().first()
    
    async def user_exists(self, session: AsyncSession, email: str) -> bool:
        user = await self.get_user_email(session, email)
        return True if user is not None else False
    
    async def create_user(self, session: AsyncSession, user_data: UserCreateModel) -> User:
        user_data_dict = user_data.model_dump(exclude={'password'})

        new_user = User(
            **user_data_dict,
            hashed_password = generate_passwd_hash(user_data.password)
        )
       

        
        session.add(new_user)
        await session.commit()
        return new_user
    
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker,DeclarativeBase
from app.core.config import settings




#  Create Base for SQLAlchemy models
class Base(DeclarativeBase):
    pass

#  Create async engine correctly
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True
    
)

#Initialize database
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Create sessionmaker correctly
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)



# 4. Dependency for routes
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


from config import CONFIG

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Create async engine
engine = create_async_engine(CONFIG["database"], echo=False)

# Define Base
Base = declarative_base()
Base.metadata.bind = engine

async_session = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False, autocommit=False
)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

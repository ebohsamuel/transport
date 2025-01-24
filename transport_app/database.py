from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker, DeclarativeBase


# sqlite+aiosqlite:///./transport.db for local server"
DATABASE_URL = "postgresql+asyncpg://postgres:PG/eng1102493@localhost:5432/transport"

async_engine = create_async_engine(DATABASE_URL)

async_SessionLocal = async_sessionmaker(autoflush=False, bind=async_engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass

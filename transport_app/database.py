from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker, DeclarativeBase


# "postgresql://postgres:PG/eng1102493@localhost:5432/shop_application.db" for local server"
DATABASE_URL = "sqlite+aiosqlite:///./transport.db"

async_engine = create_async_engine(DATABASE_URL, connect_args={"check_same_thread": False})

async_SessionLocal = async_sessionmaker(autoflush=False, bind=async_engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass

from pathlib import Path
from typing import AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app import get_settings

settings = get_settings()

# This is to ensure the sqlite DB ends up in the same place as when
# created and managed by alembic
sqlite_path = (
    f"sqlite+aiosqlite:///{Path(__file__).absolute().parent.parent.parent}"
)

if settings.environment == "production":
    # Use postgres
    SQLALCHEMY_URL: str = (
        "postgresql+asyncpg://"
        f"{settings.postgres_user}:{settings.postgres_password}"
        f"@{settings.postgres_host}/{settings.postgres_db}"
    )
    engine = create_async_engine(
        SQLALCHEMY_URL,
        echo=False,
        pool_pre_ping=True,
        pool_size=64,
        max_overflow=200,
    )
else:
    SQLALCHEMY_URL = rf"{sqlite_path}/database.db"
    engine = create_async_engine(
        SQLALCHEMY_URL,
        echo=True,
        pool_pre_ping=True,
        connect_args={"check_same_thread": False},
    )

async_session = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


# get_session Dependency
async def get_session() -> AsyncGenerator:
    async with async_session() as session:
        yield session


metadata = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)

Base = declarative_base(metadata=metadata)
SQLModel.metadata = Base.metadata

__all__ = ["SQLModel"]

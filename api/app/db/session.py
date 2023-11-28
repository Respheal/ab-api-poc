from collections.abc import Generator

from sqlalchemy import Engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.ext.asyncio.session import AsyncSession

from app import settings

engine: AsyncEngine | Engine

if settings.environment == "production":
    # Use postgres
    engine = create_async_engine(
        (
            "postgresql+asyncpg://"
            f"{settings.postgres_user}:{settings.postgres_password}"
            f"@{settings.postgres_host}/{settings.postgres_db}"
        ),
        echo=True,
        pool_pre_ping=True,
        pool_size=64,
        max_overflow=200,
    )
else:
    engine = create_engine(
        "sqlite:///database.db",
        echo=True,
        pool_pre_ping=True,
        connect_args={"check_same_thread": False},
    )


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


async def get_session() -> Generator[AsyncSession | Session, None, None]:
    if settings.environment == "production":
        async_session = sessionmaker(
            bind=engine, class_=AsyncSession, expire_on_commit=False
        )
        async with async_session() as session:
            yield session
    else:
        with Session(engine) as session:
            yield session

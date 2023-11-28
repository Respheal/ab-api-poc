from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from app import get_settings

settings = get_settings()

if settings.environment == "production":
    # Use postgres
    SQLALCHEMY_URL: str = (
        "postgresql+asyncpg://"
        f"{settings.postgres_user}:{settings.postgres_password}"
        f"@{settings.postgres_host}/{settings.postgres_db}"
    )
    engine: AsyncEngine = create_async_engine(
        SQLALCHEMY_URL,
        echo=False,
        pool_pre_ping=True,
        pool_size=64,
        max_overflow=200,
    )
if settings.environment == "test":
    SQLALCHEMY_URL = "sqlite+aiosqlite:///test.db"
    engine = create_async_engine(
        SQLALCHEMY_URL,
        echo=False,
        pool_pre_ping=True,
        connect_args={"check_same_thread": False},
    )
else:
    SQLALCHEMY_URL = "sqlite+aiosqlite:///database.db"
    engine = create_async_engine(
        SQLALCHEMY_URL,
        echo=False,
        pool_pre_ping=True,
        connect_args={"check_same_thread": False},
    )


async_session = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


# get_session Dependency
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

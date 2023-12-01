from app.db.models import User
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession


async def get_users(
    session: AsyncSession, skip: int = 0, limit: int = 5000
) -> list[User]:
    users = await session.exec(
        select(User).order_by(User.id).offset(skip).limit(limit)
    )
    return users.all()


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    return await session.get(User, user_id)


async def get_user_by_name(session: AsyncSession, name: str):
    user = await session.exec(select(User).where(User.name == name))
    return user.first()

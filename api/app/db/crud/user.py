from typing import Sequence

from sqlmodel import col, select
from sqlmodel.ext.asyncio.session import AsyncSession

import app.utils.security as security_utils
from app.db.models import OpenIDUser, User, UserCreate
from app.utils.generators import namegenerator, passgenerator


async def get_users(
    session: AsyncSession,
    skip: int = 0,
    limit: int = 5000,
    email: str | None = None,
    oauth_id: str | None = None,
    oauth_provider: str | None = None,
) -> Sequence[User]:
    statement = select(User)
    if oauth_provider and oauth_id:
        statement = statement.join(OpenIDUser).where(
            OpenIDUser.openid == oauth_id,
            OpenIDUser.provider == oauth_provider,
        )
    if email:
        statement = statement.where(User.email == email)
    statement = statement.order_by(col(User.id)).offset(skip).limit(limit)
    users = await session.exec(statement)
    return users.all()


async def create_user(session: AsyncSession, user: UserCreate) -> User:
    if not user.name:
        user.name = namegenerator()
    if not user.password:
        user.password = passgenerator()
    db_user: User = User.model_validate(user)
    db_user.hashed_password = security_utils.get_password_hash(user.password)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    if user.oauth_id and user.oauth_provider:
        openid_user = OpenIDUser(
            user=db_user.id, openid=user.oauth_id, provider=user.oauth_provider
        )
        session.add(openid_user)
        await session.commit()

    return db_user


async def get_user(session: AsyncSession, id: int) -> User | None:
    return await session.get(User, id)


async def get_user_by_name(session: AsyncSession, name: str) -> User | None:
    user = await session.exec(select(User).where(User.name == name))
    return user.first()

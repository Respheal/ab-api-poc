from typing import Sequence

from sqlmodel import col, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.models import Comic, ComicCreate


async def get_comics(
    session: AsyncSession,
    skip: int = 0,
    limit: int = 5000,
) -> Sequence[Comic]:
    statement = select(Comic)
    statement = statement.order_by(col(Comic.id)).offset(skip).limit(limit)
    comics = await session.exec(statement)
    return comics.all()


async def get_comic(session: AsyncSession, id: int) -> Comic | None:
    return await session.get(Comic, id)


async def create_comic(session: AsyncSession, comic: ComicCreate) -> Comic:
    db_comic = Comic.model_validate(comic)
    session.add(db_comic)
    await session.commit()
    await session.refresh(db_comic)

    return db_comic

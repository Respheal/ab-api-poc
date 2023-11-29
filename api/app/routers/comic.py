from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.models import Comic, ComicCreate, ComicRead, ComicList
from app.db.session import get_session

router = APIRouter(
    prefix="/comic",
    tags=["comic"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[ComicList])
async def get_comics(
    session: AsyncSession = Depends(get_session),
) -> Sequence[Comic]:
    comics = await session.exec(select(Comic))
    return comics.all()


@router.get("/{id}", response_model=ComicRead)
async def get_comic(
    *, session: AsyncSession = Depends(get_session), id: int
) -> Comic:
    comic = await session.get(Comic, id)
    if not comic:
        raise HTTPException(status_code=404, detail="Comic not found")
    return comic


@router.post("/", response_model=ComicRead)
async def create_comic(
    *, session: AsyncSession = Depends(get_session), comic: ComicCreate
) -> Comic:
    db_comic = Comic.from_orm(comic)
    session.add(db_comic)
    await session.commit()
    await session.refresh(db_comic)

    return db_comic

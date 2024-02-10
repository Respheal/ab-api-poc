from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.crud import comic as crud_comic
from app.db.models import Comic, ComicCreate, ComicList
from app.db.session import get_session

router = APIRouter(
    prefix="/comic",
    tags=["comic"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[ComicList])
async def get_comics(
    session: AsyncSession = Depends(get_session),
    skip: int = 0,
    limit: int = 5000,
) -> Sequence[Comic]:
    return await crud_comic.get_comics(session, skip, limit)


@router.get("/{id}", response_model=Comic)
async def get_comic(
    *, session: AsyncSession = Depends(get_session), id: int
) -> Comic:
    comic = await session.get(Comic, id)
    if not comic:
        raise HTTPException(status_code=404, detail="Comic not found")
    return comic


@router.post("/", response_model=Comic)
async def create_comic(
    *, session: AsyncSession = Depends(get_session), comic: ComicCreate
) -> Comic:
    return await crud_comic.create_comic(session, comic)

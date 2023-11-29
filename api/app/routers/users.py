from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.models import (
    User,
    UserCreate,
    # UserReadWithRecipes,
)
from app.db.session import get_session


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[User])
async def read_users(
    session: AsyncSession = Depends(get_session),
) -> Sequence[User]:
    users = await session.exec(select(User))
    return users.all()


# @router.get("/{user_id}", response_model=UserReadWithRecipes)
# async def read_user(
#     *, session: AsyncSession = Depends(get_session), user_id: int
# ) -> User:
#     user = await session.get(User, user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user


@router.post("/", response_model=User)
async def create_user(
    *, session: AsyncSession = Depends(get_session), user: UserCreate
) -> User:
    db_user = User.from_orm(user)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user

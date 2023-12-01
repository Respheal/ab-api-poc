from typing import Sequence

from app.db.crud import user as crud_user
from app.db.models import User, UserCreate, UserReadWithSubs
from app.db.session import get_session
from app.utils.security import get_password_hash
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[User])
async def read_users(
    session: AsyncSession = Depends(get_session),
    skip: int = 0,
    limit: int = 5000,
) -> Sequence[User]:
    return await crud_user.get_users(session, skip, limit)


@router.get("/{user_id}", response_model=UserReadWithSubs)
async def read_user(
    *, session: AsyncSession = Depends(get_session), user_id: int
) -> User:
    user: User | None = await crud_user.get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", response_model=User)
async def create_user(
    *, session: AsyncSession = Depends(get_session), user: UserCreate
) -> User:
    db_user = User.from_orm(
        user, {"hashed_password": get_password_hash(user.password)}
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user

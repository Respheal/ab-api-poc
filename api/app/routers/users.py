from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.crud import user as crud_user
from app.db.models import User, UserCreate, UserReadWithSubs
from app.db.session import get_session
from app.utils.security import get_current_user

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
    email: str | None = None,
    oauth_id: str | None = None,
    oauth_provider: str | None = None,
) -> Sequence[User]:
    # oauth id and provider must both be empty or both have values
    if bool(oauth_id) != bool(oauth_provider):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "OAuth ID and Provider must both be empty or both have values."
            ),
        )
    return await crud_user.get_users(
        session, skip, limit, email, oauth_id, oauth_provider
    )


@router.get("/{user_id}", response_model=UserReadWithSubs)
async def read_user(
    *, session: AsyncSession = Depends(get_session), user_id: int
) -> User:
    user: User | None = await crud_user.get_user(session, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.post("/", response_model=User)
async def create_user(
    *, session: AsyncSession = Depends(get_session), user: UserCreate
) -> User:
    # oauth id and provider must both be empty or both have values
    if bool(user.oauth_id) != bool(user.oauth_provider):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "OAuth ID and Provider must both be empty or both have values."
            ),
        )
    # Check if the user already exists
    check_user: Sequence[User] = await crud_user.get_users(
        session,
        email=user.email,
        oauth_id=user.oauth_id,
        oauth_provider=user.oauth_provider,
    )
    if check_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=("User already exists."),
        )
    return await crud_user.create_user(session, user)


@router.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    return current_user

from typing import Annotated, Sequence

from app.db.crud import user as crud_user
from app.db.models import OpenIDUser, User, UserCreate, UserReadWithSubs
from app.db.session import get_session
from app.utils.security import get_current_user, get_password_hash
from fastapi import APIRouter, Body, Depends, HTTPException, status
from google.auth.transport import requests
from google.oauth2 import id_token
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
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


@router.post("/google", response_model=User)
async def create_google_user(
    *,
    session: AsyncSession = Depends(get_session),
    jwt: Annotated[str, Body(embed=True)]
) -> User:
    # Specify the CLIENT_ID of the app that accesses the backend:
    idinfo = id_token.verify_oauth2_token(
        jwt,
        requests.Request(),
        "751923381039-do8cbpk1fljvos3k118r3n1tuscfhllv.apps.googleusercontent.com",
        clock_skew_in_seconds=2,
    )

    # except ValueError:
    #     # Invalid token
    #     pass

    db_user = User(
        name="weh",
        email=idinfo["email"],
        hashed_password=get_password_hash("aaaaaaaa"),
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    openid_user = OpenIDUser(
        user=db_user.id, openid=idinfo["sub"], provider="google"
    )
    session.add(openid_user)
    await session.commit()

    return db_user


@router.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user

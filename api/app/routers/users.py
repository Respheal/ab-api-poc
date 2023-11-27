from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.db.models import (
    User,
    UserReadWithRecipes,
)
from app.db.session import get_session

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[User])
def read_users(session: Session = Depends(get_session)) -> Sequence[User]:
    return session.exec(select(User)).all()


@router.get("/{user_id}", response_model=UserReadWithRecipes)
def read_user(
    *, session: Session = Depends(get_session), user_id: int
) -> User:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", response_model=User)
def create_user(
    *, session: Session = Depends(get_session), user: User
) -> User:
    db_user = User.from_orm(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

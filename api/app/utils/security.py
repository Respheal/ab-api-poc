from datetime import datetime, timedelta
from typing import Annotated, Any

import bcrypt
from authlib.jose import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel.ext.asyncio.session import AsyncSession

from app import get_settings
from app.db.crud.user import get_user_by_name
from app.db.models import TokenData, User
from app.db.session import get_session

settings = get_settings()

SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"
HEADER = {"alg": ALGORITHM}
ACCESS_TOKEN_EXPIRE_MINUTES = settings.token_expiration
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Check if the provided password matches the stored password (hashed)
    return bcrypt.checkpw(
        password=plain_password.encode("utf-8"),
        hashed_password=hashed_password.encode("utf-8"),
    )


def get_password_hash(password: str) -> str:
    # Hash a password using bcrypt
    return str(
        bcrypt.hashpw(password=password.encode("utf-8"), salt=bcrypt.gensalt())
    )


async def authenticate_user(
    session: AsyncSession, username: str, password: str
) -> User | None:
    user: User | None = await get_user_by_name(session, username)
    if not user:
        return None
    if not user.hashed_password:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(
    data: dict[str, Any], expires_delta: timedelta | None = None
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    # encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    encoded_jwt = jwt.encode(header=HEADER, payload=to_encode, key=SECRET_KEY)
    return str(encoded_jwt)


async def get_current_user(
    session: Annotated[AsyncSession, Depends(get_session)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # try:
    # payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    payload = jwt.decode(token, SECRET_KEY)
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    token_data = TokenData(username=username)
    if token_data.username is None:
        raise credentials_exception
    # except JWTError:
    #     raise credentials_exception
    user: User | None = await get_user_by_name(
        session, name=token_data.username
    )
    if user is None:
        raise credentials_exception
    return user


# async def get_current_active_user(
#     current_user: Annotated[User, Depends(get_current_user)]
# ):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user

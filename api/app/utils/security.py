from datetime import datetime, timedelta
from typing import Annotated

from app.db.crud.user import get_user_by_name
from app.db.models import TokenData, User
from app.db.session import get_session
from authlib.jose import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlmodel.ext.asyncio.session import AsyncSession

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "4d7a2388684b2a1597348ff66e1da8bbcaa98c0c75e579ce8ff7a6c7f4167b12"
ALGORITHM = "HS256"
HEADER = {"alg": ALGORITHM}
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bool(PWD_CONTEXT.verify(plain_password, hashed_password))


def get_password_hash(password: str) -> str:
    return str(PWD_CONTEXT.hash(password))


async def authenticate_user(
    session: AsyncSession, username: str, password: str
) -> User | None:
    user: User | None = await get_user_by_name(session, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(
    data: dict, expires_delta: timedelta | None = None
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    # encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    encoded_jwt = jwt.encode(header=HEADER, payload=to_encode, key=SECRET_KEY)
    return encoded_jwt


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

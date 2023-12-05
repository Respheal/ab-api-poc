from app.db.session import SQLModel
from pydantic import BaseModel
from sqlmodel import JSON, Column, Field, Relationship


# Pydantic-only Schemas
class HealthCheck(BaseModel):
    name: str
    version: str
    description: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


# Association Tables
class ComicSubs(SQLModel, table=True):
    user_id: int = Field(default=None, foreign_key="user.id", primary_key=True)
    comic_id: int = Field(
        default=None, foreign_key="comic.id", primary_key=True
    )


# Base Tables
# Comic
class ComicBase(SQLModel):
    name: str


class ComicList(ComicBase):
    id: int


class ComicInfo(ComicBase):
    image: str | None = Field(max_length=256, nullable=True)
    summary: str | None = Field(max_length=1000, nullable=True)
    creator: str | None = Field(max_length=100, nullable=True)
    rating_enabled: bool = Field(default=False)
    status: str | None = Field(max_length=256, nullable=True)
    frequency: str | None = Field(max_length=256, nullable=True)
    rss: str | None = Field(max_length=256, nullable=True)


class ComicRead(ComicInfo):
    """Add pages when viewing an individual comic."""

    pages: list[str] = []


class Comic(ComicBase, table=True):
    """SQL-specific Comic fields and attributes."""

    id: int | None = Field(default=None, index=True, primary_key=True)
    rating_enabled: bool = Field(default=False)
    pages: list[str] = Field(sa_column=Column(JSON))

    subscribers: list["User"] = Relationship(
        back_populates="subs", link_model=ComicSubs
    )


class ComicCreate(ComicBase):
    summary: str | None = None
    creator: str | None = None
    status: str | None = None
    frequency: str | None = None
    rss: str | None = None
    pages: list[str] = []


# User
class UserBase(SQLModel):
    """Common User fields."""

    name: str
    email: str | None = Field(nullable=True)
    is_superuser: bool = Field(default=False)


class User(UserBase, table=True):
    """SQL-specific User fields."""

    id: int | None = Field(default=None, index=True, primary_key=True)
    hashed_password: str = Field(nullable=False)

    subs: list["Comic"] = Relationship(
        back_populates="subscribers",
        link_model=ComicSubs,
        sa_relationship_kwargs={
            "lazy": "selectin",  # https://docs.sqlalchemy.org/en/14/orm/loading_relationships.html#relationship-loading-techniques  # noqa
        },
    )


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int


class UserUpdate(SQLModel):
    name: str | None = None
    email: str | None = None


class UserReadWithSubs(UserRead):
    subs: list[ComicBase] = []


class OpenIDUser(SQLModel, table=True):
    id: int = Field(default=None, index=True, primary_key=True)
    user: int = Field(default=None, foreign_key="user.id")
    openid: str
    provider: str


# class UserBase(SQLModel):
#     name: str = Field(index=True)
#     email: str = Field(index=True, nullable=False)
#     is_superuser: bool = Field(default=False)


# class User(UserBase, table=True):
#     id: int | None = Field(default=None, primary_key=True)

#     recipes: list["Recipe"] = Relationship(
#         back_populates="submitter",
#         sa_relationship_kwargs={
#             "cascade": "all,delete,delete-orphan",
#             "lazy": "selectin",  # https://docs.sqlalchemy.org/en/14/orm/loading_relationships.html#relationship-loading-techniques  # noqa
#         },
#     )


# class UserCreate(UserBase):
#     pass


# class UserRead(UserBase):
#     id: int


# class UserUpdate(SQLModel):
#     id: int | None = None
#     name: str | None = None
#     headquarters: str | None = None


# class RecipeBase(SQLModel):
#     label: str = Field(max_length=256, nullable=False)
#     url: str = Field(max_length=256, index=True, nullable=True)
#     source: str = Field(max_length=256, nullable=True)

#     submitter_id: int | None = Field(default=None, foreign_key="user.id")


# class Recipe(RecipeBase, table=True):
#     id: int | None = Field(default=None, primary_key=True)

#     submitter: User | None = Relationship(back_populates="recipes")


# class RecipeCreate(RecipeBase):
#     pass


# class RecipeRead(RecipeBase):
#     id: int


# class RecipeReadWithUser(RecipeRead):
#     submitter: UserRead | None = None


# class UserReadWithRecipes(UserRead):
#     recipes: list[RecipeRead] = []

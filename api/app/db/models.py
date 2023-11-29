from sqlmodel import Field, Relationship
from pydantic import BaseModel

from app.db.session import SQLModel


class HealthCheck(BaseModel):
    name: str
    version: str
    description: str


class UserBase(SQLModel):
    name: str = Field(index=True)
    headquarters: str
    first_name: str = Field(max_length=256, nullable=True)
    surname: str = Field(max_length=256, nullable=True)
    email: str = Field(index=True, nullable=False)
    is_superuser: bool = Field(default=False)


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    recipes: list["Recipe"] = Relationship(
        back_populates="submitter",
        sa_relationship_kwargs={
            "cascade": "all,delete,delete-orphan",
            "lazy": "selectin",  # https://docs.sqlalchemy.org/en/14/orm/loading_relationships.html#relationship-loading-techniques
        },
    )


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int


class UserUpdate(SQLModel):
    id: int | None = None
    name: str | None = None
    headquarters: str | None = None


class RecipeBase(SQLModel):
    label: str = Field(max_length=256, nullable=False)
    url: str = Field(max_length=256, index=True, nullable=True)
    source: str = Field(max_length=256, nullable=True)

    submitter_id: int | None = Field(default=None, foreign_key="user.id")


class Recipe(RecipeBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    submitter: User | None = Relationship(back_populates="recipes")


class RecipeCreate(RecipeBase):
    pass


class RecipeRead(RecipeBase):
    id: int


class RecipeReadWithUser(RecipeRead):
    submitter: UserRead | None = None


class UserReadWithRecipes(UserRead):
    recipes: list[RecipeRead] = []

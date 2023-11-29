from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.models import (
    RecipeCreate,
    RecipeRead,
    Recipe,
    User,
    RecipeReadWithUser,
)
from app.db.session import get_session

router = APIRouter(
    prefix="/recipes",
    tags=["recipes"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[RecipeRead])
async def read_recipes(
    session: AsyncSession = Depends(get_session),
) -> Sequence[Recipe]:
    recipes = await session.exec(select(Recipe))
    return recipes.all()


@router.get("/{id}", response_model=RecipeReadWithUser)
async def read_recipe(
    *, session: AsyncSession = Depends(get_session), id: int
) -> Recipe:
    recipe = await session.get(Recipe, id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@router.post("/", response_model=RecipeRead)
async def create_recipe(
    *, session: AsyncSession = Depends(get_session), recipe: RecipeCreate
) -> Recipe:
    db_recipe = Recipe.from_orm(recipe)
    db_recipe.submitter_id = 1
    session.add(db_recipe)

    user = await session.get(User, 1)
    if user:
        user.recipes.append(db_recipe)
        session.add(user)
    await session.commit()

    await session.refresh(db_recipe)

    return db_recipe

from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

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
def read_recipes(session: Session = Depends(get_session)) -> Sequence[Recipe]:
    recipes = session.exec(select(Recipe)).all()
    return recipes


@router.get("/", response_model=RecipeReadWithUser)
def read_recipe(*, session: Session = Depends(get_session), id: int) -> Recipe:
    recipe = session.get(Recipe, id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@router.post("/", response_model=RecipeRead)
def create_recipe(
    *, session: Session = Depends(get_session), recipe: RecipeCreate
) -> Recipe:
    db_recipe = Recipe.from_orm(recipe)
    db_recipe.submitter_id = 1
    session.add(db_recipe)

    user = session.get(User, 1)
    if user:
        user.recipes.append(db_recipe)
        session.add(user)
    session.commit()

    session.refresh(db_recipe)

    return db_recipe

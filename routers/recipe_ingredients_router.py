from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from schemas import (
    RecipeIngredientCreate,
    RecipeIngredientUpdate,
    RecipeIngredientRead,
)
from services.recipe_ingredient_service import RecipeIngredientService


router = APIRouter(
    prefix="/recipes/{recipe_id}/ingredients",
    tags=["Recipe Ingredients"],
)

DbSession = Annotated[Session, Depends(get_db)]


@router.get("/", response_model=list[RecipeIngredientRead])
def get_recipe_ingredients(recipe_id: int, db: DbSession):
    return RecipeIngredientService.get_all(db, recipe_id)


@router.post(
    "/",
    response_model=RecipeIngredientRead,
    status_code=status.HTTP_201_CREATED,
)
def add_recipe_ingredient(
    recipe_id: int,
    data: RecipeIngredientCreate,
    db: DbSession,
):
    return RecipeIngredientService.add(db, recipe_id, data)


@router.put(
    "/{ingredient_id}",
    response_model=RecipeIngredientRead,
)
def update_recipe_ingredient(
    recipe_id: int,
    ingredient_id: int,
    data: RecipeIngredientUpdate,
    db: DbSession,
):
    return RecipeIngredientService.update(
        db,
        recipe_id,
        ingredient_id,
        data,
    )


@router.delete(
    "/{ingredient_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_recipe_ingredient(
    recipe_id: int,
    ingredient_id: int,
    db: DbSession,
):
    RecipeIngredientService.delete(db, recipe_id, ingredient_id)
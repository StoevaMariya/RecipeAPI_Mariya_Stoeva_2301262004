from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import RecipeIngredient
from schemas import (
    RecipeCreate,
    RecipeRead,
    RecipeUpdate,
    ScaledRecipe,
)
from services.recipe_service import RecipeService


router = APIRouter(prefix="/recipes", tags=["Recipes"])

DbSession = Annotated[Session, Depends(get_db)]


# GET - All recipes with optional filters
@router.get("/", response_model=list[RecipeRead])
def get_recipes(
    db: DbSession,
    title: str | None = None,
    category_id: int | None = Query(default=None, gt=0),
    max_prep_time: int | None = Query(default=None, gt=0),
):
    return RecipeService.get_all(
        db,
        title=title,
        category_id=category_id,
        max_prep_time=max_prep_time,
    )


# POST - Create a recipe
@router.post(
    "/",
    response_model=RecipeRead,
    status_code=status.HTTP_201_CREATED,
)
def create_recipe(data: RecipeCreate, db: DbSession):
    return RecipeService.create(db, data)


# GET - Get a recipe by ID
@router.get("/{recipe_id}", response_model=RecipeRead)
def get_recipe(recipe_id: int, db: DbSession):
    return RecipeService.get_by_id(db, recipe_id)


# PUT - Update a recipe
@router.put("/{recipe_id}", response_model=RecipeRead)
def update_recipe(
    recipe_id: int,
    data: RecipeUpdate,
    db: DbSession,
):
    return RecipeService.update(db, recipe_id, data)


# DELETE - Delete a recipe
@router.delete(
    "/{recipe_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_recipe(recipe_id: int, db: DbSession):
    RecipeService.delete(db, recipe_id)


# GET - Scale recipe ingredients for 1 to 54 servings
@router.get("/{recipe_id}/scaled", response_model=ScaledRecipe)
def get_scaled_recipe(
    recipe_id: int,
    db: DbSession,
    requested_servings: int = Query(ge=1, le=54),
):
    recipe = RecipeService.get_by_id(db, recipe_id)

    ingredients = db.scalars(
        select(RecipeIngredient).where(
            RecipeIngredient.recipe_id == recipe_id
        )
    ).all()

    scaled_ingredients = [
        {
            "ingredient_id": item.ingredient_id,
            "quantity": item.quantity * requested_servings / recipe.servings,
            "unit": item.unit,
        }
        for item in ingredients
    ]

    return {
        "recipe": recipe,
        "requested_servings": requested_servings,
        "ingredients": scaled_ingredients,
    }
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Ingredient, RecipeIngredient
from schemas import (
    RecipeIngredientCreate,
    RecipeIngredientUpdate,
)
from services.recipe_service import RecipeService


class RecipeIngredientService:

    @staticmethod
    def get_all(db: Session, recipe_id: int):
        RecipeService.get_by_id(db, recipe_id)

        return db.scalars(
            select(RecipeIngredient).where(
                RecipeIngredient.recipe_id == recipe_id
            )
        ).all()

    @staticmethod
    def add(db: Session, recipe_id: int, data: RecipeIngredientCreate):
        RecipeService.get_by_id(db, recipe_id)

        ingredient = db.get(Ingredient, data.ingredient_id)

        if ingredient is None:
            raise HTTPException(
                status_code=404,
                detail="Ingredient not found"
            )

        existing = db.get(
            RecipeIngredient,
            (recipe_id, data.ingredient_id)
        )

        if existing is not None:
            raise HTTPException(
                status_code=409,
                detail="Ingredient already added to recipe"
            )

        recipe_ingredient = RecipeIngredient(
            recipe_id=recipe_id,
            ingredient_id=data.ingredient_id,
            quantity=data.quantity,
            unit=data.unit,
        )

        db.add(recipe_ingredient)
        db.commit()
        db.refresh(recipe_ingredient)

        return recipe_ingredient

    @staticmethod
    def update(
        db: Session,
        recipe_id: int,
        ingredient_id: int,
        data: RecipeIngredientUpdate
    ):
        RecipeService.get_by_id(db, recipe_id)

        recipe_ingredient = db.get(
            RecipeIngredient,
            (recipe_id, ingredient_id)
        )

        if recipe_ingredient is None:
            raise HTTPException(
                status_code=404,
                detail="Ingredient not found in recipe"
            )

        recipe_ingredient.quantity = data.quantity
        recipe_ingredient.unit = data.unit

        db.commit()
        db.refresh(recipe_ingredient)

        return recipe_ingredient

    @staticmethod
    def delete(
        db: Session,
        recipe_id: int,
        ingredient_id: int
    ):
        RecipeService.get_by_id(db, recipe_id)

        recipe_ingredient = db.get(
            RecipeIngredient,
            (recipe_id, ingredient_id)
        )

        if recipe_ingredient is None:
            raise HTTPException(
                status_code=404,
                detail="Ingredient not found in recipe"
            )

        db.delete(recipe_ingredient)
        db.commit()
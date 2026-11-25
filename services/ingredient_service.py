from fastapi import HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from models import Ingredient, RecipeIngredient
from schemas import IngredientCreate, IngredientUpdate


class IngredientService:

    @staticmethod
    def get_all(db: Session):
        return db.scalars(select(Ingredient)).all()

    @staticmethod
    def get_by_id(db: Session, ingredient_id: int):
        ingredient = db.get(Ingredient, ingredient_id)

        if ingredient is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ingredient not found"
            )

        return ingredient

    @staticmethod
    def check_duplicate(
        db: Session,
        name: str,
        exclude_id: int | None = None
    ):
        query = select(Ingredient).where(
            func.lower(Ingredient.name) == name.lower()
        )

        if exclude_id is not None:
            query = query.where(Ingredient.id != exclude_id)

        if db.scalar(query):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ingredient name already exists"
            )

    @staticmethod
    def create(db: Session, data: IngredientCreate):
        IngredientService.check_duplicate(db, data.name)

        ingredient = Ingredient(**data.model_dump())
        db.add(ingredient)
        db.commit()
        db.refresh(ingredient)

        return ingredient

    @staticmethod
    def update(db: Session, ingredient_id: int, data: IngredientUpdate):
        ingredient = IngredientService.get_by_id(db, ingredient_id)

        IngredientService.check_duplicate(
            db,
            data.name,
            exclude_id=ingredient_id
        )

        ingredient.name = data.name

        db.commit()
        db.refresh(ingredient)

        return ingredient

    @staticmethod
    def delete(db: Session, ingredient_id: int):
        ingredient = IngredientService.get_by_id(db, ingredient_id)

        in_use = db.scalar(
            select(RecipeIngredient.recipe_id).where(
                RecipeIngredient.ingredient_id == ingredient_id
            )
        )

        if in_use is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Cannot delete ingredient used in recipes"
            )

        db.delete(ingredient)
        db.commit()
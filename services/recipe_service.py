from fastapi import HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from models import Author, Category, Recipe
from schemas import RecipeCreate, RecipeUpdate


class RecipeService:

    @staticmethod
    def get_by_id(db: Session, recipe_id: int):
        recipe = db.get(Recipe, recipe_id)

        if recipe is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recipe not found"
            )

        return recipe

    @staticmethod
    def get_all(
        db: Session,
        title: str | None = None,
        category_id: int | None = None,
        max_prep_time: int | None = None
    ):
        query = select(Recipe)

        if title is not None:
            query = query.where(
                func.lower(Recipe.title).contains(title.strip().lower())
            )

        if category_id is not None:
            query = query.where(Recipe.category_id == category_id)

        if max_prep_time is not None:
            query = query.where(
                Recipe.prep_time <= max_prep_time
            )

        return db.scalars(query).all()

    @staticmethod
    def validate_relations(
        db: Session,
        author_id: int,
        category_id: int | None
    ):
        if db.get(Author, author_id) is None:
            raise HTTPException(
                status_code=404,
                detail="Author not found"
            )

        if category_id is not None:
            if db.get(Category, category_id) is None:
                raise HTTPException(
                    status_code=404,
                    detail="Category not found"
                )

    @staticmethod
    def check_duplicate(
        db: Session,
        author_id: int,
        title: str,
        exclude_id: int | None = None
    ):
        title_key = title.strip().casefold()

        query = select(Recipe).where(
            Recipe.author_id == author_id,
            Recipe.title_key == title_key
        )

        if exclude_id is not None:
            query = query.where(Recipe.id != exclude_id)

        if db.scalar(query):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Author already has a recipe with this title"
            )

        return title_key

    @staticmethod
    def create(db: Session, data: RecipeCreate):
        RecipeService.validate_relations(
            db, data.author_id, data.category_id
        )

        title_key = RecipeService.check_duplicate(
            db, data.author_id, data.title
        )

        recipe = Recipe(
            **data.model_dump(),
            title_key=title_key
        )

        db.add(recipe)
        db.commit()
        db.refresh(recipe)

        return recipe

    @staticmethod
    def update(db: Session, recipe_id: int, data: RecipeUpdate):
        recipe = RecipeService.get_by_id(db, recipe_id)

        RecipeService.validate_relations(
            db, data.author_id, data.category_id
        )

        title_key = RecipeService.check_duplicate(
            db,
            data.author_id,
            data.title,
            exclude_id=recipe_id
        )

        for key, value in data.model_dump().items():
            setattr(recipe, key, value)

        recipe.title_key = title_key

        db.commit()
        db.refresh(recipe)

        return recipe

    @staticmethod
    def delete(db: Session, recipe_id: int):
        recipe = RecipeService.get_by_id(db, recipe_id)

        db.delete(recipe)
        db.commit()

    @staticmethod
    def get_by_author(db: Session, author_id: int):
        if db.get(Author, author_id) is None:
            raise HTTPException(
                status_code=404,
                detail="Author not found"
            )

        return db.scalars(
            select(Recipe).where(Recipe.author_id == author_id)
        ).all()
from fastapi import HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from models import Category
from schemas import CategoryCreate, CategoryUpdate


class CategoryService:

    @staticmethod
    def get_all(db: Session):
        return db.scalars(select(Category)).all()

    @staticmethod
    def get_by_id(db: Session, category_id: int):
        category = db.get(Category, category_id)

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )

        return category

    @staticmethod
    def check_duplicate(
        db: Session,
        name: str,
        exclude_id: int | None = None
    ):
        query = select(Category).where(
            func.lower(Category.name) == name.lower()
        )

        if exclude_id is not None:
            query = query.where(Category.id != exclude_id)

        if db.scalar(query):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Category name already exists"
            )

    @staticmethod
    def create(db: Session, data: CategoryCreate):
        CategoryService.check_duplicate(db, data.name)

        category = Category(**data.model_dump())
        db.add(category)
        db.commit()
        db.refresh(category)

        return category

    @staticmethod
    def update(db: Session, category_id: int, data: CategoryUpdate):
        category = CategoryService.get_by_id(db, category_id)

        CategoryService.check_duplicate(
            db,
            data.name,
            exclude_id=category_id
        )

        category.name = data.name

        db.commit()
        db.refresh(category)

        return category

    @staticmethod
    def delete(db: Session, category_id: int):
        category = CategoryService.get_by_id(db, category_id)

        db.delete(category)
        db.commit()
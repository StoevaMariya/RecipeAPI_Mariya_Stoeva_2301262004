from fastapi import HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from models import Author, Recipe
from schemas import AuthorCreate, AuthorUpdate


class AuthorService:

    @staticmethod
    def get_all(db: Session):
        return db.scalars(select(Author)).all()

    @staticmethod
    def get_by_id(db: Session, author_id: int):
        author = db.get(Author, author_id)

        if author is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Author not found"
            )

        return author

    @staticmethod
    def create(db: Session, data: AuthorCreate):
        existing = db.scalar(
            select(Author).where(
                func.lower(Author.email) == data.email.lower()
            )
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Author email already exists"
            )

        author = Author(**data.model_dump())
        db.add(author)
        db.commit()
        db.refresh(author)

        return author

    @staticmethod
    def update(db: Session, author_id: int, data: AuthorUpdate):
        author = AuthorService.get_by_id(db, author_id)

        existing = db.scalar(
            select(Author).where(
                func.lower(Author.email) == data.email.lower(),
                Author.id != author_id
            )
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Author email already exists"
            )

        for key, value in data.model_dump().items():
            setattr(author, key, value)

        db.commit()
        db.refresh(author)

        return author

    @staticmethod
    def delete(db: Session, author_id: int):
        author = AuthorService.get_by_id(db, author_id)

        has_recipes = db.scalar(
            select(Recipe.id).where(Recipe.author_id == author_id)
        )

        if has_recipes is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Cannot delete author with recipes"
            )

        db.delete(author)
        db.commit()
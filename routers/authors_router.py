from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from schemas import AuthorCreate, AuthorUpdate, AuthorRead, RecipeRead
from services.author_service import AuthorService
from services.recipe_service import RecipeService


router = APIRouter(prefix="/authors", tags=["Authors"])

DbSession = Annotated[Session, Depends(get_db)]


@router.get("/", response_model=list[AuthorRead])
def get_authors(db: DbSession):
    return AuthorService.get_all(db)


@router.get("/{author_id}", response_model=AuthorRead)
def get_author(author_id: int, db: DbSession):
    return AuthorService.get_by_id(db, author_id)


@router.post(
    "/",
    response_model=AuthorRead,
    status_code=status.HTTP_201_CREATED
)
def create_author(data: AuthorCreate, db: DbSession):
    return AuthorService.create(db, data)


@router.put("/{author_id}", response_model=AuthorRead)
def update_author(
    author_id: int,
    data: AuthorUpdate,
    db: DbSession
):
    return AuthorService.update(db, author_id, data)


@router.delete(
    "/{author_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_author(author_id: int, db: DbSession):
    AuthorService.delete(db, author_id)


@router.get("/{author_id}/recipes", response_model=list[RecipeRead])
def get_author_recipes(author_id: int, db: DbSession):
    return RecipeService.get_by_author(db, author_id)
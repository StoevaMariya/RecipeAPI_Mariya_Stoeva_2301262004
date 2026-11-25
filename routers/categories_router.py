from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from schemas import CategoryCreate, CategoryUpdate, CategoryRead
from services.category_service import CategoryService


router = APIRouter(prefix="/categories", tags=["Categories"])

DbSession = Annotated[Session, Depends(get_db)]


@router.get("/", response_model=list[CategoryRead])
def get_categories(db: DbSession):
    return CategoryService.get_all(db)


@router.get("/{category_id}", response_model=CategoryRead)
def get_category(category_id: int, db: DbSession):
    return CategoryService.get_by_id(db, category_id)


@router.post(
    "/",
    response_model=CategoryRead,
    status_code=status.HTTP_201_CREATED
)
def create_category(data: CategoryCreate, db: DbSession):
    return CategoryService.create(db, data)


@router.put("/{category_id}", response_model=CategoryRead)
def update_category(
    category_id: int,
    data: CategoryUpdate,
    db: DbSession
):
    return CategoryService.update(db, category_id, data)


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_category(category_id: int, db: DbSession):
    CategoryService.delete(db, category_id)
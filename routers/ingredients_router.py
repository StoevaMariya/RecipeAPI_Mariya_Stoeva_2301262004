from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from schemas import IngredientCreate, IngredientUpdate, IngredientRead
from services.ingredient_service import IngredientService


router = APIRouter(prefix="/ingredients", tags=["Ingredients"])

DbSession = Annotated[Session, Depends(get_db)]


@router.get("/", response_model=list[IngredientRead])
def get_ingredients(db: DbSession):
    return IngredientService.get_all(db)


@router.get("/{ingredient_id}", response_model=IngredientRead)
def get_ingredient(ingredient_id: int, db: DbSession):
    return IngredientService.get_by_id(db, ingredient_id)


@router.post(
    "/",
    response_model=IngredientRead,
    status_code=status.HTTP_201_CREATED
)
def create_ingredient(data: IngredientCreate, db: DbSession):
    return IngredientService.create(db, data)


@router.put("/{ingredient_id}", response_model=IngredientRead)
def update_ingredient(
    ingredient_id: int,
    data: IngredientUpdate,
    db: DbSession
):
    return IngredientService.update(db, ingredient_id, data)


@router.delete(
    "/{ingredient_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_ingredient(ingredient_id: int, db: DbSession):
    IngredientService.delete(db, ingredient_id)
from typing import Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
)


class CleanText(BaseModel):
    @field_validator("*", mode="before", check_fields=False)
    @classmethod
    def clean_text(cls, value):
        return value.strip() if isinstance(value, str) else value


class AuthorCreate(CleanText):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr


class AuthorUpdate(AuthorCreate):
    pass


class AuthorRead(AuthorCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int


class CategoryCreate(CleanText):
    name: str = Field(min_length=1, max_length=100)


class CategoryUpdate(CategoryCreate):
    pass


class CategoryRead(CategoryCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int


class IngredientCreate(CleanText):
    name: str = Field(min_length=1, max_length=100)


class IngredientUpdate(IngredientCreate):
    pass


class IngredientRead(IngredientCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int


class RecipeCreate(CleanText):
    title: str = Field(min_length=1, max_length=200)
    instructions: str = Field(min_length=1)
    prep_time: int = Field(gt=0)
    servings: int = Field(gt=0)
    difficulty: Literal["easy", "medium", "hard"]
    author_id: int = Field(gt=0)
    category_id: int | None = Field(default=None, gt=0)


class RecipeUpdate(RecipeCreate):
    pass


class RecipeRead(RecipeCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int


class RecipeIngredientCreate(BaseModel):
    ingredient_id: int = Field(gt=0)
    quantity: float = Field(gt=0)
    unit: Literal["g", "ml", "pcs"]


class RecipeIngredientUpdate(BaseModel):
    quantity: float = Field(gt=0)
    unit: Literal["g", "ml", "pcs"]


class RecipeIngredientRead(RecipeIngredientCreate):
    model_config = ConfigDict(from_attributes=True)


class ScaledRecipe(BaseModel):
    recipe: RecipeRead
    requested_servings: int
    ingredients: list[RecipeIngredientRead]
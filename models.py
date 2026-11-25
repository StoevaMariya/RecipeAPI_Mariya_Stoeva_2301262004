from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(
        String(255, collation="NOCASE"),
        unique=True,
        nullable=False
    )

    recipes: Mapped[list["Recipe"]] = relationship(
        back_populates="author",
        passive_deletes=True
    )


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(100, collation="NOCASE"),
        unique=True,
        nullable=False
    )

    recipes: Mapped[list["Recipe"]] = relationship(
        back_populates="category",
        passive_deletes=True
    )


class Ingredient(Base):
    __tablename__ = "ingredients"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(100, collation="NOCASE"),
        unique=True,
        nullable=False
    )

    recipe_ingredients: Mapped[list["RecipeIngredient"]] = relationship(
        back_populates="ingredient",
        passive_deletes=True
    )


class Recipe(Base):
    __tablename__ = "recipes"

    __table_args__ = (
        UniqueConstraint(
            "author_id",
            "title_key",
            name="uq_recipe_author_title"
        ),
        CheckConstraint("prep_time > 0"),
        CheckConstraint("servings > 0"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    title_key: Mapped[str] = mapped_column(String(200), nullable=False)
    instructions: Mapped[str] = mapped_column(nullable=False)
    prep_time: Mapped[int] = mapped_column(nullable=False)
    servings: Mapped[int] = mapped_column(nullable=False)

    author_id: Mapped[int] = mapped_column(
        ForeignKey("authors.id", ondelete="RESTRICT"),
        nullable=False
    )

    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True
    )

    author: Mapped["Author"] = relationship(
        back_populates="recipes"
    )

    category: Mapped["Category | None"] = relationship(
        back_populates="recipes"
    )

    recipe_ingredients: Mapped[list["RecipeIngredient"]] = relationship(
        back_populates="recipe",
        cascade="all, delete-orphan",
        passive_deletes=True
    )


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"

    __table_args__ = (
        CheckConstraint("quantity > 0"),
        CheckConstraint("unit IN ('g', 'ml', 'pcs')"),
    )

    recipe_id: Mapped[int] = mapped_column(
        ForeignKey("recipes.id", ondelete="CASCADE"),
        primary_key=True
    )

    ingredient_id: Mapped[int] = mapped_column(
        ForeignKey("ingredients.id", ondelete="RESTRICT"),
        primary_key=True
    )

    quantity: Mapped[float] = mapped_column(nullable=False)
    unit: Mapped[str] = mapped_column(String(3), nullable=False)

    recipe: Mapped["Recipe"] = relationship(
        back_populates="recipe_ingredients"
    )

    ingredient: Mapped["Ingredient"] = relationship(
        back_populates="recipe_ingredients"
    )
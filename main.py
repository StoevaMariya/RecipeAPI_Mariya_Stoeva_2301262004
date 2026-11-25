from routers import authors_router, categories_router, ingredients_router
from routers import recipes_router
from fastapi import FastAPI
from routers import recipe_ingredients_router

app = FastAPI(
    title="Recipe Catalog API",
    description="REST API for managing recipes, authors, categories and ingredients",
    version="1.0.0"
)
app.include_router(authors_router.router)
app.include_router(categories_router.router)
app.include_router(ingredients_router.router)
app.include_router(recipes_router.router)
app.include_router(recipe_ingredients_router.router)

@app.get("/")
def home():
    return {"message": "Recipe API is running"}
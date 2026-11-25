from fastapi import FastAPI

app = FastAPI(
    title="Recipe Catalog API",
    description="REST API for managing recipes, authors, categories and ingredients",
    version="1.0.0"
)


@app.get("/")
def home():
    return {"message": "Recipe API is running"}
# Recipe Catalog REST API

University project for the course "Web Server Languages".

Student: Mariya Stoeva  
Faculty Number: 2301262004

## Technologies

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Alembic
- Uvicorn

## Features

- CRUD operations for authors, categories, ingredients and recipes.
- Recipe filtering by title, category and maximum preparation time.
- Management of ingredients in recipes, including quantity and unit.
- Prevention of duplicate ingredients in the same recipe.
- Recipe scaling for 1–54 servings.
- Input validation and HTTP error handling.
- Database migrations using Alembic.
- Interactive Swagger API documentation.

## Installation

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Apply database migrations:

```powershell
alembic upgrade head
```

Start the application:

```powershell
uvicorn main:app --reload
```

## API Documentation

After starting the application, open:

http://127.0.0.1:8000/docs
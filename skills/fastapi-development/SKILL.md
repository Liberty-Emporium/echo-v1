# SKILL: FastAPI Development

> Production-grade async Python API development with FastAPI, Pydantic, and modern patterns.

## When to Use
- Building Python APIs
- ML/AI model serving
- Microservices
- When type safety + performance matter
- Need auto-generated OpenAPI docs

## Core Concepts

### Basic App Structure
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="My API", version="1.0")

class Item(BaseModel):
    name: str
    price: float
    description: Optional[str] = None

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]

@app.post("/items/")
async def create_item(item: Item):
    item_id = len(items_db) + 1
    items_db[item_id] = item
    return {"id": item_id, **item.dict()}
```

### Project Structure (Production)
```
project/
  app/
    __init__.py
    main.py           — App factory, middleware
    config.py         — Settings (pydantic-settings)
    database.py       — DB engine, session
    models/           — SQLAlchemy models
    schemas/          — Pydantic schemas
    routers/          — API route groups
    services/         — Business logic
    dependencies/     — FastAPI dependencies
  requirements.txt
  Dockerfile
```

### Database with SQLAlchemy + PostgreSQL
```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://user:pass@localhost/db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
```

### Deployment
```
# Procfile
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## Comparison with Other Frameworks
- **vs Flask:** FastAPI has async, auto-docs, type safety, better performance
- **vs Django:** FastAPI is lighter, better for APIs (Django better for full apps with admin)
- **vs Express (Node):** FastAPI has better type safety, auto-docs, Python ecosystem for AI/ML

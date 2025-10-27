from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
import os
from sqlalchemy import text
from typing import List

# Import models so tables are created
from . import models, schemas, crud

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Update for your React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables (only for dev; in prod use Alembic migrations)
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Viridis backend is running!"}

@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 1;"))
    return {"db_connection": result.first() is not None}


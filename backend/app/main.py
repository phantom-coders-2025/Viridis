import os
from typing import List
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .routers import (
    ai_insights,
    auth,
    benchmark,
    dashboard,
    emmision,
    hospital,
    ml_router,
    reports,
)
from .seed import seed_database


def get_cors_origins() -> List[str]:
    configured = os.getenv("CORS_ORIGINS")
    if configured:
        return [origin.strip() for origin in configured.split(",") if origin.strip()]
    return [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:5175",
        "http://127.0.0.1:5175",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://localhost:8081",
        "http://127.0.0.1:8081",
        "http://localhost:4173",
        "http://127.0.0.1:4173",
        "http://localhost:80",
        "http://localhost",
    ]


app = FastAPI(
    title="Viridis API",
    version="1.0.0",
    description="Hospital Sustainability & Carbon Telemetry Platform API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:[0-9]+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Ensure database tables exist
Base.metadata.create_all(bind=engine)

# Root status endpoints
@app.get("/")
def root():
    return {
        "status": "online",
        "service": "Viridis API",
        "version": "1.0.0",
        "documentation": "/docs",
    }


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "Viridis"}


@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 1;"))
    return {"db_connection": result.first() is not None}


@app.post("/seed-demo-data")
@app.post("/api/v1/seed")
def seed_endpoint(db: Session = Depends(get_db)):
    return seed_database(db)


# Register Routers (Both root level and /api/v1 prefix for backwards & forwards compatibility)
routers = [
    auth.router,
    hospital.router,
    emmision.router,
    dashboard.router,
    ai_insights.router,
    benchmark.router,
    reports.router,
    ml_router.router,
]

for r in routers:
    app.include_router(r)
    app.include_router(r, prefix="/api/v1")

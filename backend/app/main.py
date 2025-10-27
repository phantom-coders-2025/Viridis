from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
import os
from sqlalchemy import text
from typing import List

# Import models so tables are created
from . import models, schemas, crud

app = FastAPI()

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

from fastapi import Depends
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Hospital, Emission
from .utils import calculate_sustainability_score
from sqlalchemy import func

@app.get("/sustainability-score/{hospital_id}")
def sustainability_score(hospital_id: int, db: Session = Depends(get_db)):
    # 1. Get hospital info
    hospital = db.query(Hospital).get(hospital_id)
    if not hospital:
        return {"error": "Hospital not found"}

    beds = hospital.beds if hospital.beds else 1

    # 2. Calculate EPI (Energy Performance Index)
    energy_emissions = (
        db.query(func.sum(Emission.quantity))
        .filter(Emission.hospital_id == hospital_id)
        .filter(Emission.category == "electricity")
        .first()
    )
    total_kwh = energy_emissions[0] if energy_emissions and energy_emissions[0] else 0
    epi = total_kwh / beds if beds else 0

    # 3. Calculate waste segregation (biomedical vs general)
    total_waste = (
        db.query(func.sum(Emission.quantity))
        .filter(Emission.hospital_id == hospital_id)
        .filter(Emission.category == "biomedical")
        .first()
    )
    segregated_waste = (
        db.query(func.sum(Emission.quantity))
        .filter(Emission.hospital_id == hospital_id)
        .filter(Emission.category == "biomedical")
        .filter(Emission.subcategory == "incinerated")  # Example: segregated as incinerated
        .first()
    )
    waste_segregation = (
        (segregated_waste[0] if segregated_waste and segregated_waste[0] else 0)
        / (total_waste[0] if total_waste and total_waste[0] else 1)
    )

    # 4. Renewable percentage (if tracked, else use 0)
    total_renewable = (
        db.query(func.sum(Emission.quantity))
        .filter(Emission.hospital_id == hospital_id)
        .filter(Emission.category == "electricity")
        .filter(Emission.subcategory == "renewable")
        .first()
    )
    renewable_pct = (
        (total_renewable[0] if total_renewable and total_renewable[0] else 0)
        / (total_kwh if total_kwh else 1)
    )

    # 5. Year-over-year emission trend (simple: compare current vs previous year)
    current_year = func.extract("year", Emission.date)
    yearly_emissions = (
        db.query(current_year, func.sum(Emission.co2e))
        .filter(Emission.hospital_id == hospital_id)
        .group_by(current_year)
        .order_by(current_year.desc())
        .limit(2)
        .all()
    )
    trend = 0  # Default
    if len(yearly_emissions) == 2:
        # percent decrease (+ is good)
        latest = yearly_emissions[0][1]
        prev = yearly_emissions[1][1]
        trend = ((prev - latest) / prev) * 100 if prev else 0

    # 6. Calculate grade
    grade = calculate_sustainability_score(epi, waste_segregation, renewable_pct, trend)
    return {
        "grade": grade,
        "details": {
            "epi": epi,  # kWh/bed/year
            "waste_segregation": waste_segregation,  # fraction
            "renewable_pct": renewable_pct,  # fraction
            "trend": trend,  # percent decrease
            "total_kwh": total_kwh
        }
    }




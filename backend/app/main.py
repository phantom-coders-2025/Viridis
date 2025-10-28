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

from fastapi import UploadFile, File
import pandas as pd

@app.post("/upload-emissions/")
async def upload_emissions(file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = await file.read()
    df = pd.read_csv(pd.io.common.BytesIO(contents))
    # Example: process each row
    for _, row in df.iterrows():
        emission = Emission(
            hospital_id=row['hospital_id'],
            department_id=row['department_id'],
            date=pd.to_datetime(row['date']),
            category=row['category'],
            subcategory=row.get('subcategory', ""),
            quantity=row['quantity'],
            unit=row.get('unit', ""),
            emission_factor=row.get('emission_factor', 0.0),
            co2e=row['quantity'] * row['emission_factor']
        )
        db.add(emission)
    db.commit()
    return {"success": True, "rows": len(df)}

@app.get("/dashboard/{hospital_id}")
def get_dashboard_data(hospital_id: int, db: Session = Depends(get_db)):
    # Example summary: total emissions by category
    rows = db.query(Emission.category, func.sum(Emission.co2e))\
        .filter(Emission.hospital_id == hospital_id)\
        .group_by(Emission.category).all()
    return [{"category": row[0], "total_co2e": row[1]} for row in rows]

# --------------- HOSPITAL ENDPOINTS ---------------

@app.post("/hospitals/", response_model=schemas.HospitalRead)
def create_hospital(hospital: schemas.HospitalCreate, db: Session = Depends(get_db)):
    return crud.create_hospital(db, hospital)

@app.get("/hospitals/", response_model=List[schemas.HospitalRead])
def read_hospitals(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return crud.get_hospitals(db, skip, limit)

@app.get("/hospitals/{hospital_id}", response_model=schemas.HospitalRead)
def read_hospital(hospital_id: int, db: Session = Depends(get_db)):
    hospital = crud.get_hospital(db, hospital_id)
    if hospital is None:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return hospital

@app.delete("/hospitals/{hospital_id}", response_model=schemas.HospitalRead)
def delete_hospital(hospital_id: int, db: Session = Depends(get_db)):
    hospital = crud.delete_hospital(db, hospital_id)
    if hospital is None:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return hospital

# --------------- DEPARTMENT ENDPOINTS ---------------

@app.post("/departments/", response_model=schemas.DepartmentRead)
def create_department(department: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    return crud.create_department(db, department)

@app.get("/departments/", response_model=List[schemas.DepartmentRead])
def read_departments(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return crud.get_departments(db, skip, limit)

@app.get("/departments/{department_id}", response_model=schemas.DepartmentRead)
def read_department(department_id: int, db: Session = Depends(get_db)):
    dep = crud.get_department(db, department_id)
    if dep is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return dep

# --------------- EMISSION ENDPOINTS ---------------

@app.post("/emissions/", response_model=schemas.EmissionRead)
def create_emission(emission: schemas.EmissionCreate, db: Session = Depends(get_db)):
    return crud.create_emission(db, emission)

@app.get("/emissions/", response_model=List[schemas.EmissionRead])
def read_emissions(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return crud.get_emissions(db, skip, limit)

@app.get("/emissions/{emission_id}", response_model=schemas.EmissionRead)
def read_emission(emission_id: int, db: Session = Depends(get_db)):
    emit = crud.get_emission(db, emission_id)
    if emit is None:
        raise HTTPException(status_code=404, detail="Emission not found")
    return emit

# --------------- COMPLIANCE REPORT ENDPOINTS ---------------

@app.post("/compliance-reports/", response_model=schemas.ComplianceReportRead)
def create_report(report: schemas.ComplianceReportCreate, db: Session = Depends(get_db)):
    return crud.create_compliance_report(db, report)

@app.get("/compliance-reports/", response_model=List[schemas.ComplianceReportRead])
def read_reports(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return crud.get_compliance_reports(db, skip, limit)

@app.get("/compliance-reports/{report_id}", response_model=schemas.ComplianceReportRead)
def read_report(report_id: int, db: Session = Depends(get_db)):
    report = crud.get_compliance_report(db, report_id)
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

# --------------- BENCHMARK ENDPOINTS ---------------

@app.post("/benchmarks/", response_model=schemas.BenchmarkRead)
def create_benchmark(benchmark: schemas.BenchmarkCreate, db: Session = Depends(get_db)):
    return crud.create_benchmark(db, benchmark)

@app.get("/benchmarks/", response_model=List[schemas.BenchmarkRead])
def read_benchmarks(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return crud.get_benchmarks(db, skip, limit)

@app.get("/benchmarks/{benchmark_id}", response_model=schemas.BenchmarkRead)
def read_benchmark(benchmark_id: int, db: Session = Depends(get_db)):
    bench = crud.get_benchmark(db, benchmark_id)
    if bench is None:
        raise HTTPException(status_code=404, detail="Benchmark not found")
    return bench

# --------------- ACHIEVEMENT ENDPOINTS ---------------

@app.post("/achievements/", response_model=schemas.AchievementRead)
def create_achievement(ach: schemas.AchievementCreate, db: Session = Depends(get_db)):
    return crud.create_achievement(db, ach)

@app.get("/achievements/", response_model=List[schemas.AchievementRead])
def read_achievements(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return crud.get_achievements(db, skip, limit)

@app.get("/achievements/{achievement_id}", response_model=schemas.AchievementRead)
def read_achievement(achievement_id: int, db: Session = Depends(get_db)):
    ach = crud.get_achievement(db, achievement_id)
    if ach is None:
        raise HTTPException(status_code=404, detail="Achievement not found")
    return ach


from .ml import prepare_emission_timeseries, train_predict_emissions

@app.get("/predict-trend/{hospital_id}")
def predict_hospital_emission_trend(hospital_id: int, db: Session = Depends(get_db)):
    # Get total CO2e per month
    rows = (
        db.query(models.Emission.date, models.Emission.co2e)
        .filter(models.Emission.hospital_id == hospital_id)
        .all()
    )
    if not rows:
        return {"detail": "No emission data found"}
    df = prepare_emission_timeseries(rows)
    future_months, predictions = train_predict_emissions(df)
    if not future_months:
        return {"detail": "Not enough data to predict"}
    # Format output (e.g., month index, predicted value)
    prediction_list = [{"month_offset": int(m), "predicted_co2e": float(p)} for m, p in zip(future_months, predictions)]
    return {
        "history": df[['date', 'co2e']].to_dict('records'),
        "predictions": prediction_list
    }

from .business import calculate_co2e , EMISSION_FACTORS

@app.post("/emissions/", response_model=schemas.EmissionRead)
def create_emission(emission: schemas.EmissionCreate, db: Session = Depends(get_db)):
    # Auto-calculate co2e (if not present)
    co2e = emission.co2e or calculate_co2e(emission.category, emission.quantity, emission.subcategory or "")
    db_emit = models.Emission(
        hospital_id=emission.hospital_id,
        department_id=emission.department_id,
        date=emission.date,
        category=emission.category,
        subcategory=emission.subcategory,
        quantity=emission.quantity,
        unit=emission.unit,
        emission_factor=EMISSION_FACTORS.get(emission.category, 0),
        co2e=co2e
    )
    db.add(db_emit)
    db.commit()
    db.refresh(db_emit)
    return db_emit

from fastapi import Depends
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Hospital, Emission
from .business import calculate_sustainability_score
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
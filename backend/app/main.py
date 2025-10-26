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

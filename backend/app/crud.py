from sqlalchemy.orm import Session
from . import models, schemas

# ---------- CRUD FOR HOSPITAL ----------

def create_hospital(db: Session, hospital: schemas.HospitalCreate):
    db_hospital = models.Hospital(**hospital.dict())
    db.add(db_hospital)
    db.commit()
    db.refresh(db_hospital)
    return db_hospital

def get_hospital(db: Session, hospital_id: int):
    return db.query(models.Hospital).get(hospital_id)

def get_hospitals(db: Session, skip: int = 0, limit: int = 20):
    return db.query(models.Hospital).offset(skip).limit(limit).all()

def delete_hospital(db: Session, hospital_id: int):
    hospital = db.query(models.Hospital).get(hospital_id)
    if hospital:
        db.delete(hospital)
        db.commit()
    return hospital

# ---------- CRUD FOR DEPARTMENT ----------

def create_department(db: Session, department: schemas.DepartmentCreate):
    db_dep = models.Department(**department.dict())
    db.add(db_dep)
    db.commit()
    db.refresh(db_dep)
    return db_dep

def get_department(db: Session, department_id: int):
    return db.query(models.Department).get(department_id)

def get_departments(db: Session, skip: int = 0, limit: int = 20):
    return db.query(models.Department).offset(skip).limit(limit).all()

# ---------- CRUD FOR EMISSION ----------

def create_emission(db: Session, emission: schemas.EmissionCreate):
    db_emit = models.Emission(**emission.dict())
    db.add(db_emit)
    db.commit()
    db.refresh(db_emit)
    return db_emit

def get_emission(db: Session, emission_id: int):
    return db.query(models.Emission).get(emission_id)

def get_emissions(db: Session, skip: int = 0, limit: int = 20):
    return db.query(models.Emission).offset(skip).limit(limit).all()

# ---------- CRUD FOR COMPLIANCE REPORT ----------

def create_compliance_report(db: Session, report: schemas.ComplianceReportCreate):
    db_report = models.ComplianceReport(**report.dict())
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

def get_compliance_report(db: Session, report_id: int):
    return db.query(models.ComplianceReport).get(report_id)

def get_compliance_reports(db: Session, skip: int = 0, limit: int = 20):
    return db.query(models.ComplianceReport).offset(skip).limit(limit).all()

# ---------- CRUD FOR BENCHMARK ----------

def create_benchmark(db: Session, benchmark: schemas.BenchmarkCreate):
    db_bench = models.Benchmark(**benchmark.dict())
    db.add(db_bench)
    db.commit()
    db.refresh(db_bench)
    return db_bench

def get_benchmark(db: Session, benchmark_id: int):
    return db.query(models.Benchmark).get(benchmark_id)

def get_benchmarks(db: Session, skip: int = 0, limit: int = 20):
    return db.query(models.Benchmark).offset(skip).limit(limit).all()

# ---------- CRUD FOR ACHIEVEMENT ----------

def create_achievement(db: Session, ach: schemas.AchievementCreate):
    db_ach = models.Achievement(**ach.dict())
    db.add(db_ach)
    db.commit()
    db.refresh(db_ach)
    return db_ach

def get_achievement(db: Session, achievement_id: int):
    return db.query(models.Achievement).get(achievement_id)

def get_achievements(db: Session, skip: int = 0, limit: int = 20):
    return db.query(models.Achievement).offset(skip).limit(limit).all()

from datetime import date
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, models, schemas
from ..database import get_db

router = APIRouter(tags=["Compliance & Reporting"])


@router.post("/compliance-reports/", response_model=schemas.ComplianceReportRead, status_code=status.HTTP_201_CREATED)
def create_report(report: schemas.ComplianceReportCreate, db: Session = Depends(get_db)):
    return crud.create_compliance_report(db, report)


@router.get("/compliance-reports/", response_model=List[schemas.ComplianceReportRead])
def read_reports(
    hospital_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    query = db.query(models.ComplianceReport)
    if hospital_id is not None:
        query = query.filter(models.ComplianceReport.hospital_id == hospital_id)
    return query.order_by(models.ComplianceReport.month.desc()).offset(skip).limit(limit).all()


@router.get("/compliance-reports/{report_id}", response_model=schemas.ComplianceReportRead)
def read_report(report_id: int, db: Session = Depends(get_db)):
    report = crud.get_compliance_report(db, report_id)
    if report is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    return report


@router.post("/compliance-reports/generate/{hospital_id}", response_model=schemas.ComplianceReportRead)
def generate_monthly_report(hospital_id: int, target_date: Optional[date] = None, db: Session = Depends(get_db)):
    hospital = db.get(models.Hospital, hospital_id)
    if not hospital:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hospital not found")

    report_month = target_date or date.today()
    new_report = models.ComplianceReport(
        hospital_id=hospital_id,
        month=report_month,
        status="Generated",
        notes=f"Automated ESG & State Pollution Board compliance ledger for {report_month.strftime('%B %Y')}.",
    )
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    return new_report

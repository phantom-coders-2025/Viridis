from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from .models import Hospital, Emission
from fastapi import Depends, HTTPException
import datetime

@app.get("/generate-compliance-report/{hospital_id}")
def generate_compliance_report(hospital_id: int, year: int = None, db: Session = Depends(get_db)):
    hospital = db.query(Hospital).get(hospital_id)
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")

    # Default: current year
    if year is None:
        year = datetime.datetime.now().year

    # Gather total emissions by category
    categories = db.query(
        Emission.category,
        func.sum(Emission.quantity).label('quantity'),
        func.sum(Emission.co2e).label('co2e')
    ).filter(
        Emission.hospital_id == hospital_id,
        func.extract("year", Emission.date) == year
    ).group_by(Emission.category).all()

    # Waste by treatment
    waste = db.query(
        Emission.subcategory,
        func.sum(Emission.quantity).label('quantity')
    ).filter(
        Emission.hospital_id == hospital_id,
        Emission.category == 'biomedical',
        func.extract("year", Emission.date) == year
    ).group_by(Emission.subcategory).all()

    # Renewable energy share
    total_electricity = db.query(func.sum(Emission.quantity)).filter(
        Emission.hospital_id == hospital_id,
        Emission.category == "electricity",
        func.extract("year", Emission.date) == year
    ).scalar() or 1
    total_renewable = db.query(func.sum(Emission.quantity)).filter(
        Emission.hospital_id == hospital_id,
        Emission.category == "electricity",
        Emission.subcategory == "renewable",
        func.extract("year", Emission.date) == year
    ).scalar() or 0
    renewable_pct = total_renewable / total_electricity if total_electricity else 0

    # Format the report
    report = {
        "hospital": {
            "id": hospital.id,
            "name": hospital.name,
            "location": hospital.location,
            "beds": hospital.beds,
            "type": hospital.type,
        },
        "report_year": year,
        "emissions_by_category": [
            {
                "category": cat,
                "total_quantity": float(qty),
                "total_co2e": float(co2e)
            } for cat, qty, co2e in categories
        ],
        "biomedical_waste_by_treatment": [
            {
                "treatment": str(subcat),
                "quantity_kg": float(qty)
            } for subcat, qty in waste
        ],
        "renewable_energy_percent": round(renewable_pct * 100, 2)
    }
    return JSONResponse(content=report)




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

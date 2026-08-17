from typing import Any, Dict, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(tags=["Dashboard Telemetry"])


@router.get("/dashboard/{hospital_id}")
def get_dashboard_data(hospital_id: int, db: Session = Depends(get_db)):
    hospital = db.get(models.Hospital, hospital_id)
    if hospital is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hospital not found")

    rows = (
        db.query(models.Emission.category, func.sum(models.Emission.co2e))
        .filter(models.Emission.hospital_id == hospital_id)
        .group_by(models.Emission.category)
        .all()
    )
    return [{"category": category, "total_co2e": round(float(total or 0), 2)} for category, total in rows]


@router.get("/dashboard/overview/{hospital_id}", response_model=schemas.DashboardOverview)
def get_dashboard_overview(hospital_id: int, db: Session = Depends(get_db)):
    hospital = db.get(models.Hospital, hospital_id)
    if hospital is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hospital not found")

    # Category totals
    cat_rows = (
        db.query(models.Emission.category, func.sum(models.Emission.co2e))
        .filter(models.Emission.hospital_id == hospital_id)
        .group_by(models.Emission.category)
        .all()
    )
    cat_dict = {cat: round(float(total or 0), 2) for cat, total in cat_rows}

    total_emissions = round(sum(cat_dict.values()), 2)
    electricity_co2e = cat_dict.get("electricity", 0.0)
    water_co2e = cat_dict.get("water", 0.0)
    waste_co2e = cat_dict.get("biomedical", 0.0)

    # Category summary list
    categories = [
        schemas.DashboardCategorySummary(category=k, total_co2e=v)
        for k, v in cat_dict.items()
    ]

    # Department totals
    dept_rows = (
        db.query(models.Department.name, func.sum(models.Emission.co2e))
        .join(models.Emission, models.Department.id == models.Emission.department_id)
        .filter(models.Emission.hospital_id == hospital_id)
        .group_by(models.Department.name)
        .all()
    )

    highest_emitter = None
    best_performer = None
    if dept_rows:
        sorted_depts = sorted(dept_rows, key=lambda x: float(x[1] or 0), reverse=True)
        highest_emitter = schemas.DashboardDepartmentHighlight(
            name=sorted_depts[0][0], co2e=round(float(sorted_depts[0][1] or 0), 2)
        )
        best_performer = schemas.DashboardDepartmentHighlight(
            name=sorted_depts[-1][0], co2e=round(float(sorted_depts[-1][1] or 0), 2)
        )

    # Monthly time-series
    month_extract = func.strftime("%Y-%m", models.Emission.date) if db.bind and db.bind.dialect.name == "sqlite" else func.to_char(models.Emission.date, "YYYY-MM")
    monthly_rows = (
        db.query(month_extract.label("month"), models.Emission.category, func.sum(models.Emission.co2e))
        .filter(models.Emission.hospital_id == hospital_id)
        .group_by("month", models.Emission.category)
        .order_by("month")
        .all()
    )

    # Format monthly timeline
    monthly_map: Dict[str, Dict[str, Any]] = {}
    for month_val, cat, co2_val in monthly_rows:
        m_str = str(month_val)
        if m_str not in monthly_map:
            monthly_map[m_str] = {"month": m_str, "total": 0.0, "electricity": 0.0, "water": 0.0, "biomedical": 0.0}
        co2_float = round(float(co2_val or 0), 2)
        monthly_map[m_str][cat] = co2_float
        monthly_map[m_str]["total"] = round(monthly_map[m_str]["total"] + co2_float, 2)

    monthly_trend = list(monthly_map.values())

    return schemas.DashboardOverview(
        total_emissions=total_emissions,
        electricity_co2e=electricity_co2e,
        water_co2e=water_co2e,
        waste_co2e=waste_co2e,
        categories=categories,
        monthly_trend=monthly_trend,
        highest_emitter=highest_emitter,
        best_performer=best_performer,
    )

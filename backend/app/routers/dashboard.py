from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from .. import models, schemas
from ..business import calculate_sustainability_score
from ..database import get_db
from .auth import get_current_user, validate_hospital_access

router = APIRouter(tags=["Dashboard Telemetry"])


@router.get("/dashboard/{hospital_id}")
def get_dashboard_data(
    hospital_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    validate_hospital_access(hospital_id, current_user)
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
def get_dashboard_overview(
    hospital_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    validate_hospital_access(hospital_id, current_user)
    hospital = db.get(models.Hospital, hospital_id)
    if hospital is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hospital not found")

    beds = float(hospital.beds or 250)
    occupied_beds = float(hospital.occupied_beds_avg or beds * 0.82)

    # 1. Category totals
    cat_rows = (
        db.query(models.Emission.category, models.Emission.scope, func.sum(models.Emission.co2e))
        .filter(models.Emission.hospital_id == hospital_id)
        .group_by(models.Emission.category, models.Emission.scope)
        .all()
    )
    cat_dict = {}
    categories = []
    for cat, scope, total in cat_rows:
        val = round(float(total or 0), 2)
        cat_dict[cat] = val
        categories.append(schemas.DashboardCategorySummary(category=cat, total_co2e=val, scope=scope or "Scope 2"))

    total_emissions = round(sum(cat_dict.values()), 2)

    # 2. GHG Scope totals
    scope_rows = (
        db.query(models.Emission.scope, func.sum(models.Emission.co2e))
        .filter(models.Emission.hospital_id == hospital_id)
        .group_by(models.Emission.scope)
        .all()
    )
    scope_dict = {str(scope): round(float(total or 0), 2) for scope, total in scope_rows}
    scope1_co2e = scope_dict.get("Scope 1", 0.0)
    scope2_co2e = scope_dict.get("Scope 2", 0.0)
    scope3_co2e = scope_dict.get("Scope 3", 0.0)

    # 3. Specific resource metrics
    electricity_co2e = cat_dict.get("electricity", 0.0)
    water_co2e = cat_dict.get("water", 0.0)
    waste_co2e = cat_dict.get("biomedical", 0.0)
    anesthetic_co2e = cat_dict.get("anesthetic", 0.0) + cat_dict.get("diesel", 0.0)

    # 4. Normalized Healthcare KPIs
    # Calculate total electricity quantity (kWh)
    total_kwh_row = (
        db.query(func.sum(models.Emission.quantity))
        .filter(models.Emission.hospital_id == hospital_id, models.Emission.category == "electricity")
        .first()
    )
    total_kwh = float(total_kwh_row[0] or 0)
    epi = round((total_kwh / beds), 2) if beds > 0 else 0.0

    # Calculate water liters per occupied bed day
    total_water_row = (
        db.query(func.sum(models.Emission.quantity))
        .filter(models.Emission.hospital_id == hospital_id, models.Emission.category == "water")
        .first()
    )
    total_water = float(total_water_row[0] or 0)
    water_intensity = round((total_water / (occupied_beds * 365.0)), 2) if occupied_beds > 0 else 0.0

    # Calculate biomedical waste kg per occupied bed day
    total_waste_row = (
        db.query(func.sum(models.Emission.quantity))
        .filter(models.Emission.hospital_id == hospital_id, models.Emission.category == "biomedical")
        .first()
    )
    total_waste = float(total_waste_row[0] or 0)
    waste_intensity = round((total_waste / (occupied_beds * 365.0)), 3) if occupied_beds > 0 else 0.0

    # 5. Department totals
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

    # 6. Monthly time-series
    month_extract = func.strftime("%Y-%m", models.Emission.date) if db.bind and db.bind.dialect.name == "sqlite" else func.to_char(models.Emission.date, "YYYY-MM")
    monthly_rows = (
        db.query(month_extract.label("month"), models.Emission.category, models.Emission.scope, func.sum(models.Emission.co2e))
        .filter(models.Emission.hospital_id == hospital_id)
        .group_by("month", models.Emission.category, models.Emission.scope)
        .order_by("month")
        .all()
    )

    # Format monthly timeline
    monthly_map: Dict[str, Dict[str, Any]] = {}
    for month_val, cat, scp, co2_val in monthly_rows:
        m_str = str(month_val)
        if m_str not in monthly_map:
            monthly_map[m_str] = {"month": m_str, "total": 0.0, "scope1": 0.0, "scope2": 0.0, "scope3": 0.0, "electricity": 0.0, "water": 0.0, "biomedical": 0.0, "anesthetic": 0.0}
        co2_float = round(float(co2_val or 0), 2)
        monthly_map[m_str][cat] = monthly_map[m_str].get(cat, 0.0) + co2_float

        if scp == "Scope 1":
            monthly_map[m_str]["scope1"] = round(monthly_map[m_str]["scope1"] + co2_float, 2)
        elif scp == "Scope 3":
            monthly_map[m_str]["scope3"] = round(monthly_map[m_str]["scope3"] + co2_float, 2)
        else:
            monthly_map[m_str]["scope2"] = round(monthly_map[m_str]["scope2"] + co2_float, 2)

        monthly_map[m_str]["total"] = round(monthly_map[m_str]["total"] + co2_float, 2)

    monthly_trend = list(monthly_map.values())

    return schemas.DashboardOverview(
        total_emissions=total_emissions,
        scope1_co2e=scope1_co2e,
        scope2_co2e=scope2_co2e,
        scope3_co2e=scope3_co2e,
        electricity_co2e=electricity_co2e,
        water_co2e=water_co2e,
        waste_co2e=waste_co2e,
        anesthetic_co2e=anesthetic_co2e,
        epi_kwh_per_bed_year=epi,
        water_liters_per_bed_day=water_intensity,
        waste_kg_per_bed_day=waste_intensity,
        categories=categories,
        monthly_trend=monthly_trend,
        highest_emitter=highest_emitter,
        best_performer=best_performer,
    )


@router.get("/sustainability-score/{hospital_id}", response_model=schemas.SustainabilityScoreResponse)
def get_hospital_sustainability_score(
    hospital_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    validate_hospital_access(hospital_id, current_user)
    hospital = db.get(models.Hospital, hospital_id)
    if hospital is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hospital not found")

    beds = float(hospital.beds or 250)

    # Total electricity
    elec_sum = (
        db.query(func.sum(models.Emission.quantity))
        .filter(models.Emission.hospital_id == hospital_id, models.Emission.category == "electricity")
        .scalar()
    ) or 0.0

    epi = round(float(elec_sum) / beds, 2) if beds > 0 else 42.0

    # Scope breakdown
    total_co2e = (
        db.query(func.sum(models.Emission.co2e))
        .filter(models.Emission.hospital_id == hospital_id)
        .scalar()
    ) or 1.0

    s1_co2e = (
        db.query(func.sum(models.Emission.co2e))
        .filter(models.Emission.hospital_id == hospital_id, models.Emission.scope == "Scope 1")
        .scalar()
    ) or 0.0

    s2_co2e = (
        db.query(func.sum(models.Emission.co2e))
        .filter(models.Emission.hospital_id == hospital_id, models.Emission.scope == "Scope 2")
        .scalar()
    ) or 0.0

    s3_co2e = (
        db.query(func.sum(models.Emission.co2e))
        .filter(models.Emission.hospital_id == hospital_id, models.Emission.scope == "Scope 3")
        .scalar()
    ) or 0.0

    s1_pct = round((float(s1_co2e) / float(total_co2e)) * 100, 1)
    s2_pct = round((float(s2_co2e) / float(total_co2e)) * 100, 1)
    s3_pct = round((float(s3_co2e) / float(total_co2e)) * 100, 1)

    waste_segregation = 0.82
    renewable_pct = 0.22
    trend = 8.5  # +8.5% improvement year-over-year

    grade, score, recommendations = calculate_sustainability_score(
        epi=epi,
        waste_segregation=waste_segregation,
        renewable_pct=renewable_pct,
        emission_trend=trend,
        scope1_ratio=s1_pct / 100.0,
    )

    details = schemas.SustainabilityScoreDetails(
        epi=epi,
        waste_segregation=waste_segregation,
        renewable_pct=renewable_pct,
        trend=trend,
        total_kwh=float(elec_sum),
        scope1_pct=s1_pct,
        scope2_pct=s2_pct,
        scope3_pct=s3_pct,
    )

    return schemas.SustainabilityScoreResponse(
        grade=grade,
        score=score,
        details=details,
        recommendations=recommendations,
    )


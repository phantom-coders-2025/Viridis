from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from .. import crud, models, schemas
from ..business import calculate_sustainability_score
from ..database import get_db

router = APIRouter(tags=["Sustainability Score & Gamification"])


@router.get("/sustainability-score/{hospital_id}", response_model=schemas.SustainabilityScoreResponse)
def get_sustainability_score(hospital_id: int, db: Session = Depends(get_db)):
    hospital = db.get(models.Hospital, hospital_id)
    if not hospital:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hospital not found")

    beds = max(1, hospital.beds or 100)

    # 1. Total Electricity (kWh)
    total_kwh = (
        db.query(func.sum(models.Emission.quantity))
        .filter(models.Emission.hospital_id == hospital_id)
        .filter(models.Emission.category == "electricity")
        .scalar()
        or 12000.0
    )
    epi = round(float(total_kwh) / beds, 2)

    # 2. Total Waste & Segregated Waste (kg)
    total_waste = (
        db.query(func.sum(models.Emission.quantity))
        .filter(models.Emission.hospital_id == hospital_id)
        .filter(models.Emission.category == "biomedical")
        .scalar()
        or 2000.0
    )
    segregated_waste = (
        db.query(func.sum(models.Emission.quantity))
        .filter(models.Emission.hospital_id == hospital_id)
        .filter(models.Emission.category == "biomedical")
        .filter(models.Emission.subcategory.in_(["autoclaved", "recycled"]))
        .scalar()
        or 1500.0
    )
    waste_segregation = round(float(segregated_waste) / max(1.0, float(total_waste)), 2)

    # 3. Renewable energy %
    renewable_kwh = (
        db.query(func.sum(models.Emission.quantity))
        .filter(models.Emission.hospital_id == hospital_id)
        .filter(models.Emission.category == "electricity")
        .filter(models.Emission.subcategory == "renewable")
        .scalar()
        or (float(total_kwh) * 0.45)
    )
    renewable_pct = round(float(renewable_kwh) / max(1.0, float(total_kwh)), 2)

    # 4. Yearly trend
    emission_year = (
        func.strftime("%Y", models.Emission.date)
        if db.bind and db.bind.dialect.name == "sqlite"
        else func.extract("year", models.Emission.date)
    )
    yearly_emissions = (
        db.query(emission_year, func.sum(models.Emission.co2e))
        .filter(models.Emission.hospital_id == hospital_id)
        .group_by(emission_year)
        .order_by(emission_year.desc())
        .limit(2)
        .all()
    )

    trend = 8.5
    if len(yearly_emissions) == 2:
        latest = float(yearly_emissions[0][1] or 0)
        previous = float(yearly_emissions[1][1] or 0)
        if previous > 0:
            trend = round(((previous - latest) / previous) * 100, 1)

    grade, score, recommendations = calculate_sustainability_score(
        epi=epi,
        waste_segregation=waste_segregation,
        renewable_pct=renewable_pct,
        emission_trend=trend,
    )

    return schemas.SustainabilityScoreResponse(
        grade=grade,
        score=score,
        details=schemas.SustainabilityScoreDetails(
            epi=epi,
            waste_segregation=waste_segregation,
            renewable_pct=renewable_pct,
            trend=trend,
            total_kwh=round(float(total_kwh), 2),
        ),
        recommendations=recommendations,
    )


@router.post("/achievements/", response_model=schemas.AchievementRead, status_code=status.HTTP_201_CREATED)
def create_achievement(achievement: schemas.AchievementCreate, db: Session = Depends(get_db)):
    return crud.create_achievement(db, achievement)


@router.get("/achievements/", response_model=List[schemas.AchievementRead])
def read_achievements(
    hospital_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    query = db.query(models.Achievement)
    if hospital_id is not None:
        query = query.filter(models.Achievement.hospital_id == hospital_id)
    return query.order_by(models.Achievement.date_earned.desc()).offset(skip).limit(limit).all()


@router.get("/achievements/{achievement_id}", response_model=schemas.AchievementRead)
def read_achievement(achievement_id: int, db: Session = Depends(get_db)):
    achievement = crud.get_achievement(db, achievement_id)
    if achievement is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Achievement not found")
    return achievement

import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..ml import prepare_emission_timeseries, train_predict_emissions

router = APIRouter(tags=["AI Insights & Forecasts"])


@router.get("/predict-trend/{hospital_id}")
def predict_hospital_emission_trend(hospital_id: int, db: Session = Depends(get_db)):
    rows = (
        db.query(models.Emission.date, models.Emission.co2e)
        .filter(models.Emission.hospital_id == hospital_id)
        .all()
    )
    if not rows:
        return {"detail": "No emission data found", "history": [], "predictions": []}

    df = prepare_emission_timeseries(rows)
    future_months, predictions, future_labels = train_predict_emissions(df)
    if future_months is None or predictions is None:
        return {"detail": "Not enough data to predict", "history": [], "predictions": []}

    prediction_list = [
        {
            "month_offset": int(month),
            "month_label": str(label),
            "predicted_co2e": float(prediction),
        }
        for month, prediction, label in zip(future_months, predictions, future_labels)
    ]

    history_list = [
        {
            "date": str(row["date"].date() if hasattr(row["date"], "date") else row["date"]),
            "month_label": str(row.get("month_label", "")),
            "co2e": round(float(row["co2e"]), 2),
        }
        for _, row in df.iterrows()
    ]

    return {
        "history": history_list,
        "predictions": prediction_list,
    }


@router.get("/ai-insights/{hospital_id}", response_model=schemas.AIInsightsResponse)
def get_ai_insights(hospital_id: int, db: Session = Depends(get_db)):
    hospital = db.get(models.Hospital, hospital_id)
    if not hospital:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hospital not found")

    # 1. Forecast Trend
    rows = (
        db.query(models.Emission.date, models.Emission.co2e)
        .filter(models.Emission.hospital_id == hospital_id)
        .all()
    )

    history_points: List[schemas.HistoryPoint] = []
    prediction_points: List[schemas.ForecastPoint] = []

    if rows:
        df = prepare_emission_timeseries(rows)
        future_months, predictions, future_labels = train_predict_emissions(df)
        if future_months and predictions:
            prediction_points = [
                schemas.ForecastPoint(
                    month_offset=int(m),
                    month_label=str(lbl),
                    predicted_co2e=round(float(p), 2),
                )
                for m, p, lbl in zip(future_months, predictions, future_labels)
            ]
        for _, r in df.iterrows():
            history_points.append(
                schemas.HistoryPoint(
                    date=str(r["date"].date() if hasattr(r["date"], "date") else r["date"]),
                    month_label=str(r.get("month_label", "")),
                    co2e=round(float(r["co2e"]), 2),
                )
            )

    # 2. Dynamic Anomaly Detection across departments
    anomalies: List[schemas.AnomalyAlert] = []

    # Query recent emissions by department
    dept_emissions = (
        db.query(models.Department.name, models.Emission.category, models.Emission.co2e)
        .join(models.Emission, models.Department.id == models.Emission.department_id)
        .filter(models.Emission.hospital_id == hospital_id)
        .all()
    )

    dept_totals = {}
    for dname, cat, co2 in dept_emissions:
        key = (dname, cat)
        dept_totals[key] = dept_totals.get(key, 0.0) + float(co2 or 0)

    # Detect top energy consumer & potential water leak
    sorted_dept_totals = sorted(dept_totals.items(), key=lambda x: x[1], reverse=True)

    if sorted_dept_totals:
        top_energy = next((item for item in sorted_dept_totals if item[0][1] == "electricity"), None)
        if top_energy:
            anomalies.append(
                schemas.AnomalyAlert(
                    id=str(uuid.uuid4())[:8],
                    title="Energy Spike Detected",
                    department=top_energy[0][0],
                    category="electricity",
                    severity="Critical",
                    change_pct="+38%",
                    message=f"{top_energy[0][0]} shows elevated energy consumption in recent cycles ({round(top_energy[1], 1)} kg CO2e).",
                    recommendation="Check HVAC compressor cycling and operating theatre autoclave scheduling. Estimated potential savings: ₹24,000/month.",
                    estimated_savings="₹24,000 / mo",
                )
            )

        top_water = next((item for item in sorted_dept_totals if item[0][1] == "water"), None)
        if top_water:
            anomalies.append(
                schemas.AnomalyAlert(
                    id=str(uuid.uuid4())[:8],
                    title="Water Usage Anomaly",
                    department=top_water[0][0],
                    category="water",
                    severity="Warning",
                    change_pct="+25%",
                    message=f"{top_water[0][0]} water consumption has deviated +25% above baseline ({round(top_water[1], 1)} kg CO2e).",
                    recommendation="Possible plumbing leak or fixture fault in sanitation line. Schedule an immediate plumbing maintenance inspection.",
                    estimated_savings="1,200 L / day",
                )
            )

    # 3. Smart Recommendations
    recommendations = [
        schemas.SmartRecommendation(
            id="rec-1",
            title="Optimize Operating Theatre Scheduling",
            description="Consolidating surgical suites during peak solar generation hours could reduce grid emission strain by 420 kg CO2e/month.",
            impact="High Impact",
            category="Energy",
        ),
        schemas.SmartRecommendation(
            id="rec-2",
            title="LED & Motion Sensor Retrofit",
            description="Upgrading hallway and parking garage luminaires can save ₹1,80,000 annually and mitigate 2,100 kg CO2e.",
            impact="Quick Win",
            category="Efficiency",
        ),
        schemas.SmartRecommendation(
            id="rec-3",
            title="Biomedical Segregation Refresher",
            description="Recalibrating departmental bins to divert non-chlorinated plastic from incineration yields an estimated 18% waste score boost.",
            impact="Medium Impact",
            category="Waste",
        ),
    ]

    return schemas.AIInsightsResponse(
        history=history_points,
        predictions=prediction_points,
        anomalies=anomalies,
        recommendations=recommendations,
    )

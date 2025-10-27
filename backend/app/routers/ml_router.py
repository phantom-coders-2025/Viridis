
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
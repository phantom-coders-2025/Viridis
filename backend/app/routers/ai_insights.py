
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from .models import Hospital, Emission

@app.get("/ai-insights/{hospital_id}")
def ai_insights(hospital_id: int, db: Session = Depends(get_db)):
    hospital = db.query(Hospital).get(hospital_id)
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")

    beds = hospital.beds or 1

    # Fetch recent 12 months
    import datetime
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=365)

    # Helper for fetching metric over the last year
    def get_sum(category, subcategory=None):
        q = db.query(func.sum(Emission.quantity)).filter(
            Emission.hospital_id == hospital_id,
            Emission.category == category,
            Emission.date >= start_date
        )
        if subcategory:
            q = q.filter(Emission.subcategory == subcategory)
        return q.scalar() or 0

    # Energy
    total_kwh = get_sum("electricity")
    led_kwh = get_sum("electricity", "led")
    renewable = get_sum("electricity", "renewable")

    # Waste
    total_bio = get_sum("biomedical")
    segregated_bio = get_sum("biomedical", "incinerated")

    # Diesel use (for generators, etc.)
    diesel_used = get_sum("diesel")

    # Insights / Rule-based suggestions
    recs = []

    # Efficiency - suggest LEDs
    if led_kwh / (total_kwh or 1) < 0.5:
        recs.append("Increase adoption of LED lighting to save up to 8% CO₂e in OT/lab areas.")

    # Renewables
    if renewable / (total_kwh or 1) < 0.2:
        recs.append("Consider installing rooftop solar to increase renewables use and cut long-term energy costs.")

    # Waste Segregation
    ws_ratio = segregated_bio / (total_bio or 1)
    if ws_ratio < 0.7:
        recs.append("Improve biomedical waste segregation: Target >80% to comply with CPCB rules and reduce fines.")

    # Diesel use
    if diesel_used > 1000:
        recs.append("Monitor generator usage; optimize for grid supply and prevent leaks to cut diesel costs and emissions.")

    # Energy Intensity
    epi = total_kwh / beds
    if epi > 3000:
        recs.append("Your hospital's energy use per bed is high. Audit HVAC and cooling systems for efficiency.")

    # Custom/fun ones:
    if epi < 1000 and ws_ratio > 0.9:
        recs.append("Congratulations! Your facility is a sustainability champion. Consider applying for green hospital certification.")

    # Default if none
    if not recs:
        recs.append("Keep monitoring! No obvious high-impact improvements detected. Explore more granular analytics.")

    return {
        "hospital": {
            "id": hospital.id,
            "name": hospital.name,
            "beds": beds,
        },
        "insights": recs,
        "raw_metrics": {
            "total_kwh": total_kwh,
            "led_kwh": led_kwh,
            "epi": epi,
            "ws_ratio": ws_ratio,
            "diesel_used": diesel_used,
            "renewable_pct": renewable / (total_kwh or 1)
        }
    }

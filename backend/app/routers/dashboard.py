@app.get("/dashboard/{hospital_id}")
def get_dashboard_data(hospital_id: int, db: Session = Depends(get_db)):
    # Example summary: total emissions by category
    rows = db.query(Emission.category, func.sum(Emission.co2e))\
        .filter(Emission.hospital_id == hospital_id)\
        .group_by(Emission.category).all()
    return [{"category": row[0], "total_co2e": row[1]} for row in rows]


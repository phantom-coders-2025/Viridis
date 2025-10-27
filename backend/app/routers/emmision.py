from .utils import calculate_co2e, EMISSION_FACTORS

@app.post("/upload-emissions/")
async def upload_emissions(file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = await file.read()
    df = pd.read_csv(pd.io.common.BytesIO(contents))
    
    for _, row in df.iterrows():
        # Use business logic for CO₂e calculation
        calculated_co2e = calculate_co2e(
            category=row['category'],
            quantity=float(row['quantity']),
            subcategory=row.get('subcategory', "")
        )
        
        emission = Emission(
            hospital_id=int(row['hospital_id']),
            department_id=int(row['department_id']),
            date=pd.to_datetime(row['date']),
            category=row['category'],
            subcategory=row.get('subcategory', ""),
            quantity=float(row['quantity']),
            unit=row.get('unit', ""),
            emission_factor=EMISSION_FACTORS.get(row['category'], 0),
            co2e=calculated_co2e  # Calculated using your business logic!
        )
        db.add(emission)
    
    db.commit()
    return {"success": True, "rows": len(df)}


# --------------- EMISSION ENDPOINTS ---------------

@app.post("/emissions/", response_model=schemas.EmissionRead)
def create_emission(emission: schemas.EmissionCreate, db: Session = Depends(get_db)):
    return crud.create_emission(db, emission)

@app.get("/emissions/", response_model=List[schemas.EmissionRead])
def read_emissions(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return crud.get_emissions(db, skip, limit)

@app.get("/emissions/{emission_id}", response_model=schemas.EmissionRead)
def read_emission(emission_id: int, db: Session = Depends(get_db)):
    emit = crud.get_emission(db, emission_id)
    if emit is None:
        raise HTTPException(status_code=404, detail="Emission not found")
    return emit


from fastapi import UploadFile, File
import pandas as pd

@app.post("/upload-emissions/")
async def upload_emissions(file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = await file.read()
    df = pd.read_csv(pd.io.common.BytesIO(contents))
    # Example: process each row
    for _, row in df.iterrows():
        emission = Emission(
            hospital_id=row['hospital_id'],
            department_id=row['department_id'],
            date=pd.to_datetime(row['date']),
            category=row['category'],
            subcategory=row.get('subcategory', ""),
            quantity=row['quantity'],
            unit=row.get('unit', ""),
            emission_factor=row.get('emission_factor', 0.0),
            co2e=row['quantity'] * row['emission_factor']
        )
        db.add(emission)
    db.commit()
    return {"success": True, "rows": len(df)}



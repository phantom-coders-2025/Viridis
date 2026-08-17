from datetime import date
from io import BytesIO
from typing import List, Optional
import pandas as pd
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from .. import crud, models, schemas
from ..business import calculate_co2e, get_emission_factor
from ..database import get_db

router = APIRouter(tags=["Emissions & Ingestion"])


@router.post("/emissions/", response_model=schemas.EmissionRead, status_code=status.HTTP_201_CREATED)
def create_emission(emission: schemas.EmissionCreate, db: Session = Depends(get_db)):
    return crud.create_emission(db, emission)


@router.get("/emissions/", response_model=List[schemas.EmissionRead])
def read_emissions(
    hospital_id: Optional[int] = None,
    department_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    query = db.query(models.Emission)
    if hospital_id is not None:
        query = query.filter(models.Emission.hospital_id == hospital_id)
    if department_id is not None:
        query = query.filter(models.Emission.department_id == department_id)
    return query.order_by(models.Emission.date.desc()).offset(skip).limit(limit).all()


@router.get("/emissions/{emission_id}", response_model=schemas.EmissionRead)
def read_emission(emission_id: int, db: Session = Depends(get_db)):
    emission = crud.get_emission(db, emission_id)
    if emission is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Emission record not found")
    return emission


@router.post("/upload-emissions/", response_model=schemas.CSVUploadResponse)
async def upload_emissions(
    file: UploadFile = File(...),
    hospital_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    if not file.filename or not file.filename.lower().endswith((".csv", ".xlsx", ".xls")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only CSV and Excel files (.csv, .xlsx, .xls) are supported.",
        )

    contents = await file.read()
    try:
        if file.filename.lower().endswith((".xlsx", ".xls")):
            df = pd.read_excel(BytesIO(contents))
        else:
            df = pd.read_csv(BytesIO(contents))
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not parse uploaded spreadsheet: {exc}",
        ) from exc

    if df.empty:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Uploaded file is empty.")

    # Normalize column names: lowercase and stripped
    col_map = {c: str(c).strip().lower() for c in df.columns}
    df = df.rename(columns=col_map)

    # Determine default hospital
    target_hospital = None
    if hospital_id:
        target_hospital = db.get(models.Hospital, hospital_id)
    if not target_hospital:
        target_hospital = db.query(models.Hospital).first()
    if not target_hospital:
        # Create default hospital if none exists
        target_hospital = models.Hospital(name="Default General Hospital", location="Main Campus", beds=250)
        db.add(target_hospital)
        db.commit()
        db.refresh(target_hospital)

    target_hosp_id = target_hospital.id

    # Department lookup cache
    existing_depts = {d.name.lower(): d.id for d in db.query(models.Department).filter(models.Department.hospital_id == target_hosp_id).all()}

    def get_or_create_dept_id(name: str) -> int:
        name_clean = str(name).strip() if pd.notna(name) else "General Ward"
        name_lower = name_clean.lower()
        if name_lower in existing_depts:
            return existing_depts[name_lower]
        new_dept = models.Department(hospital_id=target_hosp_id, name=name_clean)
        db.add(new_dept)
        db.commit()
        db.refresh(new_dept)
        existing_depts[name_lower] = new_dept.id
        return new_dept.id

    added_count = 0

    try:
        # Scenario A: Wide Format (Department, Date, Electricity, Water, Waste, etc.)
        wide_cols = {"electricity", "electricity (kwh)", "water", "water (l)", "waste", "waste (kg)", "biomedical waste (kg)"}
        has_wide_metrics = any(c in df.columns for c in wide_cols)

        if has_wide_metrics and "category" not in df.columns:
            for _, row in df.iterrows():
                dept_col = row.get("department") or row.get("department_name") or "General Ward"
                dept_id = get_or_create_dept_id(dept_col)
                row_date = pd.to_datetime(row.get("date", date.today())).date()

                # Electricity
                elec_val = row.get("electricity (kwh)") if "electricity (kwh)" in row else row.get("electricity")
                if pd.notna(elec_val) and float(elec_val) > 0:
                    val = float(elec_val)
                    factor = get_emission_factor("electricity")
                    db.add(models.Emission(
                        hospital_id=target_hosp_id,
                        department_id=dept_id,
                        date=row_date,
                        category="electricity",
                        subcategory="grid",
                        quantity=val,
                        unit="kWh",
                        emission_factor=factor,
                        co2e=calculate_co2e("electricity", val),
                    ))
                    added_count += 1

                # Water
                water_val = row.get("water (l)") if "water (l)" in row else row.get("water")
                if pd.notna(water_val) and float(water_val) > 0:
                    val = float(water_val)
                    factor = get_emission_factor("water")
                    db.add(models.Emission(
                        hospital_id=target_hosp_id,
                        department_id=dept_id,
                        date=row_date,
                        category="water",
                        subcategory="municipal",
                        quantity=val,
                        unit="L",
                        emission_factor=factor,
                        co2e=calculate_co2e("water", val),
                    ))
                    added_count += 1

                # Waste
                waste_val = (
                    row.get("biomedical waste (kg)")
                    if "biomedical waste (kg)" in row
                    else row.get("waste (kg)") if "waste (kg)" in row else row.get("waste")
                )
                if pd.notna(waste_val) and float(waste_val) > 0:
                    val = float(waste_val)
                    factor = get_emission_factor("biomedical")
                    db.add(models.Emission(
                        hospital_id=target_hosp_id,
                        department_id=dept_id,
                        date=row_date,
                        category="biomedical",
                        subcategory="incinerated",
                        quantity=val,
                        unit="kg",
                        emission_factor=factor,
                        co2e=calculate_co2e("biomedical", val, "incinerated"),
                    ))
                    added_count += 1

        else:
            # Scenario B: Standard Row-by-Row Format
            for _, row in df.iterrows():
                row_hosp_id = int(row.get("hospital_id", target_hosp_id))
                dept_val = row.get("department_id") or row.get("department") or "General"
                if isinstance(dept_val, str) and not dept_val.isdigit():
                    dept_id = get_or_create_dept_id(dept_val)
                else:
                    dept_id = int(dept_val)

                category = str(row.get("category", "electricity")).strip().lower()
                subcategory = str(row.get("subcategory", "")).strip().lower() if pd.notna(row.get("subcategory")) else None
                quantity = float(row.get("quantity", 0.0))
                factor_val = row.get("emission_factor")
                factor = float(factor_val) if pd.notna(factor_val) else get_emission_factor(category, subcategory or "")
                co2e_val = row.get("co2e")
                co2e = float(co2e_val) if pd.notna(co2e_val) else calculate_co2e(category, quantity, subcategory or "")
                row_date = pd.to_datetime(row.get("date", date.today())).date()

                db.add(models.Emission(
                    hospital_id=row_hosp_id,
                    department_id=dept_id,
                    date=row_date,
                    category=category,
                    subcategory=subcategory,
                    quantity=quantity,
                    unit=str(row.get("unit", "units")) if pd.notna(row.get("unit")) else None,
                    emission_factor=factor,
                    co2e=co2e,
                ))
                added_count += 1

        db.commit()
    except (KeyError, TypeError, ValueError, SQLAlchemyError) as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error importing emission records: {exc}",
        ) from exc

    return schemas.CSVUploadResponse(
        success=True,
        rows=added_count,
        message=f"Successfully imported {added_count} emission records into hospital system.",
    )

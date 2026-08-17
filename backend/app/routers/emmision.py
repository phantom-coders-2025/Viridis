from datetime import date
from io import BytesIO
from typing import List, Optional
import pandas as pd
from fastapi import APIRouter, Depends, File, HTTPException, Query, Request, UploadFile, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from .. import crud, models, schemas
from ..business import calculate_co2e, determine_ghg_scope, get_emission_factor
from ..database import get_db
from .auth import get_current_user, record_audit_log, require_roles, validate_hospital_access

router = APIRouter(tags=["Emissions & Telemetry Ingestion"])


@router.post("/emissions/", response_model=schemas.EmissionRead, status_code=status.HTTP_201_CREATED)
def create_emission(
    emission: schemas.EmissionCreate,
    request: Request,
    current_user: models.User = Depends(require_roles("super_admin", "hospital_admin", "department_manager")),
    db: Session = Depends(get_db),
):
    validate_hospital_access(emission.hospital_id, current_user)

    # Automatically resolve GHG Scope & Factor if not explicitly defined
    scope = emission.scope or determine_ghg_scope(emission.category, emission.subcategory or "")
    factor = emission.emission_factor if emission.emission_factor is not None else get_emission_factor(emission.category, emission.subcategory or "")
    co2e = emission.co2e if emission.co2e is not None else calculate_co2e(emission.category, emission.quantity, emission.subcategory or "")

    db_emission = models.Emission(
        hospital_id=emission.hospital_id,
        department_id=emission.department_id,
        date=emission.date,
        category=emission.category.strip().lower(),
        subcategory=emission.subcategory.strip().lower() if emission.subcategory else None,
        scope=scope,
        ghg_gas_type=emission.ghg_gas_type or "CO2e",
        quantity=emission.quantity,
        unit=emission.unit or "units",
        emission_factor=factor,
        co2e=co2e,
        notes=emission.notes,
        recorded_by_user_id=current_user.id,
    )
    db.add(db_emission)
    db.commit()
    db.refresh(db_emission)

    client_ip = request.client.host if request.client else None
    record_audit_log(db, "CREATE_EMISSION", emission.hospital_id, current_user.id, "EMISSION", f"Created {scope} emission: {emission.category} ({co2e} kg CO2e)", client_ip)

    return db_emission


@router.get("/emissions/", response_model=List[schemas.EmissionRead])
def read_emissions(
    hospital_id: Optional[int] = None,
    department_id: Optional[int] = None,
    scope: Optional[str] = None,
    category: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    target_hosp = hospital_id or current_user.hospital_id
    if target_hosp:
        validate_hospital_access(target_hosp, current_user)

    query = db.query(models.Emission)
    if target_hosp:
        query = query.filter(models.Emission.hospital_id == target_hosp)
    if department_id is not None:
        query = query.filter(models.Emission.department_id == department_id)
    if scope:
        query = query.filter(models.Emission.scope.ilike(f"%{scope}%"))
    if category:
        query = query.filter(models.Emission.category.ilike(f"%{category}%"))
    if start_date:
        query = query.filter(models.Emission.date >= start_date)
    if end_date:
        query = query.filter(models.Emission.date <= end_date)

    return query.order_by(models.Emission.date.desc()).offset(skip).limit(limit).all()


@router.get("/emissions/{emission_id}", response_model=schemas.EmissionRead)
def read_emission(
    emission_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    emission = crud.get_emission(db, emission_id)
    if emission is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Emission record not found")
    validate_hospital_access(emission.hospital_id, current_user)
    return emission


@router.delete("/emissions/{emission_id}", status_code=status.HTTP_200_OK)
def delete_emission(
    emission_id: int,
    current_user: models.User = Depends(require_roles("super_admin", "hospital_admin")),
    db: Session = Depends(get_db),
):
    emission = crud.get_emission(db, emission_id)
    if not emission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Emission record not found")
    validate_hospital_access(emission.hospital_id, current_user)

    db.delete(emission)
    db.commit()
    record_audit_log(db, "DELETE_EMISSION", emission.hospital_id, current_user.id, "EMISSION", f"Deleted emission record #{emission_id}")
    return {"success": True, "message": f"Emission record #{emission_id} deleted successfully."}


@router.post("/upload-emissions/", response_model=schemas.CSVUploadResponse)
async def upload_emissions(
    file: UploadFile = File(...),
    hospital_id: Optional[int] = None,
    request: Request = None,
    current_user: models.User = Depends(require_roles("super_admin", "hospital_admin", "department_manager")),
    db: Session = Depends(get_db),
):
    if not file.filename or not file.filename.lower().endswith((".csv", ".xlsx", ".xls")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only CSV and Excel files (.csv, .xlsx, .xls) are supported.",
        )

    target_hosp_id = hospital_id or current_user.hospital_id
    if not target_hosp_id:
        target_hospital = db.query(models.Hospital).first()
        if not target_hospital:
            target_hospital = models.Hospital(name="Apollo Main Green Facility", location="New Delhi", beds=350)
            db.add(target_hospital)
            db.commit()
            db.refresh(target_hospital)
        target_hosp_id = target_hospital.id

    validate_hospital_access(target_hosp_id, current_user)

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
        # Scenario A: Wide Multi-Column Format
        wide_indicators = {"electricity", "electricity (kwh)", "water", "water (l)", "waste", "waste (kg)", "diesel", "diesel (l)", "anesthetic", "desflurane"}
        has_wide_metrics = any(c in df.columns for c in wide_indicators)

        if has_wide_metrics and "category" not in df.columns:
            for _, row in df.iterrows():
                dept_col = row.get("department") or row.get("department_name") or "Inpatient Wards"
                dept_id = get_or_create_dept_id(dept_col)
                row_date = pd.to_datetime(row.get("date", date.today())).date()

                # 1. Electricity (Scope 2)
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
                        scope="Scope 2",
                        ghg_gas_type="CO2e",
                        quantity=val,
                        unit="kWh",
                        emission_factor=factor,
                        co2e=calculate_co2e("electricity", val),
                        recorded_by_user_id=current_user.id,
                    ))
                    added_count += 1

                # 2. Water (Scope 3)
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
                        scope="Scope 3",
                        ghg_gas_type="CO2e",
                        quantity=val,
                        unit="L",
                        emission_factor=factor,
                        co2e=calculate_co2e("water", val),
                        recorded_by_user_id=current_user.id,
                    ))
                    added_count += 1

                # 3. Bio-Medical Waste (Scope 3)
                waste_val = row.get("biomedical waste (kg)") or row.get("waste (kg)") or row.get("waste")
                if pd.notna(waste_val) and float(waste_val) > 0:
                    val = float(waste_val)
                    factor = get_emission_factor("biomedical", "yellow")
                    db.add(models.Emission(
                        hospital_id=target_hosp_id,
                        department_id=dept_id,
                        date=row_date,
                        category="biomedical",
                        subcategory="incinerated",
                        scope="Scope 3",
                        ghg_gas_type="CO2e",
                        quantity=val,
                        unit="kg",
                        emission_factor=factor,
                        co2e=calculate_co2e("biomedical", val, "incinerated"),
                        recorded_by_user_id=current_user.id,
                    ))
                    added_count += 1

                # 4. Diesel (Scope 1)
                diesel_val = row.get("diesel (l)") or row.get("diesel")
                if pd.notna(diesel_val) and float(diesel_val) > 0:
                    val = float(diesel_val)
                    factor = get_emission_factor("diesel")
                    db.add(models.Emission(
                        hospital_id=target_hosp_id,
                        department_id=dept_id,
                        date=row_date,
                        category="diesel",
                        subcategory="generator_set",
                        scope="Scope 1",
                        ghg_gas_type="CO2e",
                        quantity=val,
                        unit="L",
                        emission_factor=factor,
                        co2e=calculate_co2e("diesel", val),
                        recorded_by_user_id=current_user.id,
                    ))
                    added_count += 1

                # 5. Anesthetic Gas (Scope 1)
                anes_val = row.get("desflurane (bottles)") or row.get("anesthetic (kg)") or row.get("desflurane") or row.get("anesthetic")
                if pd.notna(anes_val) and float(anes_val) > 0:
                    val = float(anes_val)
                    factor = get_emission_factor("anesthetic", "desflurane")
                    db.add(models.Emission(
                        hospital_id=target_hosp_id,
                        department_id=dept_id,
                        date=row_date,
                        category="anesthetic",
                        subcategory="desflurane",
                        scope="Scope 1",
                        ghg_gas_type="Desflurane (GWP 2540)",
                        quantity=val,
                        unit="kg",
                        emission_factor=factor,
                        co2e=calculate_co2e("anesthetic", val, "desflurane"),
                        recorded_by_user_id=current_user.id,
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
                scope = str(row.get("scope", "")).strip() if pd.notna(row.get("scope")) and row.get("scope") else determine_ghg_scope(category, subcategory or "")
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
                    scope=scope,
                    ghg_gas_type=str(row.get("ghg_gas_type", "CO2e")),
                    quantity=quantity,
                    unit=str(row.get("unit", "units")) if pd.notna(row.get("unit")) else None,
                    emission_factor=factor,
                    co2e=co2e,
                    recorded_by_user_id=current_user.id,
                ))
                added_count += 1

        db.commit()
    except (KeyError, TypeError, ValueError, SQLAlchemyError) as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error importing emission records: {exc}",
        ) from exc

    record_audit_log(db, "BATCH_EMISSION_IMPORT", target_hosp_id, current_user.id, "EMISSION", f"Imported {added_count} records via spreadsheet {file.filename}")

    return schemas.CSVUploadResponse(
        success=True,
        rows=added_count,
        message=f"Successfully imported {added_count} GHG Scope 1-3 emission records into facility system.",
    )


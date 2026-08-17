from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, models, schemas
from ..database import get_db
from .auth import get_current_user, require_roles, validate_hospital_access

router = APIRouter(tags=["Hospitals & Departments"])


@router.post("/hospitals/", response_model=schemas.HospitalRead, status_code=status.HTTP_201_CREATED)
def create_hospital(hospital: schemas.HospitalCreate, current_user: models.User = Depends(require_roles("super_admin")), db: Session = Depends(get_db)):
    return crud.create_hospital(db, hospital)


@router.get("/hospitals/", response_model=List[schemas.HospitalRead])
def read_hospitals(skip: int = 0, limit: int = 100, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role == "super_admin":
        return crud.get_hospitals(db, skip=skip, limit=limit)
    if current_user.hospital_id:
        h = db.get(models.Hospital, current_user.hospital_id)
        return [h] if h else []
    return []


@router.get("/hospitals/{hospital_id}", response_model=schemas.HospitalRead)
def read_hospital(hospital_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    validate_hospital_access(hospital_id, current_user)
    hospital = crud.get_hospital(db, hospital_id)
    if hospital is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hospital not found")
    return hospital


@router.put("/hospitals/{hospital_id}", response_model=schemas.HospitalRead)
def update_hospital(
    hospital_id: int,
    data: schemas.HospitalBase,
    current_user: models.User = Depends(require_roles("super_admin", "hospital_admin")),
    db: Session = Depends(get_db),
):
    validate_hospital_access(hospital_id, current_user)
    hospital = db.get(models.Hospital, hospital_id)
    if not hospital:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hospital not found")

    hospital.name = data.name
    if data.location is not None:
        hospital.location = data.location
    if data.type is not None:
        hospital.type = data.type
    if data.beds is not None:
        hospital.beds = data.beds
    if data.occupied_beds_avg is not None:
        hospital.occupied_beds_avg = data.occupied_beds_avg
    if data.total_area_sqft is not None:
        hospital.total_area_sqft = data.total_area_sqft

    db.commit()
    db.refresh(hospital)
    return hospital


@router.delete("/hospitals/{hospital_id}", response_model=schemas.HospitalRead)
def delete_hospital(hospital_id: int, current_user: models.User = Depends(require_roles("super_admin")), db: Session = Depends(get_db)):
    hospital = crud.delete_hospital(db, hospital_id)
    if hospital is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hospital not found")
    return hospital


@router.get("/hospitals/{hospital_id}/departments", response_model=List[schemas.DepartmentRead])
def read_hospital_departments(hospital_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    validate_hospital_access(hospital_id, current_user)
    return db.query(models.Department).filter(models.Department.hospital_id == hospital_id).all()


@router.post("/departments/", response_model=schemas.DepartmentRead, status_code=status.HTTP_201_CREATED)
def create_department(
    department: schemas.DepartmentCreate,
    current_user: models.User = Depends(require_roles("super_admin", "hospital_admin")),
    db: Session = Depends(get_db),
):
    validate_hospital_access(department.hospital_id, current_user)
    return crud.create_department(db, department)


@router.get("/departments/", response_model=List[schemas.DepartmentRead])
def read_departments(hospital_id: Optional[int] = None, skip: int = 0, limit: int = 100, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    target_hosp = hospital_id or current_user.hospital_id
    query = db.query(models.Department)
    if target_hosp and current_user.role != "super_admin":
        query = query.filter(models.Department.hospital_id == target_hosp)
    return query.offset(skip).limit(limit).all()


@router.get("/departments/{department_id}", response_model=schemas.DepartmentRead)
def read_department(department_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    department = crud.get_department(db, department_id)
    if department is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")
    validate_hospital_access(department.hospital_id, current_user)
    return department



# --------------- HOSPITAL ENDPOINTS ---------------

@app.post("/hospitals/", response_model=schemas.HospitalRead)
def create_hospital(hospital: schemas.HospitalCreate, db: Session = Depends(get_db)):
    return crud.create_hospital(db, hospital)

@app.get("/hospitals/", response_model=List[schemas.HospitalRead])
def read_hospitals(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return crud.get_hospitals(db, skip, limit)

@app.get("/hospitals/{hospital_id}", response_model=schemas.HospitalRead)
def read_hospital(hospital_id: int, db: Session = Depends(get_db)):
    hospital = crud.get_hospital(db, hospital_id)
    if hospital is None:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return hospital

@app.delete("/hospitals/{hospital_id}", response_model=schemas.HospitalRead)
def delete_hospital(hospital_id: int, db: Session = Depends(get_db)):
    hospital = crud.delete_hospital(db, hospital_id)
    if hospital is None:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return hospital

# --------------- DEPARTMENT ENDPOINTS ---------------

@app.post("/departments/", response_model=schemas.DepartmentRead)
def create_department(department: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    return crud.create_department(db, department)

@app.get("/departments/", response_model=List[schemas.DepartmentRead])
def read_departments(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return crud.get_departments(db, skip, limit)

@app.get("/departments/{department_id}", response_model=schemas.DepartmentRead)
def read_department(department_id: int, db: Session = Depends(get_db)):
    dep = crud.get_department(db, department_id)
    if dep is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return dep



# --------------- ACHIEVEMENT ENDPOINTS ---------------

@app.post("/achievements/", response_model=schemas.AchievementRead)
def create_achievement(ach: schemas.AchievementCreate, db: Session = Depends(get_db)):
    return crud.create_achievement(db, ach)

@app.get("/achievements/", response_model=List[schemas.AchievementRead])
def read_achievements(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return crud.get_achievements(db, skip, limit)

@app.get("/achievements/{achievement_id}", response_model=schemas.AchievementRead)
def read_achievement(achievement_id: int, db: Session = Depends(get_db)):
    ach = crud.get_achievement(db, achievement_id)
    if ach is None:
        raise HTTPException(status_code=404, detail="Achievement not found")
    return ach

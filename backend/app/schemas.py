from pydantic import BaseModel
from typing import Optional, List
from datetime import date

# ---------- HOSPITAL ----------

class HospitalBase(BaseModel):
    name: str
    location: Optional[str] = None
    type: Optional[str] = None
    beds: Optional[int] = None

class HospitalCreate(HospitalBase):
    pass

class HospitalRead(HospitalBase):
    id: int


    model_config = {
        "from_attributes": True
    }

# ---------- DEPARTMENT ----------

class DepartmentBase(BaseModel):
    hospital_id: int
    name: str

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentRead(DepartmentBase):
    id: int


    model_config = {
        "from_attributes": True
    }

# ---------- EMISSION ----------

class EmissionBase(BaseModel):
    hospital_id: int
    department_id: int
    date: date
    category: str
    subcategory: Optional[str] = None
    quantity: float
    unit: Optional[str] = None
    emission_factor: Optional[float] = None
    co2e: float

class EmissionCreate(EmissionBase):
    pass

class EmissionRead(EmissionBase):
    id: int


    model_config = {
        "from_attributes": True
    }

# ---------- COMPLIANCE REPORT ----------

class ComplianceReportBase(BaseModel):
    hospital_id: int
    month: date
    status: Optional[str] = None
    notes: Optional[str] = None

class ComplianceReportCreate(ComplianceReportBase):
    pass

class ComplianceReportRead(ComplianceReportBase):
    id: int


    model_config = {
        "from_attributes": True
    }

# ---------- BENCHMARK ----------

class BenchmarkBase(BaseModel):
    hospital_id: int
    peer_group: Optional[str] = None
    metric: str
    value: float
    ranking: Optional[int] = None

class BenchmarkCreate(BenchmarkBase):
    pass

class BenchmarkRead(BenchmarkBase):
    id: int


    model_config = {
        "from_attributes": True
    }

# ---------- ACHIEVEMENT ----------

class AchievementBase(BaseModel):
    hospital_id: int
    department_id: int
    title: str
    date_earned: date

class AchievementCreate(AchievementBase):
    pass

class AchievementRead(AchievementBase):
    id: int


    model_config = {
        "from_attributes": True
    }

# ------- SAMPLE LIST RESPONSES (for FastAPI endpoints) -------
# class HospitalList(BaseModel):
#     __root__: List[HospitalRead]

# class DepartmentList(BaseModel):
#     __root__: List[DepartmentRead]

# class EmissionList(BaseModel):
#     __root__: List[EmissionRead]

from datetime import date
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, EmailStr

# ---------- AUTH & USER ----------

class UserRegister(BaseModel):
    hospitalName: str
    registrationId: Optional[str] = None
    hospitalType: Optional[str] = None
    location: Optional[str] = None
    email: str
    phone: Optional[str] = None
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserRead(BaseModel):
    id: int
    email: str
    full_name: Optional[str] = None
    phone: Optional[str] = None
    role: str = "admin"
    hospital_id: Optional[int] = None

    model_config = {
        "from_attributes": True
    }

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

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserRead
    hospital: Optional[HospitalRead] = None

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

class EmissionCreate(EmissionBase):
    co2e: Optional[float] = None

class EmissionRead(EmissionBase):
    id: int
    co2e: float

    model_config = {
        "from_attributes": True
    }

# ---------- COMPLIANCE REPORT ----------

class ComplianceReportBase(BaseModel):
    hospital_id: int
    month: date
    status: Optional[str] = "Pending"
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
    department_id: Optional[int] = None
    title: str
    date_earned: date

class AchievementCreate(AchievementBase):
    pass

class AchievementRead(AchievementBase):
    id: int

    model_config = {
        "from_attributes": True
    }

# ---------- DASHBOARD & ANALYTICS SCHEMAS ----------

class DashboardCategorySummary(BaseModel):
    category: str
    total_co2e: float

class DashboardDepartmentHighlight(BaseModel):
    name: str
    co2e: float

class DashboardOverview(BaseModel):
    total_emissions: float
    electricity_co2e: float
    water_co2e: float
    waste_co2e: float
    categories: List[DashboardCategorySummary]
    monthly_trend: List[Dict[str, Any]]
    highest_emitter: Optional[DashboardDepartmentHighlight] = None
    best_performer: Optional[DashboardDepartmentHighlight] = None

# ---------- SUSTAINABILITY SCORE SCHEMAS ----------

class SustainabilityScoreDetails(BaseModel):
    epi: float
    waste_segregation: float
    renewable_pct: float
    trend: float
    total_kwh: float

class SustainabilityScoreResponse(BaseModel):
    grade: str
    score: int
    details: SustainabilityScoreDetails
    recommendations: List[Dict[str, str]]

# ---------- AI INSIGHTS & FORECAST SCHEMAS ----------

class AnomalyAlert(BaseModel):
    id: str
    title: str
    department: str
    category: str
    severity: str
    change_pct: str
    message: str
    recommendation: str
    estimated_savings: str

class SmartRecommendation(BaseModel):
    id: str
    title: str
    description: str
    impact: str
    category: str

class ForecastPoint(BaseModel):
    month_offset: int
    month_label: Optional[str] = None
    predicted_co2e: float

class HistoryPoint(BaseModel):
    date: str
    month_label: Optional[str] = None
    co2e: float

class AIInsightsResponse(BaseModel):
    history: List[HistoryPoint]
    predictions: List[ForecastPoint]
    anomalies: List[AnomalyAlert]
    recommendations: List[SmartRecommendation]

# ---------- PEER COMPARISON SCHEMAS ----------

class PeerHospital(BaseModel):
    id: int
    name: str
    co2_per_bed: float
    renewable_pct: float
    score: int
    rank: int

class PeerComparisonResponse(BaseModel):
    hospital_id: int
    hospital_name: str
    rank: int
    total_peers: int
    co2_per_bed: float
    peer_avg_co2_per_bed: float
    peers: List[PeerHospital]

# ---------- CSV INGESTION SCHEMA ----------

class CSVUploadResponse(BaseModel):
    success: bool
    rows: int
    message: str

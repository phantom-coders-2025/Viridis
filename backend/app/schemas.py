from datetime import date, datetime
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
    role: Optional[str] = "hospital_admin"  # super_admin, hospital_admin, department_manager, auditor


class UserLogin(BaseModel):
    email: str
    password: str


class UserCreateInternal(BaseModel):
    email: str
    password: str
    full_name: Optional[str] = None
    phone: Optional[str] = None
    role: str = "department_manager"
    hospital_id: Optional[int] = None
    department_id: Optional[int] = None


class UserRead(BaseModel):
    id: int
    email: str
    full_name: Optional[str] = None
    phone: Optional[str] = None
    role: str = "hospital_admin"
    is_active: bool = True
    hospital_id: Optional[int] = None
    department_id: Optional[int] = None
    created_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }


# ---------- HOSPITAL ----------

class HospitalBase(BaseModel):
    name: str
    location: Optional[str] = None
    type: Optional[str] = None
    beds: Optional[int] = 250
    occupied_beds_avg: Optional[float] = 200.0
    total_area_sqft: Optional[float] = 150000.0


class HospitalCreate(HospitalBase):
    pass


class HospitalRead(HospitalBase):
    id: int
    created_at: Optional[datetime] = None

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
    floor: Optional[str] = None
    head_of_department: Optional[str] = None


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentRead(DepartmentBase):
    id: int

    model_config = {
        "from_attributes": True
    }


# ---------- EMISSION (SCOPES 1, 2, 3) ----------

class EmissionBase(BaseModel):
    hospital_id: int
    department_id: int
    date: date
    category: str
    subcategory: Optional[str] = None
    scope: Optional[str] = "Scope 2"
    ghg_gas_type: Optional[str] = "CO2e"
    quantity: float
    unit: Optional[str] = None
    emission_factor: Optional[float] = None
    notes: Optional[str] = None


class EmissionCreate(EmissionBase):
    co2e: Optional[float] = None


class EmissionRead(EmissionBase):
    id: int
    co2e: float
    recorded_by_user_id: Optional[int] = None

    model_config = {
        "from_attributes": True
    }


# ---------- COMPLIANCE REPORT ----------

class ComplianceReportBase(BaseModel):
    hospital_id: int
    month: date
    report_type: Optional[str] = "NABH_GREEN_OT"
    status: Optional[str] = "Submitted"
    compliance_score: Optional[float] = 85.0
    notes: Optional[str] = None


class ComplianceReportCreate(ComplianceReportBase):
    pass


class ComplianceReportRead(ComplianceReportBase):
    id: int
    generated_by: Optional[str] = None
    created_at: Optional[datetime] = None

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
    badge_code: Optional[str] = None
    points: Optional[int] = 100
    date_earned: date


class AchievementCreate(AchievementBase):
    pass


class AchievementRead(AchievementBase):
    id: int

    model_config = {
        "from_attributes": True
    }


# ---------- AUDIT LOG SCHEMA ----------

class AuditLogRead(BaseModel):
    id: int
    hospital_id: Optional[int] = None
    user_id: Optional[int] = None
    action: str
    entity_type: Optional[str] = None
    details: Optional[str] = None
    ip_address: Optional[str] = None
    timestamp: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }


# ---------- SIMULATION SCHEMAS ----------

class SimulationRequest(BaseModel):
    hospital_id: int
    name: Optional[str] = "Decarbonization Pathway 2026-2030"
    solar_capacity_kw: float = 0.0  # Rooftop solar kW
    led_retrofit_pct: float = 0.0  # 0 to 100%
    anesthetic_switch_pct: float = 0.0  # % shift from Desflurane to Sevoflurane/TIVA
    waste_autoclave_pct: float = 0.0  # % waste diverted to autoclave from incineration


class SimulationResult(BaseModel):
    hospital_id: int
    baseline_annual_co2e_kg: float
    projected_annual_co2e_kg: float
    co2e_reduction_kg: float
    co2e_reduction_pct: float
    monthly_savings_inr: float
    annual_savings_inr: float
    estimated_capex_inr: float
    payback_years: float
    scope1_reduction_kg: float
    scope2_reduction_kg: float
    scope3_reduction_kg: float
    roi_breakdown: List[Dict[str, Any]]


# ---------- DASHBOARD & ANALYTICS SCHEMAS ----------

class DashboardCategorySummary(BaseModel):
    category: str
    total_co2e: float
    scope: Optional[str] = "Scope 2"


class DashboardDepartmentHighlight(BaseModel):
    name: str
    co2e: float


class DashboardOverview(BaseModel):
    total_emissions: float
    scope1_co2e: float
    scope2_co2e: float
    scope3_co2e: float
    electricity_co2e: float
    water_co2e: float
    waste_co2e: float
    anesthetic_co2e: float
    # Normalized KPIs
    epi_kwh_per_bed_year: float
    water_liters_per_bed_day: float
    waste_kg_per_bed_day: float
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
    scope1_pct: float
    scope2_pct: float
    scope3_pct: float


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
    scope: str
    severity: str
    change_pct: str
    message: str
    recommendation: str
    estimated_savings: str
    z_score: Optional[float] = None


class SmartRecommendation(BaseModel):
    id: str
    title: str
    description: str
    impact: str
    category: str
    potential_savings_inr: Optional[str] = None
    potential_co2_cut_kg: Optional[str] = None


class ForecastPoint(BaseModel):
    month_offset: int
    month_label: Optional[str] = None
    predicted_co2e: float
    upper_bound: Optional[float] = None
    lower_bound: Optional[float] = None


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


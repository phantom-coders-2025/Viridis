from sqlalchemy import Boolean, Column, Date, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship
from .database import Base


class Hospital(Base):
    __tablename__ = "hospitals"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    location = Column(String(100))
    type = Column(String(50))
    beds = Column(Integer, default=250)
    occupied_beds_avg = Column(Float, default=200.0)
    total_area_sqft = Column(Float, default=150000.0)
    created_at = Column(DateTime, server_default=func.now())

    departments = relationship("Department", back_populates="hospital", cascade="all, delete-orphan")
    emissions = relationship("Emission", back_populates="hospital", cascade="all, delete-orphan")
    compliance_reports = relationship("ComplianceReport", back_populates="hospital", cascade="all, delete-orphan")
    benchmarks = relationship("Benchmark", back_populates="hospital", cascade="all, delete-orphan")
    achievements = relationship("Achievement", back_populates="hospital", cascade="all, delete-orphan")
    users = relationship("User", back_populates="hospital", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="hospital", cascade="all, delete-orphan")
    simulations = relationship("SimulationScenario", back_populates="hospital", cascade="all, delete-orphan")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(120), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=True)
    phone = Column(String(30), nullable=True)
    # 4-Tier Roles: super_admin, hospital_admin, department_manager, auditor
    role = Column(String(30), default="hospital_admin")
    is_active = Column(Boolean, default=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    hospital = relationship("Hospital", back_populates="users")
    department = relationship("Department")
    audit_logs = relationship("AuditLog", back_populates="user")


class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, index=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    name = Column(String(50), nullable=False)
    floor = Column(String(30), nullable=True)
    head_of_department = Column(String(100), nullable=True)

    hospital = relationship("Hospital", back_populates="departments")
    emissions = relationship("Emission", back_populates="department", cascade="all, delete-orphan")
    achievements = relationship("Achievement", back_populates="department")


class Emission(Base):
    __tablename__ = "emissions"
    id = Column(Integer, primary_key=True, index=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    department_id = Column(Integer, ForeignKey("departments.id"))
    date = Column(Date, nullable=False)
    category = Column(String(30), nullable=False)  # electricity, diesel, anesthetic, biomedical, water, etc.
    subcategory = Column(String(50))  # e.g., grid, solar_rooftop, yellow_incinerated, red_autoclaved, desflurane
    # GHG Protocol Scope: Scope 1 (Direct), Scope 2 (Indirect Energy), Scope 3 (Value Chain / Waste / Water)
    scope = Column(String(20), default="Scope 2", nullable=False)
    ghg_gas_type = Column(String(50), default="CO2e")  # CO2, CH4, N2O, Desflurane, Sevoflurane, etc.
    quantity = Column(Float, nullable=False)
    unit = Column(String(20))
    emission_factor = Column(Float)
    co2e = Column(Float, nullable=False)  # Total kg CO2e
    notes = Column(Text, nullable=True)
    recorded_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    hospital = relationship("Hospital", back_populates="emissions")
    department = relationship("Department", back_populates="emissions")
    recorder = relationship("User")


class ComplianceReport(Base):
    __tablename__ = "compliance_reports"
    id = Column(Integer, primary_key=True, index=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    month = Column(Date, nullable=False)
    report_type = Column(String(50), default="NABH_GREEN_OT")  # NABH_GREEN_OT, CPCB_FORM_IV, GHG_CORPORATE_STANDARD
    status = Column(String(20), default="Submitted")  # Draft, Submitted, Audited, Certified
    compliance_score = Column(Float, default=85.0)
    notes = Column(Text)
    generated_by = Column(String(100), nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    hospital = relationship("Hospital", back_populates="compliance_reports")


class Benchmark(Base):
    __tablename__ = "benchmarks"
    id = Column(Integer, primary_key=True, index=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    peer_group = Column(String(100))
    metric = Column(String(50))
    value = Column(Float)
    ranking = Column(Integer)

    hospital = relationship("Hospital", back_populates="benchmarks")


class Achievement(Base):
    __tablename__ = "achievements"
    id = Column(Integer, primary_key=True, index=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    title = Column(String(100))
    badge_code = Column(String(50), nullable=True)
    points = Column(Integer, default=100)
    date_earned = Column(Date)

    hospital = relationship("Hospital", back_populates="achievements")
    department = relationship("Department", back_populates="achievements")


class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String(100), nullable=False)  # e.g., "LOGIN", "EMISSION_IMPORT", "COMPLIANCE_EXPORT", "USER_CREATE"
    entity_type = Column(String(50), nullable=True)  # "EMISSION", "REPORT", "USER", "AUTH"
    details = Column(Text, nullable=True)
    ip_address = Column(String(45), nullable=True)
    timestamp = Column(DateTime, server_default=func.now())

    hospital = relationship("Hospital", back_populates="audit_logs")
    user = relationship("User", back_populates="audit_logs")


class SimulationScenario(Base):
    __tablename__ = "simulation_scenarios"
    id = Column(Integer, primary_key=True, index=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    solar_capacity_kw = Column(Float, default=0.0)
    led_retrofit_pct = Column(Float, default=0.0)
    anesthetic_switch_pct = Column(Float, default=0.0)
    waste_autoclave_pct = Column(Float, default=0.0)
    projected_co2e_reduction_kg = Column(Float, default=0.0)
    projected_monthly_savings_inr = Column(Float, default=0.0)
    estimated_capex_inr = Column(Float, default=0.0)
    payback_years = Column(Float, default=0.0)
    created_at = Column(DateTime, server_default=func.now())

    hospital = relationship("Hospital", back_populates="simulations")


import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import numpy as np

from app.main import app
from app.database import Base, get_db
from app.models import Hospital, Department, User, Emission, ComplianceReport
from app.routers.auth import hash_password, create_access_token
from app.business import calculate_whatif_simulation, EMISSION_FACTORS

# In-memory SQLite for isolated test suite
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_viridis.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(scope="session", autouse=True)
def setup_test_data():
    db = TestingSessionLocal()
    
    # 1. Hospitals
    h1 = Hospital(id=1, name="Apollo Green Care Hospital", location="Chennai, Tamil Nadu", beds=450, total_area_sqft=320000)
    h2 = Hospital(id=2, name="Fortis Healthcare Facility", location="Bengaluru, Karnataka", beds=300, total_area_sqft=210000)
    db.add_all([h1, h2])
    db.commit()

    # 2. Departments
    d1 = Department(id=1, hospital_id=1, name="Operating Theatres & Surgical Suites")
    d2 = Department(id=2, hospital_id=1, name="Intensive Care Unit (ICU)")
    db.add_all([d1, d2])
    db.commit()

    # 3. Users with 4-tier roles
    u_admin = User(
        id=1,
        email="admin@apollo.com",
        hashed_password=hash_password("Admin@12345"),
        role="hospital_admin",
        hospital_id=1,
        full_name="Dr. Arvind Sharma"
    )
    u_super = User(
        id=2,
        email="superadmin@viridis.io",
        hashed_password=hash_password("Super@12345"),
        role="super_admin",
        hospital_id=None,
        full_name="Viridis ESG Auditor"
    )
    u_dept = User(
        id=3,
        email="facility@apollo.com",
        hashed_password=hash_password("Facility@12345"),
        role="department_manager",
        hospital_id=1,
        department_id=1,
        full_name="Priya Nair"
    )
    u_auditor = User(
        id=4,
        email="auditor@esg-cert.org",
        hashed_password=hash_password("Auditor@12345"),
        role="auditor",
        hospital_id=1,
        full_name="Kavita Iyer"
    )
    db.add_all([u_admin, u_super, u_dept, u_auditor])
    db.commit()

    from datetime import date as dt_date
    # 4. Multi-Month Scope 1-3 Emissions (May, June, July 2026)
    emissions = [
        # May 2026
        Emission(hospital_id=1, department_id=1, category="electricity", subcategory="grid", scope="Scope 2", quantity=14000.0, unit="kWh", emission_factor=0.82, co2e=14000.0 * 0.82, date=dt_date(2026, 5, 15)),
        Emission(hospital_id=1, department_id=1, category="biomedical", subcategory="yellow_incinerated", scope="Scope 3", quantity=380.0, unit="kg", emission_factor=2.85, co2e=380.0 * 2.85, date=dt_date(2026, 5, 15)),
        Emission(hospital_id=1, department_id=1, category="anesthetic", subcategory="desflurane", scope="Scope 1", quantity=1.8, unit="kg", ghg_gas_type="Desflurane (GWP 2540)", emission_factor=2540.0, co2e=1.8 * 2540.0, date=dt_date(2026, 5, 15)),
        
        # June 2026
        Emission(hospital_id=1, department_id=1, category="electricity", subcategory="grid", scope="Scope 2", quantity=15000.0, unit="kWh", emission_factor=0.82, co2e=15000.0 * 0.82, date=dt_date(2026, 6, 15)),
        Emission(hospital_id=1, department_id=1, category="biomedical", subcategory="yellow_incinerated", scope="Scope 3", quantity=400.0, unit="kg", emission_factor=2.85, co2e=400.0 * 2.85, date=dt_date(2026, 6, 15)),
        Emission(hospital_id=1, department_id=1, category="anesthetic", subcategory="desflurane", scope="Scope 1", quantity=2.0, unit="kg", ghg_gas_type="Desflurane (GWP 2540)", emission_factor=2540.0, co2e=2.0 * 2540.0, date=dt_date(2026, 6, 15)),

        # July 2026
        Emission(hospital_id=1, department_id=1, category="electricity", subcategory="grid", scope="Scope 2", quantity=16200.0, unit="kWh", emission_factor=0.82, co2e=16200.0 * 0.82, date=dt_date(2026, 7, 15)),
        Emission(hospital_id=1, department_id=1, category="biomedical", subcategory="yellow_incinerated", scope="Scope 3", quantity=420.0, unit="kg", emission_factor=2.85, co2e=420.0 * 2.85, date=dt_date(2026, 7, 15)),
        Emission(hospital_id=1, department_id=1, category="anesthetic", subcategory="desflurane", scope="Scope 1", quantity=2.2, unit="kg", ghg_gas_type="Desflurane (GWP 2540)", emission_factor=2540.0, co2e=2.2 * 2540.0, date=dt_date(2026, 7, 15)),
    ]
    db.add_all(emissions)
    db.commit()
    db.close()




def test_auth_login_and_token_generation():
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@apollo.com", "password": "Admin@12345"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["role"] == "hospital_admin"
    assert data["user"]["hospital_id"] == 1


def test_auth_me_endpoint():
    token = create_access_token(data={"sub": "admin@apollo.com", "role": "hospital_admin", "hospital_id": 1})
    response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["email"] == "admin@apollo.com"
    assert data["hospital"]["id"] == 1


def test_rbac_super_admin_access():
    super_token = create_access_token(data={"sub": "superadmin@viridis.io", "role": "super_admin"})
    response = client.get("/api/v1/auth/users", headers={"Authorization": f"Bearer {super_token}"})
    assert response.status_code == 200
    users = response.json()
    assert len(users) >= 4


def test_rbac_denial_for_unauthorized_role():
    # department_manager should not be able to list all enterprise users
    dept_token = create_access_token(data={"sub": "facility@apollo.com", "role": "department_manager", "hospital_id": 1})
    response = client.get("/api/v1/auth/users", headers={"Authorization": f"Bearer {dept_token}"})
    assert response.status_code == 403


def test_multi_tenancy_cross_hospital_isolation():
    # User from hospital 1 attempting to access hospital 2
    token = create_access_token(data={"sub": "admin@apollo.com", "role": "hospital_admin", "hospital_id": 1})
    response = client.get("/api/v1/dashboard/overview/2", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403


def test_dashboard_scopes_telemetry():
    token = create_access_token(data={"sub": "admin@apollo.com", "role": "hospital_admin", "hospital_id": 1})
    response = client.get("/api/v1/dashboard/overview/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert "scope1_co2e" in data
    assert "scope2_co2e" in data
    assert "scope3_co2e" in data
    assert data["scope1_co2e"] > 0
    assert data["scope2_co2e"] > 0
    assert data["scope3_co2e"] > 0
    assert "epi_kwh_per_bed_year" in data


def test_ai_insights_and_anomaly_engine():
    token = create_access_token(data={"sub": "admin@apollo.com", "role": "hospital_admin", "hospital_id": 1})
    response = client.get("/api/v1/ai-insights/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert "predictions" in data
    assert "anomalies" in data
    assert len(data["predictions"]) > 0


def test_what_if_decarbonization_simulator_calculation():
    sim = calculate_whatif_simulation(
        baseline_annual_co2e=300000.0,
        baseline_electricity_kwh=180000.0,
        baseline_waste_kg=5000.0,
        solar_capacity_kw=100.0,
        led_retrofit_pct=80.0,
        anesthetic_switch_pct=90.0,
        waste_autoclave_pct=50.0
    )
    assert sim["co2e_reduction_kg"] > 0
    assert sim["co2e_reduction_pct"] > 0
    assert sim["annual_savings_inr"] > 0
    assert sim["payback_years"] > 0
    assert len(sim["roi_breakdown"]) == 4



def test_compliance_report_generation_nabh():
    token = create_access_token(data={"sub": "admin@apollo.com", "role": "hospital_admin", "hospital_id": 1})
    response = client.post(
        "/api/v1/compliance-reports/generate/1?report_type=NABH_GREEN_OT",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    filing = response.json()
    assert filing["report_type"] == "NABH_GREEN_OT"
    assert filing["compliance_score"] >= 80
    assert len(filing["audit_checklist"]) >= 3

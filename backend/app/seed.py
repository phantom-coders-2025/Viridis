from datetime import date, timedelta
import random
from sqlalchemy import text
from sqlalchemy.orm import Session

from .business import calculate_co2e, get_emission_factor
from .database import Base, SessionLocal, engine
from .models import Achievement, Benchmark, ComplianceReport, Department, Emission, Hospital


def seed_database(db: Session = None):
    close_at_end = False
    if db is None:
        db = SessionLocal()
        close_at_end = True

    # Ensure tables exist
    Base.metadata.create_all(bind=engine)

    try:
        # Clear child tables first
        db.query(Emission).delete()
        db.query(Achievement).delete()
        db.query(ComplianceReport).delete()
        db.query(Benchmark).delete()
        db.query(Department).delete()
        db.query(Hospital).delete()
        db.commit()

        # Reset Postgres sequences if applicable
        if db.bind and db.bind.dialect.name == "postgresql":
            try:
                for seq in [
                    "hospitals_id_seq",
                    "departments_id_seq",
                    "emissions_id_seq",
                    "benchmarks_id_seq",
                    "compliance_reports_id_seq",
                    "achievements_id_seq",
                ]:
                    db.execute(text(f"ALTER SEQUENCE IF EXISTS {seq} RESTART WITH 1;"))
                db.commit()
            except Exception:
                db.rollback()

        # 1. Hospital
        hospital = Hospital(
            name="Apollo Green Care Hospital",
            location="Chennai Central Campus",
            type="Tertiary Care Multi-Speciality",
            beds=350,
        )
        db.add(hospital)
        db.commit()
        db.refresh(hospital)

        # 2. Departments
        dept_names = [
            "Operating Theatres",
            "Intensive Care Unit (ICU)",
            "General Inpatient Wards",
            "Radiology & Imaging",
            "Outpatient Department (OPD)",
        ]

        departments = {}
        for name in dept_names:
            dept = Department(hospital_id=hospital.id, name=name)
            db.add(dept)
            db.commit()
            db.refresh(dept)
            departments[name] = dept

        # 3. Generate 12 months of realistic emissions
        today = date.today()
        dept_profiles = {
            "Operating Theatres": {"elec": 4500, "water": 18000, "bio_inc": 420, "bio_auto": 280},
            "Intensive Care Unit (ICU)": {"elec": 5200, "water": 22000, "bio_inc": 350, "bio_auto": 310},
            "General Inpatient Wards": {"elec": 3800, "water": 35000, "bio_inc": 210, "bio_auto": 450},
            "Radiology & Imaging": {"elec": 3100, "water": 8000, "bio_inc": 50, "bio_auto": 80},
            "Outpatient Department (OPD)": {"elec": 1900, "water": 12000, "bio_inc": 80, "bio_auto": 120},
        }

        emissions_to_add = []

        for m_idx in range(12, 0, -1):
            m_date = (today.replace(day=1) - timedelta(days=m_idx * 30)).replace(day=15)
            seasonal_factor = 1.0 + (0.15 * ((12 - m_idx) % 4 == 0)) - (0.05 * (m_idx > 8))

            for dept_name, profile in dept_profiles.items():
                dept = departments[dept_name]

                # Electricity Grid
                elec_qty = round(profile["elec"] * seasonal_factor * random.uniform(0.95, 1.05), 1)
                elec_factor = get_emission_factor("electricity")
                emissions_to_add.append(
                    Emission(
                        hospital_id=hospital.id,
                        department_id=dept.id,
                        date=m_date,
                        category="electricity",
                        subcategory="grid",
                        quantity=elec_qty,
                        unit="kWh",
                        emission_factor=elec_factor,
                        co2e=calculate_co2e("electricity", elec_qty),
                    )
                )

                # Renewable Solar Electricity
                solar_qty = round(elec_qty * 0.40, 1)
                emissions_to_add.append(
                    Emission(
                        hospital_id=hospital.id,
                        department_id=dept.id,
                        date=m_date,
                        category="electricity",
                        subcategory="renewable",
                        quantity=solar_qty,
                        unit="kWh",
                        emission_factor=0.0,
                        co2e=0.0,
                    )
                )

                # Water
                water_qty = round(profile["water"] * random.uniform(0.92, 1.08), 1)
                water_factor = get_emission_factor("water")
                emissions_to_add.append(
                    Emission(
                        hospital_id=hospital.id,
                        department_id=dept.id,
                        date=m_date,
                        category="water",
                        subcategory="municipal",
                        quantity=water_qty,
                        unit="L",
                        emission_factor=water_factor,
                        co2e=calculate_co2e("water", water_qty),
                    )
                )

                # Biomedical Incinerated Waste
                bio_inc_qty = round(profile["bio_inc"] * random.uniform(0.90, 1.10), 1)
                bio_inc_factor = get_emission_factor("biomedical", "incinerated")
                emissions_to_add.append(
                    Emission(
                        hospital_id=hospital.id,
                        department_id=dept.id,
                        date=m_date,
                        category="biomedical",
                        subcategory="incinerated",
                        quantity=bio_inc_qty,
                        unit="kg",
                        emission_factor=bio_inc_factor,
                        co2e=calculate_co2e("biomedical", bio_inc_qty, "incinerated"),
                    )
                )

                # Biomedical Autoclaved / Recycled Waste
                bio_auto_qty = round(profile["bio_auto"] * random.uniform(0.95, 1.05), 1)
                bio_auto_factor = get_emission_factor("biomedical", "autoclaved")
                emissions_to_add.append(
                    Emission(
                        hospital_id=hospital.id,
                        department_id=dept.id,
                        date=m_date,
                        category="biomedical",
                        subcategory="autoclaved",
                        quantity=bio_auto_qty,
                        unit="kg",
                        emission_factor=bio_auto_factor,
                        co2e=calculate_co2e("biomedical", bio_auto_qty, "autoclaved"),
                    )
                )

        db.add_all(emissions_to_add)
        db.commit()

        # 4. Benchmarks
        benchmarks = [
            Benchmark(
                hospital_id=hospital.id,
                peer_group="Tier-1 Metro Hospitals",
                metric="Energy Performance Index (kWh/bed)",
                value=42.5,
                ranking=2,
            ),
            Benchmark(
                hospital_id=hospital.id,
                peer_group="Tier-1 Metro Hospitals",
                metric="Renewable Energy Adoption (%)",
                value=40.0,
                ranking=1,
            ),
            Benchmark(
                hospital_id=hospital.id,
                peer_group="Tier-1 Metro Hospitals",
                metric="Waste Diversion Rate (%)",
                value=78.2,
                ranking=3,
            ),
            Benchmark(
                hospital_id=hospital.id,
                peer_group="Tier-1 Metro Hospitals",
                metric="Water Consumption (L/bed/day)",
                value=240.0,
                ranking=4,
            ),
        ]
        db.add_all(benchmarks)

        # 5. Compliance Reports
        reports = [
            ComplianceReport(
                hospital_id=hospital.id,
                month=(today.replace(day=1) - timedelta(days=30)).replace(day=1),
                status="Approved",
                notes="State Pollution Control Board biomedical waste manifest verified with zero discrepancies.",
            ),
            ComplianceReport(
                hospital_id=hospital.id,
                month=(today.replace(day=1) - timedelta(days=60)).replace(day=1),
                status="Approved",
                notes="Quarterly ESG carbon audit report certified by external auditor.",
            ),
            ComplianceReport(
                hospital_id=hospital.id,
                month=(today.replace(day=1) - timedelta(days=90)).replace(day=1),
                status="Submitted",
                notes="National Clean Air & Energy Efficiency disclosures logged.",
            ),
            ComplianceReport(
                hospital_id=hospital.id,
                month=today.replace(day=1),
                status="Generated",
                notes="Current month draft environmental compliance certificate generated.",
            ),
        ]
        db.add_all(reports)

        # 6. Achievements
        achievements = [
            Achievement(
                hospital_id=hospital.id,
                department_id=departments["Operating Theatres"].id,
                title="Zero Non-Compliant Biomedical Waste Spillage",
                date_earned=today - timedelta(days=45),
            ),
            Achievement(
                hospital_id=hospital.id,
                department_id=departments["Intensive Care Unit (ICU)"].id,
                title="Solar Energy Adoption Milestone (40% Rooftop Solar)",
                date_earned=today - timedelta(days=90),
            ),
            Achievement(
                hospital_id=hospital.id,
                department_id=departments["General Inpatient Wards"].id,
                title="Smart Water Aerator Installation & 15% Reduction",
                date_earned=today - timedelta(days=120),
            ),
            Achievement(
                hospital_id=hospital.id,
                department_id=None,
                title="Green Hospital Gold Certification Grade A",
                date_earned=today - timedelta(days=15),
            ),
        ]
        db.add_all(achievements)
        db.commit()

        print(f"[SUCCESS] Successfully seeded 1 hospital, 5 departments, {len(emissions_to_add)} emissions, {len(benchmarks)} benchmarks, {len(reports)} reports, and {len(achievements)} achievements.")
        return {
            "status": "success",
            "hospital": hospital.name,
            "hospital_id": hospital.id,
            "departments": len(departments),
            "emissions_records": len(emissions_to_add),
            "benchmarks": len(benchmarks),
            "compliance_reports": len(reports),
            "achievements": len(achievements),
        }

    finally:
        if close_at_end:
            db.close()


if __name__ == "__main__":
    seed_database()

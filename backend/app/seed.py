from datetime import date, timedelta
import random
from sqlalchemy import text
from sqlalchemy.orm import Session

from .business import calculate_co2e, get_emission_factor
from .database import Base, SessionLocal, engine
from .models import Achievement, AuditLog, Benchmark, ComplianceReport, Department, Emission, Hospital, SimulationScenario, User
from .routers.auth import hash_password


def seed_database(db: Session = None):
    close_at_end = False
    if db is None:
        db = SessionLocal()
        close_at_end = True

    # Ensure tables exist
    Base.metadata.create_all(bind=engine)

    try:
        # Clear existing tables cleanly
        db.query(AuditLog).delete()
        db.query(SimulationScenario).delete()
        db.query(User).delete()
        db.query(Emission).delete()
        db.query(Achievement).delete()
        db.query(ComplianceReport).delete()
        db.query(Benchmark).delete()
        db.query(Department).delete()
        db.query(Hospital).delete()
        db.commit()

        # 1. Main Hospital Facility
        hospital = Hospital(
            name="Apollo Green Care Super-Speciality",
            location="New Delhi Medical District",
            type="Tertiary Care Multi-Speciality",
            beds=350,
            occupied_beds_avg=295.0,
            total_area_sqft=220000.0,
        )
        db.add(hospital)

        # Secondary peer hospital for benchmarking
        peer_hospital = Hospital(
            name="Fortis Eco Health Institute",
            location="Gurugram Campus",
            type="Multi-Speciality",
            beds=280,
            occupied_beds_avg=220.0,
            total_area_sqft=160000.0,
        )
        db.add(peer_hospital)
        db.commit()
        db.refresh(hospital)
        db.refresh(peer_hospital)

        # 2. 4-Tier RBAC Demo Users
        users_to_seed = [
            User(
                email="admin@apollo.com",
                hashed_password=hash_password("admin123"),
                full_name="Dr. Rajesh Sharma (Chief Administrator)",
                phone="+91 98765 43210",
                role="hospital_admin",
                hospital_id=hospital.id,
            ),
            User(
                email="superadmin@viridis.io",
                hashed_password=hash_password("super123"),
                full_name="Viridis Platform Director",
                phone="+91 99999 88888",
                role="super_admin",
                hospital_id=None,
            ),
            User(
                email="facility@apollo.com",
                hashed_password=hash_password("facility123"),
                full_name="Anita Roy (Facility & Energy Lead)",
                phone="+91 98111 22233",
                role="department_manager",
                hospital_id=hospital.id,
            ),
            User(
                email="auditor@esg-cert.org",
                hashed_password=hash_password("auditor123"),
                full_name="Vikram Seth (NABH Lead ESG Auditor)",
                phone="+91 97222 33344",
                role="auditor",
                hospital_id=hospital.id,
            ),
        ]
        db.add_all(users_to_seed)
        db.commit()

        # 3. Departments
        dept_names = [
            ("Operating Theatres", "3rd Floor Wing A", "Dr. A. Mehra"),
            ("Intensive Care Unit (ICU)", "2nd Floor Critical Care", "Dr. S. Kulkarni"),
            ("General Inpatient Wards", "Floors 4-7", "Sister In-charge Rita"),
            ("Radiology & Imaging", "Ground Floor Diagnostic", "Dr. P. Nair"),
            ("Central Sterile Supply (CSSD)", "Basement Block B", "Eng. R. Verma"),
            ("Facilities & Energy Plant", "Utility Block", "Eng. K. Das"),
        ]

        departments = {}
        for name, floor, hod in dept_names:
            dept = Department(hospital_id=hospital.id, name=name, floor=floor, head_of_department=hod)
            db.add(dept)
            db.commit()
            db.refresh(dept)
            departments[name] = dept

        # 4. Generate 12 Months of Comprehensive GHG Scope 1, 2, 3 Emissions
        today = date.today()
        dept_profiles = {
            "Operating Theatres": {
                "elec": 6200, "water": 14000,
                "bio_yellow": 480, "bio_red": 320, "bio_blue": 110, "bio_white": 45,
                "anesthetic_desflurane": 4.5, "anesthetic_sevoflurane": 18.0,
            },
            "Intensive Care Unit (ICU)": {
                "elec": 7500, "water": 26000,
                "bio_yellow": 410, "bio_red": 390, "bio_blue": 95, "bio_white": 35,
                "anesthetic_desflurane": 0.0, "anesthetic_sevoflurane": 0.0,
            },
            "General Inpatient Wards": {
                "elec": 5400, "water": 48000,
                "bio_yellow": 240, "bio_red": 510, "bio_blue": 140, "bio_white": 25,
                "anesthetic_desflurane": 0.0, "anesthetic_sevoflurane": 0.0,
            },
            "Radiology & Imaging": {
                "elec": 4600, "water": 7500,
                "bio_yellow": 60, "bio_red": 85, "bio_blue": 40, "bio_white": 10,
                "anesthetic_desflurane": 0.0, "anesthetic_sevoflurane": 0.0,
            },
            "Central Sterile Supply (CSSD)": {
                "elec": 4100, "water": 22000,
                "bio_yellow": 90, "bio_red": 140, "bio_blue": 30, "bio_white": 15,
                "anesthetic_desflurane": 0.0, "anesthetic_sevoflurane": 0.0,
            },
            "Facilities & Energy Plant": {
                "elec": 2800, "water": 31000,
                "bio_yellow": 20, "bio_red": 30, "bio_blue": 10, "bio_white": 5,
                "diesel": 380.0,
                "anesthetic_desflurane": 0.0, "anesthetic_sevoflurane": 0.0,
            },
        }

        emissions_to_add = []

        for m_idx in range(12, 0, -1):
            m_date = (today.replace(day=1) - timedelta(days=m_idx * 30)).replace(day=15)
            # Seasonal factor for Indian climate (Peak HVAC in May-July)
            month_num = m_date.month
            summer_surge = 1.22 if month_num in [5, 6, 7] else 1.05 if month_num in [4, 8, 9] else 0.94

            for dept_name, profile in dept_profiles.items():
                dept = departments[dept_name]

                # Scope 2: Grid Electricity
                elec_qty = round(profile["elec"] * summer_surge * random.uniform(0.96, 1.04), 1)
                emissions_to_add.append(
                    Emission(
                        hospital_id=hospital.id,
                        department_id=dept.id,
                        date=m_date,
                        category="electricity",
                        subcategory="grid",
                        scope="Scope 2",
                        ghg_gas_type="CO2e",
                        quantity=elec_qty,
                        unit="kWh",
                        emission_factor=get_emission_factor("electricity"),
                        co2e=calculate_co2e("electricity", elec_qty),
                    )
                )

                # Scope 3: Municipal Water
                water_qty = round(profile["water"] * random.uniform(0.94, 1.06), 1)
                emissions_to_add.append(
                    Emission(
                        hospital_id=hospital.id,
                        department_id=dept.id,
                        date=m_date,
                        category="water",
                        subcategory="municipal",
                        scope="Scope 3",
                        ghg_gas_type="CO2e",
                        quantity=water_qty,
                        unit="L",
                        emission_factor=get_emission_factor("water"),
                        co2e=calculate_co2e("water", water_qty),
                    )
                )

                # Scope 3: CPCB Yellow Incinerated Waste
                yellow_qty = round(profile["bio_yellow"] * random.uniform(0.92, 1.08), 1)
                emissions_to_add.append(
                    Emission(
                        hospital_id=hospital.id,
                        department_id=dept.id,
                        date=m_date,
                        category="biomedical",
                        subcategory="yellow_incinerated",
                        scope="Scope 3",
                        ghg_gas_type="CO2e",
                        quantity=yellow_qty,
                        unit="kg",
                        emission_factor=get_emission_factor("biomedical", "yellow"),
                        co2e=calculate_co2e("biomedical", yellow_qty, "yellow"),
                    )
                )

                # Scope 3: CPCB Red Autoclaved Waste
                red_qty = round(profile["bio_red"] * random.uniform(0.92, 1.08), 1)
                emissions_to_add.append(
                    Emission(
                        hospital_id=hospital.id,
                        department_id=dept.id,
                        date=m_date,
                        category="biomedical",
                        subcategory="red_autoclaved",
                        scope="Scope 3",
                        ghg_gas_type="CO2e",
                        quantity=red_qty,
                        unit="kg",
                        emission_factor=get_emission_factor("biomedical", "red"),
                        co2e=calculate_co2e("biomedical", red_qty, "red"),
                    )
                )

                # Scope 1: Diesel for DG Sets in Energy Plant
                if "diesel" in profile:
                    diesel_qty = round(profile["diesel"] * random.uniform(0.85, 1.15), 1)
                    emissions_to_add.append(
                        Emission(
                            hospital_id=hospital.id,
                            department_id=dept.id,
                            date=m_date,
                            category="diesel",
                            subcategory="backup_dg_sets",
                            scope="Scope 1",
                            ghg_gas_type="CO2e",
                            quantity=diesel_qty,
                            unit="L",
                            emission_factor=get_emission_factor("diesel"),
                            co2e=calculate_co2e("diesel", diesel_qty),
                        )
                    )

                # Scope 1: Anesthetic Gases in Operating Theatres
                if profile.get("anesthetic_desflurane", 0) > 0:
                    des_qty = round(profile["anesthetic_desflurane"] * random.uniform(0.85, 1.15), 2)
                    emissions_to_add.append(
                        Emission(
                            hospital_id=hospital.id,
                            department_id=dept.id,
                            date=m_date,
                            category="anesthetic",
                            subcategory="desflurane",
                            scope="Scope 1",
                            ghg_gas_type="Desflurane (GWP 2540)",
                            quantity=des_qty,
                            unit="kg",
                            emission_factor=get_emission_factor("anesthetic", "desflurane"),
                            co2e=calculate_co2e("anesthetic", des_qty, "desflurane"),
                        )
                    )

                if profile.get("anesthetic_sevoflurane", 0) > 0:
                    sevo_qty = round(profile["anesthetic_sevoflurane"] * random.uniform(0.90, 1.10), 2)
                    emissions_to_add.append(
                        Emission(
                            hospital_id=hospital.id,
                            department_id=dept.id,
                            date=m_date,
                            category="anesthetic",
                            subcategory="sevoflurane",
                            scope="Scope 1",
                            ghg_gas_type="Sevoflurane (GWP 130)",
                            quantity=sevo_qty,
                            unit="kg",
                            emission_factor=get_emission_factor("anesthetic", "sevoflurane"),
                            co2e=calculate_co2e("anesthetic", sevo_qty, "sevoflurane"),
                        )
                    )

        db.add_all(emissions_to_add)
        db.commit()

        # 5. Benchmarks
        benchmarks = [
            Benchmark(
                hospital_id=hospital.id,
                peer_group="National Green Hospital Benchmark",
                metric="Energy Performance Index (kWh/bed/year)",
                value=38.2,
                ranking=2,
            ),
            Benchmark(
                hospital_id=hospital.id,
                peer_group="National Green Hospital Benchmark",
                metric="Renewable Solar Energy Adoption (%)",
                value=28.5,
                ranking=1,
            ),
            Benchmark(
                hospital_id=hospital.id,
                peer_group="National Green Hospital Benchmark",
                metric="Biomedical Waste Autoclave Diversion (%)",
                value=82.4,
                ranking=2,
            ),
            Benchmark(
                hospital_id=hospital.id,
                peer_group="National Green Hospital Benchmark",
                metric="Water Intensity (L/bed/day)",
                value=235.0,
                ranking=3,
            ),
        ]
        db.add_all(benchmarks)

        # 6. Compliance Reports
        reports = [
            ComplianceReport(
                hospital_id=hospital.id,
                month=(today.replace(day=1) - timedelta(days=30)).replace(day=1),
                report_type="NABH_GREEN_OT",
                status="Certified",
                compliance_score=92.5,
                notes="NABH Green Operating Theatre standard verified: volatile anesthetic scavenging & LED surgical lighting certified.",
                generated_by="Vikram Seth (ESG Auditor)",
            ),
            ComplianceReport(
                hospital_id=hospital.id,
                month=(today.replace(day=1) - timedelta(days=60)).replace(day=1),
                report_type="CPCB_FORM_IV",
                status="Submitted",
                compliance_score=95.0,
                notes="Central Pollution Control Board Bio-Medical Waste Annual Return Form IV verified with GPS barcoding loggers.",
                generated_by="Anita Roy (Facility Lead)",
            ),
            ComplianceReport(
                hospital_id=hospital.id,
                month=(today.replace(day=1) - timedelta(days=90)).replace(day=1),
                report_type="GHG_CORPORATE_STANDARD",
                status="Audited",
                compliance_score=88.0,
                notes="GHG Protocol Scopes 1, 2, 3 Corporate Carbon Accounting inventory verified.",
                generated_by="Dr. Rajesh Sharma",
            ),
        ]
        db.add_all(reports)

        # 7. Achievements
        achievements = [
            Achievement(
                hospital_id=hospital.id,
                department_id=departments["Operating Theatres"].id,
                title="Green Anesthesia Vanguard (Sevoflurane Transition)",
                badge_code="GREEN_OT_GOLD",
                points=250,
                date_earned=today - timedelta(days=45),
            ),
            Achievement(
                hospital_id=hospital.id,
                department_id=departments["Facilities & Energy Plant"].id,
                title="Solar Microgrid Milestone (150 kWp Commissioned)",
                badge_code="SOLAR_CHAMPION",
                points=300,
                date_earned=today - timedelta(days=90),
            ),
            Achievement(
                hospital_id=hospital.id,
                department_id=departments["General Inpatient Wards"].id,
                title="Zero BMW Segregation Error Rating for 6 Consecutive Months",
                badge_code="BMW_ZERO_ERROR",
                points=200,
                date_earned=today - timedelta(days=120),
            ),
        ]
        db.add_all(achievements)

        # 8. Audit Logs
        audit_logs = [
            AuditLog(
                hospital_id=hospital.id,
                user_id=users_to_seed[0].id,
                action="SYSTEM_INIT",
                entity_type="SYSTEM",
                details="Viridis Production Environment initialized and baseline hospital records provisioned.",
                ip_address="127.0.0.1",
            ),
            AuditLog(
                hospital_id=hospital.id,
                user_id=users_to_seed[3].id,
                action="AUDIT_VERIFICATION",
                entity_type="REPORT",
                details="NABH Green OT and CPCB Form IV manifests verified and signed.",
                ip_address="192.168.1.45",
            ),
        ]
        db.add_all(audit_logs)

        # 9. Simulation Scenario
        sim = SimulationScenario(
            hospital_id=hospital.id,
            name="Net Zero Healthcare Pathway 2026-2030",
            description="Comprehensive decarbonization roadmap including 150 kW solar rooftop, LED luminaires, and Desflurane elimination.",
            solar_capacity_kw=150.0,
            led_retrofit_pct=80.0,
            anesthetic_switch_pct=90.0,
            waste_autoclave_pct=50.0,
            projected_co2e_reduction_kg=215000.0,
            projected_monthly_savings_inr=195000.0,
            estimated_capex_inr=7500000.0,
            payback_years=3.2,
        )
        db.add(sim)

        db.commit()

        print(f"[SUCCESS] Seeded hospital '{hospital.name}' with {len(users_to_seed)} RBAC users, {len(departments)} departments, {len(emissions_to_add)} Scope 1-3 emissions, and compliance files.")
        return {
            "status": "success",
            "hospital": hospital.name,
            "hospital_id": hospital.id,
            "demo_users": [u.email for u in users_to_seed],
            "departments": len(departments),
            "emissions_records": len(emissions_to_add),
            "compliance_reports": len(reports),
            "benchmarks": len(benchmarks),
        }

    finally:
        if close_at_end:
            db.close()


if __name__ == "__main__":
    seed_database()


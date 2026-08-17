import sys
from sqlalchemy import create_engine, text
from app.database import DATABASE_URL, Base, engine
from app import models
from app.seed import seed_database
from sqlalchemy.orm import sessionmaker

def migrate_and_sync():
    print(f"Connecting to database: {DATABASE_URL}...")

    
    # 1. Create any missing tables (audit_logs, simulation_scenarios, etc.)
    Base.metadata.create_all(bind=engine)
    print("Base.metadata.create_all executed.")

    # 2. Add missing columns to existing tables if PostgreSQL
    with engine.connect() as conn:
        # Check users columns
        conn.execute(text("""
            DO $$
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='users' AND column_name='created_at') THEN

                    ALTER TABLE users ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
                END IF;
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='users' AND column_name='department_id') THEN
                    ALTER TABLE users ADD COLUMN department_id INTEGER REFERENCES departments(id);
                END IF;
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='users' AND column_name='phone') THEN
                    ALTER TABLE users ADD COLUMN phone VARCHAR(30);
                END IF;
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='users' AND column_name='full_name') THEN
                    ALTER TABLE users ADD COLUMN full_name VARCHAR(100);
                END IF;
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='users' AND column_name='role') THEN
                    ALTER TABLE users ADD COLUMN role VARCHAR(30) DEFAULT 'hospital_admin';
                END IF;
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='users' AND column_name='is_active') THEN
                    ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT TRUE;
                END IF;


                -- Hospitals columns
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='hospitals' AND column_name='created_at') THEN
                    ALTER TABLE hospitals ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
                END IF;
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='hospitals' AND column_name='occupied_beds_avg') THEN
                    ALTER TABLE hospitals ADD COLUMN occupied_beds_avg DOUBLE PRECISION DEFAULT 200.0;
                END IF;
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='hospitals' AND column_name='total_area_sqft') THEN
                    ALTER TABLE hospitals ADD COLUMN total_area_sqft DOUBLE PRECISION DEFAULT 150000.0;
                END IF;

                -- Departments columns
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='departments' AND column_name='created_at') THEN
                    ALTER TABLE departments ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
                END IF;
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='departments' AND column_name='floor') THEN
                    ALTER TABLE departments ADD COLUMN floor VARCHAR(30);
                END IF;
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='departments' AND column_name='head_of_department') THEN
                    ALTER TABLE departments ADD COLUMN head_of_department VARCHAR(100);
                END IF;

                -- Achievements columns
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='achievements' AND column_name='badge_code') THEN
                    ALTER TABLE achievements ADD COLUMN badge_code VARCHAR(50);
                END IF;
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='achievements' AND column_name='points') THEN
                    ALTER TABLE achievements ADD COLUMN points INTEGER DEFAULT 100;
                END IF;


                -- Emissions columns
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='emissions' AND column_name='scope') THEN
                    ALTER TABLE emissions ADD COLUMN scope VARCHAR(20) DEFAULT 'Scope 2';
                END IF;
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='emissions' AND column_name='ghg_gas_type') THEN
                    ALTER TABLE emissions ADD COLUMN ghg_gas_type VARCHAR(50) DEFAULT 'CO2e';
                END IF;
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='emissions' AND column_name='subcategory') THEN
                    ALTER TABLE emissions ADD COLUMN subcategory VARCHAR(50);
                END IF;
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='emissions' AND column_name='notes') THEN
                    ALTER TABLE emissions ADD COLUMN notes TEXT;
                END IF;
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='emissions' AND column_name='recorded_by_user_id') THEN
                    ALTER TABLE emissions ADD COLUMN recorded_by_user_id INTEGER REFERENCES users(id);
                END IF;


                -- Compliance Reports columns
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='compliance_reports' AND column_name='created_at') THEN
                    ALTER TABLE compliance_reports ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
                END IF;
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='compliance_reports' AND column_name='report_type') THEN
                    ALTER TABLE compliance_reports ADD COLUMN report_type VARCHAR(50) DEFAULT 'NABH_GREEN_OT';
                END IF;
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='compliance_reports' AND column_name='compliance_score') THEN
                    ALTER TABLE compliance_reports ADD COLUMN compliance_score DOUBLE PRECISION DEFAULT 85.0;
                END IF;
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='compliance_reports' AND column_name='generated_by') THEN
                    ALTER TABLE compliance_reports ADD COLUMN generated_by VARCHAR(100);
                END IF;

            END $$;
        """))
        conn.commit()
        print("Schema columns successfully aligned and migrated!")

    # 3. Seed demo accounts & data
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        res = seed_database(db)
        print("Database seeded:", res)
    finally:
        db.close()

if __name__ == "__main__":
    migrate_and_sync()

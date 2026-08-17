<div align="center">

# 🌿 Viridis | Healthcare Decarbonization & ESG Platform

**Intelligent Hospital Sustainability, Clinical Carbon Telemetry & Regulatory Compliance**

[![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![React](https://img.shields.io/badge/React_18-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![Vite](https://img.shields.io/badge/Vite_5-646CFF?style=for-the-badge&logo=vite&logoColor=white)](https://vitejs.dev/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)

</div>

---

## 📖 Executive Overview

**Viridis** is an enterprise-grade hospital sustainability and carbon accounting platform. Designed specifically for healthcare institutions, multi-speciality medical centers, and hospital networks, Viridis automates the tracking, analysis, and reduction of clinical carbon emissions across **Scope 1 (Direct), Scope 2 (Purchased Electricity), and Scope 3 (Biomedical Waste & Supply Chain)**.

Viridis connects real-time departmental utility and waste manifests to an AI-driven analytics core, providing audit-ready ESG reporting, dynamic anomaly alerts, regional peer benchmarking, and gamified clinical engagement.

---

## 🏛️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              VIRIDIS WEB PLATFORM                               │
└─────────────────────────────────────────────────────────────────────────────────┘
                                         │
              ┌──────────────────────────┴──────────────────────────┐
              ▼                                                     ▼
┌───────────────────────────────────────────┐   ┌─────────────────────────────────────────┐
│        Frontend: viridis-green-hub        │   │             Backend API Core            │
│          (React 18 + Vite 5 + TS)         │   │          (FastAPI + Python 3.12)        │
├───────────────────────────────────────────┤   ├─────────────────────────────────────────┤
│ • React Router v6 Navigation              │   │ • Modular APIRouters (/api/v1/*)        │
│ • TanStack React Query Telemetry          │   │ • Flexible CSV Ingestion (Wide & Tall)  │
│ • Recharts Carbon Visualizations          │   │ • Scikit-learn Linear Forecast Engine   │
│ • Tailwind CSS & shadcn/Radix UI          │   │ • Dynamic Anomaly & Spike Detection     │
│ • Downloadable Template Generators        │   │ • Multi-variable Sustainability Scoring │
└───────────────────────────────────────────┘   └─────────────────────────────────────────┘
                      │                                               │
                      │               HTTP REST (JSON)                │
                      └───────────────────────────────────────────────┘
                                              │
                                              ▼
                                ┌───────────────────────────┐
                                │   PostgreSQL Database     │
                                │ (SQLAlchemy 2.0 + Alembic)│
                                └───────────────────────────┘
```

---

## ✨ Key Platform Capabilities

### 📊 1. Real-Time Telemetry Dashboard
- Comprehensive multi-department overview tracking total $\text{kg CO}_2\text{e}$, grid electricity, municipal water consumption, and incinerated/autoclaved waste streams.
- Recharts-powered monthly emission trendline with automated reduction target curves.
- Instant identification of highest emitting clinical units (e.g., Operating Theatres, ICU) and top sustainability performers.

### 📥 2. Flexible Data Ingestion Engine
- **Dual-Schema Compatibility:** Supports both human-friendly wide monthly departmental logs (`Department, Date, Electricity (kWh), Water (L), Biomedical Waste (kg)`) and granular row-by-row spreadsheets.
- **Automated Factor Derivation:** Applies standard emission factors ($\text{kg CO}_2\text{e}$ multipliers) on ingestion.
- Built-in downloadable sample CSV template directly from the UI.

### 🤖 3. AI Predictive Analytics & Anomaly Detection
- **Machine Learning Forecasting:** Scikit-learn Linear Regression model predicting hospital carbon trajectories for future months with calendar labels.
- **Dynamic Anomaly Engine:** Statistical variance monitoring detecting departmental equipment faults (e.g., HVAC continuous cycling in ICU, water pipe leaks in general wards) with estimated rupee and carbon savings.
- **Smart Recommendations:** Actionable ROI-driven clinical efficiency suggestions (e.g., solar autoclave rescheduling, LED retrofits).

### 🌱 4. Multi-Variable Sustainability Scoring
- Computes comprehensive institutional sustainability grades (**$A+$ to $F$**) and numeric indices ($0-100$).
- Weighted scoring combining:
  - **Energy Performance Index (EPI):** $\text{kWh / bed / year}$ (40% weight)
  - **Waste Diversion Rate:** Autoclaved/Recycled vs Incinerated (25% weight)
  - **Renewable Energy Adoption:** Rooftop solar captive mix (20% weight)
  - **Yearly Reduction Trend:** Year-over-year percentage progress (15% weight)

### 🏆 5. Peer Benchmarking & Regional Comparison
- Compares hospital carbon intensity ($\text{kg CO}_2\text{e} / \text{bed}$) against regional peer medians and top green hospital performers.
- Actionable benchmarking cards detailing annual potential cost savings.

### 📑 6. ESG & Regulatory Compliance
- Audit-ready environmental reporting tailored for State Pollution Control Boards, NABH, and ESG disclosures.
- One-click monthly manifest generation and compliance verification status tracking.

### 🎮 7. Gamification & Clinical Engagement
- Departmental green leaderboards celebrating top performing clinical units.
- Milestone badge system recognizing accomplishments (e.g., *Solar Pioneer*, *Zero Bio-Waste Spillage*, *Water Conservation Award*).

---

## 📁 Repository Layout

```
Viridis/
├── backend/
│   ├── alembic/                      # Database schema migrations
│   ├── app/
│   │   ├── routers/                  # Modular FastAPI API routers
│   │   │   ├── ai_insights.py        # ML forecasting & anomaly detection
│   │   │   ├── benchmark.py          # Peer benchmarking & hospital rankings
│   │   │   ├── dashboard.py          # Aggregate telemetry & KPI overviews
│   │   │   ├── emmision.py           # Emission tracking & flexible CSV ingestion
│   │   │   ├── hospital.py           # Hospital & department CRUD
│   │   │   ├── ml_router.py          # Scoring engine & gamification milestones
│   │   │   └── reports.py            # Compliance ledger & audit generation
│   │   ├── business.py               # Sustainability scoring & CO2e algorithms
│   │   ├── crud.py                   # SQLAlchemy database operations
│   │   ├── database.py               # Engine, SessionLocal, and DB fallback
│   │   ├── main.py                   # FastAPI app entry point & CORS configuration
│   │   ├── ml.py                     # Scikit-learn time-series forecasting
│   │   ├── models.py                 # SQLAlchemy ORM models with relationships
│   │   ├── schemas.py                # Pydantic v2 validation & response schemas
│   │   └── seed.py                   # 12-Month realistic demo hospital seeder
│   ├── requirements.txt              # Python package dependencies
│   ├── sample_emissions_granular.csv # Sample standard ingestion template
│   └── .env.example                  # Environment configuration template
│
└── viridis-green-hub/                # React 18 frontend
    ├── public/
    │   └── sample_emissions_template.csv  # Downloadable wide CSV template
    ├── src/
    │   ├── components/               # Core UI & chart components
    │   │   ├── ui/                   # 49 shadcn/Radix UI primitive components
    │   │   ├── CategoryBreakdown.tsx # Recharts pie breakdown
    │   │   ├── EmissionsChart.tsx    # Recharts area/line trend chart
    │   │   ├── Layout.tsx            # App shell with Sidebar & TopBar
    │   │   ├── MetricCard.tsx        # KPI telemetry card
    │   │   └── Sidebar.tsx           # Navigation drawer
    │   ├── lib/
    │   │   └── api.ts                # Unified strongly-typed API client
    │   ├── pages/                    # 14 platform views
    │   │   ├── AIInsights.tsx        # Predictive forecasting & anomaly alerts
    │   │   ├── CarbonCalculator.tsx  # Quick carbon estimator
    │   │   ├── ComplianceReports.tsx # Audit ledger & report generator
    │   │   ├── Dashboard.tsx         # Executive dashboard
    │   │   ├── DataImport.tsx        # CSV spreadsheet ingestion
    │   │   ├── Gamification.tsx      # Leaderboards & badge milestones
    │   │   ├── PeerComparison.tsx    # Regional benchmark rankings
    │   │   └── SustainabilityScorePage.tsx # Live ESG score gauge
    │   ├── App.tsx                   # React Router & Query Provider setup
    │   └── main.tsx                  # Vite DOM mounting
    ├── tailwind.config.ts            # Design tokens & color variables
    ├── tsconfig.json                 # TypeScript compiler configuration
    └── vite.config.ts                # Vite 5 bundle configuration with path aliases
```

---

## 🔌 API Reference Guide

All endpoints are registered under both root `/` and `/api/v1/` prefixes. Interactive Swagger documentation is accessible at `http://localhost:8000/docs`.

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **GET** | `/health` | Health check probe |
| **POST** | `/api/v1/seed` | Re-seeds database with 12-month demo hospital dataset |
| **GET** | `/api/v1/hospitals/{id}` | Get hospital metadata by ID |
| **GET** | `/api/v1/hospitals/{id}/departments` | List all departments belonging to hospital |
| **GET** | `/api/v1/dashboard/overview/{hospital_id}` | Aggregate KPIs, monthly time-series, and department highlights |
| **POST** | `/api/v1/upload-emissions/` | Multipart upload for wide or standard CSV/Excel manifests |
| **GET** | `/api/v1/emissions/` | Query historical emission logs with filters |
| **GET** | `/api/v1/ai-insights/{hospital_id}` | Linear regression forecast, anomalies, and smart recommendations |
| **GET** | `/api/v1/sustainability-score/{hospital_id}` | Multi-variable ESG score, letter grade ($A+$ to $F$), and EPI metrics |
| **GET** | `/api/v1/benchmarks/peer-comparison/{hospital_id}` | Regional peer group ranking and carbon per bed comparisons |
| **GET** | `/api/v1/compliance-reports/` | List regulatory audit manifests |
| **POST** | `/api/v1/compliance-reports/generate/{hospital_id}` | Trigger automated compliance ledger creation |
| **GET** | `/api/v1/achievements/` | Retrieve unlocked sustainability milestone badges |

---

## 🚀 Quickstart & Installation

### Prerequisites
- **Node.js:** v20.x or newer & `npm` 10+
- **Python:** 3.12+
- **Database:** PostgreSQL (or automatic fallback to local SQLite)

---

### 1. Backend Setup

```powershell
# Navigate to backend directory
cd backend

# Create and activate Python virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install required dependencies
pip install -r requirements.txt

# Configure environment variables
Copy-Item .env.example .env

# Run database migrations
alembic upgrade head

# Seed 12 months of realistic hospital demo data
python -m app.seed

# Launch FastAPI development server
uvicorn app.main:app --reload --port 8000
```
> The API will be available at `http://localhost:8000` (Swagger UI at `http://localhost:8000/docs`).

---

### 2. Frontend Setup

```powershell
# Navigate to frontend directory
cd viridis-green-hub

# Install npm packages
npm install

# Start Vite development server
npm run dev
```
> The React dashboard will be live at `http://localhost:5173`.

---

## 🛠️ Verification & Quality Commands

```powershell
# Frontend Type Check
cd viridis-green-hub
npx tsc --noEmit

# Frontend Code Linting
npm run lint

# Production Build
npm run build

# Backend Syntax & Import Compilation
cd ../backend
python -c "import glob, py_compile; [py_compile.compile(f, doraise=True) for f in glob.glob('app/**/*.py', recursive=True)]"
```

---

## 📄 License & Attribution

Viridis is distributed under the MIT License. Developed as a modern healthcare carbon intelligence platform.

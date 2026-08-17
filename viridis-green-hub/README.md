# 🌿 Viridis Green Hub (Frontend)

The modern, responsive React 18 + TypeScript + Vite dashboard for the Viridis Healthcare Sustainability platform.

## Features & Architecture

- **React 18 & Vite 5:** Fast HMR and lightweight bundle optimization.
- **Tailwind CSS & shadcn/Radix UI:** Modern design system with accessible UI primitives and dark/light color tokens.
- **TanStack React Query:** Automated server-state management, cache invalidation, and real-time syncing with FastAPI.
- **Recharts Integration:** High-performance SVG charts for monthly emission trends, category pie distributions, and peer comparisons.
- **Type-Safe API Client:** Centralized fetch-based client in [`src/lib/api.ts`](./src/lib/api.ts) interfacing with `http://localhost:8000/api/v1`.

## Quick Start

```powershell
# Install dependencies
npm install

# Start Vite dev server (defaults to port 5173)
npm run dev

# Run ESLint check
npm run lint

# Build for production
npm run build
```

## Available Pages

- **`/dashboard`**: Live executive KPIs, carbon trends, category shares, and department highlights.
- **`/import`**: Multipart spreadsheet upload supporting wide monthly logs and granular CSVs with a downloadable template.
- **`/insights`**: AI & Scikit-learn emission forecast curves, anomaly alert cards, and ROI savings recommendations.
- **`/score`**: Dynamic multi-variable ESG scoring gauge ($A+$ to $F$), Energy Performance Index (EPI), and waste breakdown.
- **`/comparison`**: Regional peer hospital rankings and carbon intensity benchmarks.
- **`/compliance`**: Regulatory audit manifest tracker with one-click report generation.
- **`/gamification`**: Departmental leaderboards and sustainability milestone badges.
- **`/calculator`**: Instant clinical carbon footprint estimator.
- **`/profile`**: Hospital facility details and account credentials.

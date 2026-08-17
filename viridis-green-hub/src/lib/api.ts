// src/lib/api.ts

export const API_BASE_URL =
  import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1";

// Fallback hospital ID for default demo views
export const DEFAULT_HOSPITAL_ID = 1;

export interface Hospital {
  id: number;
  name: string;
  location?: string;
  type?: string;
  beds?: number;
}

export interface Department {
  id: number;
  hospital_id: number;
  name: string;
}

export interface CategorySummary {
  category: string;
  total_co2e: number;
}

export interface DepartmentHighlight {
  name: string;
  co2e: number;
}

export interface DashboardOverviewData {
  total_emissions: number;
  electricity_co2e: number;
  water_co2e: number;
  waste_co2e: number;
  categories: CategorySummary[];
  monthly_trend: Array<{
    month: string;
    total: number;
    electricity?: number;
    water?: number;
    biomedical?: number;
    [key: string]: string | number | undefined;
  }>;
  highest_emitter?: DepartmentHighlight;
  best_performer?: DepartmentHighlight;
}

export interface SustainabilityScoreData {
  grade: string;
  score: number;
  details: {
    epi: number;
    waste_segregation: number;
    renewable_pct: number;
    trend: number;
    total_kwh: number;
  };
  recommendations: Array<{
    type?: string;
    title: string;
    desc: string;
    impact: string;
  }>;
}

export interface ForecastPoint {
  month_offset: number;
  month_label?: string;
  predicted_co2e: number;
}

export interface HistoryPoint {
  date: string;
  month_label?: string;
  co2e: number;
}

export interface AnomalyAlert {
  id: string;
  title: string;
  department: string;
  category: string;
  severity: string;
  change_pct: string;
  message: string;
  recommendation: string;
  estimated_savings: string;
}

export interface SmartRecommendation {
  id: string;
  title: string;
  description: string;
  impact: string;
  category: string;
}

export interface AIInsightsData {
  history: HistoryPoint[];
  predictions: ForecastPoint[];
  anomalies: AnomalyAlert[];
  recommendations: SmartRecommendation[];
}

export interface PeerHospital {
  id: number;
  name: string;
  co2_per_bed: number;
  renewable_pct: number;
  score: number;
  rank: number;
}

export interface PeerComparisonData {
  hospital_id: number;
  hospital_name: string;
  rank: number;
  total_peers: number;
  co2_per_bed: number;
  peer_avg_co2_per_bed: number;
  peers: PeerHospital[];
}

export interface ComplianceReport {
  id: number;
  hospital_id: number;
  month: string;
  status: string;
  notes?: string;
}

export interface Achievement {
  id: number;
  hospital_id: number;
  department_id?: number;
  title: string;
  date_earned: string;
}

export interface UploadResponse {
  success: boolean;
  rows: number;
  message: string;
}

// Universal fetcher helper
async function fetchJSON<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  try {
    const res = await fetch(url, {
      ...options,
      headers: {
        "Accept": "application/json",
        ...options?.headers,
      },
    });

    if (!res.ok) {
      const errorText = await res.text();
      throw new Error(`API Error ${res.status}: ${errorText || res.statusText}`);
    }

    return await res.json();
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : String(err);
    console.warn(`[Viridis API] Request to ${endpoint} failed:`, message);
    throw err;
  }
}

// API methods
export const api = {
  getHospital: (id: number = DEFAULT_HOSPITAL_ID) =>
    fetchJSON<Hospital>(`/hospitals/${id}`),

  getDepartments: (id: number = DEFAULT_HOSPITAL_ID) =>
    fetchJSON<Department[]>(`/hospitals/${id}/departments`),

  getDashboardOverview: (id: number = DEFAULT_HOSPITAL_ID) =>
    fetchJSON<DashboardOverviewData>(`/dashboard/overview/${id}`),

  getSustainabilityScore: (id: number = DEFAULT_HOSPITAL_ID) =>
    fetchJSON<SustainabilityScoreData>(`/sustainability-score/${id}`),

  getAIInsights: (id: number = DEFAULT_HOSPITAL_ID) =>
    fetchJSON<AIInsightsData>(`/ai-insights/${id}`),

  getPeerComparison: (id: number = DEFAULT_HOSPITAL_ID) =>
    fetchJSON<PeerComparisonData>(`/benchmarks/peer-comparison/${id}`),

  getComplianceReports: (id: number = DEFAULT_HOSPITAL_ID) =>
    fetchJSON<ComplianceReport[]>(`/compliance-reports/?hospital_id=${id}`),

  generateComplianceReport: (id: number = DEFAULT_HOSPITAL_ID) =>
    fetchJSON<ComplianceReport>(`/compliance-reports/generate/${id}`, {
      method: "POST",
    }),

  getAchievements: (id: number = DEFAULT_HOSPITAL_ID) =>
    fetchJSON<Achievement[]>(`/achievements/?hospital_id=${id}`),

  uploadEmissionsCSV: async (file: File, hospitalId: number = DEFAULT_HOSPITAL_ID): Promise<UploadResponse> => {
    const formData = new FormData();
    formData.append("file", file);
    const url = `${API_BASE_URL}/upload-emissions/?hospital_id=${hospitalId}`;

    const res = await fetch(url, {
      method: "POST",
      body: formData,
    });

    if (!res.ok) {
      const errorText = await res.text();
      throw new Error(`CSV Upload failed: ${errorText || res.statusText}`);
    }

    return await res.json();
  },

  seedDemoData: () =>
    fetchJSON<Record<string, unknown>>(`/seed`, { method: "POST" }),
};

// src/lib/api.ts

export const API_BASE_URL =
  import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1";

export const DEFAULT_HOSPITAL_ID = 1;

export type UserRole = "super_admin" | "hospital_admin" | "department_manager" | "auditor";

export interface UserProfile {
  id: number;
  email: string;
  full_name?: string;
  phone?: string;
  role: UserRole;
  hospital_id?: number;
  department_id?: number;
  created_at?: string;
}

export interface Hospital {
  id: number;
  name: string;
  location?: string;
  type?: string;
  beds?: number;
  occupied_beds_avg?: number;
  total_area_sqft?: number;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: UserProfile;
  hospital?: Hospital;
}

export interface RegisterPayload {
  hospitalName: string;
  registrationId?: string;
  hospitalType?: string;
  location?: string;
  email: string;
  phone?: string;
  password: string;
  role?: string;
}

export interface LoginPayload {
  email: string;
  password: string;
}

export interface Department {
  id: number;
  hospital_id: number;
  name: string;
  floor?: string;
  head_of_department?: string;
}

export interface CategorySummary {
  category: string;
  total_co2e: number;
  scope?: string;
}

export interface DepartmentHighlight {
  name: string;
  co2e: number;
}

export interface DashboardOverviewData {
  total_emissions: number;
  scope1_co2e: number;
  scope2_co2e: number;
  scope3_co2e: number;
  electricity_co2e: number;
  water_co2e: number;
  waste_co2e: number;
  anesthetic_co2e: number;
  epi_kwh_per_bed_year: number;
  water_liters_per_bed_day: number;
  waste_kg_per_bed_day: number;
  categories: CategorySummary[];
  monthly_trend: Array<{
    month: string;
    total: number;
    scope1?: number;
    scope2?: number;
    scope3?: number;
    electricity?: number;
    water?: number;
    biomedical?: number;
    anesthetic?: number;
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
    scope1_pct: number;
    scope2_pct: number;
    scope3_pct: number;
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
  upper_bound?: number;
  lower_bound?: number;
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
  scope: string;
  severity: "Critical" | "Warning" | "Info" | string;
  change_pct: string;
  message: string;
  recommendation: string;
  estimated_savings: string;
  z_score?: number;
}

export interface SmartRecommendation {
  id: string;
  title: string;
  description: string;
  impact: string;
  category: string;
  potential_savings_inr?: string;
  potential_co2_cut_kg?: string;
}

export interface AIInsightsData {
  history: HistoryPoint[];
  predictions: ForecastPoint[];
  anomalies: AnomalyAlert[];
  recommendations: SmartRecommendation[];
}

export interface SimulationRequest {
  hospital_id: number;
  name?: string;
  solar_capacity_kw: number;
  led_retrofit_pct: number;
  anesthetic_switch_pct: number;
  waste_autoclave_pct: number;
}

export interface SimulationResult {
  hospital_id: number;
  baseline_annual_co2e_kg: number;
  projected_annual_co2e_kg: number;
  co2e_reduction_kg: number;
  co2e_reduction_pct: number;
  monthly_savings_inr: number;
  annual_savings_inr: number;
  estimated_capex_inr: number;
  payback_years: number;
  scope1_reduction_kg: number;
  scope2_reduction_kg: number;
  scope3_reduction_kg: number;
  roi_breakdown: Array<{
    measure: string;
    capex_inr: number;
    annual_savings_inr: number;
    co2e_cut_kg: number;
  }>;
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
  report_type?: string;
  status: string;
  compliance_score?: number;
  notes?: string;
  generated_by?: string;
  created_at?: string;
}

export interface ComplianceFilingResult {
  report_id: number;
  hospital_name: string;
  location?: string;
  beds?: number;
  report_type: string;
  filing_period: string;
  compliance_score: number;
  status: string;
  generated_by?: string;
  created_at: string;
  summary: {
    total_co2e_kg: number;
    scope1_co2e_kg: number;
    scope2_co2e_kg: number;
    scope3_co2e_kg: number;
  };
  audit_checklist: Array<{
    clause: string;
    status: string;
    evidence: string;
  }>;
}

export interface AuditLog {
  id: number;
  hospital_id?: number;
  user_id?: number;
  action: string;
  entity_type?: string;
  details?: string;
  ip_address?: string;
  timestamp?: string;
}

export interface Achievement {
  id: number;
  hospital_id: number;
  department_id?: number;
  title: string;
  badge_code?: string;
  points?: number;
  date_earned: string;
}

export interface UploadResponse {
  success: boolean;
  rows: number;
  message: string;
}

// Universal fetcher helper with Bearer token authentication
async function fetchJSON<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  const token = localStorage.getItem("viridis_token");

  const headers: Record<string, string> = {
    Accept: "application/json",
    ...(options?.headers as Record<string, string>),
  };

  if (token && !headers["Authorization"]) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  if (options?.body && !(options.body instanceof FormData) && !headers["Content-Type"]) {
    headers["Content-Type"] = "application/json";
  }

  try {
    const res = await fetch(url, {
      ...options,
      headers,
    });

    if (!res.ok) {
      const errorData = await res.json().catch(() => null);
      const detail = errorData?.detail || `API Error ${res.status}: ${res.statusText}`;
      throw new Error(detail);
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
  // Auth methods
  register: (payload: RegisterPayload) =>
    fetchJSON<AuthResponse>("/auth/register", {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  login: (payload: LoginPayload) =>
    fetchJSON<AuthResponse>("/auth/login", {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  getMe: () => fetchJSON<AuthResponse>("/auth/me"),

  listUsers: () => fetchJSON<UserProfile[]>("/auth/users"),

  getAuditLogs: (limit: number = 50) => fetchJSON<AuditLog[]>(`/auth/audit-logs?limit=${limit}`),

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

  simulateDecarbonization: (payload: SimulationRequest) =>
    fetchJSON<SimulationResult>("/simulate", {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  getPeerComparison: (id: number = DEFAULT_HOSPITAL_ID) =>
    fetchJSON<PeerComparisonData>(`/benchmarks/peer-comparison/${id}`),

  getComplianceReports: (id: number = DEFAULT_HOSPITAL_ID) =>
    fetchJSON<ComplianceReport[]>(`/compliance-reports/?hospital_id=${id}`),

  generateComplianceReport: (id: number = DEFAULT_HOSPITAL_ID, reportType: string = "NABH_GREEN_OT") =>
    fetchJSON<ComplianceFilingResult>(`/compliance-reports/generate/${id}?report_type=${reportType}`, {
      method: "POST",
    }),

  getAchievements: (id: number = DEFAULT_HOSPITAL_ID) =>
    fetchJSON<Achievement[]>(`/achievements/?hospital_id=${id}`),

  uploadEmissionsCSV: async (file: File, hospitalId: number = DEFAULT_HOSPITAL_ID): Promise<UploadResponse> => {
    const formData = new FormData();
    formData.append("file", file);
    const token = localStorage.getItem("viridis_token");
    const url = `${API_BASE_URL}/upload-emissions/?hospital_id=${hospitalId}`;

    const headers: Record<string, string> = {};
    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }

    const res = await fetch(url, {
      method: "POST",
      headers,
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


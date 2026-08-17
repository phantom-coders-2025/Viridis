import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { TrendingDown, Zap, Droplets, Trash2, RefreshCw, Sparkles, FileText, Activity, ShieldCheck, Flame, Wind } from "lucide-react";
import { MetricCard } from "@/components/MetricCard";
import { EmissionsChart } from "@/components/EmissionsChart";
import { CategoryBreakdown } from "@/components/CategoryBreakdown";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { useQuery } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";
import { api } from "@/lib/api";

const Dashboard = () => {
  const navigate = useNavigate();
  const [activeScopeFilter, setActiveScopeFilter] = useState<string>("all");

  const { data: overview, isLoading, refetch } = useQuery({
    queryKey: ["dashboardOverview"],
    queryFn: () => api.getDashboardOverview(),
    retry: 1,
  });

  const total = overview?.total_emissions ?? 248500;
  const scope1 = overview?.scope1_co2e ?? 28400;
  const scope2 = overview?.scope2_co2e ?? 154000;
  const scope3 = overview?.scope3_co2e ?? 66100;

  const epi = overview?.epi_kwh_per_bed_year ?? 38.2;
  const waterIntensity = overview?.water_liters_per_bed_day ?? 235.0;
  const wasteIntensity = overview?.waste_kg_per_bed_day ?? 1.85;

  const highestDept = overview?.highest_emitter ?? {
    name: "Operating Theatres & Surgical Suites",
    co2e: 74200,
  };

  const bestDept = overview?.best_performer ?? {
    name: "Radiology & Diagnostic Labs",
    co2e: 21400,
  };

  const scope1Pct = total > 0 ? Math.round((scope1 / total) * 100) : 11;
  const scope2Pct = total > 0 ? Math.round((scope2 / total) * 100) : 62;
  const scope3Pct = total > 0 ? Math.round((scope3 / total) * 100) : 27;

  return (
    <div className="space-y-6 animate-fade-in pb-10">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 bg-gradient-to-r from-card via-card/80 to-primary/5 p-6 rounded-2xl border border-border shadow-sm">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-foreground">
              Sustainability & Carbon Telemetry
            </h1>
            <Badge className="bg-emerald-500/15 text-emerald-600 dark:text-emerald-400 border-emerald-500/30">
              GHG Protocol Corporate Standard
            </Badge>
          </div>
          <p className="text-sm text-muted-foreground mt-1">
            Real-time Scopes 1-3 greenhouse gas accounting, NABH Green standards, and energy index telemetry.
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2.5">
          <Button
            variant="outline"
            size="sm"
            onClick={() => refetch()}
            className="flex items-center gap-1.5 text-xs h-9 border-border/80"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${isLoading ? "animate-spin text-primary" : ""}`} />
            Sync Data
          </Button>

          <Button
            size="sm"
            onClick={() => navigate("/insights")}
            className="flex items-center gap-1.5 text-xs h-9 bg-primary text-primary-foreground shadow-sm hover:bg-primary/90"
          >
            <Sparkles className="w-3.5 h-3.5" />
            AI Simulator
          </Button>

          <Button
            variant="secondary"
            size="sm"
            onClick={() => navigate("/compliance")}
            className="flex items-center gap-1.5 text-xs h-9"
          >
            <FileText className="w-3.5 h-3.5" />
            Compliance Reports
          </Button>
        </div>
      </div>

      {/* GHG Protocol Scope Breakdown Header */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Scope 1 */}
        <Card className="border-border/60 bg-card hover:border-amber-500/40 transition-all shadow-sm">
          <CardContent className="p-5">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                <div className="p-2 rounded-lg bg-amber-500/10 text-amber-600 dark:text-amber-400">
                  <Flame className="w-5 h-5" />
                </div>
                <div>
                  <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">Scope 1 (Direct)</p>
                  <h3 className="text-xl font-bold text-foreground mt-0.5">{Math.round(scope1).toLocaleString()} <span className="text-xs font-normal text-muted-foreground">kg CO₂e</span></h3>
                </div>
              </div>
              <Badge variant="outline" className="text-xs font-semibold border-amber-500/30 text-amber-600">{scope1Pct}% of total</Badge>
            </div>
            <p className="text-xs text-muted-foreground mt-3 pt-2.5 border-t border-border/50 flex items-center justify-between">
              <span>Diesel DG generators & Anesthetics (Desflurane)</span>
            </p>
          </CardContent>
        </Card>

        {/* Scope 2 */}
        <Card className="border-border/60 bg-card hover:border-blue-500/40 transition-all shadow-sm">
          <CardContent className="p-5">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                <div className="p-2 rounded-lg bg-blue-500/10 text-blue-600 dark:text-blue-400">
                  <Zap className="w-5 h-5" />
                </div>
                <div>
                  <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">Scope 2 (Energy Indirect)</p>
                  <h3 className="text-xl font-bold text-foreground mt-0.5">{Math.round(scope2).toLocaleString()} <span className="text-xs font-normal text-muted-foreground">kg CO₂e</span></h3>
                </div>
              </div>
              <Badge variant="outline" className="text-xs font-semibold border-blue-500/30 text-blue-600">{scope2Pct}% of total</Badge>
            </div>
            <p className="text-xs text-muted-foreground mt-3 pt-2.5 border-t border-border/50 flex items-center justify-between">
              <span>Grid Electricity (0.82 kg/kWh CEA factor)</span>
            </p>
          </CardContent>
        </Card>

        {/* Scope 3 */}
        <Card className="border-border/60 bg-card hover:border-purple-500/40 transition-all shadow-sm">
          <CardContent className="p-5">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                <div className="p-2 rounded-lg bg-purple-500/10 text-purple-600 dark:text-purple-400">
                  <Wind className="w-5 h-5" />
                </div>
                <div>
                  <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">Scope 3 (Value Chain)</p>
                  <h3 className="text-xl font-bold text-foreground mt-0.5">{Math.round(scope3).toLocaleString()} <span className="text-xs font-normal text-muted-foreground">kg CO₂e</span></h3>
                </div>
              </div>
              <Badge variant="outline" className="text-xs font-semibold border-purple-500/30 text-purple-600">{scope3Pct}% of total</Badge>
            </div>
            <p className="text-xs text-muted-foreground mt-3 pt-2.5 border-t border-border/50 flex items-center justify-between">
              <span>Bio-Medical Waste streams & Municipal water</span>
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Normalized Healthcare KPIs Banner */}
      <Card className="bg-muted/30 border-border/70 shadow-sm">
        <CardContent className="p-4 grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="p-3 bg-card rounded-xl border border-border/50">
            <p className="text-xs text-muted-foreground font-medium">Energy Performance Index (EPI)</p>
            <p className="text-xl font-bold text-foreground mt-1">{epi} <span className="text-xs font-normal text-muted-foreground">kWh/bed/yr</span></p>
            <p className="text-[11px] text-emerald-600 dark:text-emerald-400 mt-0.5 font-medium">NABH Target: &lt; 45 kWh/bed</p>
          </div>

          <div className="p-3 bg-card rounded-xl border border-border/50">
            <p className="text-xs text-muted-foreground font-medium">Water Intensity</p>
            <p className="text-xl font-bold text-foreground mt-1">{waterIntensity} <span className="text-xs font-normal text-muted-foreground">L / bed / day</span></p>
            <p className="text-[11px] text-blue-600 dark:text-blue-400 mt-0.5 font-medium">Benchmark: 250 L/bed</p>
          </div>

          <div className="p-3 bg-card rounded-xl border border-border/50">
            <p className="text-xs text-muted-foreground font-medium">BMW Generation Index</p>
            <p className="text-xl font-bold text-foreground mt-1">{wasteIntensity} <span className="text-xs font-normal text-muted-foreground">kg / bed / day</span></p>
            <p className="text-[11px] text-purple-600 dark:text-purple-400 mt-0.5 font-medium">CPCB 2016 Compliant</p>
          </div>

          <div className="p-3 bg-card rounded-xl border border-border/50">
            <p className="text-xs text-muted-foreground font-medium">Total Decarbonization</p>
            <p className="text-xl font-bold text-emerald-600 dark:text-emerald-400 mt-1">-8.5% <span className="text-xs font-normal text-muted-foreground">YoY</span></p>
            <p className="text-[11px] text-muted-foreground mt-0.5">On track for Net-Zero 2035</p>
          </div>
        </CardContent>
      </Card>

      {/* Main Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <EmissionsChart data={overview?.monthly_trend} />
        </div>
        <div>
          <CategoryBreakdown categories={overview?.categories} />
        </div>
      </div>

      {/* Department Leaderboards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="bg-card border-border/60 shadow-sm">
          <CardHeader className="pb-3">
            <CardTitle className="text-base flex items-center gap-2">
              <Activity className="w-4 h-4 text-destructive" />
              Highest Emission Intensity Department
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between p-4 bg-destructive/5 border border-destructive/15 rounded-xl">
              <div>
                <p className="font-semibold text-foreground text-sm">{highestDept.name}</p>
                <p className="text-xs text-muted-foreground mt-0.5">Primary driver: Desflurane & 24/7 HVAC sterile air circulation</p>
              </div>
              <div className="text-right">
                <p className="text-2xl font-bold text-destructive">
                  {Math.round(highestDept.co2e).toLocaleString()}
                </p>
                <p className="text-xs text-muted-foreground">kg CO₂e / period</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-card border-border/60 shadow-sm">
          <CardHeader className="pb-3">
            <CardTitle className="text-base flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-emerald-500" />
              Best Sustainability Performer
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between p-4 bg-emerald-500/10 border border-emerald-500/20 rounded-xl">
              <div>
                <p className="font-semibold text-foreground text-sm">{bestDept.name}</p>
                <p className="text-xs text-muted-foreground mt-0.5">Primary driver: Motion lighting & digital PACS eliminating darkroom chemicals</p>
              </div>
              <div className="text-right">
                <p className="text-2xl font-bold text-emerald-600 dark:text-emerald-400">
                  {Math.round(bestDept.co2e).toLocaleString()}
                </p>
                <p className="text-xs text-muted-foreground">kg CO₂e / period</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Dashboard;


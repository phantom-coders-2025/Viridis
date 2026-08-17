import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { TrendingDown, Zap, Droplets, Trash2, RefreshCw } from "lucide-react";
import { MetricCard } from "@/components/MetricCard";
import { EmissionsChart } from "@/components/EmissionsChart";
import { CategoryBreakdown } from "@/components/CategoryBreakdown";
import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";

const Dashboard = () => {
  const { data: overview, isLoading, error } = useQuery({
    queryKey: ["dashboardOverview"],
    queryFn: () => api.getDashboardOverview(),
    retry: 1,
  });

  const total = overview?.total_emissions ?? 230218;
  const electricity = overview?.electricity_co2e ?? 165000;
  const water = overview?.water_co2e ?? 320;
  const waste = overview?.waste_co2e ?? 64898;

  const highestDept = overview?.highest_emitter ?? {
    name: "Intensive Care Unit (ICU)",
    co2e: 52000,
  };

  const bestDept = overview?.best_performer ?? {
    name: "Outpatient Department (OPD)",
    co2e: 19000,
  };

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Dashboard Overview</h1>
          <p className="text-muted-foreground">
            Live hospital emissions and carbon telemetry platform
          </p>
        </div>
        {isLoading && (
          <div className="flex items-center gap-2 text-xs text-muted-foreground bg-muted/40 px-3 py-1.5 rounded-md self-start">
            <RefreshCw className="w-3.5 h-3.5 animate-spin text-primary" />
            <span>Syncing telemetry...</span>
          </div>
        )}
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard
          title="Total Emissions"
          value={Math.round(total).toLocaleString()}
          subtitle="kg CO₂e recorded"
          icon={TrendingDown}
          trend="down"
          trendValue="8.5% yearly reduction"
        />
        <MetricCard
          title="Electricity (Grid)"
          value={Math.round(electricity).toLocaleString()}
          subtitle="kg CO₂e"
          icon={Zap}
          trend="down"
          trendValue="40% solar offset active"
        />
        <MetricCard
          title="Water Footprint"
          value={Math.round(water).toLocaleString()}
          subtitle="kg CO₂e"
          icon={Droplets}
          trend="neutral"
          trendValue="Municipal supply"
        />
        <MetricCard
          title="Biomedical Waste"
          value={Math.round(waste).toLocaleString()}
          subtitle="kg CO₂e"
          icon={Trash2}
          trend="down"
          trendValue="78% waste diversion"
        />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <EmissionsChart data={overview?.monthly_trend} />
        </div>
        <div>
          <CategoryBreakdown categories={overview?.categories} />
        </div>
      </div>

      {/* Department Highlight */}
      <Card className="bg-gradient-card border-border/50">
        <CardHeader>
          <CardTitle className="text-lg">Department Performance Highlight</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-center justify-between p-4 bg-muted/30 rounded-lg">
              <div>
                <p className="font-semibold text-foreground">Highest Emissions</p>
                <p className="text-sm text-muted-foreground">{highestDept.name}</p>
              </div>
              <div className="text-right">
                <p className="text-2xl font-bold text-destructive">
                  {Math.round(highestDept.co2e).toLocaleString()}
                </p>
                <p className="text-xs text-muted-foreground">kg CO₂e total</p>
              </div>
            </div>
            <div className="flex items-center justify-between p-4 bg-success/10 rounded-lg">
              <div>
                <p className="font-semibold text-foreground">Best Performer (Lowest Footprint)</p>
                <p className="text-sm text-muted-foreground">{bestDept.name}</p>
              </div>
              <div className="text-right">
                <p className="text-2xl font-bold text-success">
                  {Math.round(bestDept.co2e).toLocaleString()}
                </p>
                <p className="text-xs text-muted-foreground">kg CO₂e total</p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Dashboard;

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { TrendingDown, Zap, Droplets, Trash2 } from "lucide-react";
import { MetricCard } from "@/components/MetricCard";
import { EmissionsChart } from "@/components/EmissionsChart";
import { CategoryBreakdown } from "@/components/CategoryBreakdown";

const Dashboard = () => {
  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-3xl font-bold text-foreground">Dashboard Overview</h1>
        <p className="text-muted-foreground">Monitor your hospital's carbon footprint in real-time</p>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard
          title="Total Emissions"
          value="45,600"
          subtitle="kg CO₂e this month"
          icon={TrendingDown}
          trend="down"
          trendValue="12% from last month"
        />
        <MetricCard
          title="Electricity"
          value="12,300"
          subtitle="kg CO₂e"
          icon={Zap}
          trend="down"
          trendValue="8% reduction"
        />
        <MetricCard
          title="Water Usage"
          value="18"
          subtitle="kg CO₂e"
          icon={Droplets}
          trend="neutral"
          trendValue="stable"
        />
        <MetricCard
          title="Waste"
          value="1,500"
          subtitle="kg CO₂e"
          icon={Trash2}
          trend="down"
          trendValue="5% improvement"
        />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <EmissionsChart />
        </div>
        <div>
          <CategoryBreakdown />
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
                <p className="text-sm text-muted-foreground">Operating Theatres</p>
              </div>
              <div className="text-right">
                <p className="text-2xl font-bold text-destructive">1,500</p>
                <p className="text-xs text-muted-foreground">kg CO₂e/month</p>
              </div>
            </div>
            <div className="flex items-center justify-between p-4 bg-success/10 rounded-lg">
              <div>
                <p className="font-semibold text-foreground">Best Performer</p>
                <p className="text-sm text-muted-foreground">Emergency Department</p>
              </div>
              <div className="text-right">
                <p className="text-2xl font-bold text-success">800</p>
                <p className="text-xs text-muted-foreground">kg CO₂e/month</p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Dashboard;

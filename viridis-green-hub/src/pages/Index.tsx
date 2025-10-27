import { Hero } from "@/components/Hero";
import { MetricCard } from "@/components/MetricCard";
import { DepartmentCard } from "@/components/DepartmentCard";
import { EmissionsChart } from "@/components/EmissionsChart";
import { CategoryBreakdown } from "@/components/CategoryBreakdown";
import { SustainabilityScore } from "@/components/SustainabilityScore";
import { Cloud, Droplets, Trash2, TrendingDown, Upload } from "lucide-react";
import { Button } from "@/components/ui/button";

const Index = () => {
  const departments = [
    { name: "Emergency Department", emissions: 1200, score: 85, rank: 1, target: 100 },
    { name: "Operating Theatres", emissions: 1500, score: 78, rank: 2, target: 100 },
    { name: "Intensive Care", emissions: 1100, score: 72, rank: 3, target: 100 },
    { name: "General Wards", emissions: 800, score: 68, rank: 4, target: 100 },
  ];

  return (
    <div className="min-h-screen bg-background">
      {/* Hero Section */}
      <Hero />

      {/* Main Dashboard */}
      <div className="container px-4 py-12 space-y-8">
        {/* Quick Actions */}
        <div className="flex flex-wrap gap-4 items-center justify-between">
          <div>
            <h2 className="text-3xl font-bold text-foreground">Dashboard Overview</h2>
            <p className="text-muted-foreground">Track your hospital's sustainability performance</p>
          </div>
          <Button className="bg-primary hover:bg-primary/90 shadow-md">
            <Upload className="w-4 h-4 mr-2" />
            Upload Data
          </Button>
        </div>

        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <MetricCard
            title="Total Emissions"
            value="4,600"
            subtitle="kg CO₂e this month"
            icon={Cloud}
            trend="down"
            trendValue="12% from last month"
          />
          <MetricCard
            title="Water Usage"
            value="15,200"
            subtitle="liters this month"
            icon={Droplets}
            trend="down"
            trendValue="8% from last month"
          />
          <MetricCard
            title="Waste Generated"
            value="850"
            subtitle="kg this month"
            icon={Trash2}
            trend="down"
            trendValue="5% from last month"
          />
          <MetricCard
            title="Carbon Savings"
            value="520"
            subtitle="kg CO₂e saved"
            icon={TrendingDown}
            trend="neutral"
            trendValue="vs. target"
          />
        </div>

        {/* Charts Row */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2">
            <EmissionsChart />
          </div>
          <div className="space-y-6">
            <SustainabilityScore />
            <CategoryBreakdown />
          </div>
        </div>

        {/* Department Performance */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-2xl font-bold text-foreground">Department Performance</h3>
              <p className="text-muted-foreground">How each department is contributing to sustainability goals</p>
            </div>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {departments.map((dept) => (
              <DepartmentCard key={dept.name} {...dept} />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Index;

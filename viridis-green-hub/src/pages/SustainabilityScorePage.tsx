import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Leaf, TrendingUp, Zap, Recycle, RefreshCw } from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";

const SustainabilityScorePage = () => {
  const { data, isLoading } = useQuery({
    queryKey: ["sustainabilityScore"],
    queryFn: () => api.getSustainabilityScore(),
    retry: 1,
  });

  const score = data?.score ?? 78;
  const grade = data?.grade ?? "B+";
  const details = data?.details ?? {
    epi: 42.5,
    waste_segregation: 0.78,
    renewable_pct: 0.40,
    trend: 8.5,
    total_kwh: 12000,
  };

  const metrics = [
    {
      label: `Energy Performance Index (${details.epi} kWh/bed)`,
      value: Math.min(100, Math.max(0, Math.round(100 - details.epi))),
      icon: Zap,
      color: "text-primary",
    },
    {
      label: `Waste Segregation Rate (${Math.round(details.waste_segregation * 100)}%)`,
      value: Math.round(details.waste_segregation * 100),
      icon: Recycle,
      color: "text-success",
    },
    {
      label: `Renewable Energy Mix (${Math.round(details.renewable_pct * 100)}%)`,
      value: Math.round(details.renewable_pct * 100),
      icon: Leaf,
      color: "text-warning",
    },
    {
      label: `Yearly Emission Trend (${details.trend > 0 ? `+${details.trend}% reduction` : `${details.trend}%`})`,
      value: Math.min(100, Math.max(0, Math.round(50 + details.trend * 2.5))),
      icon: TrendingUp,
      color: "text-primary",
    },
  ];

  const recommendations = data?.recommendations ?? [
    {
      title: "Increase Renewable Energy Mix",
      desc: "Currently at 40% renewable solar mix. Adding 50kW rooftop arrays can improve the hospital grade to A.",
      impact: "High Impact",
    },
    {
      title: "Maintain Biomedical Waste Standards",
      desc: "Waste segregation is above peer benchmark (78%). Continue monthly manifest audit tracking.",
      impact: "Ongoing",
    },
  ];

  return (
    <div className="max-w-5xl mx-auto space-y-6 animate-fade-in">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Sustainability Score</h1>
          <p className="text-muted-foreground">
            Multi-variable ESG and energy performance index evaluation
          </p>
        </div>
        {isLoading && (
          <div className="flex items-center gap-2 text-xs text-muted-foreground bg-muted/40 px-3 py-1.5 rounded-md self-start">
            <RefreshCw className="w-3.5 h-3.5 animate-spin text-primary" />
            <span>Calculating live grade...</span>
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Score Gauge Card */}
        <Card className="bg-gradient-success border-success/20">
          <CardHeader>
            <CardTitle className="text-xl text-success-foreground">
              Overall ESG Rating
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="flex items-center justify-center">
              <div className="relative">
                <svg className="w-48 h-48 transform -rotate-90">
                  <circle
                    cx="96"
                    cy="96"
                    r="80"
                    stroke="currentColor"
                    strokeWidth="16"
                    fill="transparent"
                    className="text-success-foreground/20"
                  />
                  <circle
                    cx="96"
                    cy="96"
                    r="80"
                    stroke="currentColor"
                    strokeWidth="16"
                    fill="transparent"
                    strokeDasharray={`${2 * Math.PI * 80}`}
                    strokeDashoffset={`${2 * Math.PI * 80 * (1 - score / 100)}`}
                    className="text-success-foreground transition-all duration-1000"
                    strokeLinecap="round"
                  />
                </svg>
                <div className="absolute inset-0 flex flex-col items-center justify-center">
                  <span className="text-6xl font-bold text-success-foreground">
                    {grade}
                  </span>
                  <span className="text-xl text-success-foreground/80">
                    {score}/100
                  </span>
                </div>
              </div>
            </div>

            <div className="text-center space-y-2">
              <p className="text-success-foreground font-semibold text-lg">
                Performance Rating: Grade {grade} 🌱
              </p>
              <p className="text-sm text-success-foreground/70">
                EPI: {details.epi} kWh/bed/yr • Renewables: {Math.round(details.renewable_pct * 100)}%
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Metrics Breakdown */}
        <Card className="bg-gradient-card border-border/50">
          <CardHeader>
            <CardTitle className="text-xl">Performance Breakdown</CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            {metrics.map((metric) => (
              <div key={metric.label} className="space-y-2">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <metric.icon className={`w-5 h-5 ${metric.color}`} />
                    <span className="font-medium text-foreground text-sm">
                      {metric.label}
                    </span>
                  </div>
                  <span className="text-sm font-semibold text-muted-foreground">
                    {metric.value}%
                  </span>
                </div>
                <Progress value={metric.value} className="h-2" />
              </div>
            ))}
          </CardContent>
        </Card>
      </div>

      {/* Recommendations */}
      <Card className="bg-gradient-card border-border/50">
        <CardHeader>
          <CardTitle className="text-xl">Targeted Recommendations</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {recommendations.map((rec, i) => (
              <div
                key={i}
                className="p-4 bg-primary/5 border border-primary/20 rounded-lg flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2"
              >
                <div>
                  <p className="font-medium text-foreground">{rec.title}</p>
                  <p className="text-sm text-muted-foreground mt-1">{rec.desc}</p>
                </div>
                <span className="text-xs font-semibold px-2.5 py-1 bg-primary/10 text-primary rounded self-start">
                  {rec.impact}
                </span>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default SustainabilityScorePage;

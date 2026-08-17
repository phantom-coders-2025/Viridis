import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { AlertTriangle, TrendingUp, Lightbulb, Sparkles, RefreshCw } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";

const AIInsights = () => {
  const { data, isLoading } = useQuery({
    queryKey: ["aiInsights"],
    queryFn: () => api.getAIInsights(),
    retry: 1,
  });

  // Prepare combined timeline for Recharts (History + Future Forecast)
  const history = data?.history ?? [];
  const predictions = data?.predictions ?? [];

  const chartData = [
    ...history.slice(-6).map((h) => ({
      month: h.month_label || h.date,
      actual: h.co2e,
      forecast: null,
    })),
    ...predictions.slice(0, 4).map((p) => ({
      month: p.month_label || `+${p.month_offset}m`,
      actual: null,
      forecast: p.predicted_co2e,
    })),
  ];

  const anomalies = data?.anomalies ?? [
    {
      id: "icu-energy",
      title: "Energy Spike Detected",
      department: "Intensive Care Unit (ICU)",
      severity: "Critical",
      message: "Elevated HVAC compressor cycling observed during recent weeks.",
      recommendation: "Check thermal zoning and chiller temperature differentials. Potential savings: ₹24,000/mo.",
      estimated_savings: "₹24,000 / mo",
    },
    {
      id: "ward-water",
      title: "Water Usage Anomaly",
      department: "General Inpatient Wards",
      severity: "Warning",
      message: "Water consumption has deviated +25% above baseline.",
      recommendation: "Plumbing leak or stuck flush valves suspected. Schedule maintenance inspection.",
      estimated_savings: "1,200 L / day",
    },
  ];

  const recommendations = data?.recommendations ?? [
    {
      id: "ot-schedule",
      title: "Optimize Operating Theatre Schedule",
      description: "Consolidating surgical blocks during peak solar generation reduces grid demand by 420 kg CO₂e/month.",
      impact: "High Impact",
    },
    {
      id: "led-retrofit",
      title: "LED Lighting & Motion Sensor Retrofit",
      description: "Upgrading hallway and parking garage luminaires can save ₹1,80,000 annually.",
      impact: "Quick Win",
    },
    {
      id: "waste-training",
      title: "Biomedical Segregation Refresher",
      description: "Diverting non-chlorinated plastic from incineration yields an estimated 18% waste score boost.",
      impact: "Medium Impact",
    },
  ];

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-foreground flex items-center gap-2">
            <Sparkles className="w-8 h-8 text-primary" />
            AI-Powered Insights
          </h1>
          <p className="text-muted-foreground">
            Predictive machine-learning analytics, anomaly alerts, and savings recommendations
          </p>
        </div>
        {isLoading && (
          <div className="flex items-center gap-2 text-xs text-muted-foreground bg-muted/40 px-3 py-1.5 rounded-md self-start">
            <RefreshCw className="w-3.5 h-3.5 animate-spin text-primary" />
            <span>Computing ML forecast...</span>
          </div>
        )}
      </div>

      {/* Forecast Chart */}
      <Card className="bg-gradient-card border-border/50 shadow-glow">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-primary" />
            Linear Regression Emissions Forecast (Next 4 Months)
          </CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
              <XAxis
                dataKey="month"
                stroke="hsl(var(--muted-foreground))"
                style={{ fontSize: "0.75rem" }}
              />
              <YAxis
                stroke="hsl(var(--muted-foreground))"
                style={{ fontSize: "0.75rem" }}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: "hsl(var(--card))",
                  border: "1px solid hsl(var(--border))",
                  borderRadius: "var(--radius)",
                }}
              />
              <Line
                type="monotone"
                dataKey="actual"
                name="Actual (kg CO₂e)"
                stroke="hsl(var(--primary))"
                strokeWidth={3}
                dot={{ fill: "hsl(var(--primary))" }}
              />
              <Line
                type="monotone"
                dataKey="forecast"
                name="ML Forecast"
                stroke="hsl(var(--success))"
                strokeWidth={3}
                strokeDasharray="5 5"
                dot={{ fill: "hsl(var(--success))" }}
              />
            </LineChart>
          </ResponsiveContainer>
          <div className="flex items-center justify-center gap-6 mt-4 text-xs">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-primary" />
              <span className="text-muted-foreground">Historical Actuals</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-success" />
              <span className="text-muted-foreground">ML Trend Forecast</span>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Dynamic Alert Cards */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {anomalies.map((alert) => (
          <Card
            key={alert.id}
            className={
              alert.severity === "Critical"
                ? "bg-destructive/5 border-destructive/20"
                : "bg-warning/5 border-warning/20"
            }
          >
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="flex items-center gap-2 text-lg">
                  <AlertTriangle
                    className={
                      alert.severity === "Critical"
                        ? "w-5 h-5 text-destructive"
                        : "w-5 h-5 text-warning"
                    }
                  />
                  {alert.title}
                </CardTitle>
                <Badge
                  variant={alert.severity === "Critical" ? "destructive" : "secondary"}
                >
                  {alert.department}
                </Badge>
              </div>
            </CardHeader>
            <CardContent className="space-y-3">
              <p className="text-sm text-foreground">{alert.message}</p>
              <div className="p-3 bg-muted/50 rounded-lg">
                <p className="text-xs font-medium text-foreground mb-1">
                  AI Actionable Recommendation:
                </p>
                <p className="text-xs text-muted-foreground">{alert.recommendation}</p>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Smart Recommendations */}
      <Card className="bg-gradient-card border-border/50">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Lightbulb className="w-5 h-5 text-primary" />
            Smart Recommendations
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {recommendations.map((rec) => (
              <div
                key={rec.id}
                className="flex items-start gap-3 p-4 bg-primary/5 border border-primary/20 rounded-lg"
              >
                <div className="w-2 h-2 rounded-full bg-primary mt-2" />
                <div className="flex-1">
                  <p className="font-medium text-foreground">{rec.title}</p>
                  <p className="text-sm text-muted-foreground mt-1">
                    {rec.description}
                  </p>
                  <Badge className="mt-2 bg-success/20 text-success-foreground">
                    {rec.impact}
                  </Badge>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default AIInsights;

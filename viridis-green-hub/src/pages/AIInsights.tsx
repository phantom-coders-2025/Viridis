import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { AlertTriangle, TrendingUp, Lightbulb, Sparkles } from "lucide-react";
import { Badge } from "@/components/ui/badge";

const forecastData = [
  { month: "Jan", actual: 4200, forecast: null },
  { month: "Feb", actual: 3900, forecast: null },
  { month: "Mar", actual: 4100, forecast: null },
  { month: "Apr", actual: 3800, forecast: null },
  { month: "May", actual: 3600, forecast: null },
  { month: "Jun", actual: 3400, forecast: null },
  { month: "Jul", actual: null, forecast: 3300 },
  { month: "Aug", actual: null, forecast: 3200 },
  { month: "Sep", actual: null, forecast: 3100 },
];

const AIInsights = () => {
  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-3xl font-bold text-foreground flex items-center gap-2">
          <Sparkles className="w-8 h-8 text-primary" />
          AI-Powered Insights
        </h1>
        <p className="text-muted-foreground">Predictive analytics and intelligent recommendations</p>
      </div>

      {/* Forecast Chart */}
      <Card className="bg-gradient-card border-border/50 shadow-glow">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-primary" />
            Emissions Forecast - Next 3 Months
          </CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={forecastData}>
              <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
              <XAxis 
                dataKey="month" 
                stroke="hsl(var(--muted-foreground))"
                style={{ fontSize: '0.75rem' }}
              />
              <YAxis 
                stroke="hsl(var(--muted-foreground))"
                style={{ fontSize: '0.75rem' }}
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
                stroke="hsl(var(--primary))"
                strokeWidth={3}
                dot={{ fill: "hsl(var(--primary))" }}
              />
              <Line
                type="monotone"
                dataKey="forecast"
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
              <span className="text-muted-foreground">Actual</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-success" />
              <span className="text-muted-foreground">Forecast</span>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Alert Cards */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <Card className="bg-destructive/5 border-destructive/20">
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="flex items-center gap-2 text-lg">
                <AlertTriangle className="w-5 h-5 text-destructive" />
                Energy Spike Detected
              </CardTitle>
              <Badge variant="destructive">Critical</Badge>
            </div>
          </CardHeader>
          <CardContent className="space-y-3">
            <p className="text-sm text-foreground">
              <strong>ICU Department</strong> shows a <strong className="text-destructive">+40% increase</strong> in energy consumption this week.
            </p>
            <div className="p-3 bg-muted/50 rounded-lg">
              <p className="text-xs font-medium text-foreground mb-1">AI Recommendation:</p>
              <p className="text-xs text-muted-foreground">
                Check HVAC system efficiency in ICU. Recent maintenance records show irregular patterns.
                Estimated potential savings: ₹18,000/month
              </p>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-warning/5 border-warning/20">
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="flex items-center gap-2 text-lg">
                <AlertTriangle className="w-5 h-5 text-warning" />
                Water Usage Anomaly
              </CardTitle>
              <Badge className="bg-warning text-warning-foreground">Warning</Badge>
            </div>
          </CardHeader>
          <CardContent className="space-y-3">
            <p className="text-sm text-foreground">
              <strong>General Wards</strong> water usage increased by <strong className="text-warning">+25%</strong> compared to baseline.
            </p>
            <div className="p-3 bg-muted/50 rounded-lg">
              <p className="text-xs font-medium text-foreground mb-1">AI Recommendation:</p>
              <p className="text-xs text-muted-foreground">
                Possible leak detected in Wing B plumbing system. Schedule immediate inspection to prevent waste.
              </p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* AI Suggestions */}
      <Card className="bg-gradient-card border-border/50">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Lightbulb className="w-5 h-5 text-primary" />
            Smart Recommendations
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            <div className="flex items-start gap-3 p-4 bg-primary/5 border border-primary/20 rounded-lg">
              <div className="w-2 h-2 rounded-full bg-primary mt-2" />
              <div className="flex-1">
                <p className="font-medium text-foreground">Optimize Operating Theatre Schedule</p>
                <p className="text-sm text-muted-foreground mt-1">
                  Consolidating OT schedules during peak renewable energy hours could reduce emissions by 320 kg CO₂e/month
                </p>
                <Badge className="mt-2 bg-success/20 text-success-foreground">High Impact</Badge>
              </div>
            </div>

            <div className="flex items-start gap-3 p-4 bg-primary/5 border border-primary/20 rounded-lg">
              <div className="w-2 h-2 rounded-full bg-primary mt-2" />
              <div className="flex-1">
                <p className="font-medium text-foreground">LED Lighting Upgrade</p>
                <p className="text-sm text-muted-foreground mt-1">
                  Replacing fluorescent lights in parking areas with LED could save ₹2,40,000 annually and reduce 2,400 kg CO₂e
                </p>
                <Badge className="mt-2 bg-success/20 text-success-foreground">Quick Win</Badge>
              </div>
            </div>

            <div className="flex items-start gap-3 p-4 bg-primary/5 border border-primary/20 rounded-lg">
              <div className="w-2 h-2 rounded-full bg-primary mt-2" />
              <div className="flex-1">
                <p className="font-medium text-foreground">Waste Segregation Training</p>
                <p className="text-sm text-muted-foreground mt-1">
                  AI analysis shows 15% improvement potential in waste segregation. Staff training program recommended.
                </p>
                <Badge className="mt-2 bg-primary/20 text-primary-foreground">Medium Impact</Badge>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default AIInsights;

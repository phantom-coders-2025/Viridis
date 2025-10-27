import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Leaf, TrendingUp, Zap, Recycle } from "lucide-react";

const SustainabilityScorePage = () => {
  const score = 68;
  const grade = "B";

  const metrics = [
    { label: "Energy Efficiency", value: 75, icon: Zap, color: "text-primary" },
    { label: "Waste Segregation", value: 82, icon: Recycle, color: "text-success" },
    { label: "Renewable Energy", value: 45, icon: Leaf, color: "text-warning" },
    { label: "Improvement Trend", value: 68, icon: TrendingUp, color: "text-primary" },
  ];

  return (
    <div className="max-w-5xl mx-auto space-y-6 animate-fade-in">
      <div>
        <h1 className="text-3xl font-bold text-foreground">Sustainability Score</h1>
        <p className="text-muted-foreground">Track your progress toward green excellence</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Score Card */}
        <Card className="bg-gradient-success border-success/20">
          <CardHeader>
            <CardTitle className="text-xl text-success-foreground">
              Overall Score
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
                  <span className="text-7xl font-bold text-success-foreground">
                    {grade}
                  </span>
                  <span className="text-2xl text-success-foreground/80">
                    {score}%
                  </span>
                </div>
              </div>
            </div>

            <div className="text-center space-y-2">
              <p className="text-success-foreground font-semibold text-lg">
                You're {score}% toward Green Excellence 🌱
              </p>
              <p className="text-sm text-success-foreground/70">
                Keep up the great work! You're making a real impact.
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
                    <span className="font-medium text-foreground">{metric.label}</span>
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
          <CardTitle className="text-xl">Recommendations for Improvement</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            <div className="p-4 bg-primary/5 border border-primary/20 rounded-lg">
              <p className="font-medium text-foreground">🌟 Quick Win</p>
              <p className="text-sm text-muted-foreground mt-1">
                Increase renewable energy usage by installing solar panels on rooftop areas. 
                Potential CO₂ reduction: 8,000 kg/year
              </p>
            </div>
            <div className="p-4 bg-success/5 border border-success/20 rounded-lg">
              <p className="font-medium text-foreground">♻️ Waste Management</p>
              <p className="text-sm text-muted-foreground mt-1">
                Your waste segregation is excellent! Maintain this performance to stay ahead.
              </p>
            </div>
            <div className="p-4 bg-warning/5 border border-warning/20 rounded-lg">
              <p className="font-medium text-foreground">⚡ Energy Efficiency</p>
              <p className="text-sm text-muted-foreground mt-1">
                Consider upgrading to LED lighting in common areas. 
                Estimated savings: ₹45,000/year and 4,500 kg CO₂e
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default SustainabilityScorePage;

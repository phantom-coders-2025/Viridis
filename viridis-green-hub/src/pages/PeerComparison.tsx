import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { TrendingUp, Award, Users } from "lucide-react";
import { Badge } from "@/components/ui/badge";

const comparisonData = [
  { hospital: "Your Hospital", value: 52.3, color: "hsl(var(--primary))" },
  { hospital: "Peer Median", value: 45.8, color: "hsl(var(--muted))" },
  { hospital: "Top Performer", value: 38.2, color: "hsl(var(--success))" },
];

const PeerComparison = () => {
  const percentile = 62;
  const savingsPotential = { money: 320000, co2: 32000 };

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-3xl font-bold text-foreground flex items-center gap-2">
          <Users className="w-8 h-8 text-primary" />
          Peer Comparison
        </h1>
        <p className="text-muted-foreground">Benchmark your performance against similar hospitals</p>
      </div>

      {/* Performance Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card className="bg-gradient-card border-border/50">
          <CardHeader>
            <CardTitle className="text-lg">Your Percentile</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-center">
              <p className="text-5xl font-bold text-primary">{percentile}th</p>
              <p className="text-sm text-muted-foreground mt-2">
                Better than {percentile}% of peer hospitals
              </p>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-card border-border/50">
          <CardHeader>
            <CardTitle className="text-lg">CO₂e vs Median</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-center">
              <p className="text-5xl font-bold text-warning">+14%</p>
              <p className="text-sm text-muted-foreground mt-2">
                Above median emissions
              </p>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-card border-border/50">
          <CardHeader>
            <CardTitle className="text-lg">Improvement Potential</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-center">
              <p className="text-5xl font-bold text-success">32K</p>
              <p className="text-sm text-muted-foreground mt-2">
                kg CO₂e reduction possible
              </p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Comparison Chart */}
      <Card className="bg-gradient-card border-border/50">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Award className="w-5 h-5 text-primary" />
            Energy Consumption per Bed (kg CO₂e/bed/month)
          </CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={comparisonData}>
              <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
              <XAxis 
                dataKey="hospital" 
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
              <Bar 
                dataKey="value" 
                fill="hsl(var(--primary))"
                radius={[8, 8, 0, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* Savings Potential */}
      <Card className="bg-gradient-success border-success/20">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-success-foreground">
            <TrendingUp className="w-5 h-5" />
            Savings Potential
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="text-center p-6 bg-success-foreground/10 rounded-lg">
              <p className="text-sm text-success-foreground/80 mb-2">Financial Savings</p>
              <p className="text-4xl font-bold text-success-foreground">
                ₹{savingsPotential.money.toLocaleString()}
              </p>
              <p className="text-xs text-success-foreground/70 mt-1">per year</p>
            </div>
            <div className="text-center p-6 bg-success-foreground/10 rounded-lg">
              <p className="text-sm text-success-foreground/80 mb-2">Carbon Reduction</p>
              <p className="text-4xl font-bold text-success-foreground">
                {savingsPotential.co2.toLocaleString()}
              </p>
              <p className="text-xs text-success-foreground/70 mt-1">kg CO₂e per year</p>
            </div>
          </div>
          <p className="text-center text-success-foreground/80 mt-6">
            By reaching median performance levels, your hospital could achieve these savings
          </p>
        </CardContent>
      </Card>

      {/* Best Practices */}
      <Card className="bg-gradient-card border-border/50">
        <CardHeader>
          <CardTitle>Best Practices from Top Performers</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {[
              {
                title: "Energy Management System",
                description: "Top hospitals use IoT-enabled real-time energy monitoring to reduce consumption by 18%",
                badge: "Technology"
              },
              {
                title: "Staff Engagement Programs",
                description: "Monthly sustainability challenges increase awareness and reduce waste by 22%",
                badge: "Culture"
              },
              {
                title: "Renewable Energy",
                description: "Solar installations covering 40% of energy needs is common among leaders",
                badge: "Infrastructure"
              }
            ].map((practice, i) => (
              <div key={i} className="flex items-start gap-3 p-4 bg-muted/30 rounded-lg">
                <div className="w-2 h-2 rounded-full bg-primary mt-2" />
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <p className="font-medium text-foreground">{practice.title}</p>
                    <Badge variant="secondary" className="text-xs">{practice.badge}</Badge>
                  </div>
                  <p className="text-sm text-muted-foreground">{practice.description}</p>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default PeerComparison;

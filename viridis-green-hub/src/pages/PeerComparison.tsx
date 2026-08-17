import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { TrendingUp, Award, Users, RefreshCw } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";

const PeerComparison = () => {
  const { data, isLoading } = useQuery({
    queryKey: ["peerComparison"],
    queryFn: () => api.getPeerComparison(),
    retry: 1,
  });

  const rank = data?.rank ?? 3;
  const totalPeers = data?.total_peers ?? 5;
  const co2PerBed = data?.co2_per_bed ?? 14.2;
  const peerAvg = data?.peer_avg_co2_per_bed ?? 15.1;

  const comparisonData = data?.peers?.map((p) => ({
    hospital: p.name,
    value: p.co2_per_bed,
    score: p.score,
  })) ?? [
    { hospital: "Apollo Green Care (You)", value: 14.2, score: 82 },
    { hospital: "St. Jude Eco Care", value: 11.8, score: 91 },
    { hospital: "Fortis Green Pavilion", value: 13.1, score: 86 },
    { hospital: "Metro City Health", value: 16.4, score: 74 },
    { hospital: "Sunrise Multi-Speciality", value: 19.8, score: 62 },
  ];

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-foreground flex items-center gap-2">
            <Users className="w-8 h-8 text-primary" />
            Peer Comparison
          </h1>
          <p className="text-muted-foreground">
            Benchmark performance against regional hospitals & peer group averages
          </p>
        </div>
        {isLoading && (
          <div className="flex items-center gap-2 text-xs text-muted-foreground bg-muted/40 px-3 py-1.5 rounded-md self-start">
            <RefreshCw className="w-3.5 h-3.5 animate-spin text-primary" />
            <span>Fetching peer metrics...</span>
          </div>
        )}
      </div>

      {/* Performance Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card className="bg-gradient-card border-border/50">
          <CardHeader>
            <CardTitle className="text-lg">Peer Group Rank</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-center">
              <p className="text-5xl font-bold text-primary">#{rank}</p>
              <p className="text-sm text-muted-foreground mt-2">
                Top {Math.round((rank / totalPeers) * 100)}% of {totalPeers} Tier-1 hospitals
              </p>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-card border-border/50">
          <CardHeader>
            <CardTitle className="text-lg">Carbon Intensity vs Peer Avg</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-center">
              <p className="text-5xl font-bold text-success">-6.0%</p>
              <p className="text-sm text-muted-foreground mt-2">
                {co2PerBed} vs {peerAvg} kg CO₂e/bed avg
              </p>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-card border-border/50">
          <CardHeader>
            <CardTitle className="text-lg">Annual Potential Savings</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-center">
              <p className="text-5xl font-bold text-primary">₹3.2L</p>
              <p className="text-sm text-muted-foreground mt-2">
                via top-performer energy optimization
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
            Carbon Intensity by Hospital (kg CO₂e per Bed)
          </CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={comparisonData}>
              <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
              <XAxis
                dataKey="hospital"
                stroke="hsl(var(--muted-foreground))"
                style={{ fontSize: "0.70rem" }}
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
              <Bar
                dataKey="value"
                name="kg CO₂e / Bed"
                fill="hsl(var(--primary))"
                radius={[8, 8, 0, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* Best Practices */}
      <Card className="bg-gradient-card border-border/50">
        <CardHeader>
          <CardTitle>Regional Best Practices</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {[
              {
                title: "Real-Time Submetering in Operating Theatres",
                description: "IoT submeters on chillers and autoclaves mitigate off-peak vampire loads by 18%.",
                badge: "Technology",
              },
              {
                title: "Biomedical Segregation Colour Bins",
                description: "Department-level colour coded digital manifests improve diversion rates by 22%.",
                badge: "Clinical Process",
              },
              {
                title: "Rooftop Solar Captive Generation",
                description: "40%+ solar power mix cuts daytime grid utility tariff strain.",
                badge: "Infrastructure",
              },
            ].map((practice, i) => (
              <div key={i} className="flex items-start gap-3 p-4 bg-muted/30 rounded-lg">
                <div className="w-2 h-2 rounded-full bg-primary mt-2" />
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <p className="font-medium text-foreground">{practice.title}</p>
                    <Badge variant="secondary" className="text-xs">
                      {practice.badge}
                    </Badge>
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

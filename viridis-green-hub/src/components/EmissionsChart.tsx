import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Area, AreaChart } from "recharts";

interface MonthlyPoint {
  month: string;
  total?: number;
  emissions?: number;
  target?: number;
  [key: string]: string | number | undefined;
}

interface EmissionsChartProps {
  data?: MonthlyPoint[];
}

const defaultData: MonthlyPoint[] = [
  { month: "Jan", emissions: 18200, target: 20000 },
  { month: "Feb", emissions: 19100, target: 19500 },
  { month: "Mar", emissions: 18800, target: 19000 },
  { month: "Apr", emissions: 19400, target: 18500 },
  { month: "May", emissions: 20100, target: 18000 },
  { month: "Jun", emissions: 19600, target: 17500 },
];

export const EmissionsChart = ({ data }: EmissionsChartProps) => {
  const chartData = (data && data.length > 0)
    ? data.map((d) => ({
        month: d.month,
        emissions: d.total ?? d.emissions ?? 0,
        target: d.target ?? Math.round((d.total ?? d.emissions ?? 20000) * 0.92),
      }))
    : defaultData;

  return (
    <Card className="bg-gradient-card border-border/50">
      <CardHeader>
        <CardTitle className="text-xl font-semibold">
          Monthly CO₂e Emissions Trend
        </CardTitle>
        <p className="text-sm text-muted-foreground">
          Hospital-wide carbon footprint over time (kg CO₂e)
        </p>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <AreaChart data={chartData}>
            <defs>
              <linearGradient id="colorEmissions" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="hsl(var(--primary))" stopOpacity={0.3} />
                <stop offset="95%" stopColor="hsl(var(--primary))" stopOpacity={0} />
              </linearGradient>
            </defs>
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
            <Area
              type="monotone"
              dataKey="emissions"
              name="Emissions (kg CO₂e)"
              stroke="hsl(var(--primary))"
              strokeWidth={3}
              fill="url(#colorEmissions)"
            />
            <Line
              type="monotone"
              dataKey="target"
              name="Reduction Target"
              stroke="hsl(var(--success))"
              strokeWidth={2}
              strokeDasharray="5 5"
              dot={false}
            />
          </AreaChart>
        </ResponsiveContainer>
        <div className="flex items-center justify-center gap-6 mt-4 text-xs">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-primary" />
            <span className="text-muted-foreground">Actual Emissions</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-success" />
            <span className="text-muted-foreground">Target (-8%)</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

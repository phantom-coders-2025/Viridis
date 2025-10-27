import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Area, AreaChart } from "recharts";

const data = [
  { month: "Jan", emissions: 4200, target: 4000 },
  { month: "Feb", emissions: 3900, target: 3800 },
  { month: "Mar", emissions: 4100, target: 3700 },
  { month: "Apr", emissions: 3800, target: 3600 },
  { month: "May", emissions: 3600, target: 3500 },
  { month: "Jun", emissions: 3400, target: 3400 },
];

export const EmissionsChart = () => {
  return (
    <Card className="bg-gradient-card border-border/50">
      <CardHeader>
        <CardTitle className="text-xl font-semibold">
          Monthly CO₂e Emissions Trend
        </CardTitle>
        <p className="text-sm text-muted-foreground">
          Hospital-wide carbon footprint over time
        </p>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <AreaChart data={data}>
            <defs>
              <linearGradient id="colorEmissions" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="hsl(var(--primary))" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="hsl(var(--primary))" stopOpacity={0}/>
              </linearGradient>
            </defs>
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
            <Area
              type="monotone"
              dataKey="emissions"
              stroke="hsl(var(--primary))"
              strokeWidth={3}
              fill="url(#colorEmissions)"
            />
            <Line
              type="monotone"
              dataKey="target"
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
            <span className="text-muted-foreground">Target</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

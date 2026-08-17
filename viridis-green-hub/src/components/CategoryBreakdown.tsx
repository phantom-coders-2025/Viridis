import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from "recharts";
import { CategorySummary } from "@/lib/api";

interface CategoryBreakdownProps {
  categories?: CategorySummary[];
}

const COLOR_MAP: Record<string, string> = {
  electricity: "hsl(152 65% 35%)",
  water: "hsl(165 60% 45%)",
  biomedical: "hsl(45 90% 60%)",
  diesel: "hsl(38 92% 50%)",
  gas: "hsl(200 80% 50%)",
};

const defaultData = [
  { name: "Electricity", value: 165000, color: "hsl(152 65% 35%)" },
  { name: "Biomedical Waste", value: 65000, color: "hsl(45 90% 60%)" },
  { name: "Water", value: 300, color: "hsl(165 60% 45%)" },
];

export const CategoryBreakdown = ({ categories }: CategoryBreakdownProps) => {
  const chartData = (categories && categories.length > 0)
    ? categories.map((c) => {
        const catKey = c.category.toLowerCase();
        const display = catKey.charAt(0).toUpperCase() + catKey.slice(1);
        return {
          name: display,
          value: Math.round(c.total_co2e),
          color: COLOR_MAP[catKey] || "hsl(var(--primary))",
        };
      })
    : defaultData;

  const total = chartData.reduce((acc, curr) => acc + curr.value, 0);

  return (
    <Card className="bg-gradient-card border-border/50">
      <CardHeader>
        <CardTitle className="text-xl font-semibold">
          Emissions by Category
        </CardTitle>
        <p className="text-sm text-muted-foreground">
          Where your carbon footprint comes from (kg CO₂e)
        </p>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={260}>
          <PieChart>
            <Pie
              data={chartData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
              outerRadius={90}
              dataKey="value"
            >
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip
              contentStyle={{
                backgroundColor: "hsl(var(--card))",
                border: "1px solid hsl(var(--border))",
                borderRadius: "var(--radius)",
              }}
            />
          </PieChart>
        </ResponsiveContainer>
        <div className="grid grid-cols-2 gap-3 mt-4">
          {chartData.map((cat) => {
            const pct = total > 0 ? Math.round((cat.value / total) * 100) : 0;
            return (
              <div key={cat.name} className="flex items-center gap-2">
                <div
                  className="w-3 h-3 rounded-full shrink-0"
                  style={{ backgroundColor: cat.color }}
                />
                <span className="text-xs text-muted-foreground truncate">
                  {cat.name}: {pct}% ({cat.value.toLocaleString()} kg)
                </span>
              </div>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
};

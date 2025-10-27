import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from "recharts";

const data = [
  { name: "Energy", value: 45, color: "hsl(152 65% 35%)" },
  { name: "Water", value: 25, color: "hsl(165 60% 45%)" },
  { name: "Waste", value: 20, color: "hsl(45 90% 60%)" },
  { name: "Transport", value: 10, color: "hsl(38 92% 50%)" },
];

export const CategoryBreakdown = () => {
  return (
    <Card className="bg-gradient-card border-border/50">
      <CardHeader>
        <CardTitle className="text-xl font-semibold">
          Emissions by Category
        </CardTitle>
        <p className="text-sm text-muted-foreground">
          Where your carbon footprint comes from
        </p>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
              outerRadius={100}
              fill="#8884d8"
              dataKey="value"
            >
              {data.map((entry, index) => (
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
          {data.map((category) => (
            <div key={category.name} className="flex items-center gap-2">
              <div 
                className="w-3 h-3 rounded-full" 
                style={{ backgroundColor: category.color }}
              />
              <span className="text-xs text-muted-foreground">
                {category.name}: {category.value}%
              </span>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
};

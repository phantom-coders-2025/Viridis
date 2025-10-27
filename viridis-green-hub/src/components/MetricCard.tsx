import { LucideIcon } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface MetricCardProps {
  title: string;
  value: string;
  subtitle?: string;
  icon: LucideIcon;
  trend?: "up" | "down" | "neutral";
  trendValue?: string;
}

export const MetricCard = ({ 
  title, 
  value, 
  subtitle, 
  icon: Icon, 
  trend = "neutral",
  trendValue 
}: MetricCardProps) => {
  const trendColors = {
    up: "text-destructive",
    down: "text-success",
    neutral: "text-muted-foreground"
  };

  return (
    <Card className="bg-gradient-card border-border/50 hover:shadow-md transition-smooth hover:scale-[1.02]">
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <CardTitle className="text-sm font-medium text-muted-foreground">
          {title}
        </CardTitle>
        <Icon className="w-5 h-5 text-primary" />
      </CardHeader>
      <CardContent>
        <div className="space-y-1">
          <div className="text-3xl font-bold text-foreground">{value}</div>
          {subtitle && (
            <p className="text-xs text-muted-foreground">{subtitle}</p>
          )}
          {trendValue && (
            <p className={`text-xs font-medium ${trendColors[trend]}`}>
              {trend === "down" && "↓ "}
              {trend === "up" && "↑ "}
              {trendValue}
            </p>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

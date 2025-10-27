import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";

interface DepartmentCardProps {
  name: string;
  emissions: number;
  score: number;
  rank: number;
  target: number;
}

export const DepartmentCard = ({ 
  name, 
  emissions, 
  score, 
  rank,
  target 
}: DepartmentCardProps) => {
  const getScoreColor = (score: number) => {
    if (score >= 80) return "bg-success";
    if (score >= 60) return "bg-warning";
    return "bg-destructive";
  };

  const getScoreGrade = (score: number) => {
    if (score >= 90) return "A+";
    if (score >= 80) return "A";
    if (score >= 70) return "B";
    if (score >= 60) return "C";
    return "D";
  };

  return (
    <Card className="bg-gradient-card border-border/50 hover:shadow-lg transition-smooth">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg font-semibold">{name}</CardTitle>
          <Badge variant="secondary" className="text-xs">
            Rank #{rank}
          </Badge>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-2xl font-bold text-foreground">
              {emissions.toLocaleString()}
            </p>
            <p className="text-xs text-muted-foreground">kg CO₂e/month</p>
          </div>
          <div className={`w-16 h-16 rounded-full ${getScoreColor(score)} flex items-center justify-center shadow-glow`}>
            <span className="text-2xl font-bold text-white">
              {getScoreGrade(score)}
            </span>
          </div>
        </div>

        <div className="space-y-2">
          <div className="flex justify-between text-xs text-muted-foreground">
            <span>Progress to Target</span>
            <span>{Math.round((score / 100) * target)}%</span>
          </div>
          <Progress 
            value={score} 
            className="h-2"
          />
        </div>

        <div className="pt-2 border-t border-border/50">
          <p className="text-xs text-muted-foreground">
            {score >= 80 ? "🎉 Excellent performance!" : "Keep improving!"}
          </p>
        </div>
      </CardContent>
    </Card>
  );
};

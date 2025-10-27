import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Sparkles } from "lucide-react";

export const SustainabilityScore = () => {
  const score = 78;
  const grade = "B+";

  return (
    <Card className="bg-gradient-success border-success/20 relative overflow-hidden">
      {/* Decorative Element */}
      <div className="absolute top-0 right-0 w-32 h-32 bg-success-foreground/10 rounded-full -translate-y-16 translate-x-16" />
      
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="text-xl font-semibold text-success-foreground">
            Sustainability Score
          </CardTitle>
          <Badge className="bg-success-foreground/20 text-success-foreground hover:bg-success-foreground/30">
            <Sparkles className="w-3 h-3 mr-1" />
            Improving
          </Badge>
        </div>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="flex items-center justify-center">
          <div className="relative">
            <svg className="w-40 h-40 transform -rotate-90">
              <circle
                cx="80"
                cy="80"
                r="70"
                stroke="currentColor"
                strokeWidth="12"
                fill="transparent"
                className="text-success-foreground/20"
              />
              <circle
                cx="80"
                cy="80"
                r="70"
                stroke="currentColor"
                strokeWidth="12"
                fill="transparent"
                strokeDasharray={`${2 * Math.PI * 70}`}
                strokeDashoffset={`${2 * Math.PI * 70 * (1 - score / 100)}`}
                className="text-success-foreground transition-all duration-1000 ease-out"
                strokeLinecap="round"
              />
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <span className="text-5xl font-bold text-success-foreground">
                {grade}
              </span>
              <span className="text-lg text-success-foreground/80">
                {score}/100
              </span>
            </div>
          </div>
        </div>

        <div className="space-y-2 text-center">
          <p className="text-success-foreground font-medium">
            Great Progress!
          </p>
          <p className="text-sm text-success-foreground/80">
            You're in the top 30% of hospitals for sustainability practices
          </p>
        </div>
      </CardContent>
    </Card>
  );
};

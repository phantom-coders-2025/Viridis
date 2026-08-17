import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Trophy, Award, Star, Zap, Leaf, Target, RefreshCw } from "lucide-react";
import { Progress } from "@/components/ui/progress";
import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";

const Gamification = () => {
  const { data: achievements = [], isLoading } = useQuery({
    queryKey: ["achievements"],
    queryFn: () => api.getAchievements(),
    retry: 1,
  });

  const leaderboard = [
    { dept: "Operating Theatres", score: 94, co2PerBed: 24.2, rank: 1 },
    { dept: "Intensive Care Unit (ICU)", score: 90, co2PerBed: 28.5, rank: 2 },
    { dept: "Radiology & Imaging", score: 86, co2PerBed: 31.8, rank: 3 },
    { dept: "General Inpatient Wards", score: 81, co2PerBed: 37.4, rank: 4 },
    { dept: "Outpatient Department (OPD)", score: 78, co2PerBed: 41.0, rank: 5 },
  ];

  const challenge = {
    title: "Operating Theatre Peak Solar Shift",
    description: "Consolidate elective surgery autoclave cycles during peak solar generation hours (11 AM - 3 PM)",
    progress: 75,
    daysLeft: 8,
  };

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-foreground flex items-center gap-2">
            <Trophy className="w-8 h-8 text-primary" />
            Gamification & Sustainability Badges
          </h1>
          <p className="text-muted-foreground">
            Inter-departmental green challenges, leaderboard recognition, and milestones
          </p>
        </div>
        {isLoading && (
          <div className="flex items-center gap-2 text-xs text-muted-foreground bg-muted/40 px-3 py-1.5 rounded-md self-start">
            <RefreshCw className="w-3.5 h-3.5 animate-spin text-primary" />
            <span>Syncing achievements...</span>
          </div>
        )}
      </div>

      {/* Active Challenge Banner */}
      <Card className="bg-gradient-primary border-primary/20 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-32 h-32 bg-primary-foreground/10 rounded-full -translate-y-16 translate-x-16" />
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="text-xl text-primary-foreground">
              🎯 Active Challenge
            </CardTitle>
            <Badge className="bg-primary-foreground/20 text-primary-foreground">
              {challenge.daysLeft} days left
            </Badge>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <h3 className="text-2xl font-bold text-primary-foreground">{challenge.title}</h3>
            <p className="text-primary-foreground/80 mt-1">{challenge.description}</p>
          </div>
          <div className="space-y-2">
            <div className="flex justify-between text-sm text-primary-foreground/90">
              <span>Progress</span>
              <span className="font-semibold">{challenge.progress}%</span>
            </div>
            <Progress value={challenge.progress} className="h-3 bg-primary-foreground/20" />
          </div>
        </CardContent>
      </Card>

      {/* Leaderboard */}
      <Card className="bg-gradient-card border-border/50">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Trophy className="w-5 h-5 text-primary" />
            Department Leaderboard
          </CardTitle>
          <p className="text-sm text-muted-foreground">Ranked by carbon efficiency per bed</p>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {leaderboard.map((dept) => (
              <div
                key={dept.rank}
                className={`flex items-center justify-between p-4 rounded-lg ${
                  dept.rank === 1
                    ? "bg-primary/10 border-2 border-primary/30"
                    : "bg-muted/30"
                }`}
              >
                <div className="flex items-center gap-4">
                  <div
                    className={`w-10 h-10 rounded-full flex items-center justify-center font-bold ${
                      dept.rank === 1
                        ? "bg-primary text-primary-foreground"
                        : dept.rank === 2
                        ? "bg-muted text-foreground"
                        : dept.rank === 3
                        ? "bg-warning/20 text-warning-foreground"
                        : "bg-muted text-muted-foreground"
                    }`}
                  >
                    {dept.rank === 1 && "🥇"}
                    {dept.rank === 2 && "🥈"}
                    {dept.rank === 3 && "🥉"}
                    {dept.rank > 3 && dept.rank}
                  </div>
                  <div>
                    <p className="font-semibold text-foreground">{dept.dept}</p>
                    <p className="text-sm text-muted-foreground">Score: {dept.score}/100</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-2xl font-bold text-foreground">{dept.co2PerBed}</p>
                  <p className="text-xs text-muted-foreground">kg CO₂e/bed</p>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Achievements from Live Database */}
      <Card className="bg-gradient-card border-border/50">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Star className="w-5 h-5 text-primary" />
            Hospital Achievements & Badges ({achievements.length} Unlocked)
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {achievements.map((ach) => (
              <div
                key={ach.id}
                className="p-4 rounded-lg border-2 bg-success/5 border-success/30"
              >
                <div className="flex items-start gap-3">
                  <Leaf className="w-8 h-8 text-success shrink-0" />
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <h4 className="font-semibold text-foreground">{ach.title}</h4>
                      <Badge className="bg-success text-success-foreground">Earned</Badge>
                    </div>
                    <p className="text-xs text-muted-foreground mt-1">
                      Awarded on {ach.date_earned}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Gamification;

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Trophy, Award, Star, Zap, Leaf, Target } from "lucide-react";
import { Progress } from "@/components/ui/progress";

const Gamification = () => {
  const leaderboard = [
    { dept: "Emergency Department", score: 92, co2PerBed: 28.5, rank: 1 },
    { dept: "Pediatrics", score: 88, co2PerBed: 31.2, rank: 2 },
    { dept: "Radiology", score: 84, co2PerBed: 34.8, rank: 3 },
    { dept: "General Wards", score: 78, co2PerBed: 42.1, rank: 4 },
    { dept: "Operating Theatres", score: 72, co2PerBed: 48.3, rank: 5 },
  ];

  const achievements = [
    { 
      name: "Energy Saver", 
      description: "Reduced energy by 15% in a month",
      icon: Zap,
      earned: true,
      color: "text-primary"
    },
    { 
      name: "Waste Warrior", 
      description: "Perfect waste segregation for 30 days",
      icon: Leaf,
      earned: true,
      color: "text-success"
    },
    { 
      name: "Water Champion", 
      description: "10% reduction in water usage",
      icon: Award,
      earned: false,
      color: "text-muted-foreground"
    },
    { 
      name: "Carbon Crusher", 
      description: "Hit monthly emissions target 3x",
      icon: Target,
      earned: true,
      color: "text-primary"
    },
  ];

  const challenge = {
    title: "October OT Energy Off",
    description: "Reduce Operating Theatre energy consumption by 10% this month",
    progress: 65,
    daysLeft: 12,
  };

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-3xl font-bold text-foreground flex items-center gap-2">
          <Trophy className="w-8 h-8 text-primary" />
          Gamification & Engagement
        </h1>
        <p className="text-muted-foreground">Celebrate success and drive positive change</p>
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
          <p className="text-sm text-primary-foreground/80">
            🌟 Complete this challenge to earn the <strong>"Energy Efficiency Master"</strong> badge!
          </p>
        </CardContent>
      </Card>

      {/* Leaderboard */}
      <Card className="bg-gradient-card border-border/50">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Trophy className="w-5 h-5 text-primary" />
            Department Leaderboard
          </CardTitle>
          <p className="text-sm text-muted-foreground">Ranked by CO₂ per bed efficiency</p>
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
                    <p className="text-sm text-muted-foreground">Score: {dept.score}</p>
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

      {/* Achievements */}
      <Card className="bg-gradient-card border-border/50">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Star className="w-5 h-5 text-primary" />
            Achievements & Badges
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {achievements.map((achievement) => (
              <div
                key={achievement.name}
                className={`p-4 rounded-lg border-2 ${
                  achievement.earned
                    ? "bg-success/5 border-success/30"
                    : "bg-muted/20 border-muted opacity-60"
                }`}
              >
                <div className="flex items-start gap-3">
                  <achievement.icon className={`w-8 h-8 ${achievement.color}`} />
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <h4 className="font-semibold text-foreground">{achievement.name}</h4>
                      {achievement.earned && (
                        <Badge className="bg-success text-success-foreground">Earned</Badge>
                      )}
                    </div>
                    <p className="text-sm text-muted-foreground mt-1">
                      {achievement.description}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Success Message */}
      <Card className="bg-gradient-success border-success/20 text-center">
        <CardContent className="pt-6">
          <div className="space-y-4">
            <div className="text-6xl">🎉</div>
            <div>
              <h3 className="text-2xl font-bold text-success-foreground">
                The Green Team is on fire!
              </h3>
              <p className="text-success-foreground/80 mt-2">
                You've collectively saved <strong>12,450 kg CO₂e</strong> this month
              </p>
              <p className="text-success-foreground/80">
                That's equivalent to planting <strong>570 trees!</strong> 🌳
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Gamification;

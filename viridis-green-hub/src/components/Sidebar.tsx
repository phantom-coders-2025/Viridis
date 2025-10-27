import { NavLink } from "react-router-dom";
import { 
  LayoutDashboard, 
  Calculator, 
  Award, 
  Upload, 
  Brain, 
  Users, 
  FileCheck, 
  Trophy 
} from "lucide-react";
import { cn } from "@/lib/utils";

const navItems = [
  { path: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { path: "/calculator", label: "Carbon Calculator", icon: Calculator },
  { path: "/score", label: "Sustainability Score", icon: Award },
  { path: "/import", label: "Data Import", icon: Upload },
  { path: "/insights", label: "AI Insights", icon: Brain },
  { path: "/comparison", label: "Peer Comparison", icon: Users },
  { path: "/compliance", label: "Compliance Reports", icon: FileCheck },
  { path: "/gamification", label: "Gamification", icon: Trophy },
];

export const Sidebar = () => {
  return (
    <aside className="w-64 bg-card border-r border-border min-h-screen sticky top-0">
      <div className="p-6 border-b border-border">
        <h1 className="text-2xl font-bold text-primary flex items-center gap-2">
          🌱 Viridis
        </h1>
        <p className="text-xs text-muted-foreground mt-1">
          Greening Healthcare
        </p>
      </div>
      
      <nav className="p-4 space-y-1">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            end={item.path === "/"}
            className={({ isActive }) =>
              cn(
                "flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-all",
                isActive
                  ? "bg-primary/10 text-primary shadow-sm"
                  : "text-muted-foreground hover:bg-muted hover:text-foreground"
              )
            }
          >
            <item.icon className="w-5 h-5" />
            <span>{item.label}</span>
          </NavLink>
        ))}
      </nav>
    </aside>
  );
};

import { useState, useEffect } from "react";
import { Bell, User, LogOut, Building2, Phone, Mail, Eye, ShieldCheck, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { useNavigate } from "react-router-dom";
import { api, UserProfile, Hospital } from "@/lib/api";

export const TopBar = () => {
  const [showProfile, setShowProfile] = useState(false);
  const [user, setUser] = useState<UserProfile | null>(null);
  const [hospital, setHospital] = useState<Hospital | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    // Check saved user info or fetch /auth/me
    const storedUser = localStorage.getItem("viridis_user");
    const storedHospital = localStorage.getItem("hospitalProfile");

    if (storedUser) {
      try {
        setUser(JSON.parse(storedUser));
      } catch (e) {
        console.error(e);
      }
    }
    if (storedHospital) {
      try {
        setHospital(JSON.parse(storedHospital));
      } catch (e) {
        console.error(e);
      }
    }

    // Refresh from API if token exists
    const token = localStorage.getItem("viridis_token");
    if (token) {
      api.getMe()
        .then((res) => {
          if (res.user) {
            setUser(res.user);
            localStorage.setItem("viridis_user", JSON.stringify(res.user));
          }
          if (res.hospital) {
            setHospital(res.hospital);
            localStorage.setItem("hospitalProfile", JSON.stringify(res.hospital));
          }
        })
        .catch(() => {});
    }
  }, []);

  const handleSignOut = () => {
    localStorage.removeItem("viridis_token");
    localStorage.removeItem("viridis_user");
    localStorage.removeItem("hospitalProfile");
    navigate("/signin");
  };

  const getRoleBadge = (role?: string) => {
    switch (role) {
      case "super_admin":
        return <Badge className="bg-purple-600 text-white hover:bg-purple-700">Super Admin</Badge>;
      case "auditor":
        return <Badge className="bg-amber-600 text-white hover:bg-amber-700">ESG Auditor</Badge>;
      case "department_manager":
        return <Badge className="bg-blue-600 text-white hover:bg-blue-700">Facility Lead</Badge>;
      default:
        return <Badge className="bg-emerald-600 text-white hover:bg-emerald-700">Hospital Admin</Badge>;
    }
  };

  return (
    <header className="h-16 bg-card border-b border-border px-6 flex items-center justify-between sticky top-0 z-10">
      {/* Left Section */}
      <div className="flex items-center gap-3">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-base font-bold text-foreground">
              {hospital?.name || "Apollo Green Care Facility"}
            </h2>
            {getRoleBadge(user?.role)}
          </div>
          <p className="text-xs text-muted-foreground">
            GHG Scopes 1-3 Telemetry & NABH Compliance Hub • {hospital?.location || "Main Campus"}
          </p>
        </div>
      </div>

      {/* Right Section */}
      <div className="flex items-center gap-3 relative">
        <Button
          variant="outline"
          size="sm"
          onClick={() => navigate("/insights")}
          className="hidden sm:flex items-center gap-1.5 border-primary/30 text-primary hover:bg-primary/10 text-xs h-8"
        >
          <Sparkles className="w-3.5 h-3.5" />
          AI What-If Simulator
        </Button>

        {/* Notifications */}
        <Button variant="ghost" size="icon" className="relative h-9 w-9">
          <Bell className="w-4 h-4" />
          <Badge
            variant="destructive"
            className="absolute -top-1 -right-1 w-4 h-4 flex items-center justify-center p-0 text-[9px]"
          >
            2
          </Badge>
        </Button>

        {/* Profile Button */}
        <Button
          variant="ghost"
          size="sm"
          onClick={() => setShowProfile(!showProfile)}
          className="flex items-center gap-2 h-9 px-2.5 rounded-lg border border-border"
        >
          <div className="w-6 h-6 rounded-full bg-primary/20 text-primary flex items-center justify-center text-xs font-bold">
            {user?.full_name ? user.full_name[0].toUpperCase() : "A"}
          </div>
          <span className="text-xs font-medium max-w-[110px] truncate hidden md:inline">
            {user?.full_name || user?.email || "Admin"}
          </span>
        </Button>

        {/* Profile Dropdown */}
        {showProfile && (
          <Card className="absolute right-0 top-12 w-72 bg-card border-border shadow-xl z-50 animate-fade-in">
            <div className="p-4 space-y-3">
              <div className="flex items-center gap-3 border-b border-border pb-3">
                <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center text-primary font-bold text-base">
                  {user?.full_name ? user.full_name.slice(0, 2).toUpperCase() : "AP"}
                </div>
                <div className="overflow-hidden">
                  <p className="font-semibold text-sm text-foreground truncate">
                    {user?.full_name || "Facility Administrator"}
                  </p>
                  <p className="text-xs text-muted-foreground truncate">{user?.email}</p>
                  <div className="mt-1">{getRoleBadge(user?.role)}</div>
                </div>
              </div>

              <div className="space-y-2 text-xs text-muted-foreground">
                <div className="flex items-center gap-2">
                  <Building2 className="w-3.5 h-3.5 text-primary" />
                  <span className="truncate">{hospital?.name || "Apollo Green Care"}</span>
                </div>
                <div className="flex items-center gap-2">
                  <ShieldCheck className="w-3.5 h-3.5 text-emerald-500" />
                  <span>NABH Green Verified • Grade A</span>
                </div>
                <div className="flex items-center gap-2">
                  <Mail className="w-3.5 h-3.5 text-primary" />
                  <span className="truncate">{user?.email || "admin@apollo.com"}</span>
                </div>
              </div>

              <div className="pt-3 border-t border-border space-y-1.5">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => {
                    setShowProfile(false);
                    navigate("/profile");
                  }}
                  className="w-full border-primary/30 text-primary hover:bg-primary/10 flex items-center justify-center gap-2 text-xs"
                >
                  <Eye className="w-3.5 h-3.5" /> View Profile & Hospital Details
                </Button>

                <Button
                  variant="ghost"
                  size="sm"
                  onClick={handleSignOut}
                  className="w-full text-destructive hover:bg-destructive/10 flex items-center justify-center gap-2 text-xs"
                >
                  <LogOut className="w-3.5 h-3.5" /> Sign Out
                </Button>
              </div>
            </div>
          </Card>
        )}
      </div>
    </header>
  );
};


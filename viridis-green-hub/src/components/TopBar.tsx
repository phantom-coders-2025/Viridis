import { useState } from "react";
import { Bell, User, LogOut, Building2, Phone, Mail, Eye } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { useNavigate } from "react-router-dom";

export const TopBar = () => {
  const [showProfile, setShowProfile] = useState(false);
  const navigate = useNavigate();

  const handleSignOut = () => {
    localStorage.removeItem("hospitalProfile");
    alert("Signed out successfully!");
    navigate("/signin");
  };

  // ✅ Load hospital data dynamically
  const hospitalData = JSON.parse(localStorage.getItem("hospitalProfile") || "{}");

  return (
    <header className="h-16 bg-card border-b border-border px-6 flex items-center justify-between sticky top-0 z-10">
      {/* Left Section */}
      <div>
        <h2 className="text-lg font-semibold text-foreground">
          {hospitalData.hospitalName || "Hospital Dashboard"}
        </h2>
        <p className="text-xs text-muted-foreground">Sustainability Dashboard</p>
      </div>

      {/* Right Section */}
      <div className="flex items-center gap-4 relative">
        {/* Notifications */}
        <Button variant="ghost" size="icon" className="relative">
          <Bell className="w-5 h-5" />
          <Badge
            variant="destructive"
            className="absolute -top-1 -right-1 w-5 h-5 flex items-center justify-center p-0 text-[10px]"
          >
            3
          </Badge>
        </Button>

        {/* Profile Icon */}
        <Button
          variant="ghost"
          size="icon"
          onClick={() => setShowProfile(!showProfile)}
          className="relative"
        >
          <User className="w-5 h-5" />
        </Button>

        {/* Profile Dropdown */}
        {showProfile && (
          <Card className="absolute right-0 top-12 w-64 bg-card border-border shadow-lg animate-fade-in">
            <div className="p-4 space-y-3">
              <div className="flex items-center gap-3 border-b border-border pb-3">
                <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center text-primary font-bold">
                  {hospitalData.hospitalName
                    ? hospitalData.hospitalName.slice(0, 2).toUpperCase()
                    : "HP"}
                </div>
                <div>
                  <p className="font-semibold text-foreground truncate max-w-[150px]">
                    {hospitalData.hospitalName || "Hospital Name"}
                  </p>
                  <p className="text-xs text-muted-foreground">
                    {hospitalData.registrationId || "HSP-XXXX"}
                  </p>
                </div>
              </div>

              <div className="space-y-2 text-sm text-muted-foreground">
                <div className="flex items-center gap-2">
                  <Building2 className="w-4 h-4 text-primary" />
                  <span>{hospitalData.location || "Unknown Location"}</span>
                </div>
                <div className="flex items-center gap-2">
                  <Phone className="w-4 h-4 text-primary" />
                  <span>{hospitalData.phone || "No phone added"}</span>
                </div>
                <div className="flex items-center gap-2">
                  <Mail className="w-4 h-4 text-primary" />
                  <span>{hospitalData.email || "No email set"}</span>
                </div>
              </div>

              <div className="pt-3 border-t border-border space-y-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => navigate("/profile")}
                  className="w-full border-primary/30 text-primary hover:bg-primary/10 flex items-center justify-center gap-2"
                >
                  <Eye className="w-4 h-4" /> View Profile
                </Button>

                <Button
                  variant="ghost"
                  size="sm"
                  onClick={handleSignOut}
                  className="w-full text-destructive hover:bg-destructive/10 flex items-center justify-center gap-2"
                >
                  <LogOut className="w-4 h-4" /> Sign Out
                </Button>
              </div>
            </div>
          </Card>
        )}
      </div>
    </header>
  );
};

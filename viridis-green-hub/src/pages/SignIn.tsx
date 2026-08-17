// src/pages/SignIn.tsx
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Leaf, Mail, Lock, Loader2, Sparkles } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { useToast } from "@/hooks/use-toast";
import bgImage from "@/assets/hero-hospital.jpg";
import { api } from "@/lib/api";

export const SignIn = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { toast } = useToast();

  const handleFillDemoRole = (roleEmail: string, rolePass: string, label: string) => {
    setEmail(roleEmail);
    setPassword(rolePass);
    toast({
      title: `${label} Credentials Loaded ✨`,
      description: `Ready to sign in as ${roleEmail}`,
    });
  };

  const handleSignIn = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const res = await api.login({
        email: email.trim(),
        password: password,
      });

      // Save token and hospital profile
      localStorage.setItem("viridis_token", res.access_token);
      localStorage.setItem(
        "hospitalProfile",
        JSON.stringify({
          hospitalName: res.hospital?.name || "Apollo Green Care Hospital",
          registrationId: "HSP-1023",
          hospitalType: res.hospital?.type || "Tertiary Care Multi-Speciality",
          location: res.hospital?.location || "Chennai Central Campus",
          email: res.user.email,
          phone: res.user.phone || "+91 98765 43210",
        })
      );

      toast({
        title: "Login Successful! ✅",
        description: `Welcome back, ${res.user.full_name || res.user.email}!`,
      });

      // Redirect to dashboard
      setTimeout(() => navigate("/dashboard"), 800);
    } catch (err: unknown) {
      const errorMsg =
        err instanceof Error
          ? err.message
          : "Invalid email or password. Please verify your credentials.";
      toast({
        title: "Authentication Failed",
        description: errorMsg,
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden px-4">
      {/* Background Image */}
      <div className="absolute inset-0 -z-10">
        <img
          src={bgImage}
          alt="Hospital sustainability background"
          className="w-full h-full object-cover brightness-75"
        />
        <div className="absolute inset-0 bg-gradient-to-br from-black/60 via-emerald-900/40 to-black/70" />
      </div>

      {/* Sign-in Card */}
      <Card className="w-full max-w-md bg-card/95 border-border/40 backdrop-blur-xl shadow-2xl">
        <CardHeader className="text-center">
          <div className="flex justify-center mb-3">
            <Leaf className="w-8 h-8 text-emerald-500" />
          </div>
          <CardTitle className="text-2xl font-bold text-foreground">
            Sign in to <span className="text-emerald-500">Viridis</span>
          </CardTitle>
          <p className="text-sm text-muted-foreground mt-1">
            Clinical Carbon Telemetry & ESG Intelligence 🌱
          </p>
        </CardHeader>

        <CardContent>
          <form onSubmit={handleSignIn} className="space-y-4">
            {/* Email */}
            <div>
              <div className="relative">
                <Mail className="w-4 h-4 absolute left-3 top-3 text-muted-foreground" />
                <Input
                  type="email"
                  placeholder="Email address"
                  className="pl-9"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>
            </div>

            {/* Password */}
            <div>
              <div className="relative">
                <Lock className="w-4 h-4 absolute left-3 top-3 text-muted-foreground" />
                <Input
                  type="password"
                  placeholder="Password"
                  className="pl-9"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </div>
            </div>

            {/* Submit */}
            <Button
              type="submit"
              disabled={loading}
              className="w-full bg-emerald-500 hover:bg-emerald-600 text-white flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  Authenticating...
                </>
              ) : (
                "Sign In"
              )}
            </Button>

            {/* 1-Click Role Presets */}
            <div className="pt-3 border-t border-border/40 space-y-2">
              <p className="text-[11px] text-center font-medium text-muted-foreground uppercase tracking-wider">
                Instant Demo Role Access
              </p>
              <div className="grid grid-cols-2 gap-1.5">
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={() => handleFillDemoRole("admin@apollo.com", "Admin@12345", "Hospital Admin")}
                  className="text-xs h-8 border-emerald-500/30 hover:bg-emerald-500/10 text-foreground"
                >
                  🏥 Hospital Admin
                </Button>
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={() => handleFillDemoRole("superadmin@viridis.io", "Super@12345", "Super Admin")}
                  className="text-xs h-8 border-emerald-500/30 hover:bg-emerald-500/10 text-foreground"
                >
                  👑 Super Admin
                </Button>
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={() => handleFillDemoRole("facility@apollo.com", "Facility@12345", "Facility Lead")}
                  className="text-xs h-8 border-emerald-500/30 hover:bg-emerald-500/10 text-foreground"
                >
                  ⚡ Facility Lead
                </Button>
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={() => handleFillDemoRole("auditor@esg-cert.org", "Auditor@12345", "ESG Auditor")}
                  className="text-xs h-8 border-emerald-500/30 hover:bg-emerald-500/10 text-foreground"
                >
                  📋 ESG Auditor
                </Button>
              </div>
            </div>

            {/* Link to Sign Up */}
            <p className="text-center text-xs text-muted-foreground mt-2">

              Don’t have an account?{" "}
              <button
                type="button"
                onClick={() => navigate("/signup")}
                className="text-emerald-400 hover:underline font-medium"
              >
                Register your Hospital
              </button>
            </p>
          </form>
        </CardContent>
      </Card>
    </section>
  );
};

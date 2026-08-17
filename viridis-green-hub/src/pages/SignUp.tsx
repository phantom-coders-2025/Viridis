// src/pages/SignUp.tsx
import { useState } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { useToast } from "@/hooks/use-toast";
import { useNavigate } from "react-router-dom";
import { Building2, Mail, Lock, Phone, Leaf, Loader2 } from "lucide-react";
import bgImage from "@/assets/hero-hospital.jpg";
import { api } from "@/lib/api";

export const SignUp = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  const [loading, setLoading] = useState(false);

  const [formData, setFormData] = useState({
    hospitalName: "",
    registrationId: "",
    hospitalType: "",
    location: "",
    email: "",
    phone: "",
    password: "",
    confirmPassword: "",
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (formData.password !== formData.confirmPassword) {
      toast({
        title: "Password Mismatch",
        description: "Your passwords do not match. Please verify and try again.",
        variant: "destructive",
      });
      return;
    }

    setLoading(true);

    try {
      const res = await api.register({
        hospitalName: formData.hospitalName,
        registrationId: formData.registrationId,
        hospitalType: formData.hospitalType,
        location: formData.location,
        email: formData.email,
        phone: formData.phone,
        password: formData.password,
      });

      // Save token and profile to localStorage
      localStorage.setItem("viridis_token", res.access_token);
      localStorage.setItem(
        "hospitalProfile",
        JSON.stringify({
          hospitalName: res.hospital?.name || formData.hospitalName,
          registrationId: formData.registrationId,
          hospitalType: res.hospital?.type || formData.hospitalType,
          location: res.hospital?.location || formData.location,
          email: res.user.email,
          phone: res.user.phone || formData.phone,
        })
      );

      toast({
        title: "Registration Successful! 🎉",
        description: `Welcome to Viridis, ${formData.hospitalName}! Redirecting to dashboard...`,
      });

      setTimeout(() => navigate("/dashboard"), 1000);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Failed to register hospital";
      toast({
        title: "Registration Failed",
        description: msg,
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden py-12 px-4">
      {/* Background Image */}
      <div className="absolute inset-0 -z-10">
        <img
          src={bgImage}
          alt="Hospital background"
          className="w-full h-full object-cover brightness-75"
        />
        <div className="absolute inset-0 bg-gradient-to-br from-black/60 via-emerald-900/40 to-black/70" />
      </div>

      {/* Registration Card */}
      <Card className="w-full max-w-lg bg-card/95 border-border/40 backdrop-blur-xl shadow-2xl">
        <CardHeader>
          <div className="flex justify-center mb-3">
            <Leaf className="w-8 h-8 text-emerald-500" />
          </div>
          <CardTitle className="text-2xl font-bold text-center text-foreground">
            Register with <span className="text-emerald-500">Viridis</span>
          </CardTitle>
          <p className="text-sm text-center text-muted-foreground mt-1">
            Join the movement to decarbonize healthcare 🌱
          </p>
        </CardHeader>

        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Hospital Name */}
            <div>
              <Label htmlFor="hospitalName">Hospital / Medical Center Name</Label>
              <div className="relative mt-1">
                <Building2 className="w-4 h-4 absolute left-3 top-3 text-muted-foreground" />
                <Input
                  id="hospitalName"
                  name="hospitalName"
                  value={formData.hospitalName}
                  onChange={handleChange}
                  placeholder="e.g., St. Jude Eco Care Hospital"
                  className="pl-9"
                  required
                />
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {/* Registration ID */}
              <div>
                <Label htmlFor="registrationId">Registration ID</Label>
                <Input
                  id="registrationId"
                  name="registrationId"
                  value={formData.registrationId}
                  onChange={handleChange}
                  placeholder="HSP-1023"
                  className="mt-1"
                  required
                />
              </div>

              {/* Hospital Type */}
              <div>
                <Label htmlFor="hospitalType">Hospital Type</Label>
                <Input
                  id="hospitalType"
                  name="hospitalType"
                  value={formData.hospitalType}
                  onChange={handleChange}
                  placeholder="Private / Public / Trust"
                  className="mt-1"
                  required
                />
              </div>
            </div>

            {/* Location */}
            <div>
              <Label htmlFor="location">Campus Location</Label>
              <Input
                id="location"
                name="location"
                value={formData.location}
                onChange={handleChange}
                placeholder="City, State"
                className="mt-1"
                required
              />
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {/* Email */}
              <div>
                <Label htmlFor="email">Official Email</Label>
                <div className="relative mt-1">
                  <Mail className="w-4 h-4 absolute left-3 top-3 text-muted-foreground" />
                  <Input
                    id="email"
                    name="email"
                    type="email"
                    value={formData.email}
                    onChange={handleChange}
                    className="pl-9"
                    placeholder="admin@hospital.com"
                    required
                  />
                </div>
              </div>

              {/* Phone */}
              <div>
                <Label htmlFor="phone">Contact Phone</Label>
                <div className="relative mt-1">
                  <Phone className="w-4 h-4 absolute left-3 top-3 text-muted-foreground" />
                  <Input
                    id="phone"
                    name="phone"
                    value={formData.phone}
                    onChange={handleChange}
                    className="pl-9"
                    placeholder="+91 98765 43210"
                    required
                  />
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {/* Password */}
              <div>
                <Label htmlFor="password">Password</Label>
                <div className="relative mt-1">
                  <Lock className="w-4 h-4 absolute left-3 top-3 text-muted-foreground" />
                  <Input
                    id="password"
                    name="password"
                    type="password"
                    value={formData.password}
                    onChange={handleChange}
                    className="pl-9"
                    placeholder="••••••••"
                    required
                  />
                </div>
              </div>

              {/* Confirm Password */}
              <div>
                <Label htmlFor="confirmPassword">Confirm Password</Label>
                <Input
                  id="confirmPassword"
                  name="confirmPassword"
                  type="password"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  placeholder="Re-enter password"
                  className="mt-1"
                  required
                />
              </div>
            </div>

            {/* Submit Button */}
            <Button
              type="submit"
              disabled={loading}
              className="w-full bg-emerald-500 hover:bg-emerald-600 text-white font-medium mt-4 flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  Registering Hospital Account...
                </>
              ) : (
                "Register Hospital"
              )}
            </Button>

            {/* Redirect to Sign In */}
            <p className="text-center text-xs text-muted-foreground mt-2">
              Already registered?{" "}
              <button
                type="button"
                onClick={() => navigate("/signin")}
                className="text-emerald-400 hover:underline font-medium"
              >
                Sign In here
              </button>
            </p>
          </form>
        </CardContent>
      </Card>
    </section>
  );
};

// src/pages/SignUp.tsx
import { useState } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { useToast } from "@/hooks/use-toast";
import { useNavigate } from "react-router-dom";
import { Building2, Mail, Lock, Phone, Leaf } from "lucide-react";
import bgImage from "@/assets/hero-hospital.jpg"; // ✅ Background image

export const SignUp = () => {
  const navigate = useNavigate();
  const { toast } = useToast();

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

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (formData.password !== formData.confirmPassword) {
      toast({
        title: "Password Mismatch",
        description: "Your passwords do not match. Please try again.",
        variant: "destructive",
      });
      return;
    }

    // ✅ Save hospital details to localStorage
    localStorage.setItem("hospitalProfile", JSON.stringify(formData));

    toast({
      title: "Registration Successful 🎉",
      description: `${formData.hospitalName} has been registered successfully!`,
    });

    // Redirect to Sign In page
    setTimeout(() => navigate("/signin"), 1200);
  };

  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* 🌄 Background Image */}
      <div className="absolute inset-0 -z-10">
        <img
          src={bgImage}
          alt="Hospital background"
          className="w-full h-full object-cover brightness-75"
        />
        <div className="absolute inset-0 bg-gradient-to-br from-black/60 via-emerald-900/40 to-black/70" />
      </div>

      {/* 🏥 Registration Card */}
      <Card className="w-full max-w-md bg-card/90 border-border/40 backdrop-blur-xl shadow-xl">
        <CardHeader>
          <div className="flex justify-center mb-3">
            <Leaf className="w-8 h-8 text-emerald-500" />
          </div>
          <CardTitle className="text-2xl font-bold text-center text-foreground">
            Register with <span className="text-emerald-500">Viridis</span>
          </CardTitle>
          <p className="text-sm text-center text-muted-foreground mt-1">
            Join the movement to build greener healthcare 🌱
          </p>
        </CardHeader>

        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Hospital Name */}
            <div>
              <Label htmlFor="hospitalName">Hospital Name</Label>
              <div className="relative">
                <Building2 className="w-4 h-4 absolute left-3 top-3 text-muted-foreground" />
                <Input
                  id="hospitalName"
                  name="hospitalName"
                  value={formData.hospitalName}
                  onChange={handleChange}
                  placeholder="e.g., Green Valley Medical Center"
                  className="pl-9"
                  required
                />
              </div>
            </div>

            {/* Registration ID */}
            <div>
              <Label htmlFor="registrationId">Registration ID</Label>
              <Input
                id="registrationId"
                name="registrationId"
                value={formData.registrationId}
                onChange={handleChange}
                placeholder="HSP-1023"
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
                placeholder="Government / Private / NGO"
                required
              />
            </div>

            {/* Location */}
            <div>
              <Label htmlFor="location">Location</Label>
              <Input
                id="location"
                name="location"
                value={formData.location}
                onChange={handleChange}
                placeholder="City, State"
                required
              />
            </div>

            {/* Email */}
            <div>
              <Label htmlFor="email">Official Email</Label>
              <div className="relative">
                <Mail className="w-4 h-4 absolute left-3 top-3 text-muted-foreground" />
                <Input
                  id="email"
                  name="email"
                  type="email"
                  value={formData.email}
                  onChange={handleChange}
                  className="pl-9"
                  placeholder="hospital@example.com"
                  required
                />
              </div>
            </div>

            {/* Phone */}
            <div>
              <Label htmlFor="phone">Contact Number</Label>
              <div className="relative">
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

            {/* Password */}
            <div>
              <Label htmlFor="password">Password</Label>
              <div className="relative">
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
                required
              />
            </div>

            {/* Submit Button */}
            <Button
              type="submit"
              className="w-full bg-emerald-500 hover:bg-emerald-600 text-white font-medium mt-4"
            >
              Register Hospital
            </Button>

            {/* Redirect to Sign In */}
            <p className="text-center text-xs text-muted-foreground mt-2">
              Already registered?{" "}
              <button
                type="button"
                onClick={() => navigate("/signin")}
                className="text-emerald-400 hover:underline"
              >
                Sign In
              </button>
            </p>
          </form>
        </CardContent>
      </Card>
    </section>
  );
};

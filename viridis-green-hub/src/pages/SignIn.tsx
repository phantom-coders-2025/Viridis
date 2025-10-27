// src/pages/SignIn.tsx
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Leaf, Mail, Lock } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { useToast } from "@/hooks/use-toast";
import bgImage from "@/assets/hero-hospital.jpg"; // ✅ Background image

export const SignIn = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();
  const { toast } = useToast();

  const handleSignIn = (e: React.FormEvent) => {
    e.preventDefault();

    const storedData = localStorage.getItem("hospitalProfile");

    if (!storedData) {
      toast({
        title: "No Account Found",
        description: "Please sign up before logging in.",
        variant: "destructive",
      });
      return;
    }

    const hospital = JSON.parse(storedData);

    if (email === hospital.email && password === hospital.password) {
      toast({
        title: "Login Successful ✅",
        description: `Welcome back, ${hospital.hospitalName}!`,
      });

      // Redirect to dashboard
      setTimeout(() => navigate("/dashboard"), 1000);
    } else {
      toast({
        title: "Invalid Credentials",
        description: "Please check your email or password.",
        variant: "destructive",
      });
    }
  };

  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* 🌄 Background Image */}
      <div className="absolute inset-0 -z-10">
        <img
          src={bgImage}
          alt="Hospital sustainability background"
          className="w-full h-full object-cover brightness-75"
        />
        <div className="absolute inset-0 bg-gradient-to-br from-black/60 via-emerald-900/40 to-black/70" />
      </div>

      {/* 🪪 Sign-in Card */}
      <Card className="w-full max-w-md bg-card/90 border-border/40 backdrop-blur-xl shadow-xl">
        <CardHeader className="text-center">
          <div className="flex justify-center mb-3">
            <Leaf className="w-8 h-8 text-emerald-500" />
          </div>
          <CardTitle className="text-2xl font-bold text-foreground">
            Sign in to <span className="text-emerald-500">Viridis</span>
          </CardTitle>
          <p className="text-sm text-muted-foreground mt-1">
            Welcome back — let’s continue greening healthcare 🌱
          </p>
        </CardHeader>

        <CardContent>
          <form onSubmit={handleSignIn} className="space-y-4">
            {/* Email */}
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

            {/* Password */}
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

            {/* Submit */}
            <Button
              type="submit"
              className="w-full bg-emerald-500 hover:bg-emerald-600 text-white"
            >
              Sign In
            </Button>

            {/* Link to Sign Up */}
            <p className="text-center text-xs text-muted-foreground">
              Don’t have an account?{" "}
              <button
                type="button"
                onClick={() => navigate("/signup")}
                className="text-emerald-400 hover:underline"
              >
                Sign Up
              </button>
            </p>
          </form>
        </CardContent>
      </Card>
    </section>
  );
};

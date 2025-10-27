// src/pages/Home.tsx
import { Button } from "@/components/ui/button";
import { Leaf } from "lucide-react";
import { useNavigate } from "react-router-dom";
import bgImage from "@/assets/hero-hospital.jpg"; 

export const Home = () => {
  const navigate = useNavigate();

  return (
    <section className="relative min-h-screen flex flex-col items-center justify-center overflow-hidden text-center">
      {/* Background Image */}
      <div className="absolute inset-0 -z-10">
        <img
          src={bgImage}
          alt="Sustainable background"
          className="w-full h-full object-cover brightness-75"
        />
        <div className="absolute inset-0 bg-gradient-to-b from-black/60 via-emerald-900/40 to-black/80" />
      </div>

      {/* Floating glow effect */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-20 left-10 w-32 h-32 bg-emerald-500/20 blur-3xl rounded-full animate-pulse" />
        <div className="absolute bottom-10 right-10 w-48 h-48 bg-green-400/10 blur-3xl rounded-full animate-pulse" />
      </div>

      {/* Main Content */}
      <div className="max-w-3xl space-y-6 px-6 animate-fade-in">
        <div className="inline-flex items-center gap-2 bg-emerald-500/20 border border-emerald-400/40 backdrop-blur-sm px-4 py-2 rounded-full">
          <Leaf className="w-4 h-4 text-emerald-400" />
          <span className="text-sm font-medium text-emerald-200">
            Greening Healthcare with AI
          </span>
        </div>

        <h1 className="text-5xl md:text-7xl font-bold text-white leading-tight drop-shadow-lg">
          Welcome to <span className="text-emerald-400">Viridis</span>
        </h1>

        <p className="text-lg md:text-xl text-gray-200 font-light">
          Empower hospitals to measure, reduce, and celebrate sustainability — one insight at a time.
        </p>

        {/* Buttons */}
        <div className="flex flex-wrap justify-center gap-4 pt-6">
          <Button
            size="lg"
            className="bg-emerald-500 hover:bg-emerald-600 text-white font-semibold px-8 py-3 shadow-glow transition-all hover:scale-105"
            onClick={() => navigate("/signin")}
          >
            Get Started
          </Button>

          
        </div>
      </div>

      <footer className="absolute bottom-6 text-xs text-gray-300">
        © 2025 Viridis | Built for a Sustainable Future
      </footer>
    </section>
  );
};

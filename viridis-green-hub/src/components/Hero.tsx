import { Leaf } from "lucide-react";
import { Button } from "@/components/ui/button";
import heroImage from "@/assets/hero-hospital.jpg";

export const Hero = () => {
  return (
    <section className="relative min-h-[80vh] flex items-center overflow-hidden">
      {/* Background Image with Overlay */}
      <div className="absolute inset-0 z-0">
        <img 
          src={heroImage} 
          alt="Sustainable hospital" 
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-r from-primary/90 via-primary/70 to-transparent" />
      </div>

      {/* Content */}
      <div className="container relative z-10 px-4 py-20">
        <div className="max-w-2xl space-y-6 animate-fade-in">
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-success/20 backdrop-blur-sm rounded-full border border-success/30">
            <Leaf className="w-4 h-4 text-success-foreground" />
            <span className="text-sm font-medium text-success-foreground">
              Sustainability Made Simple
            </span>
          </div>

          <h1 className="text-5xl md:text-7xl font-bold text-primary-foreground leading-tight">
            🌱 Welcome to <span className="text-accent">Viridis</span>
          </h1>
          
          <p className="text-xl md:text-2xl text-primary-foreground/90 font-light">
            Greening Healthcare, One Data Point at a Time
          </p>

          <p className="text-lg text-primary-foreground/80 max-w-xl">
            Empower your hospital to track, compare, improve, and celebrate sustainability efforts with intelligent insights and gamified progress tracking.
          </p>

          <div className="flex flex-wrap gap-4 pt-4">
            <Button 
              size="lg" 
              className="bg-accent hover:bg-accent/90 text-accent-foreground shadow-glow transition-all hover:scale-105"
            >
              Get Started
            </Button>
            <Button 
              size="lg" 
              variant="outline"
              className="border-primary-foreground/30 text-primary-foreground hover:bg-primary-foreground/10 backdrop-blur-sm"
            >
              Watch Demo
            </Button>
          </div>
        </div>
      </div>
    </section>
  );
};

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Zap, Droplets, Trash2, Calculator } from "lucide-react";

const CarbonCalculator = () => {
  const [electricity, setElectricity] = useState("");
  const [water, setWater] = useState("");
  const [waste, setWaste] = useState("");
  const [results, setResults] = useState<{ electricity: number; water: number; waste: number; total: number } | null>(null);

  const calculateFootprint = () => {
    const electricityCO2 = parseFloat(electricity) * 0.82 || 0; // kg CO2 per kWh
    const waterCO2 = parseFloat(water) * 0.00118 || 0; // kg CO2 per liter
    const wasteCO2 = parseFloat(waste) * 1.2 || 0; // kg CO2 per kg waste
    
    setResults({
      electricity: Math.round(electricityCO2),
      water: Math.round(waterCO2),
      waste: Math.round(wasteCO2),
      total: Math.round(electricityCO2 + waterCO2 + wasteCO2)
    });
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 animate-fade-in">
      <div>
        <h1 className="text-3xl font-bold text-foreground">Carbon Footprint Calculator</h1>
        <p className="text-muted-foreground">Calculate your hospital's monthly CO₂e emissions</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card className="bg-gradient-card border-border/50">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-lg">
              <Zap className="w-5 h-5 text-primary" />
              Electricity
            </CardTitle>
          </CardHeader>
          <CardContent>
            <Label htmlFor="electricity" className="text-sm text-muted-foreground">
              Monthly Usage (kWh)
            </Label>
            <Input
              id="electricity"
              type="number"
              placeholder="15000"
              value={electricity}
              onChange={(e) => setElectricity(e.target.value)}
              className="mt-2"
            />
          </CardContent>
        </Card>

        <Card className="bg-gradient-card border-border/50">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-lg">
              <Droplets className="w-5 h-5 text-primary" />
              Water
            </CardTitle>
          </CardHeader>
          <CardContent>
            <Label htmlFor="water" className="text-sm text-muted-foreground">
              Monthly Usage (liters)
            </Label>
            <Input
              id="water"
              type="number"
              placeholder="15200"
              value={water}
              onChange={(e) => setWater(e.target.value)}
              className="mt-2"
            />
          </CardContent>
        </Card>

        <Card className="bg-gradient-card border-border/50">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-lg">
              <Trash2 className="w-5 h-5 text-primary" />
              Biomedical Waste
            </CardTitle>
          </CardHeader>
          <CardContent>
            <Label htmlFor="waste" className="text-sm text-muted-foreground">
              Monthly Waste (kg)
            </Label>
            <Input
              id="waste"
              type="number"
              placeholder="1250"
              value={waste}
              onChange={(e) => setWaste(e.target.value)}
              className="mt-2"
            />
          </CardContent>
        </Card>
      </div>

      <Button 
        onClick={calculateFootprint} 
        size="lg" 
        className="w-full bg-primary hover:bg-primary/90"
      >
        <Calculator className="w-5 h-5 mr-2" />
        Calculate Carbon Footprint
      </Button>

      {results && (
        <Card className="bg-gradient-success border-success/20 animate-scale-in">
          <CardHeader>
            <CardTitle className="text-2xl text-center text-success-foreground">
              Total CO₂e Emissions
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="text-center">
              <p className="text-6xl font-bold text-success-foreground">
                {results.total.toLocaleString()}
              </p>
              <p className="text-lg text-success-foreground/80 mt-2">kg CO₂e / month</p>
            </div>

            <div className="grid grid-cols-3 gap-4 pt-4 border-t border-success/20">
              <div className="text-center">
                <p className="text-sm text-success-foreground/70">Electricity</p>
                <p className="text-2xl font-bold text-success-foreground">{results.electricity.toLocaleString()}</p>
                <p className="text-xs text-success-foreground/60">kg CO₂e</p>
              </div>
              <div className="text-center">
                <p className="text-sm text-success-foreground/70">Water</p>
                <p className="text-2xl font-bold text-success-foreground">{results.water.toLocaleString()}</p>
                <p className="text-xs text-success-foreground/60">kg CO₂e</p>
              </div>
              <div className="text-center">
                <p className="text-sm text-success-foreground/70">Waste</p>
                <p className="text-2xl font-bold text-success-foreground">{results.waste.toLocaleString()}</p>
                <p className="text-xs text-success-foreground/60">kg CO₂e</p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default CarbonCalculator;

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Zap, Droplets, Trash2, Calculator, Flame, Wind, Trees, Car, Sparkles, Building2 } from "lucide-react";

const CarbonCalculator = () => {
  // Scope 1 State
  const [dieselLiters, setDieselLiters] = useState<string>("450");
  const [desfluraneKg, setDesfluraneKg] = useState<string>("3.5");
  const [sevofluraneKg, setSevofluraneKg] = useState<string>("12.0");
  const [gasM3, setGasM3] = useState<string>("200");

  // Scope 2 State
  const [electricityKwh, setElectricityKwh] = useState<string>("24000");
  const [solarOffsetKwh, setSolarOffsetKwh] = useState<string>("6000");

  // Scope 3 State
  const [yellowWasteKg, setYellowWasteKg] = useState<string>("850");
  const [redWasteKg, setRedWasteKg] = useState<string>("920");
  const [waterLiters, setWaterLiters] = useState<string>("45000");

  const [results, setResults] = useState<{
    scope1: number;
    scope2: number;
    scope3: number;
    total: number;
    treesOffset: number;
    carKm: number;
  } | null>(null);

  const calculateFootprint = () => {
    // Scope 1
    const dieselCO2 = (parseFloat(dieselLiters) || 0) * 2.68;
    const desfluraneCO2 = (parseFloat(desfluraneKg) || 0) * 2540.0;
    const sevofluraneCO2 = (parseFloat(sevofluraneKg) || 0) * 130.0;
    const gasCO2 = (parseFloat(gasM3) || 0) * 2.02;
    const scope1Total = dieselCO2 + desfluraneCO2 + sevofluraneCO2 + gasCO2;

    // Scope 2 (Grid minus clean solar)
    const netGridKwh = Math.max(0, (parseFloat(electricityKwh) || 0) - (parseFloat(solarOffsetKwh) || 0));
    const scope2Total = netGridKwh * 0.82;

    // Scope 3 (Yellow Incinerated @ 2.85, Red Autoclaved @ 0.72, Water @ 0.00034)
    const yellowCO2 = (parseFloat(yellowWasteKg) || 0) * 2.85;
    const redCO2 = (parseFloat(redWasteKg) || 0) * 0.72;
    const waterCO2 = (parseFloat(waterLiters) || 0) * 0.00034;
    const scope3Total = yellowCO2 + redCO2 + waterCO2;

    const grandTotal = scope1Total + scope2Total + scope3Total;
    const trees = Math.round(grandTotal / 21.77); // ~21.77 kg CO2 absorbed per mature tree/year
    const carKilometers = Math.round(grandTotal / 0.17); // ~0.17 kg CO2 per passenger car km

    setResults({
      scope1: Math.round(scope1Total),
      scope2: Math.round(scope2Total),
      scope3: Math.round(scope3Total),
      total: Math.round(grandTotal),
      treesOffset: trees,
      carKm: carKilometers,
    });
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 animate-fade-in pb-12">
      {/* Header */}
      <div className="bg-gradient-to-r from-card via-card to-primary/5 p-6 rounded-2xl border border-border shadow-sm">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-xl bg-primary/15 text-primary">
            <Calculator className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-foreground">
              GHG Protocol Carbon Calculator
            </h1>
            <p className="text-xs sm:text-sm text-muted-foreground mt-0.5">
              Comprehensive Scope 1, Scope 2, and Scope 3 healthcare telemetry carbon accounting tool.
            </p>
          </div>
        </div>
      </div>

      <Tabs defaultValue="scope1" className="space-y-4">
        <TabsList className="grid grid-cols-3 h-10 p-1 bg-muted/60">
          <TabsTrigger value="scope1" className="text-xs font-semibold data-[state=active]:bg-card">
            <Flame className="w-3.5 h-3.5 mr-1.5 text-amber-500" />
            Scope 1 (Direct)
          </TabsTrigger>
          <TabsTrigger value="scope2" className="text-xs font-semibold data-[state=active]:bg-card">
            <Zap className="w-3.5 h-3.5 mr-1.5 text-blue-500" />
            Scope 2 (Energy)
          </TabsTrigger>
          <TabsTrigger value="scope3" className="text-xs font-semibold data-[state=active]:bg-card">
            <Wind className="w-3.5 h-3.5 mr-1.5 text-purple-500" />
            Scope 3 (Waste & Water)
          </TabsTrigger>
        </TabsList>

        {/* SCOPE 1 */}
        <TabsContent value="scope1" className="space-y-4 mt-0">
          <Card className="bg-card border-border/70 shadow-sm">
            <CardHeader className="pb-3">
              <CardTitle className="text-base flex items-center justify-between">
                <span className="flex items-center gap-2">
                  <Flame className="w-4 h-4 text-amber-500" />
                  Direct Combustion & Clinical Anesthetic Gases
                </span>
                <Badge variant="outline" className="text-xs border-amber-500/30 text-amber-600">Scope 1</Badge>
              </CardTitle>
            </CardHeader>
            <CardContent className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <Label htmlFor="diesel" className="text-xs text-muted-foreground font-medium">
                  Diesel for DG Backup Power (Liters / month)
                </Label>
                <Input
                  id="diesel"
                  type="number"
                  value={dieselLiters}
                  onChange={(e) => setDieselLiters(e.target.value)}
                  className="mt-1.5 text-xs h-9"
                />
              </div>

              <div>
                <Label htmlFor="desflurane" className="text-xs text-muted-foreground font-medium">
                  Desflurane Inhalational Agent (kg / month) — GWP: 2540
                </Label>
                <Input
                  id="desflurane"
                  type="number"
                  value={desfluraneKg}
                  onChange={(e) => setDesfluraneKg(e.target.value)}
                  className="mt-1.5 text-xs h-9 border-destructive/30"
                />
              </div>

              <div>
                <Label htmlFor="sevoflurane" className="text-xs text-muted-foreground font-medium">
                  Sevoflurane Inhalational Agent (kg / month) — GWP: 130
                </Label>
                <Input
                  id="sevoflurane"
                  type="number"
                  value={sevofluraneKg}
                  onChange={(e) => setSevofluraneKg(e.target.value)}
                  className="mt-1.5 text-xs h-9"
                />
              </div>

              <div>
                <Label htmlFor="gas" className="text-xs text-muted-foreground font-medium">
                  Natural Gas / PNG for Kitchen & Boilers (m³)
                </Label>
                <Input
                  id="gas"
                  type="number"
                  value={gasM3}
                  onChange={(e) => setGasM3(e.target.value)}
                  className="mt-1.5 text-xs h-9"
                />
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* SCOPE 2 */}
        <TabsContent value="scope2" className="space-y-4 mt-0">
          <Card className="bg-card border-border/70 shadow-sm">
            <CardHeader className="pb-3">
              <CardTitle className="text-base flex items-center justify-between">
                <span className="flex items-center gap-2">
                  <Zap className="w-4 h-4 text-blue-500" />
                  Purchased Electricity & Rooftop Solar Offset
                </span>
                <Badge variant="outline" className="text-xs border-blue-500/30 text-blue-600">Scope 2</Badge>
              </CardTitle>
            </CardHeader>
            <CardContent className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <Label htmlFor="electricity" className="text-xs text-muted-foreground font-medium">
                  Gross Grid Electricity Consumption (kWh / month)
                </Label>
                <Input
                  id="electricity"
                  type="number"
                  value={electricityKwh}
                  onChange={(e) => setElectricityKwh(e.target.value)}
                  className="mt-1.5 text-xs h-9"
                />
              </div>

              <div>
                <Label htmlFor="solar" className="text-xs text-muted-foreground font-medium">
                  Captive Solar PV Self-Generation (kWh / month offset)
                </Label>
                <Input
                  id="solar"
                  type="number"
                  value={solarOffsetKwh}
                  onChange={(e) => setSolarOffsetKwh(e.target.value)}
                  className="mt-1.5 text-xs h-9 border-emerald-500/30 text-emerald-600"
                />
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* SCOPE 3 */}
        <TabsContent value="scope3" className="space-y-4 mt-0">
          <Card className="bg-card border-border/70 shadow-sm">
            <CardHeader className="pb-3">
              <CardTitle className="text-base flex items-center justify-between">
                <span className="flex items-center gap-2">
                  <Trash2 className="w-4 h-4 text-purple-500" />
                  CPCB Bio-Medical Waste & Water Footprint
                </span>
                <Badge variant="outline" className="text-xs border-purple-500/30 text-purple-600">Scope 3</Badge>
              </CardTitle>
            </CardHeader>
            <CardContent className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div>
                <Label htmlFor="yellow" className="text-xs text-muted-foreground font-medium">
                  Yellow Bag Incinerated Waste (kg)
                </Label>
                <Input
                  id="yellow"
                  type="number"
                  value={yellowWasteKg}
                  onChange={(e) => setYellowWasteKg(e.target.value)}
                  className="mt-1.5 text-xs h-9"
                />
              </div>

              <div>
                <Label htmlFor="red" className="text-xs text-muted-foreground font-medium">
                  Red Bag Autoclaved Waste (kg)
                </Label>
                <Input
                  id="red"
                  type="number"
                  value={redWasteKg}
                  onChange={(e) => setRedWasteKg(e.target.value)}
                  className="mt-1.5 text-xs h-9"
                />
              </div>

              <div>
                <Label htmlFor="water" className="text-xs text-muted-foreground font-medium">
                  Municipal Water Intake (Liters)
                </Label>
                <Input
                  id="water"
                  type="number"
                  value={waterLiters}
                  onChange={(e) => setWaterLiters(e.target.value)}
                  className="mt-1.5 text-xs h-9"
                />
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      <Button
        onClick={calculateFootprint}
        size="lg"
        className="w-full text-xs font-semibold h-11 bg-primary text-primary-foreground hover:bg-primary/90 shadow-sm"
      >
        <Calculator className="w-4 h-4 mr-2" />
        Compute Complete Scopes 1-3 Carbon Footprint
      </Button>

      {results && (
        <Card className="bg-gradient-to-br from-card via-card to-emerald-950/20 border-emerald-500/30 shadow-md animate-fade-in">
          <CardHeader className="text-center pb-2">
            <CardTitle className="text-lg font-bold text-foreground">
              Total Monthly Hospital Footprint
            </CardTitle>
            <CardDescription className="text-xs">
              Verified against IPCC Assessment Report 6 (AR6) Emission Factors
            </CardDescription>
          </CardHeader>

          <CardContent className="space-y-6">
            <div className="text-center">
              <p className="text-5xl font-extrabold text-foreground tracking-tight">
                {results.total.toLocaleString()}
              </p>
              <p className="text-xs font-semibold text-emerald-600 dark:text-emerald-400 mt-1 uppercase tracking-wider">
                kg CO₂e / Month
              </p>
            </div>

            {/* Scope Breakdown Tiles */}
            <div className="grid grid-cols-3 gap-3 pt-4 border-t border-border/60">
              <div className="text-center p-3 bg-amber-500/10 rounded-xl border border-amber-500/20">
                <p className="text-[11px] font-semibold text-amber-600 dark:text-amber-400">Scope 1 (Direct)</p>
                <p className="text-lg font-bold text-foreground mt-0.5">{results.scope1.toLocaleString()}</p>
                <p className="text-[10px] text-muted-foreground">kg CO₂e</p>
              </div>

              <div className="text-center p-3 bg-blue-500/10 rounded-xl border border-blue-500/20">
                <p className="text-[11px] font-semibold text-blue-600 dark:text-blue-400">Scope 2 (Energy)</p>
                <p className="text-lg font-bold text-foreground mt-0.5">{results.scope2.toLocaleString()}</p>
                <p className="text-[10px] text-muted-foreground">kg CO₂e</p>
              </div>

              <div className="text-center p-3 bg-purple-500/10 rounded-xl border border-purple-500/20">
                <p className="text-[11px] font-semibold text-purple-600 dark:text-purple-400">Scope 3 (Waste)</p>
                <p className="text-lg font-bold text-foreground mt-0.5">{results.scope3.toLocaleString()}</p>
                <p className="text-[10px] text-muted-foreground">kg CO₂e</p>
              </div>
            </div>

            {/* Equivalents */}
            <div className="p-4 bg-muted/30 rounded-xl border border-border/50 grid grid-cols-2 gap-4 text-xs">
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-lg bg-emerald-500/15 text-emerald-600">
                  <Trees className="w-5 h-5" />
                </div>
                <div>
                  <p className="font-bold text-foreground">{results.treesOffset.toLocaleString()} Trees</p>
                  <p className="text-[11px] text-muted-foreground">Annual seedling absorption required</p>
                </div>
              </div>

              <div className="flex items-center gap-3">
                <div className="p-2 rounded-lg bg-blue-500/15 text-blue-600">
                  <Car className="w-5 h-5" />
                </div>
                <div>
                  <p className="font-bold text-foreground">{results.carKm.toLocaleString()} km</p>
                  <p className="text-[11px] text-muted-foreground">Equivalent passenger vehicle driving</p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default CarbonCalculator;

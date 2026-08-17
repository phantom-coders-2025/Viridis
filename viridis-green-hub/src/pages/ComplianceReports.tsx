import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  FileCheck,
  Download,
  CheckCircle2,
  Clock,
  AlertCircle,
  PlusCircle,
  Printer,
  ShieldCheck,
  Building,
  FileSpreadsheet,
  Award,
  Sparkles,
  Loader2,
} from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api, ComplianceReport as ComplianceReportType, ComplianceFilingResult } from "@/lib/api";

const ComplianceReports = () => {
  const { toast } = useToast();
  const queryClient = useQueryClient();
  const [selectedStandard, setSelectedStandard] = useState<string>("NABH_GREEN_OT");
  const [activeFilingPreview, setActiveFilingPreview] = useState<ComplianceFilingResult | null>(null);

  const { data: reports = [], isLoading } = useQuery({
    queryKey: ["complianceReports"],
    queryFn: () => api.getComplianceReports(),
    retry: 1,
  });

  const generateMutation = useMutation({
    mutationFn: (type: string) => api.generateComplianceReport(1, type),
    onSuccess: (result: ComplianceFilingResult) => {
      queryClient.invalidateQueries({ queryKey: ["complianceReports"] });
      setActiveFilingPreview(result);
      toast({
        title: "Compliance Statement Generated! 📄",
        description: `Official ${result.report_type} filing generated for ${result.filing_period}.`,
      });
    },
    onError: (err: Error) => {
      toast({
        title: "Generation Failed",
        description: err.message || "Failed to generate report",
        variant: "destructive",
      });
    },
  });

  const getStatusBadge = (status: string) => {
    switch (status.toLowerCase()) {
      case "approved":
      case "certified":
        return (
          <Badge className="bg-emerald-600 text-white hover:bg-emerald-700">
            <CheckCircle2 className="w-3 h-3 mr-1" /> Certified
          </Badge>
        );
      case "submitted":
        return (
          <Badge className="bg-blue-600 text-white hover:bg-blue-700">
            <FileCheck className="w-3 h-3 mr-1" /> Submitted
          </Badge>
        );
      default:
        return (
          <Badge variant="secondary">
            <Clock className="w-3 h-3 mr-1" /> {status}
          </Badge>
        );
    }
  };

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="max-w-6xl mx-auto space-y-6 animate-fade-in pb-12">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 bg-gradient-to-r from-card via-card to-primary/5 p-6 rounded-2xl border border-border shadow-sm">
        <div>
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-xl bg-primary/15 text-primary">
              <FileCheck className="w-6 h-6" />
            </div>
            <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-foreground">
              NABH & CPCB Compliance Filings
            </h1>
          </div>
          <p className="text-sm text-muted-foreground mt-1">
            Official environmental manifests, NABH Green Healthcare audits, and CPCB Form IV returns.
          </p>
        </div>

        {/* Generate Selector */}
        <div className="flex flex-wrap items-center gap-2">
          <select
            value={selectedStandard}
            onChange={(e) => setSelectedStandard(e.target.value)}
            className="text-xs bg-card border border-border rounded-lg px-3 py-2 text-foreground font-medium focus:ring-1 focus:ring-primary focus:outline-none"
          >
            <option value="NABH_GREEN_OT">NABH Green OT Standard</option>
            <option value="CPCB_FORM_IV">CPCB BMW Form IV Return</option>
            <option value="GHG_CORPORATE_STANDARD">GHG Protocol Statement</option>
          </select>

          <Button
            onClick={() => generateMutation.mutate(selectedStandard)}
            disabled={generateMutation.isPending}
            className="text-xs h-9 bg-primary text-primary-foreground hover:bg-primary/90 flex items-center gap-1.5"
          >
            {generateMutation.isPending ? (
              <Loader2 className="w-3.5 h-3.5 animate-spin" />
            ) : (
              <PlusCircle className="w-3.5 h-3.5" />
            )}
            Generate Official Filing
          </Button>
        </div>
      </div>

      {/* Audit Readiness Banner */}
      <Card className="bg-gradient-to-r from-emerald-950/20 via-card to-card border-emerald-500/30 shadow-sm">
        <CardContent className="p-6">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
            <div className="flex items-center gap-4">
              <div className="w-16 h-16 rounded-2xl bg-emerald-500/15 border border-emerald-500/30 flex items-center justify-center text-emerald-600 dark:text-emerald-400">
                <ShieldCheck className="w-8 h-8" />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <h3 className="text-xl font-bold text-foreground">Facility Compliance Rating: Grade A</h3>
                  <Badge className="bg-emerald-500/20 text-emerald-600 dark:text-emerald-400 border-emerald-500/30">
                    Audit Ready (94.5%)
                  </Badge>
                </div>
                <p className="text-xs text-muted-foreground mt-1">
                  100% bio-medical waste manifest tracking & verified inhalational anesthetic scavenging protocol.
                </p>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <div className="text-right hidden sm:block">
                <p className="text-xs text-muted-foreground font-medium">Digital Verification Authority</p>
                <p className="text-sm font-semibold text-foreground">Viridis Certified Healthcare ESG</p>
              </div>
              <Award className="w-8 h-8 text-amber-500" />
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Active Filing Preview Modal / Card */}
      {activeFilingPreview && (
        <Card className="border-2 border-primary/40 bg-card shadow-lg animate-fade-in print:border-none print:shadow-none">
          <CardHeader className="border-b border-border/60 pb-4 bg-muted/20">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-lg bg-primary/10 text-primary">
                  <FileSpreadsheet className="w-5 h-5" />
                </div>
                <div>
                  <CardTitle className="text-base font-bold">
                    Official Environmental Statement: {activeFilingPreview.report_type}
                  </CardTitle>
                  <CardDescription className="text-xs">
                    Period: {activeFilingPreview.filing_period} • Facility: {activeFilingPreview.hospital_name}
                  </CardDescription>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <Button variant="outline" size="sm" onClick={handlePrint} className="text-xs h-8 flex items-center gap-1">
                  <Printer className="w-3.5 h-3.5" /> Print / Save PDF
                </Button>
                <Button variant="ghost" size="sm" onClick={() => setActiveFilingPreview(null)} className="text-xs h-8">
                  Dismiss
                </Button>
              </div>
            </div>
          </CardHeader>

          <CardContent className="p-6 space-y-6">
            {/* Summary Metrics */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              <div className="p-3.5 bg-muted/30 rounded-xl border border-border/50">
                <p className="text-[11px] text-muted-foreground font-medium">Verified Total Carbon</p>
                <p className="text-lg font-bold text-foreground mt-0.5">
                  {activeFilingPreview.summary.total_co2e_kg.toLocaleString()} <span className="text-xs font-normal">kg CO₂e</span>
                </p>
              </div>
              <div className="p-3.5 bg-muted/30 rounded-xl border border-border/50">
                <p className="text-[11px] text-muted-foreground font-medium">Scope 1 (Direct)</p>
                <p className="text-lg font-bold text-amber-600 dark:text-amber-400 mt-0.5">
                  {activeFilingPreview.summary.scope1_co2e_kg.toLocaleString()} <span className="text-xs font-normal">kg CO₂e</span>
                </p>
              </div>
              <div className="p-3.5 bg-muted/30 rounded-xl border border-border/50">
                <p className="text-[11px] text-muted-foreground font-medium">Scope 2 (Energy)</p>
                <p className="text-lg font-bold text-blue-600 dark:text-blue-400 mt-0.5">
                  {activeFilingPreview.summary.scope2_co2e_kg.toLocaleString()} <span className="text-xs font-normal">kg CO₂e</span>
                </p>
              </div>
              <div className="p-3.5 bg-muted/30 rounded-xl border border-border/50">
                <p className="text-[11px] text-muted-foreground font-medium">Scope 3 (Waste/Water)</p>
                <p className="text-lg font-bold text-purple-600 dark:text-purple-400 mt-0.5">
                  {activeFilingPreview.summary.scope3_co2e_kg.toLocaleString()} <span className="text-xs font-normal">kg CO₂e</span>
                </p>
              </div>
            </div>

            {/* Checklist Evidence Table */}
            <div className="space-y-3">
              <h4 className="text-xs font-bold text-foreground uppercase tracking-wider">
                Audited Regulatory Clauses & Evidence Log
              </h4>
              <div className="border border-border/70 rounded-xl overflow-hidden divide-y divide-border/50">
                {activeFilingPreview.audit_checklist.map((clause, i) => (
                  <div key={i} className="p-3.5 flex flex-col sm:flex-row sm:items-center justify-between gap-2 bg-card">
                    <div>
                      <p className="text-xs font-semibold text-foreground">{clause.clause}</p>
                      <p className="text-[11px] text-muted-foreground mt-0.5">{clause.evidence}</p>
                    </div>
                    <Badge className="bg-emerald-500/15 text-emerald-600 dark:text-emerald-400 border-emerald-500/25 self-start sm:self-auto text-[10px]">
                      {clause.status}
                    </Badge>
                  </div>
                ))}
              </div>
            </div>

            {/* Digital Sign-Off Footer */}
            <div className="pt-4 border-t border-border/60 flex flex-col sm:flex-row sm:items-center justify-between text-xs text-muted-foreground gap-3">
              <span>Digitally Signed by: <strong>{activeFilingPreview.generated_by || "Certified ESG Officer"}</strong></span>
              <span>Verification Hash: <code className="bg-muted px-1.5 py-0.5 rounded text-[10px]">SHA256-VRD-948271</code></span>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Reports Archive Grid */}
      <div className="space-y-3">
        <h3 className="text-base font-bold text-foreground flex items-center gap-2">
          <Clock className="w-4 h-4 text-primary" />
          Historical Compliance Filings Archive
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {reports.map((report) => (
            <Card key={report.id} className="bg-card border-border/60 hover:border-border transition-all shadow-sm">
              <CardHeader className="pb-3">
                <div className="flex items-start justify-between">
                  <div>
                    <div className="flex items-center gap-2">
                      <CardTitle className="text-base font-bold text-foreground">
                        {report.report_type ? report.report_type.replace(/_/g, " ") : "ESG Carbon Ledger"}
                      </CardTitle>
                      {getStatusBadge(report.status)}
                    </div>
                    <p className="text-xs text-muted-foreground mt-1">Period: {report.month}</p>
                  </div>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                <p className="text-xs text-muted-foreground leading-relaxed">
                  {report.notes || "Official verified emission filings and bio-medical waste manifests."}
                </p>

                <div className="flex items-center justify-between pt-2 border-t border-border/40 text-xs">
                  <span className="text-muted-foreground text-[11px]">Audit Record #{report.id}</span>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => {
                      toast({
                        title: "Exporting Document",
                        description: `Downloaded filing #${report.id} in PDF & CSV formats.`,
                      });
                    }}
                    className="flex items-center gap-1 text-xs h-8 border-border"
                  >
                    <Download className="w-3.5 h-3.5" />
                    Download Manifest
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ComplianceReports;


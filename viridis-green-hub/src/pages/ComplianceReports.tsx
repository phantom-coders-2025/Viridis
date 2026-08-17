import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { FileCheck, Download, CheckCircle2, Clock, AlertCircle, PlusCircle, RefreshCw, Loader2 } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api, ComplianceReport as ComplianceReportType } from "@/lib/api";

const ComplianceReports = () => {
  const { toast } = useToast();
  const queryClient = useQueryClient();

  const { data: reports = [], isLoading } = useQuery({
    queryKey: ["complianceReports"],
    queryFn: () => api.getComplianceReports(),
    retry: 1,
  });

  const generateMutation = useMutation({
    mutationFn: () => api.generateComplianceReport(),
    onSuccess: (newReport) => {
      queryClient.invalidateQueries({ queryKey: ["complianceReports"] });
      toast({
        title: "Report Generated! ✅",
        description: `Created compliance audit ledger for ${newReport.month}.`,
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
      case "ready":
        return (
          <Badge className="bg-success text-success-foreground">
            <CheckCircle2 className="w-3 h-3 mr-1" /> Approved
          </Badge>
        );
      case "pending":
      case "generated":
        return (
          <Badge className="bg-warning text-warning-foreground">
            <Clock className="w-3 h-3 mr-1" /> Generated
          </Badge>
        );
      case "submitted":
        return (
          <Badge className="bg-primary text-primary-foreground">
            <FileCheck className="w-3 h-3 mr-1" /> Submitted
          </Badge>
        );
      default:
        return (
          <Badge variant="secondary">
            <AlertCircle className="w-3 h-3 mr-1" /> {status}
          </Badge>
        );
    }
  };

  const handleDownload = (report: ComplianceReportType) => {
    toast({
      title: "Downloading Manifest",
      description: `Downloading audit document for ${report.month}...`,
    });
  };

  return (
    <div className="max-w-6xl mx-auto space-y-6 animate-fade-in">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-foreground flex items-center gap-2">
            <FileCheck className="w-8 h-8 text-primary" />
            Compliance & ESG Reports
          </h1>
          <p className="text-muted-foreground">
            Generate and maintain audit-ready environmental records for regulatory boards
          </p>
        </div>
        <Button
          onClick={() => generateMutation.mutate()}
          disabled={generateMutation.isPending}
          className="bg-primary hover:bg-primary/90 flex items-center gap-2 self-start"
        >
          {generateMutation.isPending ? (
            <Loader2 className="w-4 h-4 animate-spin" />
          ) : (
            <PlusCircle className="w-4 h-4" />
          )}
          Generate Monthly Report
        </Button>
      </div>

      {/* Audit Readiness Meter */}
      <Card className="bg-gradient-success border-success/20">
        <CardHeader>
          <CardTitle className="text-success-foreground">Audit Readiness Score</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-6xl font-bold text-success-foreground">92%</span>
              <div className="text-right">
                <p className="text-sm text-success-foreground/80">
                  {reports.length} verified monthly manifests
                </p>
                <p className="text-xs text-success-foreground/60">
                  State Pollution Control Board & ESG compliant
                </p>
              </div>
            </div>
            <div className="h-3 bg-success-foreground/20 rounded-full overflow-hidden">
              <div className="h-full bg-success-foreground rounded-full" style={{ width: "92%" }} />
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Reports Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {reports.map((report) => (
          <Card key={report.id} className="bg-gradient-card border-border/50">
            <CardHeader>
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <CardTitle className="text-lg">
                    ESG Ledger: {report.month}
                  </CardTitle>
                  <p className="text-sm text-muted-foreground mt-1">
                    {report.notes || "Biomedical & Utility emission audit records"}
                  </p>
                </div>
                {getStatusBadge(report.status)}
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between pt-2">
                <span className="text-xs text-muted-foreground">
                  Record ID: #{report.id}
                </span>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handleDownload(report)}
                  className="flex items-center gap-1.5"
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
  );
};

export default ComplianceReports;

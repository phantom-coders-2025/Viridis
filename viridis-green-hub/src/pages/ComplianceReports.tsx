import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { FileCheck, Download, CheckCircle2, Clock, AlertCircle } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

const ComplianceReports = () => {
  const { toast } = useToast();

  const reports = [
    {
      name: "CPCB Compliance",
      description: "Central Pollution Control Board reporting",
      status: "ready",
      lastGenerated: "2024-03-15"
    },
    {
      name: "NABH Standards",
      description: "National Accreditation Board for Hospitals",
      status: "ready",
      lastGenerated: "2024-03-10"
    },
    {
      name: "IGBC Green Hospital",
      description: "Indian Green Building Council certification",
      status: "pending",
      lastGenerated: null
    },
    {
      name: "ESG Reporting",
      description: "Environmental, Social, and Governance metrics",
      status: "submitted",
      lastGenerated: "2024-02-28"
    }
  ];

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "ready":
        return <Badge className="bg-success text-success-foreground"><CheckCircle2 className="w-3 h-3 mr-1" /> Ready</Badge>;
      case "pending":
        return <Badge className="bg-warning text-warning-foreground"><Clock className="w-3 h-3 mr-1" /> Pending</Badge>;
      case "submitted":
        return <Badge className="bg-primary text-primary-foreground"><FileCheck className="w-3 h-3 mr-1" /> Submitted</Badge>;
      default:
        return <Badge variant="secondary"><AlertCircle className="w-3 h-3 mr-1" /> Unknown</Badge>;
    }
  };

  const handleGenerateReport = (reportName: string) => {
    toast({
      title: "Generating Report",
      description: `${reportName} is being prepared for download...`,
    });
    
    setTimeout(() => {
      toast({
        title: "Report Ready",
        description: `${reportName} has been generated successfully`,
      });
    }, 2000);
  };

  return (
    <div className="max-w-6xl mx-auto space-y-6 animate-fade-in">
      <div>
        <h1 className="text-3xl font-bold text-foreground flex items-center gap-2">
          <FileCheck className="w-8 h-8 text-primary" />
          Compliance Reports
        </h1>
        <p className="text-muted-foreground">Generate audit-ready reports for regulatory compliance</p>
      </div>

      {/* Audit Readiness Meter */}
      <Card className="bg-gradient-success border-success/20">
        <CardHeader>
          <CardTitle className="text-success-foreground">Audit Readiness Score</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-6xl font-bold text-success-foreground">85%</span>
              <div className="text-right">
                <p className="text-sm text-success-foreground/80">3 of 4 reports ready</p>
                <p className="text-xs text-success-foreground/60">Last updated: March 15, 2024</p>
              </div>
            </div>
            <div className="h-3 bg-success-foreground/20 rounded-full overflow-hidden">
              <div className="h-full bg-success-foreground rounded-full" style={{ width: '85%' }} />
            </div>
            <p className="text-sm text-success-foreground/80 text-center">
              You're well-prepared for compliance audits
            </p>
          </div>
        </CardContent>
      </Card>

      {/* Reports Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {reports.map((report) => (
          <Card key={report.name} className="bg-gradient-card border-border/50">
            <CardHeader>
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <CardTitle className="text-lg">{report.name}</CardTitle>
                  <p className="text-sm text-muted-foreground mt-1">{report.description}</p>
                </div>
                {getStatusBadge(report.status)}
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              {report.lastGenerated && (
                <p className="text-xs text-muted-foreground">
                  Last generated: {new Date(report.lastGenerated).toLocaleDateString()}
                </p>
              )}
              
              <div className="flex gap-2">
                <Button 
                  onClick={() => handleGenerateReport(report.name)}
                  className="flex-1 bg-primary hover:bg-primary/90"
                  disabled={report.status === "pending"}
                >
                  Generate Report
                </Button>
                {report.status === "ready" && (
                  <Button 
                    variant="outline" 
                    size="icon"
                    onClick={() => toast({
                      title: "Downloading",
                      description: `${report.name} PDF is downloading...`
                    })}
                  >
                    <Download className="w-4 h-4" />
                  </Button>
                )}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Document Upload Section */}
      <Card className="bg-gradient-card border-border/50">
        <CardHeader>
          <CardTitle>Supporting Documents</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            <div className="flex items-center justify-between p-3 bg-muted/30 rounded-lg">
              <div className="flex items-center gap-3">
                <FileCheck className="w-5 h-5 text-primary" />
                <div>
                  <p className="text-sm font-medium text-foreground">Energy Bills (Q1 2024)</p>
                  <p className="text-xs text-muted-foreground">Uploaded on March 1, 2024</p>
                </div>
              </div>
              <Badge variant="secondary">Verified</Badge>
            </div>
            
            <div className="flex items-center justify-between p-3 bg-muted/30 rounded-lg">
              <div className="flex items-center gap-3">
                <FileCheck className="w-5 h-5 text-primary" />
                <div>
                  <p className="text-sm font-medium text-foreground">Waste Management Records</p>
                  <p className="text-xs text-muted-foreground">Uploaded on February 28, 2024</p>
                </div>
              </div>
              <Badge variant="secondary">Verified</Badge>
            </div>

            <Button variant="outline" className="w-full mt-2">
              Upload Additional Documents
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Compliance Checklist */}
      <Card className="bg-gradient-card border-border/50">
        <CardHeader>
          <CardTitle>Compliance Checklist</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            {[
              { item: "Monthly emissions data recorded", done: true },
              { item: "Waste segregation protocols documented", done: true },
              { item: "Staff training certifications up to date", done: true },
              { item: "Energy audit completed this quarter", done: false },
              { item: "Water quality reports submitted", done: true },
            ].map((check, i) => (
              <div key={i} className="flex items-center gap-3 p-3 bg-muted/20 rounded-lg">
                {check.done ? (
                  <CheckCircle2 className="w-5 h-5 text-success" />
                ) : (
                  <Clock className="w-5 h-5 text-warning" />
                )}
                <span className={check.done ? "text-foreground" : "text-muted-foreground"}>
                  {check.item}
                </span>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default ComplianceReports;

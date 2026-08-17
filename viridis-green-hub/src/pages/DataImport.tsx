import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import {
  Upload,
  FileSpreadsheet,
  CheckCircle2,
  Download,
  Loader2,
  AlertCircle,
} from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";

const DataImport = () => {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState<{ rows: number; message: string } | null>(null);
  const { toast } = useToast();
  const queryClient = useQueryClient();

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      const validExtensions = [".csv", ".xlsx", ".xls"];
      const isSpreadsheet = validExtensions.some((ext) =>
        selectedFile.name.toLowerCase().endsWith(ext)
      );

      if (isSpreadsheet) {
        setFile(selectedFile);
        setUploadResult(null);
        toast({
          title: "File Selected",
          description: `${selectedFile.name} is ready for upload`,
        });
      } else {
        toast({
          title: "Invalid File Type",
          description: "Please upload a CSV or Excel spreadsheet (.csv, .xlsx, .xls)",
          variant: "destructive",
        });
      }
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setUploading(true);

    try {
      const res = await api.uploadEmissionsCSV(file);
      setUploadResult({ rows: res.rows, message: res.message });
      queryClient.invalidateQueries({ queryKey: ["dashboardOverview"] });
      queryClient.invalidateQueries({ queryKey: ["aiInsights"] });
      queryClient.invalidateQueries({ queryKey: ["sustainabilityScore"] });

      toast({
        title: "Data Import Successful! 🎉",
        description: `Imported ${res.rows} records into the hospital database.`,
      });
    } catch (err: unknown) {
      const errorMsg = err instanceof Error ? err.message : "Failed to upload and parse file";
      toast({
        title: "Import Failed",
        description: errorMsg,
        variant: "destructive",
      });
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 animate-fade-in">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Data Import</h1>
          <p className="text-muted-foreground">
            Upload hospital utility and waste manifests into the live Viridis telemetry engine
          </p>
        </div>
        <a
          href="/sample_emissions_template.csv"
          download="viridis_hospital_template.csv"
          className="self-start"
        >
          <Button variant="outline" size="sm" className="flex items-center gap-2">
            <Download className="w-4 h-4" />
            Download Sample CSV
          </Button>
        </a>
      </div>

      {/* Upload Section */}
      {!uploadResult ? (
        <Card className="bg-gradient-card border-border/50">
          <CardHeader>
            <CardTitle>Upload Monthly Spreadsheet</CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="border-2 border-dashed border-border rounded-lg p-10 text-center hover:border-primary/50 transition-colors">
              <input
                type="file"
                accept=".csv,.xlsx,.xls"
                onChange={handleFileChange}
                className="hidden"
                id="file-upload"
              />
              <label htmlFor="file-upload" className="cursor-pointer">
                <div className="flex flex-col items-center gap-3">
                  <Upload className="w-14 h-14 text-muted-foreground" />
                  <div>
                    <p className="text-lg font-medium text-foreground">
                      {file ? file.name : "Drop your hospital spreadsheet here or click to browse"}
                    </p>
                    <p className="text-sm text-muted-foreground mt-1">
                      Supports CSV and Excel files (Wide departmental logs & row-by-row)
                    </p>
                  </div>
                </div>
              </label>
            </div>

            {file && (
              <div className="flex items-center justify-between p-4 bg-muted/30 rounded-lg">
                <div className="flex items-center gap-3">
                  <FileSpreadsheet className="w-8 h-8 text-primary" />
                  <div>
                    <p className="font-medium text-foreground">{file.name}</p>
                    <p className="text-sm text-muted-foreground">
                      {(file.size / 1024).toFixed(1)} KB
                    </p>
                  </div>
                </div>
                <Button
                  onClick={handleUpload}
                  disabled={uploading}
                  className="bg-primary hover:bg-primary/90"
                >
                  {uploading ? (
                    <>
                      <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                      Parsing & Ingesting...
                    </>
                  ) : (
                    "Upload & Process"
                  )}
                </Button>
              </div>
            )}

            <div className="space-y-2">
              <p className="text-sm font-medium text-foreground">
                Supported Column Headers (Wide or Standard):
              </p>
              <div className="bg-muted/30 rounded-lg p-4 text-xs font-mono">
                <div className="grid grid-cols-1 sm:grid-cols-4 gap-2 text-muted-foreground">
                  <span>Department</span>
                  <span>Electricity (kWh)</span>
                  <span>Water (L)</span>
                  <span>Biomedical Waste (kg)</span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      ) : (
        <Card className="bg-gradient-success border-success/20 animate-scale-in">
          <CardContent className="pt-6">
            <div className="text-center space-y-6">
              <CheckCircle2 className="w-20 h-20 text-success-foreground mx-auto" />
              <div>
                <h3 className="text-2xl font-bold text-success-foreground">
                  Import Successfully Processed!
                </h3>
                <p className="text-success-foreground/80 mt-2">
                  {uploadResult.message}
                </p>
              </div>

              <div className="flex gap-4 justify-center">
                <Button
                  onClick={() => (window.location.href = "/dashboard")}
                  className="bg-success-foreground/90 text-success hover:bg-success-foreground"
                >
                  View Dashboard
                </Button>
                <Button
                  variant="outline"
                  onClick={() => {
                    setFile(null);
                    setUploadResult(null);
                  }}
                  className="bg-success-foreground/90 text-success hover:bg-success-foreground"
                >
                  Upload Another File
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default DataImport;

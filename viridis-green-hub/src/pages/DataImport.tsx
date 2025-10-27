import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import {
  Upload,
  FileSpreadsheet,
  CheckCircle2,
  AlertCircle,
  Eye,
  Trash2,
} from "lucide-react";
import { useToast } from "@/hooks/use-toast";

interface UploadedFile {
  name: string;
  size: number;
  type: string;
  url: string;
  uploadedAt: string;
}

const DataImport = () => {
  const [file, setFile] = useState<File | null>(null);
  const [uploaded, setUploaded] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([]);
  const { toast } = useToast();

  // ✅ Load uploaded files from localStorage
  useEffect(() => {
    const saved = localStorage.getItem("uploadedFiles");
    if (saved) {
      try {
        setUploadedFiles(JSON.parse(saved));
      } catch {
        console.error("Error parsing saved uploadedFiles");
      }
    }
  }, []);

  // ✅ Save uploaded files to localStorage
  useEffect(() => {
    localStorage.setItem("uploadedFiles", JSON.stringify(uploadedFiles));
  }, [uploadedFiles]);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      const validTypes = [
        "text/csv",
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
      ];
      if (validTypes.includes(selectedFile.type)) {
        setFile(selectedFile);
        toast({
          title: "File Selected",
          description: `${selectedFile.name} is ready for upload`,
        });
      } else {
        toast({
          title: "Invalid File Type",
          description: "Please upload a CSV or Excel file",
          variant: "destructive",
        });
      }
    }
  };

  const handleUpload = () => {
    if (file) {
      setTimeout(() => {
        const newFile: UploadedFile = {
          name: file.name,
          size: file.size,
          type: file.type,
          url: URL.createObjectURL(file),
          uploadedAt: new Date().toLocaleString(),
        };

        setUploadedFiles((prev) => [...prev, newFile]);
        setUploaded(true);
        toast({
          title: "Upload Complete ✅",
          description: "Your data has been successfully imported and saved locally",
        });
      }, 1500);
    }
  };

  const handleViewFile = (file: UploadedFile) => {
    window.open(file.url, "_blank");
  };

  const handleDeleteFile = (fileName: string) => {
    const updated = uploadedFiles.filter((f) => f.name !== fileName);
    setUploadedFiles(updated);
    toast({
      title: "File Removed",
      description: `${fileName} has been deleted from history`,
      variant: "destructive",
    });
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 animate-fade-in">
      <div>
        <h1 className="text-3xl font-bold text-foreground">Data Import</h1>
        <p className="text-muted-foreground">
          Upload and manage your hospital's sustainability data
        </p>
      </div>

      {/* Upload Section */}
      {!uploaded ? (
        <Card className="bg-gradient-card border-border/50">
          <CardHeader>
            <CardTitle>Upload CSV or Excel File</CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="border-2 border-dashed border-border rounded-lg p-12 text-center hover:border-primary/50 transition-colors">
              <input
                type="file"
                accept=".csv,.xlsx,.xls"
                onChange={handleFileChange}
                className="hidden"
                id="file-upload"
              />
              <label htmlFor="file-upload" className="cursor-pointer">
                <div className="flex flex-col items-center gap-4">
                  <Upload className="w-16 h-16 text-muted-foreground" />
                  <div>
                    <p className="text-lg font-medium text-foreground">
                      {file ? file.name : "Drop your file here or click to browse"}
                    </p>
                    <p className="text-sm text-muted-foreground mt-1">
                      Supports CSV and Excel files (max 10MB)
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
                      {(file.size / 1024).toFixed(2)} KB
                    </p>
                  </div>
                </div>
                <Button onClick={handleUpload} className="bg-primary hover:bg-primary/90">
                  Upload File
                </Button>
              </div>
            )}

            <div className="space-y-2">
              <p className="text-sm font-medium text-foreground">Required Data Format:</p>
              <div className="bg-muted/30 rounded-lg p-4 text-xs font-mono">
                <div className="grid grid-cols-4 gap-2 text-muted-foreground">
                  <span>Department</span>
                  <span>Electricity (kWh)</span>
                  <span>Water (L)</span>
                  <span>Waste (kg)</span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      ) : (
        <Card className="bg-gradient-success border-success/20 animate-scale-in">
          <CardContent className="pt-6">
            <div className="text-center space-y-6">
              <CheckCircle2 className="w-24 h-24 text-success-foreground mx-auto" />
              <div>
                <h3 className="text-2xl font-bold text-success-foreground">
                  Upload Complete!
                </h3>
                <p className="text-success-foreground/80 mt-2">
                  Your data has been successfully imported and stored locally
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
                    setUploaded(false);
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

      {/* File History Section */}
      {uploadedFiles.length > 0 && (
        <Card className="bg-gradient-card border-border/50">
          <CardHeader>
            <CardTitle className="text-lg font-semibold">Previously Uploaded Files</CardTitle>
          </CardHeader>

          <CardContent className="grid grid-cols-1 sm:grid-cols-2 gap-6">
            {uploadedFiles.map((f, index) => (
              <div
                key={index}
                className="relative bg-muted/40 rounded-xl border border-border/40 p-5 hover:shadow-lg hover:border-primary/50 transition-all"
              >
                {/* Delete Button inside the card */}
                <button
                  onClick={() => handleDeleteFile(f.name)}
                  className="absolute top-2 right-2 text-destructive hover:text-destructive/80 transition-colors"
                  title="Delete File"
                >
                  <Trash2 className="w-4 h-4" />
                </button>

                <div
                  className="flex flex-col items-center gap-3 text-center cursor-pointer"
                  onClick={() => handleViewFile(f)}
                >
                  <FileSpreadsheet className="w-10 h-10 text-primary" />
                  <div className="space-y-1">
                    <p className="font-medium text-foreground truncate w-48 mx-auto">
                      {f.name}
                    </p>
                    <p className="text-xs text-muted-foreground">
                      {(f.size / 1024).toFixed(1)} KB
                    </p>
                    <p className="text-xs text-muted-foreground">
                      {new Date(f.uploadedAt).toLocaleDateString()}
                    </p>
                  </div>

                  <Button
                    variant="outline"
                    size="sm"
                    className="mt-2 border-primary/40 text-primary hover:bg-primary/10"
                  >
                    <Eye className="w-4 h-4 mr-1" /> View File
                  </Button>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default DataImport;

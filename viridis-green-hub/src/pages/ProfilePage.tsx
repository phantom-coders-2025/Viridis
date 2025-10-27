// src/pages/ProfilePage.tsx
import { useState, useEffect } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { useToast } from "@/hooks/use-toast";
import { useNavigate } from "react-router-dom";

const ProfilePage = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  const [profile, setProfile] = useState<any>(null);
  const [passwords, setPasswords] = useState({ old: "", new: "", confirm: "" });

  useEffect(() => {
    const data = localStorage.getItem("hospitalProfile");
    if (data) setProfile(JSON.parse(data));
  }, []);

  const handlePasswordChange = (e: React.FormEvent) => {
    e.preventDefault();
    if (passwords.new !== passwords.confirm) {
      toast({
        title: "Password Mismatch",
        description: "New passwords do not match.",
        variant: "destructive",
      });
      return;
    }
    toast({
      title: "Password Updated",
      description: "Your password has been successfully changed.",
    });
    setPasswords({ old: "", new: "", confirm: "" });
  };

  if (!profile)
    return <p className="text-center mt-10 text-muted-foreground">Loading profile...</p>;

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-emerald-50 to-white p-6">
      <Card className="w-full max-w-3xl shadow-lg border-border/40">
        <CardHeader>
          <CardTitle className="text-2xl font-bold text-center text-emerald-600">
            Hospital Profile
          </CardTitle>
        </CardHeader>

        <CardContent className="space-y-8">
          {/* Profile Info */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <Label>Name</Label>
              <Input value={profile.hospitalName} disabled />
            </div>
            <div>
              <Label>Registration ID</Label>
              <Input value={profile.registrationId} disabled />
            </div>
            <div>
              <Label>Type</Label>
              <Input value={profile.hospitalType} disabled />
            </div>
            <div>
              <Label>Location</Label>
              <Input value={profile.location} disabled />
            </div>
            <div>
              <Label>Email</Label>
              <Input value={profile.email} disabled />
            </div>
            <div>
              <Label>Phone</Label>
              <Input value={profile.phone} disabled />
            </div>
          </div>

          {/* Change Password */}
          <div className="pt-6 border-t border-border/50 space-y-4">
            <h3 className="font-semibold text-lg text-foreground">
              Change Password
            </h3>
            <form onSubmit={handlePasswordChange} className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <Input
                type="password"
                placeholder="Old password"
                value={passwords.old}
                onChange={(e) => setPasswords({ ...passwords, old: e.target.value })}
                required
              />
              <Input
                type="password"
                placeholder="New password"
                value={passwords.new}
                onChange={(e) => setPasswords({ ...passwords, new: e.target.value })}
                required
              />
              <Input
                type="password"
                placeholder="Confirm new password"
                value={passwords.confirm}
                onChange={(e) => setPasswords({ ...passwords, confirm: e.target.value })}
                required
              />
              <div className="md:col-span-3 flex justify-end">
                <Button type="submit" className="bg-emerald-500 hover:bg-emerald-600 text-white">
                  Update Password
                </Button>
              </div>
            </form>
          </div>

          {/* Back to Dashboard */}
          <div className="text-center">
            <Button
              variant="outline"
              onClick={() => navigate("/dashboard")}
              className="mt-4 border-emerald-500 text-emerald-600 hover:bg-emerald-50"
            >
              ← Back to Dashboard
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default ProfilePage;

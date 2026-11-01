"use client";

import * as React from "react";
import { useRouter } from "next/navigation";
import {
  Cpu,
  Lock,
  User as UserIcon,
  Eye,
  EyeOff,
  ArrowRight,
  ShieldAlert,
  UserCheck,
  Sun,
  Moon,
  AlertCircle,
} from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { useAuth } from "@/components/auth-provider";
import { checkBackendConnection, BACKEND_BASE_URL } from "@/lib/api/backend-client";
import { useTheme } from "@/components/theme-provider";

const QUICK_LOGIN_PRESETS = [
  {
    name: "Director Elena Rostova",
    username: "director",
    password: "admin123",
    role: "City Manager",
    department: "Executive Directorate",
    initials: "ER",
  },
  {
    name: "Supervisor Marcus Vance",
    username: "supervisor",
    password: "super123",
    role: "Supervisor",
    department: "Urban Grid Oversight",
    initials: "MV",
  },
  {
    name: "Officer Sarah Jenkins",
    username: "staff",
    password: "staff123",
    role: "Local Staff",
    department: "Central Response Team",
    initials: "SJ",
  },
  {
    name: "Dr. Evelyn Reed",
    username: "citizen",
    password: "citizen123",
    role: "Citizen",
    department: "Civil Engineering Union",
    initials: "ER",
  },
];

export default function LoginPage() {
  const router = useRouter();
  const { login } = useAuth();
  const { theme, toggleTheme, mounted } = useTheme();

  const [identifier, setIdentifier] = React.useState("director");
  const [password, setPassword] = React.useState("admin123");
  const [showPassword, setShowPassword] = React.useState(false);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  const [backendOnline, setBackendOnline] = React.useState<boolean | null>(null);

  React.useEffect(() => {
    checkBackendConnection().then((online) => setBackendOnline(online));
  }, []);

  const handleLogin = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!identifier.trim() || !password) {
      setError("Please enter your username/email and password.");
      return;
    }

    setLoading(true);
    setError(null);
    try {
      await login(identifier, password);
      router.push("/");
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Login failed. Check your credentials.");
      }
    } finally {
      setLoading(false);
    }
  };

  const handleQuickLogin = async (preset: (typeof QUICK_LOGIN_PRESETS)[number]) => {
    setIdentifier(preset.username);
    setPassword(preset.password);
    setLoading(true);
    setError(null);
    try {
      await login(preset.username, preset.password);
      router.push("/");
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Failed to sign in with demo credentials.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col justify-center items-center p-4 relative bg-slate-50 dark:bg-[#080d1a] transition-colors duration-200">
      {/* Top Bar: Theme Switcher */}
      <div className="absolute top-4 right-4 flex items-center gap-2">
        <button
          onClick={toggleTheme}
          className="flex h-9 w-9 items-center justify-center rounded-xl border border-slate-200 dark:border-slate-800 bg-white/80 dark:bg-slate-900/80 text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors shadow-xs"
          title={`Switch to ${mounted && theme === "light" ? "Dark" : "Light"} Mode`}
        >
          {mounted && theme === "dark" ? (
            <Sun className="h-4 w-4 text-amber-400" />
          ) : (
            <Moon className="h-4 w-4 text-slate-700" />
          )}
        </button>
      </div>

      <div className="w-full max-w-md space-y-6">
        {/* Header Branding */}
        <div className="text-center space-y-2">
          <div className="inline-flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br from-cyan-500 to-blue-600 shadow-md shadow-cyan-500/20 text-white mb-2">
            <Cpu className="h-6 w-6" />
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-white">
            SmartCity<span className="text-cyan-600 dark:text-cyan-400">360</span>
          </h1>
          <p className="text-xs text-slate-500 dark:text-slate-400">
            Municipal Operations &amp; Real Telemetry Management
          </p>

          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-[11px] font-medium border border-slate-200 dark:border-slate-800 bg-white/80 dark:bg-slate-900/70">
            <span
              className={`h-2 w-2 rounded-full ${
                backendOnline ? "bg-emerald-500" : "bg-rose-500 animate-pulse"
              }`}
            />
            <span className="text-slate-600 dark:text-slate-300 font-mono text-[10px]">
              {backendOnline === null
                ? "Checking Tomcat backend..."
                : backendOnline
                ? "MySQL Backend: CONNECTED (Tomcat 9)"
                : "MySQL Backend: OFFLINE (Requires Tomcat 9)"}
            </span>
          </div>
        </div>

        {/* Backend Offline Warning Banner if Tomcat not running */}
        {backendOnline === false && (
          <div className="rounded-xl border border-rose-300 dark:border-rose-900/50 bg-rose-50 dark:bg-rose-950/40 p-3 text-xs text-rose-800 dark:text-rose-200 space-y-1 shadow-xs">
            <div className="flex items-center gap-1.5 font-bold">
              <AlertCircle className="h-4 w-4 text-rose-600 shrink-0" />
              <span>Backend Required for Real Authentication</span>
            </div>
            <p className="text-[11px] text-rose-700/90 dark:text-rose-300/80 leading-relaxed">
              Real login queries the MySQL database directly. Please start Apache Tomcat 9 in IntelliJ IDEA to connect to <code className="bg-rose-100 dark:bg-rose-900/60 px-1 py-0.5 rounded text-[10px]">{BACKEND_BASE_URL}</code>.
            </p>
          </div>
        )}

        {/* Main Login Card */}
        <Card className="border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/80 shadow-md backdrop-blur-sm">
          <CardHeader className="pb-3">
            <CardTitle className="text-base text-slate-900 dark:text-white">
              Municipal Portal Sign In
            </CardTitle>
            <CardDescription className="text-xs">
              Authenticates directly against MySQL <code className="text-slate-600 dark:text-slate-300">smartcity360_db.users</code>
            </CardDescription>
          </CardHeader>

          <CardContent className="space-y-4">
            {error && (
              <div className="flex items-center gap-2 p-3 rounded-xl border border-rose-300 dark:border-rose-900/50 bg-rose-50 dark:bg-rose-950/30 text-rose-800 dark:text-rose-200 text-xs">
                <ShieldAlert className="h-4 w-4 shrink-0 text-rose-600 dark:text-rose-400" />
                <span>{error}</span>
              </div>
            )}

            <form onSubmit={handleLogin} className="space-y-3.5">
              <div className="space-y-1.5">
                <label className="text-xs font-semibold text-slate-700 dark:text-slate-300">
                  Username or Official Email
                </label>
                <div className="relative">
                  <UserIcon className="absolute left-3 top-2.5 h-4 w-4 text-slate-400" />
                  <Input
                    type="text"
                    placeholder="e.g. director or director@smartcity360.gov"
                    value={identifier}
                    onChange={(e) => setIdentifier(e.target.value)}
                    className="pl-9 text-xs h-9"
                    required
                  />
                </div>
              </div>

              <div className="space-y-1.5">
                <label className="text-xs font-semibold text-slate-700 dark:text-slate-300">
                  Password
                </label>
                <div className="relative">
                  <Lock className="absolute left-3 top-2.5 h-4 w-4 text-slate-400" />
                  <Input
                    type={showPassword ? "text" : "password"}
                    placeholder="Enter password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="pl-9 pr-9 text-xs h-9"
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-2.5 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200"
                  >
                    {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                  </button>
                </div>
              </div>

              <Button
                type="submit"
                disabled={loading}
                className="w-full gap-2 text-xs font-semibold h-9 shadow-sm"
              >
                <span>{loading ? "Authenticating via Tomcat..." : "Sign In to Operations"}</span>
                <ArrowRight className="h-4 w-4" />
              </Button>
            </form>

            {/* Quick Login for VIVA Examination */}
            <div className="pt-2 border-t border-slate-200 dark:border-slate-800 space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-semibold text-amber-800 dark:text-amber-400 flex items-center gap-1.5">
                  <UserCheck className="h-3.5 w-3.5" />
                  Real Database Seed Accounts (VIVA Demo)
                </span>
                <Badge variant="warning" className="text-[9px] py-0">
                  MySQL Users
                </Badge>
              </div>

              <div className="grid grid-cols-2 gap-2 pt-1">
                {QUICK_LOGIN_PRESETS.map((preset) => (
                  <button
                    key={preset.username}
                    type="button"
                    onClick={() => handleQuickLogin(preset)}
                    className="flex flex-col text-left p-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50/70 dark:bg-slate-800/40 hover:border-amber-400 dark:hover:border-amber-500/60 hover:bg-amber-50/50 dark:hover:bg-amber-950/20 transition-all text-xs group"
                  >
                    <div className="flex items-center justify-between">
                      <span className="font-semibold text-slate-900 dark:text-white group-hover:text-amber-800 dark:group-hover:text-amber-300 truncate">
                        {preset.name}
                      </span>
                      <span className="text-[9px] font-mono text-slate-400 group-hover:text-amber-600">
                        {preset.initials}
                      </span>
                    </div>
                    <span className="text-[10px] text-slate-500 dark:text-slate-400 capitalize">
                      {preset.role}
                    </span>
                  </button>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Footer info */}
        <p className="text-center text-[11px] text-slate-500 dark:text-slate-400">
          SmartCity360 • Object-Oriented Design Patterns Assessment
        </p>
      </div>
    </div>
  );
}

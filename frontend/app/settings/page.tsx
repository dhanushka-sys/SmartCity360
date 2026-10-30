"use client";

import * as React from "react";
import {
  Settings,
  Sliders,
  RotateCcw,
  Shield,
  Monitor,
  Check,
  Info,
  Database,
  Building,
  Sun,
  Moon,
  GraduationCap,
  Building2,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { useTheme } from "@/components/theme-provider";
import { useAppMode } from "@/components/mode-provider";

export default function SettingsPage() {
  const { theme, setTheme } = useTheme();
  const { mode, setMode, isAcademic } = useAppMode();
  const [density, setDensity] = React.useState<"comfortable" | "compact">("comfortable");
  const [refreshInterval, setRefreshInterval] = React.useState("30");
  const [resetSuccess, setResetSuccess] = React.useState(false);

  const handleResetData = () => {
    // Flash reset confirmation
    setResetSuccess(true);
    setTimeout(() => setResetSuccess(false), 3000);
  };

  return (
    <div className="space-y-6 max-w-4xl">
      {/* Header */}
      <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/80 p-4 shadow-xs">
        <div className="flex items-center gap-2">
          <Settings className="h-5 w-5 text-cyan-600 dark:text-cyan-400" />
          <h2 className="text-base font-bold text-slate-900 dark:text-white tracking-tight">System &amp; Demo Settings</h2>
        </div>
        <p className="mt-1 text-xs text-slate-600 dark:text-slate-300">
          Frontend interface preferences, application mode switching, and sample state management.
        </p>
      </div>

      {/* Interface Preferences */}
      <Card className="border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/70 shadow-sm">
        <CardHeader className="pb-3">
          <CardTitle className="text-sm text-slate-900 dark:text-white">Display &amp; Mode Preferences</CardTitle>
          <CardDescription>
            Configure operational presentation mode, theme palette, and table densities
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4 text-xs">
          {/* Mode Selector: Normal vs Academic */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-3 border-b border-slate-200 dark:border-slate-800 gap-3">
            <div>
              <p className="font-semibold text-slate-900 dark:text-white flex items-center gap-1.5">
                <span>Application Mode</span>
                <Badge variant={isAcademic ? "purple" : "info"} className="text-[9px]">
                  {isAcademic ? "Academic / Pattern Mode" : "Real-World Enterprise Mode"}
                </Badge>
              </p>
              <p className="text-[11px] text-slate-500 dark:text-slate-400 max-w-md mt-0.5">
                {isAcademic
                  ? "Academic Mode reveals GoF Design Pattern banners, UML class roles, AST grammar trees, and VIVA examination test scenarios."
                  : "Normal Mode hides academic pattern labels and displays a realistic, production-ready smart city operations platform."}
              </p>
            </div>
            <div className="flex items-center gap-2 shrink-0">
              <button
                onClick={() => setMode("normal")}
                className={`flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-xs font-semibold transition-all border ${
                  mode === "normal"
                    ? "border-cyan-500 bg-cyan-50 text-cyan-800 dark:bg-cyan-950/40 dark:text-cyan-300 shadow-xs"
                    : "border-slate-200 bg-slate-50 text-slate-600 hover:text-slate-900 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-400"
                }`}
              >
                <Building2 className="h-3.5 w-3.5 text-cyan-600 dark:text-cyan-400" />
                <span>Normal Mode</span>
              </button>
              <button
                onClick={() => setMode("academic")}
                className={`flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-xs font-semibold transition-all border ${
                  mode === "academic"
                    ? "border-purple-400 bg-purple-50 text-purple-800 dark:bg-purple-950/40 dark:text-purple-300 shadow-xs ring-1 ring-purple-400/40"
                    : "border-slate-200 bg-slate-50 text-slate-600 hover:text-slate-900 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-400"
                }`}
              >
                <GraduationCap className="h-3.5 w-3.5 text-purple-600 dark:text-purple-400" />
                <span>Pattern Mode 🎓</span>
              </button>
            </div>
          </div>

          {/* Theme Selector */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-3 border-b border-slate-200 dark:border-slate-800 gap-3">
            <div>
              <p className="font-semibold text-slate-900 dark:text-white">Visual Design Theme</p>
              <p className="text-[11px] text-slate-500 dark:text-slate-400">
                Switch between Crisp Light Mode and Dark Navy SaaS
              </p>
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={() => setTheme("light")}
                className={`flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-xs font-semibold transition-all border ${
                  theme === "light"
                    ? "border-cyan-500 bg-cyan-50 text-cyan-800 shadow-xs"
                    : "border-slate-200 bg-slate-50 text-slate-600 hover:text-slate-900 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-400"
                }`}
              >
                <Sun className="h-3.5 w-3.5 text-amber-500" />
                <span>Light Mode (Active)</span>
              </button>
              <button
                onClick={() => setTheme("dark")}
                className={`flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-xs font-semibold transition-all border ${
                  theme === "dark"
                    ? "border-cyan-500 bg-cyan-950/60 text-cyan-300 shadow-xs"
                    : "border-slate-200 bg-slate-50 text-slate-600 hover:text-slate-900 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-400"
                }`}
              >
                <Moon className="h-3.5 w-3.5 text-cyan-400" />
                <span>Dark Navy</span>
              </button>
            </div>
          </div>

          {/* Table Data Density */}
          <div className="flex items-center justify-between pb-3 border-b border-slate-200 dark:border-slate-800">
            <div>
              <p className="font-semibold text-slate-900 dark:text-white">Table Data Density</p>
              <p className="text-[11px] text-slate-500 dark:text-slate-400">
                Adjust row padding across registry tables
              </p>
            </div>
            <div className="flex items-center gap-1 rounded-lg border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950/60 p-1">
              <button
                onClick={() => setDensity("comfortable")}
                className={`rounded px-2.5 py-1 text-xs font-medium transition-colors ${
                  density === "comfortable"
                    ? "bg-white text-cyan-700 shadow-xs font-semibold dark:bg-slate-800 dark:text-cyan-300"
                    : "text-slate-600 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white"
                }`}
              >
                Comfortable
              </button>
              <button
                onClick={() => setDensity("compact")}
                className={`rounded px-2.5 py-1 text-xs font-medium transition-colors ${
                  density === "compact"
                    ? "bg-white text-cyan-700 shadow-xs font-semibold dark:bg-slate-800 dark:text-cyan-300"
                    : "text-slate-600 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white"
                }`}
              >
                Compact
              </button>
            </div>
          </div>

          {/* Polling Rate */}
          <div className="flex items-center justify-between">
            <div>
              <p className="font-semibold text-slate-900 dark:text-white">Simulated Telemetry Poll Rate</p>
              <p className="text-[11px] text-slate-500 dark:text-slate-400">
                Interval for mocked sensor updates
              </p>
            </div>
            <select
              value={refreshInterval}
              onChange={(e) => setRefreshInterval(e.target.value)}
              className="rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-950 px-2.5 py-1 text-xs text-slate-900 dark:text-white shadow-xs"
            >
              <option value="15">Every 15s</option>
              <option value="30">Every 30s</option>
              <option value="60">Every 60s</option>
            </select>
          </div>
        </CardContent>
      </Card>

      {/* State Reset Card */}
      <Card className="border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/70 shadow-sm">
        <CardHeader className="pb-3">
          <CardTitle className="text-sm text-slate-900 dark:text-white">Sample Dataset State Management</CardTitle>
          <CardDescription>
            Reset in-memory mock datasets back to their pristine starting values
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-3 text-xs">
          <p className="text-slate-600 dark:text-slate-400 leading-relaxed">
            During an operational review or academic viva demonstration, you can reset all modified data streams,
            cascaded zone statuses, escalated complaints, and policy rules back to their default demo state.
          </p>

          <div className="pt-2">
            <Button
              variant="outline"
              size="sm"
              onClick={handleResetData}
              className="gap-2 text-xs text-amber-700 dark:text-amber-400 hover:text-amber-800 dark:hover:text-amber-300 hover:border-amber-500/50"
            >
              <RotateCcw className="h-3.5 w-3.5" />
              <span>Reset All Simulated Data</span>
            </Button>

            {resetSuccess && (
              <span className="ml-3 text-emerald-700 dark:text-emerald-400 text-xs font-medium inline-flex items-center gap-1">
                <Check className="h-3.5 w-3.5" />
                <span>Simulated state reset successfully!</span>
              </span>
            )}
          </div>
        </CardContent>
      </Card>

      {/* About SmartCity360 Card */}
      <Card className="border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/70 shadow-sm">
        <CardHeader className="pb-3">
          <div className="flex items-center gap-2">
            <Info className="h-4 w-4 text-cyan-600 dark:text-cyan-400" />
            <CardTitle className="text-sm text-slate-900 dark:text-white">About SmartCity360</CardTitle>
          </div>
          <CardDescription>
            Platform architecture &amp; decoupled backend integration specification
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-3 text-xs leading-relaxed text-slate-600 dark:text-slate-300">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950/50 p-3.5 font-mono text-[11px]">
            <div>
              <span className="text-slate-500 dark:text-slate-400">Target Environment:</span>
              <p className="text-slate-900 dark:text-white font-semibold">Metropolis Neo-Prime Smart City</p>
            </div>
            <div>
              <span className="text-slate-500 dark:text-slate-400">Engineering Role:</span>
              <p className="text-cyan-700 dark:text-cyan-400 font-semibold">UrbanTech Solutions</p>
            </div>
            <div>
              <span className="text-slate-500 dark:text-slate-400">Unit ID &amp; Unit:</span>
              <p className="text-slate-900 dark:text-white">JIAT/OODP II /EX/01 • OODP II</p>
            </div>
            <div>
              <span className="text-slate-500 dark:text-slate-400">Architecture Phase:</span>
              <p className="text-emerald-700 dark:text-emerald-400 font-semibold">Frontend-Only (Decoupled)</p>
            </div>
          </div>

          <div className="rounded-xl border border-cyan-200 dark:border-cyan-950/60 bg-cyan-50/70 dark:bg-cyan-950/20 p-3 text-[11px] text-cyan-900 dark:text-cyan-300 space-y-1">
            <p className="font-semibold text-cyan-800 dark:text-cyan-200">Future Backend Integration Pathway:</p>
            <p className="text-slate-700 dark:text-slate-300 leading-relaxed">
              Every data entity and operation is encapsulated behind dedicated service abstractions in{" "}
              <code className="text-cyan-800 dark:text-cyan-300 font-mono">lib/api/</code>. To connect your future real backend,
              replace the mock asynchronous service methods with real HTTP/Fetch calls to your backend endpoints
              without altering any component or UI layout.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

"use client";

import * as React from "react";
import { BentoKpi } from "@/components/dashboard/bento-kpi";
import { EnergyChart } from "@/components/dashboard/energy-chart";
import { ComplaintTrendChart } from "@/components/dashboard/complaint-trend-chart";
import { QuickActions } from "@/components/dashboard/quick-actions";
import { RecentComplaintsTable } from "@/components/dashboard/recent-complaints-table";
import { SystemActivityFeed } from "@/components/dashboard/system-activity-feed";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import {
  ShieldAlert,
  ArrowRight,
  Radio,
  CheckCircle2,
  Sparkles,
  ExternalLink,
  Activity,
  Layers,
} from "lucide-react";
import { useAppMode } from "@/components/mode-provider";

export default function DashboardPage() {
  const { isAcademic } = useAppMode();

  return (
    <div className="space-y-6">
      {/* Top Banner Notice: Architecture & Simulation Context */}
      <div className="relative overflow-hidden rounded-2xl border border-cyan-200 dark:border-cyan-500/30 bg-gradient-to-r from-cyan-50 via-white to-blue-50 dark:from-slate-900 dark:via-cyan-950/20 dark:to-blue-950/30 p-5 backdrop-blur-md shadow-xs">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="flex h-2 w-2 rounded-full bg-cyan-500 animate-pulse" />
              <Badge variant={isAcademic ? "purple" : "info"} className="text-[10px] font-semibold">
                {isAcademic ? "OODP II ACADEMIC DEMONSTRATOR" : "MUNICIPAL OPERATIONS COMMAND"}
              </Badge>
              <span className="text-xs text-slate-500 dark:text-slate-400">UrbanTech Solutions • Metropolis Neo-Prime</span>
            </div>
            <h2 className="text-lg md:text-xl font-bold text-slate-900 dark:text-white tracking-tight">
              {isAcademic
                ? "Enterprise Smart City Operations & Design Patterns Suite"
                : "Metropolis Smart City Operations Center"}
            </h2>
            <p className="text-xs text-slate-600 dark:text-slate-300 max-w-3xl leading-relaxed">
              {isAcademic
                ? "Demonstrating 5 core object-oriented design patterns across modular city services. Frontend-only architecture with decoupled service interfaces ready for backend phase integration."
                : "Centralized real-time monitoring and control of municipal energy grids, urban zone hierarchies, citizen incident dispatch, smart streetlight fleets, and automated compliance policies."}
            </p>
          </div>
          <div className="flex items-center gap-2 shrink-0">
            <Link href="/test-center">
              <Button variant="default" size="sm" className="gap-2">
                {isAcademic ? (
                  <>
                    <Sparkles className="h-4 w-4" />
                    <span>Launch VIVA Test Suite</span>
                  </>
                ) : (
                  <>
                    <Activity className="h-4 w-4" />
                    <span>System Diagnostics</span>
                  </>
                )}
              </Button>
            </Link>
          </div>
        </div>
      </div>

      {/* Bento Grid KPI Overview */}
      <BentoKpi />

      {/* Main Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <EnergyChart />
        <ComplaintTrendChart />
      </div>

      {/* Quick Launchers */}
      <QuickActions />

      {/* Operational Highlights & Summaries */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Zone Hierarchy Snapshot (Composite) */}
        <Card className="border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/70 flex flex-col justify-between shadow-sm">
          <div>
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <CardTitle className="text-sm">Zone Hierarchy Summary</CardTitle>
                <Badge variant="blue" className="text-[10px]">
                  {isAcademic ? "Composite Pattern" : "Urban Hierarchy"}
                </Badge>
              </div>
              <CardDescription>
                City → District → Street → Building composition
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="rounded-xl border border-slate-200 dark:border-slate-800/80 bg-slate-50 dark:bg-slate-950/50 p-3 space-y-2">
                <div className="flex justify-between text-xs">
                  <span className="text-slate-500 dark:text-slate-400">Root City:</span>
                  <span className="font-semibold text-slate-900 dark:text-white">Metropolis Neo-Prime</span>
                </div>
                <div className="flex justify-between text-xs">
                  <span className="text-slate-500 dark:text-slate-400">Active Districts:</span>
                  <span className="text-slate-700 dark:text-slate-200">3 Sub-zones</span>
                </div>
                <div className="flex justify-between text-xs">
                  <span className="text-slate-500 dark:text-slate-400">Municipal Streets:</span>
                  <span className="text-slate-700 dark:text-slate-200">6 Arterials</span>
                </div>
                <div className="flex justify-between text-xs">
                  <span className="text-slate-500 dark:text-slate-400">Facilities:</span>
                  <span className="text-slate-700 dark:text-slate-200">10 Facilities</span>
                </div>
              </div>
              <p className="text-[11px] text-slate-500 dark:text-slate-400 leading-relaxed">
                {isAcademic ? (
                  <>
                    Commands like <code className="text-cyan-700 dark:text-cyan-300 font-semibold">SHUTDOWN</code> and{" "}
                    <code className="text-cyan-700 dark:text-cyan-300 font-semibold">REPORT_USAGE</code> apply
                    uniformly to leaves and composites.
                  </>
                ) : (
                  "Emergency shutdown, restart, and energy audit commands cascade seamlessly across entire districts and individual buildings."
                )}
              </p>
            </CardContent>
          </div>
          <div className="p-5 pt-0">
            <Link href="/zones">
              <Button variant="outline" size="sm" className="w-full justify-between text-xs">
                <span>Explore Zone Tree</span>
                <ArrowRight className="h-3.5 w-3.5" />
              </Button>
            </Link>
          </div>
        </Card>

        {/* Streetlight Flyweight Memory Snapshot */}
        <Card className="border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/70 flex flex-col justify-between shadow-sm">
          <div>
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <CardTitle className="text-sm">
                  {isAcademic ? "Flyweight Profile Pool" : "Lighting Profile Management"}
                </CardTitle>
                <Badge variant="success" className="text-[10px]">
                  {isAcademic ? "Flyweight Pattern" : "Resource Efficiency"}
                </Badge>
              </div>
              <CardDescription>
                {isAcademic
                  ? "Intrinsic profiles vs extrinsic light coordinates"
                  : "Shared hardware profiles vs individual pole coordinates"}
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="rounded-xl border border-slate-200 dark:border-slate-800/80 bg-slate-50 dark:bg-slate-950/50 p-3 space-y-2">
                <div className="flex justify-between text-xs">
                  <span className="text-slate-500 dark:text-slate-400">Simulated Grid Scale:</span>
                  <span className="font-semibold text-slate-900 dark:text-white">24,500 Streetlights</span>
                </div>
                <div className="flex justify-between text-xs">
                  <span className="text-slate-500 dark:text-slate-400">
                    {isAcademic ? "Flyweight Profiles:" : "Standard Profiles:"}
                  </span>
                  <span className="text-emerald-600 dark:text-emerald-400 font-medium">4 Shared Instances</span>
                </div>
                <div className="flex justify-between text-xs">
                  <span className="text-slate-500 dark:text-slate-400">Memory Un-optimized:</span>
                  <span className="text-rose-600 dark:text-rose-400 font-mono">28.2 MB</span>
                </div>
                <div className="flex justify-between text-xs">
                  <span className="text-slate-500 dark:text-slate-400">Optimized Footprint:</span>
                  <span className="text-emerald-600 dark:text-emerald-400 font-mono font-semibold">3.1 MB (-88.8%)</span>
                </div>
              </div>
              <p className="text-[11px] text-slate-500 dark:text-slate-400 leading-relaxed">
                Shared wattage, schedules, and optics instantiated once; individual poles retain coordinates.
              </p>
            </CardContent>
          </div>
          <div className="p-5 pt-0">
            <Link href="/streetlights">
              <Button variant="outline" size="sm" className="w-full justify-between text-xs">
                <span>Manage Streetlights</span>
                <ArrowRight className="h-3.5 w-3.5" />
              </Button>
            </Link>
          </div>
        </Card>

        {/* Policy Interpreter Snapshot */}
        <Card className="border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/70 flex flex-col justify-between shadow-sm">
          <div>
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <CardTitle className="text-sm">
                  {isAcademic ? "City Policy DSL Rules" : "Environmental & Traffic Policies"}
                </CardTitle>
                <Badge variant="purple" className="text-[10px]">
                  {isAcademic ? "Interpreter Pattern" : "Compliance Engine"}
                </Badge>
              </div>
              <CardDescription>
                {isAcademic
                  ? "Grammar parsing for real-time sensor evaluations"
                  : "Automated real-time compliance evaluation on city sensors"}
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="rounded-xl border border-slate-200 dark:border-slate-800/80 bg-slate-50 dark:bg-slate-950/50 p-3 space-y-2">
                <div className="flex justify-between text-xs">
                  <span className="text-slate-500 dark:text-slate-400">Active Rule Count:</span>
                  <span className="font-semibold text-slate-900 dark:text-white">5 Policies Active</span>
                </div>
                <div className="flex justify-between text-xs">
                  <span className="text-slate-500 dark:text-slate-400">
                    {isAcademic ? "Grammar Operators:" : "Monitored Domains:"}
                  </span>
                  <span className="text-purple-700 dark:text-purple-300 font-medium text-[11px]">
                    {isAcademic ? "<=, >=, BETWEEN, AND" : "Noise, Speed, Air Quality, Power"}
                  </span>
                </div>
                <div className="flex justify-between text-xs">
                  <span className="text-slate-500 dark:text-slate-400">
                    {isAcademic ? "Execution Safety:" : "Enforcement Action:"}
                  </span>
                  <span className="text-emerald-600 dark:text-emerald-400 font-medium">
                    {isAcademic ? "Safe AST (No eval)" : "Automated Incident Alert"}
                  </span>
                </div>
                <div className="flex justify-between text-xs">
                  <span className="text-slate-500 dark:text-slate-400">Last Evaluation:</span>
                  <span className="text-slate-700 dark:text-slate-200">14 min ago (Violation)</span>
                </div>
              </div>
              <p className="text-[11px] text-slate-500 dark:text-slate-400 leading-relaxed">
                {isAcademic
                  ? "Expressions parsed into AST nodes at runtime without compiling or executing arbitrary code."
                  : "Continuous automated compliance monitoring evaluating live city sensor feeds and notifying field teams."}
              </p>
            </CardContent>
          </div>
          <div className="p-5 pt-0">
            <Link href="/policies">
              <Button variant="outline" size="sm" className="w-full justify-between text-xs">
                <span>Policy Rule Studio</span>
                <ArrowRight className="h-3.5 w-3.5" />
              </Button>
            </Link>
          </div>
        </Card>
      </div>

      {/* Tables & Activity Trace Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <RecentComplaintsTable />
        <SystemActivityFeed />
      </div>
    </div>
  );
}

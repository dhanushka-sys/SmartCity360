"use client";

import * as React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Activity,
  Layers,
  Network,
  AlertTriangle,
  Lightbulb,
  FileCode2,
  CheckCircle2,
  Settings,
  ChevronLeft,
  ChevronRight,
  Radio,
  Cpu,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { useAppMode } from "@/components/mode-provider";
import { checkBackendConnection } from "@/lib/api/backend-client";

interface SidebarProps {
  collapsed: boolean;
  onToggleCollapse: () => void;
  mobileOpen: boolean;
  onMobileClose: () => void;
}

export function Sidebar({ collapsed, onToggleCollapse, mobileOpen, onMobileClose }: SidebarProps) {
  const pathname = usePathname();
  const { isAcademic } = useAppMode();
  const [backendOnline, setBackendOnline] = React.useState<boolean | null>(null);

  React.useEffect(() => {
    let mounted = true;
    const verifyBackend = async () => {
      const isOnline = await checkBackendConnection();
      if (mounted) setBackendOnline(isOnline);
    };

    verifyBackend();
    const interval = setInterval(verifyBackend, 12000);
    return () => {
      mounted = false;
      clearInterval(interval);
    };
  }, []);

  const navItems = [
    {
      title: "Overview",
      href: "/",
      icon: Activity,
      subtitleNormal: "Real-time City Metrics",
      subtitleAcademic: undefined,
    },
    {
      title: "Data Streams",
      href: "/data-streams",
      icon: Layers,
      subtitleNormal: "Telemetry Security",
      subtitleAcademic: "Telemetry Security",
    },
    {
      title: "Zone Management",
      href: "/zones",
      icon: Network,
      subtitleNormal: "Urban Hierarchy",
      subtitleAcademic: "Urban Hierarchy",
    },
    {
      title: "Citizen Complaints",
      href: "/complaints",
      icon: AlertTriangle,
      subtitleNormal: "Incident Escalation",
      subtitleAcademic: "Incident Escalation",
    },
    {
      title: "Streetlights",
      href: "/streetlights",
      icon: Lightbulb,
      subtitleNormal: "Fleet Management",
      subtitleAcademic: "Fleet Management",
    },
    {
      title: "City Policies",
      href: "/policies",
      icon: FileCode2,
      subtitleNormal: "Automated Rules",
      subtitleAcademic: "Automated Rules",
    },
    {
      title: "System Diagnostics",
      href: "/test-center",
      icon: CheckCircle2,
      subtitleNormal: "Scenario Verification",
      subtitleAcademic: "Scenario Verification",
      color: "text-emerald-600 dark:text-emerald-300",
      badge: "Verify",
    },
    {
      title: "Settings",
      href: "/settings",
      icon: Settings,
      subtitleNormal: "System Preferences",
      subtitleAcademic: undefined,
    },
  ];

  return (
    <>
      {/* Mobile Backdrop */}
      {mobileOpen && (
        <div
          className="fixed inset-0 z-40 bg-slate-900/50 dark:bg-slate-950/80 backdrop-blur-sm lg:hidden"
          onClick={onMobileClose}
        />
      )}

      {/* Sidebar Panel */}
      <aside
        className={cn(
          "fixed inset-y-0 left-0 z-50 flex flex-col border-r border-slate-200 dark:border-slate-800/90 bg-white/95 dark:bg-[#0a101f]/95 backdrop-blur-xl transition-all duration-300 lg:relative lg:z-40 shadow-sm lg:shadow-none",
          collapsed ? "w-20" : "w-64",
          mobileOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"
        )}
      >
        {/* Brand Header */}
        <div
          className={cn(
            "relative flex h-16 items-center border-b border-slate-200 dark:border-slate-800/80 transition-all",
            collapsed ? "justify-center px-0" : "justify-between px-4"
          )}
        >
          <Link
            href="/"
            className={cn(
              "flex items-center gap-3 overflow-hidden",
              collapsed && "justify-center"
            )}
            title="SmartCity360"
          >
            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-cyan-500 to-blue-600 shadow-md shadow-cyan-500/20 text-white">
              <Cpu className="h-5 w-5" />
            </div>
            {!collapsed && (
              <div className="flex flex-col">
                <span className="text-base font-bold tracking-tight text-slate-900 dark:text-white flex items-center gap-1.5">
                  SmartCity<span className="text-cyan-600 dark:text-cyan-400">360</span>
                </span>
                <span className="text-[10px] text-slate-500 dark:text-slate-400 font-medium tracking-wide">
                  {isAcademic ? "OODP II PLATFORM" : "MUNICIPAL PLATFORM"}
                </span>
              </div>
            )}
          </Link>

          {/* Desktop Collapse Toggle */}
          <button
            onClick={onToggleCollapse}
            className={cn(
              "hidden lg:flex items-center justify-center transition-all",
              collapsed
                ? "absolute -right-3.5 top-1/2 -translate-y-1/2 z-30 h-7 w-7 rounded-full border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white shadow-md hover:bg-slate-50 dark:hover:bg-slate-700"
                : "h-7 w-7 rounded-lg border border-slate-200 dark:border-slate-700/60 bg-slate-100 dark:bg-slate-800/50 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-200 dark:hover:bg-slate-700"
            )}
            title={collapsed ? "Expand Sidebar" : "Collapse Sidebar"}
          >
            {collapsed ? <ChevronRight className="h-4 w-4" /> : <ChevronLeft className="h-4 w-4" />}
          </button>
        </div>

        {/* Navigation List */}
        <div className="flex-1 overflow-y-auto px-3 py-4 space-y-1">
          <div className={cn("px-2", !collapsed ? "pb-2" : "hidden")}>
            <p className="text-[10px] font-semibold uppercase tracking-wider text-slate-400 dark:text-slate-500">
              {isAcademic ? "Operations & Patterns" : "Operations & Modules"}
            </p>
          </div>

          {navItems.map((item) => {
            const isActive = pathname === item.href || (item.href !== "/" && pathname.startsWith(item.href));
            const Icon = item.icon;
            const subtitle = isAcademic ? item.subtitleAcademic : item.subtitleNormal;

            return (
              <Link
                key={item.href}
                href={item.href}
                onClick={onMobileClose}
                className={cn(
                  "group relative flex items-center rounded-xl text-xs transition-all duration-150",
                  collapsed ? "justify-center px-0 py-2.5" : "gap-3 px-3 py-2.5",
                  isActive
                    ? "bg-slate-100 dark:bg-slate-800/90 text-slate-900 dark:text-white shadow-sm border border-slate-300 dark:border-slate-700 font-semibold"
                    : "text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 hover:bg-slate-100/80 dark:hover:bg-slate-800/40 border border-transparent"
                )}
                title={collapsed ? item.title : undefined}
              >
                {isActive && (
                  <span className="absolute left-0 top-2 bottom-2 rounded-r-full w-1 bg-slate-500" />
                )}
                <Icon
                  className={cn(
                    "h-4 w-4 shrink-0 transition-transform group-hover:scale-110",
                    isActive
                      ? "text-slate-700 dark:text-slate-200"
                      : item.color || "text-slate-500 dark:text-slate-400"
                  )}
                />

                {!collapsed && (
                  <div className="flex flex-1 items-center justify-between min-w-0">
                    <div className="flex flex-col truncate">
                      <span
                        className={cn(
                          "truncate",
                          isActive
                            ? "font-semibold text-slate-900 dark:text-white"
                            : "text-slate-700 dark:text-slate-300"
                        )}
                      >
                        {item.title}
                      </span>
                      {subtitle && (
                        <span className="text-[10px] truncate text-slate-400 dark:text-slate-500">
                          {subtitle}
                        </span>
                      )}
                    </div>
                    {item.badge && (
                      <span
                        className={cn(
                          "ml-2 rounded-full border px-2 py-0.5 text-[9px] font-semibold",
                          isAcademic
                            ? "bg-purple-100 dark:bg-purple-950/80 border-purple-300 dark:border-purple-800/60 text-purple-800 dark:text-purple-300"
                            : "bg-cyan-100 dark:bg-cyan-950/80 border-cyan-300 dark:border-cyan-800/60 text-cyan-800 dark:text-cyan-300"
                        )}
                      >
                        {item.badge}
                      </span>
                    )}
                  </div>
                )}
              </Link>
            );
          })}
        </div>

        {/* Footer Status Pill */}
        {!collapsed ? (
          <div className="p-3 border-t border-slate-200 dark:border-slate-800/80">
            <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/60 p-3">
              <div
                className={cn(
                  "flex items-center gap-2 text-xs font-semibold",
                  backendOnline
                    ? "text-emerald-600 dark:text-emerald-400"
                    : "text-rose-600 dark:text-rose-400"
                )}
              >
                <span className="relative flex h-2 w-2">
                  <span
                    className={cn(
                      "animate-ping absolute inline-flex h-full w-full rounded-full opacity-75",
                      backendOnline ? "bg-emerald-400" : "bg-rose-400"
                    )}
                  ></span>
                  <span
                    className={cn(
                      "relative inline-flex rounded-full h-2 w-2",
                      backendOnline ? "bg-emerald-500" : "bg-rose-500"
                    )}
                  ></span>
                </span>
                <span>
                  {backendOnline === null
                    ? "Checking MySQL..."
                    : backendOnline
                    ? "MySQL: Connected"
                    : "MySQL: Offline"}
                </span>
              </div>
              <p className="mt-1 text-[11px] text-slate-500 dark:text-slate-400">
                {backendOnline
                  ? "Live sync via Tomcat 9 (localhost:8080)"
                  : "Start Tomcat 9 to query database"}
              </p>
            </div>
          </div>
        ) : (
          <div className="p-3 border-t border-slate-200 dark:border-slate-800/80 flex justify-center">
            <Radio
              className={cn(
                "h-4 w-4 animate-pulse",
                backendOnline ? "text-emerald-500" : "text-rose-500"
              )}
            />
          </div>
        )}
      </aside>
    </>
  );
}

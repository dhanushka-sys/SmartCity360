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
      isDevelopModule: false,
    },
    {
      title: "Data Streams",
      href: "/data-streams",
      icon: Layers,
      subtitleNormal: "Telemetry Security",
      subtitleAcademic: "Decorator Pattern",
      color: "text-amber-600 dark:text-amber-400",
      isDevelopModule: true,
    },
    {
      title: "Zone Management",
      href: "/zones",
      icon: Network,
      subtitleNormal: "Urban Hierarchy",
      subtitleAcademic: "Composite Pattern",
      color: "text-amber-600 dark:text-amber-400",
      isDevelopModule: true,
    },
    {
      title: "Citizen Complaints",
      href: "/complaints",
      icon: AlertTriangle,
      subtitleNormal: "Incident Escalation",
      subtitleAcademic: "Chain of Resp.",
      color: "text-amber-600 dark:text-amber-400",
      isDevelopModule: true,
    },
    {
      title: "Streetlights",
      href: "/streetlights",
      icon: Lightbulb,
      subtitleNormal: "Fleet Management",
      subtitleAcademic: "Flyweight Pattern",
      color: "text-amber-600 dark:text-amber-400",
      isDevelopModule: true,
    },
    {
      title: "City Policies",
      href: "/policies",
      icon: FileCode2,
      subtitleNormal: "Automated Rules",
      subtitleAcademic: "Interpreter Pattern",
      color: "text-amber-600 dark:text-amber-400",
      isDevelopModule: true,
    },
    {
      title: isAcademic ? "Test Center" : "System Diagnostics",
      href: "/test-center",
      icon: CheckCircle2,
      subtitleNormal: "Scenario Verification",
      subtitleAcademic: "Academic Demo / VIVA",
      color: "text-emerald-600 dark:text-emerald-300",
      badge: isAcademic ? "5 Patterns" : "Verify",
      isDevelopModule: false,
    },
    {
      title: "Settings",
      href: "/settings",
      icon: Settings,
      subtitleNormal: "System Preferences",
      subtitleAcademic: undefined,
      isDevelopModule: false,
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
          "fixed inset-y-0 left-0 z-50 flex flex-col border-r border-slate-200 dark:border-slate-800/90 bg-white/95 dark:bg-[#0a101f]/95 backdrop-blur-xl transition-all duration-300 lg:static shadow-sm lg:shadow-none",
          collapsed ? "w-20" : "w-64",
          mobileOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"
        )}
      >
        {/* Brand Header */}
        <div className="flex h-16 items-center justify-between px-4 border-b border-slate-200 dark:border-slate-800/80">
          <Link href="/" className="flex items-center gap-3 overflow-hidden">
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
            className="hidden lg:flex h-7 w-7 items-center justify-center rounded-lg border border-slate-200 dark:border-slate-700/60 bg-slate-100 dark:bg-slate-800/50 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
            title={collapsed ? "Expand Sidebar" : "Collapse Sidebar"}
          >
            {collapsed ? <ChevronRight className="h-4 w-4" /> : <ChevronLeft className="h-4 w-4" />}
          </button>
        </div>

        {/* Navigation List */}
        <div className="flex-1 overflow-y-auto px-3 py-4 space-y-1">
          <div className="px-2 pb-2">
            {!collapsed && (
              <p className="text-[10px] font-semibold uppercase tracking-wider text-slate-400 dark:text-slate-500">
                {isAcademic ? "Operations & Patterns" : "Operations & Modules"}
              </p>
            )}
          </div>

          {navItems.map((item) => {
            const isActive = pathname === item.href || (item.href !== "/" && pathname.startsWith(item.href));
            const Icon = item.icon;
            const subtitle = isAcademic ? item.subtitleAcademic : item.subtitleNormal;
            const isDevelop = !!item.isDevelopModule;

            return (
              <Link
                key={item.href}
                href={item.href}
                onClick={onMobileClose}
                className={cn(
                  "group relative flex items-center gap-3 rounded-xl px-3 py-2.5 text-xs transition-all duration-150",
                  isDevelop
                    ? isActive
                      ? "bg-amber-100/90 dark:bg-amber-950/70 text-amber-950 dark:text-amber-100 shadow-sm border border-amber-400 dark:border-amber-500/80 font-bold ring-1 ring-amber-400/40"
                      : "bg-amber-50/50 dark:bg-amber-950/20 text-amber-900/90 dark:text-amber-200/90 border border-amber-200/70 dark:border-amber-900/50 hover:bg-amber-100/80 dark:hover:bg-amber-900/40 hover:border-amber-300 dark:hover:border-amber-700 font-medium"
                    : isActive
                    ? "bg-slate-100 dark:bg-slate-800/90 text-slate-900 dark:text-white shadow-sm border border-slate-300 dark:border-slate-700 font-semibold"
                    : "text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 hover:bg-slate-100/80 dark:hover:bg-slate-800/40 border border-transparent"
                )}
                title={collapsed ? item.title : undefined}
              >
                {isActive && (
                  <span
                    className={cn(
                      "absolute left-0 top-2 bottom-2 rounded-r-full",
                      isDevelop ? "w-1.5 bg-amber-500 shadow-sm shadow-amber-500/50" : "w-1 bg-slate-500"
                    )}
                  />
                )}
                <Icon
                  className={cn(
                    "h-4 w-4 shrink-0 transition-transform group-hover:scale-110",
                    isDevelop
                      ? "text-amber-600 dark:text-amber-400"
                      : isActive
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
                          isDevelop
                            ? isActive
                              ? "font-bold text-amber-950 dark:text-amber-100"
                              : "font-semibold text-amber-900 dark:text-amber-200"
                            : isActive
                            ? "font-semibold text-slate-900 dark:text-white"
                            : "text-slate-700 dark:text-slate-300"
                        )}
                      >
                        {item.title}
                      </span>
                      {subtitle && (
                        <span
                          className={cn(
                            "text-[10px] truncate",
                            isDevelop
                              ? "text-amber-700/75 dark:text-amber-400/80"
                              : "text-slate-400 dark:text-slate-500"
                          )}
                        >
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
                  "flex items-center gap-2 text-xs font-medium",
                  backendOnline
                    ? "text-emerald-600 dark:text-emerald-400"
                    : "text-cyan-600 dark:text-cyan-400"
                )}
              >
                <span className="relative flex h-2 w-2">
                  <span
                    className={cn(
                      "animate-ping absolute inline-flex h-full w-full rounded-full opacity-75",
                      backendOnline ? "bg-emerald-400" : "bg-cyan-400"
                    )}
                  ></span>
                  <span
                    className={cn(
                      "relative inline-flex rounded-full h-2 w-2",
                      backendOnline ? "bg-emerald-500" : "bg-cyan-500"
                    )}
                  ></span>
                </span>
                <span>
                  {backendOnline === null
                    ? "Checking Backend..."
                    : backendOnline
                    ? "Backend Connected"
                    : "Standalone Mode"}
                </span>
              </div>
              <p className="mt-1 text-[11px] text-slate-500 dark:text-slate-400">
                {backendOnline
                  ? "Connected to MySQL via Tomcat 9 (localhost:8080)"
                  : "Client demo data active. Ready for Tomcat 9"}
              </p>
            </div>
          </div>
        ) : (
          <div className="p-3 border-t border-slate-200 dark:border-slate-800/80 flex justify-center">
            <Radio
              className={cn(
                "h-4 w-4 animate-pulse",
                backendOnline ? "text-emerald-500" : "text-cyan-500"
              )}
            />
          </div>
        )}
      </aside>
    </>
  );
}

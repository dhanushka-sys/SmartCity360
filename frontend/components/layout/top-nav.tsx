"use client";

import * as React from "react";
import { usePathname } from "next/navigation";
import {
  Bell,
  Search,
  Menu,
  CheckCircle,
  AlertTriangle,
  User as UserIcon,
  SlidersHorizontal,
  ExternalLink,
  ChevronRight,
  ShieldCheck,
  Sun,
  Moon,
  GraduationCap,
  Building2,
  Activity,
  LogOut,
  RefreshCw,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Modal } from "@/components/ui/modal";
import { Input } from "@/components/ui/input";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useTheme } from "@/components/theme-provider";
import { useAppMode } from "@/components/mode-provider";
import { useAuth } from "@/components/auth-provider";
import { AuthService } from "@/lib/api/auth-service";
import { User } from "@/types/user";

interface TopNavProps {
  onMobileMenuOpen: () => void;
}

const pageTitles: Record<
  string,
  {
    title: string;
    subtitleNormal: string;
    subtitleAcademic: string;
    pattern?: string;
  }
> = {
  "/": {
    title: "Operations Command Center",
    subtitleNormal: "Real-time city overview & integrated municipal telemetry analytics",
    subtitleAcademic: "Real-time city overview & multi-pattern simulation analytics",
  },
  "/data-streams": {
    title: "Data Stream Security Pipeline",
    subtitleNormal: "Configure real-time encryption, authentication, and compression layers for smart grid feeds",
    subtitleAcademic: "Dynamic layered stream processing using the Decorator Pattern",
    pattern: "Decorator Pattern",
  },
  "/zones": {
    title: "Hierarchical Smart Zone Tree",
    subtitleNormal: "Manage city districts, street corridors, and municipal buildings with centralized commands",
    subtitleAcademic: "Uniform recursive command dispatch using the Composite Pattern",
    pattern: "Composite Pattern",
  },
  "/complaints": {
    title: "Citizen Complaint Escalation Engine",
    subtitleNormal: "Multi-tier incident resolution routing from local field staff to city administration",
    subtitleAcademic: "Decoupled multi-tier incident routing using the Chain of Responsibility Pattern",
    pattern: "Chain of Responsibility",
  },
  "/streetlights": {
    title: "Smart Streetlight Grid Manager",
    subtitleNormal: "Monitor and manage municipal streetlights with centralized hardware profiles",
    subtitleAcademic: "High-scale memory optimization using the Flyweight Pattern",
    pattern: "Flyweight Pattern",
  },
  "/policies": {
    title: "City Policy Rule Engine",
    subtitleNormal: "Automated municipal rule compliance checking against live city sensors",
    subtitleAcademic: "Domain-specific language parsing & evaluation using the Interpreter Pattern",
    pattern: "Interpreter Pattern",
  },
  "/test-center": {
    title: "System Diagnostics & Scenarios",
    subtitleNormal: "Deterministic scenario verification for smart city subsystems",
    subtitleAcademic: "Interactive VIVA test suite & GoF design pattern academic justifications",
    pattern: "All 5 Patterns",
  },
  "/settings": {
    title: "System & Demo Settings",
    subtitleNormal: "Frontend interface preferences, mode switching, and sample data reset",
    subtitleAcademic: "Frontend interface preferences, pattern mode switching, and architectural documentation",
  },
};

export function TopNav({ onMobileMenuOpen }: TopNavProps) {
  const pathname = usePathname();
  const router = useRouter();
  const { theme, toggleTheme, mounted: themeMounted } = useTheme();
  const { mode, toggleMode, isAcademic } = useAppMode();
  const { user, logout, switchUser } = useAuth();
  const currentTheme = themeMounted ? theme : "light";
  const [searchOpen, setSearchOpen] = React.useState(false);
  const [notificationsOpen, setNotificationsOpen] = React.useState(false);
  const [searchQuery, setSearchQuery] = React.useState("");
  const [profileOpen, setProfileOpen] = React.useState(false);
  const [availableUsers, setAvailableUsers] = React.useState<User[]>([]);

  React.useEffect(() => {
    AuthService.getDemoUsers()
      .then((users) => setAvailableUsers(users))
      .catch(() => {});
  }, []);

  const currentMeta = pageTitles[pathname] || {
    title: "SmartCity360",
    subtitleNormal: "Smart City Management System",
    subtitleAcademic: "Smart City Management System (OODP II)",
  };

  const sampleNotifications = [
    {
      id: "notif-1",
      title: "Complaint Escalation Required",
      message: "Ticket CMP-7701 (Chemical Spill) auto-promoted to City Manager.",
      time: "8 min ago",
      type: "critical",
    },
    {
      id: "notif-2",
      title: "Policy Violation Flagged",
      message: "Acoustic sensor registered 68.4 dB exceeding 60 dB limit on Silicon Promenade.",
      time: "24 min ago",
      type: "warning",
    },
    {
      id: "notif-3",
      title: "Stream Security Layer Configured",
      message: "North Metro Grid Feed attached HMAC + AES-GCM + Snappy pipeline.",
      time: "48 min ago",
      type: "info",
    },
  ];

  return (
    <>
      <header className="sticky top-0 z-30 flex h-16 w-full items-center justify-between border-b border-slate-200 dark:border-slate-800/80 bg-white/85 dark:bg-[#080d1a]/80 px-4 md:px-6 backdrop-blur-md transition-colors duration-200">
        {/* Left: Mobile hamburger & Breadcrumb / Title */}
        <div className="flex items-center gap-3">
          <button
            onClick={onMobileMenuOpen}
            className="flex h-9 w-9 items-center justify-center rounded-lg border border-slate-200 dark:border-slate-700/60 bg-slate-100 dark:bg-slate-800/50 text-slate-700 dark:text-slate-300 hover:text-black dark:hover:text-white lg:hidden"
          >
            <Menu className="h-5 w-5" />
          </button>

          <div className="flex flex-col">
            <div className="flex items-center gap-1.5 text-[11px] font-medium text-slate-500 dark:text-slate-400">
              <Link href="/" className="hover:text-cyan-600 dark:hover:text-cyan-400 transition-colors">
                SmartCity360
              </Link>
              <ChevronRight className="h-3 w-3 text-slate-400 dark:text-slate-600" />
              <span className="text-slate-800 dark:text-slate-200 capitalize">
                {pathname === "/" ? "Dashboard" : pathname.replace("/", "").replace("-", " ")}
              </span>
              {/* Only show pattern badge in breadcrumb when Academic Mode is ON */}
              {isAcademic && currentMeta.pattern && (
                <>
                  <span className="text-slate-300 dark:text-slate-600">•</span>
                  <span className="rounded bg-purple-50 dark:bg-purple-950/70 border border-purple-200 dark:border-purple-800/50 px-1.5 py-0.2 text-[10px] font-semibold text-purple-700 dark:text-purple-300">
                    {currentMeta.pattern}
                  </span>
                </>
              )}
            </div>
            <h1 className="text-sm md:text-base font-bold text-slate-900 dark:text-white tracking-tight truncate max-w-[240px] md:max-w-md">
              {pathname === "/test-center" && !isAcademic
                ? "System Diagnostics & Scenarios"
                : currentMeta.title}
            </h1>
          </div>
        </div>

        {/* Right: Search, Mode Toggle (Normal vs Academic), Theme Toggle, Notifications, Profile Demo */}
        <div className="flex items-center gap-2 sm:gap-2.5">
          {/* Global Search Shortcut */}
          <button
            onClick={() => setSearchOpen(true)}
            className="hidden xl:flex items-center gap-2 rounded-xl border border-slate-200 dark:border-slate-700/60 bg-slate-100/80 dark:bg-slate-900/60 px-3 py-1.5 text-xs text-slate-600 dark:text-slate-400 hover:border-slate-300 dark:hover:border-slate-600 hover:text-slate-900 dark:hover:text-slate-200 transition-all shadow-sm"
          >
            <Search className="h-3.5 w-3.5 text-slate-500 dark:text-slate-400" />
            <span>Search modules, zones, rules...</span>
            <kbd className="ml-2 rounded border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-1.5 py-0.5 text-[10px] text-slate-500 dark:text-slate-400">
              ⌘K
            </kbd>
          </button>

          <button
            onClick={() => setSearchOpen(true)}
            className="flex xl:hidden h-9 w-9 items-center justify-center rounded-lg border border-slate-200 dark:border-slate-700/60 bg-slate-100 dark:bg-slate-800/50 text-slate-700 dark:text-slate-300"
          >
            <Search className="h-4 w-4" />
          </button>

          {/* Test Center Quick Link */}
          <Link href="/test-center" className="hidden lg:block">
            <Button variant="glass" size="sm" className="gap-1.5 text-xs">
              {isAcademic ? (
                <>
                  <ShieldCheck className="h-3.5 w-3.5 text-purple-600 dark:text-purple-400" />
                  <span>VIVA Suite</span>
                </>
              ) : (
                <>
                  <Activity className="h-3.5 w-3.5 text-cyan-600 dark:text-cyan-400" />
                  <span>Diagnostics</span>
                </>
              )}
            </Button>
          </Link>

          {/* MODE TOGGLE BUTTON: Real-World Normal Mode vs Academic / Pattern Mode */}
          <button
            onClick={toggleMode}
            className={`flex items-center gap-1.5 sm:gap-2 rounded-xl px-2.5 sm:px-3 py-1.5 text-xs font-semibold transition-all shadow-xs border ${
              isAcademic
                ? "border-purple-300 dark:border-purple-500/60 bg-purple-50 dark:bg-purple-950/40 text-purple-800 dark:text-purple-300 ring-1 ring-purple-400/30 hover:bg-purple-100 dark:hover:bg-purple-900/50"
                : "border-slate-200 dark:border-slate-700/80 bg-white dark:bg-slate-900/80 text-slate-700 dark:text-slate-300 hover:border-cyan-400 dark:hover:border-cyan-500"
            }`}
            title={
              isAcademic
                ? "Academic & Pattern Mode is ON (showing GoF pattern labels, UML notes, and VIVA banners). Click to switch to clean Real-World Normal Mode."
                : "Normal Mode is active (clean enterprise interface). Click to reveal GoF Design Pattern banners and VIVA academic demonstrator."
            }
          >
            {isAcademic ? (
              <>
                <GraduationCap className="h-4 w-4 text-purple-600 dark:text-purple-400" />
                <span className="hidden sm:inline">Pattern Mode</span>
                <span className="rounded bg-purple-200 dark:bg-purple-800/80 px-1.5 py-0.2 text-[9px] font-mono text-purple-900 dark:text-purple-200 font-bold">
                  ON
                </span>
              </>
            ) : (
              <>
                <Building2 className="h-4 w-4 text-cyan-600 dark:text-cyan-400" />
                <span className="hidden sm:inline">Normal Mode</span>
                <span className="text-[10px] text-cyan-700 dark:text-cyan-400 font-medium">Show Patterns 🎓</span>
              </>
            )}
          </button>

          {/* Theme Toggle Button (Light / Dark) */}
          <button
            onClick={toggleTheme}
            className="flex h-9 w-9 items-center justify-center rounded-lg border border-slate-200 dark:border-slate-700/60 bg-slate-100/80 dark:bg-slate-900/60 text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-800 transition-colors"
            title={`Switch to ${currentTheme === "light" ? "Dark" : "Light"} Mode`}
          >
            {currentTheme === "light" ? (
              <Moon className="h-4 w-4 text-slate-700" />
            ) : (
              <Sun className="h-4 w-4 text-amber-400" />
            )}
          </button>

          {/* Notifications Drawer Toggle */}
          <div className="relative">
            <button
              onClick={() => setNotificationsOpen(true)}
              className="relative flex h-9 w-9 items-center justify-center rounded-lg border border-slate-200 dark:border-slate-700/60 bg-slate-100/80 dark:bg-slate-900/60 text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-800 transition-colors"
            >
              <Bell className="h-4 w-4" />
              <span className="absolute top-1.5 right-1.5 h-2 w-2 rounded-full bg-rose-500 animate-pulse" />
            </button>
          </div>

          {/* User Profile Pill */}
          <div className="relative">
            <button
              onClick={() => setProfileOpen(true)}
              className="flex items-center gap-2 rounded-xl border border-slate-200 dark:border-slate-700/60 bg-white dark:bg-slate-900/60 p-1.5 pr-3 hover:border-amber-400 dark:hover:border-amber-500/60 transition-colors shadow-sm"
            >
              <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-gradient-to-tr from-amber-500 to-amber-600 text-xs font-bold text-white shadow-sm">
                {user?.avatarInitials || "OP"}
              </div>
              <div className="hidden 2xl:flex flex-col text-left">
                <span className="text-xs font-semibold text-slate-800 dark:text-slate-200">
                  {user?.fullName || "Operator"}
                </span>
                <span className="text-[10px] text-amber-600 dark:text-amber-400 font-medium capitalize">
                  {user?.role ? user.role.replace("_", " ").toLowerCase() : "Municipal Staff"}
                </span>
              </div>
            </button>
          </div>
        </div>
      </header>

      {/* Global Search Modal */}
      <Modal
        isOpen={searchOpen}
        onClose={() => setSearchOpen(false)}
        title="SmartCity360 Global Navigation"
        description="Jump to any module, zone node, policy or streetlight profile"
        maxWidth="lg"
      >
        <div className="space-y-4">
          <Input
            placeholder="Type to search modules, commands, or zones..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            autoFocus
          />

          <div className="space-y-2 pt-2">
            <p className="text-[11px] font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">
              City Modules &amp; Shortcuts
            </p>
            <div className="grid grid-cols-1 gap-2">
              {[
                {
                  title: isAcademic ? "Module A: Data Streams" : "Data Streams Management",
                  subtitle: isAcademic ? "Decorator Pattern" : "Security & Processing Pipeline",
                  href: "/data-streams",
                },
                {
                  title: isAcademic ? "Module B: Zone Hierarchy" : "Urban Zone Infrastructure",
                  subtitle: isAcademic ? "Composite Pattern" : "City → District → Street Hierarchy",
                  href: "/zones",
                },
                {
                  title: isAcademic ? "Module C: Citizen Complaints" : "Citizen Incident Escalation",
                  subtitle: isAcademic ? "Chain of Responsibility" : "Multi-Tier Resolution Routing",
                  href: "/complaints",
                },
                {
                  title: isAcademic ? "Module D: Smart Streetlights" : "Smart Streetlight Fleet",
                  subtitle: isAcademic ? "Flyweight Pattern" : "Centralized Profile Management",
                  href: "/streetlights",
                },
                {
                  title: isAcademic ? "Module E: City Policy Interpreter" : "City Policy & Compliance Engine",
                  subtitle: isAcademic ? "Interpreter Pattern" : "Real-Time Sensor Rules",
                  href: "/policies",
                },
                {
                  title: isAcademic ? "VIVA Test Center" : "System Diagnostics & Scenarios",
                  subtitle: isAcademic ? "Interactive 5-Pattern Verification" : "Deterministic Subsystem Tests",
                  href: "/test-center",
                },
              ]
                .filter(
                  (item) =>
                    !searchQuery ||
                    item.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                    item.subtitle.toLowerCase().includes(searchQuery.toLowerCase())
                )
                .map((item) => (
                  <Link
                    key={item.href}
                    href={item.href}
                    onClick={() => setSearchOpen(false)}
                    className="flex items-center justify-between rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950/60 p-3 hover:border-cyan-500/50 hover:bg-slate-100 dark:hover:bg-slate-900 transition-all"
                  >
                    <div>
                      <p className="text-xs font-semibold text-slate-900 dark:text-white">{item.title}</p>
                      <p className="text-[11px] text-cyan-700 dark:text-cyan-400">{item.subtitle}</p>
                    </div>
                    <ChevronRight className="h-4 w-4 text-slate-400" />
                  </Link>
                ))}
            </div>
          </div>
        </div>
      </Modal>

      {/* Notifications Drawer Modal */}
      <Modal
        isOpen={notificationsOpen}
        onClose={() => setNotificationsOpen(false)}
        title="Simulated City Alerts"
        description="Real-time notifications generated across smart city subsystems"
        maxWidth="md"
      >
        <div className="space-y-3">
          {sampleNotifications.map((notif) => (
            <div
              key={notif.id}
              className="flex items-start gap-3 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950/60 p-3.5"
            >
              {notif.type === "critical" && (
                <AlertTriangle className="h-5 w-5 text-rose-500 dark:text-rose-400 shrink-0 mt-0.5" />
              )}
              {notif.type === "warning" && (
                <SlidersHorizontal className="h-5 w-5 text-amber-500 dark:text-amber-400 shrink-0 mt-0.5" />
              )}
              {notif.type === "info" && (
                <CheckCircle className="h-5 w-5 text-cyan-600 dark:text-cyan-400 shrink-0 mt-0.5" />
              )}
              <div className="flex-1">
                <div className="flex items-center justify-between">
                  <p className="text-xs font-semibold text-slate-900 dark:text-white">{notif.title}</p>
                  <span className="text-[10px] text-slate-500 dark:text-slate-400">{notif.time}</span>
                </div>
                <p className="mt-1 text-xs text-slate-600 dark:text-slate-300">{notif.message}</p>
              </div>
            </div>
          ))}
        </div>
      </Modal>

      {/* Profile Modal */}
      <Modal
        isOpen={profileOpen}
        onClose={() => setProfileOpen(false)}
        title="Municipal User Profile"
        description="Active operator credentials and role-based permissions"
        maxWidth="md"
        footer={
          <div className="flex items-center justify-between w-full">
            <Button
              variant="outline"
              size="sm"
              onClick={async () => {
                await logout();
                setProfileOpen(false);
                router.push("/login");
              }}
              className="gap-1.5 text-xs text-rose-600 hover:text-rose-700 dark:text-rose-400 hover:bg-rose-50 dark:hover:bg-rose-950/30"
            >
              <LogOut className="h-3.5 w-3.5" />
              <span>Sign Out</span>
            </Button>
            <Button variant="secondary" size="sm" onClick={() => setProfileOpen(false)}>
              Close
            </Button>
          </div>
        }
      >
        <div className="space-y-4 text-xs text-slate-600 dark:text-slate-300">
          <div className="flex items-center gap-3 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950/60 p-3">
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-tr from-amber-500 to-amber-600 text-lg font-bold text-white shadow-sm">
              {user?.avatarInitials || "OP"}
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-semibold text-slate-900 dark:text-white truncate">
                {user?.fullName || "Operator"}
              </p>
              <p className="text-amber-600 dark:text-amber-400 font-medium capitalize">
                {user?.role ? user.role.replace("_", " ").toLowerCase() : "Officer"}
              </p>
              <p className="text-[11px] text-slate-500 dark:text-slate-400 truncate">
                {user?.department || "Municipal Management"} • {user?.email}
              </p>
            </div>
          </div>

          <div className="space-y-2 pt-1">
            <div className="flex items-center justify-between">
              <p className="text-[11px] font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">
                Switch Role / VIVA Demo Account
              </p>
              <span className="text-[10px] text-amber-600 dark:text-amber-400 font-medium">1-Click Switch</span>
            </div>
            <div className="grid grid-cols-2 gap-2 max-h-56 overflow-y-auto pr-1">
              {availableUsers.slice(0, 10).map((demo) => {
                const isCurrent = user?.id === demo.id;
                return (
                  <button
                    key={demo.id}
                    onClick={() => {
                      switchUser(demo);
                      setProfileOpen(false);
                    }}
                    className={`flex flex-col text-left p-2.5 rounded-xl border text-xs transition-all ${
                      isCurrent
                        ? "border-amber-500 bg-amber-50 dark:bg-amber-950/40 ring-1 ring-amber-400/40 font-semibold text-amber-950 dark:text-amber-200"
                        : "border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/60 hover:border-amber-300 hover:bg-amber-50/30 text-slate-700 dark:text-slate-300"
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="truncate">{demo.fullName}</span>
                      {isCurrent && <span className="h-1.5 w-1.5 rounded-full bg-amber-500" />}
                    </div>
                    <span className="text-[10px] text-slate-500 dark:text-slate-400 capitalize">
                      {demo.role.replace("_", " ").toLowerCase()}
                    </span>
                  </button>
                );
              })}
            </div>
          </div>
        </div>
      </Modal>
    </>
  );
}

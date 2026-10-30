import type { Metadata } from "next";
import "./globals.css";
import { AppShell } from "@/components/layout/app-shell";
import { ThemeProvider } from "@/components/theme-provider";
import { AppModeProvider } from "@/components/mode-provider";
import { AuthProvider } from "@/components/auth-provider";

export const metadata: Metadata = {
  title: "SmartCity360 — Smart City Management Platform",
  description:
    "Enterprise Smart City Management Platform demonstrating Object-Oriented Design Patterns (Decorator, Composite, Chain of Responsibility, Flyweight, Interpreter).",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="light" suppressHydrationWarning>
      <body
        suppressHydrationWarning
        className="antialiased min-h-screen bg-slate-50 dark:bg-[#080d1a] text-slate-900 dark:text-slate-100 selection:bg-cyan-500/20 selection:text-cyan-600 dark:selection:text-cyan-300"
      >
        <ThemeProvider>
          <AppModeProvider>
            <AuthProvider>
              <AppShell>{children}</AppShell>
            </AuthProvider>
          </AppModeProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}

"use client";

import * as React from "react";

export type AppMode = "normal" | "academic";

interface ModeContextType {
  mode: AppMode;
  setMode: (mode: AppMode) => void;
  toggleMode: () => void;
  isAcademic: boolean;
}

const ModeContext = React.createContext<ModeContextType | undefined>(undefined);

export function AppModeProvider({ children }: { children: React.ReactNode }) {
  const [mode, setModeState] = React.useState<AppMode>("normal");
  const [mounted, setMounted] = React.useState(false);

  React.useEffect(() => {
    try {
      const saved = localStorage.getItem("smartcity_app_mode") as AppMode | null;
      if (saved === "normal" || saved === "academic") {
        setModeState(saved);
      } else {
        setModeState("normal"); // Default to real-world normal mode
      }
    } catch {
      setModeState("normal");
    }
    setMounted(true);
  }, []);

  const setMode = (m: AppMode) => {
    setModeState(m);
    try {
      localStorage.setItem("smartcity_app_mode", m);
    } catch (e) {
      console.error(e);
    }
  };

  const toggleMode = () => {
    const next: AppMode = mode === "normal" ? "academic" : "normal";
    setMode(next);
  };

  return (
    <ModeContext.Provider
      value={{
        mode,
        setMode,
        toggleMode,
        isAcademic: mounted ? mode === "academic" : false,
      }}
    >
      {children}
    </ModeContext.Provider>
  );
}

export function useAppMode() {
  const context = React.useContext(ModeContext);
  if (!context) {
    throw new Error("useAppMode must be used within an AppModeProvider");
  }
  return context;
}

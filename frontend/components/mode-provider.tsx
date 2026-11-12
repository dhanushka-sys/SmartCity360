"use client";

import * as React from "react";

export type AppMode = "normal";

interface ModeContextType {
  mode: AppMode;
  setMode: (mode: AppMode) => void;
  toggleMode: () => void;
  isAcademic: boolean;
}

const ModeContext = React.createContext<ModeContextType | undefined>(undefined);

export function AppModeProvider({ children }: { children: React.ReactNode }) {
  // Always stay strictly in Normal Mode (Enterprise Municipal Operations)
  const [mode] = React.useState<AppMode>("normal");

  React.useEffect(() => {
    try {
      localStorage.setItem("smartcity_app_mode", "normal");
    } catch {
      // ignore
    }
  }, []);

  const setMode = () => {};
  const toggleMode = () => {};

  return (
    <ModeContext.Provider
      value={{
        mode: "normal",
        setMode,
        toggleMode,
        isAcademic: false,
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

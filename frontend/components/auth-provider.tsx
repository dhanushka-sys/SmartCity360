"use client";

import * as React from "react";
import { User } from "@/types/user";
import { AuthService, DEMO_USERS } from "@/lib/api/auth-service";

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (identifier: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  switchUser: (user: User) => void;
}

const AuthContext = React.createContext<AuthContextType | undefined>(undefined);

const STORAGE_KEY = "smartcity360_active_user";

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = React.useState<User | null>(null);
  const [isLoading, setIsLoading] = React.useState(true);

  React.useEffect(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved) {
        setUser(JSON.parse(saved));
      } else {
        // Default to Director Elena Rostova for initial view if none saved
        const defaultUser = DEMO_USERS[0];
        setUser(defaultUser);
        localStorage.setItem(STORAGE_KEY, JSON.stringify(defaultUser));
      }
    } catch {
      // Fallback
      setUser(DEMO_USERS[0]);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const login = async (identifier: string, password: string) => {
    setIsLoading(true);
    try {
      const authenticatedUser = await AuthService.login(identifier, password);
      setUser(authenticatedUser);
      localStorage.setItem(STORAGE_KEY, JSON.stringify(authenticatedUser));
    } finally {
      setIsLoading(false);
    }
  };

  const logout = async () => {
    setIsLoading(true);
    try {
      await AuthService.logout();
    } finally {
      setUser(null);
      localStorage.removeItem(STORAGE_KEY);
      setIsLoading(false);
    }
  };

  const switchUser = (newUser: User) => {
    setUser(newUser);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(newUser));
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoading,
        isAuthenticated: !!user,
        login,
        logout,
        switchUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = React.useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}


import { fetchFromBackend } from "./backend-client";
import { LoginResponse, User } from "@/types/user";

export const AuthService = {
  async login(identifier: string, password: string): Promise<User> {
    const trimmedId = identifier.trim().toLowerCase();

    const res = await fetchFromBackend<LoginResponse>("/auth/login", {
      method: "POST",
      body: JSON.stringify({ identifier: trimmedId, password }),
    });

    if (res && res.success && res.user) {
      return res.user;
    }

    if (res && res.error) {
      throw new Error(res.error);
    }

    throw new Error("Invalid username/email or password.");
  },

  async logout(): Promise<void> {
    try {
      await fetchFromBackend("/auth/logout", { method: "POST" });
    } catch {
      // Ignored
    }
  },

  async getDemoUsers(): Promise<User[]> {
    return await fetchFromBackend<User[]>("/auth/users");
  },
};

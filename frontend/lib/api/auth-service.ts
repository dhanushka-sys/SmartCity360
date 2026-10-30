import { fetchFromBackend } from "./backend-client";
import { LoginResponse, User } from "@/types/user";

export const DEMO_USERS: (User & { passwordHint: string })[] = [
  {
    id: "USR-001",
    username: "director",
    email: "director@smartcity360.gov",
    fullName: "Director Elena Rostova",
    role: "CITY_MANAGER",
    department: "Municipal Executive Directorate",
    avatarInitials: "ER",
    passwordHint: "admin123",
  },
  {
    id: "USR-002",
    username: "supervisor",
    email: "supervisor@smartcity360.gov",
    fullName: "Supervisor Marcus Vance",
    role: "SUPERVISOR",
    department: "Urban Grid & Infrastructure Oversight",
    avatarInitials: "MV",
    passwordHint: "super123",
  },
  {
    id: "USR-003",
    username: "staff",
    email: "staff@smartcity360.gov",
    fullName: "Officer Sarah Jenkins",
    role: "LOCAL_STAFF",
    department: "Central District Response Team",
    avatarInitials: "SJ",
    passwordHint: "staff123",
  },
  {
    id: "USR-004",
    username: "citizen",
    email: "citizen@smartcity360.gov",
    fullName: "Dr. Evelyn Reed",
    role: "CITIZEN",
    department: "Metropolis Civil Engineering Union",
    avatarInitials: "ER",
    passwordHint: "citizen123",
  },
];

export const AuthService = {
  async login(identifier: string, password: string): Promise<User> {
    const trimmedId = identifier.trim().toLowerCase();

    try {
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
    } catch (err: unknown) {
      if (err instanceof Error && err.message !== "Failed to fetch") {
        throw err;
      }
      // If backend offline or unreachable, fall back to demo accounts
    }

    // Fallback authentication for standalone mode
    const matched = DEMO_USERS.find(
      (u) =>
        (u.username.toLowerCase() === trimmedId || u.email.toLowerCase() === trimmedId) &&
        u.passwordHint === password
    );

    if (matched) {
      const { passwordHint: _hint, ...userWithoutHint } = matched;
      return {
        ...userWithoutHint,
        token: `LOCAL-${Date.now()}`,
      };
    }

    throw new Error("Invalid username/email or password.");
  },

  async logout(): Promise<void> {
    try {
      await fetchFromBackend("/auth/logout", { method: "POST" });
    } catch {
      // Ignore network errors on logout
    }
  },

  async getDemoUsers(): Promise<User[]> {
    try {
      const users = await fetchFromBackend<User[]>("/auth/users");
      if (users && users.length > 0) return users;
    } catch {
      // Fallback
    }
    return DEMO_USERS.map(({ passwordHint: _hint, ...u }) => u);
  },
};


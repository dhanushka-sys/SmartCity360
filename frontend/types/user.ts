export type UserRole = "CITY_MANAGER" | "SUPERVISOR" | "LOCAL_STAFF" | "CITIZEN";

export interface User {
  id: string;
  username: string;
  email: string;
  fullName: string;
  role: UserRole;
  department: string;
  avatarInitials: string;
  token?: string;
}

export interface LoginResponse {
  success: boolean;
  user?: User;
  token?: string;
  error?: string;
}


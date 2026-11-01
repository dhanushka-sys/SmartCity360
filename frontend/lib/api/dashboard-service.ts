import { fetchFromBackend } from "./backend-client";
import { CitizenComplaint } from "@/types/complaint";

export interface EnergyTrendPoint {
  time: string;
  actual: number;
  projected: number;
}

export interface ComplaintTrendPoint {
  day: string;
  submitted: number;
  resolved: number;
  escalated: number;
}

export interface DashboardActivityLog {
  id: string;
  title: string;
  description: string;
  timestamp: string;
  severity: "INFO" | "WARNING" | "CRITICAL" | "SUCCESS";
  module: string;
  patternRelated: string;
}

export interface DashboardStats {
  totalZones: number;
  districtCount: number;
  streetCount: number;
  buildingCount: number;
  totalPowerKw: number;
  totalStreams: number;
  totalPackets: number;
  totalStreetlights: number;
  onlineStreetlights: number;
  totalLightKw: number;
  totalComplaints: number;
  openComplaints: number;
  criticalComplaints: number;
  totalPolicies: number;
  activePolicies: number;
  recentComplaints: CitizenComplaint[];
  energyTrends?: EnergyTrendPoint[];
  complaintTrends?: ComplaintTrendPoint[];
  recentActivity?: DashboardActivityLog[];
}

export const DashboardService = {
  async getStats(): Promise<DashboardStats> {
    return await fetchFromBackend<DashboardStats>("/dashboard");
  },
};

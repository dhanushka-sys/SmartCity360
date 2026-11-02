export type ComplaintCategory =
  | "INFRASTRUCTURE"
  | "NOISE"
  | "TRAFFIC"
  | "WASTE"
  | "PUBLIC_SAFETY"
  | "ENVIRONMENT";

export type ComplaintSeverity = "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";

export type HandlerRole = "LOCAL_STAFF" | "SUPERVISOR" | "CITY_MANAGER" | "TRIAGE_OFFICER";

export type ComplaintStatus =
  | "SUBMITTED"
  | "ASSIGNED"
  | "ESCALATED"
  | "UNDER_REVIEW"
  | "RESOLVED";

export interface EscalationRecord {
  id: string;
  fromRole: HandlerRole | "CITIZEN";
  toRole: HandlerRole;
  timestamp: string;
  reason: string;
  automated: boolean;
  notes?: string;
}

export interface ComplaintNote {
  id: string;
  author: string;
  role: HandlerRole;
  text: string;
  createdAt: string;
}

export interface CitizenComplaint {
  id: string;
  trackingNumber: string;
  title: string;
  description: string;
  category: ComplaintCategory;
  severity: ComplaintSeverity;
  zoneId: string;
  zoneName: string;
  citizenName: string;
  citizenContact: string;
  currentHandlerRole: HandlerRole;
  status: ComplaintStatus;
  submittedAt: string;
  updatedAt: string;
  escalationHistory: EscalationRecord[];
  notes: ComplaintNote[];
  resolutionSummary?: string;
  resolvedAt?: string;
}


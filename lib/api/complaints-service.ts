import { initialComplaints } from "@/lib/mock-data/complaints-data";
import {
  CitizenComplaint,
  ComplaintCategory,
  ComplaintNote,
  ComplaintSeverity,
  EscalationRecord,
  HandlerRole,
} from "@/types/complaint";

let complaintsState: CitizenComplaint[] = [...initialComplaints];

const delay = (ms = 180) => new Promise((resolve) => setTimeout(resolve, ms));

/**
 * Chain of Responsibility:
 * Determines appropriate handler tier based on complaint severity.
 */
function resolveInitialHandler(severity: ComplaintSeverity): {
  role: HandlerRole;
  escalationHistory: EscalationRecord[];
} {
  const now = new Date().toISOString();
  if (severity === "LOW" || severity === "MEDIUM") {
    return {
      role: "LOCAL_STAFF",
      escalationHistory: [
        {
          id: `esc-${Math.random().toString(36).substring(2, 7)}`,
          fromRole: "CITIZEN",
          toRole: "LOCAL_STAFF",
          timestamp: now,
          reason: `Severity ${severity}: Direct assignment to Local Staff field handler.`,
          automated: true,
        },
      ],
    };
  } else if (severity === "HIGH") {
    return {
      role: "SUPERVISOR",
      escalationHistory: [
        {
          id: `esc-${Math.random().toString(36).substring(2, 7)}`,
          fromRole: "CITIZEN",
          toRole: "LOCAL_STAFF",
          timestamp: now,
          reason: "Intake registered.",
          automated: true,
        },
        {
          id: `esc-${Math.random().toString(36).substring(2, 7)}`,
          fromRole: "LOCAL_STAFF",
          toRole: "SUPERVISOR",
          timestamp: now,
          reason: "Severity HIGH: Exceeds Local Staff resolution limit; forwarded along Chain of Responsibility.",
          automated: true,
        },
      ],
    };
  } else {
    // CRITICAL
    return {
      role: "CITY_MANAGER",
      escalationHistory: [
        {
          id: `esc-${Math.random().toString(36).substring(2, 7)}`,
          fromRole: "CITIZEN",
          toRole: "LOCAL_STAFF",
          timestamp: now,
          reason: "Intake registered.",
          automated: true,
        },
        {
          id: `esc-${Math.random().toString(36).substring(2, 7)}`,
          fromRole: "LOCAL_STAFF",
          toRole: "SUPERVISOR",
          timestamp: now,
          reason: "Severity CRITICAL: Forwarded along chain.",
          automated: true,
        },
        {
          id: `esc-${Math.random().toString(36).substring(2, 7)}`,
          fromRole: "SUPERVISOR",
          toRole: "CITY_MANAGER",
          timestamp: now,
          reason: "Severity CRITICAL: Requires executive inter-agency authorization.",
          automated: true,
        },
      ],
    };
  }
}

export const ComplaintsService = {
  async getComplaints(): Promise<CitizenComplaint[]> {
    await delay();
    return [...complaintsState];
  },

  async getComplaintById(id: string): Promise<CitizenComplaint | undefined> {
    await delay();
    return complaintsState.find((c) => c.id === id);
  },

  async createComplaint(data: {
    title: string;
    description: string;
    category: ComplaintCategory;
    severity: ComplaintSeverity;
    zoneId: string;
    zoneName: string;
    citizenName: string;
    citizenContact: string;
  }): Promise<CitizenComplaint> {
    await delay(250);
    const { role, escalationHistory } = resolveInitialHandler(data.severity);
    const now = new Date().toISOString();

    const newComplaint: CitizenComplaint = {
      ...data,
      id: `CMP-${Math.floor(7700 + Math.random() * 2000)}`,
      trackingNumber: `CT-2026-${Math.floor(1000 + Math.random() * 9000)}`,
      currentHandlerRole: role,
      status: role === "LOCAL_STAFF" ? "ASSIGNED" : "ESCALATED",
      submittedAt: now,
      updatedAt: now,
      escalationHistory,
      notes: [
        {
          id: `note-${Math.random().toString(36).substring(2, 7)}`,
          author: "SmartCity Automated Dispatcher",
          role: role,
          text: `Complaint evaluated with ${data.severity} severity and assigned to ${role.replace("_", " ")} handler.`,
          createdAt: now,
        },
      ],
    };

    complaintsState = [newComplaint, ...complaintsState];
    return newComplaint;
  },

  async escalateComplaint(
    complaintId: string,
    reason: string,
    customToRole?: HandlerRole
  ): Promise<CitizenComplaint> {
    await delay(250);
    const complaint = complaintsState.find((c) => c.id === complaintId);
    if (!complaint) throw new Error("Complaint not found");

    let nextRole: HandlerRole;
    if (customToRole) {
      nextRole = customToRole;
    } else {
      if (complaint.currentHandlerRole === "LOCAL_STAFF") {
        nextRole = "SUPERVISOR";
      } else if (complaint.currentHandlerRole === "SUPERVISOR") {
        nextRole = "CITY_MANAGER";
      } else {
        throw new Error("Complaint is already at the highest escalation tier (City Manager).");
      }
    }

    const now = new Date().toISOString();
    const escalationRecord: EscalationRecord = {
      id: `esc-${Math.random().toString(36).substring(2, 7)}`,
      fromRole: complaint.currentHandlerRole,
      toRole: nextRole,
      timestamp: now,
      reason,
      automated: false,
      notes: `Escalated along Chain of Responsibility to ${nextRole.replace("_", " ")}.`,
    };

    const newNote: ComplaintNote = {
      id: `note-${Math.random().toString(36).substring(2, 7)}`,
      author: `${complaint.currentHandlerRole.replace("_", " ")} Officer`,
      role: complaint.currentHandlerRole,
      text: `Escalation dispatched to ${nextRole.replace("_", " ")}. Reason: ${reason}`,
      createdAt: now,
    };

    complaint.currentHandlerRole = nextRole;
    complaint.status = "ESCALATED";
    complaint.updatedAt = now;
    complaint.escalationHistory.push(escalationRecord);
    complaint.notes.push(newNote);

    return { ...complaint };
  },

  async addNote(complaintId: string, text: string, author: string, role: HandlerRole): Promise<CitizenComplaint> {
    await delay(180);
    const complaint = complaintsState.find((c) => c.id === complaintId);
    if (!complaint) throw new Error("Complaint not found");

    const note: ComplaintNote = {
      id: `note-${Math.random().toString(36).substring(2, 7)}`,
      author,
      role,
      text,
      createdAt: new Date().toISOString(),
    };

    complaint.notes.push(note);
    complaint.updatedAt = new Date().toISOString();
    return { ...complaint };
  },

  async resolveComplaint(complaintId: string, resolutionSummary: string): Promise<CitizenComplaint> {
    await delay(250);
    const complaint = complaintsState.find((c) => c.id === complaintId);
    if (!complaint) throw new Error("Complaint not found");

    const now = new Date().toISOString();
    complaint.status = "RESOLVED";
    complaint.resolutionSummary = resolutionSummary;
    complaint.resolvedAt = now;
    complaint.updatedAt = now;

    complaint.notes.push({
      id: `note-${Math.random().toString(36).substring(2, 7)}`,
      author: `${complaint.currentHandlerRole.replace("_", " ")} Handler`,
      role: complaint.currentHandlerRole,
      text: `Ticket resolved: ${resolutionSummary}`,
      createdAt: now,
    });

    return { ...complaint };
  },
};


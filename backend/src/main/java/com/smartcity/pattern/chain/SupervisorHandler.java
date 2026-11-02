package com.smartcity.pattern.chain;

import com.smartcity.model.Complaint;

public class SupervisorHandler extends ComplaintHandler {

    @Override
    public ComplaintRoutingResult handle(Complaint complaint) {
        String severity = complaint.getSeverity() != null ? complaint.getSeverity().toUpperCase() : "MEDIUM";

        if ("HIGH".equals(severity)) {
            complaint.setCurrentHandlerRole("SUPERVISOR");
            complaint.setStatus("ESCALATED");
            ComplaintRoutingResult result = new ComplaintRoutingResult(
                    complaint.getId(),
                    severity,
                    "SUPERVISOR",
                    "Escalated to District Supervisor for departmental coordination",
                    true
            );
            result.getRouteHistory().add("LOCAL_STAFF -> SUPERVISOR");
            return result;
        }

        if (this.nextHandler != null) {
            ComplaintRoutingResult result = this.nextHandler.handle(complaint);
            result.getRouteHistory().add(0, "LOCAL_STAFF -> SUPERVISOR");
            return result;
        }

        return new ComplaintRoutingResult(complaint.getId(), severity, "UNASSIGNED", "No handler could process request", false);
    }
}


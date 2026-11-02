package com.smartcity.pattern.chain;

import com.smartcity.model.Complaint;

public class LocalStaffHandler extends ComplaintHandler {

    @Override
    public ComplaintRoutingResult handle(Complaint complaint) {
        String severity = complaint.getSeverity() != null ? complaint.getSeverity().toUpperCase() : "LOW";

        if ("LOW".equals(severity) || "MEDIUM".equals(severity)) {
            complaint.setCurrentHandlerRole("LOCAL_STAFF");
            complaint.setStatus("ASSIGNED");
            ComplaintRoutingResult result = new ComplaintRoutingResult(
                    complaint.getId(),
                    severity,
                    "LOCAL_STAFF",
                    "Assigned to Local Staff for field resolution",
                    true
            );
            result.getRouteHistory().add("CITIZEN -> LOCAL_STAFF");
            return result;
        }

        if (this.nextHandler != null) {
            ComplaintRoutingResult result = this.nextHandler.handle(complaint);
            result.getRouteHistory().add(0, "CITIZEN -> LOCAL_STAFF");
            return result;
        }

        return new ComplaintRoutingResult(complaint.getId(), severity, "UNASSIGNED", "No handler could process request", false);
    }
}


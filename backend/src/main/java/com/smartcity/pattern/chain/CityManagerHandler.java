package com.smartcity.pattern.chain;

import com.smartcity.model.Complaint;

public class CityManagerHandler extends ComplaintHandler {

    @Override
    public ComplaintRoutingResult handle(Complaint complaint) {
        String severity = complaint.getSeverity() != null ? complaint.getSeverity().toUpperCase() : "HIGH";

        complaint.setCurrentHandlerRole("CITY_MANAGER");
        complaint.setStatus("ESCALATED");

        ComplaintRoutingResult result = new ComplaintRoutingResult(
                complaint.getId(),
                severity,
                "CITY_MANAGER",
                "Escalated to City Manager for emergency executive action",
                true
        );
        result.getRouteHistory().add("SUPERVISOR -> CITY_MANAGER");
        return result;
    }
}


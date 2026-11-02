package com.smartcity.pattern.chain;

import com.smartcity.model.Complaint;

import java.time.Instant;

public class CityManagerHandler extends ComplaintHandler {

    @Override
    public ComplaintRoutingResult handle(Complaint complaint) {
        ComplaintSeverity severity = ComplaintSeverity.parse(complaint.getSeverity());

        if (severity == ComplaintSeverity.HIGH || severity == ComplaintSeverity.CRITICAL) {
            complaint.setCurrentHandlerRole("CITY_MANAGER");
            complaint.setStatus("ESCALATED_EMERGENCY");
            String actionNote = severity == ComplaintSeverity.CRITICAL
                    ? "Emergency executive declaration dispatched to City Manager for immediate inter-agency crisis mobilization"
                    : "Escalated to City Manager for strategic infrastructure remediation";

            ComplaintRoutingResult result = new ComplaintRoutingResult(
                    complaint.getId(),
                    severity.name(),
                    "CITY_MANAGER",
                    "EXECUTIVE_ESCALATION",
                    actionNote,
                    true
            );
            result.addAuditRecord(new ComplaintAuditRecord(
                    Instant.now().toString(),
                    "SUPERVISOR",
                    "CITY_MANAGER",
                    "ROUTED_" + severity.name(),
                    "Resolved at Tier 3 municipal executive leadership"
            ));
            return result;
        }

        return passToNext(complaint);
    }
}

package com.smartcity.pattern.chain;

import com.smartcity.model.Complaint;

import java.time.Instant;

public class SupervisorHandler extends ComplaintHandler {

    @Override
    public ComplaintRoutingResult handle(Complaint complaint) {
        ComplaintSeverity severity = ComplaintSeverity.parse(complaint.getSeverity());

        if (severity == ComplaintSeverity.MEDIUM) {
            complaint.setCurrentHandlerRole("SUPERVISOR");
            complaint.setStatus("ESCALATED");
            ComplaintRoutingResult result = new ComplaintRoutingResult(
                    complaint.getId(),
                    "MEDIUM",
                    "SUPERVISOR",
                    "ESCALATED_SUPERVISOR",
                    "Escalated to District Supervisor for departmental resource coordination",
                    true
            );
            result.addAuditRecord(new ComplaintAuditRecord(
                    Instant.now().toString(),
                    "SUPERVISOR",
                    "SUPERVISOR",
                    "ROUTED_MEDIUM",
                    "Resolved at Tier 2 supervisor management level"
            ));
            return result;
        }

        ComplaintRoutingResult nextResult = passToNext(complaint);
        nextResult.addAuditRecord(new ComplaintAuditRecord(
                Instant.now().toString(),
                "SUPERVISOR",
                "CITY_MANAGER",
                "ESCALATE_TIER3",
                "Severity exceeds Tier 2 threshold; escalating to executive leadership"
        ));
        return nextResult;
    }
}

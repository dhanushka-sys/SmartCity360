package com.smartcity.pattern.chain;

import com.smartcity.model.Complaint;

import java.time.Instant;

public class LocalStaffHandler extends ComplaintHandler {

    @Override
    public ComplaintRoutingResult handle(Complaint complaint) {
        ComplaintSeverity severity = ComplaintSeverity.parse(complaint.getSeverity());

        if (severity == ComplaintSeverity.LOW) {
            complaint.setCurrentHandlerRole("LOCAL_STAFF");
            complaint.setStatus("ASSIGNED");
            ComplaintRoutingResult result = new ComplaintRoutingResult(
                    complaint.getId(),
                    "LOW",
                    "LOCAL_STAFF",
                    "ASSIGNED",
                    "Assigned to Local Staff for routine field inspection and resolution",
                    true
            );
            result.addAuditRecord(new ComplaintAuditRecord(
                    Instant.now().toString(),
                    "ENTRY_GATEWAY",
                    "LOCAL_STAFF",
                    "ROUTED_LOW",
                    "Resolved at Tier 1 local operations level"
            ));
            return result;
        }

        ComplaintRoutingResult nextResult = passToNext(complaint);
        nextResult.addAuditRecord(new ComplaintAuditRecord(
                Instant.now().toString(),
                "LOCAL_STAFF",
                "SUPERVISOR",
                "ESCALATE_TIER2",
                "Severity exceeds Tier 1 threshold; escalating upward"
        ));
        return nextResult;
    }
}

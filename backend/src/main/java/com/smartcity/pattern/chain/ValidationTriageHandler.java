package com.smartcity.pattern.chain;

import com.smartcity.model.Complaint;

import java.time.Instant;

public class ValidationTriageHandler extends ComplaintHandler {

    @Override
    public ComplaintRoutingResult handle(Complaint complaint) {
        if (complaint == null) {
            ComplaintRoutingResult nullErr = new ComplaintRoutingResult(
                    "INVALID_NULL",
                    "UNKNOWN",
                    "REJECTED_TRIAGE",
                    "VALIDATION_ERROR",
                    "Complaint payload cannot be null",
                    false
            );
            nullErr.addAuditRecord(new ComplaintAuditRecord(
                    Instant.now().toString(),
                    "ENTRY_GATEWAY",
                    "REJECTED_TRIAGE",
                    "REJECT_NULL",
                    "Null complaint rejected at triage gateway"
            ));
            return nullErr;
        }

        String rawSeverity = complaint.getSeverity();
        ComplaintSeverity parsed = ComplaintSeverity.parse(rawSeverity);
        if (parsed == null) {
            complaint.setCurrentHandlerRole("TRIAGE_DISPATCH_OFFICER");
            complaint.setStatus("PENDING_TRIAGE");
            ComplaintRoutingResult err = new ComplaintRoutingResult(
                    complaint.getId(),
                    rawSeverity != null ? rawSeverity : "MISSING",
                    "TRIAGE_DISPATCH_OFFICER",
                    "VALIDATION_REQUIRED",
                    "Missing or invalid severity ['" + rawSeverity + "']. Routed to triage officer for manual assessment; never defaulted to LOW.",
                    false
            );
            err.addAuditRecord(new ComplaintAuditRecord(
                    Instant.now().toString(),
                    "ENTRY_GATEWAY",
                    "TRIAGE_DISPATCH_OFFICER",
                    "TRIAGE_INTERCEPT",
                    "Hazard mitigation: unverified severity prevented from automatic LOW default"
            ));
            return err;
        }

        ComplaintRoutingResult nextResult = passToNext(complaint);
        nextResult.addAuditRecord(new ComplaintAuditRecord(
                Instant.now().toString(),
                "ENTRY_GATEWAY",
                "LOCAL_STAFF",
                "VALIDATED",
                "Severity verified as " + parsed.name()
        ));
        return nextResult;
    }
}

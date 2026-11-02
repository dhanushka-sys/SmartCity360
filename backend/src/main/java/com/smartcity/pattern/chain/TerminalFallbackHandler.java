package com.smartcity.pattern.chain;

import com.smartcity.model.Complaint;

import java.time.Instant;

public class TerminalFallbackHandler extends ComplaintHandler {

    @Override
    public ComplaintRoutingResult handle(Complaint complaint) {
        String cid = complaint != null ? complaint.getId() : "UNKNOWN";
        String sev = complaint != null && complaint.getSeverity() != null ? complaint.getSeverity() : "UNKNOWN";

        if (complaint != null) {
            complaint.setCurrentHandlerRole("FALLBACK_DISPATCH_DESK");
            complaint.setStatus("TERMINAL_FALLBACK_HELD");
        }

        ComplaintRoutingResult fallback = new ComplaintRoutingResult(
                cid,
                sev,
                "FALLBACK_DISPATCH_DESK",
                "FALLBACK_ASSIGNED",
                "Captured by terminal fallback handler to prevent drop hazard. Enqueued for special dispatch review.",
                true
        );
        fallback.addAuditRecord(new ComplaintAuditRecord(
                Instant.now().toString(),
                "CHAIN_TERMINUS",
                "FALLBACK_DISPATCH_DESK",
                "TERMINAL_RESCUE",
                "Guaranteed processing: complaint prevented from falling off chain"
        ));
        return fallback;
    }
}

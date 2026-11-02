package com.smartcity.pattern.chain;

import com.smartcity.model.Complaint;

import java.time.Instant;

public abstract class ComplaintHandler {

    protected ComplaintHandler nextHandler;

    public ComplaintHandler getNextHandler() {
        return this.nextHandler;
    }

    public void setNextHandler(ComplaintHandler nextHandler) {
        this.nextHandler = nextHandler;
    }

    public ComplaintHandler setNext(ComplaintHandler nextHandler) {
        this.nextHandler = nextHandler;
        return nextHandler;
    }

    public abstract ComplaintRoutingResult handle(Complaint complaint);

    protected ComplaintRoutingResult passToNext(Complaint complaint) {
        if (this.nextHandler != null) {
            return this.nextHandler.handle(complaint);
        }
        ComplaintRoutingResult unhandled = new ComplaintRoutingResult(
                complaint != null ? complaint.getId() : "UNKNOWN",
                complaint != null ? complaint.getSeverity() : "UNKNOWN",
                "UNASSIGNED",
                "CHAIN_EXHAUSTED",
                "No subsequent handler available in processing chain",
                false
        );
        unhandled.addAuditRecord(new ComplaintAuditRecord(
                Instant.now().toString(),
                getClass().getSimpleName(),
                "NONE",
                "DROP_HAZARD",
                "End of chain reached without handler assignment"
        ));
        return unhandled;
    }
}

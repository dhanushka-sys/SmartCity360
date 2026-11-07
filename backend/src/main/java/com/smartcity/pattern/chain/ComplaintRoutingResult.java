package com.smartcity.pattern.chain;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class ComplaintRoutingResult {

    private String complaintId;
    private String severity;
    private String handledByRole;
    private String status;
    private String message;
    private boolean handled;
    private final List<String> routeHistory = new ArrayList<>();
    private final List<ComplaintAuditRecord> auditTrail = new ArrayList<>();

    public ComplaintRoutingResult() {}

    public ComplaintRoutingResult(String complaintId, String severity, String handledByRole, String status, String message, boolean handled) {
        this.complaintId = complaintId;
        this.severity = severity;
        this.handledByRole = handledByRole;
        this.status = status;
        this.message = message;
        this.handled = handled;
    }

    public String getComplaintId() {
        return complaintId;
    }

    public void setComplaintId(String complaintId) {
        this.complaintId = complaintId;
    }

    public String getSeverity() {
        return severity;
    }

    public void setSeverity(String severity) {
        this.severity = severity;
    }

    public String getHandledByRole() {
        return handledByRole;
    }

    public void setHandledByRole(String handledByRole) {
        this.handledByRole = handledByRole;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public boolean isHandled() {
        return handled;
    }

    public void setHandled(boolean handled) {
        this.handled = handled;
    }

    public List<String> getRouteHistory() {
        return Collections.unmodifiableList(routeHistory);
    }

    public void setRouteHistory(List<String> routeHistory) {
        this.routeHistory.clear();
        if (routeHistory != null) {
            this.routeHistory.addAll(routeHistory);
        }
    }

    public List<ComplaintAuditRecord> getAuditTrail() {
        return Collections.unmodifiableList(auditTrail);
    }

    public void setAuditTrail(List<ComplaintAuditRecord> auditTrail) {
        this.auditTrail.clear();
        if (auditTrail != null) {
            this.auditTrail.addAll(auditTrail);
        }
    }

    public void addAuditRecord(ComplaintAuditRecord record) {
        if (record != null) {
            this.auditTrail.add(0, record);
            this.routeHistory.add(0, record.getFromRole() + " -> " + record.getToRole());
        }
    }
}


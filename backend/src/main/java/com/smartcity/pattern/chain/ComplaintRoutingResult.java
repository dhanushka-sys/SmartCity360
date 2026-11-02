package com.smartcity.pattern.chain;

import java.util.ArrayList;
import java.util.List;

public class ComplaintRoutingResult {

    private String complaintId;
    private String severity;
    private String handledByRole;
    private String message;
    private boolean handled;
    private List<String> routeHistory = new ArrayList<>();

    public ComplaintRoutingResult() {}

    public ComplaintRoutingResult(String complaintId, String severity, String handledByRole, String message, boolean handled) {
        this.complaintId = complaintId;
        this.severity = severity;
        this.handledByRole = handledByRole;
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
        return routeHistory;
    }

    public void setRouteHistory(List<String> routeHistory) {
        this.routeHistory = routeHistory;
    }
}


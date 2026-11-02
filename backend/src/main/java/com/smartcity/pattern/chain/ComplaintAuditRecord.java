package com.smartcity.pattern.chain;

public class ComplaintAuditRecord {

    private final String timestamp;
    private final String fromRole;
    private final String toRole;
    private final String action;
    private final String reason;

    public ComplaintAuditRecord(String timestamp, String fromRole, String toRole, String action, String reason) {
        this.timestamp = timestamp;
        this.fromRole = fromRole;
        this.toRole = toRole;
        this.action = action;
        this.reason = reason;
    }

    public String getTimestamp() {
        return timestamp;
    }

    public String getFromRole() {
        return fromRole;
    }

    public String getToRole() {
        return toRole;
    }

    public String getAction() {
        return action;
    }

    public String getReason() {
        return reason;
    }

    @Override
    public String toString() {
        return "[" + timestamp + "] " + fromRole + " -> " + toRole + " (" + action + "): " + reason;
    }
}


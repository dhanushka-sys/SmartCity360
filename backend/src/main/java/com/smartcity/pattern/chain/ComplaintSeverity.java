package com.smartcity.pattern.chain;

public enum ComplaintSeverity {
    LOW,
    MEDIUM,
    HIGH,
    CRITICAL;

    public static ComplaintSeverity parse(String raw) {
        if (raw == null || raw.trim().isEmpty()) {
            return null;
        }
        try {
            return ComplaintSeverity.valueOf(raw.trim().toUpperCase());
        } catch (IllegalArgumentException e) {
            return null;
        }
    }

    public static boolean isValid(String raw) {
        return parse(raw) != null;
    }
}


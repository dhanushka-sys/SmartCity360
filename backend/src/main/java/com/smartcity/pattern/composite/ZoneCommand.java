package com.smartcity.pattern.composite;

public enum ZoneCommand {
    SHUTDOWN_POWER("shutdownPower"),
    RESTORE_POWER("restorePower"),
    EMERGENCY_ISOLATE("emergencyIsolate");

    private final String commandName;

    ZoneCommand(String commandName) {
        this.commandName = commandName;
    }

    public String getCommandName() {
        return commandName;
    }

    public static ZoneCommand fromString(String text) {
        if (text == null || text.trim().isEmpty()) {
            throw new IllegalArgumentException("Command cannot be null or empty");
        }
        String clean = text.trim();
        for (ZoneCommand cmd : values()) {
            if (cmd.name().equalsIgnoreCase(clean) || cmd.commandName.equalsIgnoreCase(clean)) {
                return cmd;
            }
        }
        throw new IllegalArgumentException("Invalid or unsupported zone command: '" + text + "'. Supported: shutdownPower, restorePower, emergencyIsolate");
    }
}

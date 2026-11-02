package com.smartcity.pattern.composite;

public class BuildingLeaf extends ZoneComponent {

    private final double baselinePowerKw;
    private double currentPowerKw;
    private String status;

    public BuildingLeaf(String id, String name, double powerUsageKw) {
        super(id, name, "BUILDING");
        if (powerUsageKw < 0) {
            throw new IllegalArgumentException("Power consumption cannot be negative");
        }
        this.baselinePowerKw = powerUsageKw;
        this.currentPowerKw = powerUsageKw;
        this.status = "ONLINE";
    }

    @Override
    public void executeCommand(ZoneCommand command) {
        if (command == null) {
            throw new IllegalArgumentException("Command cannot be null");
        }
        switch (command) {
            case SHUTDOWN_POWER:
                this.status = "OFFLINE";
                this.currentPowerKw = 0.0;
                break;
            case RESTORE_POWER:
                this.status = "ONLINE";
                this.currentPowerKw = this.baselinePowerKw;
                break;
            case EMERGENCY_ISOLATE:
                this.status = "ISOLATED";
                this.currentPowerKw = 0.0;
                break;
        }
    }

    @Override
    public double getPowerConsumption() {
        return this.currentPowerKw;
    }

    public double getBaselinePowerKw() {
        return this.baselinePowerKw;
    }

    @Override
    public String getStatus() {
        return this.status;
    }
}

package com.smartcity.pattern.composite;

public class BuildingLeaf extends ZoneComponent {
    private double powerUsageKw;
    private String status;

    public BuildingLeaf(String id, String name, double powerUsageKw) {
        super(id, name, "BUILDING");
        this.powerUsageKw = powerUsageKw;
        this.status = "ONLINE";
    }

    @Override
    public void executeCommand(String command) {
        if ("shutdownPower".equalsIgnoreCase(command)) {
            this.status = "OFFLINE";
            this.powerUsageKw = 0.0;
        } else if ("restorePower".equalsIgnoreCase(command)) {
            this.status = "ONLINE";
            this.powerUsageKw = 150.0;
        }
    }

    @Override
    public double getTotalPowerConsumption() {
        return powerUsageKw;
    }

    public String getStatus() {
        return status;
    }
}


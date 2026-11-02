package com.smartcity.pattern.flyweight;

public class NaiveHeavyStreetlight {

    private final String poleId;
    private final double latitude;
    private final double longitude;
    private int brightnessLevel;
    private String operationalStatus;
    private final String model;
    private final String lampType;
    private final int wattage;
    private final int maxLumens;
    private final int colorTemperatureK;
    private final String firmwareVersion;

    public NaiveHeavyStreetlight(String poleId, double latitude, double longitude,
                                 String model, String lampType, int wattage, int maxLumens,
                                 int colorTemperatureK, String firmwareVersion) {
        this.poleId = poleId;
        this.latitude = latitude;
        this.longitude = longitude;
        this.model = new String(model);
        this.lampType = new String(lampType);
        this.wattage = wattage;
        this.maxLumens = maxLumens;
        this.colorTemperatureK = colorTemperatureK;
        this.firmwareVersion = new String(firmwareVersion);
        this.brightnessLevel = 0;
        this.operationalStatus = "ACTIVE";
    }

    public void setBrightnessLevel(int level) {
        this.brightnessLevel = level;
    }

    public String display() {
        return String.format("[%s] %s (%dW, %dK, %s) at (%.4f, %.4f) -> Brightness: %d%% [%s]",
                poleId, model, wattage, colorTemperatureK, lampType, latitude, longitude, brightnessLevel, operationalStatus);
    }
}

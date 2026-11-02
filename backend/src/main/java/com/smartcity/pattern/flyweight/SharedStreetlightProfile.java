package com.smartcity.pattern.flyweight;

public class SharedStreetlightProfile {
    private final String model;
    private final String lampType;
    private final int wattage;
    private final int maxLumens;
    private final String firmwareVersion;

    public SharedStreetlightProfile(String model, String lampType, int wattage, int maxLumens, String firmwareVersion) {
        this.model = model;
        this.lampType = lampType;
        this.wattage = wattage;
        this.maxLumens = maxLumens;
        this.firmwareVersion = firmwareVersion;
    }

    public String getModel() {
        return model;
    }

    public String getLampType() {
        return lampType;
    }

    public int getWattage() {
        return wattage;
    }

    public int getMaxLumens() {
        return maxLumens;
    }

    public String getFirmwareVersion() {
        return firmwareVersion;
    }

    public String render(String poleId, double lat, double lng, int brightness) {
        return String.format("[%s] Model: %s (%dW) at (%.4f, %.4f) -> Brightness: %d%%",
                poleId, model, wattage, lat, lng, brightness);
    }
}


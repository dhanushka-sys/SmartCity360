package com.smartcity.pattern.flyweight;

public final class SharedStreetlightProfile {

    private final String model;
    private final String lampType;
    private final int wattage;
    private final int maxLumens;
    private final int colorTemperatureK;
    private final String firmwareVersion;

    public SharedStreetlightProfile(String model, String lampType, int wattage, int maxLumens, int colorTemperatureK, String firmwareVersion) {
        if (model == null || model.trim().isEmpty()) {
            throw new IllegalArgumentException("Model cannot be null or empty");
        }
        this.model = model;
        this.lampType = lampType != null ? lampType : "LED";
        this.wattage = wattage;
        this.maxLumens = maxLumens;
        this.colorTemperatureK = colorTemperatureK;
        this.firmwareVersion = firmwareVersion != null ? firmwareVersion : "v1.0";
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

    public int getColorTemperatureK() {
        return colorTemperatureK;
    }

    public String getFirmwareVersion() {
        return firmwareVersion;
    }

    public String render(String poleId, double lat, double lng, int brightness, String status) {
        return String.format("[%s] %s (%dW, %dK, %s) at (%.4f, %.4f) -> Brightness: %d%% [%s]",
                poleId, model, wattage, colorTemperatureK, lampType, lat, lng, brightness, status);
    }
}

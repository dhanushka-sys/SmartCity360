package com.smartcity.model;

public class StreetlightProfile {

    private String id;
    private String modelName;
    private String manufacturer;
    private int wattageRating;
    private String lampType;
    private int defaultBrightness;
    private String operatingSchedule;
    private int colorTempKelvin;

    public StreetlightProfile() {}

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getModelName() {
        return modelName;
    }

    public void setModelName(String modelName) {
        this.modelName = modelName;
    }

    public String getManufacturer() {
        return manufacturer;
    }

    public void setManufacturer(String manufacturer) {
        this.manufacturer = manufacturer;
    }

    public int getWattageRating() {
        return wattageRating;
    }

    public void setWattageRating(int wattageRating) {
        this.wattageRating = wattageRating;
    }

    public String getLampType() {
        return lampType;
    }

    public void setLampType(String lampType) {
        this.lampType = lampType;
    }

    public int getDefaultBrightness() {
        return defaultBrightness;
    }

    public void setDefaultBrightness(int defaultBrightness) {
        this.defaultBrightness = defaultBrightness;
    }

    public String getOperatingSchedule() {
        return operatingSchedule;
    }

    public void setOperatingSchedule(String operatingSchedule) {
        this.operatingSchedule = operatingSchedule;
    }

    public int getColorTempKelvin() {
        return colorTempKelvin;
    }

    public void setColorTempKelvin(int colorTempKelvin) {
        this.colorTempKelvin = colorTempKelvin;
    }
}


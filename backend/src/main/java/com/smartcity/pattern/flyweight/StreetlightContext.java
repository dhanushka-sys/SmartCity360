package com.smartcity.pattern.flyweight;

public class StreetlightContext {

    private final String poleId;
    private final double latitude;
    private final double longitude;
    private int brightnessLevel;
    private String operationalStatus;
    private final SharedStreetlightProfile profile;

    public StreetlightContext(String poleId, double latitude, double longitude, SharedStreetlightProfile profile) {
        if (poleId == null || poleId.trim().isEmpty()) {
            throw new IllegalArgumentException("Pole ID cannot be null or empty");
        }
        if (profile == null) {
            throw new IllegalArgumentException("Shared profile cannot be null");
        }
        this.poleId = poleId;
        this.latitude = latitude;
        this.longitude = longitude;
        this.profile = profile;
        this.brightnessLevel = 0;
        this.operationalStatus = "ACTIVE";
    }

    public void setBrightnessLevel(int level) {
        this.brightnessLevel = Math.max(0, Math.min(100, level));
    }

    public void setOperationalStatus(String status) {
        this.operationalStatus = status != null ? status : "ACTIVE";
    }

    public String display() {
        return this.profile.render(poleId, latitude, longitude, brightnessLevel, operationalStatus);
    }

    public String getPoleId() {
        return poleId;
    }

    public double getLatitude() {
        return latitude;
    }

    public double getLongitude() {
        return longitude;
    }

    public int getBrightnessLevel() {
        return brightnessLevel;
    }

    public String getOperationalStatus() {
        return operationalStatus;
    }

    public SharedStreetlightProfile getProfile() {
        return profile;
    }
}

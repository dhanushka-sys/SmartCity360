package com.smartcity.pattern.flyweight;

public class StreetlightContext {
    private final String poleId;
    private final double latitude;
    private final double longitude;
    private int brightnessLevel;
    private final SharedStreetlightProfile profile;

    public StreetlightContext(String poleId, double latitude, double longitude, SharedStreetlightProfile profile) {
        this.poleId = poleId;
        this.latitude = latitude;
        this.longitude = longitude;
        this.profile = profile;
        this.brightnessLevel = 0;
    }

    public void setBrightnessLevel(int level) {
        this.brightnessLevel = Math.max(0, Math.min(100, level));
    }

    public String display() {
        return profile.render(poleId, latitude, longitude, brightnessLevel);
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

    public SharedStreetlightProfile getProfile() {
        return profile;
    }
}


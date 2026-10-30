package com.smartcity.model;

public class Streetlight {

    private String id;
    private String serialNumber;
    private String profileId;
    private String zoneId;
    private String zoneName;
    private String streetName;
    private double latitude;
    private double longitude;
    private String status;
    private int brightness;
    private double powerUsageKw;
    private String lastPing;

    public Streetlight() {}

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getSerialNumber() {
        return serialNumber;
    }

    public void setSerialNumber(String serialNumber) {
        this.serialNumber = serialNumber;
    }

    public String getProfileId() {
        return profileId;
    }

    public void setProfileId(String profileId) {
        this.profileId = profileId;
    }

    public String getZoneId() {
        return zoneId;
    }

    public void setZoneId(String zoneId) {
        this.zoneId = zoneId;
    }

    public String getZoneName() {
        return zoneName;
    }

    public void setZoneName(String zoneName) {
        this.zoneName = zoneName;
    }

    public String getStreetName() {
        return streetName;
    }

    public void setStreetName(String streetName) {
        this.streetName = streetName;
    }

    public double getLatitude() {
        return latitude;
    }

    public void setLatitude(double latitude) {
        this.latitude = latitude;
    }

    public double getLongitude() {
        return longitude;
    }

    public void setLongitude(double longitude) {
        this.longitude = longitude;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public int getBrightness() {
        return brightness;
    }

    public void setBrightness(int brightness) {
        this.brightness = brightness;
    }

    public double getPowerUsageKw() {
        return powerUsageKw;
    }

    public void setPowerUsageKw(double powerUsageKw) {
        this.powerUsageKw = powerUsageKw;
    }

    public String getLastPing() {
        return lastPing;
    }

    public void setLastPing(String lastPing) {
        this.lastPing = lastPing;
    }
}


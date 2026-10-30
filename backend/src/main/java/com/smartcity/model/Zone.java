package com.smartcity.model;

import java.util.ArrayList;
import java.util.List;

public class Zone {

    private String id;
    private String name;
    private String code;
    private String type;
    private String parentId;
    private String status;
    private double powerUsageKw;
    private double dailyConsumptionKwh;
    private int activeSensors;
    private int totalSensors;
    private int activeStreetlights;
    private int activeAlerts;
    private String manager;
    private Integer floors;
    private List<Zone> children = new ArrayList<>();

    public Zone() {}

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getCode() {
        return code;
    }

    public void setCode(String code) {
        this.code = code;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getParentId() {
        return parentId;
    }

    public void setParentId(String parentId) {
        this.parentId = parentId;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public double getPowerUsageKw() {
        return powerUsageKw;
    }

    public void setPowerUsageKw(double powerUsageKw) {
        this.powerUsageKw = powerUsageKw;
    }

    public double getDailyConsumptionKwh() {
        return dailyConsumptionKwh;
    }

    public void setDailyConsumptionKwh(double dailyConsumptionKwh) {
        this.dailyConsumptionKwh = dailyConsumptionKwh;
    }

    public int getActiveSensors() {
        return activeSensors;
    }

    public void setActiveSensors(int activeSensors) {
        this.activeSensors = activeSensors;
    }

    public int getTotalSensors() {
        return totalSensors;
    }

    public void setTotalSensors(int totalSensors) {
        this.totalSensors = totalSensors;
    }

    public int getActiveStreetlights() {
        return activeStreetlights;
    }

    public void setActiveStreetlights(int activeStreetlights) {
        this.activeStreetlights = activeStreetlights;
    }

    public int getActiveAlerts() {
        return activeAlerts;
    }

    public void setActiveAlerts(int activeAlerts) {
        this.activeAlerts = activeAlerts;
    }

    public String getManager() {
        return manager;
    }

    public void setManager(String manager) {
        this.manager = manager;
    }

    public Integer getFloors() {
        return floors;
    }

    public void setFloors(Integer floors) {
        this.floors = floors;
    }

    public List<Zone> getChildren() {
        return children;
    }

    public void setChildren(List<Zone> children) {
        this.children = children;
    }
}


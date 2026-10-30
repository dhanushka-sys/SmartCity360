package com.smartcity.model;

import java.util.ArrayList;
import java.util.List;

public class DataStream {

    private String id;
    private String name;
    private String sourceZoneId;
    private String sourceZoneName;
    private int meterCount;
    private String status;
    private double voltage;
    private double currentAmps;
    private double powerKw;
    private double frequencyHz;
    private double powerFactor;
    private double totalKwh;
    private long packetsProcessed;
    private double avgLatencyMs;
    private double errorRatePercent;
    private String lastProcessedAt;
    private List<ProcessingLayer> pipelineLayers = new ArrayList<>();

    public DataStream() {}

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

    public String getSourceZoneId() {
        return sourceZoneId;
    }

    public void setSourceZoneId(String sourceZoneId) {
        this.sourceZoneId = sourceZoneId;
    }

    public String getSourceZoneName() {
        return sourceZoneName;
    }

    public void setSourceZoneName(String sourceZoneName) {
        this.sourceZoneName = sourceZoneName;
    }

    public int getMeterCount() {
        return meterCount;
    }

    public void setMeterCount(int meterCount) {
        this.meterCount = meterCount;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public double getVoltage() {
        return voltage;
    }

    public void setVoltage(double voltage) {
        this.voltage = voltage;
    }

    public double getCurrentAmps() {
        return currentAmps;
    }

    public void setCurrentAmps(double currentAmps) {
        this.currentAmps = currentAmps;
    }

    public double getPowerKw() {
        return powerKw;
    }

    public void setPowerKw(double powerKw) {
        this.powerKw = powerKw;
    }

    public double getFrequencyHz() {
        return frequencyHz;
    }

    public void setFrequencyHz(double frequencyHz) {
        this.frequencyHz = frequencyHz;
    }

    public double getPowerFactor() {
        return powerFactor;
    }

    public void setPowerFactor(double powerFactor) {
        this.powerFactor = powerFactor;
    }

    public double getTotalKwh() {
        return totalKwh;
    }

    public void setTotalKwh(double totalKwh) {
        this.totalKwh = totalKwh;
    }

    public long getPacketsProcessed() {
        return packetsProcessed;
    }

    public void setPacketsProcessed(long packetsProcessed) {
        this.packetsProcessed = packetsProcessed;
    }

    public double getAvgLatencyMs() {
        return avgLatencyMs;
    }

    public void setAvgLatencyMs(double avgLatencyMs) {
        this.avgLatencyMs = avgLatencyMs;
    }

    public double getErrorRatePercent() {
        return errorRatePercent;
    }

    public void setErrorRatePercent(double errorRatePercent) {
        this.errorRatePercent = errorRatePercent;
    }

    public String getLastProcessedAt() {
        return lastProcessedAt;
    }

    public void setLastProcessedAt(String lastProcessedAt) {
        this.lastProcessedAt = lastProcessedAt;
    }

    public List<ProcessingLayer> getPipelineLayers() {
        return pipelineLayers;
    }

    public void setPipelineLayers(List<ProcessingLayer> pipelineLayers) {
        this.pipelineLayers = pipelineLayers;
    }
}


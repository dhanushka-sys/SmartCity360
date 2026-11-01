package com.smartcity.pattern.decorator;

public class EnergyStreamData implements StreamData {

    private final String streamId;
    private final String payload;

    public EnergyStreamData(String streamId, double voltage, double currentAmps, double powerKw) {
        this.streamId = streamId;
        this.payload = "{\"streamId\":\"" + streamId + "\",\"voltage\":" + voltage + ",\"currentAmps\":" + currentAmps + ",\"powerKw\":" + powerKw + "}";
    }

    @Override
    public String getData() {
        return this.payload;
    }

    @Override
    public int getPayloadSize() {
        return this.payload.getBytes().length;
    }

    @Override
    public String getDescription() {
        return "Energy Stream (" + this.streamId + ")";
    }
}

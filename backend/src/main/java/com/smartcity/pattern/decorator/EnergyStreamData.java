package com.smartcity.pattern.decorator;

import java.nio.charset.StandardCharsets;

public class EnergyStreamData implements StreamData {

    private final String streamId;
    private final String payload;
    private final byte[] payloadBytes;

    public EnergyStreamData(String streamId, double voltage, double currentAmps, double powerKw) {
        this.streamId = streamId;
        this.payload = "{\"streamId\":\"" + streamId + "\",\"voltage\":" + voltage + ",\"currentAmps\":" + currentAmps + ",\"powerKw\":" + powerKw + "}";
        this.payloadBytes = this.payload.getBytes(StandardCharsets.UTF_8);
    }

    @Override
    public String getData() {
        return this.payload;
    }

    @Override
    public byte[] getPayloadBytes() {
        return this.payloadBytes.clone();
    }

    @Override
    public int getPayloadSize() {
        return this.payloadBytes.length;
    }

    @Override
    public String getDescription() {
        return "Energy Stream (" + this.streamId + ")";
    }
}

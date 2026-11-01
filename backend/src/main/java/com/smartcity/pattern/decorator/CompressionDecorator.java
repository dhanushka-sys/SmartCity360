package com.smartcity.pattern.decorator;

public class CompressionDecorator extends StreamDataDecorator {

    public CompressionDecorator(StreamData streamData) {
        super(streamData);
    }

    @Override
    public String getData() {
        return "{\"format\":\"GZIP\",\"compressedPayload\":\"" + Integer.toHexString(this.streamData.getData().hashCode()) + "\"}";
    }

    @Override
    public int getPayloadSize() {
        return (int) (this.streamData.getPayloadSize() * 0.45);
    }

    @Override
    public String getDescription() {
        return this.streamData.getDescription() + " with Compression";
    }
}

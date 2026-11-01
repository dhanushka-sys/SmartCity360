package com.smartcity.pattern.decorator;

public abstract class StreamDataDecorator implements StreamData {

    protected StreamData streamData;

    public StreamDataDecorator(StreamData streamData) {
        this.streamData = streamData;
    }

    @Override
    public String getData() {
        return this.streamData.getData();
    }

    @Override
    public int getPayloadSize() {
        return this.streamData.getPayloadSize();
    }

    @Override
    public String getDescription() {
        return this.streamData.getDescription();
    }
}

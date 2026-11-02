package com.smartcity.pattern.decorator;

public abstract class StreamDataDecorator implements StreamData {

    protected final StreamData wrappee;

    public StreamDataDecorator(StreamData wrappee) {
        if (wrappee == null) {
            throw new IllegalArgumentException("Wrappee component cannot be null");
        }
        this.wrappee = wrappee;
    }

    public StreamData getWrappee() {
        return this.wrappee;
    }

    @Override
    public String getData() {
        return this.wrappee.getData();
    }

    @Override
    public byte[] getPayloadBytes() {
        return this.wrappee.getPayloadBytes();
    }

    @Override
    public int getPayloadSize() {
        return this.wrappee.getPayloadSize();
    }

    @Override
    public String getDescription() {
        return this.wrappee.getDescription();
    }
}

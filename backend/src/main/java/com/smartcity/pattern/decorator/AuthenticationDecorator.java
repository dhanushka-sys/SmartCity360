package com.smartcity.pattern.decorator;

public class AuthenticationDecorator extends StreamDataDecorator {

    public AuthenticationDecorator(StreamData streamData) {
        super(streamData);
    }

    @Override
    public String getData() {
        return "{\"auth\":\"HMAC-SHA256\",\"signature\":\"0x" + Integer.toHexString(this.streamData.getData().hashCode()) + "\",\"payload\":" + this.streamData.getData() + "}";
    }

    @Override
    public int getPayloadSize() {
        return getData().getBytes().length;
    }

    @Override
    public String getDescription() {
        return this.streamData.getDescription() + " with Authentication";
    }
}

package com.smartcity.pattern.decorator;

import java.util.Base64;

public class EncryptionDecorator extends StreamDataDecorator {

    public EncryptionDecorator(StreamData streamData) {
        super(streamData);
    }

    @Override
    public String getData() {
        String cipher = Base64.getEncoder().encodeToString(this.streamData.getData().getBytes());
        return "{\"cipher\":\"AES-256-GCM\",\"ciphertext\":\"" + cipher + "\"}";
    }

    @Override
    public int getPayloadSize() {
        return getData().getBytes().length;
    }

    @Override
    public String getDescription() {
        return this.streamData.getDescription() + " with Encryption";
    }
}

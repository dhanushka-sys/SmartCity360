package com.smartcity.pattern.decorator;

public interface StreamData {

    String getData();

    byte[] getPayloadBytes();

    int getPayloadSize();

    String getDescription();
}

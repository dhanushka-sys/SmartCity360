package com.smartcity.pattern.decorator;

/**
 * Component interface for SmartCity360 telemetry data streams (GoF Decorator Pattern).
 * Defines the contract for concrete stream components and dynamic security decorators.
 */
public interface StreamData {

    /**
     * Retrieves the serialized string or JSON envelope representation of the stream packet.
     *
     * @return String representation of the payload or envelope.
     */
    String getData();

    /**
     * Retrieves the exact binary representation of the underlying stream payload.
     * For raw telemetry, this is UTF-8 encoded text bytes; for compressed streams, the raw GZIP bytes;
     * for encrypted streams, the raw AES-256-GCM ciphertext bytes.
     *
     * @return A copy of the payload byte array.
     */
    byte[] getPayloadBytes();

    /**
     * Retrieves the size in bytes of the stream payload.
     * Contractual Invariant: Implementations must guarantee that {@code getPayloadSize() == getPayloadBytes().length}.
     *
     * @return Total size of the payload in bytes.
     */
    int getPayloadSize();

    /**
     * Retrieves an informational summary of the stream and its applied decorative wrappers.
     *
     * @return Description text.
     */
    String getDescription();
}


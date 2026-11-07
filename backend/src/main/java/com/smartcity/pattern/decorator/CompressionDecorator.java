package com.smartcity.pattern.decorator;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.Base64;
import java.util.zip.GZIPInputStream;
import java.util.zip.GZIPOutputStream;

public class CompressionDecorator extends StreamDataDecorator {

    private final String compressedJson;
    private final byte[] compressedBytes;
    private final int originalSize;
    private final int compressedSize;

    public CompressionDecorator(StreamData wrappee) {
        super(wrappee);
        byte[] input = wrappee.getPayloadBytes();
        this.originalSize = input.length;
        this.compressedBytes = compressBytes(input);
        this.compressedSize = this.compressedBytes.length;
        String b64 = Base64.getEncoder().encodeToString(this.compressedBytes);
        this.compressedJson = "{\"format\":\"GZIP\",\"originalBytes\":" + this.originalSize
                + ",\"compressedBytes\":" + this.compressedSize
                + ",\"data\":\"" + b64 + "\"}";
    }

    private static byte[] compressBytes(byte[] data) {
        try {
            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            try (GZIPOutputStream gzip = new GZIPOutputStream(baos)) {
                gzip.write(data);
                gzip.finish();
            }
            return baos.toByteArray();
        } catch (IOException e) {
            throw new RuntimeException("GZIP compression failure", e);
        }
    }

    public static byte[] decompress(byte[] compressed) throws IOException {
        ByteArrayInputStream bais = new ByteArrayInputStream(compressed);
        try (GZIPInputStream gzip = new GZIPInputStream(bais);
             ByteArrayOutputStream baos = new ByteArrayOutputStream()) {
            byte[] buf = new byte[256];
            int n;
            while ((n = gzip.read(buf)) != -1) {
                baos.write(buf, 0, n);
            }
            return baos.toByteArray();
        }
    }

    @Override
    public String getData() {
        return this.compressedJson;
    }

    @Override
    public byte[] getPayloadBytes() {
        return this.compressedJson.getBytes(StandardCharsets.UTF_8);
    }

    @Override
    public int getPayloadSize() {
        return this.compressedJson.getBytes(StandardCharsets.UTF_8).length;
    }

    public int getCompressedBinarySize() {
        return this.compressedSize;
    }

    public int getOriginalSize() {
        return this.originalSize;
    }

    public double getCompressionRatio() {
        if (originalSize == 0) return 1.0;
        return (double) compressedSize / (double) originalSize;
    }

    @Override
    public String getDescription() {
        return this.wrappee.getDescription() + " with GZIP-Compression";
    }
}

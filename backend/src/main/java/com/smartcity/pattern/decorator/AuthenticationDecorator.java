package com.smartcity.pattern.decorator;

import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import java.nio.charset.StandardCharsets;
import java.security.GeneralSecurityException;
import java.security.MessageDigest;
import java.util.Base64;

public class AuthenticationDecorator extends StreamDataDecorator {

    private static final byte[] FALLBACK_HMAC_KEY = "SmartCity360-Gateway-Hmac-Secret-Key-2026".getBytes(StandardCharsets.UTF_8);

    public static byte[] resolveDefaultKey() {
        String envKey = System.getenv("STREAM_HMAC_KEY");
        if (envKey != null && !envKey.trim().isEmpty()) {
            return envKey.trim().getBytes(StandardCharsets.UTF_8);
        }
        return FALLBACK_HMAC_KEY;
    }

    private final String authenticatedJson;
    private final String signatureBase64;
    private final byte[] hmacKey;

    public AuthenticationDecorator(StreamData wrappee) {
        this(wrappee, resolveDefaultKey());
    }

    public AuthenticationDecorator(StreamData wrappee, byte[] hmacKey) {
        super(wrappee);
        if (hmacKey == null || hmacKey.length == 0) {
            throw new IllegalArgumentException("HMAC key cannot be empty");
        }
        this.hmacKey = hmacKey.clone();
        String innerData = wrappee.getData();
        this.signatureBase64 = sign(innerData, this.hmacKey);
        this.authenticatedJson = "{\"auth\":\"HMAC-SHA256\",\"keyId\":\"GW-KEY-01\",\"signature\":\""
                + this.signatureBase64 + "\",\"payload\":" + innerData + "}";
    }

    public static String sign(String payload, byte[] key) {
        try {
            Mac mac = Mac.getInstance("HmacSHA256");
            mac.init(new SecretKeySpec(key, "HmacSHA256"));
            byte[] rawSig = mac.doFinal(payload.getBytes(StandardCharsets.UTF_8));
            return Base64.getEncoder().encodeToString(rawSig);
        } catch (GeneralSecurityException e) {
            throw new RuntimeException("HMAC signature generation failed", e);
        }
    }

    public static boolean verify(String payload, String expectedSignatureBase64, byte[] key) {
        String calculated = sign(payload, key);
        byte[] a = calculated.getBytes(StandardCharsets.UTF_8);
        byte[] b = expectedSignatureBase64.getBytes(StandardCharsets.UTF_8);
        return MessageDigest.isEqual(a, b);
    }

    public boolean isValid() {
        return verify(this.wrappee.getData(), this.signatureBase64, this.hmacKey);
    }

    @Override
    public String getData() {
        return this.authenticatedJson;
    }

    @Override
    public byte[] getPayloadBytes() {
        return this.authenticatedJson.getBytes(StandardCharsets.UTF_8);
    }

    @Override
    public int getPayloadSize() {
        return this.authenticatedJson.getBytes(StandardCharsets.UTF_8).length;
    }

    public String getSignatureBase64() {
        return this.signatureBase64;
    }

    @Override
    public String getDescription() {
        return this.wrappee.getDescription() + " with HMAC-SHA256-Authentication";
    }
}

package com.smartcity.pattern.decorator;

import javax.crypto.Cipher;
import javax.crypto.SecretKey;
import javax.crypto.spec.GCMParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import java.nio.charset.StandardCharsets;
import java.security.GeneralSecurityException;
import java.security.SecureRandom;
import java.util.Base64;

public class EncryptionDecorator extends StreamDataDecorator {

    public static final int GCM_IV_LENGTH = 12;
    public static final int GCM_TAG_LENGTH = 128;
    private static final byte[] FALLBACK_KEY = new byte[] {
            (byte) 0x2b, (byte) 0x7e, (byte) 0x15, (byte) 0x16,
            (byte) 0x28, (byte) 0xae, (byte) 0xd2, (byte) 0xa6,
            (byte) 0xab, (byte) 0xf7, (byte) 0x15, (byte) 0x88,
            (byte) 0x09, (byte) 0xcf, (byte) 0x4f, (byte) 0x3c,
            (byte) 0x76, (byte) 0x2e, (byte) 0x71, (byte) 0x60,
            (byte) 0xf3, (byte) 0x8b, (byte) 0x4d, (byte) 0xa5,
            (byte) 0x6a, (byte) 0x78, (byte) 0x4d, (byte) 0x90,
            (byte) 0x45, (byte) 0x19, (byte) 0x0c, (byte) 0xfe
    };

    public static byte[] resolveDefaultKey() {
        String envKey = System.getenv("STREAM_AES_KEY");
        if (envKey != null && !envKey.trim().isEmpty()) {
            try {
                byte[] decoded = Base64.getDecoder().decode(envKey.trim());
                if (decoded.length == 32) return decoded;
            } catch (IllegalArgumentException e) {
                System.err.println("[WARN] EncryptionDecorator: Invalid Base64 for STREAM_ENCRYPTION_KEY; using default 256-bit key.");
            }
        }
        return FALLBACK_KEY;
    }

    private final String encryptedJson;
    private final byte[] ivBytes;
    private final byte[] ciphertextBytes;
    private final byte[] keyBytes;

    public EncryptionDecorator(StreamData wrappee) {
        this(wrappee, resolveDefaultKey());
    }

    public EncryptionDecorator(StreamData wrappee, byte[] keyBytes) {
        super(wrappee);
        if (keyBytes == null || keyBytes.length != 32) {
            throw new IllegalArgumentException("AES-256 requires exactly 32-byte key");
        }
        this.keyBytes = keyBytes.clone();
        byte[] input = wrappee.getPayloadBytes();
        this.ivBytes = new byte[GCM_IV_LENGTH];
        new SecureRandom().nextBytes(this.ivBytes);

        try {
            SecretKey secretKey = new SecretKeySpec(this.keyBytes, "AES");
            Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
            GCMParameterSpec spec = new GCMParameterSpec(GCM_TAG_LENGTH, this.ivBytes);
            cipher.init(Cipher.ENCRYPT_MODE, secretKey, spec);
            this.ciphertextBytes = cipher.doFinal(input);
        } catch (GeneralSecurityException e) {
            throw new RuntimeException("AES-GCM encryption failed", e);
        }

        String ivB64 = Base64.getEncoder().encodeToString(this.ivBytes);
        String cipherB64 = Base64.getEncoder().encodeToString(this.ciphertextBytes);
        this.encryptedJson = "{\"cipher\":\"AES-256-GCM\",\"iv\":\"" + ivB64
                + "\",\"tagLength\":" + GCM_TAG_LENGTH
                + ",\"ciphertext\":\"" + cipherB64 + "\"}";
    }

    public static byte[] decrypt(String ivB64, String ciphertextB64, byte[] keyBytes) throws GeneralSecurityException {
        if (keyBytes == null || keyBytes.length != 32) {
            throw new IllegalArgumentException("AES-256 requires exactly 32-byte key");
        }
        byte[] iv = Base64.getDecoder().decode(ivB64);
        byte[] ciphertext = Base64.getDecoder().decode(ciphertextB64);
        SecretKey secretKey = new SecretKeySpec(keyBytes, "AES");
        Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
        GCMParameterSpec spec = new GCMParameterSpec(GCM_TAG_LENGTH, iv);
        cipher.init(Cipher.DECRYPT_MODE, secretKey, spec);
        return cipher.doFinal(ciphertext);
    }

    @Override
    public String getData() {
        return this.encryptedJson;
    }

    @Override
    public byte[] getPayloadBytes() {
        return this.encryptedJson.getBytes(StandardCharsets.UTF_8);
    }

    @Override
    public int getPayloadSize() {
        return this.encryptedJson.getBytes(StandardCharsets.UTF_8).length;
    }

    public int getCiphertextBinarySize() {
        return this.ciphertextBytes.length;
    }

    public String getIvBase64() {
        return Base64.getEncoder().encodeToString(this.ivBytes);
    }

    public String getCiphertextBase64() {
        return Base64.getEncoder().encodeToString(this.ciphertextBytes);
    }

    public byte[] getKeyBytes() {
        return this.keyBytes.clone();
    }

    @Override
    public String getDescription() {
        return this.wrappee.getDescription() + " with AES-256-GCM-Encryption";
    }
}

package com.smartcity.pattern.decorator;

import java.nio.charset.StandardCharsets;

public class Test {

    public static void main(String[] args) throws Exception {
        StreamData raw = new EnergyStreamData("STR-101", 230.5, 14.2, 3.27);
        System.out.println("1. Raw Component: " + raw.getDescription());
        System.out.println("Payload: " + raw.getData());
        System.out.println("Size: " + raw.getPayloadSize() + " bytes\n");

        StreamData compressed = new CompressionDecorator(raw);
        System.out.println("2. Layer 1 (Compression First): " + compressed.getDescription());
        System.out.println("Payload: " + compressed.getData());
        System.out.println("Compressed Size: " + compressed.getPayloadSize() + " bytes\n");

        StreamData encrypted = new EncryptionDecorator(compressed);
        System.out.println("3. Layer 2 (AES-GCM Encryption Second): " + encrypted.getDescription());
        System.out.println("Payload: " + encrypted.getData());
        System.out.println("Ciphertext Size: " + encrypted.getPayloadSize() + " bytes\n");

        StreamData authenticated = new AuthenticationDecorator(encrypted);
        System.out.println("4. Layer 3 (HMAC Authentication Third): " + authenticated.getDescription());
        System.out.println("Payload: " + authenticated.getData());
        System.out.println("Enveloped Size: " + authenticated.getPayloadSize() + " bytes\n");

        AuthenticationDecorator authLayer = (AuthenticationDecorator) authenticated;
        System.out.println("Signature Verified: " + authLayer.isValid());

        EncryptionDecorator encLayer = (EncryptionDecorator) authLayer.getWrappee();
        byte[] decryptedBytes = EncryptionDecorator.decrypt(
                encLayer.getIvBase64(),
                encLayer.getCiphertextBase64(),
                encLayer.getKeyBytes()
        );
        String decryptedJson = new String(decryptedBytes, StandardCharsets.UTF_8);
        System.out.println("Decrypted Inner Payload: " + decryptedJson);

        CompressionDecorator compLayer = (CompressionDecorator) encLayer.getWrappee();
        byte[] decompressedRaw = CompressionDecorator.decompress(
                java.util.Base64.getDecoder().decode(
                        decryptedJson.split("\"data\":\"")[1].split("\"")[0]
                )
        );
        System.out.println("Restored Original Payload: " + new String(decompressedRaw, StandardCharsets.UTF_8));
    }
}

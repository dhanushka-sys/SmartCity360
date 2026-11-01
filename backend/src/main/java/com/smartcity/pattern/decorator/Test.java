package com.smartcity.pattern.decorator;

public class Test {

    public static void main(String[] args) {
        StreamData stream1 = new EnergyStreamData("STR-101", 230.5, 14.2, 3.27);
        System.out.println(stream1.getDescription());
        System.out.println(stream1.getData());
        System.out.println("Size: " + stream1.getPayloadSize() + " bytes\n");

        StreamData stream2 = new EnergyStreamData("STR-202", 231.0, 18.5, 4.27);
        stream2 = new AuthenticationDecorator(stream2);
        System.out.println(stream2.getDescription());
        System.out.println(stream2.getData());
        System.out.println("Size: " + stream2.getPayloadSize() + " bytes\n");

        stream2 = new EncryptionDecorator(stream2);
        System.out.println(stream2.getDescription());
        System.out.println(stream2.getData());
        System.out.println("Size: " + stream2.getPayloadSize() + " bytes\n");

        stream2 = new CompressionDecorator(stream2);
        System.out.println(stream2.getDescription());
        System.out.println(stream2.getData());
        System.out.println("Size: " + stream2.getPayloadSize() + " bytes");
    }
}

package com.smartcity.pattern.flyweight;

public class Test {

    public static void main(String[] args) {
        SharedStreetlightProfile p1 = StreetlightProfileFactory.getProfile(
                "Philips SmartLum-150", "LED", 150, 18000, "v3.2");
        SharedStreetlightProfile p2 = StreetlightProfileFactory.getProfile(
                "Philips SmartLum-150", "LED", 150, 18000, "v3.2");

        System.out.println("Are profiles identical instance? " + (p1 == p2));
        System.out.println("Total Flyweights cached: " + StreetlightProfileFactory.getFlyweightCount());

        StreetlightContext light1 = new StreetlightContext("POLE-001", 6.9271, 79.8612, p1);
        light1.setBrightnessLevel(85);

        StreetlightContext light2 = new StreetlightContext("POLE-002", 6.9280, 79.8620, p2);
        light2.setBrightnessLevel(60);

        System.out.println(light1.display());
        System.out.println(light2.display());
    }
}


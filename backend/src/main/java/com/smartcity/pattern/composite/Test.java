package com.smartcity.pattern.composite;

public class Test {

    public static void main(String[] args) {
        ZoneComposite city = new ZoneComposite("CITY-01", "Metropolis Neo-Prime", "CITY");
        ZoneComposite district1 = new ZoneComposite("DIST-01", "Commercial Financial District", "DISTRICT");
        ZoneComposite street1 = new ZoneComposite("STR-01", "Boulevard of Light", "STREET");

        BuildingLeaf b1 = new BuildingLeaf("BLD-101", "Neo-Prime Tower", 450.0);
        BuildingLeaf b2 = new BuildingLeaf("BLD-102", "Tech Plaza", 320.0);

        street1.add(b1);
        street1.add(b2);
        district1.add(street1);
        city.add(district1);

        System.out.println("Zone: " + city.getName());
        System.out.println("Total Power: " + city.getTotalPowerConsumption() + " kW");

        city.executeCommand("shutdownPower");
        System.out.println("After Shutdown Power: " + city.getTotalPowerConsumption() + " kW");
        System.out.println("Building 1 Status: " + b1.getStatus());
        System.out.println("Building 2 Status: " + b2.getStatus());

        city.executeCommand("restorePower");
        System.out.println("After Restore Power: " + city.getTotalPowerConsumption() + " kW");
    }
}


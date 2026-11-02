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
        System.out.println("Child Count at City level: " + city.getChildCount());
        System.out.println("Initial Total Power: " + city.getPowerConsumption() + " kW");
        System.out.println("City Status: " + city.getStatus());

        city.executeCommand(ZoneCommand.SHUTDOWN_POWER);
        System.out.println("\nAfter 'shutdownPower':");
        System.out.println("Total Power: " + city.getPowerConsumption() + " kW");
        System.out.println("Building 1 Status: " + b1.getStatus());
        System.out.println("Building 2 Status: " + b2.getStatus());
        System.out.println("City Status: " + city.getStatus());

        city.executeCommand("restorePower");
        System.out.println("\nAfter 'restorePower':");
        System.out.println("Total Power: " + city.getPowerConsumption() + " kW");
        System.out.println("Building 1 Restored Power: " + b1.getPowerConsumption() + " kW");
        System.out.println("Building 2 Restored Power: " + b2.getPowerConsumption() + " kW");
        System.out.println("City Status: " + city.getStatus());

        street1.remove(b2);
        System.out.println("\nAfter removing Tech Plaza from Boulevard of Light:");
        System.out.println("Street 1 Child Count: " + street1.getChildCount());
        System.out.println("City Total Power: " + city.getPowerConsumption() + " kW");

        try {
            city.executeCommand("invalidCommandXYZ");
        } catch (IllegalArgumentException e) {
            System.out.println("Successfully caught invalid command: " + e.getMessage());
        }

        try {
            b1.add(new BuildingLeaf("BLD-999", "Illegal Child", 10.0));
        } catch (UnsupportedOperationException e) {
            System.out.println("Successfully caught illegal leaf mutation: " + e.getMessage());
        }
    }
}

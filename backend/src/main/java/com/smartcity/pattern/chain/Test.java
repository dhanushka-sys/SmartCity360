package com.smartcity.pattern.chain;

import com.smartcity.model.Complaint;

public class Test {

    public static void main(String[] args) {
        ComplaintHandler chain = ComplaintChainFactory.createChain();

        Complaint c1 = new Complaint();
        c1.setId("CMP-101");
        c1.setTitle("Pothole on Main Street");
        c1.setSeverity("LOW");

        Complaint c2 = new Complaint();
        c2.setId("CMP-202");
        c2.setTitle("Water Main Pipe Burst on 4th Ave");
        c2.setSeverity("HIGH");

        Complaint c3 = new Complaint();
        c3.setId("CMP-303");
        c3.setTitle("City Center Substation Transformer Fire");
        c3.setSeverity("CRITICAL");

        ComplaintRoutingResult r1 = chain.handle(c1);
        System.out.println("Complaint: " + c1.getTitle());
        System.out.println("Severity: " + c1.getSeverity());
        System.out.println("Assigned Handler: " + r1.getHandledByRole());
        System.out.println("Message: " + r1.getMessage());
        System.out.println("Route: " + String.join(" -> ", r1.getRouteHistory()) + "\n");

        ComplaintRoutingResult r2 = chain.handle(c2);
        System.out.println("Complaint: " + c2.getTitle());
        System.out.println("Severity: " + c2.getSeverity());
        System.out.println("Assigned Handler: " + r2.getHandledByRole());
        System.out.println("Message: " + r2.getMessage());
        System.out.println("Route: " + String.join(" -> ", r2.getRouteHistory()) + "\n");

        ComplaintRoutingResult r3 = chain.handle(c3);
        System.out.println("Complaint: " + c3.getTitle());
        System.out.println("Severity: " + c3.getSeverity());
        System.out.println("Assigned Handler: " + r3.getHandledByRole());
        System.out.println("Message: " + r3.getMessage());
        System.out.println("Route: " + String.join(" -> ", r3.getRouteHistory()));
    }
}


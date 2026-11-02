package com.smartcity.pattern.chain;

import com.smartcity.model.Complaint;

public class Test {

    public static void main(String[] args) {
        ComplaintHandler chain = ComplaintChainFactory.createChain();

        Complaint cLow = new Complaint();
        cLow.setId("CMP-101");
        cLow.setTitle("Pothole on Main Street");
        cLow.setSeverity("LOW");
        ComplaintRoutingResult rLow = chain.handle(cLow);
        System.out.println("1. LOW Complaint: " + cLow.getTitle());
        System.out.println("Handled Role: " + rLow.getHandledByRole() + ", Status: " + rLow.getStatus());
        System.out.println("Audit trail entries: " + rLow.getAuditTrail().size() + "\n");

        Complaint cMed = new Complaint();
        cMed.setId("CMP-102");
        cMed.setTitle("Traffic Signal Timing Fault");
        cMed.setSeverity("MEDIUM");
        ComplaintRoutingResult rMed = chain.handle(cMed);
        System.out.println("2. MEDIUM Complaint: " + cMed.getTitle());
        System.out.println("Handled Role: " + rMed.getHandledByRole() + ", Status: " + rMed.getStatus());
        System.out.println("Audit trail entries: " + rMed.getAuditTrail().size() + "\n");

        Complaint cHigh = new Complaint();
        cHigh.setId("CMP-202");
        cHigh.setTitle("Water Main Pipe Burst on 4th Ave");
        cHigh.setSeverity("HIGH");
        ComplaintRoutingResult rHigh = chain.handle(cHigh);
        System.out.println("3. HIGH Complaint: " + cHigh.getTitle());
        System.out.println("Handled Role: " + rHigh.getHandledByRole() + ", Status: " + rHigh.getStatus());
        System.out.println("Audit trail entries: " + rHigh.getAuditTrail().size() + "\n");

        Complaint cCrit = new Complaint();
        cCrit.setId("CMP-303");
        cCrit.setTitle("City Center Substation Transformer Fire");
        cCrit.setSeverity("CRITICAL");
        ComplaintRoutingResult rCrit = chain.handle(cCrit);
        System.out.println("4. CRITICAL Complaint: " + cCrit.getTitle());
        System.out.println("Handled Role: " + rCrit.getHandledByRole() + ", Status: " + rCrit.getStatus());
        System.out.println("Audit trail entries: " + rCrit.getAuditTrail().size() + "\n");

        Complaint cMissing = new Complaint();
        cMissing.setId("CMP-404");
        cMissing.setTitle("Mysterious Hum in Downtown Alley");
        cMissing.setSeverity(null);
        ComplaintRoutingResult rMissing = chain.handle(cMissing);
        System.out.println("5. MISSING Severity Complaint: " + cMissing.getTitle());
        System.out.println("Handled: " + rMissing.isHandled() + ", Role: " + rMissing.getHandledByRole());
        System.out.println("Safety Guardrail Message: " + rMissing.getMessage());
        System.out.println("Audit trail entries: " + rMissing.getAuditTrail().size() + "\n");

        Complaint cInvalid = new Complaint();
        cInvalid.setId("CMP-505");
        cInvalid.setTitle("Erratic Drone Hovering");
        cInvalid.setSeverity("APOCALYPTIC_UNSPECIFIED");
        ComplaintRoutingResult rInvalid = chain.handle(cInvalid);
        System.out.println("6. INVALID Severity Complaint: " + cInvalid.getTitle());
        System.out.println("Handled: " + rInvalid.isHandled() + ", Role: " + rInvalid.getHandledByRole());
        System.out.println("Safety Guardrail Message: " + rInvalid.getMessage() + "\n");

        ComplaintHandler brokenChain = new LocalStaffHandler();
        Complaint cOrphan = new Complaint();
        cOrphan.setId("CMP-999");
        cOrphan.setTitle("High-Voltage Arc Flash");
        cOrphan.setSeverity("HIGH");
        ComplaintRoutingResult rOrphan = brokenChain.handle(cOrphan);
        System.out.println("7. Broken Chain (No next handler attached):");
        System.out.println("Handled: " + rOrphan.isHandled() + ", Status: " + rOrphan.getStatus() + ", Message: " + rOrphan.getMessage());
    }
}

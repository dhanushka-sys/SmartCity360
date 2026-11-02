package com.smartcity.pattern.chain;

public class ComplaintChainFactory {

    public static ComplaintHandler createChain() {
        ComplaintHandler triage = new ValidationTriageHandler();
        ComplaintHandler localStaff = new LocalStaffHandler();
        ComplaintHandler supervisor = new SupervisorHandler();
        ComplaintHandler cityManager = new CityManagerHandler();
        ComplaintHandler fallback = new TerminalFallbackHandler();

        triage.setNext(localStaff);
        localStaff.setNext(supervisor);
        supervisor.setNext(cityManager);
        cityManager.setNext(fallback);

        return triage;
    }
}

package com.smartcity.pattern.chain;

public class ComplaintChainFactory {

    public static ComplaintHandler createChain() {
        ComplaintHandler localStaff = new LocalStaffHandler();
        ComplaintHandler supervisor = new SupervisorHandler();
        ComplaintHandler cityManager = new CityManagerHandler();

        localStaff.setNext(supervisor);
        supervisor.setNext(cityManager);

        return localStaff;
    }
}


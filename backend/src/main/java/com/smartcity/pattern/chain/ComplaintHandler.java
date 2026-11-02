package com.smartcity.pattern.chain;

import com.smartcity.model.Complaint;

public abstract class ComplaintHandler {

    protected ComplaintHandler nextHandler;

    public ComplaintHandler getNextHandler() {
        return nextHandler;
    }

    public void setNextHandler(ComplaintHandler nextHandler) {
        this.nextHandler = nextHandler;
    }

    public ComplaintHandler setNext(ComplaintHandler nextHandler) {
        this.nextHandler = nextHandler;
        return nextHandler;
    }

    public abstract ComplaintRoutingResult handle(Complaint complaint);
}


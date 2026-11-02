package com.smartcity.pattern.composite;

import java.util.List;

public abstract class ZoneComponent {
    protected final String id;
    protected final String name;
    protected final String type;

    public ZoneComponent(String id, String name, String type) {
        this.id = id;
        this.name = name;
        this.type = type;
    }

    public String getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public String getType() {
        return type;
    }

    public abstract void executeCommand(String command);

    public abstract double getTotalPowerConsumption();

    public void add(ZoneComponent component) {
        throw new UnsupportedOperationException();
    }

    public void remove(ZoneComponent component) {
        throw new UnsupportedOperationException();
    }

    public List<ZoneComponent> getChildren() {
        throw new UnsupportedOperationException();
    }
}


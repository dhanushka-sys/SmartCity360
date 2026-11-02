package com.smartcity.pattern.composite;

import java.util.List;

public abstract class ZoneComponent {

    protected final String id;
    protected final String name;
    protected final String type;

    public ZoneComponent(String id, String name, String type) {
        if (id == null || id.trim().isEmpty()) {
            throw new IllegalArgumentException("ZoneComponent id cannot be null or empty");
        }
        if (name == null || name.trim().isEmpty()) {
            throw new IllegalArgumentException("ZoneComponent name cannot be null or empty");
        }
        this.id = id;
        this.name = name;
        this.type = type != null ? type : "GENERIC";
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

    public abstract void executeCommand(ZoneCommand command);

    public void executeCommand(String command) {
        executeCommand(ZoneCommand.fromString(command));
    }

    public abstract double getPowerConsumption();

    public double getTotalPowerConsumption() {
        return getPowerConsumption();
    }

    public abstract String getStatus();

    public void add(ZoneComponent component) {
        throw new UnsupportedOperationException("add() is not supported on leaf component: " + getClass().getSimpleName());
    }

    public void remove(ZoneComponent component) {
        throw new UnsupportedOperationException("remove() is not supported on leaf component: " + getClass().getSimpleName());
    }

    public List<ZoneComponent> getChildren() {
        throw new UnsupportedOperationException("getChildren() is not supported on leaf component: " + getClass().getSimpleName());
    }

    public ZoneComponent getChild(int index) {
        throw new UnsupportedOperationException("getChild() is not supported on leaf component: " + getClass().getSimpleName());
    }
}

package com.smartcity.pattern.composite;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class ZoneComposite extends ZoneComponent {

    private final List<ZoneComponent> children = new ArrayList<>();

    public ZoneComposite(String id, String name, String type) {
        super(id, name, type);
    }

    @Override
    public void add(ZoneComponent component) {
        if (component == null) {
            throw new IllegalArgumentException("Cannot add null component to " + getName());
        }
        if (component == this) {
            throw new IllegalArgumentException("Cannot add composite to itself");
        }
        this.children.add(component);
    }

    @Override
    public void remove(ZoneComponent component) {
        if (component == null) {
            throw new IllegalArgumentException("Cannot remove null component from " + getName());
        }
        this.children.remove(component);
    }

    @Override
    public List<ZoneComponent> getChildren() {
        return Collections.unmodifiableList(this.children);
    }

    @Override
    public ZoneComponent getChild(int index) {
        if (index < 0 || index >= this.children.size()) {
            throw new IndexOutOfBoundsException("Child index " + index + " out of bounds for size " + this.children.size());
        }
        return this.children.get(index);
    }

    public int getChildCount() {
        return this.children.size();
    }

    @Override
    public void executeCommand(ZoneCommand command) {
        if (command == null) {
            throw new IllegalArgumentException("Command cannot be null");
        }
        for (ZoneComponent child : this.children) {
            child.executeCommand(command);
        }
    }

    @Override
    public double getPowerConsumption() {
        double total = 0.0;
        for (ZoneComponent child : this.children) {
            total += child.getPowerConsumption();
        }
        return total;
    }

    @Override
    public String getStatus() {
        if (this.children.isEmpty()) {
            return "STANDBY";
        }
        int onlineCount = 0;
        int offlineCount = 0;
        for (ZoneComponent child : this.children) {
            String s = child.getStatus();
            if ("ONLINE".equalsIgnoreCase(s)) {
                onlineCount++;
            } else if ("OFFLINE".equalsIgnoreCase(s) || "ISOLATED".equalsIgnoreCase(s)) {
                offlineCount++;
            }
        }
        if (onlineCount == this.children.size()) {
            return "ONLINE";
        }
        if (offlineCount == this.children.size()) {
            return "OFFLINE";
        }
        return "PARTIAL_OUTAGE";
    }
}

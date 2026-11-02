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
        children.add(component);
    }

    @Override
    public void remove(ZoneComponent component) {
        children.remove(component);
    }

    @Override
    public List<ZoneComponent> getChildren() {
        return Collections.unmodifiableList(children);
    }

    @Override
    public void executeCommand(String command) {
        for (ZoneComponent child : children) {
            child.executeCommand(command);
        }
    }

    @Override
    public double getTotalPowerConsumption() {
        double total = 0.0;
        for (ZoneComponent child : children) {
            total += child.getTotalPowerConsumption();
        }
        return total;
    }
}


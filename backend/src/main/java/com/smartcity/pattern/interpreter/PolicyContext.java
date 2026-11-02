package com.smartcity.pattern.interpreter;

import java.util.HashMap;
import java.util.Map;

public class PolicyContext {

    private final Map<String, Object> variables = new HashMap<>();

    public void set(String key, Object value) {
        if (key != null) {
            variables.put(key.trim().toUpperCase(), value);
        }
    }

    public Object get(String key) {
        if (key == null) return null;
        return variables.get(key.trim().toUpperCase());
    }

    public double getDouble(String key) {
        Object val = get(key);
        if (val instanceof Number) {
            return ((Number) val).doubleValue();
        }
        if (val instanceof String) {
            try {
                return Double.parseDouble(((String) val).trim());
            } catch (NumberFormatException ignored) {}
        }
        return 0.0;
    }

    public boolean has(String key) {
        if (key == null) return false;
        return variables.containsKey(key.trim().toUpperCase());
    }

    public void clear() {
        variables.clear();
    }
}

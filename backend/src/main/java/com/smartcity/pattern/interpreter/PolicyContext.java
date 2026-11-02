package com.smartcity.pattern.interpreter;

import java.util.HashMap;
import java.util.Map;

public class PolicyContext {
    private final Map<String, Object> variables = new HashMap<>();

    public void set(String key, Object value) {
        variables.put(key, value);
    }

    public Object get(String key) {
        return variables.get(key);
    }

    public double getDouble(String key) {
        Object val = variables.get(key);
        if (val instanceof Number) {
            return ((Number) val).doubleValue();
        }
        return 0.0;
    }

    public boolean has(String key) {
        return variables.containsKey(key);
    }
}


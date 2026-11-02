package com.smartcity.pattern.flyweight;

import java.util.HashMap;
import java.util.Map;

public class StreetlightProfileFactory {
    private static final Map<String, SharedStreetlightProfile> profiles = new HashMap<>();

    public static synchronized SharedStreetlightProfile getProfile(String model, String lampType, int wattage, int maxLumens, String firmware) {
        String key = model + "|" + lampType + "|" + wattage;
        if (!profiles.containsKey(key)) {
            profiles.put(key, new SharedStreetlightProfile(model, lampType, wattage, maxLumens, firmware));
        }
        return profiles.get(key);
    }

    public static int getFlyweightCount() {
        return profiles.size();
    }
}


package com.smartcity.pattern.flyweight;

import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentMap;

public class StreetlightProfileFactory {

    private static final ConcurrentMap<String, SharedStreetlightProfile> profiles = new ConcurrentHashMap<>();

    public static SharedStreetlightProfile getProfile(String model, String lampType, int wattage, int maxLumens, int colorTemperatureK, String firmware) {
        String key = (model != null ? model : "") + "|" + (lampType != null ? lampType : "") + "|" + wattage + "|" + maxLumens + "|" + colorTemperatureK + "|" + (firmware != null ? firmware : "");
        return profiles.computeIfAbsent(key, k -> new SharedStreetlightProfile(model, lampType, wattage, maxLumens, colorTemperatureK, firmware));
    }

    public static SharedStreetlightProfile getProfile(String model, String lampType, int wattage, int maxLumens, String firmware) {
        return getProfile(model, lampType, wattage, maxLumens, 4000, firmware);
    }

    public static int getFlyweightCount() {
        return profiles.size();
    }

    public static void clear() {
        profiles.clear();
    }
}

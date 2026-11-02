package com.smartcity.pattern.flyweight;

import java.lang.management.ManagementFactory;
import java.lang.management.MemoryMXBean;

public class FlyweightBenchmark {

    public static class BenchmarkResult {
        public int objectCount;
        public long naiveEstimatedBytes;
        public long flyweightEstimatedBytes;
        public long naiveAllocatedBytes;
        public long flyweightAllocatedBytes;
        public double savingsPercent;
        public long naiveTimeMs;
        public long flyweightTimeMs;
        public int flyweightPoolSize;
        public String jvmInfo;
    }

    public static BenchmarkResult runBenchmark(int count) {
        BenchmarkResult res = new BenchmarkResult();
        res.objectCount = count;
        res.jvmInfo = System.getProperty("java.vm.name") + " v" + System.getProperty("java.version")
                + " (" + System.getProperty("os.name") + " " + System.getProperty("os.arch") + ")";

        String[] models = {"Philips SmartLum-150", "Siemens CityRay-200", "Osram UrbanEco-90"};
        String[] types = {"LED", "Solar-LED", "High-Efficiency LED"};
        int[] wattages = {150, 200, 90};
        int[] lumens = {18000, 24000, 11000};
        int[] temps = {4000, 5000, 3000};
        String firmware = "v3.2.1-prod";

        int bytesPerNaiveObject = 288;
        int bytesPerFlyweightContext = 80;
        int bytesPerSharedProfile = 288;
        res.naiveEstimatedBytes = (long) count * bytesPerNaiveObject;
        res.flyweightEstimatedBytes = ((long) count * bytesPerFlyweightContext) + (3L * bytesPerSharedProfile);

        MemoryMXBean mem = ManagementFactory.getMemoryMXBean();
        settleGc();

        StreetlightProfileFactory.clear();
        long memBeforeFly = mem.getHeapMemoryUsage().getUsed();
        long t1 = System.currentTimeMillis();

        StreetlightContext[] flyArray = new StreetlightContext[count];
        for (int i = 0; i < count; i++) {
            int idx = i % 3;
            SharedStreetlightProfile p = StreetlightProfileFactory.getProfile(
                    models[idx], types[idx], wattages[idx], lumens[idx], temps[idx], firmware
            );
            flyArray[i] = new StreetlightContext(
                    "POLE-" + String.format("%06d", i),
                    6.9271 + (i * 0.0001),
                    79.8612 + (i * 0.0001),
                    p
            );
        }
        res.flyweightTimeMs = System.currentTimeMillis() - t1;
        long memAfterFly = mem.getHeapMemoryUsage().getUsed();
        res.flyweightAllocatedBytes = Math.max(1, memAfterFly - memBeforeFly);
        res.flyweightPoolSize = StreetlightProfileFactory.getFlyweightCount();

        settleGc();
        long memBeforeNaive = mem.getHeapMemoryUsage().getUsed();
        long t0 = System.currentTimeMillis();

        NaiveHeavyStreetlight[] naiveArray = new NaiveHeavyStreetlight[count];
        for (int i = 0; i < count; i++) {
            int idx = i % 3;
            naiveArray[i] = new NaiveHeavyStreetlight(
                    "POLE-" + String.format("%06d", i),
                    6.9271 + (i * 0.0001),
                    79.8612 + (i * 0.0001),
                    models[idx], types[idx], wattages[idx], lumens[idx], temps[idx], firmware
            );
        }
        res.naiveTimeMs = System.currentTimeMillis() - t0;
        long memAfterNaive = mem.getHeapMemoryUsage().getUsed();
        res.naiveAllocatedBytes = Math.max(1, memAfterNaive - memBeforeNaive);

        if (flyArray.length > 0 && naiveArray.length > 0) {
            res.savingsPercent = ((double) (res.naiveEstimatedBytes - res.flyweightEstimatedBytes) / res.naiveEstimatedBytes) * 100.0;
        }

        return res;
    }

    private static void settleGc() {
        for (int i = 0; i < 3; i++) {
            System.gc();
            try {
                Thread.sleep(50);
            } catch (InterruptedException ignored) {}
        }
    }
}

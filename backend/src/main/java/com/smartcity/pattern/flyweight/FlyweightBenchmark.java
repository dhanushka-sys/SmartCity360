package com.smartcity.pattern.flyweight;

import java.lang.management.ManagementFactory;
import java.lang.management.MemoryMXBean;
import java.util.ArrayList;
import java.util.List;

public class FlyweightBenchmark {

    public static class BenchmarkResult {
        public int objectCount;
        public long naiveEstimatedBytes;
        public long flyweightEstimatedBytes;
        public long naiveAllocatedBytes;
        public long flyweightAllocatedBytes;
        public double savingsPercent; // Analytical layout savings estimate
        public double analyticalSavingsPercent;
        public double measuredHeapSavingsPercent; // Measured HotSpot heap delta
        public long naiveTimeMs;
        public long flyweightTimeMs;
        public int flyweightPoolSize;
        public String jvmInfo;
    }

    public static class ScalingComparisonRow {
        public int count;
        public long naiveEstimatedBytes;
        public long flyweightEstimatedBytes;
        public double analyticalSavingsPercent;
        public long naiveAllocatedBytes;
        public long flyweightAllocatedBytes;
        public double measuredHeapSavingsPercent;
        public long naiveTimeMs;
        public long flyweightTimeMs;
    }

    public static List<ScalingComparisonRow> runScalingSuite() {
        int[] scales = {1000, 10000, 25000, 100000};
        List<ScalingComparisonRow> rows = new ArrayList<>();
        for (int scale : scales) {
            BenchmarkResult b = runBenchmark(scale);
            ScalingComparisonRow row = new ScalingComparisonRow();
            row.count = scale;
            row.naiveEstimatedBytes = b.naiveEstimatedBytes;
            row.flyweightEstimatedBytes = b.flyweightEstimatedBytes;
            row.analyticalSavingsPercent = b.analyticalSavingsPercent;
            row.naiveAllocatedBytes = b.naiveAllocatedBytes;
            row.flyweightAllocatedBytes = b.flyweightAllocatedBytes;
            row.measuredHeapSavingsPercent = b.measuredHeapSavingsPercent;
            row.naiveTimeMs = b.naiveTimeMs;
            row.flyweightTimeMs = b.flyweightTimeMs;
            rows.add(row);
        }
        return rows;
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
        res.analyticalSavingsPercent = ((double) (res.naiveEstimatedBytes - res.flyweightEstimatedBytes) / res.naiveEstimatedBytes) * 100.0;
        res.savingsPercent = res.analyticalSavingsPercent;

        MemoryMXBean mem = ManagementFactory.getMemoryMXBean();

        // 1. Measure Naive Heavy allocation in isolation
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

        // Discard naive array and settle GC before measuring Flyweight
        naiveArray = null;
        settleGc();

        // 2. Measure Flyweight pattern allocation in isolation
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

        if (res.naiveAllocatedBytes > 0 && res.flyweightAllocatedBytes > 0) {
            double measured = ((double) (res.naiveAllocatedBytes - res.flyweightAllocatedBytes) / res.naiveAllocatedBytes) * 100.0;
            res.measuredHeapSavingsPercent = Math.max(0.0, Math.min(99.0, measured));
        }

        flyArray = null;
        settleGc();

        return res;
    }

    private static void settleGc() {
        for (int i = 0; i < 3; i++) {
            System.gc();
            try {
                Thread.sleep(50);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            }
        }
    }
}

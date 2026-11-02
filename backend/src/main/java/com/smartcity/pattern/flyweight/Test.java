package com.smartcity.pattern.flyweight;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

public class Test {

    public static void main(String[] args) throws Exception {
        SharedStreetlightProfile p1 = StreetlightProfileFactory.getProfile(
                "Philips SmartLum-150", "LED", 150, 18000, 4000, "v3.2");
        SharedStreetlightProfile p2 = StreetlightProfileFactory.getProfile(
                "Philips SmartLum-150", "LED", 150, 18000, 4000, "v3.2");

        System.out.println("Are profiles identical instance? " + (p1 == p2));
        System.out.println("Total Flyweights cached: " + StreetlightProfileFactory.getFlyweightCount());

        StreetlightContext light1 = new StreetlightContext("POLE-001", 6.9271, 79.8612, p1);
        light1.setBrightnessLevel(85);

        StreetlightContext light2 = new StreetlightContext("POLE-002", 6.9280, 79.8620, p2);
        light2.setBrightnessLevel(60);

        System.out.println(light1.display());
        System.out.println(light2.display() + "\n");

        ExecutorService pool = Executors.newFixedThreadPool(8);
        List<Callable<SharedStreetlightProfile>> tasks = new ArrayList<>();
        for (int i = 0; i < 50; i++) {
            tasks.add(() -> StreetlightProfileFactory.getProfile("Philips SmartLum-150", "LED", 150, 18000, 4000, "v3.2"));
        }
        List<Future<SharedStreetlightProfile>> results = pool.invokeAll(tasks);
        boolean allSame = true;
        for (Future<SharedStreetlightProfile> f : results) {
            if (f.get() != p1) {
                allSame = false;
                break;
            }
        }
        pool.shutdown();
        System.out.println("Concurrent access across 8 threads produced single identical instance: " + allSame);
        System.out.println("Flyweight pool size after concurrent test: " + StreetlightProfileFactory.getFlyweightCount() + "\n");

        System.out.println("=== Running 25,000 Streetlight Memory Benchmark ===");
        FlyweightBenchmark.BenchmarkResult bench = FlyweightBenchmark.runBenchmark(25000);
        System.out.println("JVM Environment: " + bench.jvmInfo);
        System.out.println("Object Count: " + bench.objectCount);
        System.out.println("Flyweight Pool Size: " + bench.flyweightPoolSize);
        System.out.printf("Naive Memory Estimated: %.2f MB (%d bytes) in %d ms%n",
                bench.naiveEstimatedBytes / (1024.0 * 1024.0), bench.naiveEstimatedBytes, bench.naiveTimeMs);
        System.out.printf("Flyweight Memory Estimated: %.2f MB (%d bytes) in %d ms%n",
                bench.flyweightEstimatedBytes / (1024.0 * 1024.0), bench.flyweightEstimatedBytes, bench.flyweightTimeMs);
        System.out.printf("Calculated Memory Savings: %.1f%%%n", bench.savingsPercent);
    }
}

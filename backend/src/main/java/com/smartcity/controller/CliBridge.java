package com.smartcity.controller;

import com.google.gson.Gson;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import com.smartcity.model.Complaint;
import com.smartcity.model.ProcessingLayer;
import com.smartcity.pattern.chain.ComplaintAuditRecord;
import com.smartcity.pattern.chain.ComplaintChainFactory;
import com.smartcity.pattern.chain.ComplaintRoutingResult;
import com.smartcity.pattern.composite.BuildingLeaf;
import com.smartcity.pattern.composite.ZoneCommand;
import com.smartcity.pattern.composite.ZoneComponent;
import com.smartcity.pattern.composite.ZoneComposite;
import com.smartcity.pattern.decorator.AuthenticationDecorator;
import com.smartcity.pattern.decorator.CompressionDecorator;
import com.smartcity.pattern.decorator.EncryptionDecorator;
import com.smartcity.pattern.decorator.EnergyStreamData;
import com.smartcity.pattern.decorator.StreamData;
import com.smartcity.pattern.flyweight.FlyweightBenchmark;
import com.smartcity.pattern.interpreter.DslPolicyParser;
import com.smartcity.pattern.interpreter.Expression;
import com.smartcity.pattern.interpreter.PolicyContext;
import com.smartcity.test.ComprehensiveTestSuite;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.util.*;

public class CliBridge {
    private static final Gson gson = new Gson();

    public static void main(String[] args) {
        if (args.length == 0) {
            System.err.println("Usage: CliBridge <action> [args...]");
            System.exit(1);
        }

        String action = args[0];
        try {
            switch (action) {
                case "pipeline":
                    handlePipeline(args);
                    break;
                case "evaluate":
                    handleEvaluate(args);
                    break;
                case "command":
                    handleCommand(args);
                    break;
                case "complaint":
                    handleComplaint(args);
                    break;
                case "benchmark":
                    handleBenchmark(args);
                    break;
                case "test":
                    handleTest();
                    break;
                default:
                    System.err.println("Unknown action: " + action);
                    System.exit(1);
            }
        } catch (Exception e) {
            Map<String, Object> err = new HashMap<>();
            err.put("error", e.getMessage() != null ? e.getMessage() : e.getClass().getSimpleName());
            err.put("success", false);
            System.out.println(gson.toJson(err));
            System.exit(1);
        }
    }

    private static void handlePipeline(String[] args) {
        String streamId = args.length > 1 ? args[1] : "STR-001";
        double voltage = 230.5;
        double currentAmps = 14.2;
        double powerKw = 3.27;

        if (args.length > 2 && args[2] != null && !args[2].trim().isEmpty()) {
            try {
                JsonObject obj = JsonParser.parseString(args[2]).getAsJsonObject();
                if (obj.has("voltage")) voltage = obj.get("voltage").getAsDouble();
                if (obj.has("currentAmps")) currentAmps = obj.get("currentAmps").getAsDouble();
                if (obj.has("powerKw")) powerKw = obj.get("powerKw").getAsDouble();
            } catch (Exception e) {
                System.err.println("[WARN] CliBridge: Custom telemetry JSON unparseable, using standard baseline: " + e.getMessage());
            }
        }

        StreamData base = new EnergyStreamData(streamId, voltage, currentAmps, powerKw);
        int rawSize = base.getPayloadSize();
        String rawData = base.getData();

        long t0 = System.nanoTime();
        StreamData compressed = new CompressionDecorator(base);
        int compSize = compressed.getPayloadSize();
        long t1 = System.nanoTime();

        StreamData encrypted = new EncryptionDecorator(compressed);
        int encSize = encrypted.getPayloadSize();
        long t2 = System.nanoTime();

        StreamData signed = new AuthenticationDecorator(encrypted);
        int signSize = signed.getPayloadSize();
        long t3 = System.nanoTime();

        boolean verified = ((AuthenticationDecorator) signed).isValid();

        List<ProcessingLayer> layers = new ArrayList<>();
        ProcessingLayer l1 = new ProcessingLayer();
        l1.setLayerType("COMPRESSION");
        l1.setLayerName("GZIP Compression");
        l1.setLayerOrder(1);
        l1.setEnabled(true);
        layers.add(l1);

        ProcessingLayer l2 = new ProcessingLayer();
        l2.setLayerType("ENCRYPTION");
        l2.setLayerName("AES-256-GCM Encryption");
        l2.setLayerOrder(2);
        l2.setEnabled(true);
        layers.add(l2);

        ProcessingLayer l3 = new ProcessingLayer();
        l3.setLayerType("AUTHENTICATION");
        l3.setLayerName("HMAC-SHA256 Signing");
        l3.setLayerOrder(3);
        l3.setEnabled(true);
        layers.add(l3);

        Map<String, Object> resp = new LinkedHashMap<>();
        resp.put("streamId", streamId);
        resp.put("success", true);
        resp.put("rawSize", rawSize);
        resp.put("compressedSize", compSize);
        resp.put("encryptedSize", encSize);
        resp.put("authenticatedSize", signSize);
        resp.put("payloadBase64", Base64.getEncoder().encodeToString(signed.getData().getBytes(StandardCharsets.UTF_8)));
        resp.put("verified", verified);
        resp.put("compressionTimeUs", (t1 - t0) / 1000);
        resp.put("encryptionTimeUs", (t2 - t1) / 1000);
        resp.put("signingTimeUs", (t3 - t2) / 1000);
        resp.put("totalTimeUs", (t3 - t0) / 1000);
        resp.put("layers", layers);

        System.out.println(gson.toJson(resp));
    }

    private static void handleEvaluate(String[] args) {
        String expression = args.length > 1 ? args[1] : "AIR_QUALITY_INDEX > 100";
        String contextJson = args.length > 2 ? args[2] : "{}";

        PolicyContext ctx = new PolicyContext();
        if (contextJson != null && !contextJson.trim().isEmpty() && !contextJson.equals("{}")) {
            JsonObject obj = JsonParser.parseString(contextJson).getAsJsonObject();
            for (String key : obj.keySet()) {
                if (obj.get(key).isJsonPrimitive() && obj.get(key).getAsJsonPrimitive().isNumber()) {
                    ctx.set(key, obj.get(key).getAsDouble());
                } else if (obj.get(key).isJsonPrimitive() && obj.get(key).getAsJsonPrimitive().isString()) {
                    ctx.set(key, obj.get(key).getAsString());
                }
            }
        }

        long start = System.nanoTime();
        Expression ast = DslPolicyParser.parse(expression);
        boolean result = ast.interpret(ctx);
        long elapsedMicros = (System.nanoTime() - start) / 1000;

        Map<String, Object> resp = new LinkedHashMap<>();
        resp.put("success", true);
        resp.put("result", result);
        resp.put("passed", result);
        resp.put("ast", ast.toString());
        resp.put("executionTimeMicros", elapsedMicros);
        resp.put("expression", expression);

        System.out.println(gson.toJson(resp));
    }

    private static void handleCommand(String[] args) {
        String zoneId = args.length > 1 ? args[1] : "CITY_ROOT";
        String commandName = args.length > 2 ? args[2] : "restorePower";

        ZoneCommand cmd = ZoneCommand.fromString(commandName);

        ZoneComposite root = new ZoneComposite("CITY_ROOT", "Metropolis Neo-Prime", "MUNICIPALITY");
        ZoneComposite district = new ZoneComposite("DIST_NORTH", "North Sector", "DISTRICT");
        district.add(new BuildingLeaf("BLD_01", "City Hall", 120.0));
        district.add(new BuildingLeaf("BLD_02", "General Hospital", 280.0));
        root.add(district);

        root.executeCommand(cmd);

        Map<String, Object> resp = new LinkedHashMap<>();
        resp.put("success", true);
        resp.put("zoneId", zoneId);
        resp.put("command", cmd.name());
        resp.put("status", root.getStatus());
        resp.put("powerConsumptionKw", root.getPowerConsumption());

        System.out.println(gson.toJson(resp));
    }

    private static void handleComplaint(String[] args) {
        String severity = args.length > 1 ? args[1] : "LOW";
        String category = args.length > 2 ? args[2] : "STREETLIGHT_OUTAGE";
        String description = args.length > 3 ? args[3] : "Complaint description";

        Complaint complaint = new Complaint();
        complaint.setId("CMP-" + (System.currentTimeMillis() % 10000));
        complaint.setSeverity(severity);
        complaint.setCategory(category);
        complaint.setDescription(description);
        complaint.setTitle("Municipal Incident: " + category);
        complaint.setZoneId("ZONE_1");

        ComplaintRoutingResult result = ComplaintChainFactory.createChain().handle(complaint);

        Map<String, Object> resp = new LinkedHashMap<>();
        resp.put("success", true);
        resp.put("handledByRole", result.getHandledByRole());
        resp.put("status", result.getStatus());
        resp.put("message", result.getMessage());
        resp.put("auditTrail", result.getAuditTrail());

        System.out.println(gson.toJson(resp));
    }

    private static void handleBenchmark(String[] args) {
        int count = args.length > 1 ? Integer.parseInt(args[1]) : 25000;
        FlyweightBenchmark.BenchmarkResult res = FlyweightBenchmark.runBenchmark(count);

        Map<String, Object> resp = new LinkedHashMap<>();
        resp.put("success", true);
        resp.put("count", count);
        resp.put("naiveMemoryBytes", res.naiveEstimatedBytes);
        resp.put("flyweightMemoryBytes", res.flyweightEstimatedBytes);
        resp.put("savingsPercentage", res.savingsPercent);
        resp.put("measuredSavingsPercentage", res.measuredHeapSavingsPercent);
        resp.put("poolSize", res.flyweightPoolSize);
        resp.put("executionTimeMs", res.flyweightTimeMs);

        System.out.println(gson.toJson(resp));
    }

    private static void handleTest() {
        PrintStream originalOut = System.out;
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        ComprehensiveTestSuite suite = new ComprehensiveTestSuite();
        try {
            System.setOut(new PrintStream(baos, true, StandardCharsets.UTF_8));
            suite.runAllTests();
            suite.printMarkdownReport();
        } finally {
            System.setOut(originalOut);
        }

        String rawOutput = baos.toString(StandardCharsets.UTF_8);
        List<ComprehensiveTestSuite.TestResult> testResults = suite.getResults();
        int total = testResults.size();
        int passed = 0;
        for (ComprehensiveTestSuite.TestResult r : testResults) {
            if (r.passed) passed++;
        }
        int failed = total - passed;
        double passPct = total > 0 ? ((double) passed / total) * 100.0 : 0.0;

        Map<String, Object> resp = new LinkedHashMap<>();
        resp.put("success", failed == 0);
        resp.put("output", rawOutput);
        resp.put("testsRun", total);
        resp.put("testsPassed", passed);
        resp.put("testsFailed", failed);
        resp.put("passRate", String.format(Locale.US, "%.1f%%", passPct));

        System.out.println(gson.toJson(resp));
    }
}

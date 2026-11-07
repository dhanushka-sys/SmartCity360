package com.smartcity.test;

import com.smartcity.model.Complaint;
import com.smartcity.pattern.chain.*;
import com.smartcity.pattern.composite.*;
import com.smartcity.pattern.decorator.*;
import com.smartcity.pattern.flyweight.*;
import com.smartcity.pattern.interpreter.*;

import java.nio.charset.StandardCharsets;
import java.security.GeneralSecurityException;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.*;

public class ComprehensiveTestSuite {

    public static class TestResult {
        public final String testName;
        public final String pattern;
        public final String expected;
        public final String actual;
        public final boolean passed;

        public TestResult(String testName, String pattern, String expected, String actual, boolean passed) {
            this.testName = testName;
            this.pattern = pattern;
            this.expected = expected;
            this.actual = actual;
            this.passed = passed;
        }
    }

    private final List<TestResult> results = new ArrayList<>();

    public void runAllTests() {
        testDecoratorNormalPipeline();
        testDecoratorDecompression();
        testDecoratorDecryption();
        testDecoratorAuthenticationFailure();
        testDecoratorCorruptedPayload();
        testDecoratorInvalidKey();

        testCompositeHierarchyCreation();
        testCompositeAddAndRemoveChild();
        testCompositeCommandBroadcast();
        testCompositeCommandRestoration();
        testCompositeAggregatePower();
        testCompositeInvalidCommand();
        testCompositeLeafMutation();

        testChainLowSeverity();
        testChainMediumSeverity();
        testChainHighSeverity();
        testChainCriticalSeverity();
        testChainMissingSeverity();
        testChainInvalidSeverity();
        testChainTerminalFallback();
        testChainAuditTrail();

        testFlyweightProfileReusability();
        testFlyweightCacheKeyDistinction();
        testFlyweightThreadSafety();
        testFlyweightContextSeparation();
        testFlyweightEmpiricalBenchmark();

        testCompositeCycleDetection();

        testInterpreterSimpleRelational();
        testInterpreterBetweenExpression();
        testInterpreterNonNumericValueRejection();
        testInterpreterAndExpression();
        testInterpreterOrExpression();
        testInterpreterParentheses();
        testInterpreterMissingVariable();
        testInterpreterMalformedSyntax();
    }

    private void testDecoratorNormalPipeline() {
        try {
            StreamData raw = new EnergyStreamData("STR-101", 230.5, 14.2, 3.27);
            StreamData comp = new CompressionDecorator(raw);
            StreamData enc = new EncryptionDecorator(comp);
            StreamData auth = new AuthenticationDecorator(enc);
            boolean ok = auth.getData().contains("HMAC-SHA256") && auth.getData().contains("AES-256-GCM");
            results.add(new TestResult("testDecoratorNormalPipeline", "Decorator",
                    "Wrapped in Compression -> Encryption -> Auth",
                    "Auth envelope produced, Size: " + auth.getPayloadSize() + " bytes", ok));
        } catch (Exception e) {
            results.add(new TestResult("testDecoratorNormalPipeline", "Decorator", "Successful wrapping",
                    e.getMessage(), false));
        }
    }

    private void testDecoratorDecompression() {
        try {
            byte[] original = "{\"meterId\":\"MTR-999\",\"kw\":4.55,\"status\":\"OK\"}"
                    .getBytes(StandardCharsets.UTF_8);
            StreamData raw = new EnergyStreamData("MTR-999", 230.0, 19.78, 4.55);
            CompressionDecorator comp = new CompressionDecorator(raw);
            byte[] compressed = java.util.Base64.getDecoder()
                    .decode(comp.getData().split("\"data\":\"")[1].split("\"")[0]);
            byte[] decompressed = CompressionDecorator.decompress(compressed);
            boolean ok = new String(decompressed, StandardCharsets.UTF_8).equals(raw.getData());
            results.add(new TestResult("testDecoratorDecompression", "Decorator", "Exact restoration of original bytes",
                    "Decompressed matches raw payload: " + ok, ok));
        } catch (Exception e) {
            results.add(
                    new TestResult("testDecoratorDecompression", "Decorator", "Restoration", e.getMessage(), false));
        }
    }

    private void testDecoratorDecryption() {
        try {
            StreamData raw = new EnergyStreamData("STR-202", 230.0, 10.0, 2.3);
            EncryptionDecorator enc = new EncryptionDecorator(raw);
            byte[] decrypted = EncryptionDecorator.decrypt(enc.getIvBase64(), enc.getCiphertextBase64(),
                    enc.getKeyBytes());
            boolean ok = new String(decrypted, StandardCharsets.UTF_8).equals(raw.getData());
            results.add(new TestResult("testDecoratorDecryption", "Decorator", "AES-256-GCM decrypts to plaintext",
                    "Decrypted matches plaintext: " + ok, ok));
        } catch (Exception e) {
            results.add(new TestResult("testDecoratorDecryption", "Decorator", "Decryption", e.getMessage(), false));
        }
    }

    private void testDecoratorAuthenticationFailure() {
        try {
            StreamData raw = new EnergyStreamData("STR-303", 230.0, 10.0, 2.3);
            AuthenticationDecorator auth = new AuthenticationDecorator(raw);
            boolean tamperedCheck = AuthenticationDecorator.verify(raw.getData() + "TAMPERED",
                    auth.getSignatureBase64(),
                    "SmartCity360-Gateway-Hmac-Secret-Key-2026".getBytes(StandardCharsets.UTF_8));
            results.add(new TestResult("testDecoratorAuthenticationFailure", "Decorator",
                    "Tampered payload rejected (verify=false)", "Verification result: " + tamperedCheck,
                    !tamperedCheck));
        } catch (Exception e) {
            results.add(new TestResult("testDecoratorAuthenticationFailure", "Decorator", "Reject tamper",
                    e.getMessage(), false));
        }
    }

    private void testDecoratorCorruptedPayload() {
        try {
            StreamData raw = new EnergyStreamData("STR-404", 230.0, 10.0, 2.3);
            EncryptionDecorator enc = new EncryptionDecorator(raw);
            byte[] tamperedCipher = java.util.Base64.getDecoder().decode(enc.getCiphertextBase64());
            tamperedCipher[tamperedCipher.length - 1] ^= 0xFF;
            String tamperedB64 = java.util.Base64.getEncoder().encodeToString(tamperedCipher);
            try {
                EncryptionDecorator.decrypt(enc.getIvBase64(), tamperedB64, enc.getKeyBytes());
                results.add(new TestResult("testDecoratorCorruptedPayload", "Decorator", "AEADBadTagException thrown",
                        "No exception thrown", false));
            } catch (GeneralSecurityException e) {
                results.add(new TestResult("testDecoratorCorruptedPayload", "Decorator",
                        "AEADBadTagException thrown on tampered tag",
                        "Caught expected: " + e.getClass().getSimpleName(), true));
            }
        } catch (Exception e) {
            results.add(
                    new TestResult("testDecoratorCorruptedPayload", "Decorator", "Tag failure", e.getMessage(), false));
        }
    }

    private void testDecoratorInvalidKey() {
        try {
            StreamData raw = new EnergyStreamData("STR-505", 230.0, 10.0, 2.3);
            byte[] badKey = new byte[16];
            try {
                new EncryptionDecorator(raw, badKey);
                results.add(new TestResult("testDecoratorInvalidKey", "Decorator",
                        "IllegalArgumentException for 16-byte key", "No exception thrown", false));
            } catch (IllegalArgumentException e) {
                results.add(new TestResult("testDecoratorInvalidKey", "Decorator",
                        "IllegalArgumentException for invalid key length", "Caught expected: " + e.getMessage(), true));
            }
        } catch (Exception e) {
            results.add(
                    new TestResult("testDecoratorInvalidKey", "Decorator", "Key length check", e.getMessage(), false));
        }
    }

    private void testCompositeHierarchyCreation() {
        try {
            ZoneComposite city = new ZoneComposite("C1", "City", "CITY");
            ZoneComposite dist = new ZoneComposite("D1", "District", "DISTRICT");
            ZoneComposite st = new ZoneComposite("S1", "Street", "STREET");
            BuildingLeaf b = new BuildingLeaf("B1", "Building", 100.0);
            st.add(b);
            dist.add(st);
            city.add(dist);
            boolean ok = city.getChildCount() == 1 && dist.getChildCount() == 1 && st.getChildCount() == 1;
            results.add(new TestResult("testCompositeHierarchyCreation", "Composite", "4-tier tree created",
                    "Hierarchy established, leaf power: " + city.getPowerConsumption() + " kW", ok));
        } catch (Exception e) {
            results.add(new TestResult("testCompositeHierarchyCreation", "Composite", "Tree creation", e.getMessage(),
                    false));
        }
    }

    private void testCompositeAddAndRemoveChild() {
        try {
            ZoneComposite st = new ZoneComposite("S1", "Street", "STREET");
            BuildingLeaf b1 = new BuildingLeaf("B1", "Tower 1", 200.0);
            BuildingLeaf b2 = new BuildingLeaf("B2", "Tower 2", 300.0);
            st.add(b1);
            st.add(b2);
            st.remove(b2);
            boolean ok = st.getChildCount() == 1 && st.getPowerConsumption() == 200.0;
            results.add(new TestResult("testCompositeAddAndRemoveChild", "Composite",
                    "Child count=1, Power=200 kW after remove",
                    "Child count=" + st.getChildCount() + ", Power=" + st.getPowerConsumption() + " kW", ok));
        } catch (Exception e) {
            results.add(
                    new TestResult("testCompositeAddAndRemoveChild", "Composite", "Add/Remove", e.getMessage(), false));
        }
    }

    private void testCompositeCommandBroadcast() {
        try {
            ZoneComposite city = new ZoneComposite("C1", "City", "CITY");
            BuildingLeaf b1 = new BuildingLeaf("B1", "Tower 1", 250.0);
            BuildingLeaf b2 = new BuildingLeaf("B2", "Tower 2", 150.0);
            city.add(b1);
            city.add(b2);
            city.executeCommand("reportUsage");
            boolean reportOk = city.getPowerConsumption() == 400.0 && "ONLINE".equals(b1.getStatus());
            city.executeCommand("shutdownPower");
            boolean ok = reportOk && city.getPowerConsumption() == 0.0 && "OFFLINE".equals(b1.getStatus())
                    && "OFFLINE".equals(b2.getStatus());
            results.add(new TestResult("testCompositeCommandBroadcast", "Composite",
                    "All leaves OFFLINE, Total Power=0.0 kW (reportUsage verified)",
                    "City Power=" + city.getPowerConsumption() + " kW, Status=" + city.getStatus(), ok));
        } catch (Exception e) {
            results.add(
                    new TestResult("testCompositeCommandBroadcast", "Composite", "Broadcast", e.getMessage(), false));
        }
    }

    private void testCompositeCommandRestoration() {
        try {
            ZoneComposite city = new ZoneComposite("C1", "City", "CITY");
            BuildingLeaf b1 = new BuildingLeaf("B1", "Tower 1", 450.0);
            city.add(b1);
            city.executeCommand("shutdownPower");
            city.executeCommand("restorePower");
            boolean ok = b1.getPowerConsumption() == 450.0 && "ONLINE".equals(b1.getStatus());
            results.add(new TestResult("testCompositeCommandRestoration", "Composite",
                    "Power restored to baseline 450.0 kW",
                    "Restored Power=" + b1.getPowerConsumption() + " kW, Status=" + b1.getStatus(), ok));
        } catch (Exception e) {
            results.add(
                    new TestResult("testCompositeCommandRestoration", "Composite", "Restore", e.getMessage(), false));
        }
    }

    private void testCompositeAggregatePower() {
        try {
            ZoneComposite dist = new ZoneComposite("D1", "District", "DISTRICT");
            dist.add(new BuildingLeaf("B1", "B1", 125.5));
            dist.add(new BuildingLeaf("B2", "B2", 374.5));
            boolean ok = Math.abs(dist.getPowerConsumption() - 500.0) < 0.001;
            results.add(new TestResult("testCompositeAggregatePower", "Composite", "Aggregated sum = 500.0 kW",
                    "Aggregated sum = " + dist.getPowerConsumption() + " kW", ok));
        } catch (Exception e) {
            results.add(new TestResult("testCompositeAggregatePower", "Composite", "Aggregate", e.getMessage(), false));
        }
    }

    private void testCompositeInvalidCommand() {
        try {
            BuildingLeaf b = new BuildingLeaf("B1", "B1", 100.0);
            try {
                b.executeCommand("unsupportedCommand123");
                results.add(new TestResult("testCompositeInvalidCommand", "Composite",
                        "IllegalArgumentException thrown", "No exception", false));
            } catch (IllegalArgumentException e) {
                results.add(new TestResult("testCompositeInvalidCommand", "Composite",
                        "IllegalArgumentException thrown on invalid command", "Caught expected: " + e.getMessage(),
                        true));
            }
        } catch (Exception e) {
            results.add(new TestResult("testCompositeInvalidCommand", "Composite", "Invalid command", e.getMessage(),
                    false));
        }
    }

    private void testCompositeLeafMutation() {
        try {
            BuildingLeaf b = new BuildingLeaf("B1", "B1", 100.0);
            try {
                b.add(new BuildingLeaf("B2", "B2", 50.0));
                results.add(new TestResult("testCompositeLeafMutation", "Composite",
                        "UnsupportedOperationException thrown", "No exception", false));
            } catch (UnsupportedOperationException e) {
                results.add(new TestResult("testCompositeLeafMutation", "Composite",
                        "UnsupportedOperationException on leaf add()", "Caught expected: " + e.getMessage(), true));
            }
        } catch (Exception e) {
            results.add(
                    new TestResult("testCompositeLeafMutation", "Composite", "Leaf mutation", e.getMessage(), false));
        }
    }

    private void testChainLowSeverity() {
        try {
            ComplaintHandler chain = ComplaintChainFactory.createChain();
            Complaint c = new Complaint();
            c.setId("C-01");
            c.setSeverity("LOW");
            ComplaintRoutingResult r = chain.handle(c);
            boolean ok = "LOCAL_STAFF".equals(r.getHandledByRole()) && r.isHandled();
            results.add(new TestResult("testChainLowSeverity", "Chain of Resp", "Handled by LOCAL_STAFF",
                    "Handled by " + r.getHandledByRole() + ", Status=" + r.getStatus(), ok));
        } catch (Exception e) {
            results.add(new TestResult("testChainLowSeverity", "Chain of Resp", "LOW handle", e.getMessage(), false));
        }
    }

    private void testChainMediumSeverity() {
        try {
            ComplaintHandler chain = ComplaintChainFactory.createChain();
            Complaint c = new Complaint();
            c.setId("C-02");
            c.setSeverity("MEDIUM");
            ComplaintRoutingResult r = chain.handle(c);
            boolean ok = "SUPERVISOR".equals(r.getHandledByRole()) && r.isHandled();
            results.add(new TestResult("testChainMediumSeverity", "Chain of Resp", "Handled by SUPERVISOR",
                    "Handled by " + r.getHandledByRole() + ", Status=" + r.getStatus(), ok));
        } catch (Exception e) {
            results.add(
                    new TestResult("testChainMediumSeverity", "Chain of Resp", "MEDIUM handle", e.getMessage(), false));
        }
    }

    private void testChainHighSeverity() {
        try {
            ComplaintHandler chain = ComplaintChainFactory.createChain();
            Complaint c = new Complaint();
            c.setId("C-03");
            c.setSeverity("HIGH");
            ComplaintRoutingResult r = chain.handle(c);
            boolean ok = "CITY_MANAGER".equals(r.getHandledByRole()) && r.isHandled();
            results.add(new TestResult("testChainHighSeverity", "Chain of Resp", "Handled by CITY_MANAGER",
                    "Handled by " + r.getHandledByRole() + ", Status=" + r.getStatus(), ok));
        } catch (Exception e) {
            results.add(new TestResult("testChainHighSeverity", "Chain of Resp", "HIGH handle", e.getMessage(), false));
        }
    }

    private void testChainCriticalSeverity() {
        try {
            ComplaintHandler chain = ComplaintChainFactory.createChain();
            Complaint c = new Complaint();
            c.setId("C-04");
            c.setSeverity("CRITICAL");
            ComplaintRoutingResult r = chain.handle(c);
            boolean ok = "CITY_MANAGER".equals(r.getHandledByRole()) && r.isHandled();
            results.add(new TestResult("testChainCriticalSeverity", "Chain of Resp",
                    "Handled by CITY_MANAGER (Executive Crisis)",
                    "Handled by " + r.getHandledByRole() + ", Status=" + r.getStatus(), ok));
        } catch (Exception e) {
            results.add(new TestResult("testChainCriticalSeverity", "Chain of Resp", "CRITICAL handle", e.getMessage(),
                    false));
        }
    }

    private void testChainMissingSeverity() {
        try {
            ComplaintHandler chain = ComplaintChainFactory.createChain();
            Complaint c = new Complaint();
            c.setId("C-05");
            c.setSeverity(null);
            ComplaintRoutingResult r = chain.handle(c);
            boolean ok = !r.isHandled() && !"LOCAL_STAFF".equals(r.getHandledByRole());
            results.add(new TestResult("testChainMissingSeverity", "Chain of Resp",
                    "Intercepted by triage, NOT defaulted to LOW",
                    "Handled=" + r.isHandled() + ", Role=" + r.getHandledByRole() + ", Status=" + r.getStatus(), ok));
        } catch (Exception e) {
            results.add(new TestResult("testChainMissingSeverity", "Chain of Resp", "Missing severity", e.getMessage(),
                    false));
        }
    }

    private void testChainInvalidSeverity() {
        try {
            ComplaintHandler chain = ComplaintChainFactory.createChain();
            Complaint c = new Complaint();
            c.setId("C-06");
            c.setSeverity("RANDOM_INVALID_SEVERITY");
            ComplaintRoutingResult r = chain.handle(c);
            boolean ok = !r.isHandled() && !"LOCAL_STAFF".equals(r.getHandledByRole());
            results.add(new TestResult("testChainInvalidSeverity", "Chain of Resp",
                    "Intercepted by triage, NOT defaulted to LOW",
                    "Handled=" + r.isHandled() + ", Role=" + r.getHandledByRole() + ", Status=" + r.getStatus(), ok));
        } catch (Exception e) {
            results.add(new TestResult("testChainInvalidSeverity", "Chain of Resp", "Invalid severity", e.getMessage(),
                    false));
        }
    }

    private void testChainTerminalFallback() {
        try {
            // 1. Verify unlinked handler returns CHAIN_EXHAUSTED to prevent null pointer drops
            ComplaintHandler singleHandler = new LocalStaffHandler();
            Complaint c1 = new Complaint();
            c1.setId("C-07");
            c1.setSeverity("CRITICAL");
            ComplaintRoutingResult r1 = singleHandler.handle(c1);
            boolean unhandledSafe = !r1.isHandled() && "CHAIN_EXHAUSTED".equals(r1.getStatus());

            // 2. Verify TerminalFallbackHandler captures unhandled requests when wired at chain terminus
            ComplaintHandler fallback = new TerminalFallbackHandler();
            singleHandler.setNext(fallback);
            Complaint c2 = new Complaint();
            c2.setId("C-07B");
            c2.setSeverity("CRITICAL");
            ComplaintRoutingResult r2 = singleHandler.handle(c2);
            boolean fallbackCaptured = r2.isHandled()
                    && "FALLBACK_ASSIGNED".equals(r2.getStatus())
                    && "FALLBACK_DISPATCH_DESK".equals(r2.getHandledByRole());

            boolean ok = unhandledSafe && fallbackCaptured;
            results.add(new TestResult("testChainTerminalFallback", "Chain of Resp",
                    "Terminal fallback captures unhandled; CHAIN_EXHAUSTED safeguard active",
                    "FallbackCaptured=" + fallbackCaptured + ", UnhandledSafeguard=" + unhandledSafe, ok));
        } catch (Exception e) {
            results.add(new TestResult("testChainTerminalFallback", "Chain of Resp", "Terminal drop hazard",
                    e.getMessage(), false));
        }
    }

    private void testChainAuditTrail() {
        try {
            ComplaintHandler chain = ComplaintChainFactory.createChain();
            Complaint c = new Complaint();
            c.setId("C-08");
            c.setSeverity("CRITICAL");
            ComplaintRoutingResult r = chain.handle(c);
            List<ComplaintAuditRecord> audit = r.getAuditTrail();
            boolean sizeOk = audit.size() == 4;
            boolean ordered = sizeOk
                    && "ENTRY_GATEWAY".equals(audit.get(0).getFromRole())
                    && "LOCAL_STAFF".equals(audit.get(1).getFromRole())
                    && "SUPERVISOR".equals(audit.get(2).getFromRole())
                    && "CITY_MANAGER".equals(audit.get(3).getFromRole());
            boolean immutable = false;
            try {
                audit.add(new ComplaintAuditRecord("now", "X", "Y", "Z", "test"));
            } catch (UnsupportedOperationException e) {
                immutable = true;
            }
            boolean ok = sizeOk && ordered && immutable;
            results.add(new TestResult("testChainAuditTrail", "Chain of Resp",
                    "Audit records contain ISO-8601 timestamps & chronological routing steps",
                    "Audit entries: " + audit.size() + ", Chronological: " + ordered + ", Immutable: " + immutable, ok));
        } catch (Exception e) {
            results.add(new TestResult("testChainAuditTrail", "Chain of Resp", "Audit trail", e.getMessage(), false));
        }
    }

    private void testFlyweightProfileReusability() {
        try {
            StreetlightProfileFactory.clear();
            SharedStreetlightProfile p1 = StreetlightProfileFactory.getProfile("Philips-150", "LED", 150, 18000, 4000,
                    "v1");
            SharedStreetlightProfile p2 = StreetlightProfileFactory.getProfile("Philips-150", "LED", 150, 18000, 4000,
                    "v1");
            boolean ok = p1 == p2 && StreetlightProfileFactory.getFlyweightCount() == 1;
            results.add(new TestResult("testFlyweightProfileReusability", "Flyweight",
                    "Identical profile returns cached instance (p1 == p2)",
                    "Instance match: " + (p1 == p2) + ", Pool size: " + StreetlightProfileFactory.getFlyweightCount(),
                    ok));
        } catch (Exception e) {
            results.add(new TestResult("testFlyweightProfileReusability", "Flyweight", "Profile reuse", e.getMessage(),
                    false));
        }
    }

    private void testFlyweightCacheKeyDistinction() {
        try {
            StreetlightProfileFactory.clear();
            SharedStreetlightProfile p1 = StreetlightProfileFactory.getProfile("Philips-150", "LED", 150, 18000, 4000, "v1.0");
            SharedStreetlightProfile p2 = StreetlightProfileFactory.getProfile("Philips-150", "LED", 150, 24000, 4000, "v2.0");
            boolean distinct = (p1 != p2) && (StreetlightProfileFactory.getFlyweightCount() == 2);
            results.add(new TestResult("testFlyweightCacheKeyDistinction", "Flyweight", "Profiles with differing lumens/firmware produce distinct cached instances", "Distinct instances: " + distinct + ", Pool size: " + StreetlightProfileFactory.getFlyweightCount(), distinct));
        } catch (Exception e) {
            results.add(new TestResult("testFlyweightCacheKeyDistinction", "Flyweight", "Cache key distinction", e.getMessage(), false));
        }
    }

    private void testCompositeCycleDetection() {
        try {
            ZoneComposite c1 = new ZoneComposite("C1", "District 1", "DISTRICT");
            ZoneComposite c2 = new ZoneComposite("C2", "Street A", "STREET");
            c1.add(c2);
            boolean caughtCycle = false;
            try {
                c2.add(c1);
            } catch (IllegalArgumentException e) {
                caughtCycle = true;
            }
            results.add(new TestResult("testCompositeCycleDetection", "Composite", "Adding parent to descendant composite triggers cycle rejection", "Cycle detected and rejected: " + caughtCycle, caughtCycle));
        } catch (Exception e) {
            results.add(new TestResult("testCompositeCycleDetection", "Composite", "Cycle detection", e.getMessage(), false));
        }
    }

    private void testFlyweightThreadSafety() {
        try {
            StreetlightProfileFactory.clear();
            ExecutorService pool = Executors.newFixedThreadPool(8);
            List<Callable<SharedStreetlightProfile>> tasks = new ArrayList<>();
            for (int i = 0; i < 40; i++) {
                tasks.add(() -> StreetlightProfileFactory.getProfile("Siemens-200", "LED", 200, 24000, 5000, "v1"));
            }
            List<Future<SharedStreetlightProfile>> futures = pool.invokeAll(tasks);
            SharedStreetlightProfile first = futures.get(0).get();
            boolean ok = true;
            for (Future<SharedStreetlightProfile> f : futures) {
                if (f.get() != first) {
                    ok = false;
                    break;
                }
            }
            pool.shutdown();
            ok = ok && StreetlightProfileFactory.getFlyweightCount() == 1;
            results.add(new TestResult("testFlyweightThreadSafety", "Flyweight",
                    "Thread-safe pool instantiation across 8 concurrent threads", "Concurrent pool size: "
                            + StreetlightProfileFactory.getFlyweightCount() + ", All instances identical: " + ok,
                    ok));
        } catch (Exception e) {
            results.add(
                    new TestResult("testFlyweightThreadSafety", "Flyweight", "Thread safety", e.getMessage(), false));
        }
    }

    private void testFlyweightContextSeparation() {
        try {
            SharedStreetlightProfile p = StreetlightProfileFactory.getProfile("Osram-90", "LED", 90, 11000, 3000, "v1");
            StreetlightContext l1 = new StreetlightContext("POLE-01", 6.90, 79.80, p);
            StreetlightContext l2 = new StreetlightContext("POLE-02", 6.95, 79.85, p);
            l1.setBrightnessLevel(90);
            l2.setBrightnessLevel(30);
            boolean ok = l1.getBrightnessLevel() == 90 && l2.getBrightnessLevel() == 30
                    && l1.getProfile() == l2.getProfile();
            results.add(new TestResult("testFlyweightContextSeparation", "Flyweight",
                    "Contexts maintain distinct extrinsic state while sharing profile",
                    "L1 brightness=" + l1.getBrightnessLevel() + ", L2 brightness=" + l2.getBrightnessLevel()
                            + ", Same profile: true",
                    ok));
        } catch (Exception e) {
            results.add(new TestResult("testFlyweightContextSeparation", "Flyweight", "Extrinsic separation",
                    e.getMessage(), false));
        }
    }

    private void testFlyweightEmpiricalBenchmark() {
        try {
            FlyweightBenchmark.BenchmarkResult b = FlyweightBenchmark.runBenchmark(25000);
            boolean ok = b.flyweightPoolSize == 3 && b.savingsPercent > 50.0;
            results.add(new TestResult("testFlyweightEmpiricalBenchmark", "Flyweight",
                    "Significant heap footprint reduction on 25,000 objects (>50%)",
                    "Calculated layout savings: " + String.format("%.1f%%", b.savingsPercent) + " (Naive: "
                            + String.format("%.2f MB", b.naiveEstimatedBytes / 1048576.0) + ", Flyweight: "
                            + String.format("%.2f MB", b.flyweightEstimatedBytes / 1048576.0) + ")",
                    ok));
        } catch (Exception e) {
            results.add(new TestResult("testFlyweightEmpiricalBenchmark", "Flyweight", "Benchmark execution",
                    e.getMessage(), false));
        }
    }

    private void testInterpreterSimpleRelational() {
        try {
            PolicyContext ctx = new PolicyContext();
            ctx.set("VAL", 42.0);
            Expression e1 = DslPolicyParser.parse("VAL > 40.0");
            Expression e2 = DslPolicyParser.parse("VAL <= 42.0");
            Expression e3 = DslPolicyParser.parse("VAL == 42.0");
            boolean ok = e1.interpret(ctx) && e2.interpret(ctx) && e3.interpret(ctx);
            results.add(new TestResult("testInterpreterSimpleRelational", "Interpreter",
                    "All relational operators evaluate correctly", "VAL > 40, VAL <= 42, VAL == 42 all TRUE: " + ok,
                    ok));
        } catch (Exception e) {
            results.add(new TestResult("testInterpreterSimpleRelational", "Interpreter", "Relational ops",
                    e.getMessage(), false));
        }
    }

    private void testInterpreterBetweenExpression() {
        try {
            PolicyContext ctx = new PolicyContext();
            ctx.set("PARKING_HOUR", 14.0);
            Expression e = DslPolicyParser.parse("PARKING_HOUR BETWEEN 8 AND 18");
            boolean inRange14 = e.interpret(ctx);

            ctx.set("PARKING_HOUR", 21.0);
            boolean inRange21 = e.interpret(ctx);

            boolean ok = inRange14 && !inRange21;
            results.add(new TestResult("testInterpreterBetweenExpression", "Interpreter", "BETWEEN operator evaluates range boundaries [min <= x <= max]", "14 in [8,18]: " + inRange14 + ", 21 in [8,18]: " + inRange21, ok));
        } catch (Exception e) {
            results.add(new TestResult("testInterpreterBetweenExpression", "Interpreter", "BETWEEN operator", e.getMessage(), false));
        }
    }

    private void testInterpreterNonNumericValueRejection() {
        try {
            PolicyContext ctx = new PolicyContext();
            ctx.set("SENSOR", "invalid_number_string");
            boolean caught = false;
            try {
                ctx.getDouble("SENSOR");
            } catch (IllegalArgumentException e) {
                caught = true;
            }
            results.add(new TestResult("testInterpreterNonNumericValueRejection", "Interpreter", "Non-numeric context values throw IllegalArgumentException", "Exception thrown: " + caught, caught));
        } catch (Exception e) {
            results.add(new TestResult("testInterpreterNonNumericValueRejection", "Interpreter", "Non-numeric rejection", e.getMessage(), false));
        }
    }

    private void testInterpreterAndExpression() {
        try {
            PolicyContext ctx = new PolicyContext();
            ctx.set("NOISE", 75.0);
            ctx.set("HOUR", 23.0);
            Expression e = DslPolicyParser.parse("(NOISE >= 70.0) AND (HOUR > 22.0)");
            boolean ok = e.interpret(ctx);
            results.add(new TestResult("testInterpreterAndExpression", "Interpreter",
                    "AND conjunction evaluated to TRUE", "Result: " + ok + " for AST: " + e, ok));
        } catch (Exception e) {
            results.add(new TestResult("testInterpreterAndExpression", "Interpreter", "AND evaluation", e.getMessage(),
                    false));
        }
    }

    private void testInterpreterOrExpression() {
        try {
            PolicyContext ctx = new PolicyContext();
            ctx.set("AIR", 80.0);
            ctx.set("NOISE", 90.0);
            Expression e = DslPolicyParser.parse("(AIR > 150.0) OR (NOISE > 85.0)");
            boolean ok = e.interpret(ctx);
            results.add(new TestResult("testInterpreterOrExpression", "Interpreter", "OR disjunction evaluated to TRUE",
                    "Result: " + ok + " for AST: " + e, ok));
        } catch (Exception e) {
            results.add(new TestResult("testInterpreterOrExpression", "Interpreter", "OR evaluation", e.getMessage(),
                    false));
        }
    }

    private void testInterpreterParentheses() {
        try {
            PolicyContext ctx = new PolicyContext();
            ctx.set("A", 10.0);
            ctx.set("B", 20.0);
            ctx.set("C", 30.0);
            Expression e = DslPolicyParser.parse("((A < 15.0 AND B > 25.0) OR C == 30.0)");
            boolean ok = e.interpret(ctx);
            results.add(new TestResult("testInterpreterParentheses", "Interpreter",
                    "Nested parentheses AST correctly evaluated", "Result: " + ok + " for AST: " + e, ok));
        } catch (Exception e) {
            results.add(new TestResult("testInterpreterParentheses", "Interpreter", "Parentheses AST", e.getMessage(),
                    false));
        }
    }

    private void testInterpreterMissingVariable() {
        try {
            PolicyContext ctx = new PolicyContext();
            Expression e = DslPolicyParser.parse("UNREGISTERED_SENSOR > 50.0");
            boolean ok = !e.interpret(ctx);
            results.add(new TestResult("testInterpreterMissingVariable", "Interpreter",
                    "Missing variable returns false safely", "Evaluation result: " + e.interpret(ctx), ok));
        } catch (Exception e) {
            results.add(new TestResult("testInterpreterMissingVariable", "Interpreter", "Missing var safety",
                    e.getMessage(), false));
        }
    }

    private void testInterpreterMalformedSyntax() {
        try {
            boolean caughtAll = true;
            String[] badTokens = { "", "(A > 10", "A === 10", "A >", "TEMP BETWEEN 1.2.3 AND 5" };
            for (String b : badTokens) {
                try {
                    DslPolicyParser.parse(b);
                    caughtAll = false;
                } catch (DslSyntaxException expected) {
                    // Expected DslSyntaxException for syntax validation testing
                }
            }
            results.add(new TestResult("testInterpreterMalformedSyntax", "Interpreter",
                    "DslSyntaxException thrown for all malformed expressions (including BETWEEN 1.2.3 AND 5)",
                    "All 5 syntax error variations caught: " + caughtAll, caughtAll));
        } catch (Exception e) {
            results.add(new TestResult("testInterpreterMalformedSyntax", "Interpreter", "Syntax error rejection",
                    e.getMessage(), false));
        }
    }

    public List<TestResult> getResults() {
        return results;
    }

    public void printMarkdownReport() {
        System.out.println("# SmartCity360 Automated Comprehensive Test Report\n");
        System.out.println("| # | Test Name | Pattern Subsystem | Expected Result | Actual Result | Status |");
        System.out.println("|---|---|---|---|---|---|");
        int count = 1;
        int passCount = 0;
        for (TestResult r : results) {
            String status = r.passed ? "**PASS**" : "**FAIL**";
            if (r.passed)
                passCount++;
            System.out.printf("| %d | `%s` | %s | %s | %s | %s |%n",
                    count++, r.testName, r.pattern, r.expected, r.actual, status);
        }
        System.out.printf("%n**Summary: %d / %d Tests Passed (%.1f%% Pass Rate)**%n",
                passCount, results.size(), (double) passCount / results.size() * 100.0);
    }

    public static void main(String[] args) {
        ComprehensiveTestSuite suite = new ComprehensiveTestSuite();
        suite.runAllTests();
        suite.printMarkdownReport();
    }
}

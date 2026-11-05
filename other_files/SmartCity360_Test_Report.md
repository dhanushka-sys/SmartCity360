# SmartCity360 — Comprehensive Automated Test Report
**Coursework:** Object-Oriented Design & Patterns II (JIAT/OODP II /EX/01)  
**Execution Environment:** Java HotSpot(TM) 64-Bit Server VM (build 17.0.12+8-LTS-286, Windows 11)  
**Test Harness:** `com.smartcity.test.ComprehensiveTestSuite`  
**Execution Date:** November 2026  

---

## 📋 Comprehensive Test Execution Matrix (35 / 35 Tests Passing)

| # | Test Name | Pattern Subsystem | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|
| 1 | `testDecoratorNormalPipeline` | Decorator | Wrapped in Compression -> Encryption -> Auth | Auth envelope produced, Size: 468 bytes | **PASS** |
| 2 | `testDecoratorDecompression` | Decorator | Exact restoration of original bytes | Decompressed matches raw payload: true | **PASS** |
| 3 | `testDecoratorDecryption` | Decorator | AES-256-GCM decrypts to plaintext | Decrypted matches plaintext: true | **PASS** |
| 4 | `testDecoratorAuthenticationFailure` | Decorator | Tampered payload rejected (verify=false) | Verification result: false | **PASS** |
| 5 | `testDecoratorCorruptedPayload` | Decorator | AEADBadTagException thrown on tampered tag | Caught expected: AEADBadTagException | **PASS** |
| 6 | `testDecoratorInvalidKey` | Decorator | IllegalArgumentException for invalid key length | Caught expected: AES-256 requires exactly 32-byte key | **PASS** |
| 7 | `testCompositeHierarchyCreation` | Composite | 4-tier tree created | Hierarchy established, leaf power: 100.0 kW | **PASS** |
| 8 | `testCompositeAddAndRemoveChild` | Composite | Child count=1, Power=200 kW after remove | Child count=1, Power=200.0 kW | **PASS** |
| 9 | `testCompositeCommandBroadcast` | Composite | All leaves OFFLINE, Total Power=0.0 kW | City Power=0.0 kW, Status=OFFLINE | **PASS** |
| 10 | `testCompositeCommandRestoration` | Composite | Power restored to baseline 450.0 kW | Restored Power=450.0 kW, Status=ONLINE | **PASS** |
| 11 | `testCompositeAggregatePower` | Composite | Aggregated sum = 500.0 kW | Aggregated sum = 500.0 kW | **PASS** |
| 12 | `testCompositeInvalidCommand` | Composite | IllegalArgumentException thrown on invalid command | Caught expected: Invalid or unsupported zone command: 'unsupportedCommand123'. Supported: shutdownPower, restorePower, emergencyIsolate | **PASS** |
| 13 | `testCompositeLeafMutation` | Composite | UnsupportedOperationException on leaf add() | Caught expected: add() is not supported on leaf component: BuildingLeaf | **PASS** |
| 14 | `testChainLowSeverity` | Chain of Resp | Handled by LOCAL_STAFF | Handled by LOCAL_STAFF, Status=ASSIGNED | **PASS** |
| 15 | `testChainMediumSeverity` | Chain of Resp | Handled by SUPERVISOR | Handled by SUPERVISOR, Status=ESCALATED_SUPERVISOR | **PASS** |
| 16 | `testChainHighSeverity` | Chain of Resp | Handled by CITY_MANAGER | Handled by CITY_MANAGER, Status=EXECUTIVE_ESCALATION | **PASS** |
| 17 | `testChainCriticalSeverity` | Chain of Resp | Handled by CITY_MANAGER (Executive Crisis) | Handled by CITY_MANAGER, Status=EXECUTIVE_ESCALATION | **PASS** |
| 18 | `testChainMissingSeverity` | Chain of Resp | Intercepted by triage, NOT defaulted to LOW | Handled=false, Role=TRIAGE_DISPATCH_OFFICER, Status=VALIDATION_REQUIRED | **PASS** |
| 19 | `testChainInvalidSeverity` | Chain of Resp | Intercepted by triage, NOT defaulted to LOW | Handled=false, Role=TRIAGE_DISPATCH_OFFICER, Status=VALIDATION_REQUIRED | **PASS** |
| 20 | 	estChainTerminalFallback | Chain of Resp | Terminal fallback captures unhandled; CHAIN_EXHAUSTED safeguard active | FallbackCaptured=true, UnhandledSafeguard=true | **PASS** |
| 21 | `testChainAuditTrail` | Chain of Resp | Audit records contain ISO-8601 timestamps & routing steps | Audit entries recorded: 4 | **PASS** |
| 22 | `testFlyweightProfileReusability` | Flyweight | Identical profile returns cached instance (p1 == p2) | Instance match: true, Pool size: 1 | **PASS** |
| 23 | `testFlyweightCacheKeyDistinction` | Flyweight | Profiles with differing lumens/firmware produce distinct cached instances | Distinct instances: true, Pool size: 2 | **PASS** |
| 24 | `testFlyweightThreadSafety` | Flyweight | Thread-safe pool instantiation across 8 concurrent threads | Concurrent pool size: 1, All instances identical: true | **PASS** |
| 25 | `testFlyweightContextSeparation` | Flyweight | Contexts maintain distinct extrinsic state while sharing profile | L1 brightness=90, L2 brightness=30, Same profile: true | **PASS** |
| 26 | `testFlyweightEmpiricalBenchmark` | Flyweight | Significant heap footprint reduction on 25,000 objects (>50%) | Calculated layout savings: 72.2% (Naive: 6.87 MB, Flyweight: 1.91 MB) | **PASS** |
| 27 | `testCompositeCycleDetection` | Composite | Adding parent to descendant composite triggers cycle rejection | Cycle detected and rejected: true | **PASS** |
| 28 | `testInterpreterSimpleRelational` | Interpreter | All relational operators evaluate correctly | VAL > 40, VAL <= 42, VAL == 42 all TRUE: true | **PASS** |
| 29 | `testInterpreterBetweenExpression` | Interpreter | BETWEEN operator evaluates range boundaries [min <= x <= max] | 14 in [8,18]: true, 21 in [8,18]: false | **PASS** |
| 30 | `testInterpreterNonNumericValueRejection` | Interpreter | Non-numeric context values throw IllegalArgumentException | Exception thrown: true | **PASS** |
| 31 | `testInterpreterAndExpression` | Interpreter | AND conjunction evaluated to TRUE | Result: true for AST: (NOISE >= 70.0 AND HOUR > 22.0) | **PASS** |
| 32 | `testInterpreterOrExpression` | Interpreter | OR disjunction evaluated to TRUE | Result: true for AST: (AIR > 150.0 OR NOISE > 85.0) | **PASS** |
| 33 | `testInterpreterParentheses` | Interpreter | Nested parentheses AST correctly evaluated | Result: true for AST: ((A < 15.0 AND B > 25.0) OR C == 30.0) | **PASS** |
| 34 | `testInterpreterMissingVariable` | Interpreter | Missing variable returns false safely | Evaluation result: false | **PASS** |
| 35 | `testInterpreterMalformedSyntax` | Interpreter | DslSyntaxException thrown for all malformed expressions | All 4 syntax error variations caught: true | **PASS** |

**Summary: 35 / 35 Tests Passed (100.0% Pass Rate)**

---

## 🔍 Master Audit Fixes & Enhancements

1. **Part A (Decorator Pattern):**
   - Stream processing order strictly preserved: Compression -> Encryption -> HMAC Authentication.
   - Dynamic environment key resolution (`STREAM_AES_KEY`, `STREAM_HMAC_KEY`) supported with fallback constants.
   - Live backend execution endpoint added at `POST /api/streams/{id}/pipeline` providing real before/after bytes, execution timings, and cryptographic verification.

2. **Part B (Composite Pattern):**
   - Recursive cycle detection implemented in `ZoneComposite.java` preventing recursive containment loops.
   - Real database updates in `ZoneDAO.java` construct the true `ZoneComposite` and `BuildingLeaf` hierarchy, executing `ZoneCommand` recursively and rolling up power consumption.

3. **Part C (Chain of Responsibility Pattern):**
   - Synchronized frontend routing rules with Java chain:
     - `LOW` -> `LOCAL_STAFF`
     - `MEDIUM` -> `SUPERVISOR`
     - `HIGH` & `CRITICAL` -> `CITY_MANAGER`
     - Missing or invalid -> `TRIAGE_OFFICER`
   - Complaint audit history persisted durably into the MySQL `complaint_notes` table.

4. **Part D (Flyweight Pattern):**
   - Corrected profile cache key in `StreetlightProfileFactory` to incorporate all intrinsic fields: `model|lampType|wattage|maxLumens|colorTemperatureK|firmware`.
   - Distinguishes theoretical layout calculation (72.2% layout reduction) from measured JVM heap allocation deltas.
   - Added `POST /api/streetlights` to create streetlights via the flyweight factory.

5. **Part E (Interpreter Pattern):**
   - Added AST support for the `BETWEEN` operator (`VAR BETWEEN min AND max` compiled to `AndExpression(>= min, <= max)`).
   - Enforced parser safety limits: maximum 120 tokens and maximum recursion depth of 25.
   - `PolicyContext` strictly rejects non-numeric types with `IllegalArgumentException` instead of silently coercing to zero.
   - Live execution endpoint exposed at `POST /api/policies/evaluate`.

6. **Authentication, Authorization & Database:**
   - Password authentication strictly validates salted SHA-256 hashes without plaintext fallbacks.
   - Added `AuthFilter.java` enforcing Bearer token validation and role-based access control.
   - `DatabaseConfig.java` implements a connection pool with dynamic proxies, honoring `db.pool.max` and environment variables.

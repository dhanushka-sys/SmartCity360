# SmartCity360 — Comprehensive Automated Test Report
**Coursework:** Object-Oriented Design & Patterns II (JIAT/OODP II /EX/01)  
**Execution Environment:** OpenJDK 17 64-Bit Server VM (build 17.0.12+8-LTS-286, Windows 11 amd64)  
**Test Harness:** `com.smartcity.test.ComprehensiveTestSuite`  
**Execution Status:** 35 / 35 Tests Passing (100.0% Success Rate)  

---

# SmartCity360 Automated Comprehensive Test Report

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
| 9 | `testCompositeCommandBroadcast` | Composite | All leaves OFFLINE, Total Power=0.0 kW (reportUsage verified) | City Power=0.0 kW, Status=OFFLINE | **PASS** |
| 10 | `testCompositeCommandRestoration` | Composite | Power restored to baseline 450.0 kW | Restored Power=450.0 kW, Status=ONLINE | **PASS** |
| 11 | `testCompositeAggregatePower` | Composite | Aggregated sum = 500.0 kW | Aggregated sum = 500.0 kW | **PASS** |
| 12 | `testCompositeInvalidCommand` | Composite | IllegalArgumentException thrown on invalid command | Caught expected: Invalid or unsupported zone command: 'unsupportedCommand123'. Supported: shutdownPower, restorePower, emergencyIsolate, reportUsage | **PASS** |
| 13 | `testCompositeLeafMutation` | Composite | UnsupportedOperationException on leaf add() | Caught expected: add() is not supported on leaf component: BuildingLeaf | **PASS** |
| 14 | `testChainLowSeverity` | Chain of Resp | Handled by LOCAL_STAFF | Handled by LOCAL_STAFF, Status=ASSIGNED | **PASS** |
| 15 | `testChainMediumSeverity` | Chain of Resp | Handled by SUPERVISOR | Handled by SUPERVISOR, Status=ESCALATED_SUPERVISOR | **PASS** |
| 16 | `testChainHighSeverity` | Chain of Resp | Handled by CITY_MANAGER | Handled by CITY_MANAGER, Status=EXECUTIVE_ESCALATION | **PASS** |
| 17 | `testChainCriticalSeverity` | Chain of Resp | Handled by CITY_MANAGER (Executive Crisis) | Handled by CITY_MANAGER, Status=EXECUTIVE_ESCALATION | **PASS** |
| 18 | `testChainMissingSeverity` | Chain of Resp | Intercepted by triage, NOT defaulted to LOW | Handled=false, Role=TRIAGE_DISPATCH_OFFICER, Status=VALIDATION_REQUIRED | **PASS** |
| 19 | `testChainInvalidSeverity` | Chain of Resp | Intercepted by triage, NOT defaulted to LOW | Handled=false, Role=TRIAGE_DISPATCH_OFFICER, Status=VALIDATION_REQUIRED | **PASS** |
| 20 | `testChainTerminalFallback` | Chain of Resp | Terminal fallback captures unhandled; CHAIN_EXHAUSTED safeguard active | FallbackCaptured=true, UnhandledSafeguard=true | **PASS** |
| 21 | `testChainAuditTrail` | Chain of Resp | Audit records contain ISO-8601 timestamps & chronological routing steps | Audit entries: 4, Chronological: true, Immutable: true | **PASS** |
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
| 35 | `testInterpreterMalformedSyntax` | Interpreter | DslSyntaxException thrown for all malformed expressions (including BETWEEN 1.2.3 AND 5) | All 5 syntax error variations caught: true | **PASS** |

**Summary: 35 / 35 Tests Passed (100.0% Pass Rate)**

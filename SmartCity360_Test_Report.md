# SmartCity360 — Comprehensive Automated Test Report
**Coursework:** Object-Oriented Design & Patterns II (JIAT/OODP II /EX/01)  
**Execution Environment:** Java HotSpot(TM) 64-Bit Server VM (build 17.0.12+8-LTS-286, Windows 11)  
**Test Harness:** com.smartcity.test.ComprehensiveTestSuite  
**Execution Date:** November 2026  

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
| 20 | `testChainTerminalFallback` | Chain of Resp | CHAIN_EXHAUSTED returned when next handler missing | Status=CHAIN_EXHAUSTED, Message=No subsequent handler available in processing chain | **PASS** |
| 21 | `testChainAuditTrail` | Chain of Resp | Audit records contain ISO-8601 timestamps & routing steps | Audit entries recorded: 4 | **PASS** |
| 22 | `testFlyweightProfileReusability` | Flyweight | Identical profile returns cached instance (p1 == p2) | Instance match: true, Pool size: 1 | **PASS** |
| 23 | `testFlyweightThreadSafety` | Flyweight | Thread-safe pool instantiation across 8 concurrent threads | Concurrent pool size: 1, All instances identical: true | **PASS** |
| 24 | `testFlyweightContextSeparation` | Flyweight | Contexts maintain distinct extrinsic state while sharing profile | L1 brightness=90, L2 brightness=30, Same profile: true | **PASS** |
| 25 | `testFlyweightEmpiricalBenchmark` | Flyweight | Significant heap footprint reduction on 25,000 objects (>50%) | Calculated layout savings: 72.2% (Naive: 6.87 MB, Flyweight: 1.91 MB) | **PASS** |
| 26 | `testInterpreterSimpleRelational` | Interpreter | All relational operators evaluate correctly | VAL > 40, VAL <= 42, VAL == 42 all TRUE: true | **PASS** |
| 27 | `testInterpreterAndExpression` | Interpreter | AND conjunction evaluated to TRUE | Result: true for AST: (NOISE >= 70.0 AND HOUR > 22.0) | **PASS** |
| 28 | `testInterpreterOrExpression` | Interpreter | OR disjunction evaluated to TRUE | Result: true for AST: (AIR > 150.0 OR NOISE > 85.0) | **PASS** |
| 29 | `testInterpreterParentheses` | Interpreter | Nested parentheses AST correctly evaluated | Result: true for AST: ((A < 15.0 AND B > 25.0) OR C == 30.0) | **PASS** |
| 30 | `testInterpreterMissingVariable` | Interpreter | Missing variable returns false safely | Evaluation result: false | **PASS** |
| 31 | `testInterpreterMalformedSyntax` | Interpreter | DslSyntaxException thrown for all malformed expressions | All 4 syntax error variations caught: true | **PASS** |

**Summary: 31 / 31 Tests Passed (100.0% Pass Rate)**

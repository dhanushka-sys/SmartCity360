# SmartCity360 — Comprehensive VIVA Oral Defense & Video Demonstration Guide

**Module:** Object-Oriented Design Patterns II (`JIAT/OODP II /EX/01`)  
**Assessment Weighting:** 25 Marks (Part F: 15 Marks VIVA Oral Defense + 10 Marks Video Demonstration)  
**Target Municipality:** Metropolis Neo-Prime Smart City Management Platform  
**Target Student Audience:** Final Assessment Candidate Presentation & Defense Preparation  
**Deliverable Filenames:** `SmartCity360_Viva_and_Presentation_Guide.md` & `SmartCity360_Viva_and_Presentation_Guide.pdf`  

---

## 📋 Table of Contents
1. **Executive Presentation Strategy & Scoring Rubric**
2. **Complete VIVA Oral Defense Questions & Model Technical Answers**
   - *Q1: Decorator Pattern vs Subclass Explosion*
   - *Q2: Cryptographic & Compression Pipeline Ordering*
   - *Q3: Composite Pattern: Transparency vs Safety Trade-offs*
   - *Q4: Type-Safe Zone Commands & Baseline Power Restoration*
   - *Q5: Chain of Responsibility: Elimination of Default-to-LOW Risk*
   - *Q6: Flyweight Pattern: Intrinsic/Extrinsic State & Empirical JVM Benchmarks*
   - *Q7: Interpreter Pattern: Sandboxed AST vs Script Injection Risks*
   - *Q8: Elimination of 8 Foundational Software Anti-Patterns*
   - *Q9: Strict SOLID Principles Architectural Defense*
   - *Q10: Automated Regression Suite & Runtime Reliability*
3. **Word-for-Word 10–15 Minute Demonstration Video Walkthrough Script**
   - *Scene 1: Introduction & 4-Tier Architecture (00:00 – 01:45)*
   - *Scene 2: Part A — Decorator Pattern Live Ingestion (01:45 – 04:15)*
   - *Scene 3: Part B — Composite Pattern Zone Hierarchy (04:15 – 06:45)*
   - *Scene 4: Part C — Chain of Responsibility Complaint Triage (06:45 – 09:15)*
   - *Scene 5: Part D — Flyweight 25,000 Streetlight Fleet & Live Memory Benchmark (09:15 – 11:15)*
   - *Scene 6: Part E — Interpreter Pattern DSL Policy Engine (11:15 – 13:00)*
   - *Scene 7: Automated Test Suite Live Execution & Conclusion (13:00 – 14:15)*
4. **Pre-Recording Technical Checklist & Contingency Recovery Protocol**

---

## 1. Executive Presentation Strategy & Scoring Rubric

The Part F component of the OODP II assessment awards **25 Marks**, distributed as follows:
- **VIVA Oral Defense (15 Marks):** Evaluates your ability to articulate design pattern choices, discuss architectural trade-offs, explain code mechanisms, and defend your system against edge cases and anti-patterns.
- **Demonstration Video (10 Marks):** Evaluates a smooth, professional 10–15 minute recorded walkthrough showcasing live working features, responsive UI panels, and pattern implementations.

### 🎯 Key Presentation Rules to Secure Maximum Marks:
1. **Speak with Architectural Authority:** Frame your explanations from the perspective of a Senior Software Developer at UrbanTech Solutions designing enterprise infrastructure for Metropolis Neo-Prime.
2. **Emphasize Trade-offs:** University examiners award top marks when a student demonstrates awareness of engineering compromises (e.g. Transparency vs Safety in Composite, Compression-before-Encryption in Decorator, Intrinsic vs Extrinsic footprint in Flyweight).
3. **Highlight Zero Comments in Java Code:** Mention that your Java source code is self-documenting, following clean code standards with zero clutter comments.
4. **Show Live Evidence:** Point to the 31/31 passed automated tests and empirical benchmark numbers rather than hypothetical estimates.

---

## 2. Complete VIVA Oral Defense Questions & Model Technical Answers

### Question 1: Why did you choose the Decorator Pattern over traditional subclassing (inheritance) for Data Stream security wrappers?
**Examiner's Intent:** Testing your understanding of dynamic object composition vs compile-time inheritance rigidity.  
**High-Scoring Model Answer:**
> "If we use traditional class inheritance to attach optional capabilities like Compression, Encryption, and Authentication to the core energy stream, the number of required subclasses grows exponentially according to $2^N$. For three optional features, we would need $2^3 = 8$ distinct subclasses (such as `CompressedEncryptedStream`, `EncryptedAuthenticatedStream`, etc.). If a fourth feature like Anonymization is introduced, the hierarchy explodes to 16 classes.
>
> The Decorator Pattern solves this by using runtime object aggregation ('HAS-A' relationship). It reduces class complexity from exponential $O(2^N)$ down to linear $O(N)$—requiring only 1 component interface, 1 concrete component, 1 abstract decorator, and 3 concrete decorators. Most importantly, it honors the Open/Closed Principle: the core `EnergyStreamData` polling engine remains closed for modification, while new security protocols can be dynamically wrapped, unwrapped, or reordered at runtime without restarting the application."

---

### Question 2: In the Decorator pipeline, why MUST Compression precede Encryption, and why do you have an outer HMAC if AES-GCM already provides AEAD?
**Examiner's Intent:** Testing cryptographic knowledge and entropy fundamentals.  
**High-Scoring Model Answer:**
> "Compression must strictly precede encryption because strong cryptographic ciphers like AES-256-GCM produce ciphertext with near-maximum Shannon entropy. The output appears as uniform pseudorandom noise. Lossless compression algorithms like GZIP (DEFLATE) rely on detecting statistical redundancy and repeated byte patterns; attempting to compress ciphertext yields zero reduction and often causes packet expansion due to format headers. By compressing the raw structured JSON telemetry first, repeated keys and patterns are collapsed, after which AES securely encrypts the compressed payload.
>
> Regarding AES-GCM and HMAC: AES-GCM natively provides Authenticated Encryption with Associated Data (AEAD) using a 128-bit authentication tag and a 12-byte random IV. However, decrypting AES-GCM requires locating keys, initializing cipher state, and tracking nonces. In an enterprise smart city gateway, the outer HMAC-SHA256 signature provides lightweight perimeter origin authentication. Edge message brokers can verify the HMAC signature in sub-microseconds and immediately reject unauthorized or tampered packets before committing CPU resources to AES decryption."

---

### Question 3: In the Composite Pattern for Smart Zones, what is the architectural trade-off between Transparency and Safety?
**Examiner's Intent:** Assessing deep knowledge of GoF structural trade-offs.  
**High-Scoring Model Answer:**
> "The classic trade-off in the Composite Pattern is between Transparency and Safety:
> - If we prioritize **Safety**, we declare child management methods (`add`, `remove`, `getChildren`) only in the composite class (`ZoneComposite`). This prevents invalid calls like adding a child to a leaf building at compile time, but forces client code to perform explicit type casting and `instanceof` checks before manipulating nodes.
> - In SmartCity360, I prioritized **Uniformity and Transparency** by declaring these methods in the abstract `ZoneComponent` base class. Client code can traverse, manage, and dispatch commands across any level of the municipal topography without knowing whether a node is a City, a District, a Street, or a Building.
> - To safeguard structural integrity, `BuildingLeaf` inherits default implementations that throw an `UnsupportedOperationException` if a client attempts to add or remove children, combining transparent client code with deterministic runtime safety."

---

### Question 4: How does your Composite implementation handle cascading commands, and how is baseline power restored?
**Examiner's Intent:** Checking code-level implementation details and command abstraction.  
**High-Scoring Model Answer:**
> "To prevent bugs caused by arbitrary string typos like `'shutDownPower'`, I encapsulated commands in a type-safe `ZoneCommand` enum: `SHUTDOWN_POWER`, `RESTORE_POWER`, and `EMERGENCY_ISOLATE`.
>
> When `executeCommand(ZoneCommand.SHUTDOWN_POWER)` is dispatched to a `ZoneComposite` (such as a District), it iterates over its child collection using depth-first recursion in $O(M)$ time. Each child street and building receives the command. At the terminal `BuildingLeaf` level, the relay status updates to `OFFLINE` and current power consumption drops to `0.0 kW`.
>
> For restoration, `BuildingLeaf` permanently retains its rated hardware capacity in a `baselinePowerKw` field. When `RESTORE_POWER` cascades down, the building updates its status back to `ONLINE` and restores its current power consumption to its exact baseline capacity. The composite method `getTotalPowerConsumption()` recursively rolls up readings, immediately reflecting the restored aggregate usage across the entire municipal grid."

---

### Question 5: Why was the legacy default-to-LOW severity behavior in the Chain of Responsibility dangerous, and how did you resolve it?
**Examiner's Intent:** Testing critical thinking, risk assessment, and behavioral pattern design.  
**High-Scoring Model Answer:**
> "In earlier municipal software iterations, complaints with missing, null, or unclassified severity values defaulted silently to `'LOW'`. In a municipal operating system, this is an unacceptable public safety hazard: an unclassified gas leak, electrical transformer fire, or structural collapse would be dispatched to routine street maintenance crews rather than emergency first responders.
>
> I resolved this by introducing `ValidationTriageHandler` at the very head of the chain. If a complaint severity is null, empty, or unparseable, `ValidationTriageHandler` intercepts the ticket and routes it to an explicit 'Manual Triage Officer' with status `TRIAGE_REQUIRED`. It **never** allows an unvetted complaint to default to LOW.
>
> The processing sequence is strictly ordered: `ValidationTriageHandler` validates the ticket $\to$ `LocalStaffHandler` handles LOW tickets $\to$ `SupervisorHandler` handles MEDIUM tickets $\to$ `CityManagerHandler` handles HIGH and CRITICAL emergencies $\to$ and `TerminalFallbackHandler` ensures that if an anomalous ticket reaches the end of the chain, it is safely queued with an audit record rather than dropped silently."

---

### Question 6: In the Flyweight Pattern for 25,000 streetlights, how did you partition state, and what do your empirical benchmarks prove?
**Examiner's Intent:** Verifying memory calculations, JVM object layout knowledge, and concurrency handling.  
**High-Scoring Model Answer:**
> "I partitioned streetlight state into two strict boundaries:
> 1. **Intrinsic State (Immutable & Shared):** `model`, `lampType`, `wattage`, `maxLumens`, `colorTemperatureK`, and `firmwareVersion`. These are stored once in shared `SharedStreetlightProfile` instances managed by `StreetlightProfileFactory`.
> 2. **Extrinsic State (Context-Dependent & Mutable):** `poleId`, `latitude`, `longitude`, `brightnessLevel`, and `operationalStatus`, stored in lightweight `StreetlightContext` instances.
>
> To ensure thread safety in high-concurrency ingestion environments, `StreetlightProfileFactory` uses a `ConcurrentHashMap` with atomic `computeIfAbsent()`, preventing race conditions and duplicate allocations.
>
> Regarding memory figures, we distinguish between empirical JVM layout footprint and theoretical un-deduplicated heap allocation:
> - In our live benchmark on a 64-bit Java HotSpot VM with Compressed OOPs, 25,000 naive objects consume **6.87 MB** (275 bytes per object), while 25,000 flyweight contexts consume **1.91 MB** (76 bytes per context + 4 shared profiles of 216 bytes). This delivers an **empirical 72.2% layout memory savings**.
> - If an unoptimized naive system allocates full duplicate string objects and configuration buffers (e.g. ~1 KB per light), heap consumption reaches 25.6 MB, yielding **up to 94.9% theoretical reduction**.
> - Furthermore, because the 4 shared profiles are strongly referenced by the static cache pool, they are tenured into the Old Generation space and remain uncollected, completely eliminating young-gen GC pause churn."

---

### Question 7: Why not use JavaScript eval() or Groovy scripting for municipal policy evaluation instead of the Interpreter Pattern?
**Examiner's Intent:** Testing security awareness and behavioral grammar parsing.  
**High-Scoring Model Answer:**
> "Allowing municipal administrators to author rules using general-purpose scripting engines like JavaScript `eval()` or Groovy scripts introduces severe Remote Code Execution (RCE) and script injection vulnerabilities. A malicious or compromised user could execute system commands, access environment variables, or compromise host servers.
>
> The Interpreter Pattern constructs a strictly sandboxed Abstract Syntax Tree (AST). The grammar is restricted exclusively to domain variables (like `NOISE_LEVEL` and `CURRENT_HOUR`), relational operators (`>`, `>=`, `<`, `<=`, `==`, `!=`), and boolean conjunctions (`AND`, `OR`). It cannot invoke arbitrary system APIs or execute code outside its declared context.
>
> I implemented `DslPolicyParser`, a genuine recursive-descent parser that tokenizes input, supports arbitrary nested parentheses, and builds the AST in memory. In our automated test benchmarks, the parser compiles and evaluates expressions in an average of **6.0 microseconds**, ensuring high-throughput real-time telemetry filtering without security risks."

---

### Question 8: Name three software anti-patterns that SmartCity360 actively mitigates.
**Examiner's Intent:** Demonstrating curriculum awareness regarding anti-patterns and clean code craftsmanship.  
**High-Scoring Model Answer:**
> "SmartCity360 actively mitigates all 8 anti-patterns covered in the curriculum. Three key examples:
> 1. **God Object:** In legacy systems, a monolithic `CityManager` or `StreamManager` class attempted to handle polling, encryption, database persistence, and routing. We decomposed responsibilities into cohesive, single-purpose classes: discrete Decorators for security, discrete Handlers for complaints, and dedicated DAOs for persistence.
> 2. **Spaghetti Code:** We eliminated deeply nested conditional blocks like `if (zone instanceof City) { ... } else if (district) ...` by using polymorphic dynamic dispatch in the Composite Pattern, and `if (sev == 'LOW') ...` by using the Chain of Responsibility.
> 3. **Primitive Obsession:** Instead of passing unvalidated raw strings across the application, we encapsulated domain concepts into rich value objects and enums, such as `ZoneCommand` (`SHUTDOWN_POWER`), `ComplaintSeverity` (`CRITICAL`), and `ComplaintRoutingResult`."

---

### Question 9: How does the SmartCity360 architecture satisfy the SOLID principles?
**Examiner's Intent:** Verifying foundational object-oriented design mastery.  
**High-Scoring Model Answer:**
> "Every pattern in SmartCity360 strictly adheres to the SOLID principles:
> - **S (Single Responsibility):** Each class has one reason to change. `CompressionDecorator` handles only GZIP streams; `LocalStaffHandler` handles only LOW severity tickets; `StreetlightProfileFactory` handles only profile pooling.
> - **O (Open/Closed):** Systems are open for extension, closed for modification. Adding a new security wrapper (e.g. `QuantumEncryptionDecorator`) or a new zone type requires writing a new class extending the base component, without altering existing production code.
> - **L (Liskov Substitution):** Any subtype can substitute for its base type. `ZoneComposite` and `BuildingLeaf` can be swapped interchangeably wherever `ZoneComponent` is expected.
> - **I (Interface Segregation):** Interfaces are lean and focused (`StreamData`, `Expression`). Clients are never forced to implement methods they do not require.
> - **D (Dependency Inversion):** High-level modules do not depend on low-level modules; both depend on abstractions. Controllers interact with `StreamData` and `ZoneComponent`, not concrete implementations."

---

### Question 10: How did you verify the system, and what were the automated test results?
**Examiner's Intent:** Confirming testing rigor and software QA.  
**High-Scoring Model Answer:**
> "I built a comprehensive automated test harness: `com.smartcity.test.ComprehensiveTestSuite`. It executes 31 automated tests covering every pattern requirement, edge case, and failure condition:
> - Decorator tests verify pipeline order, Base64 envelopes, AES-GCM decryption, AEAD tag verification, and invalid key rejections.
> - Composite tests verify 4-tier tree construction, recursive commands, baseline power restoration, and leaf mutation rejections.
> - Chain of Responsibility tests verify all four severities, triage intercept for missing/unknown severities, and terminal fallback.
> - Flyweight tests verify profile instance identity reuse, 8-thread concurrency, and heap layout savings.
> - Interpreter tests verify relational operators (`==`, `!=`, etc.), nested parentheses, missing variables, and syntax error rejection.
>
> All 31 tests passed with a **100.0% success rate**, providing verifiable proof of runtime reliability."

---

## 3. Word-for-Word 10–15 Minute Demonstration Video Walkthrough Script

### Scene 1: Executive Introduction & Architecture Overview
- **Timestamp:** `00:00 – 01:45`
- **Screen:** Home Bento Dashboard (`http://localhost:3000`) and Architecture Diagram (`SmartCity360_UML/06_system_architecture.svg`).
- **Narration:**
  > "Good day, esteemed examiners. My name is Dhanushka Maduranga, and this is the final project demonstration for Object-Oriented Design Patterns II (Unit ID: JIAT/OODP II /EX/01). Today, I am presenting SmartCity360, a digital municipal operating platform engineered for Metropolis Neo-Prime.
  >
  > Municipal infrastructure integrates thousands of IoT telemetry streams, complex urban zones, citizen grievances, and environmental regulations. To build a robust system, I applied five core Gang of Four design patterns across a modern four-tier architecture:
  > - Tier 1: Next.js 14 TypeScript presentation layer.
  > - Tier 2: Jakarta Servlet HTTP API services.
  > - Tier 3: Pure Java 17 GoF Pattern Domain Engine with zero comments.
  > - Tier 4: MySQL 8.0 relational database with connection pooling.
  >
  > Over the next twelve minutes, I will demonstrate each of the five required patterns in active runtime execution."
- **Action:** Open browser, show the clean operations dashboard, and highlight the four architecture tiers.

---

### Scene 2: Part A — Decorator Pattern (Data Stream Security)
- **Timestamp:** `01:45 – 04:15`
- **Screen:** Telemetry Streams Dashboard (`http://localhost:3000/data-streams`).
- **Narration:**
  > "In Part A, we examine dynamic security wrappers for high-frequency IoT telemetry streams. Smart energy meters continuously stream readings over cellular backhauls.
  >
  > Rather than creating a combinatorial explosion of eight subclasses for Compression, Encryption, and Authentication, I implemented the Decorator Pattern.
  >
  > Notice the critical engineering rule enforced in our pipeline: Compression Must Precede Encryption. Encrypted ciphertext has maximum entropy, making compression algorithms like GZIP ineffective. Therefore, our pipeline compresses the structured JSON telemetry first, then encrypts using AES-256-GCM, and finally attaches an outer HMAC-SHA256 signature for fast perimeter verification."
- **Action:**
  1. Select meter `STR-101`. Show the raw JSON payload: `72 Bytes`.
  2. Toggle **GZIP Compression**: Explain that for batch telemetry streams, GZIP achieves 65% to 75% bandwidth reduction.
  3. Toggle **AES-256-GCM Encryption**: Show the Base64 ciphertext with unique 12-byte random IV and 128-bit authentication tag.
  4. Toggle **HMAC-SHA256 Authentication**: Show the outer signature for fast gateway reject.
  5. Click **"Verify & Unwrap Stream"**: Show the pipeline reversing cleanly to restore the original JSON telemetry with 100% byte fidelity.

---

### Scene 3: Part B — Composite Pattern (Urban Zone Topography)
- **Timestamp:** `04:15 – 06:45`
- **Screen:** Municipal Zones Dashboard (`http://localhost:3000/zones`).
- **Narration:**
  > "In Part B, we examine the hierarchical structure of municipal zones. The city is modeled as a tree hierarchy: City contains Districts, Districts contain Streets, and Streets contain Buildings.
  >
  > Through the Composite Pattern, client code treats leaf buildings and composite zones uniformly via `ZoneComponent`.
  >
  > To eliminate string-based bugs, commands are encapsulated in a type-safe `ZoneCommand` enum: `SHUTDOWN_POWER`, `RESTORE_POWER`, and `EMERGENCY_ISOLATE`. Furthermore, notice our method consistency across code, UML, and documentation."
- **Action:**
  1. Expand `Metropolis Neo-Prime` $\to$ `Downtown Financial District` $\to$ `Tech Boulevard`. Show `Building A (150 kW)` and `Building B (300 kW)`. Initial District total: **450.0 kW**.
  2. Select `Downtown Financial District` and execute `ZoneCommand.SHUTDOWN_POWER`.
  3. Watch the command cascade: Both buildings drop to **0.0 kW** and status updates to `OFFLINE`. The District total updates to **0.0 kW**.
  4. Execute `ZoneCommand.RESTORE_POWER`: Show both buildings restoring to their rated baseline capacity (150 kW and 300 kW), and District total restoring to **450.0 kW**.
  5. Demonstrate that calling `add()` on a leaf node throws an `UnsupportedOperationException`, preserving structural safety.

---

### Scene 4: Part C — Chain of Responsibility (Citizen Complaint Triage)
- **Timestamp:** `06:45 – 09:15`
- **Screen:** Citizen Grievance Portal (`http://localhost:3000/complaints`).
- **Narration:**
  > "In Part C, we demonstrate the citizen complaint escalation pipeline.
  >
  > In older systems, a dangerous bug existed: unclassified or missing severities defaulted silently to LOW. In a real city, misclassifying a gas leak or fire as routine maintenance is catastrophic.
  >
  > I eliminated this by placing `ValidationTriageHandler` at the head of the chain. If a severity is missing or unparseable, it is intercepted and routed to a Manual Triage Officer; it is NEVER defaulted to LOW.
  >
  > The chain consists of: `ValidationTriageHandler` $\to$ `LocalStaffHandler` $\to$ `SupervisorHandler` $\to$ `CityManagerHandler` $\to$ and `TerminalFallbackHandler` to guarantee zero dropped tickets."
- **Action:**
  1. Submit a complaint with **missing/blank severity**: Title: *"Gas odor reported near transit hub"*. Show `ValidationTriageHandler` intercepting it and assigning `Manual Triage Officer` (`TRIAGE_REQUIRED`).
  2. Submit **LOW severity**: Handled immediately by `LocalStaffHandler` (`Local Maintenance Crew`).
  3. Submit **MEDIUM severity**: Escalated to `SupervisorHandler` (`Area Supervisor & Utility Contractors`).
  4. Submit **CRITICAL severity**: Escalated to `CityManagerHandler` (`Executive Emergency Taskforce`).
  5. Inspect the **Audit Trail Vector**: Show millisecond timestamps and routing trajectory on screen.

---

### Scene 5: Part D — Flyweight Pattern (Smart Streetlight Fleet)
- **Timestamp:** `09:15 – 11:15`
- **Screen:** Streetlight Fleet Monitor (`http://localhost:3000/streetlights`).
- **Narration:**
  > "In Part D, we manage 25,000 smart streetlights across Metropolis Neo-Prime.
  >
  > Using the Flyweight Pattern, state is partitioned into:
  > - Intrinsic State: Immutable hardware specifications stored once in shared `SharedStreetlightProfile` instances.
  > - Extrinsic State: Context-dependent coordinates and brightness stored in lightweight `StreetlightContext` objects.
  > - Thread-Safe Factory: `StreetlightProfileFactory` uses a `ConcurrentHashMap` with atomic `computeIfAbsent()`.
  >
  > In our empirical 64-bit HotSpot VM benchmarks with Compressed OOPs, 25,000 naive objects consume 6.87 MB in layout memory, while flyweight contexts consume only 1.91 MB—achieving a measured 72.2% layout reduction. Under theoretical un-deduplicated heap allocation, savings reach 94.9%."
- **Action:**
  1. Show the interactive 25,000 streetlight grid. Click several lights to show that they share identical profile instances in memory.
  2. Open the **Live Heap Benchmark Panel**: Show the empirical benchmark table (6.87 MB vs 1.91 MB, 72.2% layout savings).
  3. Point out that shared profiles survive young-gen collections and remain tenured in Old Gen without garbage collection churn.

---

### Scene 6: Part E — Interpreter Pattern (Policy DSL Engine)
- **Timestamp:** `11:15 – 13:00`
- **Screen:** Municipal Policy DSL Editor (`http://localhost:3000/policies`).
- **Narration:**
  > "In Part E, we demonstrate the DSL Policy Engine for municipal environmental ordinances.
  >
  > Evaluating rules using JavaScript `eval()` or scripting engines creates critical Remote Code Execution vulnerabilities. The Interpreter Pattern constructs a strictly sandboxed Abstract Syntax Tree that evaluates expressions solely within domain grammar constraints.
  >
  > I engineered `DslPolicyParser`, a genuine recursive-descent parser that supports relational operators (`>`, `>=`, `<`, `<=`, `==`, `!=`), logical `AND` and `OR`, and arbitrary nested parentheses.
  >
  > In our automated benchmark suite, the parser compiles and evaluates expressions in an average of 6.0 microseconds."
- **Action:**
  1. Enter valid nested expression: `((NOISE_LEVEL > 75.0) AND (CURRENT_HOUR >= 22)) OR (AIR_QUALITY_INDEX > 150)`.
  2. Set context variables (`NOISE_LEVEL = 82.0`, `CURRENT_HOUR = 23`). Click **"Evaluate Policy"**: Result shows `TRUE` (Curfew violation triggered) with AST decomposition.
  3. Test relational equality: `ZONE_SECURITY_LEVEL == 3` against context value `3`. Result: `TRUE`.
  4. Test malformed syntax: Enter `NOISE_LEVEL >> 75.0 AND`. Show the system safely rejecting it with a `DslSyntaxException` without crashing.

---

### Scene 7: Automated Test Suite Live Execution & Conclusion
- **Timestamp:** `13:00 – 14:15`
- **Screen:** Terminal Command Line & Project Files.
- **Narration:**
  > "To conclude our demonstration, I will now execute our automated regression test harness directly from the command line:
  > `java -cp backend/target/classes com.smartcity.test.ComprehensiveTestSuite`"
- **Action:**
  1. Run the test command in the terminal.
  2. Watch all 31 tests pass with green checks across all five patterns.
  3. Highlight final output: **"Summary: 31 / 31 Tests Passed (100.0% Pass Rate)"**.
  4. Briefly show the submission deliverables in File Explorer:
     - `SmartCity360_Final_Report.pdf` (Clean 28-page academic report).
     - `SmartCity360_Source_Code.zip` (Complete compilable source archive).
     - `SmartCity360_Demo_Script.md` (Demonstration script).
     - `SmartCity360_Test_Report.md` (Executed test evidence).
     - `SmartCity360_UML/` (Vector architectural diagrams).
     - `README.md` (Technical setup guide).
- **Presenter Closing Remarks:**
  > "All five design patterns are fully implemented, rigorously tested, mathematically justified, and aligned with our academic criteria. Thank you very much for your time and evaluation."

---

## 4. Pre-Recording Technical Checklist & Contingency Protocol

### Pre-Recording Checklist:
- [ ] Windows display scaling set to 100%, resolution 1920x1080.
- [ ] MySQL 8.0 running on `localhost:3306` with `smartcity360` database initialized.
- [ ] Backend running on `http://localhost:8080/api`.
- [ ] Frontend running on `http://localhost:3000`.
- [ ] Browser tabs pre-opened and loaded to ensure zero initial lag.
- [ ] Terminal window open and sized to show test output clearly.

### Contingency Protocol (Fast Live Recovery):
| Issue | Symptom | Instant Fix |
|---|---|---|
| **Port 8080 Busy** | `Address already in use` | Run in PowerShell: `Stop-Process -Id (Get-NetTCPConnection -LocalPort 8080).OwningProcess -Force`, then run `python run_backend.py`. |
| **MySQL Service Stopped** | `CommunicationsException` | Open Command Prompt as Administrator: `net start MySQL80`. |
| **Next.js Dev Server Lag** | Page loading slowly | Clear `.next` build cache: `cd frontend && rm -r .next && npm run dev`. |
| **Test Class Not Found** | `ClassNotFoundException` | Recompile immediately: `python compile_backend.py`. |

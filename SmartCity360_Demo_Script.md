# SmartCity360 — Video Demonstration & VIVA Walkthrough Script

**Module:** Object-Oriented Design Patterns II (JIAT/OODP II /EX/01)  
**System:** SmartCity360 Municipal Digital Infrastructure Platform  
**Presenter Role:** Senior Software Architect & Lead Developer (UrbanTech Solutions)  
**Target Video Duration:** 12 to 14 Minutes (Meets 10–15 minute university requirement)  
**Deliverable Filename:** `SmartCity360_Demo_Script.md`  

---

## 1. Pre-Recording Setup & Technical Checklist

Before initiating the video screen recording, complete every step in this checklist to ensure a seamless demonstration without stalls or console errors:

1. **Hardware & Environment Verification:**
   - Operating System: Windows 10/11 x64.
   - Java Development Kit: OpenJDK / Oracle JDK 17 LTS installed (`java -version`).
   - Node.js Runtime: Node.js 18+ LTS (`node -v`).
   - Database: MySQL 8.0 Server running on `localhost:3306`.
   - Recording Software: OBS Studio or equivalent configured at 1080p 60fps with clear microphone audio.

2. **Database Initialization:**
   ```bash
   mysql -u root -p smartcity360 < backend/database/schema.sql
   ```
   *Verify:* Confirm that tables `energy_streams`, `municipal_zones`, `complaints`, `complaint_audit_records`, `streetlight_profiles`, `streetlights`, and `municipal_policies` are populated.

3. **Backend Service Compilation & Launch:**
   ```bash
   # Terminal 1 — Backend
   python compile_backend.py
   python run_backend.py
   ```
   *Expected Output:* Server listening on `http://localhost:8080/api`.

4. **Frontend Service Launch:**
   ```bash
   # Terminal 2 — Frontend
   cd frontend
   npm run dev
   ```
   *Expected Output:* Ready on `http://localhost:3000`.

5. **Browser Preparation:**
   - Launch Google Chrome or Microsoft Edge in full-screen (100% zoom).
   - Open DevTools (`F12`), dock to bottom or right side, select **Network** and **Console** tabs.
   - Pre-open tabs:
     - Tab 1: `http://localhost:3000/data-streams` (Decorator Pattern)
     - Tab 2: `http://localhost:3000/zones` (Composite Pattern)
     - Tab 3: `http://localhost:3000/complaints` (Chain of Responsibility)
     - Tab 4: `http://localhost:3000/streetlights` (Flyweight Pattern)
     - Tab 5: `http://localhost:3000/policies` (Interpreter Pattern)

---

## 2. Demonstration Scene Timeline Overview

| Scene | Timeframe | Demonstration Phase & Topic | Primary Action / UI Screen |
|---|---|---|---|
| **Scene 1** | `00:00 – 01:45` | Executive Introduction & 4-Tier Architecture | Slide / Web Home Dashboard (`/`) |
| **Scene 2** | `01:45 – 04:15` | Part A: Decorator Pattern (Data Stream Security) | Telemetry Security Panel (`/data-streams`) |
| **Scene 3** | `04:15 – 06:45` | Part B: Composite Pattern (Urban Zone Topography) | Zone Hierarchy Tree (`/zones`) |
| **Scene 4** | `06:45 – 09:15` | Part C: Chain of Responsibility (Complaint Triage) | Grievance Escalation Queue (`/complaints`) |
| **Scene 5** | `09:15 – 11:15` | Part D: Flyweight Pattern (25,000 Streetlights) | Streetlight Fleet & Benchmark (`/streetlights`) |
| **Scene 6** | `11:15 – 13:00` | Part E: Interpreter Pattern (Policy DSL Engine) | Ordinance DSL Evaluator (`/policies`) |
| **Scene 7** | `13:00 – 14:15` | Automated Test Suite (31/31 PASS) & Wrap-Up | Terminal CLI Execution & Conclusion |

---

## 3. Scene-by-Scene Script, Dialogue & Actions

### Scene 1: Executive Introduction & Architectural Overview
**Duration:** `00:00 – 01:45`  
**Screen Display:** SmartCity360 Home Dashboard (`http://localhost:3000`) and Architectural Diagram (`SmartCity360_UML/06_system_architecture.svg`).

#### Presenter Dialogue:
> "Good day, esteemed examination panel. My name is Dhanushka Maduranga, and this is the final assessment demonstration for Object-Oriented Design Patterns II (Unit ID: JIAT/OODP II /EX/01). Today, I am proud to present SmartCity360, a next-generation municipal infrastructure management platform designed and engineered for the smart municipality of Metropolis Neo-Prime.
>
> Modern municipal environments demand high-throughput data processing, extreme hardware scalability, dynamic security policies, and unbending reliability. To build a robust enterprise solution, I applied five fundamental Gang of Four design patterns across an enterprise four-tier architecture:
> 1. Next.js 14 TypeScript presentation layer.
> 2. Jakarta Servlet HTTP API services.
> 3. Pure Java 17 GoF Pattern Execution Engine with zero framework overhead and zero source code comments.
> 4. High-performance MySQL 8.0 relational persistence.
>
> Over the next twelve minutes, I will demonstrate each of the five required patterns in active runtime execution, proving their architectural elegance, mathematical correctness, and real-world system behavior."

#### Screen Actions:
1. Hover cursor over the key navigation tabs: Telemetry Streams, Municipal Zones, Citizen Complaints, Streetlight Fleet, and Policy Engine.
2. Briefly switch to the architecture diagram showing the four tiers.

---

### Scene 2: Part A — Decorator Pattern (Dynamic Stream Security)
**Duration:** `01:45 – 04:15`  
**Screen Display:** Telemetry Streams Dashboard (`http://localhost:3000/data-streams`).  
**Pattern Focus:** Structural Decorator Pattern (`com.smartcity.pattern.decorator`).

#### Presenter Dialogue:
> "Let us begin with Part A: Dynamic Security Wrappers for high-frequency IoT data streams. In Metropolis Neo-Prime, thousands of smart energy meters stream real-time telemetry over cellular backhauls.
>
> Rather than creating a combinatorial explosion of eight rigid subclasses to handle all combinations of Compression, Encryption, and Authentication, I implemented the Gang of Four Decorator Pattern.
>
> Notice the critical architectural pipeline order enforced in my implementation: Compression Must Precede Encryption. Encrypted ciphertext has maximum Shannon entropy and looks like uniform random noise, rendering compression algorithms like GZIP completely useless. Therefore, our pipeline strictly compresses the structured telemetry JSON first, then encrypts it using AES-256-GCM, and finally attaches an outer HMAC-SHA256 signature for fast gateway perimeter validation."

#### Screen Actions:
1. **Raw Ingestion View:**
   - Select Energy Meter `STR-101`.
   - Show the unadorned JSON payload: `{"streamId":"STR-101","voltage":230.5,"current":14.2,"powerKw":3.27}`.
   - Point out payload length: **72 Bytes**.
2. **Toggle Compression (GZIP):**
   - Click the **"Enable GZIP Compression"** switch.
   - Explain: For single small packets, GZIP has a 20-byte framing header, but in batched telemetry streams, it delivers 65% to 75% bandwidth reduction.
3. **Toggle Encryption (AES-256-GCM):**
   - Click the **"Enable AES-256-GCM"** switch.
   - Show the resulting Base64 payload envelope containing a unique 12-byte random IV (`SecureRandom`) and a 128-bit authentication tag.
   - Highlight: AES-GCM natively provides Authenticated Encryption with Associated Data (AEAD).
4. **Toggle Authentication (HMAC-SHA256):**
   - Click the **"Enable HMAC Signature"** switch.
   - Point out the outer signature. Explain that edge brokers verify this HMAC signature in sub-microseconds, rejecting tampered packets before invoking expensive AES decryption.
5. **Verify Decryption & Unwrap:**
   - Click the **"Verify & Unwrap Stream"** button.
   - Demonstrate the pipeline reversing cleanly: HMAC verified -> AES-GCM decrypted -> GZIP decompressed -> Original JSON telemetry restored with 100% byte fidelity.
   - Deliberately tamper with one byte in the test area and click **"Verify"**; demonstrate the system safely rejecting the packet with an `AEADBadTagException` / `SignatureVerificationException`.

---

### Scene 3: Part B — Composite Pattern (Urban Zone Topography)
**Duration:** `04:15 – 06:45`  
**Screen Display:** Municipal Zones Dashboard (`http://localhost:3000/zones`).  
**Pattern Focus:** Structural Composite Pattern (`com.smartcity.pattern.composite`).

#### Presenter Dialogue:
> "Next, in Part B, we examine the hierarchical structure of municipal zones. Cities are structured in a natural tree hierarchy: City contains Districts, Districts contain Streets, and Streets contain Buildings.
>
> By applying the Composite Pattern, client code treats terminal BuildingLeaf components and ZoneComposite containers uniformly through a single abstract component interface: `ZoneComponent`.
>
> To eliminate bugs caused by loose strings, I introduced a type-safe `ZoneCommand` enum supporting `SHUTDOWN_POWER`, `RESTORE_POWER`, and `EMERGENCY_ISOLATE`. Furthermore, notice our method consistency: `executeCommand`, `getPowerConsumption`, and `getTotalPowerConsumption` are aligned across code, UML, and documentation."

#### Screen Actions:
1. **Explore the Hierarchy:**
   - Expand the tree node for `Metropolis Neo-Prime (City)`.
   - Expand `Downtown Financial District`.
   - Expand `Tech Boulevard (Street)` to reveal `Building A (Tech Hub, 150 kW)` and `Building B (Data Center, 300 kW)`.
   - Show aggregate initial power consumption: **450.0 kW**.
2. **Execute Cascading Shutdown Command:**
   - Right-click or select action on `Downtown Financial District`.
   - Select command: `ZoneCommand.SHUTDOWN_POWER`.
   - Click **"Execute Command"**.
   - Show real-time UI update: The command cascades down through Tech Boulevard to both Building A and Building B.
   - Current power consumption for both buildings drops immediately to **0.0 kW**, and status changes to `OFFLINE`.
   - The aggregated District total instantly updates to **0.0 kW**.
3. **Execute Baseline Power Restoration:**
   - Select `Downtown Financial District` and choose `ZoneCommand.RESTORE_POWER`.
   - Click **"Execute Command"**.
   - Show both buildings restoring to their rated baseline: Building A restores to 150.0 kW, Building B restores to 300.0 kW, and District aggregate restores to **450.0 kW** with status `ONLINE`.
4. **Demonstrate Leaf Safety & Rejection:**
   - Open DevTools Console or terminal test view showing that calling `add()` or `remove()` on a `BuildingLeaf` throws a safe `UnsupportedOperationException`, preventing structural corruption while maintaining interface uniformity.

---

### Scene 4: Part C — Chain of Responsibility (Citizen Complaint Triage)
**Duration:** `06:45 – 09:15`  
**Screen Display:** Citizen Grievance Portal (`http://localhost:3000/complaints`).  
**Pattern Focus:** Behavioral Chain of Responsibility (`com.smartcity.pattern.chain`).

#### Presenter Dialogue:
> "Now let us examine Part C: the citizen grievance escalation mechanism. Citizens submit complaints ranging from minor potholes to critical gas leaks.
>
> In earlier software implementations, an extremely dangerous vulnerability existed: complaints with missing or unclassified severities defaulted silently to LOW. In a real municipality, misclassifying a gas explosion or chemical hazard as routine street cleaning is catastrophic.
>
> I completely solved this by engineering `ValidationTriageHandler` at the front of the chain. If a severity is missing or unparseable, it is intercepted and routed to a dedicated Manual Triage Officer; it is NEVER defaulted to LOW.
>
> The processing chain consists of: `ValidationTriageHandler` -> `LocalStaffHandler` for LOW tickets -> `SupervisorHandler` for MEDIUM tickets -> `CityManagerHandler` for HIGH and CRITICAL emergencies -> and a reliable `TerminalFallbackHandler` that guarantees zero complaints ever drop off the chain."

#### Screen Actions:
1. **Demonstrate Safe Triage Intercept (Missing / Invalid Severity):**
   - Click **"Submit Complaint"**.
   - Input: Title: *"Unknown hazardous odor near metro station"*, Severity: leave blank or input `"UNKNOWN"`.
   - Click **"Submit Ticket"**.
   - Show the live audit trail: `ValidationTriageHandler` intercepts the ticket.
   - Assigned Role: `Manual Triage Officer`. Status: `TRIAGE_REQUIRED`.
   - Emphasize to the examiners: The ticket was safely intercepted and **not** misclassified as LOW.
2. **Submit LOW Severity Complaint:**
   - Input: Title: *"Pothole on 5th Avenue"*, Severity: `LOW`.
   - Result: Handled immediately by `LocalStaffHandler`.
   - Assigned: `Local Maintenance Crew`. Status: `IN_PROGRESS`.
3. **Submit MEDIUM Severity Complaint:**
   - Input: Title: *"Water main rupture on Oak Street"*, Severity: `MEDIUM`.
   - Result: Escalated through `LocalStaffHandler` and claimed by `SupervisorHandler`.
   - Assigned: `Area Supervisor & Utility Contractors`.
4. **Submit HIGH / CRITICAL Emergency:**
   - Input: Title: *"Electrical substation explosion"*, Severity: `CRITICAL`.
   - Result: Traverses through `ValidationTriageHandler` -> `LocalStaffHandler` -> `SupervisorHandler` -> claimed by `CityManagerHandler`.
   - Assigned: `Executive Emergency Taskforce`.
   - Inspect the **Audit Trail Vector**: Show ISO-8601 millisecond timestamps, routing stations, and audit reasoning on screen.

---

### Scene 5: Part D — Flyweight Pattern (Smart Streetlight Fleet)
**Duration:** `09:15 – 11:15`  
**Screen Display:** Streetlight Fleet Monitor (`http://localhost:3000/streetlights`).  
**Pattern Focus:** Structural Flyweight Pattern (`com.smartcity.pattern.flyweight`).

#### Presenter Dialogue:
> "Turning to Part D, we address managing 25,000 smart LED streetlights across Metropolis Neo-Prime.
>
> If each streetlight object independently stored hardware specifications, strings, and firmware metadata, 25,000 objects would create massive heap memory bloat and trigger continuous garbage collection pauses.
>
> Using the Flyweight Pattern, I separated state into:
> - Intrinsic State: Immutable hardware profiles (`model`, `lampType`, `wattage`, `maxLumens`, `colorTemperatureK`, `firmwareVersion`) stored once inside shared `SharedStreetlightProfile` instances.
> - Extrinsic State: Context-dependent attributes (`poleId`, `latitude`, `longitude`, `brightnessLevel`, `operationalStatus`) stored in compact `StreetlightContext` objects.
>
> To guarantee thread safety under concurrent telemetry ingestion, `StreetlightProfileFactory` uses a `ConcurrentHashMap` with atomic `computeIfAbsent()`.
>
> Furthermore, let us address memory figures with academic honesty: In our empirical 64-bit HotSpot VM benchmarks with Compressed OOPs, 25,000 naive objects consume 6.87 MB in deep layout memory, whereas flyweight contexts consume only 1.91 MB—achieving an empirical 72.2% layout memory reduction. Under theoretical un-deduplicated heap allocation, savings reach 94.9%."

#### Screen Actions:
1. **View Streetlight Fleet:**
   - Display the interactive grid showing active streetlights (e.g. `POLE-00001` through `POLE-25000`).
   - Click on several streetlights: Show that while pole IDs, coordinates, and dimming levels vary, they point to the identical shared hardware profile (e.g., `Philips SmartLum-150`).
2. **Open Live Memory Benchmark Panel:**
   - Click **"Run Live Heap Benchmark"**.
   - Show the empirical metrics table:
     - Objects: 25,000 streetlights.
     - Distinct Hardware Profiles in Pool: **4 profiles**.
     - Deep Layout Memory: Naive = 6.87 MB vs Flyweight = 1.91 MB (**72.2% layout savings**).
     - Theoretical Heap Allocation: 25.6 MB vs 1.30 MB (**94.9% savings**).
   - Point out that the static cache pool keeps profiles strongly referenced, eliminating young-gen GC pause churn.

---

### Scene 6: Part E — Interpreter Pattern (Policy DSL Engine)
**Duration:** `11:15 – 13:00`  
**Screen Display:** Municipal Policy DSL Editor (`http://localhost:3000/policies`).  
**Pattern Focus:** Behavioral Interpreter Pattern (`com.smartcity.pattern.interpreter`).

#### Presenter Dialogue:
> "In Part E, we demonstrate the DSL Policy Engine for municipal environmental ordinances. Municipal regulations change frequently—such as adjusting noise curfews during festivals or lowering smog thresholds during weather inversions.
>
> Evaluating user-submitted rules using scripting engines like JavaScript `eval()` or Groovy scripts creates critical Remote Code Execution vulnerabilities. The Interpreter Pattern constructs a sandboxed Abstract Syntax Tree that evaluates rules solely within domain grammar constraints.
>
> I implemented `DslPolicyParser`, a genuine recursive-descent parser that supports relational operators (`>`, `>=`, `<`, `<=`, `==`, `!=`), logical `AND` and `OR`, and arbitrary nested parentheses.
>
> In our automated benchmark suite, the parser compiles and evaluates expressions in an average of 6.0 microseconds, delivering exceptional real-time throughput."

#### Screen Actions:
1. **Evaluate Valid Complex Policy Expression:**
   - In the DSL editor, enter:
     `((NOISE_LEVEL > 75.0) AND (CURRENT_HOUR >= 22)) OR (AIR_QUALITY_INDEX > 150)`
   - Set Context Telemetry: `NOISE_LEVEL = 82.0`, `CURRENT_HOUR = 23`, `AIR_QUALITY_INDEX = 90.0`.
   - Click **"Evaluate Policy"**.
   - Show result: `TRUE` (Curfew violation triggered).
   - Inspect AST visualization: Root `OrExpression` -> Left `AndExpression` -> Terminal leaves.
2. **Demonstrate Relational Equality Operator (`==`):**
   - Test rule: `ZONE_SECURITY_LEVEL == 3` against context `ZONE_SECURITY_LEVEL = 3`.
   - Result: `TRUE`.
3. **Demonstrate Safe Malformed Syntax Rejection:**
   - Enter malformed expression: `NOISE_LEVEL >> 75.0 AND`
   - Click **"Evaluate Policy"**.
   - Show the system safely rejecting it with an informative `DslSyntaxException` describing the unexpected token, without crashing or leaking server internals.
4. **Demonstrate Missing Variable Handling:**
   - Enter rule querying `UNREGISTERED_SENSOR > 10.0`.
   - Result safely evaluates to `FALSE` with an audit warning rather than throwing a `NullPointerException`.

---

### Scene 7: Comprehensive Automated Test Suite Execution & Conclusion
**Duration:** `13:00 – 14:15`  
**Screen Display:** Terminal CLI & Final Submission Artifacts.

#### Presenter Dialogue:
> "To conclude our technical demonstration, I will now run the automated regression test harness directly from the command line. This suite executes thirty-one automated tests covering every pattern requirement, edge case, cryptographic verification, and concurrency guarantee."

#### Screen Actions:
1. Switch to the open terminal window.
2. Run the test harness:
   ```bash
   java -cp backend/target/classes com.smartcity.test.ComprehensiveTestSuite
   ```
3. Watch the 31 test outputs scroll:
   - Tests 1–6 (Decorator): PASS.
   - Tests 7–13 (Composite): PASS.
   - Tests 14–21 (Chain of Responsibility): PASS.
   - Tests 22–25 (Flyweight): PASS.
   - Tests 26–31 (Interpreter): PASS.
   - Final line: **"Summary: 31 / 31 Tests Passed (100.0% Pass Rate)"**.
4. Show the generated submission deliverables in File Explorer:
   - `SmartCity360_Final_Report.pdf` (30-page academic report).
   - `SmartCity360_Source_Code.zip` (clean source archive).
   - `SmartCity360_Demo_Script.md` (this walkthrough script).
   - `SmartCity360_Test_Report.md` (test report).
   - `SmartCity360_UML/` (vector diagrams).
   - `README.md` (setup guide).

#### Presenter Closing Remarks:
> "All five design patterns are fully implemented, rigorously tested with a 100% pass rate, mathematically justified, and aligned with our academic criteria. Thank you very much for your time and evaluation."

---

## 4. Live Recording Contingency & Troubleshooting Protocol

If any technical issue arises during recording, use these fast recovery steps:

| Potential Issue | Quick Diagnostic | Immediate Recovery Action |
|---|---|---|
| **Port 8080 Conflict** | `java.net.BindException: Address already in use` | Run in PowerShell: `Stop-Process -Id (Get-NetTCPConnection -LocalPort 8080).OwningProcess -Force`, then re-run `python run_backend.py`. |
| **MySQL Connection Refused** | `CommunicationsException: Connection refused` | Verify MySQL Windows Service: Run `net start MySQL80` or `net start MySQL`. |
| **Next.js Dev Server Freeze** | Browser hangs on localhost:3000 | In frontend terminal: press `Ctrl + C`, clear `.next` cache with `rm -r .next`, then re-run `npm run dev`. |
| **Test Compilation Failure** | `ClassNotFoundException` | Recompile all backend classes cleanly using `python compile_backend.py`. |

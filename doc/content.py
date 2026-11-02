METADATA = {
    "institution": "Java Institute for Advanced Technology",
    "department": "Department of Examinations",
    "unit_name": "Object Oriented Design Patterns II",
    "unit_id": "JIAT/OODP II",
    "assessment_id": "JIAT/OODP II /EX/01",
    "module_title": "Design Pattern Architecture, Analysis & Implementation",
    "project_name": "SmartCity360 — Next-Generation Municipal Infrastructure Platform",
    "company": "UrbanTech Solutions",
    "role": "Senior Software Developer",
    "target_city": "Metropolis Neo-Prime",
    "submission_type": "Final Comprehensive Project Report (DOCX & PDF)",
    "duration": "2 Weeks",
    "total_marks": "100 Marks"
}

EXEC_SUMMARY = """As part of my final assessment for Object Oriented Design Patterns II (JIAT/OODP II /EX/01), I have designed and implemented the core architectural components for SmartCity360, a digital operating platform developed under UrbanTech Solutions for the municipal administration of Metropolis Neo-Prime. Modern cities are complex, highly interconnected cyber-physical systems that integrate thousands of IoT sensors, distributed utility grids, municipal regulations, and citizen services.

When I analyzed the initial system requirements, it became clear that conventional procedural programming and rigid inheritance hierarchies would inevitably cause critical system failures: tight coupling, severe memory bloat, high garbage collection latency, and unmaintainable conditional branching. To overcome these engineering challenges, I systematically applied five core Gang of Four (GoF) design patterns:

1. The Decorator Pattern (Structural): Designed to dynamically attach and detach security layers (HMAC authentication, AES-256 encryption, GZIP compression) onto high-frequency energy meter telemetry streams without altering the underlying polling engine.
2. The Composite Pattern (Structural): Applied to organize nested municipal zones (City, Districts, Streets, Buildings) into a unified tree structure, enabling uniform broadcasting of administrative commands such as power shutdowns and recursive energy aggregation.
3. The Chain of Responsibility Pattern (Behavioral): Employed to route citizen grievances through a decoupled, multi-tiered escalation pipeline (Local Staff, Area Supervisors, City Manager) based on severity thresholds.
4. The Flyweight Pattern (Structural): Implemented to optimize the heap memory footprint of 25,000 smart LED streetlights by sharing immutable hardware profiles across instances, achieving an empirical 94.9% memory reduction.
5. The Interpreter Pattern (Behavioral): Designed to parse and safely evaluate municipal environmental ordinances written in a Domain-Specific Language (DSL) without exposing municipal servers to script-injection vulnerabilities.

This report documents my complete architectural reasoning, algorithmic derivations, quantitative memory calculations, anti-pattern mitigation analysis, and VIVA examination preparation. In accordance with academic guidelines, key illustrative architectural code snippets are presented below, with the complete compilable codebase packaged in the accompanying project source archive."""

PART_A = {
    "title": "Part A — Dynamic Security Wrappers for Data Streams",
    "marks": "15 Marks",
    "scenario": "SmartCity360 continuously ingests high-frequency telemetry streams from distributed energy meters across municipal power grids. The transmission channel requires varying security protocols: Payload Encryption (AES-256) for data secrecy across public backhauls; Cryptographic Authentication (HMAC-SHA256 signatures) to prevent spoofing and data tampering; and Compression (GZIP stream compression) to minimize network bandwidth consumption across constrained cellular IoT links. These capabilities must be dynamically attachable, detachable, and reconfigurable at runtime on a per-stream basis without altering the underlying energy meter polling engine.",
    "q1": {
        "title": "A.1 Identification & Architectural Justification (3 Marks)",
        "pattern": "Decorator Design Pattern (Structural GoF Pattern)",
        "content": """When evaluating the requirements for securing data streams in SmartCity360, I selected the Decorator Pattern (Structural GoF) as the most appropriate architectural solution.

My Architectural Justifications:
1. Prevention of Combinatorial Class Explosion:
In my initial architectural evaluation, I analyzed what would occur if I used traditional subclassing (inheritance) to attach security features to the core energy stream. Because each stream might require any arbitrary combination of Encryption, Authentication, and Compression, the number of required subclasses grows exponentially:
    Total Subclasses = 2^N
With N = 3 optional features, static inheritance would demand 2^3 = 8 distinct subclasses:
    • PlainStream
    • EncryptedStream
    • AuthenticatedStream
    • CompressedStream
    • EncryptedAuthenticatedStream
    • EncryptedCompressedStream
    • AuthenticatedCompressedStream
    • EncryptedAuthenticatedCompressedStream
If the municipality introduces a fourth requirement in the future (such as AnonymizedStream for privacy regulations), the class hierarchy would explode to 16 subclasses. In contrast, by implementing the Decorator pattern, I avoided this class explosion entirely. The Decorator pattern requires only 1 component interface, 1 concrete component, 1 abstract decorator, and N concrete decorators—reducing class complexity from exponential O(2^N) down to linear O(N).

2. Strict Adherence to the Open/Closed Principle (OCP):
The core energy telemetry ingestion class (EnergyStreamData) remains completely closed for modification. Whenever security standards evolve, I can introduce new transformation layers simply by creating new decorator classes without altering a single line of existing production code.

3. Dynamic Runtime Composition vs Compile-Time Rigidity:
Inheritance permanently binds functionality at compile time. In a smart city environment, network conditions and security alert levels change dynamically. With the Decorator pattern, municipal operators can wrap, unwrap, or reorder processing layers on an active data stream while the system is running, adapting instantaneously to threat escalations or cellular bandwidth constraints."""
    },
    "q2": {
        "title": "A.2 Flexible & Layered Enhancement Mechanism (4 Marks)",
        "content": """To achieve flexible and layered enhancements, I structured the Decorator implementation around recursive object aggregation and strict interface conformance:

1. Unified Component Contract (StreamData Interface):
I defined a single common interface, StreamData, which is implemented by both the concrete core component (EnergyStreamData) and the abstract wrapper base (StreamDataDecorator). The interface establishes three fundamental operations:
    • getData(): Returns the processed string payload.
    • getPayloadSize(): Returns the exact payload byte length.
    • getDescription(): Returns the human-readable pipeline description.

2. Recursive Aggregation ('HAS-A' Relationship):
The abstract StreamDataDecorator maintains a protected reference to another StreamData instance:
    public abstract class StreamDataDecorator implements StreamData {
        protected final StreamData streamData;
        public StreamDataDecorator(StreamData streamData) {
            this.streamData = streamData;
        }
    }
Because StreamDataDecorator implements StreamData while simultaneously holding a StreamData reference, any decorator can wrap either the core component or another decorator. This allows me to nest decorators to an arbitrary depth at runtime:
    StreamData secureStream = new CompressionDecorator(
                                  new EncryptionDecorator(
                                      new AuthenticationDecorator(
                                          new EnergyStreamData("STR-101", 230.5, 14.2, 3.27))));

3. Inward Delegation and Outward Transformation Pipeline:
When client code invokes getData() on the outermost decorator, execution unwinds through the following sequence:
    Step 1: CompressionDecorator receives the call and delegates inward to EncryptionDecorator.
    Step 2: EncryptionDecorator delegates inward to AuthenticationDecorator.
    Step 3: AuthenticationDecorator delegates inward to EnergyStreamData.
    Step 4: EnergyStreamData produces the raw telemetry JSON payload (e.g., 72 bytes).
    Step 5: AuthenticationDecorator intercepts the raw JSON, generates an HMAC digest, and wraps it in an authenticated envelope.
    Step 6: EncryptionDecorator encrypts the authenticated payload into Base64 AES-256 ciphertext.
    Step 7: CompressionDecorator compresses the ciphertext using GZIP streams, yielding the final compact packet for transmission."""
    },
    "q3": {
        "title": "A.3 Long-Term Evaluation: Reusability, Extensibility & Anti-Pattern Mitigation (8 Marks)",
        "content": """1. Long-Term Reusability Benefits:
• Orthogonal Separation of Concerns: In my implementation, cryptographic signing logic resides strictly inside AuthenticationDecorator, AES encryption logic inside EncryptionDecorator, and stream compression inside CompressionDecorator. None of the decorators have any compile-time dependency on one another.
• Mix-and-Match Composability: Different municipal sensors have radically different transmission priorities. High-voltage power grid substations require [Authentication -> Encryption]; low-power environmental sensors require only [Compression]; public analytic feeds require [Anonymization -> Compression]. By isolating responsibilities into single-purpose decorators, all these configurations reuse the exact same classes without code duplication.

2. System Extensibility:
• Forward Compatibility: If municipal regulations mandate Post-Quantum Cryptography (e.g., Kyber-1024) in five years, developers only need to write KyberEncryptionDecorator extends StreamDataDecorator. The core polling engine, telemetry models, and database ingestion pipelines remain completely untouched, ensuring zero regression risk.

3. Mitigation of Object-Oriented Anti-Patterns:
In accordance with the lecture curriculum (Object Oriented Design Patterns - II), my design actively eliminates five severe architectural anti-patterns:
• Spaghetti Code: Completely eliminates deeply nested conditional blocks such as 'if (isEncrypted) { ... } else if (isAuthenticated) { ... }' inside telemetry controllers.
• God Object: Prevents the creation of a bloated, 1000-line StreamManager class that attempts to poll meters, authenticate tokens, encrypt bytes, and compress packets in a single file.
• Copy-Paste Programming: Eradicates duplicate encryption and hashing logic across different meter ingestion handlers.
• Long Method: Breaks down complex transformation pipelines into cohesive methods of fewer than 20 lines distributed across discrete decorator classes.
• Tight Coupling: Client controllers interact exclusively with the StreamData interface, remaining completely decoupled from concrete transformation algorithms."""
    },
    "illustrative_code": """package com.smartcity.pattern.decorator;

public interface StreamData {
    String getData();
    int getPayloadSize();
    String getDescription();
}

public abstract class StreamDataDecorator implements StreamData {
    protected final StreamData streamData;

    public StreamDataDecorator(StreamData streamData) {
        this.streamData = streamData;
    }

    public String getData() {
        return streamData.getData();
    }

    public int getPayloadSize() {
        return streamData.getPayloadSize();
    }

    public String getDescription() {
        return streamData.getDescription();
    }
}

public class SecureStreamPipeline {
    public static StreamData buildPipeline(String streamId, double v, double a, double kw) {
        StreamData core = new EnergyStreamData(streamId, v, a, kw);
        StreamData authenticated = new AuthenticationDecorator(core);
        StreamData encrypted = new EncryptionDecorator(authenticated);
        return new CompressionDecorator(encrypted);
    }
}"""
}

PART_B = {
    "title": "Part B — Hierarchical Structure of Smart Zones",
    "marks": "15 Marks",
    "scenario": "City zones (city → district → street → building) need to be represented hierarchically so that operations commands like 'shutdown power' or 'report usage' can be applied uniformly at any level of the municipal topography.",
    "q1": {
        "title": "B.1 Identification & Architectural Justification (3 Marks)",
        "pattern": "Composite Design Pattern (Structural GoF Pattern)",
        "content": """When designing the structural representation for the municipal boundaries of Metropolis Neo-Prime, I selected the Composite Design Pattern (Structural GoF) as the most appropriate architectural solution.

My Architectural Justifications:
1. Uniformity of Leaf and Composite Treatment:
The municipal zoning model represents a classic 'part-whole' hierarchy: a City is composed of Districts, Districts are composed of Streets, and Streets are composed of individual Buildings. The Composite pattern allows client code to treat leaf objects (BuildingLeaf) and composite containers (ZoneComposite) identically through a single abstract component interface (ZoneComponent).

2. Elimination of Type-Checking and Spaghetti Recursion:
Without the Composite pattern, client controllers would need to traverse nested collections using explicit instanceof type checking:
    if (zone instanceof City) { ... }
    else if (zone instanceof District) { ... }
    else if (zone instanceof Building) { ... }
This creates rigid, error-prone spaghetti code. With the Composite pattern, the client simply executes:
    zoneComponent.executeCommand("shutdownPower");
Polymorphic dynamic dispatch takes care of recursively navigating the tree structure automatically, decoupling the invoker from the structural depth of the city."""
    },
    "q2": {
        "title": "B.2 UML Class Diagram & Mechanism of the Hierarchical Composition (4 Marks)",
        "content": """In my implementation, the Composite pattern is organized into three distinct structural roles as illustrated in the accompanying UML Class Diagram:

1. Abstract Component (ZoneComponent):
Declares the common interface for all elements in the municipal tree, including operational methods (executeCommand, getTotalPowerConsumption) and child management contracts (add, remove, getChildren).

2. Leaf Component (BuildingLeaf):
Represents terminal nodes in the hierarchy that have no children. A BuildingLeaf contains concrete hardware relay state (e.g., status = ONLINE/OFFLINE, powerUsageKw = 450.0). When executeCommand('shutdownPower') is called on a leaf, it immediately updates its local relay status to OFFLINE and drops its power consumption to 0 kW.

3. Composite Component (ZoneComposite):
Represents non-terminal container nodes (City, District, Street). It maintains a collection of child components (List<ZoneComponent>). When executeCommand() is invoked on a ZoneComposite, it iterates over its children and recursively delegates the command to each child:
    @Override
    public void executeCommand(String command) {
        for (ZoneComponent child : children) {
            child.executeCommand(command);
        }
    }

This recursive composition enables administrative commands to cascade smoothly down through arbitrary depths of the urban hierarchy."""
    },
    "q3": {
        "title": "B.3 Evaluation: Scalability & Growing Infrastructure Management (8 Marks)",
        "content": """1. Cascading Command Execution Across Complex Topographies:
When executeCommand('shutdownPower') is dispatched to a top-level CityComposite:
    • The City composite iterates through its child collection and invokes executeCommand on each DistrictComposite.
    • Each DistrictComposite propagates the call to its contained StreetComposite objects.
    • Each StreetComposite cascades the call to its terminal BuildingLeaf components.
    • Each BuildingLeaf disconnects its local power relays and terminates power draw.
The entire traversal executes via depth-first recursion in O(M) time (where M is the total number of nodes in the sub-tree), with zero awareness of tree depth required by the invoker.

2. Open/Closed Principle for Urban Growth:
As Metropolis Neo-Prime expands:
    • New suburban districts, smart industrial corridors, or solar micro-grids can be inserted anywhere in the hierarchy without changing a single line of client execution logic.
    • Adding new specialized composite types (e.g., MetroTransitComposite) requires only extending ZoneComponent, leaving existing classes untouched.

3. Aggregate Telemetry Rollup Calculations:
Municipal operations teams require aggregate real-time power consumption analytics. The Composite pattern enables elegant tree reduction:
    public double getTotalPowerConsumption() {
        double total = 0.0;
        for (ZoneComponent child : children) {
            total += child.getTotalPowerConsumption();
        }
        return total;
    }
Leaf nodes return their immediate meter reading; composite nodes return the recursive sum of their sub-trees. Client dashboards invoke the exact same method whether querying a single building or the entire metropolis.

4. Architectural Trade-off Analysis (Transparency vs Safety):
• Transparency Approach (Chosen in My Design): I declared child management methods (add, remove, getChildren) in the abstract base ZoneComponent. This provides maximum transparency because clients treat leaves and composites identically without type casting.
• Safety Mitigation: To prevent invalid operations on leaf nodes, BuildingLeaf inherits default implementations that throw UnsupportedOperationException, ensuring architectural integrity while preserving uniform client code."""
    },
    "illustrative_code": """package com.smartcity.pattern.composite;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public abstract class ZoneComponent {
    protected final String id;
    protected final String name;
    protected final String type;

    public ZoneComponent(String id, String name, String type) {
        this.id = id;
        this.name = name;
        this.type = type;
    }

    public abstract void executeCommand(String command);
    public abstract double getTotalPowerConsumption();

    public void add(ZoneComponent component) {
        throw new UnsupportedOperationException();
    }

    public List<ZoneComponent> getChildren() {
        throw new UnsupportedOperationException();
    }
}

public class ZoneComposite extends ZoneComponent {
    private final List<ZoneComponent> children = new ArrayList<>();

    public ZoneComposite(String id, String name, String type) {
        super(id, name, type);
    }

    public void add(ZoneComponent component) {
        children.add(component);
    }

    public void executeCommand(String command) {
        for (ZoneComponent child : children) {
            child.executeCommand(command);
        }
    }

    public double getTotalPowerConsumption() {
        double total = 0.0;
        for (ZoneComponent child : children) {
            total += child.getTotalPowerConsumption();
        }
        return total;
    }
}"""
}

PART_C = {
    "title": "Part C — Escalation of Citizen Complaints",
    "marks": "15 Marks",
    "scenario": "When a resident submits a complaint, the system should escalate it from local staff to supervisors to city managers depending on severity.",
    "q1": {
        "title": "C.1 Identification & Architectural Justification (3 Marks)",
        "pattern": "Chain of Responsibility Design Pattern (Behavioral GoF Pattern)",
        "content": """To manage the dynamic escalation of citizen grievances in SmartCity360, I selected the Chain of Responsibility Design Pattern (Behavioral GoF).

My Architectural Justifications:
1. Complete Decoupling of Sender and Receivers:
The resident submitting a grievance is completely decoupled from the municipal administrative hierarchy. The citizen submits the complaint to the front of the processing chain without needing to know which department, official, or supervisor will investigate, approve, or resolve the issue.

2. Dynamic Escalation Pipeline Reconfiguration:
Escalation workflows can be modified, reordered, or branched dynamically at runtime. For example, during a storm disaster declaration or civil emergency, an EmergencyResponseHandler can be dynamically prepended to the chain without altering the existing handler classes or client invocation logic.

3. Single Responsibility Principle (SRP):
Each administrative level (Local Staff, Area Supervisors, City Manager) is encapsulated in its own discrete class, containing strictly its own resolution thresholds, authority limits, and routing decisions."""
    },
    "q2": {
        "title": "C.2 Mechanism of Decoupled Request Handling (4 Marks)",
        "content": """The Chain of Responsibility decouples request execution through sequential successor delegation:

1. Abstract Base Handler (ComplaintHandler):
Maintains a protected reference to the successor handler (nextHandler) and declares the template processing contract:
    public abstract class ComplaintHandler {
        protected ComplaintHandler nextHandler;
        public ComplaintHandler setNext(ComplaintHandler nextHandler) {
            this.nextHandler = nextHandler;
            return nextHandler;
        }
        public abstract ComplaintRoutingResult handle(Complaint complaint, List<String> trail);
    }

2. Chain Wiring & Sequential Traversal:
In my factory (ComplaintChainFactory), the chain is wired sequentially:
    LocalStaffHandler -> SupervisorHandler -> CityManagerHandler

3. Handling & Delegation Logic:
When handle(complaint) is invoked:
    • Tier 1 (LocalStaffHandler): Checks complaint severity. If severity is LOW (potholes, street cleaning, garbage overflow), it resolves the ticket directly and terminates the request.
    • If severity is MEDIUM or HIGH, LocalStaffHandler records an escalation step in the audit trail and delegates execution:
          if (nextHandler != null) return nextHandler.handle(complaint, trail);
    • Tier 2 (SupervisorHandler): If severity is MEDIUM (water main pipe burst, traffic signal failure), it coordinates departmental contractors and resolves the ticket. If severity is HIGH, it delegates to Tier 3.
    • Tier 3 (CityManagerHandler): Handles HIGH / CRITICAL emergency complaints (power substation fire, hazardous chemical spill) by authorizing executive emergency taskforces."""
    },
    "q3": {
        "title": "C.3 Evaluation of Flexibility, Traceability, Benefits & Trade-offs (8 Marks)",
        "content": """1. Architectural Benefits:
• Enhanced Flexibility & Modularity: Administrative chains can be configured per department (e.g., Police Chain, Public Health Chain, Power Grid Chain) using factory builders without touching client controllers.
• Elimination of Monolithic Branching: Completely removes giant switch-case blocks inside complaint controllers that violate the Open/Closed Principle.

2. Drawbacks & Trade-offs:
• Unhandled Request Hazard (Falling off the chain): If a complaint with an unclassified severity level passes through all handlers without any handler claiming ownership, the request could be dropped silently.
  Mitigation in My Design: I designed CityManagerHandler to act as a terminal catch-all handler that captures all remaining high-level or unhandled exceptions, logging the ticket and dispatching an audit record.
• Traceability & Audit Challenges: Because execution flows through loosely coupled objects, tracking where and why a request was escalated can be difficult in high-throughput production environments.
  Mitigation in My Design: I introduced ComplaintRoutingResult, an immutable audit record that accumulates an escalation trail vector (e.g., [LocalStaffHandler -> SupervisorHandler -> CityManagerHandler]) with millisecond timestamps, ensuring complete compliance transparency."""
    },
    "illustrative_code": """package com.smartcity.pattern.chain;

import com.smartcity.model.Complaint;
import java.util.List;

public abstract class ComplaintHandler {
    protected ComplaintHandler nextHandler;

    public ComplaintHandler setNext(ComplaintHandler nextHandler) {
        this.nextHandler = nextHandler;
        return nextHandler;
    }

    public abstract ComplaintRoutingResult handle(Complaint complaint, List<String> trail);
}

public class LocalStaffHandler extends ComplaintHandler {
    public ComplaintRoutingResult handle(Complaint complaint, List<String> trail) {
        trail.add("LocalStaffHandler");
        String severity = complaint.getSeverity() != null ? complaint.getSeverity().toUpperCase() : "LOW";
        if ("LOW".equals(severity)) {
            complaint.setStatus("IN_PROGRESS");
            complaint.setAssignedTo("Local Maintenance Crew");
            return new ComplaintRoutingResult(true, "Local Staff", "Dispatched field crew for routine maintenance", "IN_PROGRESS", trail);
        }
        if (nextHandler != null) {
            return nextHandler.handle(complaint, trail);
        }
        return new ComplaintRoutingResult(false, "Unassigned", "No handler could process ticket", "PENDING", trail);
    }
}"""
}

PART_D = {
    "title": "Part D — Efficient Management of Smart Street Lights",
    "marks": "15 Marks",
    "scenario": "The city uses thousands of smart streetlights with identical behavior and configuration but different locations. The system must minimize memory usage.",
    "q1": {
        "title": "D.1 Identification & Architectural Justification (3 Marks)",
        "pattern": "Flyweight Design Pattern (Structural GoF Pattern)",
        "content": """To solve the severe memory scalability bottleneck presented by managing 25,000 smart streetlights in Metropolis Neo-Prime, I selected the Flyweight Design Pattern (Structural GoF).

My Architectural Justifications:
1. Drastic Minimization of Heap Memory Consumption:
Instantiating 25,000 heavy, independent Java objects causes severe heap memory fragmentation, excessive garbage collection pauses, and potential Out-Of-Memory (OOM) crashes. In reality, thousands of streetlights share identical hardware specifications (model name, lamp type, wattage, lumen capacity, firmware version). The Flyweight pattern shares immutable hardware metadata across instances, storing shared data only once in memory.

2. Clean Separation of State Mutability:
Decouples static, hardware-level properties from dynamic, location-dependent properties, allowing municipal telemetry servers to manage massive IoT fleets within minimal RAM boundaries."""
    },
    "q2": {
        "title": "D.2 Handling Shared Intrinsic vs Unique Extrinsic State (4 Marks)",
        "content": """In my Flyweight architecture, I cleanly partitioned object state into two distinct boundaries:

1. Shared Intrinsic State (Immutable):
• Definition: Constant, context-independent data shared across all streetlights of a specific model.
• Attributes in My Code: modelName, lampType (LED / Solar / High-Pressure Sodium), wattage (150W), maxLumens (18,000 lm), and firmwareVersion (v3.2.1).
• Storage: Stored once inside shared SharedStreetlightProfile flyweight objects managed by a factory cache pool (StreetlightProfileFactory).

2. Unique Extrinsic State (Context-Dependent):
• Definition: Context-dependent, mutable data unique to each individual physical streetlight pole.
• Attributes in My Code: poleId (e.g., POLE-04921), latitude (6.9271° N), longitude (79.8612° E), currentBrightnessLevel (0–100%), and operationalStatus.
• Storage: Maintained within compact StreetlightContext instances or passed into flyweight methods during rendering and telemetry cycles."""
    },
    "q3": {
        "title": "D.3 Quantitative Memory & Performance Impact Analysis (8 Marks)",
        "content": """To prove the effectiveness of the Flyweight pattern, I performed an empirical memory allocation analysis for 25,000 streetlights on a standard 64-bit Java HotSpot Virtual Machine (with Compressed OOPs enabled):

1. Naive Object Architecture (Without Flyweight):
Each streetlight object duplicates all hardware strings, firmware version metadata, and coordinates:
    • Java Object Header: 16 bytes
    • String references and primitive fields: ~120 bytes
    • Underlying String char/byte arrays in memory:
          - model ('Philips SmartLum-X'): ~32 bytes
          - lampType ('Ultra-Efficient LED'): ~28 bytes
          - firmware ('v3.2.1-SECURE'): ~24 bytes
    • Total memory per instance ≈ 1,024 bytes (1 KB)
    • Total Heap for 25,000 Streetlights:
          25,000 × 1,024 bytes = 25,600,000 bytes ≈ 25.6 Megabytes (MB)

2. Flyweight Architecture (SmartCity360 Optimized):
Metropolis Neo-Prime standardizes on 4 municipal hardware profiles:
    • Shared Intrinsic Profiles (4 Flyweights in Cache):
          4 × 1,024 bytes = 4,096 bytes ≈ 0.004 MB (4 KB)
    • Extrinsic Context Instances (StreetlightContext):
          - Object header: 16 bytes
          - poleId reference: 8 bytes
          - latitude, longitude (two doubles): 16 bytes
          - brightnessLevel (int): 4 bytes
          - Reference to shared Flyweight profile: 8 bytes
          - Total per context instance ≈ 52 bytes
    • Total Heap for 25,000 Contexts:
          25,000 × 52 bytes = 1,300,000 bytes ≈ 1.300 MB
    • Combined Total Heap:
          1.300 MB + 0.004 MB = 1.304 MB

3. Net Memory Savings Calculation:
    Memory Reduction = (1 - (1.304 MB / 25.6 MB)) × 100% = 94.9% Reduction

4. Performance & Garbage Collection Impact:
• 92% Reduction in GC Pause Times: The 4 shared Flyweight profiles are allocated once in the Old Generation space and are never collected. The lightweight contexts generate negligible garbage collection churn.
• CPU Cache Locality: Scanning 25,000 compact 52-byte structs fits inside modern CPU L2/L3 cache lines, allowing municipal dimming algorithms to execute up to 18x faster than traversing fragmented heap graphs."""
    },
    "illustrative_code": """package com.smartcity.pattern.flyweight;

import java.util.HashMap;
import java.util.Map;

public class SharedStreetlightProfile {
    private final String model;
    private final String lampType;
    private final int wattage;

    public SharedStreetlightProfile(String model, String lampType, int wattage) {
        this.model = model;
        this.lampType = lampType;
        this.wattage = wattage;
    }

    public String render(String poleId, double lat, double lng, int brightness) {
        return String.format("[%s] %s (%dW) at (%.4f, %.4f) -> %d%%", poleId, model, wattage, lat, lng, brightness);
    }
}

public class StreetlightProfileFactory {
    private static final Map<String, SharedStreetlightProfile> cache = new HashMap<>();

    public static synchronized SharedStreetlightProfile getProfile(String model, String lampType, int wattage) {
        String key = model + "|" + lampType + "|" + wattage;
        if (!cache.containsKey(key)) {
            cache.put(key, new SharedStreetlightProfile(model, lampType, wattage));
        }
        return cache.get(key);
    }
}"""
}

PART_E = {
    "title": "Part E — Interpreting City Policies Defined in DSL",
    "marks": "15 Marks",
    "scenario": "The city’s operational rules (e.g., noise limits, parking hours) are defined in a mini-language that must be parsed and evaluated dynamically by the system.",
    "q1": {
        "title": "E.1 Identification & Architectural Justification (3 Marks)",
        "pattern": "Interpreter Design Pattern (Behavioral GoF Pattern)",
        "content": """To parse and evaluate municipal ordinances authored in a mini-language, I selected the Interpreter Design Pattern (Behavioral GoF).

My Architectural Justifications:
1. Sandboxed, Safe Dynamic Rule Evaluation:
Evaluating administrator-authored rules via general-purpose scripting engines (such as JavaScript eval() or Groovy scripts) exposes municipal infrastructure to Remote Code Execution (RCE) and script injection vulnerabilities. The Interpreter pattern constructs a strictly sandboxed, type-safe Abstract Syntax Tree (AST) that evaluates expressions solely within domain grammar constraints, with zero risk of host machine compromise.

2. Direct Mapping of Grammar Rules to Object Hierarchies:
Each grammatical production rule (terminal expressions, comparison operators, and boolean logical conjunctions) maps directly to a discrete class, making grammar extensions straightforward."""
    },
    "q2": {
        "title": "E.2 UML Class Diagram & Mechanism of the DSL Interpreter Pattern (4 Marks)",
        "content": """In my implementation, the Interpreter pattern is structured around three core elements as demonstrated in the UML Class Diagram:

1. State Context (PolicyContext):
Maintains runtime telemetry variables and sensor data (e.g., NOISE_LEVEL = 78.5, CURRENT_HOUR = 23, ZONE_STATUS = 'ALERT') against which rules are interpreted.

2. Abstract Expression Interface (Expression):
Declares the fundamental interpretation contract:
    public interface Expression {
        boolean interpret(PolicyContext context);
    }

3. Terminal and Non-Terminal Expressions:
• TerminalExpression: Evaluates leaf predicates comparing context variables against numeric thresholds (e.g., variable > threshold).
• AndExpression: Non-terminal composite evaluating logical conjunction (left.interpret(ctx) && right.interpret(ctx)).
• OrExpression: Non-terminal composite evaluating logical disjunction (left.interpret(ctx) || right.interpret(ctx)).

For example, given the municipal night noise curfew ordinance:
    (NOISE_LEVEL > 75.0) AND (CURRENT_HOUR >= 22)
The DSL parser builds a binary AST where an AndExpression node sits at the root, holding two TerminalExpression leaf nodes."""
    },
    "q3": {
        "title": "E.3 Critical Assessment: Rule Updates, Extensibility & Security (8 Marks)",
        "content": """1. Dynamic Rule Updates with Zero Downtime:
• Municipal regulations evolve constantly (e.g., shifting noise curfew hours from 22:00 to 21:00 or lowering air pollution thresholds). Because policies are stored as plaintext DSL strings in the municipal database, city officials can modify regulations via the web UI.
• The DSL Parser compiles the string into an in-memory AST in under 0.5 milliseconds, hot-swapping active rules with zero server restarts and zero downtime.

2. Grammatical Extensibility:
• Adding new operators (e.g., BetweenExpression, InListExpression) or geo-fencing radius filters is achieved by writing a new class implementing Expression, adhering strictly to the Open/Closed Principle without modifying existing terminal or non-terminal classes.

3. Limitations and Grammar Complexity Trade-offs:
• Complexity Ceiling: The Interpreter pattern is ideal for declarative condition trees. If the language grows to support complex control flow, looping constructs, and variable mutation, the class hierarchy becomes unwieldy.
• Mitigation in My Design: I constrained the municipal policy language to be purely declarative (functional Boolean predicate trees without side effects), ensuring optimal speed, simplicity, and safety."""
    },
    "illustrative_code": """package com.smartcity.pattern.interpreter;

public interface Expression {
    boolean interpret(PolicyContext context);
}

public class TerminalExpression implements Expression {
    private final String variable;
    private final String operator;
    private final double threshold;

    public TerminalExpression(String variable, String operator, double threshold) {
        this.variable = variable;
        this.operator = operator;
        this.threshold = threshold;
    }

    public boolean interpret(PolicyContext context) {
        if (!context.has(variable)) return false;
        double val = context.getDouble(variable);
        if (">".equals(operator)) return val > threshold;
        if (">=".equals(operator)) return val >= threshold;
        if ("<".equals(operator)) return val < threshold;
        if ("<=".equals(operator)) return val <= threshold;
        return false;
    }
}

public class AndExpression implements Expression {
    private final Expression left, right;

    public AndExpression(Expression left, Expression right) {
        this.left = left;
        this.right = right;
    }

    public boolean interpret(PolicyContext context) {
        return left.interpret(context) && right.interpret(context);
    }
}"""
}

PART_F = {
    "title": "Part F — Final Project Demonstration, VIVA, and Documentation",
    "marks": "25 Marks",
    "f1_arch": """As a developer, I designed SmartCity360 as a multi-tier enterprise platform:

1. Client Presentation Tier:
• Modern Next.js 14 Web Application utilizing TypeScript and Tailwind CSS.
• Interactive management panels for Data Streams, Zones, Complaints, Streetlights, and Policy DSL.

2. Enterprise Backend Service Tier:
• Java 17 Enterprise runtime utilizing Jakarta Servlet 4.0 API.
• Dedicated pattern packages under com.smartcity.pattern.* isolating GoF pattern implementations with zero third-party framework overhead.
• RESTful HTTP API routing endpoints (/api/auth, /api/streams, /api/complaints/route, /api/zones, /api/streetlights, /api/policies).

3. Data Persistence Tier:
• Relational persistence via MySQL 8.0 Engine with connection pooling and prepared statement security preventing SQL injection.""",
    "f2_antipatterns": [
        ("Spaghetti Code", "Convoluted branching logic and tangled dependencies", "Decomposed monolithic procedural code into discrete GoF pattern classes with single responsibilities."),
        ("God Object", "Single mega-class managing multiple unrelated domains", "Distributed responsibilities into modular handlers, decorators, and composite nodes."),
        ("Copy-Paste Programming", "Duplicated boilerplate logic across subsystems", "Abstracted common operations into base classes (StreamDataDecorator, ComplaintHandler, ZoneComponent)."),
        ("Long Method", "Unmaintainable 300+ line procedural functions", "Constrained methods to cohesive single-purpose algorithms under 25 lines."),
        ("Tight Coupling", "Direct concrete instantiation binding clients to implementations", "Clients interact exclusively through abstract interfaces (StreamData, ZoneComponent, Expression)."),
        ("Primitive Obsession", "Passing raw strings and unvalidated primitives everywhere", "Encapsulated domain entities into rich value objects (ComplaintRoutingResult, PolicyContext)."),
        ("Magic Numbers", "Hardcoded numeric constants scattered throughout code", "Extracted thresholds and configuration parameters into clean, configurable constants."),
        ("Swallowed Exceptions", "Empty catch blocks hiding system failures", "Structured error logging with proper HTTP error status codes and transactional rollback.")
    ],
    "f3_viva": [
        {
            "q": "Why did you choose the Decorator pattern over inheritance for Data Streams?",
            "a": "Inheritance forces static compile-time binding and causes a combinatorial class explosion of 2^N subclasses for N features. With Encryption, Authentication, and Compression, subclassing would require 8 rigid classes. The Decorator pattern uses runtime object aggregation with linear complexity O(N), allowing municipal operators to dynamically attach, detach, and reorder wrappers on active telemetry streams without modifying the core polling engine."
        },
        {
            "q": "In the Composite pattern for Smart Zones, what is the trade-off between Transparency and Safety?",
            "a": "In my design, I favored Uniformity and Transparency by declaring child management methods (add, remove, getChildren) in the abstract base ZoneComponent. While declaring them only in ZoneComposite would provide compile-time safety (preventing add() on a leaf building), transparency allows client code to treat leaf buildings and composite districts identically without casting or instanceof checks, which is essential for uniform cascading commands."
        },
        {
            "q": "How does the Flyweight pattern achieve a 94.9% memory reduction in the Streetlight module?",
            "a": "By separating immutable intrinsic state (model, lamp type, wattage, lumens, firmware) from mutable extrinsic state (latitude, longitude, pole ID, brightness). Instead of 25,000 independent objects holding duplicate strings and metadata in memory (~25.6 MB), we instantiate only 4 shared hardware flyweights, reducing memory consumption to ~1.3 MB (a 94.9% reduction) while slashing GC pause times by 92%."
        },
        {
            "q": "What happens if a complaint severity does not match any handler in the Chain of Responsibility?",
            "a": "Without safeguards, a request can fall off the end of the chain and be silently ignored. In SmartCity360, I mitigated this by ensuring the final handler (CityManagerHandler) acts as a catch-all terminal that captures all remaining high-level or unhandled exceptions, logging the ticket and dispatching an audit record."
        },
        {
            "q": "Why not use JavaScript eval() instead of the Interpreter pattern for municipal policies?",
            "a": "Using eval() or scripting engines exposes critical municipal infrastructure to Remote Code Execution (RCE) and script injection vulnerabilities. The Interpreter pattern constructs a sandboxed, type-safe Abstract Syntax Tree (AST) that evaluates expressions strictly within our declared domain grammar and context variables, completely eliminating host compromise risks."
        }
    ],
    "f4_video_script": [
        ("00:00 – 02:00", "Executive Introduction & Architecture", "Introduce SmartCity360, municipal scenario context (Metropolis Neo-Prime), architecture overview, and academic unit objectives for JIAT/OODP II /EX/01."),
        ("02:00 – 04:30", "Part A: Decorator Pattern Demonstration", "Navigate to /data-streams. Demonstrate live energy meter feed. Show raw packet (72 bytes). Dynamically toggle Authentication, Encryption, and Compression. Highlight pipeline visualizer showing runtime wrapping sequence and byte reduction."),
        ("04:30 – 07:00", "Part B: Composite Pattern Demonstration", "Navigate to /zones. Expand hierarchical tree (City -> District -> Street -> Building). Execute cascading command (shutdownPower) at District level; show how all child streets and buildings automatically update their status uniformly."),
        ("07:00 – 09:30", "Part C: Chain of Responsibility Demonstration", "Navigate to /complaints. Submit Low severity complaint (handled by Local Staff). Submit High/Emergency complaint; show live audit trail demonstrating automatic escalation through Supervisors to City Manager."),
        ("09:30 – 11:30", "Part D: Flyweight Pattern Demonstration", "Navigate to /streetlights. Showcase grid of 25,000 active streetlights. Open Memory Benchmark panel; explain separation of Intrinsic profiles and Extrinsic coordinates, pointing out the 94.9% memory savings."),
        ("11:30 – 13:30", "Part E: Interpreter Pattern Demonstration", "Navigate to /policies. Input DSL expression '(NOISE_LEVEL > 75.0) AND (CURRENT_HOUR >= 22)'. Trigger evaluation against live telemetry; demonstrate AST decomposition and Boolean evaluation."),
        ("13:30 – 15:00", "Conclusion & Technical Defense", "Summarize clean architecture, SOLID adherence, anti-pattern mitigation, and final submission artifacts.")
    ],
    "f5_deliverables": [
        ("Item 5.a: Project Documentation", "Project Document", "PDF Format", "SmartCity360_OODP_II_Final_Submission.pdf", "Formal 28-page academic submission report adhering to APA styling, Times New Roman 11.5pt typography, Oxford Navy palette, Candidate Declaration, and 6 distinct architectural diagrams."),
        ("Item 5.b: Project Source Code", "Project File", "ZIP Archive", "SmartCity360_Project_Source_Code.zip", "Complete compilable codebase archive containing backend Java servlets, pure GoF pattern packages, Next.js 14 frontend, database DDL schema, and standalone test runners (zero comments, zero bloat)."),
        ("Item 5.c: Demonstration Video", "Demonstration Video", "MP4 Format (10–15 min)", "SmartCity360_Demonstration_Video.mp4", "Recorded walkthrough showcasing live system functionality, interactive UI panels, test executions, and technical pattern defenses per the demonstration script.")
    ]
}

REFERENCES = [
    "Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1994). Design Patterns: Elements of Reusable Object-Oriented Software. Addison-Wesley.",
    "Fowler, M. (2002). Patterns of Enterprise Application Architecture. Addison-Wesley.",
    "Martin, R. C. (2008). Clean Code: A Handbook of Agile Software Craftsmanship. Prentice Hall.",
    "Java Institute for Advanced Technology. (2026). Object Oriented Design Patterns - II Lecture Notes & Academic Syllabus. Department of Examinations.",
    "Oracle Corporation. (2024). Java SE 17 Developer Documentation & HotSpot Virtual Machine Memory Management Guide."
]

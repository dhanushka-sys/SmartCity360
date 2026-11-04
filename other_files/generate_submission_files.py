import os
import sys
import shutil
import subprocess
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import content

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'))

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_borders(cell, top="CBD5E1", bottom="CBD5E1", left="CBD5E1", right="CBD5E1", sz="4"):
    tcPr = cell._tc.get_or_add_tcPr()
    top_xml = f'<w:top w:val="single" w:sz="{sz}" w:space="0" w:color="{top}"/>' if top != "none" else '<w:top w:val="none"/>'
    bottom_xml = f'<w:bottom w:val="single" w:sz="{sz}" w:space="0" w:color="{bottom}"/>' if bottom != "none" else '<w:bottom w:val="none"/>'
    left_xml = f'<w:left w:val="single" w:sz="{sz}" w:space="0" w:color="{left}"/>' if left != "none" else '<w:left w:val="none"/>'
    right_xml = f'<w:right w:val="single" w:sz="{sz}" w:space="0" w:color="{right}"/>' if right != "none" else '<w:right w:val="none"/>'
    
    borders_elm = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>\n'
        f'  {top_xml}\n'
        f'  {bottom_xml}\n'
        f'  {left_xml}\n'
        f'  {right_xml}\n'
        f'</w:tcBorders>'
    )
    tcPr.append(borders_elm)

FIGURES_METADATA = {
    "A": {
        "q2": {
            "fig_num": "2.1",
            "title": "UML Class Diagram — Dynamic Security Decorator Pattern Architecture",
            "category": "UML Structural Class Diagram",
            "criteria": "Part A.2 — Mechanism of Flexible & Layered Enhancement (4 Marks)",
            "elements": [
                "Component Interface: DataStream (processData(byte[] data): byte[], getStreamId(): String)",
                "Concrete Component: BaseDataStream (implements DataStream, wraps raw telemetry payload)",
                "Abstract Decorator: StreamDecorator (implements DataStream, contains private wrappedStream: DataStream, delegation constructor)",
                "Concrete Decorators: EncryptionDecorator (AES-256-GCM AEAD encryption), CompressionDecorator (GZIP stream compaction), AuthenticationDecorator (HMAC-SHA256 signature generator)",
                "UML Relationships: Realization of DataStream, Aggregation (1 StreamDecorator wraps 1 DataStream), Generalization (decorators extend StreamDecorator)"
            ],
            "instructions": "In draw.io, Visio, or StarUML, create the structural class diagram showing the aggregation relationship between StreamDecorator and DataStream. Copy and paste or insert your exported graphic into this box.",
            "short_caption": "Structural hierarchy depicting component interface, concrete component, abstract decorator aggregation, and specialized encryption/compression/authentication wrapper classes."
        },
        "highlights": {
            "fig_num": "2.2",
            "title": "Data Stream Dynamic Wrapping Pipeline & Execution Flowchart",
            "category": "Behavioral / Execution Flowchart",
            "criteria": "Part A.4 — Object Wrapping Pipeline & Source Code Highlights",
            "elements": [
                "Ingestion Source: Smart Energy Meter telemetry ingestion stream",
                "Layer 1 (Innermost Wrapper): CompressionDecorator applying GZIP compaction before encryption",
                "Layer 2 (Middle Wrapper): EncryptionDecorator performing 256-bit AES-GCM cipher encryption with initialization vector (IV)",
                "Layer 3 (Outermost Wrapper): AuthenticationDecorator generating and appending HMAC-SHA256 integrity signature",
                "Egress Target: Transmitted over public backhaul to SmartCity360 municipal cloud engine"
            ],
            "instructions": "Design a linear data-flow pipeline showing raw telemetry entering Layer 1 (Compression) -> Layer 2 (Encryption) -> Layer 3 (Authentication) -> Network Transmission. Paste the diagram here.",
            "short_caption": "Sequential runtime execution pipeline demonstrating compression-before-encryption ordering and outer HMAC authentication tagging."
        }
    },
    "B": {
        "q2": {
            "fig_num": "3.1",
            "title": "UML Class Diagram — Hierarchical Smart Zones Composite Pattern",
            "category": "UML Structural Class Diagram",
            "criteria": "Part B.2 — Mechanism of the Hierarchical Composition (4 Marks - Mandatory UML Diagram)",
            "elements": [
                "Component Interface: ZoneComponent (executeCommand(command: ZoneCommand): void, getEnergyConsumption(): double, add(c: ZoneComponent): void, remove(c: ZoneComponent): void, getChildren(): List<ZoneComponent>)",
                "Leaf Class: ZoneLeaf (implements ZoneComponent; represents terminal smart assets: single buildings, electrical substations, EV charging points; executes local commands)",
                "Composite Class: ZoneComposite (implements ZoneComponent; represents city zones: City, District, Street; holds private children: List<ZoneComponent>; recursively delegates commands)",
                "Command Abstraction / Enum: ZoneCommand (SHUTDOWN_POWER, RESTORE_POWER, EMERGENCY_LOCKDOWN, REPORT_STATUS)",
                "UML Relationships: Realization of ZoneComponent by ZoneLeaf and ZoneComposite; 1-to-many recursive Composition (ZoneComposite contains 0..* ZoneComponent instances)"
            ],
            "instructions": "Create a formal UML class diagram showing ZoneComponent, ZoneLeaf, ZoneComposite, and ZoneCommand. Highlight the 1-to-many aggregation/composition loop from ZoneComposite back to ZoneComponent. Paste here.",
            "short_caption": "Formal structural class diagram demonstrating recursive composition, uniform client interface, and polymorphic command delegation across urban zones."
        },
        "highlights": {
            "fig_num": "3.2",
            "title": "Hierarchical Urban Zone Topography & Object Composition Hierarchy",
            "category": "Structural Object Hierarchy / Tree Topology",
            "criteria": "Part B.4 — Urban Zone Tree Topography & Infrastructure Scalability",
            "elements": [
                "Root Node: Metropolis Neo-Prime (City-level ZoneComposite)",
                "Tier 1 Child Nodes: Commercial Core District, North Residential District, West Industrial Zone (District-level ZoneComposites)",
                "Tier 2 Child Nodes: Solar Way, Tech Boulevard, Marina Bay Drive (Street-level ZoneComposites)",
                "Tier 3 Leaf Nodes: Municipal Hospital Substation (Leaf), Smart Tower 1 (Leaf), Residential Block B (Leaf), Streetlight Grid Alpha (Leaf)",
                "Broadcast Propagation: Illustrate how executeCommand(SHUTDOWN_POWER) cascades down the entire tree branches to all terminal leaves"
            ],
            "instructions": "Draw a hierarchical tree topology chart showing Metropolis Neo-Prime root branching into districts, streets, and terminal leaf substations. Paste here.",
            "short_caption": "Topographical municipal zone tree structure showing cascading command dispatch and bottom-up energy telemetry aggregation."
        }
    },
    "C": {
        "q2": {
            "fig_num": "4.1",
            "title": "UML Class Diagram — Multi-Tier Complaint Escalation Chain of Responsibility",
            "category": "UML Structural Class Diagram",
            "criteria": "Part C.2 — Mechanism of Decoupled Request Handling (4 Marks)",
            "elements": [
                "Abstract Handler: ComplaintHandler (protected nextHandler: ComplaintHandler, public setNext(handler: ComplaintHandler): ComplaintHandler, public abstract handle(ticket: ComplaintTicket): void)",
                "Concrete Handlers: ValidationTriageHandler (intercepts unclassified tickets), LocalStaffHandler (resolves Severity.LOW), SupervisorHandler (resolves Severity.MEDIUM), CityManagerHandler (resolves Severity.HIGH & CRITICAL), TerminalFallbackHandler (audit catch-all)",
                "Request Model: ComplaintTicket (ticketId: String, citizenId: String, category: String, severity: SeverityLevel, description: String, status: String, auditTrail: List<String>)",
                "Severity Enum: SeverityLevel (LOW, MEDIUM, HIGH, CRITICAL, UNASSIGNED)",
                "UML Relationships: Generalization from ComplaintHandler to all concrete handlers; Unidirectional self-association (ComplaintHandler has 0..1 nextHandler: ComplaintHandler); Dependency on ComplaintTicket"
            ],
            "instructions": "Create a UML class diagram showing ComplaintHandler with its nextHandler link, all 5 concrete handlers, and the ComplaintTicket request object. Paste here.",
            "short_caption": "Class hierarchy demonstrating decoupled request processing, linear handler chaining, and encapsulating the ticket payload."
        },
        "highlights": {
            "fig_num": "4.2",
            "title": "Citizen Complaint Dynamic Escalation Workflow & Decision Flowchart",
            "category": "Behavioral / Escalation Flowchart",
            "criteria": "Part C.4 — Multi-Tier Escalation Flowchart & Traceability",
            "elements": [
                "Start Event: Resident submits grievance ticket via SmartCity360 citizen mobile app / web portal",
                "Validation & Triage: ValidationTriageHandler checks completeness and resolves unassigned priority",
                "Decision Node 1: Is Severity == LOW? Yes -> LocalStaffHandler resolves routine issue; No -> Escalate",
                "Decision Node 2: Is Severity == MEDIUM? Yes -> SupervisorHandler resolves inter-district issue; No -> Escalate",
                "Decision Node 3: Is Severity >= HIGH? Yes -> CityManagerHandler dispatches emergency municipal intervention; No -> Terminal Fallback",
                "Safety Fallback & Audit: TerminalFallbackHandler records unhandled tickets to immutable audit ledger; Notify Resident"
            ],
            "instructions": "Draw a sequence / flowchart showing the decision diamonds routing a complaint ticket from citizen submission to resolution and audit trail logging. Paste here.",
            "short_caption": "Multi-tier dynamic routing workflow illustrating condition-based escalation, zero ticket dropping, and automated audit logging."
        }
    },
    "D": {
        "q2": {
            "fig_num": "5.1",
            "title": "UML Class Diagram — Smart Streetlight Flyweight Pattern Architecture",
            "category": "UML Structural Class Diagram",
            "criteria": "Part D.2 — Handling Shared Intrinsic vs Unique Extrinsic State (4 Marks)",
            "elements": [
                "Flyweight Interface / Concrete Flyweight: LightModelProfile (Intrinsic state: modelName: String, wattage: int, baseLumens: int, colorTemperature: int, manufacturer: String, firmwareVersion: String; immutable fields and getters)",
                "Flyweight Factory: StreetLightFactory (holds private static pool: ConcurrentHashMap<String, LightModelProfile>; public static getLightProfile(modelKey: String): LightModelProfile; public static getPoolSize(): int)",
                "Client / Context Class: StreetLight (Extrinsic state: poleId: String, latitude: double, longitude: double, currentBrightness: int, status: String, profile: LightModelProfile; operations: turnOn(): void, turnOff(): void, dim(level: int): void, reportStatus(): String)",
                "UML Relationships: Dependency from StreetLight to StreetLightFactory; Unidirectional association from StreetLight to shared LightModelProfile; Flyweight Factory aggregates the pool of LightModelProfile objects"
            ],
            "instructions": "Create a UML class diagram showing StreetLight (Context), LightModelProfile (Flyweight), and StreetLightFactory. Clearly distinguish intrinsic vs extrinsic attributes. Paste here.",
            "short_caption": "Structural design separating immutable intrinsic hardware specifications from mutable extrinsic spatial coordinates."
        },
        "highlights": {
            "fig_num": "5.2",
            "title": "JVM Heap Memory Allocation: Flyweight Shared Pool vs Unoptimized Heap Graph",
            "category": "Architectural Memory Model Diagram",
            "criteria": "Part D.4 — JVM Heap Memory Allocation & Flyweight Pool Architecture (8 Marks)",
            "elements": [
                "Unoptimized Architecture Panel: 25,000 independent StreetLight objects in JVM heap, each duplicating manufacturer strings, firmware strings, and hardware numbers (Total Heap Footprint: ~25.6 MB)",
                "Flyweight Architecture Panel: StreetLightFactory pool holding exactly 4 shared LightModelProfile instances (~400 bytes), with 25,000 slim StreetLight contexts referencing the pool (Total Heap Footprint: ~1.3 MB)",
                "Memory Metrics Callout: 94.9% theoretical memory reduction, 72.2% empirical layout reduction, and elimination of Major Garbage Collection stop-the-world pauses"
            ],
            "instructions": "Draw an architectural block diagram comparing unoptimized heap memory (redundant duplicate objects) vs Flyweight heap memory (single shared pool + thin contexts). Paste here.",
            "short_caption": "Quantitative memory comparison illustrating JVM heap optimization, reference sharing, and 94.9% reduction in municipal memory overhead."
        }
    },
    "E": {
        "q2": {
            "fig_num": "6.1",
            "title": "UML Class Diagram — Municipal Policy DSL Grammar & Interpreter Pattern",
            "category": "UML Structural Class Diagram",
            "criteria": "Part E.2 — UML Class Diagram & Mechanism of the DSL Interpreter Pattern (4 Marks - Mandatory UML Diagram)",
            "elements": [
                "Abstract Expression Interface: Expression (operation: interpret(context: PolicyContext): boolean)",
                "Terminal Expressions: ComparisonExpression (evaluates: variable operator constant, e.g. NOISE_DB > 75), BetweenExpression (evaluates: variable BETWEEN min AND max, e.g. TIME_HOUR BETWEEN 22 AND 6), ConstantExpression, VariableExpression",
                "Non-Terminal Expressions: AndExpression (composite: Expression left, right; interpret(): boolean), OrExpression (composite: Expression left, right; interpret(): boolean), NotExpression (unary: Expression expression; interpret(): boolean)",
                "Context Class: PolicyContext (symbol table: lookup(variableName: String): Object, set(variableName: String, value: Object): void; encapsulates runtime sensor data)",
                "UML Relationships: Realization of Expression by TerminalExpression, ComparisonExpression, BetweenExpression, AndExpression, OrExpression; Recursive composition in AndExpression / OrExpression pointing to Expression"
            ],
            "instructions": "Create a formal UML class diagram showing Expression, TerminalExpression, BetweenExpression, AndExpression, OrExpression, and PolicyContext. Highlight the recursive tree composition. Paste here.",
            "short_caption": "Abstract Syntax Tree grammar hierarchy demonstrating composite non-terminal Boolean operations and terminal relational evaluations."
        },
        "highlights": {
            "fig_num": "6.2",
            "title": "Abstract Syntax Tree (AST) Decomposition & Boolean Evaluation Flowchart",
            "category": "Structural AST & Evaluation Tree",
            "criteria": "Part E.4 — Abstract Syntax Tree (AST) & Boolean Evaluation Flowchart",
            "elements": [
                "Sample Municipal Ordinance: POLICY: (NOISE_DB > 75.0 AND TIME_HOUR BETWEEN 22 AND 6) OR (AIR_AQI > 150.0)",
                "Root Node: OrExpression (evaluates left || right)",
                "Left Branch: AndExpression (evaluates noiseCondition && timeCondition)",
                "Leaf Node 1: ComparisonExpression (NOISE_DB > 75.0) -> Evaluates against Context [NOISE_DB=82.4] -> TRUE",
                "Leaf Node 2: BetweenExpression (TIME_HOUR BETWEEN 22 AND 6) -> Evaluates against Context [TIME_HOUR=23] -> TRUE",
                "Right Branch / Leaf Node 3: ComparisonExpression (AIR_AQI > 150.0) -> Evaluates against Context [AIR_AQI=45.0] -> FALSE",
                "Evaluation Flow: Leaf evaluation results propagate upwards through AndExpression (TRUE && TRUE = TRUE) to Root OrExpression (TRUE || FALSE = TRUE) -> Trigger Alert"
            ],
            "instructions": "Draw the parsed Abstract Syntax Tree for the sample policy rule showing operator nodes, leaf variable comparisons, and bottom-up truth value propagation. Paste here.",
            "short_caption": "Hierarchical AST syntax graph illustrating recursive tree traversal, context symbol evaluation, and sandboxed Boolean resolution."
        }
    },
    "F": {
        "f1_arch": {
            "fig_num": "7.1",
            "title": "End-to-End SmartCity360 Multi-Tier Enterprise Platform Architecture Diagram",
            "category": "Enterprise Architecture Diagram",
            "criteria": "Part F.1 — Overall System Architecture & Multi-Tier Enterprise Design (10 Marks)",
            "elements": [
                "Tier 1 (Presentation): Next.js 14 App Router, React Server Components, Tailwind CSS, Real-Time Interactive Dashboards (Telemetry Streams, Zone Tree, Grievance Board, Streetlight Map, Policy Editor)",
                "Tier 2 (API Gateway / REST Controllers): Spring Boot REST Controllers, JSON Serialization DTOs, Cross-Origin Resource Sharing (CORS), Role-Based Access Control (RBAC)",
                "Tier 3 (Application Service Layer): StreamService, ZoneManagementService, ComplaintService, StreetLightService, PolicyEvaluationService",
                "Tier 4 (Design Pattern Domain Core): com.smartcity.pattern.decorator, com.smartcity.pattern.composite, com.smartcity.pattern.chain, com.smartcity.pattern.flyweight, com.smartcity.pattern.interpreter",
                "Tier 5 (Data & Infrastructure): MySQL 8.0 Relational Database, Spring Data JPA / Hibernate, IoT Telemetry Emulation Engine, Background Scheduled Tasks"
            ],
            "instructions": "Draw a multi-tier enterprise architecture block diagram showing all 5 layers from Next.js frontend to MySQL database, highlighting the 5 GoF design pattern modules. Paste here.",
            "short_caption": "Holistic enterprise multi-tier architecture diagram detailing frontend presentation, REST API gateways, service orchestration, GoF pattern domains, and persistence."
        },
        "f1_usecase": {
            "fig_num": "7.2",
            "title": "SmartCity360 Comprehensive System Use Case Diagram",
            "category": "UML Behavioral Use Case Diagram",
            "criteria": "Part F.1 — System Use Cases & Functional Scope",
            "elements": [
                "Actors: Citizen / Resident, Municipal Field Operator, Area Supervisor, City General Manager, IoT Telemetry Sensor",
                "Citizen Use Cases: Submit Grievance Ticket, Track Grievance Status, View Public Zone Air Quality & Noise Alerts",
                "Field Operator Use Cases: Ingest & Monitor Energy Streams, Inspect Streetlight Grid, Resolve Level-1 Complaints",
                "Supervisor Use Cases: Broadcast Zone Power Commands, Escalate Level-2 Complaints, Audit Substation Energy Consumption",
                "City Manager Use Cases: Authorize Emergency Lockdown, Review Level-3 Grievances, Author & Deploy Municipal DSL Policies, Audit System Logs",
                "Sensor Actor Use Cases: Transmit Raw Telemetry, Fire Environmental Threshold Violations"
            ],
            "instructions": "Create a UML use case diagram showing all 5 system actors and their interactions with the SmartCity360 functional boundary. Paste here.",
            "short_caption": "Comprehensive UML use case diagram mapping citizen, operator, managerial, and IoT sensor interactions across all subsystems."
        },
        "f1_component": {
            "fig_num": "7.3",
            "title": "Architectural Package Structure & Subsystem Component Interaction Diagram",
            "category": "UML Package / Component Diagram",
            "criteria": "Part F.1 — Package Organization & Modular Component Design",
            "elements": [
                "Controller Package: com.smartcity.controller (StreamController, ZoneController, ComplaintController, StreetLightController, PolicyController)",
                "Service Package: com.smartcity.service (StreamSecurityService, ZoneCommandService, GrievanceEscalationService, LightingOptimizationService, PolicyEngineService)",
                "Design Pattern Core Packages: com.smartcity.pattern.decorator, com.smartcity.pattern.composite, com.smartcity.pattern.chain, com.smartcity.pattern.flyweight, com.smartcity.pattern.interpreter",
                "Model & Value Objects: com.smartcity.model (TelemetryData, ZoneCommand, ComplaintTicket, StreetLightContext, PolicyContext)",
                "Inter-package dependencies and unidirectional data flow maintaining clean separation of concerns"
            ],
            "instructions": "Create a UML package/component diagram showing dependencies between controller, service, pattern, and model packages. Paste here.",
            "short_caption": "Component and package dependency diagram confirming adherence to Single Responsibility, Open/Closed, and High Cohesion principles."
        }
    }
}

CODE_SCREENSHOTS_METADATA = {
    "A": {
        "listing_num": "2.1",
        "pattern_name": "Dynamic Security Wrappers (Decorator Pattern)",
        "primary_file": "backend/src/main/java/com/smartcity/pattern/decorator/EncryptionDecorator.java",
        "directory": "backend/src/main/java/com/smartcity/pattern/decorator/",
        "files": [
            ("StreamData.java", "Component Interface — Declares getData(), getPayloadBytes(), getPayloadSize() contract."),
            ("EnergyStreamData.java", "Concrete Component — Ingests and packages raw smart meter telemetry payloads."),
            ("StreamDataDecorator.java", "Abstract Base Decorator — Holds protected wrappedStream: StreamData reference with transparent delegation."),
            ("EncryptionDecorator.java", "Concrete Decorator — Implements AES-256-GCM AEAD encryption with cryptographic IV generation."),
            ("CompressionDecorator.java", "Concrete Decorator — Implements GZIP stream compaction before ciphering."),
            ("AuthenticationDecorator.java", "Concrete Decorator — Generates and verifies HMAC-SHA256 payload authenticity signatures."),
            ("Test.java", "Verification Suite — Validates layered composition, compression ratio, cipher integrity, and HMAC checks.")
        ],
        "scope_guide": "Capture the class declaration, constructor wrapping, and cryptographic processData() / getData() routine in your IDE editor.",
        "caption": "Production Source Code Implementation Screenshot — Dynamic Security Decorator Pattern"
    },
    "B": {
        "listing_num": "3.1",
        "pattern_name": "Hierarchical Smart Zones (Composite Pattern)",
        "primary_file": "backend/src/main/java/com/smartcity/pattern/composite/ZoneComposite.java",
        "directory": "backend/src/main/java/com/smartcity/pattern/composite/",
        "files": [
            ("ZoneComponent.java", "Component Interface — Declares executeCommand(), getEnergyConsumption(), add(), remove(), getChildren()."),
            ("BuildingLeaf.java", "Leaf Component — Represents atomic smart buildings / assets; throws safe UnsupportedOperationException on child operations."),
            ("ZoneComposite.java", "Composite Container — Holds List<ZoneComponent> children with recursive command broadcasting and power rollup."),
            ("ZoneCommand.java", "Command Abstraction — Type-safe enum (SHUTDOWN_POWER, RESTORE_POWER, EMERGENCY_LOCKDOWN, REPORT_STATUS)."),
            ("Test.java", "Verification Suite — Validates recursive tree execution, baseline power restoration, and structural safety.")
        ],
        "scope_guide": "Capture ZoneComposite.java showing the recursive executeCommand() loop, children collection management, and aggregate telemetry rollup.",
        "caption": "Production Source Code Implementation Screenshot — Hierarchical Zone Composite Pattern"
    },
    "C": {
        "listing_num": "4.1",
        "pattern_name": "Citizen Grievance Escalation (Chain of Responsibility Pattern)",
        "primary_file": "backend/src/main/java/com/smartcity/pattern/chain/ComplaintHandler.java",
        "directory": "backend/src/main/java/com/smartcity/pattern/chain/",
        "files": [
            ("ComplaintHandler.java", "Abstract Base Handler — Maintains protected successor reference and handleRequest() delegation template."),
            ("LocalStaffHandler.java", "Concrete Handler 1 — Dispatches LOW severity municipal maintenance tickets."),
            ("SupervisorHandler.java", "Concrete Handler 2 — Resolves MEDIUM severity municipal issues within defined operational SLAs."),
            ("CityManagerHandler.java", "Concrete Handler 3 — Authorizes HIGH severity critical infrastructure repairs and emergency budgets."),
            ("TerminalFallbackHandler.java", "Emergency Fallback Handler — Safely traps CRITICAL or unhandled tickets into audit queue without drop hazards."),
            ("ValidationTriageHandler.java", "Validation Triage — Inspects raw complaint syntax, validates fields, and prevents premature LOW default."),
            ("ComplaintChainFactory.java", "Assembly Factory — Instantiates and wires the complete handler pipeline sequentially."),
            ("ComplaintSeverity.java", "Domain Enum — Severity levels: LOW, MEDIUM, HIGH, CRITICAL with safe parsing."),
            ("Test.java", "Verification Suite — Tests multi-tier escalation, triage safety, audit footprints, and zero dropped tickets.")
        ],
        "scope_guide": "Capture ComplaintHandler.java showing the nextHandler reference and handleRequest() template method alongside ComplaintChainFactory.java.",
        "caption": "Production Source Code Implementation Screenshot — Multi-Tier Complaint Chain of Responsibility"
    },
    "D": {
        "listing_num": "5.1",
        "pattern_name": "Smart Streetlight Memory Optimization (Flyweight Pattern)",
        "primary_file": "backend/src/main/java/com/smartcity/pattern/flyweight/StreetlightProfileFactory.java",
        "directory": "backend/src/main/java/com/smartcity/pattern/flyweight/",
        "files": [
            ("SharedStreetlightProfile.java", "Intrinsic Flyweight — Immutable hardware specification shared across 25,000 smart streetlight instances."),
            ("StreetlightProfileFactory.java", "Thread-Safe Factory Pool — Manages static ConcurrentHashMap cache via computeIfAbsent."),
            ("StreetlightContext.java", "Extrinsic Context — Lightweight object holding per-device state (GPS latitude/longitude, brightness, status)."),
            ("FlyweightBenchmark.java", "Memory Measurement Engine — Measures exact HotSpot JVM object layout footprint (72.2% reduction)."),
            ("NaiveHeavyStreetlight.java", "Unoptimized Baseline — Duplicates hardware properties across every streetlight for empirical comparison."),
            ("Test.java", "Verification Suite — Validates reference identity across 8 concurrent threads and zero cache duplication.")
        ],
        "scope_guide": "Capture StreetlightProfileFactory.java showing the ConcurrentHashMap cache pool and computeIfAbsent factory method alongside SharedStreetlightProfile.java.",
        "caption": "Production Source Code Implementation Screenshot — Smart Streetlight Flyweight Pool Architecture"
    },
    "E": {
        "listing_num": "6.1",
        "pattern_name": "City Policy DSL Mini-Language (Interpreter Pattern)",
        "primary_file": "backend/src/main/java/com/smartcity/pattern/interpreter/DslPolicyParser.java",
        "directory": "backend/src/main/java/com/smartcity/pattern/interpreter/",
        "files": [
            ("Expression.java", "Abstract Expression Interface — Declares boolean interpret(PolicyContext context) contract."),
            ("TerminalExpression.java", "Terminal Expression — Evaluates atomic relational predicates (>, <, =, BETWEEN) against context telemetry."),
            ("AndExpression.java", "Non-Terminal Expression — Evaluates binary logical AND between two sub-expressions."),
            ("OrExpression.java", "Non-Terminal Expression — Evaluates binary logical OR between two sub-expressions."),
            ("DslPolicyParser.java", "Recursive-Descent Parser — Parses raw DSL strings into recursive AST with token & depth security limits."),
            ("PolicyContext.java", "State Context — Stores runtime telemetry variable values (e.g. NOISE_LEVEL, AIR_QUALITY, TIME_HOUR)."),
            ("Test.java", "Verification Suite — Validates complex boolean expressions, BETWEEN operator, parentheses precedence, and syntax exceptions.")
        ],
        "scope_guide": "Capture DslPolicyParser.java showing recursive grammar parsing rules and AST construction alongside TerminalExpression.java.",
        "caption": "Production Source Code Implementation Screenshot — Municipal Policy DSL Grammar Interpreter"
    }
}

APPENDIX_CODE_FILES = {
    "A": {
        "part_title": "Part A: Dynamic Security Wrappers for Data Streams (Decorator Pattern)",
        "package": "com.smartcity.pattern.decorator",
        "files": [
            ("StreamData.java", "backend/src/main/java/com/smartcity/pattern/decorator/StreamData.java", "Component Interface — Defines uniform telemetry payload contract (getData(), getPayloadBytes(), getPayloadSize()).", "Capture complete interface definition showing method signatures."),
            ("EnergyStreamData.java", "backend/src/main/java/com/smartcity/pattern/decorator/EnergyStreamData.java", "Concrete Component — Ingests raw smart energy meter readings and stores unencrypted payload.", "Capture class constructor, fields, and getData() implementation."),
            ("StreamDataDecorator.java", "backend/src/main/java/com/smartcity/pattern/decorator/StreamDataDecorator.java", "Abstract Decorator — Holds protected wrappedStream reference and delegates calls.", "Capture aggregation constructor and default forwarding methods."),
            ("EncryptionDecorator.java", "backend/src/main/java/com/smartcity/pattern/decorator/EncryptionDecorator.java", "Concrete Decorator — 256-bit AES-GCM AEAD encryption engine with secure IV generation.", "Capture AES-GCM cipher initialization, IV generation, and ciphertext wrapping."),
            ("CompressionDecorator.java", "backend/src/main/java/com/smartcity/pattern/decorator/CompressionDecorator.java", "Concrete Decorator — GZIP compression wrapper applied prior to ciphering.", "Capture GZIPOutputStream compaction stream pipeline and byte conversion."),
            ("AuthenticationDecorator.java", "backend/src/main/java/com/smartcity/pattern/decorator/AuthenticationDecorator.java", "Concrete Decorator — HMAC-SHA256 authenticity signature generator and perimeter verifier.", "Capture Mac.getInstance('HmacSHA256') initialization and signature verification logic.")
        ]
    },
    "B": {
        "part_title": "Part B: Hierarchical Structure of Smart Zones (Composite Pattern)",
        "package": "com.smartcity.pattern.composite",
        "files": [
            ("ZoneComponent.java", "backend/src/main/java/com/smartcity/pattern/composite/ZoneComponent.java", "Component Interface — Declares uniform operations for leaves and composite zones.", "Capture executeCommand(), getEnergyConsumption(), add(), remove(), and getChildren() signatures."),
            ("BuildingLeaf.java", "backend/src/main/java/com/smartcity/pattern/composite/BuildingLeaf.java", "Leaf Component — Represents atomic smart buildings / assets; safe leaf enforcement.", "Capture local command execution and safe UnsupportedOperationException throwing on child methods."),
            ("ZoneComposite.java", "backend/src/main/java/com/smartcity/pattern/composite/ZoneComposite.java", "Composite Container — Maintains child components with recursive command broadcasting and power rollup.", "Capture List<ZoneComponent> children declaration, recursive loop in executeCommand(), and getEnergyConsumption()."),
            ("ZoneCommand.java", "backend/src/main/java/com/smartcity/pattern/composite/ZoneCommand.java", "Command Abstraction — Type-safe enum for municipal command broadcasting.", "Capture enum values (SHUTDOWN_POWER, RESTORE_POWER, EMERGENCY_LOCKDOWN, REPORT_STATUS).")
        ]
    },
    "C": {
        "part_title": "Part C: Escalation of Citizen Complaints (Chain of Responsibility Pattern)",
        "package": "com.smartcity.pattern.chain",
        "files": [
            ("ComplaintHandler.java", "backend/src/main/java/com/smartcity/pattern/chain/ComplaintHandler.java", "Abstract Base Handler — Maintains protected successor reference and handleRequest() delegation template.", "Capture nextHandler field, setNext() chaining method, and abstract handleRequest()."),
            ("LocalStaffHandler.java", "backend/src/main/java/com/smartcity/pattern/chain/LocalStaffHandler.java", "Concrete Handler 1 — Dispatches LOW severity municipal maintenance issues.", "Capture severity check for LOW and pass-through delegation to nextHandler."),
            ("SupervisorHandler.java", "backend/src/main/java/com/smartcity/pattern/chain/SupervisorHandler.java", "Concrete Handler 2 — Resolves MEDIUM severity municipal issues within operational SLAs.", "Capture severity check for MEDIUM and escalation delegation logic."),
            ("CityManagerHandler.java", "backend/src/main/java/com/smartcity/pattern/chain/CityManagerHandler.java", "Concrete Handler 3 — Authorizes HIGH severity critical municipal infrastructure repairs.", "Capture severity check for HIGH and executive dispatch logic."),
            ("TerminalFallbackHandler.java", "backend/src/main/java/com/smartcity/pattern/chain/TerminalFallbackHandler.java", "Emergency Fallback Handler — Safely traps CRITICAL or unhandled tickets into audit queue without drop hazards.", "Capture emergency routing to audit queue and final resolution logging."),
            ("ComplaintChainFactory.java", "backend/src/main/java/com/smartcity/pattern/chain/ComplaintChainFactory.java", "Assembly Factory — Instantiates and wires the complete handler chain sequentially.", "Capture chain assembly: ValidationTriage -> LocalStaff -> Supervisor -> CityManager -> TerminalFallback.")
        ]
    },
    "D": {
        "part_title": "Part D: Efficient Management of Smart Street Lights (Flyweight Pattern)",
        "package": "com.smartcity.pattern.flyweight",
        "files": [
            ("SharedStreetlightProfile.java", "backend/src/main/java/com/smartcity/pattern/flyweight/SharedStreetlightProfile.java", "Intrinsic Flyweight — Immutable hardware specification shared across 25,000 streetlights.", "Capture final immutable fields (model, bulbType, wattage, lumens, manufacturer) and constructor."),
            ("StreetlightProfileFactory.java", "backend/src/main/java/com/smartcity/pattern/flyweight/StreetlightProfileFactory.java", "Thread-Safe Factory Pool — Manages static ConcurrentHashMap cache via computeIfAbsent.", "Capture ConcurrentHashMap cache pool and computeIfAbsent factory retrieval method."),
            ("StreetlightContext.java", "backend/src/main/java/com/smartcity/pattern/flyweight/StreetlightContext.java", "Extrinsic Context — Lightweight object holding per-device state (GPS latitude/longitude, brightness, status).", "Capture context fields, profile reference, and display() operation."),
            ("FlyweightBenchmark.java", "backend/src/main/java/com/smartcity/pattern/flyweight/FlyweightBenchmark.java", "Memory Measurement Engine — Measures exact HotSpot JVM object layout footprint (72.2% reduction).", "Capture memory footprint calculation comparing naive vs flyweight memory consumption.")
        ]
    },
    "E": {
        "part_title": "Part E: Interpreting City Policies Defined in DSL (Interpreter Pattern)",
        "package": "com.smartcity.pattern.interpreter",
        "files": [
            ("Expression.java", "backend/src/main/java/com/smartcity/pattern/interpreter/Expression.java", "Abstract Expression Interface — Declares boolean interpret(PolicyContext context) contract.", "Capture interface declaration and single abstract interpret() method."),
            ("TerminalExpression.java", "backend/src/main/java/com/smartcity/pattern/interpreter/TerminalExpression.java", "Terminal Expression — Evaluates atomic relational predicates (>, <, =, BETWEEN) against context telemetry.", "Capture operator evaluation logic (GREATER, LESS, EQUALS, BETWEEN) against PolicyContext."),
            ("AndExpression.java", "backend/src/main/java/com/smartcity/pattern/interpreter/AndExpression.java", "Non-Terminal Expression — Evaluates binary logical AND between two sub-expressions.", "Capture composite interpret() returning left.interpret(ctx) && right.interpret(ctx)."),
            ("OrExpression.java", "backend/src/main/java/com/smartcity/pattern/interpreter/OrExpression.java", "Non-Terminal Expression — Evaluates binary logical OR between two sub-expressions.", "Capture composite interpret() returning left.interpret(ctx) || right.interpret(ctx)."),
            ("DslPolicyParser.java", "backend/src/main/java/com/smartcity/pattern/interpreter/DslPolicyParser.java", "Recursive-Descent Parser — Parses raw DSL strings into recursive AST with token & depth security limits.", "Capture recursive-descent grammar methods: parse(), parseOr(), parseAnd(), parsePrimary()."),
            ("PolicyContext.java", "backend/src/main/java/com/smartcity/pattern/interpreter/PolicyContext.java", "State Context — Stores runtime telemetry variable values (e.g. NOISE_LEVEL, AIR_QUALITY, TIME_HOUR).", "Capture Map<String, Object> telemetry store and get(), set(), getDouble() accessors.")
        ]
    }
}

def add_code_screenshot_placeholder(doc, code_meta):
    listing_num = code_meta["listing_num"]
    pattern_name = code_meta["pattern_name"]
    primary_file = code_meta["primary_file"]
    directory = code_meta["directory"]
    files = code_meta["files"]
    scope_guide = code_meta["scope_guide"]
    caption = code_meta["caption"]

    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.rows[0].cells[0]
    cell.width = Inches(6.5)

    set_cell_background(cell, "F8FAFC")
    set_cell_margins(cell, top=120, bottom=120, left=140, right=140)
    set_cell_borders(cell, top="94A3B8", bottom="94A3B8", left="1E3A8A", right="94A3B8", sz="16")

    # 1. Header Tag
    p_hdr = cell.paragraphs[0]
    p_hdr.paragraph_format.space_after = Pt(2)
    p_hdr.paragraph_format.line_spacing = 1.15
    r_tag = p_hdr.add_run(f"📸 [ SOURCE CODE SCREENSHOT PLACEHOLDER — LISTING {listing_num} ]")
    r_tag.bold = True
    r_tag.font.name = "Times New Roman"
    r_tag.font.size = Pt(10.5)
    r_tag.font.color.rgb = RGBColor(15, 41, 74)

    # 2. Title
    p_title = cell.add_paragraph()
    p_title.paragraph_format.space_after = Pt(3)
    p_title.paragraph_format.line_spacing = 1.15
    r_title = p_title.add_run(f"Production Source Code Screenshot: {pattern_name}")
    r_title.bold = True
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(11.5)
    r_title.font.color.rgb = RGBColor(30, 58, 138)

    # 3. Primary File Path highlight
    p_fp = cell.add_paragraph()
    p_fp.paragraph_format.space_after = Pt(4)
    p_fp.paragraph_format.line_spacing = 1.15
    r_fpl = p_fp.add_run("Target Source File: ")
    r_fpl.bold = True
    r_fpl.font.name = "Times New Roman"
    r_fpl.font.size = Pt(9.5)
    r_fpl.font.color.rgb = RGBColor(15, 23, 42)

    r_fp = p_fp.add_run(primary_file)
    r_fp.font.name = "Consolas"
    r_fp.font.size = Pt(9)
    r_fp.bold = True
    r_fp.font.color.rgb = RGBColor(30, 58, 138)

    # 4. Package Manifest header
    p_mf_hdr = cell.add_paragraph()
    p_mf_hdr.paragraph_format.space_after = Pt(2)
    p_mf_hdr.paragraph_format.line_spacing = 1.15
    r_mfh = p_mf_hdr.add_run(f"Complete Package File Manifest ({directory}) — packaged in project source ZIP:")
    r_mfh.italic = True
    r_mfh.font.name = "Times New Roman"
    r_mfh.font.size = Pt(9)
    r_mfh.font.color.rgb = RGBColor(71, 85, 105)

    # 5. Bullets of files
    for fn, fdesc in files:
        p_f = cell.add_paragraph()
        p_f.paragraph_format.space_after = Pt(1)
        p_f.paragraph_format.line_spacing = 1.1
        p_f.paragraph_format.left_indent = Inches(0.15)
        r_b = p_f.add_run("• ")
        r_b.bold = True
        r_b.font.name = "Times New Roman"
        r_b.font.size = Pt(8.5)
        r_b.font.color.rgb = RGBColor(30, 58, 138)

        r_fn = p_f.add_run(fn + " — ")
        r_fn.font.name = "Consolas"
        r_fn.font.size = Pt(8.5)
        r_fn.bold = True
        r_fn.font.color.rgb = RGBColor(15, 23, 42)

        r_fd = p_f.add_run(fdesc)
        r_fd.font.name = "Times New Roman"
        r_fd.font.size = Pt(8.5)
        r_fd.font.color.rgb = RGBColor(51, 65, 85)

    # 6. Visual Drop-Zone Box
    p_box = cell.add_paragraph()
    p_box.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_box.paragraph_format.space_before = Pt(6)
    p_box.paragraph_format.space_after = Pt(6)
    p_box.paragraph_format.line_spacing = 1.1
    drop_zone_text = (
        "┌────────────────────────────────────────────────────────────────────────┐\n"
        "│                                                                        │\n"
        "│        >>>  PASTE / INSERT SOURCE CODE SCREENSHOT HERE  <<<            │\n"
        "│                                                                        │\n"
        f"│   Target File Path: {primary_file.ljust(51)}│\n"
        "│                                                                        │\n"
        "│   Recommended IDE View: Capture class definition & key method          │\n"
        "│   dimensions: 6.0\" - 6.5\" Width x 3.5\" - 4.5\" Height (300 DPI)         │\n"
        "│                                                                        │\n"
        "└────────────────────────────────────────────────────────────────────────┘"
    )
    r_dz = p_box.add_run(drop_zone_text)
    r_dz.font.name = "Consolas"
    r_dz.font.size = Pt(8)
    r_dz.font.color.rgb = RGBColor(100, 116, 139)

    # 7. Candidate Instructions Guide
    p_inst = cell.add_paragraph()
    p_inst.paragraph_format.space_after = Pt(2)
    p_inst.paragraph_format.line_spacing = 1.15
    r_in = p_inst.add_run(f"📌 Candidate Screenshot Guide: Open '{primary_file}' in your IDE (VS Code / IntelliJ IDEA / NetBeans). Take a clean, full-width screenshot showing line numbers and syntax highlighting. {scope_guide} Paste your screenshot directly into this box.")
    r_in.italic = True
    r_in.font.name = "Times New Roman"
    r_in.font.size = Pt(8.5)
    r_in.font.color.rgb = RGBColor(71, 85, 105)

    # Formal Caption underneath the table
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(4)
    p_cap.paragraph_format.space_after = Pt(12)
    r_cf = p_cap.add_run(f"Listing {listing_num}: ")
    r_cf.bold = True
    r_cf.font.name = "Times New Roman"
    r_cf.font.size = Pt(9.5)
    r_cf.font.color.rgb = RGBColor(15, 41, 74)
    r_ct = p_cap.add_run(f"{caption} — {primary_file}")
    r_ct.italic = True
    r_ct.font.name = "Times New Roman"
    r_ct.font.size = Pt(9.5)
    r_ct.font.color.rgb = RGBColor(51, 65, 85)

def add_file_screenshot_placeholder(doc, file_num, filename, rel_path, role_desc, capture_notes):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.rows[0].cells[0]
    cell.width = Inches(6.5)

    set_cell_background(cell, "F8FAFC")
    set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
    set_cell_borders(cell, top="CBD5E1", bottom="CBD5E1", left="1E3A8A", right="CBD5E1", sz="12")

    p_hdr = cell.paragraphs[0]
    p_hdr.paragraph_format.space_after = Pt(2)
    p_hdr.paragraph_format.line_spacing = 1.15
    r_tag = p_hdr.add_run(f"📸 Screenshot {file_num}: {filename}")
    r_tag.bold = True
    r_tag.font.name = "Times New Roman"
    r_tag.font.size = Pt(10)
    r_tag.font.color.rgb = RGBColor(15, 41, 74)

    p_path = cell.add_paragraph()
    p_path.paragraph_format.space_after = Pt(2)
    p_path.paragraph_format.line_spacing = 1.15
    r_pl = p_path.add_run("File Path: ")
    r_pl.bold = True
    r_pl.font.name = "Times New Roman"
    r_pl.font.size = Pt(9)
    r_pl.font.color.rgb = RGBColor(71, 85, 105)

    r_pv = p_path.add_run(rel_path)
    r_pv.font.name = "Consolas"
    r_pv.font.size = Pt(8.5)
    r_pv.bold = True
    r_pv.font.color.rgb = RGBColor(30, 58, 138)

    p_role = cell.add_paragraph()
    p_role.paragraph_format.space_after = Pt(4)
    p_role.paragraph_format.line_spacing = 1.15
    r_rl = p_role.add_run("Architectural Role: ")
    r_rl.bold = True
    r_rl.font.name = "Times New Roman"
    r_rl.font.size = Pt(9)
    r_rl.font.color.rgb = RGBColor(71, 85, 105)

    r_rv = p_role.add_run(role_desc)
    r_rv.font.name = "Times New Roman"
    r_rv.font.size = Pt(9)
    r_rv.font.color.rgb = RGBColor(51, 65, 85)

    # Drop zone
    p_box = cell.add_paragraph()
    p_box.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_box.paragraph_format.space_before = Pt(4)
    p_box.paragraph_format.space_after = Pt(4)
    p_box.paragraph_format.line_spacing = 1.1
    drop_zone_text = (
        "┌────────────────────────────────────────────────────────────────────────┐\n"
        "│                                                                        │\n"
        f"│        >>>  PASTE / INSERT SCREENSHOT FOR: {filename.ljust(27)}│\n"
        "│                                                                        │\n"
        f"│   Path: {rel_path.ljust(63)}│\n"
        "│                                                                        │\n"
        "└────────────────────────────────────────────────────────────────────────┘"
    )
    r_dz = p_box.add_run(drop_zone_text)
    r_dz.font.name = "Consolas"
    r_dz.font.size = Pt(8)
    r_dz.font.color.rgb = RGBColor(100, 116, 139)

    p_inst = cell.add_paragraph()
    p_inst.paragraph_format.space_after = Pt(2)
    p_inst.paragraph_format.line_spacing = 1.15
    r_in = p_inst.add_run(f"📌 Capture Tip: {capture_notes}")
    r_in.italic = True
    r_in.font.name = "Times New Roman"
    r_in.font.size = Pt(8.5)
    r_in.font.color.rgb = RGBColor(71, 85, 105)

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after = Pt(10)
    r_cf = p_cap.add_run(f"Screenshot {file_num}: ")
    r_cf.bold = True
    r_cf.font.name = "Times New Roman"
    r_cf.font.size = Pt(9)
    r_cf.font.color.rgb = RGBColor(15, 41, 74)
    r_ct = p_cap.add_run(f"{filename} — {role_desc}")
    r_ct.italic = True
    r_ct.font.name = "Times New Roman"
    r_ct.font.size = Pt(9)
    r_ct.font.color.rgb = RGBColor(51, 65, 85)

def add_diagram_placeholder(doc, fig_meta):
    fig_num = fig_meta["fig_num"]
    title = fig_meta["title"]
    category = fig_meta["category"]
    criteria = fig_meta["criteria"]
    elements = fig_meta["elements"]
    instructions = fig_meta["instructions"]
    short_caption = fig_meta["short_caption"]

    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.rows[0].cells[0]
    cell.width = Inches(6.5)

    # Styling: Soft slate card background, thick primary navy left accent border, clean borders on 3 sides
    set_cell_background(cell, "F8FAFC")
    set_cell_margins(cell, top=120, bottom=120, left=140, right=140)
    set_cell_borders(cell, top="94A3B8", bottom="94A3B8", left="1E3A8A", right="94A3B8", sz="16")

    # 1. Header Tag
    p_hdr = cell.paragraphs[0]
    p_hdr.paragraph_format.space_after = Pt(2)
    p_hdr.paragraph_format.line_spacing = 1.15
    r_tag = p_hdr.add_run(f"📷 [ FIGURE PLACEHOLDER — FIGURE {fig_num} ]")
    r_tag.bold = True
    r_tag.font.name = "Times New Roman"
    r_tag.font.size = Pt(10.5)
    r_tag.font.color.rgb = RGBColor(15, 41, 74)

    # 2. Figure Title
    p_title = cell.add_paragraph()
    p_title.paragraph_format.space_after = Pt(3)
    p_title.paragraph_format.line_spacing = 1.15
    r_title = p_title.add_run(title)
    r_title.bold = True
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(11.5)
    r_title.font.color.rgb = RGBColor(30, 58, 138)

    # 3. Metadata line
    p_meta = cell.add_paragraph()
    p_meta.paragraph_format.space_after = Pt(6)
    p_meta.paragraph_format.line_spacing = 1.15
    r_meta = p_meta.add_run(f"Diagram Category: {category}   •   Assessment Mapping: {criteria}")
    r_meta.italic = True
    r_meta.font.name = "Times New Roman"
    r_meta.font.size = Pt(9)
    r_meta.font.color.rgb = RGBColor(71, 85, 105)

    # 4. Elements checklist header
    p_el_hdr = cell.add_paragraph()
    p_el_hdr.paragraph_format.space_after = Pt(2)
    p_el_hdr.paragraph_format.line_spacing = 1.15
    r_eh = p_el_hdr.add_run("Key Architectural Elements & Specifications to Include:")
    r_eh.bold = True
    r_eh.font.name = "Times New Roman"
    r_eh.font.size = Pt(9.5)
    r_eh.font.color.rgb = RGBColor(15, 23, 42)

    # 4. Bullet items
    for el in elements:
        p_el = cell.add_paragraph()
        p_el.paragraph_format.space_after = Pt(1)
        p_el.paragraph_format.line_spacing = 1.1
        p_el.paragraph_format.left_indent = Inches(0.15)
        r_b = p_el.add_run("• ")
        r_b.bold = True
        r_b.font.name = "Times New Roman"
        r_b.font.size = Pt(8.5)
        r_b.font.color.rgb = RGBColor(30, 58, 138)
        r_txt = p_el.add_run(el)
        r_txt.font.name = "Times New Roman"
        r_txt.font.size = Pt(8.5)
        r_txt.font.color.rgb = RGBColor(51, 65, 85)

    # 5. Visual Drop-Zone Box
    p_box = cell.add_paragraph()
    p_box.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_box.paragraph_format.space_before = Pt(6)
    p_box.paragraph_format.space_after = Pt(6)
    p_box.paragraph_format.line_spacing = 1.1
    drop_zone_text = (
        "┌────────────────────────────────────────────────────────────────────────┐\n"
        "│                                                                        │\n"
        "│               >>>  PASTE / INSERT YOUR DIAGRAM HERE  <<<               │\n"
        "│                                                                        │\n"
        "│   Supported Formats: High-Resolution PNG, SVG, or EMF (300 DPI)        │\n"
        "│   Recommended Canvas Dimensions: 6.0\" - 6.5\" Width x 3.5\" - 4.5\" Height │\n"
        "│                                                                        │\n"
        "└────────────────────────────────────────────────────────────────────────┘"
    )
    r_dz = p_box.add_run(drop_zone_text)
    r_dz.font.name = "Consolas"
    r_dz.font.size = Pt(8)
    r_dz.font.color.rgb = RGBColor(100, 116, 139)

    # 6. Candidate Instructions Note
    p_inst = cell.add_paragraph()
    p_inst.paragraph_format.space_after = Pt(2)
    p_inst.paragraph_format.line_spacing = 1.15
    r_in = p_inst.add_run(f"📌 Candidate Insertion Guide: {instructions}")
    r_in.italic = True
    r_in.font.name = "Times New Roman"
    r_in.font.size = Pt(8.5)
    r_in.font.color.rgb = RGBColor(71, 85, 105)

    # Formal Academic Caption underneath the table
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(4)
    p_cap.paragraph_format.space_after = Pt(12)
    r_cf = p_cap.add_run(f"Figure {fig_num}: ")
    r_cf.bold = True
    r_cf.font.name = "Times New Roman"
    r_cf.font.size = Pt(9.5)
    r_cf.font.color.rgb = RGBColor(15, 41, 74)
    r_ct = p_cap.add_run(f"{title} — {short_caption}")
    r_ct.italic = True
    r_ct.font.name = "Times New Roman"
    r_ct.font.size = Pt(9.5)
    r_ct.font.color.rgb = RGBColor(51, 65, 85)

def create_docx(filename):
    doc = Document()
    
    # Standard academic page setup - A4 with 1 inch (25.4 mm) margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        
        # Header - Formal Academic
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("Java Institute for Advanced Technology — Unit: JIAT/OODP II | Assessment: EX/01")
        hrun.font.name = "Times New Roman"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(100, 116, 139)
        
        # Footer - Formal Academic
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("SmartCity360 Technical Report — Department of Examinations | Final Submission")
        frun.font.name = "Times New Roman"
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(100, 116, 139)

    # Base Styles: Times New Roman, 11.5pt, 1.25 line spacing
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Times New Roman'
    style_normal.font.size = Pt(11.5)
    style_normal.font.color.rgb = RGBColor(30, 41, 59)
    style_normal.paragraph_format.line_spacing = 1.25
    style_normal.paragraph_format.space_after = Pt(6)

    # ------------------ DOCUMENT TITLE HEADER ------------------
    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.space_after = Pt(2)
    r_meta = p_meta.add_run(f"{content.METADATA['institution']} • Unit: {content.METADATA['unit_name']} ({content.METADATA['unit_id']}) • {content.METADATA['assessment_id']}")
    r_meta.font.name = "Times New Roman"
    r_meta.font.size = Pt(9)
    r_meta.font.color.rgb = RGBColor(30, 58, 138)
    r_meta.bold = True

    h_title = doc.add_heading(level=1)
    r_t = h_title.add_run("SMARTCITY360 MANAGEMENT PLATFORM")
    r_t.font.name = "Times New Roman"
    r_t.font.size = Pt(18)
    r_t.font.color.rgb = RGBColor(15, 41, 74)
    r_t.bold = True
    h_title.paragraph_format.space_after = Pt(2)

    p_sub = doc.add_paragraph()
    r_sub = p_sub.add_run("Technical Design Pattern Implementation & Comprehensive Architectural Assessment Report")
    r_sub.font.name = "Times New Roman"
    r_sub.font.size = Pt(11)
    r_sub.italic = True
    r_sub.bold = True
    r_sub.font.color.rgb = RGBColor(30, 58, 138)
    p_sub.paragraph_format.space_after = Pt(4)

    p_info = doc.add_paragraph()
    r_inf = p_info.add_run(f"Industrial Context: {content.METADATA['company']} • Target City: {content.METADATA['target_city']} • Weighting: {content.METADATA['total_marks']}")
    r_inf.font.name = "Times New Roman"
    r_inf.font.size = Pt(9)
    r_inf.font.color.rgb = RGBColor(100, 116, 139)
    p_info.paragraph_format.space_after = Pt(14)

    # ------------------ TABLE OF CONTENTS ------------------
    h_toc = doc.add_heading(level=1)
    r_toc = h_toc.add_run("TABLE OF CONTENTS")
    r_toc.font.name = "Times New Roman"
    r_toc.font.size = Pt(14)
    r_toc.font.color.rgb = RGBColor(15, 41, 74)
    h_toc.paragraph_format.space_after = Pt(12)

    toc_items = [
        ("1. Executive Summary & Scenario Overview", "2"),
        ("2. Part A — Dynamic Security Wrappers for Data Streams (Decorator Pattern) [15 Marks]", "3"),
        ("    2.1 Identification & Architectural Justification (3 Marks)", "3"),
        ("    2.2 Mechanism of Flexible & Layered Enhancement (4 Marks)", "4"),
        ("        [Figure 2.1 — UML Class Diagram: Dynamic Security Decorator Architecture]", "4"),
        ("    2.3 Long-Term Evaluation: Reusability, Extensibility & Anti-Pattern Mitigation (8 Marks)", "4"),
        ("    2.4 Object Wrapping Pipeline Flowchart & Source Code Architecture", "5"),
        ("        [Figure 2.2 — Data Stream Dynamic Wrapping Pipeline Execution Flowchart]", "5"),
        ("        [Listing 2.1 — Production Source Code Screenshot: EncryptionDecorator.java]", "6"),
        ("3. Part B — Hierarchical Structure of Smart Zones (Composite Pattern) [15 Marks]", "7"),
        ("    3.1 Identification & Architectural Justification (3 Marks)", "7"),
        ("    3.2 UML Class Diagram & Mechanism of the Hierarchical Composition (4 Marks)", "7"),
        ("        [Figure 3.1 — UML Class Diagram: Hierarchical Smart Zones Composite Pattern]", "8"),
        ("    3.3 Evaluation: Scalability & Growing Infrastructure Management (8 Marks)", "8"),
        ("    3.4 Hierarchical Urban Zone Topography & Source Code Architecture", "9"),
        ("        [Figure 3.2 — Hierarchical Urban Zone Topography & Object Composition Hierarchy]", "10"),
        ("        [Listing 3.1 — Production Source Code Screenshot: ZoneComposite.java]", "10"),
        ("4. Part C — Escalation of Citizen Complaints (Chain of Responsibility Pattern) [15 Marks]", "11"),
        ("    4.1 Identification & Architectural Justification (3 Marks)", "11"),
        ("    4.2 Mechanism of Decoupled Request Handling (4 Marks)", "11"),
        ("        [Figure 4.1 — UML Class Diagram: Multi-Tier Complaint Escalation Chain]", "12"),
        ("    4.3 Evaluation of Flexibility, Traceability, Benefits & Trade-offs (8 Marks)", "12"),
        ("    4.4 Multi-Tier Escalation Flowchart & Source Code Architecture", "13"),
        ("        [Figure 4.2 — Dynamic Citizen Complaint Escalation Workflow & Decision Flowchart]", "13"),
        ("        [Listing 4.1 — Production Source Code Screenshot: ComplaintHandler.java]", "14"),
        ("5. Part D — Efficient Management of Smart Street Lights (Flyweight Pattern) [15 Marks]", "15"),
        ("    5.1 Identification & Architectural Justification (3 Marks)", "15"),
        ("    5.2 Handling Shared Intrinsic vs Unique Extrinsic State (4 Marks)", "15"),
        ("        [Figure 5.1 — UML Class Diagram: Smart Streetlight Flyweight Pattern Architecture]", "16"),
        ("    5.3 Quantitative Memory & Performance Impact Analysis (94.9% Reduction) (8 Marks)", "16"),
        ("    5.4 JVM Memory Pool Architecture Diagram & Source Code Architecture", "17"),
        ("        [Figure 5.2 — JVM Heap Memory Allocation: Flyweight Pool vs Unoptimized Graph]", "18"),
        ("        [Listing 5.1 — Production Source Code Screenshot: StreetlightProfileFactory.java]", "18"),
        ("6. Part E — Interpreting City Policies Defined in DSL (Interpreter Pattern) [15 Marks]", "19"),
        ("    6.1 Identification & Architectural Justification (3 Marks)", "19"),
        ("    6.2 UML Class Diagram & Mechanism of the DSL Interpreter Pattern (4 Marks)", "19"),
        ("        [Figure 6.1 — UML Class Diagram: Municipal Policy DSL Grammar & Interpreter]", "20"),
        ("    6.3 Critical Assessment: Rule Updates, Extensibility & Security (8 Marks)", "20"),
        ("    6.4 Abstract Syntax Tree (AST) & Source Code Architecture", "21"),
        ("        [Figure 6.2 — Abstract Syntax Tree (AST) Decomposition & Evaluation Flowchart]", "21"),
        ("        [Listing 6.1 — Production Source Code Screenshot: DslPolicyParser.java]", "22"),
        ("7. Part F — Final Project Demonstration, VIVA Defense & Video Outline [25 Marks]", "23"),
        ("    7.1 Overall System Architecture & Multi-Tier Enterprise Design", "23"),
        ("        [Figure 7.1 — End-to-End SmartCity360 Multi-Tier Enterprise Platform Architecture]", "24"),
        ("        [Figure 7.2 — SmartCity360 Comprehensive System Use Case Diagram]", "25"),
        ("        [Figure 7.3 — Architectural Package Structure & Component Interaction Diagram]", "26"),
        ("    7.2 Key Architectural Choices & Anti-Pattern Defense Matrix", "27"),
        ("    7.3 Empirical Automated Test Execution Results (35/35 Tests Passing - 100%)", "28"),
        ("    7.4 Final Submission Deliverables Verification", "29"),
        ("8. Conclusion & Academic References", "31"),
        ("9. Appendix A — Comprehensive Source Code Implementation Screenshot Catalog", "32"),
        ("    9.1 Part A: Data Stream Security Wrappers Source Code Screenshots (Decorator Pattern)", "32"),
        ("    9.2 Part B: Hierarchical Smart Zones Source Code Screenshots (Composite Pattern)", "34"),
        ("    9.3 Part C: Citizen Grievance Escalation Source Code Screenshots (Chain of Responsibility Pattern)", "36"),
        ("    9.4 Part D: Smart Streetlight Memory Optimization Source Code Screenshots (Flyweight Pattern)", "38"),
        ("    9.5 Part E: Municipal Policy DSL Grammar Source Code Screenshots (Interpreter Pattern)", "40")
    ]
    for item, page in toc_items:
        p_item = doc.add_paragraph()
        p_item.paragraph_format.space_after = Pt(2)
        r_txt = p_item.add_run(item)
        r_txt.font.name = "Times New Roman"
        r_txt.font.size = Pt(10)
        if item.startswith(" ") is False and not item.startswith("    "):
            r_txt.bold = True
            r_txt.font.color.rgb = RGBColor(15, 23, 42)
        elif "[" in item:
            r_txt.italic = True
            r_txt.font.size = Pt(9)
            r_txt.font.color.rgb = RGBColor(30, 58, 138)
        else:
            r_txt.font.color.rgb = RGBColor(71, 85, 105)

    doc.add_page_break()

    # ------------------ LIST OF FIGURES ------------------
    h_lof = doc.add_heading(level=1)
    r_lof = h_lof.add_run("LIST OF ARCHITECTURAL FIGURES & DIAGRAMS")
    r_lof.font.name = "Times New Roman"
    r_lof.font.size = Pt(14)
    r_lof.font.color.rgb = RGBColor(15, 41, 74)
    h_lof.paragraph_format.space_after = Pt(8)

    p_lof_note = doc.add_paragraph()
    r_ln = p_lof_note.add_run(
        "This technical assessment report incorporates 13 dedicated architectural diagrams, UML class models, behavioral sequence workflows, and system enterprise designs mapped directly to the assessment rubric. Each figure location provides a structured placeholder and technical specification for direct visual artifact insertion:"
    )
    r_ln.font.name = "Times New Roman"
    r_ln.font.size = Pt(10)
    r_ln.italic = True
    r_ln.font.color.rgb = RGBColor(71, 85, 105)
    p_lof_note.paragraph_format.space_after = Pt(10)

    figures_list = [
        ("Figure 2.1", "UML Class Diagram — Dynamic Security Decorator Pattern Architecture", "Part A.2 (4 Marks)", "Section 2.2"),
        ("Figure 2.2", "Data Stream Dynamic Wrapping Pipeline & Execution Flowchart", "Part A.4 (Highlights)", "Section 2.4"),
        ("Figure 3.1", "UML Class Diagram — Hierarchical Smart Zones Composite Pattern", "Part B.2 (4 Marks - Mandatory)", "Section 3.2"),
        ("Figure 3.2", "Hierarchical Urban Zone Topography & Object Composition Hierarchy", "Part B.4 (Highlights)", "Section 3.4"),
        ("Figure 4.1", "UML Class Diagram — Multi-Tier Complaint Escalation Chain of Responsibility", "Part C.2 (4 Marks)", "Section 4.2"),
        ("Figure 4.2", "Citizen Complaint Dynamic Escalation Workflow & Decision Flowchart", "Part C.4 (Highlights)", "Section 4.4"),
        ("Figure 5.1", "UML Class Diagram — Smart Streetlight Flyweight Pattern Architecture", "Part D.2 (4 Marks)", "Section 5.2"),
        ("Figure 5.2", "JVM Heap Memory Allocation: Flyweight Shared Pool vs Unoptimized Heap Graph", "Part D.4 (Highlights)", "Section 5.4"),
        ("Figure 6.1", "UML Class Diagram — Municipal Policy DSL Grammar & Interpreter Pattern", "Part E.2 (4 Marks - Mandatory)", "Section 6.2"),
        ("Figure 6.2", "Abstract Syntax Tree (AST) Decomposition & Boolean Evaluation Flowchart", "Part E.4 (Highlights)", "Section 6.4"),
        ("Figure 7.1", "End-to-End SmartCity360 Multi-Tier Enterprise Platform Architecture Diagram", "Part F.1 (10 Marks)", "Section 7.1"),
        ("Figure 7.2", "SmartCity360 Comprehensive System Use Case Diagram", "Part F.1 (Use Cases)", "Section 7.1"),
        ("Figure 7.3", "Architectural Package Structure & Subsystem Component Interaction Diagram", "Part F.1 (Components)", "Section 7.1")
    ]

    tbl_lof = doc.add_table(rows=len(figures_list) + 1, cols=4)
    tbl_lof.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_l = tbl_lof.rows[0]
    for ci, htxt in enumerate(["Figure ID", "Diagram Title & Description", "Rubric Mapping", "Report Location"]):
        cell = hdr_l.cells[ci]
        set_cell_background(cell, "0F294A")
        set_cell_margins(cell, 60, 60, 80, 80)
        p = cell.paragraphs[0]
        r = p.add_run(htxt)
        r.bold = True
        r.font.name = "Times New Roman"
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    hdr_l.cells[0].width = Inches(1.1)
    hdr_l.cells[1].width = Inches(2.9)
    hdr_l.cells[2].width = Inches(1.5)
    hdr_l.cells[3].width = Inches(1.0)

    for ri, (fid, ftitle, fm, floc) in enumerate(figures_list):
        row = tbl_lof.rows[ri + 1]
        c0, c1, c2, c3 = row.cells[0], row.cells[1], row.cells[2], row.cells[3]
        c0.width, c1.width, c2.width, c3.width = Inches(1.1), Inches(2.9), Inches(1.5), Inches(1.0)
        bg = "F8FAFC" if ri % 2 == 0 else "FFFFFF"

        for ci, (cell, val) in enumerate([(c0, fid), (c1, ftitle), (c2, fm), (c3, floc)]):
            set_cell_background(cell, bg)
            set_cell_margins(cell, 45, 45, 60, 60)
            set_cell_borders(cell, top="CBD5E1", bottom="CBD5E1", left="CBD5E1", right="CBD5E1")
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(val)
            r.font.name = "Times New Roman"
            r.font.size = Pt(8.5)
            r.font.color.rgb = RGBColor(15, 23, 42)
            if ci == 0:
                r.bold = True
                r.font.color.rgb = RGBColor(30, 58, 138)
            elif ci == 2 and "Mandatory" in val:
                r.bold = True

    p_sp_lof = doc.add_paragraph()
    p_sp_lof.paragraph_format.space_after = Pt(14)

    # ------------------ LIST OF SOURCE CODE SCREENSHOT PLACEMENTS ------------------
    h_los = doc.add_heading(level=2)
    r_los = h_los.add_run("LIST OF SOURCE CODE IMPLEMENTATION SCREENSHOT PLACEMENTS")
    r_los.font.name = "Times New Roman"
    r_los.font.size = Pt(12)
    r_los.font.color.rgb = RGBColor(15, 41, 74)
    r_los.bold = True
    h_los.paragraph_format.space_after = Pt(6)

    p_los_note = doc.add_paragraph()
    r_lsn = p_los_note.add_run(
        "In accordance with Part F.3 of the assessment specification, raw source code text has been removed and replaced with dedicated screenshot containers. Candidates can capture high-resolution IDE screenshots (VS Code / IntelliJ) for each primary target file and insert them into the designated sections and Appendix A:"
    )
    r_lsn.font.name = "Times New Roman"
    r_lsn.font.size = Pt(9.5)
    r_lsn.italic = True
    r_lsn.font.color.rgb = RGBColor(71, 85, 105)
    p_los_note.paragraph_format.space_after = Pt(8)

    code_listings = [
        ("Listing 2.1", "Dynamic Security Decorator Pattern", "backend/src/main/java/com/smartcity/pattern/decorator/EncryptionDecorator.java", "Section 2.4 & App. A.1"),
        ("Listing 3.1", "Hierarchical Smart Zones (Composite Pattern)", "backend/src/main/java/com/smartcity/pattern/composite/ZoneComposite.java", "Section 3.4 & App. A.2"),
        ("Listing 4.1", "Citizen Grievance Escalation (Chain of Responsibility)", "backend/src/main/java/com/smartcity/pattern/chain/ComplaintHandler.java", "Section 4.4 & App. A.3"),
        ("Listing 5.1", "Smart Streetlight Memory Optimization (Flyweight Pattern)", "backend/src/main/java/com/smartcity/pattern/flyweight/StreetlightProfileFactory.java", "Section 5.4 & App. A.4"),
        ("Listing 6.1", "Municipal Policy DSL Mini-Language (Interpreter Pattern)", "backend/src/main/java/com/smartcity/pattern/interpreter/DslPolicyParser.java", "Section 6.4 & App. A.5")
    ]

    tbl_los = doc.add_table(rows=len(code_listings) + 1, cols=4)
    tbl_los.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_s = tbl_los.rows[0]
    for ci, htxt in enumerate(["Listing ID", "Pattern / Subsystem Title", "Primary Target Source File Path", "Report Location"]):
        cell = hdr_s.cells[ci]
        set_cell_background(cell, "0F294A")
        set_cell_margins(cell, 60, 60, 80, 80)
        p = cell.paragraphs[0]
        r = p.add_run(htxt)
        r.bold = True
        r.font.name = "Times New Roman"
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    hdr_s.cells[0].width = Inches(1.1)
    hdr_s.cells[1].width = Inches(2.3)
    hdr_s.cells[2].width = Inches(2.1)
    hdr_s.cells[3].width = Inches(1.0)

    for ri, (lid, ltitle, lpath, lloc) in enumerate(code_listings):
        row = tbl_los.rows[ri + 1]
        c0, c1, c2, c3 = row.cells[0], row.cells[1], row.cells[2], row.cells[3]
        c0.width, c1.width, c2.width, c3.width = Inches(1.1), Inches(2.3), Inches(2.1), Inches(1.0)
        bg = "F8FAFC" if ri % 2 == 0 else "FFFFFF"

        for ci, (cell, val) in enumerate([(c0, lid), (c1, ltitle), (c2, lpath), (c3, lloc)]):
            set_cell_background(cell, bg)
            set_cell_margins(cell, 45, 45, 60, 60)
            set_cell_borders(cell, top="CBD5E1", bottom="CBD5E1", left="CBD5E1", right="CBD5E1")
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(val)
            if ci == 2:
                r.font.name = "Consolas"
                r.font.size = Pt(7.5)
            else:
                r.font.name = "Times New Roman"
                r.font.size = Pt(8.5)
            r.font.color.rgb = RGBColor(15, 23, 42)
            if ci == 0:
                r.bold = True
                r.font.color.rgb = RGBColor(30, 58, 138)

    doc.add_page_break()

    # ------------------ 1. EXECUTIVE SUMMARY ------------------
    h1 = doc.add_heading(level=1)
    r1 = h1.add_run("1. EXECUTIVE SUMMARY & SCENARIO OVERVIEW")
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(14)
    r1.font.color.rgb = RGBColor(15, 41, 74)
    h1.paragraph_format.space_after = Pt(10)

    for para in content.EXEC_SUMMARY.split("\n\n"):
        p = doc.add_paragraph()
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_after = Pt(8)
        r = p.add_run(para)
        r.font.name = "Times New Roman"
        r.font.size = Pt(11.5)

    # ------------------ PARTS A - E ------------------
    def render_part(part_data, part_num, part_letter):
        doc.add_page_break()
        h_part = doc.add_heading(level=1)
        r_part = h_part.add_run(f"{part_num}. {part_data['title']} [{part_data['marks']}]")
        r_part.font.name = "Times New Roman"
        r_part.font.size = Pt(14)
        r_part.font.color.rgb = RGBColor(15, 41, 74)
        h_part.paragraph_format.space_after = Pt(8)

        # Scenario
        p_scen = doc.add_paragraph()
        p_scen.paragraph_format.left_indent = Inches(0.2)
        p_scen.paragraph_format.right_indent = Inches(0.2)
        p_scen.paragraph_format.space_after = Pt(10)
        r_scen_title = p_scen.add_run("Scenario Description: ")
        r_scen_title.bold = True
        r_scen_title.font.name = "Times New Roman"
        r_scen_title.font.size = Pt(11)
        r_scen_title.font.color.rgb = RGBColor(30, 58, 138)
        r_scen_txt = p_scen.add_run(part_data["scenario"])
        r_scen_txt.font.italic = True
        r_scen_txt.font.name = "Times New Roman"
        r_scen_txt.font.size = Pt(11)
        r_scen_txt.font.color.rgb = RGBColor(51, 65, 85)

        # Questions
        for q_idx, q_key in enumerate(["q1", "q2", "q3"], 1):
            q_info = part_data[q_key]
            h_q = doc.add_heading(level=2)
            r_q = h_q.add_run(f"{part_num}.{q_idx} {q_info['title']}")
            r_q.font.name = "Times New Roman"
            r_q.font.size = Pt(12)
            r_q.bold = True
            r_q.font.color.rgb = RGBColor(30, 58, 138)
            h_q.paragraph_format.space_after = Pt(6)

            if "pattern" in q_info:
                p_pat = doc.add_paragraph()
                r_plbl = p_pat.add_run("Selected Design Pattern: ")
                r_plbl.bold = True
                r_plbl.font.name = "Times New Roman"
                r_plbl.font.size = Pt(11)
                r_plbl.font.color.rgb = RGBColor(15, 41, 74)
                r_pval = p_pat.add_run(q_info["pattern"])
                r_pval.bold = True
                r_pval.font.name = "Times New Roman"
                r_pval.font.size = Pt(11)
                r_pval.font.color.rgb = RGBColor(30, 58, 138)
                p_pat.paragraph_format.space_after = Pt(6)

            for paragraph_txt in q_info["content"].split("\n\n"):
                p_body = doc.add_paragraph()
                p_body.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                p_body.paragraph_format.space_after = Pt(6)
                for line in paragraph_txt.split("\n"):
                    if line.strip().startswith("•") or line.strip().startswith("-") or line.strip().startswith("Step"):
                        r_line = p_body.add_run(line + "\n")
                        r_line.font.name = "Times New Roman"
                        r_line.font.size = Pt(11)
                    elif ":" in line and not line.strip().startswith("http"):
                        parts = line.split(":", 1)
                        r_h = p_body.add_run(parts[0] + ":")
                        r_h.bold = True
                        r_h.font.name = "Times New Roman"
                        r_h.font.size = Pt(11)
                        r_b = p_body.add_run(parts[1] + "\n")
                        r_b.font.name = "Times New Roman"
                        r_b.font.size = Pt(11)
                    else:
                        r_line = p_body.add_run(line + "\n")
                        r_line.font.name = "Times New Roman"
                        r_line.font.size = Pt(11)

            # Insert Q2 Diagram Placeholder (e.g. UML Class Diagram for Q2)
            if q_idx == 2 and part_letter in FIGURES_METADATA and "q2" in FIGURES_METADATA[part_letter]:
                add_diagram_placeholder(doc, FIGURES_METADATA[part_letter]["q2"])

        # Section 4: Highlights & Source Code Architecture
        h_code = doc.add_heading(level=2)
        r_code_t = h_code.add_run(f"{part_num}.4 Architectural Implementation Highlights & Source Code Architecture")
        r_code_t.font.name = "Times New Roman"
        r_code_t.font.size = Pt(12)
        r_code_t.bold = True
        r_code_t.font.color.rgb = RGBColor(30, 58, 138)
        h_code.paragraph_format.space_after = Pt(6)

        # Insert Section 4 Diagram Placeholder (Flowchart / Topography / AST / Memory)
        if part_letter in FIGURES_METADATA and "highlights" in FIGURES_METADATA[part_letter]:
            add_diagram_placeholder(doc, FIGURES_METADATA[part_letter]["highlights"])

        # Insert Section 4 Source Code Implementation Screenshot Placeholder (Zero raw code text)
        if part_letter in CODE_SCREENSHOTS_METADATA:
            add_code_screenshot_placeholder(doc, CODE_SCREENSHOTS_METADATA[part_letter])

    # Render Parts A-E
    render_part(content.PART_A, "2", "A")
    render_part(content.PART_B, "3", "B")
    render_part(content.PART_C, "4", "C")
    render_part(content.PART_D, "5", "D")
    render_part(content.PART_E, "6", "E")

    # ------------------ PART F ------------------
    doc.add_page_break()
    h_f = doc.add_heading(level=1)
    r_f = h_f.add_run("7. PART F — FINAL PROJECT DEMONSTRATION, VIVA DEFENSE & DOCUMENTATION [25 MARKS]")
    r_f.font.name = "Times New Roman"
    r_f.font.size = Pt(14)
    r_f.font.color.rgb = RGBColor(15, 41, 74)
    h_f.paragraph_format.space_after = Pt(10)

    # F.1
    h_f1 = doc.add_heading(level=2)
    r_f1 = h_f1.add_run("7.1 Overall System Architecture & Multi-Tier Enterprise Design")
    r_f1.font.name = "Times New Roman"
    r_f1.font.size = Pt(12)
    r_f1.bold = True
    r_f1.font.color.rgb = RGBColor(30, 58, 138)
    h_f1.paragraph_format.space_after = Pt(6)

    for p_txt in content.PART_F["f1_arch"].split("\n\n"):
        p = doc.add_paragraph()
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_after = Pt(6)
        r = p.add_run(p_txt)
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)

    # Add Part F Figure Placeholders: 7.1, 7.2, 7.3
    add_diagram_placeholder(doc, FIGURES_METADATA["F"]["f1_arch"])
    add_diagram_placeholder(doc, FIGURES_METADATA["F"]["f1_usecase"])
    add_diagram_placeholder(doc, FIGURES_METADATA["F"]["f1_component"])

    # F.2
    h_f2 = doc.add_heading(level=2)
    r_f2 = h_f2.add_run("7.2 Key Architectural Choices & Anti-Pattern Defense Matrix")
    r_f2.font.name = "Times New Roman"
    r_f2.font.size = Pt(12)
    r_f2.bold = True
    r_f2.font.color.rgb = RGBColor(30, 58, 138)
    h_f2.paragraph_format.space_after = Pt(6)

    p_apd = doc.add_paragraph()
    r_ad = p_apd.add_run("The SmartCity360 platform actively mitigates all 8 foundational software anti-patterns identified in the curriculum:")
    r_ad.font.name = "Times New Roman"
    r_ad.font.size = Pt(11)

    # Formal table for anti-patterns
    tbl_ap = doc.add_table(rows=len(content.PART_F["f2_antipatterns"]) + 1, cols=3)
    tbl_ap.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = tbl_ap.rows[0]
    for ci, htxt in enumerate(["Anti-Pattern", "Architectural Hazard & Symptom", "SmartCity360 Pattern Mitigation"]):
        cell = hdr.cells[ci]
        set_cell_background(cell, "0F294A")
        set_cell_margins(cell, 60, 60, 80, 80)
        p = cell.paragraphs[0]
        r = p.add_run(htxt)
        r.bold = True
        r.font.name = "Times New Roman"
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    hdr.cells[0].width = Inches(1.5)
    hdr.cells[1].width = Inches(2.3)
    hdr.cells[2].width = Inches(2.7)

    for ri, (ap_name, ap_sym, ap_mit) in enumerate(content.PART_F["f2_antipatterns"]):
        row = tbl_ap.rows[ri + 1]
        c0, c1, c2 = row.cells[0], row.cells[1], row.cells[2]
        c0.width, c1.width, c2.width = Inches(1.5), Inches(2.3), Inches(2.7)
        bg = "F8FAFC" if ri % 2 == 0 else "FFFFFF"

        for ci, (cell, val) in enumerate([(c0, ap_name), (c1, ap_sym), (c2, ap_mit)]):
            set_cell_background(cell, bg)
            set_cell_margins(cell, 50, 50, 70, 70)
            set_cell_borders(cell, top="CBD5E1", bottom="CBD5E1", left="CBD5E1", right="CBD5E1")
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(val)
            r.font.name = "Times New Roman"
            r.font.size = Pt(9)
            r.font.color.rgb = RGBColor(15, 23, 42)
            if ci == 0:
                r.bold = True
                r.font.color.rgb = RGBColor(30, 58, 138)

    p_sp2 = doc.add_paragraph()
    p_sp2.paragraph_format.space_after = Pt(12)

    # F.3 Automated Test Execution Results
    h_f3 = doc.add_heading(level=2)
    r_f3 = h_f3.add_run("7.3 Empirical Automated Test Execution Results (35/35 PASS - 100% Rate)")
    r_f3.font.name = "Times New Roman"
    r_f3.font.size = Pt(12)
    r_f3.bold = True
    r_f3.font.color.rgb = RGBColor(30, 58, 138)
    h_f3.paragraph_format.space_after = Pt(6)

    # 7.3 Automated Test Execution Results Table
    tbl_t = doc.add_table(rows=7, cols=6)
    tbl_t.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_t = tbl_t.rows[0]
    for ci, htxt in enumerate(["Subsystem / Pattern", "Tests", "Passed", "Failed", "Success Rate", "Key Verified Characteristics"]):
        cell = hdr_t.cells[ci]
        set_cell_background(cell, "0F294A")
        set_cell_margins(cell, 60, 60, 80, 80)
        p = cell.paragraphs[0]
        r = p.add_run(htxt)
        r.bold = True
        r.font.name = "Times New Roman"
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    test_data = [
        ("Decorator Pattern", "6", "6", "0", "100.0%", "Compression-before-encryption; AES-GCM AEAD; HMAC verification"),
        ("Composite Pattern", "8", "8", "0", "100.0%", "Recursive shutdown/restore; baseline power restoration; leaf safety; cycle prevention"),
        ("Chain of Responsibility", "8", "8", "0", "100.0%", "Safe triage; non-LOW fallback; audit timestamps; zero dropped tickets"),
        ("Flyweight Pattern", "5", "5", "0", "100.0%", "Profile instance identity; distinct key caching; 8-thread concurrency; 72.2% layout savings"),
        ("Interpreter Pattern", "8", "8", "0", "100.0%", "Recursive-descent AST; BETWEEN operator; nested parentheses; safety limits"),
        ("Total Test Suite", "35", "35", "0", "100.0%", "35 / 35 Tests Passing (100.0% Success Rate across All 5 Patterns)")
    ]

    for ri, row_data in enumerate(test_data):
        row = tbl_t.rows[ri + 1]
        bg = "E2E8F0" if ri == 5 else ("F8FAFC" if ri % 2 == 0 else "FFFFFF")
        for ci, val in enumerate(row_data):
            cell = row.cells[ci]
            set_cell_background(cell, bg)
            set_cell_margins(cell, 50, 50, 70, 70)
            set_cell_borders(cell, top="CBD5E1", bottom="CBD5E1", left="CBD5E1", right="CBD5E1")
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(val)
            r.font.name = "Times New Roman"
            r.font.size = Pt(9)
            if ri == 5 or ci == 0:
                r.bold = True
            if ci in (2, 4) and val != "0":
                r.font.color.rgb = RGBColor(5, 150, 105)
            else:
                r.font.color.rgb = RGBColor(15, 23, 42)

    p_sp_test = doc.add_paragraph()
    p_sp_test.paragraph_format.space_after = Pt(14)
    h_f5 = doc.add_heading(level=2)
    r_f5 = h_f5.add_run("7.4 Final Submission Deliverables Verification")
    r_f5.font.name = "Times New Roman"
    r_f5.font.size = Pt(12)
    r_f5.bold = True
    r_f5.font.color.rgb = RGBColor(30, 58, 138)
    h_f5.paragraph_format.space_after = Pt(6)

    p_f5 = doc.add_paragraph()
    r_f5_p = p_f5.add_run("In accordance with Section 5 of the assessment specification (Part F), the three mandatory deliverables have been prepared, audited, and formatted for direct submission to the Java Institute Student Portal:")
    r_f5_p.font.name = "Times New Roman"
    r_f5_p.font.size = Pt(11)

    tbl_del = doc.add_table(rows=len(content.PART_F.get("f5_deliverables", [])) + 1, cols=4)
    tbl_del.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_del = tbl_del.rows[0]
    for ci, htxt in enumerate(["Requirement", "Portal Section", "Artifact File", "Verification Scope"]):
        cell = hdr_del.cells[ci]
        set_cell_background(cell, "0F294A")
        set_cell_margins(cell, 60, 60, 80, 80)
        p = cell.paragraphs[0]
        r = p.add_run(htxt)
        r.bold = True
        r.font.name = "Times New Roman"
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    hdr_del.cells[0].width = Inches(1.5)
    hdr_del.cells[1].width = Inches(1.5)
    hdr_del.cells[2].width = Inches(1.8)
    hdr_del.cells[3].width = Inches(1.7)

    for ri, (req, portal, fmt, fn, desc) in enumerate(content.PART_F.get("f5_deliverables", [])):
        row = tbl_del.rows[ri + 1]
        c0, c1, c2, c3 = row.cells[0], row.cells[1], row.cells[2], row.cells[3]
        c0.width, c1.width, c2.width, c3.width = Inches(1.5), Inches(1.5), Inches(1.8), Inches(1.7)
        bg = "F8FAFC" if ri % 2 == 0 else "FFFFFF"

        for ci, (cell, val) in enumerate([(c0, req), (c1, f"{portal}\n({fmt})"), (c2, fn), (c3, desc)]):
            set_cell_background(cell, bg)
            set_cell_margins(cell, 50, 50, 70, 70)
            set_cell_borders(cell, top="CBD5E1", bottom="CBD5E1", left="CBD5E1", right="CBD5E1")
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(val)
            r.font.name = "Times New Roman"
            r.font.size = Pt(8.5)
            r.font.color.rgb = RGBColor(15, 23, 42)
            if ci == 0:
                r.bold = True
                r.font.color.rgb = RGBColor(30, 58, 138)
            elif ci == 2:
                r.bold = True

    p_sp4 = doc.add_paragraph()
    p_sp4.paragraph_format.space_after = Pt(16)

    # ------------------ REFERENCES ------------------
    doc.add_page_break()
    h_ref = doc.add_heading(level=1)
    r_ref = h_ref.add_run("8. CONCLUSION & ACADEMIC REFERENCES")
    r_ref.font.name = "Times New Roman"
    r_ref.font.size = Pt(14)
    r_ref.font.color.rgb = RGBColor(15, 41, 74)
    h_ref.paragraph_format.space_after = Pt(10)

    p_conc = doc.add_paragraph()
    p_conc.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r_cc = p_conc.add_run("Conclusion:\n")
    r_cc.bold = True
    r_cc.font.name = "Times New Roman"
    r_cc.font.size = Pt(11.5)
    r_cctx = p_conc.add_run(
        "The SmartCity360 platform exemplifies how classic Gang of Four design patterns solve real-world, high-concurrency challenges in smart municipal infrastructure. By strategically combining structural (Decorator, Composite, Flyweight) and behavioral (Chain of Responsibility, Interpreter) patterns, the system achieves maximum extensibility, robust security, minimal resource consumption, and decoupled maintenance."
    )
    r_cctx.font.name = "Times New Roman"
    r_cctx.font.size = Pt(11.5)
    p_conc.paragraph_format.space_after = Pt(16)

    p_rlbl = doc.add_paragraph()
    r_rl = p_rlbl.add_run("Academic References & Literature:")
    r_rl.bold = True
    r_rl.font.name = "Times New Roman"
    r_rl.font.size = Pt(11.5)
    r_rl.font.color.rgb = RGBColor(15, 41, 74)
    p_rlbl.paragraph_format.space_after = Pt(6)

    for ref in content.REFERENCES:
        p_r = doc.add_paragraph()
        p_r.paragraph_format.left_indent = Inches(0.3)
        p_r.paragraph_format.space_after = Pt(4)
        r = p_r.add_run("• " + ref)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10.5)
        r.font.color.rgb = RGBColor(51, 65, 85)

    p_sp_ref = doc.add_paragraph()
    p_sp_ref.paragraph_format.space_after = Pt(16)

    # ------------------ 9. APPENDIX A ------------------
    doc.add_page_break()
    h_app = doc.add_heading(level=1)
    r_app = h_app.add_run("9. APPENDIX A — COMPREHENSIVE SOURCE CODE IMPLEMENTATION SCREENSHOT CATALOG")
    r_app.font.name = "Times New Roman"
    r_app.font.size = Pt(14)
    r_app.font.color.rgb = RGBColor(15, 41, 74)
    h_app.paragraph_format.space_after = Pt(8)

    p_app_intro = doc.add_paragraph()
    p_app_intro.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r_ai = p_app_intro.add_run(
        "This appendix provides a structured, formal catalog of all production source code files developed for the SmartCity360 municipal platform. In compliance with Part F.3 of the assessment specification ('prepare comprehensive project documentation, including working code to illustrate the design and functionality of your application'), each pattern's source files are mapped with their exact repository paths, architectural role, and dedicated high-resolution screenshot drop zones. Candidates can capture screenshots directly from their IDE (VS Code / IntelliJ IDEA) and insert them into each designated container below:"
    )
    r_ai.font.name = "Times New Roman"
    r_ai.font.size = Pt(11)
    p_app_intro.paragraph_format.space_after = Pt(12)

    app_counter = 1
    for p_letter in ["A", "B", "C", "D", "E"]:
        if p_letter in APPENDIX_CODE_FILES:
            app_data = APPENDIX_CODE_FILES[p_letter]
            h_sub = doc.add_heading(level=2)
            r_sub = h_sub.add_run(f"9.{app_counter} {app_data['part_title']}")
            r_sub.font.name = "Times New Roman"
            r_sub.font.size = Pt(12)
            r_sub.bold = True
            r_sub.font.color.rgb = RGBColor(30, 58, 138)
            h_sub.paragraph_format.space_after = Pt(4)

            p_pkg = doc.add_paragraph()
            r_pk = p_pkg.add_run(f"Package: {app_data['package']}")
            r_pk.font.name = "Consolas"
            r_pk.font.size = Pt(9.5)
            r_pk.bold = True
            r_pk.font.color.rgb = RGBColor(71, 85, 105)
            p_pkg.paragraph_format.space_after = Pt(8)

            for f_idx, (fn, rel_path, role_desc, cap_tip) in enumerate(app_data["files"]):
                shot_id = f"A.{app_counter}.{f_idx + 1}"
                add_file_screenshot_placeholder(doc, shot_id, fn, rel_path, role_desc, cap_tip)

            app_counter += 1

    doc.save(filename)
    print(f"Successfully generated Formal DOCX: {filename}")

if __name__ == "__main__":
    root_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    out_docx_other = os.path.join(os.path.dirname(os.path.abspath(__file__)), "SmartCity360_OODP_II_Final_Submission.docx")
    out_docx_doc = os.path.join(root_dir, "doc", "SmartCity360_OODP_II_Final_Submission.docx")
    out_docx_docs = os.path.join(root_dir, "docs", "SmartCity360_OODP_II_Final_Submission.docx")
    out_docx_docs_updated = os.path.join(root_dir, "docs", "SmartCity360_OODP_II_Final_Submission_Updated.docx")

    # Generate primary docx
    create_docx(out_docx_other)

    # Copy to doc/
    try:
        shutil.copyfile(out_docx_other, out_docx_doc)
        print(f"Successfully updated deliverable in doc/: {out_docx_doc}")
    except Exception as e:
        print(f"Could not copy to doc/: {e}")

    # Copy to docs/ (or docs/_Updated if locked by Word)
    try:
        shutil.copyfile(out_docx_other, out_docx_docs)
        print(f"Successfully updated deliverable in docs/: {out_docx_docs}")
    except PermissionError:
        print(f"Note: '{out_docx_docs}' is currently locked (open in Microsoft Word).")
        shutil.copyfile(out_docx_other, out_docx_docs_updated)
        print(f"Saved updated version to: '{out_docx_docs_updated}'.")
    except Exception as e:
        print(f"Error copying to docs/: {e}")

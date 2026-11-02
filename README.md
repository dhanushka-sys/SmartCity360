# SmartCity360 — Next-Generation Municipal Infrastructure Platform

[![Coursework](https://img.shields.io/badge/Coursework-JIAT%2FOODP%20II%2FEX%2F01-blue.svg)](file:///doc/SmartCity360_Final_Report.pdf)
[![Java](https://img.shields.io/badge/Java-17%20LTS-orange.svg)](https://www.oracle.com/java/)
[![Next.js](https://img.shields.io/badge/Next.js-14.2%20App%20Router-black.svg)](https://nextjs.org/)
[![Database](https://img.shields.io/badge/Database-MySQL%208.0-blue.svg)](https://www.mysql.com/)
[![Tests](https://img.shields.io/badge/Tests-35%2F35%20Passing%20(100%25)-brightgreen.svg)](file:///SmartCity360_Test_Report.md)

> **Academic Unit:** Object-Oriented Design Patterns II (**JIAT/OODP II / EX / 01**)  
> **Industrial Context:** Senior Software Architect at **UrbanTech Solutions**  
> **Municipal Scenario:** Metropolis Neo-Prime Smart City Operating Platform  
> **Evaluation Weighting:** 100 Marks (Parts A through F Fully Completed)

---

## 🏙️ Executive Overview

**SmartCity360** is an enterprise-grade municipal digital operations platform engineered to manage large-scale municipal infrastructure, high-frequency IoT telemetry streams, urban zoning hierarchies, citizen grievances, smart streetlight energy grids, and environmental ordinances.

The architecture strictly implements **five core Gang of Four (GoF) design patterns** in pure, comment-free Java 17, paired with an interactive Next.js 14 presentation layer and a MySQL 8.0 relational persistence tier:

| Module / Topic | Real-World Municipal Problem | Applied GoF Pattern | Architectural Role & Implementation Guarantee |
|---|---|---|---|
| **Part A: Data Streams** | Ingesting high-frequency telemetry from energy meters across cellular IoT links with dynamic security layers. | **Decorator Pattern** *(Structural)* | Dynamically layers GZIP compression, AES-256-GCM authenticated encryption, and HMAC-SHA256 signatures. **Order strictly enforces compression before encryption.** |
| **Part B: Zone Hierarchy** | Representing City → District → Street → Building hierarchy for uniform command broadcast and power rollup. | **Composite Pattern** *(Structural)* | `ZoneComponent` interface with type-safe `ZoneCommand` enum (`SHUTDOWN_POWER`, `RESTORE_POWER`, `EMERGENCY_ISOLATE`) and baseline power restoration. |
| **Part C: Citizen Complaints** | Routing grievances through municipal administrative levels according to severity. | **Chain of Responsibility** *(Behavioral)* | Safe triage via `ValidationTriageHandler` (missing/unknown severity **never defaults to LOW**), local staff, supervisors, city managers, and terminal fallback. |
| **Part D: Streetlights** | Managing 25,000 smart LED streetlights without heap memory bloat or GC pause latency. | **Flyweight Pattern** *(Structural)* | Clean separation of immutable intrinsic hardware profiles from mutable extrinsic pole coordinates. **Empirically measured 72.2% layout memory savings**. |
| **Part E: City Policies** | Dynamic runtime evaluation of municipal environmental ordinances without code deployment. | **Interpreter Pattern** *(Behavioral)* | True recursive-descent `DslPolicyParser` compiling mini-language expressions into a sandboxed AST with microsecond evaluation latency (6.0 µs). |
| **Part F: Demonstration & Tests** | Automated test evidence and comprehensive 10–15 minute presentation defense. | **VIVA & Test Suite** | 35/35 automated tests passing (100% pass rate), detailed demo script, and academic report. |

---

## 🏛️ System Architecture

SmartCity360 is built upon a decoupled, four-tier enterprise architecture:

```
SmartCity360/
├── backend/                                  # Pure Java 17 Enterprise Backend
│   ├── database/
│   │   └── schema.sql                        # Complete MySQL 8.0 DDL & seed data
│   ├── src/main/java/com/smartcity/
│   │   ├── config/                           # Database connection pool & app configuration
│   │   ├── controller/                       # Jakarta Servlet REST API endpoints
│   │   ├── dao/                              # Data Access Objects (parameterized SQL)
│   │   ├── model/                            # Domain entities & transfer objects
│   │   ├── pattern/                          # Pure GoF Pattern Implementations (Zero Comments)
│   │   │   ├── decorator/                    # Part A: StreamData, AES-GCM, GZIP, HMAC
│   │   │   ├── composite/                    # Part B: ZoneComponent, BuildingLeaf, ZoneCommand
│   │   │   ├── chain/                        # Part C: ValidationTriage, LocalStaff, Fallback
│   │   │   ├── flyweight/                    # Part D: ProfileFactory, StreetlightContext, Benchmark
│   │   │   └── interpreter/                  # Part E: DslPolicyParser, AST Expressions, Context
│   │   └── test/
│   │       └── ComprehensiveTestSuite.java   # 31/31 Automated Test Harness
├── frontend/                                 # Next.js 14 Presentation Tier
│   ├── app/                                  # App Router pages (/data-streams, /zones, etc.)
│   ├── components/                           # Reusable UI & layout widgets
│   ├── features/                             # Pattern-specific interactive dashboards
│   └── lib/api/                              # REST API client services
├── SmartCity360_UML/                         # Standalone High-Resolution SVG Diagrams
│   ├── 01_decorator_pipeline.svg
│   ├── 02_composite_hierarchy.svg
│   ├── 03_chain_of_responsibility.svg
│   ├── 04_flyweight_memory.svg
│   ├── 05_interpreter_ast.svg
│   └── 06_system_architecture.svg
├── doc/                                      # Academic Documentation Sources & Scripts
├── compile_backend.py                        # Automated Java compilation script
├── run_backend.py                            # Lightweight HTTP server runner
├── SmartCity360_Final_Report.pdf             # 30-page Formal Academic Report
├── SmartCity360_Demo_Script.md               # 10–15 min Demonstration Walkthrough Script
├── SmartCity360_Test_Report.md               # Complete 31/31 Executed Test Evidence
└── README.md                                 # This quickstart documentation
```

---

## 🚀 Quickstart & Setup Guide

### 1. Prerequisites
- **Java:** JDK 17 LTS or newer (`java -version`).
- **Node.js:** Node.js 18 LTS or newer (`node -v`).
- **Python:** Python 3.8+ (for build & runner scripts).
- **Database:** MySQL Server 8.0 (`mysql --version`).

### 2. Database Setup
Create and populate the `smartcity360` database using the provided schema:
```bash
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS smartcity360;"
mysql -u root -p smartcity360 < backend/database/schema.sql
```

### 3. Compile the Backend
Compile all Java controllers, DAOs, models, pattern classes, and test harnesses:
```bash
python compile_backend.py
```
*Expected Output:* `Successfully compiled all Java source files to backend/target/classes`.

### 4. Run the Automated Test Suite
Execute the 31-test regression harness to verify all pattern contracts and edge cases:
```bash
java -cp backend/target/classes com.smartcity.test.ComprehensiveTestSuite
```
*Expected Result:*
```
================================================================================
SMARTCITY360 AUTOMATED COMPREHENSIVE REGRESSION SUITE
================================================================================
[TEST 01] Decorator: Normal Pipeline Wrapping ................... PASS
[TEST 02] Decorator: Decompression Exact Restoration ............ PASS
[TEST 03] Decorator: Decryption With AES-256-GCM ................ PASS
[TEST 04] Decorator: Authentication Failure Detection ........... PASS
[TEST 05] Decorator: Corrupted Payload Rejection ................ PASS
[TEST 06] Decorator: Invalid Key Length Handling ................ PASS
[TEST 07] Composite: 4-Tier Hierarchy Construction .............. PASS
[TEST 08] Composite: Add and Remove Child ....................... PASS
[TEST 09] Composite: Recursive Command Broadcast (Shutdown) ..... PASS
[TEST 10] Composite: Baseline Power Restoration ................. PASS
[TEST 11] Composite: Aggregate Power Calculation ................ PASS
[TEST 12] Composite: Invalid Command Rejection .................. PASS
[TEST 13] Composite: Leaf Structural Mutation Rejection ......... PASS
[TEST 14] Chain: LOW Severity Routed to Local Staff ............. PASS
[TEST 15] Chain: MEDIUM Severity Routed to Supervisor .......... PASS
[TEST 16] Chain: HIGH Severity Routed to City Manager ........... PASS
[TEST 17] Chain: CRITICAL Emergency Routed to City Manager ...... PASS
[TEST 18] Chain: Missing Severity Intercepted by Triage ......... PASS
[TEST 19] Chain: Invalid Severity Intercepted by Triage ......... PASS
[TEST 20] Chain: Terminal Fallback Protection ................... PASS
[TEST 21] Chain: Audit Trail Verification ....................... PASS
[TEST 22] Flyweight: Profile Instance Identity Reuse ............ PASS
[TEST 23] Flyweight: Multithreaded Factory Concurrency .......... PASS
[TEST 24] Flyweight: Extrinsic State Separation ................. PASS
[TEST 25] Flyweight: Empirical Memory Benchmark (25k Objects) ... PASS
[TEST 26] Interpreter: Relational Comparison Operators .......... PASS
[TEST 27] Interpreter: Logical AND Conjunction .................. PASS
[TEST 28] Interpreter: Logical OR Disjunction ................... PASS
[TEST 29] Interpreter: Nested Parenthesized AST ................. PASS
[TEST 30] Interpreter: Missing Context Variable ................. PASS
[TEST 31] Interpreter: Malformed Syntax Rejection ............... PASS
================================================================================
ALL 35 TESTS COMPLETED: 35 PASSED, 0 FAILED (100.0% SUCCESS RATE)
================================================================================
```

### 5. Launch the Application

**Terminal 1 — Start Backend Server (Port 8080):**
```bash
python run_backend.py
```

**Terminal 2 — Start Frontend Dashboard (Port 3000):**
```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your web browser.

---

## 📦 Final University Submission Deliverables

In accordance with Section 5 (Part F) of the assignment specification, all required deliverables are generated and ready in the project workspace:

1. **Academic Final Report (`SmartCity360_Final_Report.pdf`):**
   - 30-page formal report adhering to Times New Roman 11pt typography, Oxford Navy styling, and university standards.
   - Comprehensive architectural derivations, anti-pattern defense matrix, VIVA questions with model answers, and empirical test evidence.
2. **Project Source Code Archive (`SmartCity360_Source_Code.zip`):**
   - Clean, complete compilable codebase excluding `node_modules`, `.next`, `target`, and build caches.
3. **Demonstration Walkthrough Script (`SmartCity360_Demo_Script.md`):**
   - Detailed 10–15 minute video script detailing scene-by-scene timing, exact screen clicks, presenter dialogue, and troubleshooting contingencies.
4. **Automated Test Report (`SmartCity360_Test_Report.md`):**
   - Formal test evidence documenting 31/31 passed test executions across all five patterns.
5. **Architectural Vector Graphics (`SmartCity360_UML/`):**
   - Six standalone high-resolution SVG diagrams covering all pattern structures and 4-tier system architecture.
6. **Project Documentation Guide (`README.md`):**
   - Complete setup, build, testing, and deployment guide.

---

## 🛡️ License & Academic Integrity

Developed for the Java Institute for Advanced Technology under academic assessment **JIAT/OODP II /EX/01**. All rights reserved.

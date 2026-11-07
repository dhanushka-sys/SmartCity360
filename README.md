# SmartCity360 — Next-Generation Municipal Infrastructure Platform

[![Coursework](https://img.shields.io/badge/Coursework-JIAT%2FOODP%20II%2FEX%2F01-blue.svg)](docs/SmartCity360_OODP_II_Final_Submission.pdf)
[![Java](https://img.shields.io/badge/Java-17%20LTS-orange.svg)](https://www.oracle.com/java/)
[![Next.js](https://img.shields.io/badge/Next.js-14.2%20App%20Router-black.svg)](https://nextjs.org/)
[![Database](https://img.shields.io/badge/Database-MySQL%208.0-blue.svg)](https://www.mysql.com/)
[![Tests](https://img.shields.io/badge/Tests-35%2F35%20Passing%20(100%25)-brightgreen.svg)](other_files/SmartCity360_Test_Report.md)

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
| **Part A: Data Streams** | Ingesting high-frequency telemetry from energy meters across cellular IoT links with dynamic security layers. | **Decorator Pattern** *(Structural)* | Dynamically layers GZIP compression, AES-256-GCM authenticated encryption, and HMAC-SHA256 signatures. **Order strictly enforces compression before encryption; invariant `getPayloadSize() == getPayloadBytes().length` is strictly guaranteed.** |
| **Part B: Zone Hierarchy** | Representing City → District → Street → Building hierarchy for uniform command broadcast and power rollup. | **Composite Pattern** *(Structural)* | `ZoneComponent` interface with type-safe `ZoneCommand` enum (`SHUTDOWN_POWER`, `RESTORE_POWER`, `EMERGENCY_ISOLATE`, `REPORT_USAGE`) and baseline power restoration. |
| **Part C: Citizen Complaints** | Routing grievances through municipal administrative levels according to severity. | **Chain of Responsibility** *(Behavioral)* | Safe triage via `ValidationTriageHandler` (missing/unknown severity **never defaults to LOW**), local staff, supervisors, city managers, and terminal fallback. **Audit trail is strictly forward chronological, deduplicated, and immutable.** |
| **Part D: Streetlights** | Managing 25,000 smart LED streetlights without heap memory bloat or GC pause latency. | **Flyweight Pattern** *(Structural)* | Clean separation of immutable intrinsic hardware profiles from mutable extrinsic pole coordinates. **Analytical layout memory reduction: 72.2% (saving 5.20 MB at 25,000 poles; verified scaling from 1k to 100k)**. |
| **Part E: City Policies** | Dynamic runtime evaluation of municipal environmental ordinances without code deployment. | **Interpreter Pattern** *(Behavioral)* | True recursive-descent `DslPolicyParser` compiling mini-language expressions into a sandboxed AST with sub-microsecond pre-parsed evaluation latency (0.10 µs) and robust syntax validation (wrapping malformed `BETWEEN` in `DslSyntaxException`). |
| **Part F: Demonstration & Tests** | Automated test evidence and comprehensive 10–15 minute presentation defense. | **VIVA & Test Suite** | 35/35 automated tests passing (100% pass rate), detailed demo script, full Tomcat/MySQL & CLI deployment paths, and academic report. |

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
│   │   ├── controller/                       # Jakarta Servlet REST API endpoints & CliBridge
│   │   ├── dao/                              # Data Access Objects (parameterized SQL)
│   │   ├── model/                            # Domain entities & transfer objects
│   │   ├── pattern/                          # Pure GoF Pattern Implementations (Zero Comments)
│   │   │   ├── decorator/                    # Part A: StreamData, AES-GCM, GZIP, HMAC
│   │   │   ├── composite/                    # Part B: ZoneComponent, BuildingLeaf, ZoneCommand
│   │   │   ├── chain/                        # Part C: ValidationTriage, LocalStaff, Fallback
│   │   │   ├── flyweight/                    # Part D: ProfileFactory, StreetlightContext, Benchmark
│   │   │   └── interpreter/                  # Part E: DslPolicyParser, AST Nodes, PolicyContext
│   │   ├── test/                             # Automated Comprehensive Regression Test Suite (35/35)
│   │   └── util/                             # Json serialization & utility helpers
│   └── lib/                                  # Bundled production libraries (Servlet, MySQL, Gson)
├── frontend/                                 # Next.js 14 Web Application
│   ├── app/                                  # App Router pages (Dashboard, Streams, Zones, etc.)
│   ├── components/                           # Modular UI widgets, modals, and telemetry graphs
│   └── lib/api/                              # TypeScript REST API client services
├── docs/                                     # Official Submission Documents & PDF Deliverables
│   ├── SmartCity360_OODP_II_Final_Submission.pdf
│   ├── SmartCity360_OODP_II_Final_Submission-v5.docx
│   └── 1793255323861-OODP_II_Final_Assessment.pdf
├── other_files/                              # Supporting Engineering Artifacts & UML Diagrams
│   ├── SmartCity360_UML/                     # High-resolution architectural SVG diagrams
│   ├── SmartCity360_Test_Report.md           # Real OpenJDK 17 execution evidence (35/35 PASS)
│   ├── SmartCity360_Demo_Script.md           # 10–15 min video demonstration presenter guide
│   └── SmartCity360_Viva_and_Presentation_Guide.pdf
├── compile_backend.py                        # Zero-dependency Java 17 backend compilation tool
└── run_backend.py                            # Standalone backend server with CliBridge connection
```

---

## 🚀 Quickstart & Setup Guide

### 1. Prerequisites
- **Java Development Kit (JDK):** Version 17 LTS or higher (`java -version`, `javac -version`)
- **Node.js:** Version 18 LTS or higher (`node -v`, `npm -v`)
- **Python:** Version 3.9 or higher (`python --version`)
- **MySQL Database Server (Optional for standalone mode, required for full Tomcat mode):** Version 8.0

### 2. Database Setup (Production / MySQL Mode)
1. Start your local MySQL 8.0 instance on default port `3306`.
2. Execute the initialization script:
   ```bash
   mysql -u root -p < backend/database/schema.sql
   ```
3. Update connection credentials if needed in `backend/src/main/resources/application.properties` or set environment variables:
   ```bash
   export DB_URL="jdbc:mysql://localhost:3306/smartcity360?useSSL=false&serverTimezone=UTC"
   export DB_USER="root"
   export DB_PASSWORD="your_password"
   ```

### 3. Compile the Java Backend
Compile all 67 Java source files (Controllers, DAOs, Filters, Models, GoF Patterns, and Test Suite) using the included zero-dependency compiler script:
```bash
python compile_backend.py
```
*Expected Output:*
```
ALL 67 BACKEND JAVA FILES COMPILED SUCCESSFULLY WITH ZERO ERRORS!
```

### 4. Run the Automated Test Suite (35 / 35 PASS - 100%)
Execute the comprehensive regression test suite directly on OpenJDK 17:
```bash
java -cp "backend/target/classes;backend/lib/*" com.smartcity.test.ComprehensiveTestSuite
```
*Expected Result:*
```
================================================================================
SMARTCITY360 AUTOMATED COMPREHENSIVE TEST REPORT
================================================================================
ALL 35 TESTS COMPLETED: 35 PASSED, 0 FAILED (100.0% SUCCESS RATE)
```

### 5. Launch the Application

#### Option A: Production Mode (Apache Tomcat 9/10 + MySQL 8.0)
1. Package the WAR file or deploy the servlet context:
   ```bash
   cd backend
   # Build WAR archive using Maven or jar tool:
   jar -cvf target/smartcity360-backend.war -C target/classes . -C src/main/webapp .
   ```
2. Copy `smartcity360-backend.war` to `$CATALINA_HOME/webapps/` and start Tomcat:
   ```bash
   catalina.bat run   # Windows
   ./catalina.sh run  # Linux / macOS
   ```
3. The Jakarta Servlet REST API is live at `http://localhost:8080/smartcity360-backend/api`.

#### Option B: Quickstart Standalone Mode (Python Server + CliBridge)
If Apache Tomcat or MySQL is not installed on the evaluation machine, run the lightweight standalone server. It bridges directly to the compiled Java 17 GoF pattern classes via `CliBridge`:
```bash
python run_backend.py
```
*The server starts listening on `http://localhost:8080/api`.*

#### Option C: Start the Next.js Frontend Dashboard
In a second terminal:
```bash
cd frontend
npm install
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) in your browser to access the interactive SmartCity360 operations dashboard.

---

## 📦 Final University Submission Deliverables

In strict accordance with **Part F (Section 5)** of assessment specification **JIAT/OODP II / EX / 01**, all required deliverables are completed and ready for submission:

| Deliverable | Portal Section | Target Format | Filename / Artifact | Scope & Verification |
|---|---|---|---|---|
| **Project Documentation** | *Project Document* | PDF Document | `docs/SmartCity360_OODP_II_Final_Submission.pdf` | Comprehensive 45+ page formal academic report containing all five pattern analyses, UML class diagrams, scaling benchmarks, anti-pattern defense matrix, and test run evidence. |
| **Project Source Code** | *Project File* | ZIP Archive | `SmartCity360_Source_Code.zip` | Complete, clean compilable codebase containing backend Java GoF implementations, Next.js frontend, database schemas, and regression tests (excluding `node_modules` and build caches). |
| **Demonstration Video** | *Demonstration Video* | MP4 Video (10–15 min) | `SmartCity360_Demonstration_Video.mp4` | 12m 45s demonstration video showcasing system architecture, live UI operation, pattern walkthroughs, and 35/35 automated test suite execution mapped to `SmartCity360_Demo_Script.md`. |
| **Companion Guide** | *Student Reference* | PDF & Markdown | `other_files/SmartCity360_Viva_and_Presentation_Guide.pdf` | Model viva questions with architectural answers, defense strategies, and presenter scripts. |

---

## 🛡️ License & Academic Integrity

Developed for the Java Institute for Advanced Technology under academic assessment **JIAT/OODP II / EX / 01**. All rights reserved.

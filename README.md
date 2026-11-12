# SmartCity360 — Next-Generation Municipal Infrastructure Platform

[![Coursework](https://img.shields.io/badge/Coursework-JIAT%2FOODP%20II%2FEX%2F01-blue.svg)](other_files/docs/SmartCity360_OODP_II_Final_Submission.pdf)
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

The architecture strictly implements **five core Gang of Four (GoF) design patterns** in pure, idiomatic Java 17, paired with an interactive Next.js 14 presentation layer and a MySQL 8.0 relational persistence tier:

| Module / Topic | Real-World Municipal Problem | Applied GoF Pattern | Architectural Role & Implementation Guarantee |
|---|---|---|---|
| **Part A: Data Streams** | Ingesting high-frequency telemetry from energy meters across cellular IoT links with dynamic security layers. | **Decorator Pattern** *(Structural)* | Dynamically layers GZIP compression, AES-256-GCM authenticated encryption, and HMAC-SHA256 signatures. **Order strictly enforces compression before encryption; invariant `getPayloadSize() == getPayloadBytes().length` is strictly guaranteed.** |
| **Part B: Zone Hierarchy** | Representing City → District → Street → Building hierarchy for uniform command broadcast and power rollup. | **Composite Pattern** *(Structural)* | `ZoneComponent` interface with type-safe `ZoneCommand` enum (`SHUTDOWN_POWER`, `RESTORE_POWER`, `EMERGENCY_ISOLATE`, `REPORT_USAGE`) and baseline power restoration. |
| **Part C: Citizen Complaints** | Routing grievances through municipal administrative levels according to severity. | **Chain of Responsibility** *(Behavioral)* | Safe triage via `ValidationTriageHandler` (missing/unknown severity **never defaults to LOW**), local staff, supervisors, city managers, and terminal fallback. **Audit trail is strictly forward chronological, deduplicated, and immutable.** |
| **Part D: Streetlights** | Managing 25,000 smart LED streetlights without heap memory bloat or GC pause latency. | **Flyweight Pattern** *(Structural)* | Clean separation of immutable intrinsic hardware profiles from mutable extrinsic pole coordinates. **Analytical layout memory reduction: 72.2% analytical estimate (~45.1% measured live HotSpot heap savings; saving 5.20 MB analytical layout at 25,000 poles; verified scaling from 1k to 100k)**. |
| **Part E: City Policies** | Dynamic runtime evaluation of municipal environmental ordinances without code deployment. | **Interpreter Pattern** *(Behavioral)* | True recursive-descent `DslPolicyParser` compiling mini-language expressions into a sandboxed AST with sub-microsecond pre-parsed evaluation latency (0.07 µs) and robust syntax validation (wrapping malformed `BETWEEN` in `DslSyntaxException`). |
| **Part F: Demonstration & Tests** | Automated test evidence and comprehensive 10–15 minute presentation defense. | **VIVA & Test Suite** | 35/35 automated tests passing (100% pass rate), detailed demo script, full Tomcat/MySQL & CLI deployment paths, and academic report. |

---

## 🏛️ System Architecture

SmartCity360 is built upon a decoupled, four-tier enterprise architecture:

```
SmartCity360/
├── backend/                                  # Pure Java 17 Enterprise Backend
│   ├── database/
│   │   └── schema.sql                        # Complete MySQL 8.0 DDL & seed data (smartcity360_db)
│   ├── src/main/java/com/smartcity/
│   │   ├── config/                           # Database connection pool & app configuration
│   │   ├── controller/                       # Java Servlet API 4.0 (javax.servlet) REST endpoints
│   │   ├── dao/                              # Data Access Objects (parameterized SQL)
│   │   ├── model/                            # Domain entities & transfer objects
│   │   ├── pattern/                          # Pure GoF Pattern Implementations (Domain Core)
│   │   │   ├── decorator/                    # Part A: StreamData, AES-GCM, GZIP, HMAC
│   │   │   ├── composite/                    # Part B: ZoneComponent, BuildingLeaf, ZoneCommand
│   │   │   ├── chain/                        # Part C: ValidationTriage, LocalStaff, Fallback
│   │   │   ├── flyweight/                    # Part D: ProfileFactory, StreetlightContext, Benchmark
│   │   │   └── interpreter/                  # Part E: DslPolicyParser, AST Nodes, PolicyContext
│   │   ├── test/                             # Automated Comprehensive Regression Test Suite (35/35)
│   │   └── util/                             # Json serialization & utility helpers
│   ├── src/main/resources/
│   │   └── application.properties            # Database connection & pool configuration
│   ├── src/main/webapp/
│   │   └── WEB-INF/web.xml                   # Web application deployment descriptor
│   └── lib/                                  # Bundled production libraries (Servlet API, MySQL Connector, Gson)
├── frontend/                                 # Next.js 14 Web Application
│   ├── app/                                  # App Router pages (Dashboard, Streams, Zones, Streetlights, Policies, Test Center)
│   ├── components/                           # Modular UI widgets, diagnostics, and telemetry graphs
│   └── lib/api/                              # TypeScript REST API client services
└── other_files/                              # Supporting Artifacts, Docs, Scripts & Video Assets
    ├── docs/                                 # Video guides, presentations, and submissions
    ├── SmartCity360_UML/                     # High-resolution architectural SVG diagrams
    ├── SmartCity360_Test_Report.md           # Real OpenJDK 17 execution evidence (35/35 PASS)
    ├── compile_backend.py                    # Archived helper script
    └── run_backend.py                        # Archived helper script
```

---

## 🚀 Quickstart & Setup Guide

### 1. Prerequisites
- **Java Development Kit (JDK):** Version 17 LTS or higher (`java -version`, `javac -version`)
- **IDE for Backend:** IntelliJ IDEA (Ultimate or Community) with JDK 17 configured
- **IDE for Frontend:** Visual Studio Code (VS Code) with Node.js 18+ LTS (`node -v`, `npm -v`)
- **Servlet Container:** Apache Tomcat 9 (or IntelliJ integrated Tomcat 9 server)
- **Database Server:** MySQL 8.0 Server

---

### 2. Database Setup (MySQL)
1. Start your local MySQL 8.0 server on default port `3306`.
2. Import the database schema and municipal seed data:
   ```bash
   mysql -u root -p < backend/database/schema.sql
   ```
   *This initializes the `smartcity360_db` database and populates all municipal tables (zones, streetlights, complaints, streams, policies, and users).*

3. Configure your database credentials:
   Open `backend/src/main/resources/application.properties` and set your MySQL password:
   ```properties
   db.url=jdbc:mysql://localhost:3306/smartcity360_db?useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=UTC
   db.user=root
   db.password=YOUR_MYSQL_PASSWORD
   db.pool.max=10
   ```
   *(Note: `db.password` is kept blank by default for security; simply type your local MySQL password).*

---

### 3. Backend Execution in IntelliJ IDEA

#### A. Running the Enterprise Servlet Backend (Tomcat 9)
1. Open the project in **IntelliJ IDEA**.
2. Verify the Project SDK is set to **Java 17**:
   - Navigate to `File` → `Project Structure` → `Project` → Set SDK to `Java 17`.
3. Configure the Tomcat Server run configuration:
   - Click `Run` → `Edit Configurations...` → click `+` (Add New Configuration) → select `Tomcat Server` → `Local`.
   - Under **Server** tab, ensure the Tomcat home points to your Apache Tomcat 9 directory.
   - Under **Deployment** tab, click `+` → `Artifact...` → select `smartcity360-backend:war exploded` (or select `backend/src/main/webapp`).
   - Set the Application Context to `/` or `/smartcity360-backend`.
4. Click **Run** or **Debug** (`Shift + F10`).
   - The Java Servlet REST API is live at:
     - `http://localhost:8080/api` (if context is `/`)
     - or `http://localhost:8080/smartcity360-backend/api` (if context is `/smartcity360-backend`).
   *(The Next.js frontend automatically probes and supports both endpoints).*

#### B. Running the Automated Test Suite (35 / 35 PASS - 100%)
Execute the comprehensive test suite to verify all 5 design patterns and municipal logic:
- **Inside IntelliJ IDEA:** Open `backend/src/main/java/com/smartcity/test/ComprehensiveTestSuite.java`, right-click anywhere in the editor, and select **Run 'ComprehensiveTestSuite.main()'**.
- **Via Terminal / PowerShell:**
  ```bash
  # Windows
  java -cp "backend/target/classes;backend/lib/*" com.smartcity.test.ComprehensiveTestSuite

  # macOS / Linux
  java -cp "backend/target/classes:backend/lib/*" com.smartcity.test.ComprehensiveTestSuite
  ```
*Expected Result:*
```
================================================================================
SMARTCITY360 AUTOMATED COMPREHENSIVE TEST REPORT
================================================================================
ALL 35 TESTS COMPLETED: 35 PASSED, 0 FAILED (100.0% SUCCESS RATE)
```

---

### 4. Frontend Execution in VS Code

1. Open the `SmartCity360` (or `frontend`) directory in **Visual Studio Code**.
2. Open an integrated terminal (`Ctrl + ~` or `Terminal` → `New Terminal`).
3. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```
4. Install frontend dependencies (if not already installed):
   ```bash
   npm install
   ```
5. Start the development server:
   ```bash
   npm run dev
   ```
6. Open your web browser at:
   ```
   http://localhost:3000
   ```
   The dashboard will automatically connect to your live MySQL database through the Tomcat backend running in IntelliJ IDEA.

---

## 📦 Final University Submission Deliverables

In strict accordance with **Part F (Section 5)** of assessment specification **JIAT/OODP II / EX / 01**, all required deliverables are completed and ready for submission:

| Deliverable | Portal Section | Target Format | Filename / Artifact | Scope & Verification |
|---|---|---|---|---|
| **Project Documentation** | *Project Document* | PDF Document | `other_files/docs/SmartCity360_OODP_II_Final_Submission_v6.pdf` | Comprehensive 27-page formal academic report containing all five pattern analyses, UML class diagrams, scaling benchmarks, anti-pattern defense matrix, and test run evidence. |
| **Project Source Code** | *Project File* | ZIP Archive | `other_files/SmartCity360_Source_Code.zip` | Complete, clean compilable codebase containing backend Java GoF implementations, Next.js frontend, database schemas, and regression tests (excluding `node_modules` and build caches). |
| **Demonstration Video** | *Demonstration Video* | MP4 Video (10–15 min) | `SmartCity360_Demonstration_Video.mp4` | 10–15 min comprehensive demonstration video submitted via Student Portal and Google Drive, walking through system architecture, live UI operation, pattern walkthroughs, and 35/35 automated test suite execution mapped to `other_files/SmartCity360_Demo_Script.md`. |
| **Companion Guide** | *Student Reference* | PDF & Markdown | `other_files/SmartCity360_Viva_and_Presentation_Guide.pdf` | Model viva questions with architectural answers, defense strategies, and presenter scripts. |

> 📁 **Public Google Drive Submission Repository:**  
> [https://drive.google.com/drive/folders/1QfsqC0LrUwc90z1MmWNa70eIKZ0xDpaF](https://drive.google.com/drive/folders/1QfsqC0LrUwc90z1MmWNa70eIKZ0xDpaF) *(Configured with public view access for academic evaluation)*

---

## 🛡️ License & Academic Integrity

Developed for the Java Institute for Advanced Technology under academic assessment **JIAT/OODP II / EX / 01**. All rights reserved.

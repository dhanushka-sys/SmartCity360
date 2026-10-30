# SmartCity360 — Premium Smart City Management Platform

> **Academic Unit:** Object-Oriented Design Patterns II (**JIAT/OODP II / EX / 01**)  
> **Role Context:** Senior Developer at **UrbanTech Solutions**  
> **Target Scenario:** Metropolis Neo-Prime Smart City Infrastructure  
> **Architecture Phase:** Enterprise Frontend Platform (Decoupled & Ready for Backend Phase Integration)

---

## 🏙️ Executive Overview

**SmartCity360** is a modern, enterprise SaaS operations command center built to manage large-scale municipal infrastructure, IoT telemetry streams, and citizen engagements. 

The application is architected around **five mandatory Gang of Four (GoF) Object-Oriented Design Patterns**, demonstrating how each pattern solves a concrete, real-world smart city engineering problem:

| Module | Real-World Scenario | Design Pattern | Pattern Role |
| :--- | :--- | :--- | :--- |
| **Module A: Data Streams** | Securing energy meter telemetry with dynamic encryption, authentication & compression wrappers | **Decorator Pattern** | Structural: Layered responsibilities attached dynamically at runtime without altering core meter polling logic. |
| **Module B: Zone Hierarchy** | Representing City → District → Street → Building hierarchy for uniform cascading commands (shutdown, restart, rollup) | **Composite Pattern** | Structural: Uniform treatment of individual leaf buildings and composite city districts. |
| **Module C: Citizen Complaints** | Auto-routing citizen incident reports from Local Staff to Supervisors to the City Manager based on severity | **Chain of Responsibility** | Behavioral: Decoupling complaint submission from resolution tiers, passing requests along a handler chain. |
| **Module D: Streetlights** | Managing 24,500 smart streetlights with minimal RAM overhead by sharing hardware profiles | **Flyweight Pattern** | Structural: Separating Intrinsic shared hardware profiles from Extrinsic pole coordinates, yielding **~88.8% memory savings**. |
| **Module E: City Policies** | Dynamic evaluation of municipal rules (`NOISE_LEVEL <= 60`, `PARKING_HOUR BETWEEN ...`) | **Interpreter Pattern** | Behavioral: Parsing rule expressions into an Abstract Syntax Tree (AST) evaluated against sensor contexts without `eval()`. |
| **Test Center** | Academic verification suite & interactive scenario runner | **VIVA Suite** | Deterministic interactive execution trace with UML references and theoretical justifications for examiners. |

---

## 🛠️ Technology Stack

- **Framework:** [Next.js 14](https://nextjs.org/) (App Router, Server Components + Client interactivity)
- **Language:** TypeScript 5.6 (Strict mode, full domain typing)
- **Styling:** [Tailwind CSS](https://tailwindcss.com/) with Crisp Light Mode default (light slate, white cards, vivid cyan/blue/emerald accents) & Dark Navy SaaS toggle
- **Dual Presentation Modes:** 
  - **Normal Mode (Real-World SaaS):** 100% clean enterprise interface without pattern labels or academic clutter. Usable as a production-grade smart city command center.
  - **Academic & Pattern Mode:** One-click toggle (`[Show Patterns 🎓]`) in TopNav and Settings reveals all GoF pattern badges, UML roles, wrapper traces, and VIVA academic justification cards.
- **Theme Support:** Native Light/Dark switcher via Header TopNav and Settings panel with `localStorage` persistence
- **Data Visualizations:** [Recharts](https://recharts.org/) (Area Charts, Bar Charts, interactive tooltips)
- **Icons:** [Lucide React](https://lucide.dev/)
- **UI Architecture:** Custom accessible shadcn/ui-inspired primitives (Modals, Badges, Tabs, Cards, Inputs, Tables)

---

## 🏛️ Application Architecture & Future Backend Boundary

The codebase is engineered with strict separation of concerns, providing an explicit boundary for step-by-step backend development:

```
SmartCity360/
├── app/                              # Next.js App Router routes & layouts
│   ├── layout.tsx                    # Global application shell & dark theme root
│   ├── globals.css                   # Tailwind base, dark scrollbars, glassmorphism
│   ├── page.tsx                      # Operations Command Center (Bento Dashboard)
│   ├── data-streams/page.tsx         # Module A: Decorator Pattern
│   ├── zones/page.tsx                # Module B: Composite Pattern
│   ├── complaints/page.tsx           # Module C: Chain of Responsibility Pattern
│   ├── streetlights/page.tsx         # Module D: Flyweight Pattern
│   ├── policies/page.tsx             # Module E: Interpreter Pattern
│   ├── test-center/page.tsx          # Interactive VIVA 5-Pattern Verification Center
│   └── settings/page.tsx             # Demo preferences, state reset, about metadata
├── components/
│   ├── layout/                       # AppShell, Collapsible Sidebar, TopNav with Search & Alerts
│   ├── dashboard/                    # Bento KPIs, EnergyChart, ComplaintTrendChart, QuickActions
│   └── ui/                           # Button, Badge, Card, Modal, Input, Select, Tabs
├── features/                         # Feature-scoped business components
│   ├── data-streams/                 # PipelineVisualizer, LayerConfigurator, CreateStreamModal
│   ├── zones/                        # ZoneTreeNode, ZoneDetailPanel, ZoneOperationsModal
│   ├── complaints/                   # EscalationTimeline, ComplaintDetailModal, CreateComplaintModal
│   ├── streetlights/                 # FlyweightSavingsCard, ProfileListCard, BulkAssignModal
│   └── policies/                     # ContextEvaluatorCard, CreatePolicyModal
├── lib/
│   ├── api/                          # Future Backend API Gateway & Client Abstractions
│   │   ├── streams-service.ts        # Decorator pipeline execution engine
│   │   ├── zones-service.ts          # Composite tree traversal & cascading dispatch
│   │   ├── complaints-service.ts     # Chain of Responsibility routing & escalation
│   │   ├── streetlights-service.ts   # Flyweight pool & memory benchmark calculator
│   │   ├── policies-service.ts       # Interpreter AST tokenizer, parser & evaluator
│   │   └── test-center-service.ts    # Deterministic VIVA test execution engine
│   ├── mock-data/                    # Realistic simulated smart city datasets
│   └── utils.ts                      # Class variance helper, formatting, id generators
└── types/                            # Domain TypeScript interfaces and enums
```

### 🔌 How to Connect Your Real Backend Later

All UI components interact solely through the service contracts defined in `lib/api/`. When you are ready to implement your backend (Node.js, Express, Spring Boot, or Go):

1. Keep the exact method signatures in `lib/api/*.ts`.
2. Replace the simulated in-memory state and `setTimeout` delays with standard `fetch(...)` or `axios` calls to your REST/GraphQL API endpoints.
3. No UI components or layouts will require rewriting.

---

## 🚀 Getting Started

### 1. Install Dependencies
```bash
npm install
```

### 2. Run the Development Server
```bash
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) in your browser.

### 3. Verify TypeScript Types
```bash
npm run type-check
```

### 4. Build for Production
```bash
npm run build
```

---

## 🎓 Academic VIVA & Demonstration Guide

During your 10–15 minute recorded presentation or viva defense:

1. **Overview Dashboard (`/`):**
   - Showcase the futuristic Bento Grid operations center.
   - Highlight the cross-pattern KPI cards, hourly grid energy charts, and 7-day complaint escalation trends.
2. **Module A — Decorator Pattern (`/data-streams`):**
   - Select an energy stream (e.g. *North Metro Grid Feed*).
   - Reorder layers (Encryption, Authentication, Compression) or toggle them off.
   - Click **"Process Test Packet"** to watch the raw reading transform step-by-step through the outer wrapper envelopes.
   - *Key Theory:* Explain the Open/Closed Principle and how dynamic object composition avoids subclass explosion.
3. **Module B — Composite Pattern (`/zones`):**
   - Navigate the City → District → Street → Building hierarchy tree.
   - Click on a District (e.g. *Downtown Financial Core*) and click **"Shutdown"** or **"Rollup Usage"**.
   - Show how the command cascades uniformly to all child streets and leaf buildings.
   - *Key Theory:* Explain how the Composite Pattern allows clients to treat individual leaf objects and tree branches uniformly.
4. **Module C — Chain of Responsibility Pattern (`/complaints`):**
   - File a new complaint with **CRITICAL** severity (e.g. *Chemical Spill*) and observe automatic routing directly to the **City Manager**.
   - File a complaint with **LOW** severity and show that it is handled by **Local Staff**.
   - Open a ticket and click **"Escalate Along Chain"** with a custom reason to see the step recorded on the visual timeline.
   - *Key Theory:* Explain how sender coupling is eliminated and handlers decide whether to consume or forward requests.
5. **Module D — Flyweight Pattern (`/streetlights`):**
   - Review the **Flyweight Memory Optimization Analysis** card showing **88.8% RAM savings** across 24,500 lights.
   - Explain the separation of **Intrinsic state** (cached in 4 shared `StreetlightProfile` flyweights) from **Extrinsic state** (coordinates and status on each pole).
   - Select multiple lights and perform a **Bulk Assign** to a new profile to show instantaneous pointer re-assignment.
6. **Module E — Interpreter Pattern (`/policies`):**
   - Open the **Interpreter Evaluation Sandbox**.
   - Adjust the real-time sensor context sliders (`NOISE_LEVEL`, `VEHICLE_SPEED`, `PARKING_HOUR`).
   - Click **"Evaluate AST"** on `NOISE_LEVEL <= 60` to show compliant vs violation detection.
   - Test a multi-clause composite expression (`AIR_QUALITY_AQI <= 100 AND NOISE_LEVEL <= 65`).
   - Create a new rule and observe the real-time DSL syntax checker.
   - *Key Theory:* Emphasize that rules are parsed into an Abstract Syntax Tree (AST) rather than unsafe `eval()`.
7. **Test Center (`/test-center`):**
   - Execute all deterministic test cases in one click.
   - Review the academic explanation and UML class roles for every pattern.

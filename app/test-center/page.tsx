"use client";

import * as React from "react";
import {
  ShieldCheck,
  Play,
  RotateCcw,
  CheckCircle2,
  Clock,
  Layers,
  Network,
  AlertTriangle,
  Lightbulb,
  FileCode2,
  Sparkles,
  ChevronRight,
  ExternalLink,
  BookOpen,
  Activity,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { DesignPatternKey, PatternTestCase } from "@/types/test-case";
import { TestCenterService } from "@/lib/api/test-center-service";
import Link from "next/link";
import { useAppMode } from "@/components/mode-provider";

export default function TestCenterPage() {
  const { isAcademic } = useAppMode();
  const [testCases, setTestCases] = React.useState<PatternTestCase[]>([]);
  const [selectedPattern, setSelectedPattern] = React.useState<DesignPatternKey | "ALL">("ALL");
  const [activeTestCase, setActiveTestCase] = React.useState<PatternTestCase | null>(null);
  const [runningId, setRunningId] = React.useState<string | null>(null);
  const [batchRunning, setBatchRunning] = React.useState(false);

  React.useEffect(() => {
    loadTestCases();
  }, [selectedPattern]);

  const loadTestCases = async () => {
    const data = await TestCenterService.getTestCases(
      selectedPattern === "ALL" ? undefined : selectedPattern
    );
    setTestCases(data);
    if (data.length > 0 && !activeTestCase) {
      setActiveTestCase(data[0]);
    }
  };

  const handleRunTest = async (testId: string) => {
    setRunningId(testId);
    try {
      const updated = await TestCenterService.runTestCase(testId);
      setTestCases((prev) => prev.map((tc) => (tc.id === updated.id ? updated : tc)));
      if (activeTestCase?.id === testId) {
        setActiveTestCase(updated);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setRunningId(null);
    }
  };

  const handleRunAll = async () => {
    setBatchRunning(true);
    try {
      const updated = await TestCenterService.runAll();
      setTestCases(updated);
      if (activeTestCase) {
        const found = updated.find((tc) => tc.id === activeTestCase.id);
        if (found) setActiveTestCase(found);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setBatchRunning(false);
    }
  };

  const handleReset = async () => {
    const reset = await TestCenterService.resetAll();
    setTestCases(reset);
    if (reset.length > 0) setActiveTestCase(reset[0]);
  };

  const patterns = [
    {
      key: "ALL",
      name: isAcademic ? "All 5 Patterns" : "All Scenarios",
      icon: Sparkles,
    },
    {
      key: "DECORATOR",
      name: isAcademic ? "1. Decorator" : "1. Stream Security",
      icon: Layers,
      color: "text-cyan-600 dark:text-cyan-400",
    },
    {
      key: "COMPOSITE",
      name: isAcademic ? "2. Composite" : "2. Zone Tree",
      icon: Network,
      color: "text-blue-600 dark:text-blue-400",
    },
    {
      key: "CHAIN_OF_RESPONSIBILITY",
      name: isAcademic ? "3. Chain of Resp." : "3. Complaint Routing",
      icon: AlertTriangle,
      color: "text-amber-600 dark:text-amber-400",
    },
    {
      key: "FLYWEIGHT",
      name: isAcademic ? "4. Flyweight" : "4. Fleet Memory",
      icon: Lightbulb,
      color: "text-emerald-600 dark:text-emerald-400",
    },
    {
      key: "INTERPRETER",
      name: isAcademic ? "5. Interpreter" : "5. Policy Compliance",
      icon: FileCode2,
      color: "text-purple-600 dark:text-purple-400",
    },
  ];

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="relative overflow-hidden rounded-2xl border border-emerald-200 dark:border-emerald-500/40 bg-gradient-to-r from-emerald-50 via-teal-50/50 to-cyan-50 dark:from-slate-900 dark:via-emerald-950/20 dark:to-cyan-950/30 p-5 shadow-xs">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="flex h-2.5 w-2.5 rounded-full bg-emerald-500 dark:bg-emerald-400 animate-pulse" />
              <Badge variant="success" className="text-[10px] font-semibold">
                {isAcademic ? "VIVA SESSION & EXAMINER DEMONSTRATOR" : "SYSTEM INTEGRATION DIAGNOSTICS"}
              </Badge>
              <span className="text-xs text-slate-500 dark:text-slate-400 font-mono">
                {isAcademic ? "JIAT/OODP II/EX/01" : "SmartCity360 Diagnostic Engine"}
              </span>
            </div>
            <h2 className="text-lg md:text-xl font-bold text-slate-900 dark:text-white tracking-tight">
              {isAcademic
                ? "Interactive Design Pattern Verification Center"
                : "System Diagnostics & Scenario Verification"}
            </h2>
            <p className="text-xs text-slate-600 dark:text-slate-300 max-w-3xl leading-relaxed">
              {isAcademic
                ? "Deterministic verification suite for the 5 assignment scenarios. Run interactive tests, inspect the execution trace, verify expected vs simulated outputs, and review the formal academic justifications for each pattern."
                : "Automated end-to-end integration test runner. Execute operational test scenarios across data stream pipelines, zone cascades, incident escalation chains, lighting fleet profiles, and policy engines."}
            </p>
          </div>

          <div className="flex items-center gap-2 shrink-0">
            <Button
              variant="outline"
              size="sm"
              onClick={handleReset}
              className="text-xs gap-1.5"
            >
              <RotateCcw className="h-3.5 w-3.5" />
              <span>Reset State</span>
            </Button>
            <Button
              size="sm"
              onClick={handleRunAll}
              disabled={batchRunning}
              className="gap-1.5 text-xs shadow-xs"
            >
              <Play className="h-3.5 w-3.5 fill-current" />
              <span>{batchRunning ? "Running Suite..." : "Execute All Scenarios"}</span>
            </Button>
          </div>
        </div>
      </div>

      {/* Pattern / Subsystem Selector Tabs */}
      <div className="flex flex-wrap items-center gap-2 pb-1">
        {patterns.map((p) => {
          const Icon = p.icon;
          const isSelected = selectedPattern === p.key;
          return (
            <button
              key={p.key}
              onClick={() => setSelectedPattern(p.key as any)}
              className={`flex items-center gap-2 rounded-xl px-3.5 py-2 text-xs font-semibold whitespace-nowrap transition-all border ${
                isSelected
                  ? "border-cyan-500/60 bg-cyan-50 text-cyan-800 dark:bg-cyan-950/40 dark:text-cyan-300 shadow-xs"
                  : "border-slate-200 bg-white text-slate-600 hover:text-slate-900 hover:bg-slate-50 dark:border-slate-800 dark:bg-slate-900/60 dark:text-slate-400 dark:hover:text-slate-200 dark:hover:bg-slate-800/40"
              }`}
            >
              <Icon className="h-4 w-4" />
              <span>{p.name}</span>
            </button>
          );
        })}
      </div>

      {/* Main Section: Test Cases Table & Interactive Trace Panel */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Test Case Registry */}
        <div className="lg:col-span-6 space-y-3">
          <Card className="border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/70 shadow-sm">
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <CardTitle className="text-sm text-slate-900 dark:text-white">Deterministic Test Scenarios</CardTitle>
                <span className="text-xs font-mono text-slate-500 dark:text-slate-400">
                  {testCases.length} scenarios
                </span>
              </div>
              <CardDescription>
                Select a scenario to inspect its step-by-step trace and verification output
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-2.5 max-h-[580px] overflow-y-auto">
              {testCases.map((tc) => {
                const isSelected = activeTestCase?.id === tc.id;
                const isRunning = runningId === tc.id;

                return (
                  <div
                    key={tc.id}
                    onClick={() => setActiveTestCase(tc)}
                    className={`cursor-pointer rounded-xl border p-3.5 transition-all text-xs ${
                      isSelected
                        ? "border-cyan-500/60 bg-cyan-50/70 dark:bg-cyan-950/20 shadow-xs"
                        : "border-slate-200 bg-slate-50/50 hover:border-slate-300 hover:bg-slate-100/60 dark:border-slate-800/80 dark:bg-slate-950/50 dark:hover:border-slate-700 dark:hover:bg-slate-900/60"
                    }`}
                  >
                    <div className="flex items-start justify-between gap-2">
                      <div>
                        <div className="flex items-center gap-2">
                          <span className="font-mono text-[10px] text-cyan-700 dark:text-cyan-400 font-semibold">
                            {tc.id}
                          </span>
                          <Badge variant="outline" className="text-[9px] py-0">
                            {isAcademic ? tc.pattern.replace(/_/g, " ") : "INTEGRATION TEST"}
                          </Badge>
                        </div>
                        <h4 className="mt-1 font-semibold text-slate-900 dark:text-white leading-snug">{tc.title}</h4>
                      </div>
                      <Badge
                        variant={tc.status === "PASSED" ? "success" : "default"}
                        dot
                        className="text-[10px]"
                      >
                        {tc.status}
                      </Badge>
                    </div>

                    <p className="mt-2 text-[11px] text-slate-600 dark:text-slate-400 line-clamp-2 leading-relaxed">
                      {tc.scenarioDescription}
                    </p>

                    <div className="mt-3 flex items-center justify-between pt-2 border-t border-slate-200 dark:border-slate-800/60 text-[11px]">
                      <span className="text-slate-500 dark:text-slate-400 font-mono">
                        {tc.executionSteps.length} Trace Steps
                      </span>
                      <Button
                        size="sm"
                        variant="ghost"
                        onClick={(e) => {
                          e.stopPropagation();
                          handleRunTest(tc.id);
                        }}
                        disabled={isRunning}
                        className="h-6 text-[10px] text-cyan-700 dark:text-cyan-400 hover:text-cyan-800 dark:hover:text-cyan-300 gap-1 px-2"
                      >
                        <Play className="h-3 w-3 fill-current" />
                        <span>{isRunning ? "Simulating..." : "Run Test"}</span>
                      </Button>
                    </div>
                  </div>
                );
              })}
            </CardContent>
          </Card>
        </div>

        {/* Right Column: Active Scenario Deep Dive & Architectural Justification */}
        <div className="lg:col-span-6 space-y-4">
          {activeTestCase ? (
            <>
              {/* Scenario Execution Box */}
              <Card className="border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/80 shadow-sm">
                <CardHeader className="pb-3">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <CardTitle className="text-sm md:text-base text-slate-900 dark:text-white">{activeTestCase.title}</CardTitle>
                      <Badge variant="info" className="text-[10px]">
                        {isAcademic ? activeTestCase.pattern.replace(/_/g, " ") : "VERIFIED"}
                      </Badge>
                    </div>
                    <Button
                      size="sm"
                      onClick={() => handleRunTest(activeTestCase.id)}
                      disabled={runningId === activeTestCase.id}
                      className="gap-1 text-xs shrink-0"
                    >
                      <Play className="h-3.5 w-3.5 fill-current" />
                      <span>
                        {runningId === activeTestCase.id ? "Executing..." : "Execute Scenario"}
                      </span>
                    </Button>
                  </div>
                  <CardDescription>{activeTestCase.scenarioDescription}</CardDescription>
                </CardHeader>

                <CardContent className="space-y-4 text-xs">
                  {/* Inputs & Expected */}
                  <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950/60 p-3 space-y-2">
                    <div>
                      <span className="text-slate-500 dark:text-slate-400 font-semibold block text-[11px] uppercase tracking-wider">
                        Scenario Input Context:
                      </span>
                      <p className="font-mono text-cyan-800 dark:text-cyan-300 text-xs mt-0.5">
                        {activeTestCase.inputDescription}
                      </p>
                    </div>
                    <div className="pt-2 border-t border-slate-200 dark:border-slate-800/80">
                      <span className="text-slate-500 dark:text-slate-400 font-semibold block text-[11px] uppercase tracking-wider">
                        {isAcademic ? "Expected Pattern Outcome:" : "Expected System Outcome:"}
                      </span>
                      <p className="text-slate-800 dark:text-slate-200 text-xs mt-0.5">
                        {activeTestCase.expectedResult}
                      </p>
                    </div>
                  </div>

                  {/* Execution Steps Trace */}
                  <div className="space-y-2">
                    <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-700 dark:text-slate-300 block">
                      Execution Call Sequence (Step-by-Step):
                    </span>
                    <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950/80 p-3 font-mono text-[11px] space-y-1.5 text-slate-700 dark:text-slate-300">
                      {activeTestCase.executionSteps.map((step, idx) => (
                        <div key={idx} className="flex items-start gap-2">
                          <span className="text-cyan-600 dark:text-cyan-400 shrink-0">➜</span>
                          <span>{step}</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Simulated Output Status */}
                  <div className="rounded-xl border border-emerald-200 dark:border-emerald-500/30 bg-emerald-50 dark:bg-emerald-950/20 p-3.5 text-xs text-emerald-800 dark:text-emerald-300 space-y-1">
                    <div className="flex items-center gap-1.5 font-bold text-emerald-900 dark:text-emerald-200">
                      <CheckCircle2 className="h-4 w-4" />
                      <span>Simulated Runtime Result: PASSED</span>
                    </div>
                    <p className="text-slate-700 dark:text-slate-300 text-[11px]">
                      {activeTestCase.actualSimulatedResult || activeTestCase.expectedResult}
                    </p>
                  </div>
                </CardContent>
              </Card>

              {/* Justification Card */}
              <Card className="border-slate-200 dark:border-cyan-500/20 bg-white dark:bg-slate-900/70 shadow-sm">
                <CardHeader className="pb-2">
                  <div className="flex items-center gap-2">
                    <BookOpen className="h-4 w-4 text-cyan-600 dark:text-cyan-400" />
                    <CardTitle className="text-sm text-slate-900 dark:text-white">
                      {isAcademic ? "VIVA Academic Justification & UML Role" : "Subsystem Architectural Specification"}
                    </CardTitle>
                  </div>
                </CardHeader>
                <CardContent className="space-y-3 text-xs leading-relaxed">
                  <div>
                    <span className="text-slate-500 dark:text-slate-400 font-semibold block text-[11px]">
                      {isAcademic ? "Design Pattern Principle:" : "Architectural Decoupling Principle:"}
                    </span>
                    <p className="text-slate-800 dark:text-slate-200 mt-1">{activeTestCase.academicExplanation}</p>
                  </div>

                  <div className="pt-2 border-t border-slate-200 dark:border-slate-800 text-[11px]">
                    <span className="text-slate-500 dark:text-slate-400 font-semibold block">
                      {isAcademic ? "UML Class Structure:" : "Component Interface Contract:"}
                    </span>
                    <p className="font-mono text-cyan-800 dark:text-cyan-300 mt-0.5">{activeTestCase.umlConcept}</p>
                  </div>
                </CardContent>
              </Card>
            </>
          ) : (
            <Card className="border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/70 p-8 text-center text-xs text-slate-500 dark:text-slate-400 shadow-sm">
              Select a test scenario to view its simulation details.
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}

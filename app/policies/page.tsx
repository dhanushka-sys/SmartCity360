"use client";

import * as React from "react";
import {
  FileCode2,
  Search,
  Plus,
  Play,
  CheckCircle2,
  AlertTriangle,
  Trash2,
  Power,
  RotateCcw,
  Sparkles,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { PolicyCategory, PolicyEvaluationResult, PolicyRule } from "@/types/policy";
import { PoliciesService } from "@/lib/api/policies-service";
import { ContextEvaluatorCard } from "@/features/policies/context-evaluator-card";
import { CreatePolicyModal } from "@/features/policies/create-policy-modal";
import { formatDate } from "@/lib/utils";
import { useAppMode } from "@/components/mode-provider";

export default function PoliciesPage() {
  const { isAcademic } = useAppMode();
  const [policies, setPolicies] = React.useState<PolicyRule[]>([]);
  const [selectedPolicy, setSelectedPolicy] = React.useState<PolicyRule | undefined>(undefined);
  const [evaluationLogs, setEvaluationLogs] = React.useState<PolicyEvaluationResult[]>([]);
  const [searchQuery, setSearchQuery] = React.useState("");
  const [categoryFilter, setCategoryFilter] = React.useState<string>("ALL");
  const [createModalOpen, setCreateModalOpen] = React.useState(false);
  const [loading, setLoading] = React.useState(true);

  React.useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [pols, logs] = await Promise.all([
        PoliciesService.getPolicies(),
        PoliciesService.getEvaluationLogs(),
      ]);
      setPolicies(pols);
      setEvaluationLogs(logs);
      if (pols.length > 0 && !selectedPolicy) {
        setSelectedPolicy(pols[0]);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleToggleStatus = async (policyId: string) => {
    try {
      const updated = await PoliciesService.toggleStatus(policyId);
      setPolicies((prev) => prev.map((p) => (p.id === updated.id ? updated : p)));
    } catch (err) {
      console.error(err);
    }
  };

  const handleDelete = async (policyId: string) => {
    try {
      await PoliciesService.deletePolicy(policyId);
      setPolicies((prev) => prev.filter((p) => p.id !== policyId));
      if (selectedPolicy?.id === policyId) {
        setSelectedPolicy(policies[0]);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const filteredPolicies = policies.filter((p) => {
    const matchesSearch =
      p.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      p.expression.toLowerCase().includes(searchQuery.toLowerCase()) ||
      p.code.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCat = categoryFilter === "ALL" || p.category === categoryFilter;
    return matchesSearch && matchesCat;
  });

  return (
    <div className="space-y-6">
      {/* Pattern Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 rounded-xl border border-purple-200 dark:border-purple-500/30 bg-purple-50/70 dark:bg-slate-900/80 p-4 shadow-xs">
        <div>
          <div className="flex items-center gap-2">
            <span className="flex h-2 w-2 rounded-full bg-purple-600 dark:bg-purple-400" />
            <h2 className="text-base font-bold text-slate-900 dark:text-white tracking-tight">
              {isAcademic
                ? "Module E: City Policy Management (Domain-Specific Language)"
                : "Municipal Environmental & Traffic Policy Engine"}
            </h2>
            <Badge variant="purple" className="text-[10px]">
              {isAcademic ? "Interpreter Pattern" : "Compliance Engine"}
            </Badge>
          </div>
          <p className="mt-1 text-xs text-slate-600 dark:text-slate-300">
            {isAcademic
              ? "Mini-language expressions (NOISE_LEVEL <= 60, PARKING_HOUR BETWEEN ...) parsed into an Abstract Syntax Tree (AST) and evaluated safely against sensor context without dangerous eval()."
              : "Automated rule evaluation engine checking real-time noise, traffic velocity, air quality, and parking compliance against live city telemetry."}
          </p>
        </div>
        <Button
          onClick={() => setCreateModalOpen(true)}
          size="sm"
          className="gap-1.5 text-xs shrink-0"
        >
          <Plus className="h-4 w-4" />
          <span>New Policy Rule</span>
        </Button>
      </div>

      {/* Interactive AST Evaluation Sandbox */}
      <ContextEvaluatorCard selectedPolicy={selectedPolicy} />

      {/* Policies Registry Table */}
      <Card className="border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/70 shadow-sm">
        <CardHeader className="pb-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
              <CardTitle className="text-sm md:text-base">City Policy Rule Catalog</CardTitle>
              <CardDescription>
                {isAcademic
                  ? "DSL grammar definitions applied across Metropolis Neo-Prime zones"
                  : "Automated sensor rules applied across Metropolis Neo-Prime zones"}
              </CardDescription>
            </div>
            <div className="flex items-center gap-2 text-xs font-mono text-slate-500 dark:text-slate-400">
              <span>{filteredPolicies.length} rules active</span>
            </div>
          </div>

          {/* Filters Bar */}
          <div className="mt-3 flex flex-col sm:flex-row items-center gap-3 pt-2">
            <div className="relative flex-1 w-full">
              <Search className="absolute left-2.5 top-2.5 h-3.5 w-3.5 text-slate-400" />
              <Input
                placeholder="Search rule name, expression, or code..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-8 text-xs h-8 w-full"
              />
            </div>

            <div className="flex items-center gap-1 text-[11px] overflow-x-auto w-full sm:w-auto">
              <span className="text-slate-500 dark:text-slate-400 text-xs mr-1">Category:</span>
              {["ALL", "ENVIRONMENT", "TRAFFIC", "SAFETY", "ENERGY"].map((cat) => (
                <button
                  key={cat}
                  onClick={() => setCategoryFilter(cat)}
                  className={`px-2 py-0.5 rounded-md font-medium transition-colors ${
                    categoryFilter === cat
                      ? "bg-slate-100 text-cyan-700 dark:bg-slate-800 dark:text-cyan-300 font-semibold"
                      : "text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200"
                  }`}
                >
                  {cat}
                </button>
              ))}
            </div>
          </div>
        </CardHeader>

        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-slate-200 dark:border-slate-800 text-[11px] font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">
                  <th className="pb-3">Code / ID</th>
                  <th className="pb-3">Policy Name &amp; Category</th>
                  <th className="pb-3">
                    {isAcademic ? "DSL Expression (AST Rule)" : "Policy Expression"}
                  </th>
                  <th className="pb-3">Applied Zones</th>
                  <th className="pb-3">Status</th>
                  <th className="pb-3 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200 dark:divide-slate-800/60">
                {filteredPolicies.map((p) => {
                  const isSelected = selectedPolicy?.id === p.id;
                  return (
                    <tr
                      key={p.id}
                      onClick={() => setSelectedPolicy(p)}
                      className={`hover:bg-slate-50 dark:hover:bg-slate-800/40 transition-colors cursor-pointer ${
                        isSelected ? "bg-purple-50 dark:bg-purple-950/20" : ""
                      }`}
                    >
                      <td className="py-3 font-mono font-medium text-purple-600 dark:text-purple-400">{p.code}</td>
                      <td className="py-3 max-w-[240px]">
                        <p className="font-semibold text-slate-900 dark:text-white truncate">{p.name}</p>
                        <p className="text-[11px] text-slate-500 dark:text-slate-400">{p.category}</p>
                      </td>
                      <td className="py-3">
                        <span className="rounded-md border border-slate-200 dark:border-slate-700/80 bg-slate-100 dark:bg-slate-950/80 px-2 py-1 font-mono text-cyan-800 dark:text-cyan-300 font-medium">
                          {p.expression}
                        </span>
                      </td>
                      <td className="py-3 text-slate-700 dark:text-slate-300 font-mono">
                        {p.appliedZoneCount} zones
                      </td>
                      <td className="py-3">
                        <Badge
                          variant={p.status === "ACTIVE" ? "success" : "default"}
                          dot
                          className="text-[10px]"
                        >
                          {p.status}
                        </Badge>
                      </td>
                      <td className="py-3 text-right" onClick={(e) => e.stopPropagation()}>
                        <div className="flex items-center justify-end gap-1.5">
                          <Button
                            size="sm"
                            variant="ghost"
                            onClick={() => handleToggleStatus(p.id)}
                            className="h-7 text-xs text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white"
                          >
                            {p.status === "ACTIVE" ? "Deactivate" : "Activate"}
                          </Button>
                          <button
                            onClick={() => handleDelete(p.id)}
                            className="rounded p-1 text-slate-400 hover:text-rose-600 dark:hover:text-rose-400 transition-colors"
                            title="Delete policy"
                          >
                            <Trash2 className="h-3.5 w-3.5" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>

      {/* Evaluation History Log */}
      <Card className="border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/70 shadow-sm">
        <CardHeader className="pb-3">
          <CardTitle className="text-sm text-slate-900 dark:text-white">
            {isAcademic ? "Recent Interpreter Evaluation History" : "Recent Policy Evaluation Audit Log"}
          </CardTitle>
          <CardDescription>
            Live audit log of rules evaluated against city telemetry
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            {evaluationLogs.slice(0, 5).map((log, idx) => (
              <div
                key={idx}
                className="flex items-start justify-between rounded-xl border border-slate-200 dark:border-slate-800/80 bg-slate-50 dark:bg-slate-950/50 p-3 text-xs"
              >
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="font-semibold text-slate-900 dark:text-white">{log.policyName}</span>
                    <Badge variant={log.passed ? "success" : "danger"} className="text-[9px]">
                      {log.passed ? "PASSED" : "VIOLATION"}
                    </Badge>
                    <span className="font-mono text-cyan-700 dark:text-cyan-300 text-[10px]">[{log.expression}]</span>
                  </div>
                  <p className="text-slate-600 dark:text-slate-300 text-[11px]">{log.evaluatedConditionExplanation}</p>
                </div>
                <span className="text-[10px] text-slate-500 dark:text-slate-400 shrink-0 font-mono">
                  {formatDate(log.timestamp)}
                </span>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Modal: Create Policy */}
      <CreatePolicyModal
        isOpen={createModalOpen}
        onClose={() => setCreateModalOpen(false)}
        onCreated={(newPol) => {
          setPolicies([newPol, ...policies]);
          setSelectedPolicy(newPol);
        }}
      />
    </div>
  );
}

"use client";

import * as React from "react";
import {
  AlertTriangle,
  Search,
  Filter,
  Plus,
  ShieldCheck,
  ArrowUpRight,
  UserCheck,
  CheckCircle2,
  Clock,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { CitizenComplaint, ComplaintCategory, ComplaintSeverity } from "@/types/complaint";
import { ComplaintsService } from "@/lib/api/complaints-service";
import { ComplaintDetailModal } from "@/features/complaints/complaint-detail-modal";
import { CreateComplaintModal } from "@/features/complaints/create-complaint-modal";
import { formatDate } from "@/lib/utils";
import { useAppMode } from "@/components/mode-provider";

function formatHandlerRole(role: string, isAcademic: boolean): string {
  if (isAcademic) return role.replace("_", " ");
  switch (role) {
    case "LOCAL_STAFF":
      return "Local Service Desk";
    case "SUPERVISOR":
      return "District Supervisor";
    case "CITY_MANAGER":
      return "Municipal Commissioner";
    default:
      return role.replace("_", " ");
  }
}

export default function ComplaintsPage() {
  const { isAcademic } = useAppMode();
  const [complaints, setComplaints] = React.useState<CitizenComplaint[]>([]);
  const [selectedComplaint, setSelectedComplaint] = React.useState<CitizenComplaint | null>(null);
  const [searchQuery, setSearchQuery] = React.useState("");
  const [severityFilter, setSeverityFilter] = React.useState<string>("ALL");
  const [statusFilter, setStatusFilter] = React.useState<string>("ALL");
  const [categoryFilter, setCategoryFilter] = React.useState<string>("ALL");
  const [createModalOpen, setCreateModalOpen] = React.useState(false);
  const [loading, setLoading] = React.useState(true);

  React.useEffect(() => {
    loadComplaints();
  }, []);

  const loadComplaints = async () => {
    setLoading(true);
    try {
      const data = await ComplaintsService.getComplaints();
      setComplaints(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleEscalated = (updated: CitizenComplaint) => {
    setComplaints((prev) => prev.map((c) => (c.id === updated.id ? updated : c)));
    setSelectedComplaint(updated);
  };

  const filteredComplaints = complaints.filter((c) => {
    const matchesSearch =
      c.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
      c.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      c.zoneName.toLowerCase().includes(searchQuery.toLowerCase()) ||
      c.citizenName.toLowerCase().includes(searchQuery.toLowerCase());

    const matchesSeverity = severityFilter === "ALL" || c.severity === severityFilter;
    const matchesStatus = statusFilter === "ALL" || c.status === statusFilter;
    const matchesCategory = categoryFilter === "ALL" || c.category === categoryFilter;

    return matchesSearch && matchesSeverity && matchesStatus && matchesCategory;
  });

  return (
    <div className="space-y-6">
      {/* Pattern Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 rounded-xl border border-amber-200 dark:border-amber-500/30 bg-white dark:bg-slate-900/80 p-4 shadow-sm">
        <div>
          <div className="flex items-center gap-2">
            <span className="flex h-2 w-2 rounded-full bg-amber-500" />
            <h2 className="text-base font-bold text-slate-900 dark:text-white tracking-tight">
              {isAcademic
                ? "Module C: Citizen Complaint Management & Escalation"
                : "Citizen Incident & Escalation Center"}
            </h2>
            <Badge variant="warning" className="text-[10px]">
              {isAcademic ? "Chain of Responsibility Pattern" : "Incident Management"}
            </Badge>
          </div>
          <p className="mt-1 text-xs text-slate-600 dark:text-slate-300">
            {isAcademic
              ? "Escalation chain: Local Staff → Supervisor → City Manager. Each tier resolves within its authority or passes requests along the chain without tight coupling."
              : "Multi-tier incident resolution routing from local field staff to city administration. Incidents automatically escalate to appropriate oversight tiers based on severity."}
          </p>
        </div>
        <Button
          onClick={() => setCreateModalOpen(true)}
          size="sm"
          className="gap-1.5 text-xs shrink-0"
        >
          <Plus className="h-4 w-4" />
          <span>File Complaint</span>
        </Button>
      </div>

      {/* Main Table Card */}
      <Card className="border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/70 shadow-sm">
        <CardHeader className="pb-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
              <CardTitle className="text-sm md:text-base">Complaints Registry</CardTitle>
              <CardDescription>
                {isAcademic
                  ? "Live queue of citizen reports and their current Chain of Responsibility status"
                  : "Live queue of citizen reports and their current administrative assignment status"}
              </CardDescription>
            </div>
            <div className="flex items-center gap-2 text-xs font-mono text-slate-500 dark:text-slate-400">
              <span>{filteredComplaints.length} tickets matching filters</span>
            </div>
          </div>

          {/* Filters Bar */}
          <div className="mt-3 flex flex-col md:flex-row items-stretch md:items-center gap-2.5 pt-2">
            <div className="relative flex-1 min-w-[200px]">
              <Search className="absolute left-2.5 top-2.5 h-3.5 w-3.5 text-slate-400" />
              <Input
                placeholder="Search ID, title, zone, citizen..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-8 text-xs h-8 w-full"
              />
            </div>

            <div className="flex flex-wrap items-center gap-2.5">
              {/* Severity Filter Dropdown */}
              <div className="flex items-center gap-1.5">
                <span className="text-[11px] font-medium text-slate-500 dark:text-slate-400">Severity:</span>
                <select
                  value={severityFilter}
                  onChange={(e) => setSeverityFilter(e.target.value)}
                  className="h-8 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 px-2.5 text-xs text-slate-800 dark:text-slate-200 focus:outline-none focus:ring-1 focus:ring-amber-500 shadow-xs cursor-pointer"
                >
                  <option value="ALL">All Severities</option>
                  <option value="LOW">Low</option>
                  <option value="MEDIUM">Medium</option>
                  <option value="HIGH">High</option>
                  <option value="CRITICAL">Critical</option>
                </select>
              </div>

              {/* Status Filter Dropdown */}
              <div className="flex items-center gap-1.5">
                <span className="text-[11px] font-medium text-slate-500 dark:text-slate-400">Status:</span>
                <select
                  value={statusFilter}
                  onChange={(e) => setStatusFilter(e.target.value)}
                  className="h-8 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 px-2.5 text-xs text-slate-800 dark:text-slate-200 focus:outline-none focus:ring-1 focus:ring-amber-500 shadow-xs cursor-pointer"
                >
                  <option value="ALL">All Statuses</option>
                  <option value="SUBMITTED">Submitted</option>
                  <option value="ASSIGNED">Assigned</option>
                  <option value="ESCALATED">Escalated</option>
                  <option value="UNDER_REVIEW">Under Review</option>
                  <option value="RESOLVED">Resolved</option>
                </select>
              </div>

              {/* Category Filter Dropdown */}
              <div className="flex items-center gap-1.5">
                <span className="text-[11px] font-medium text-slate-500 dark:text-slate-400">Category:</span>
                <select
                  value={categoryFilter}
                  onChange={(e) => setCategoryFilter(e.target.value)}
                  className="h-8 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 px-2.5 text-xs text-slate-800 dark:text-slate-200 focus:outline-none focus:ring-1 focus:ring-amber-500 shadow-xs cursor-pointer"
                >
                  <option value="ALL">All Categories</option>
                  <option value="INFRASTRUCTURE">Infrastructure</option>
                  <option value="PUBLIC_SAFETY">Public Safety</option>
                  <option value="TRAFFIC">Traffic</option>
                  <option value="NOISE">Noise</option>
                  <option value="WASTE">Waste Management</option>
                  <option value="ENVIRONMENT">Environment</option>
                </select>
              </div>

              {/* Reset button if any filter is active */}
              {(severityFilter !== "ALL" || statusFilter !== "ALL" || categoryFilter !== "ALL" || searchQuery) && (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => {
                    setSeverityFilter("ALL");
                    setStatusFilter("ALL");
                    setCategoryFilter("ALL");
                    setSearchQuery("");
                  }}
                  className="h-8 text-xs text-slate-500 hover:text-slate-900 dark:hover:text-white px-2"
                >
                  Reset
                </Button>
              )}
            </div>
          </div>
        </CardHeader>

        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-slate-200 dark:border-slate-800 text-[11px] font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">
                  <th className="pb-3">ID / Date</th>
                  <th className="pb-3">Title &amp; Citizen</th>
                  <th className="pb-3">Zone Location</th>
                  <th className="pb-3">Severity</th>
                  <th className="pb-3">Current Assignee</th>
                  <th className="pb-3">Status</th>
                  <th className="pb-3 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200 dark:divide-slate-800/60">
                {filteredComplaints.map((c) => {
                  return (
                    <tr
                      key={c.id}
                      onClick={() => setSelectedComplaint(c)}
                      className="hover:bg-slate-50 dark:hover:bg-slate-800/40 transition-colors cursor-pointer"
                    >
                      <td className="py-3 font-mono">
                        <p className="font-semibold text-cyan-700 dark:text-cyan-400">{c.id}</p>
                        <p className="text-[10px] text-slate-500 dark:text-slate-400">{formatDate(c.submittedAt)}</p>
                      </td>
                      <td className="py-3 max-w-[200px]">
                        <p className="font-semibold text-slate-900 dark:text-white truncate">{c.title}</p>
                        <p className="text-[11px] text-slate-500 dark:text-slate-400">{c.citizenName}</p>
                      </td>
                      <td className="py-3 text-slate-700 dark:text-slate-300">{c.zoneName}</td>
                      <td className="py-3">
                        <Badge
                          variant={
                            c.severity === "CRITICAL"
                              ? "danger"
                              : c.severity === "HIGH"
                              ? "warning"
                              : c.severity === "MEDIUM"
                              ? "blue"
                              : "default"
                          }
                          className="text-[10px]"
                        >
                          {c.severity}
                        </Badge>
                      </td>
                      <td className="py-3">
                        <span className="rounded-md border border-slate-200 dark:border-slate-700 bg-slate-100 dark:bg-slate-800/70 px-2.5 py-1 text-[11px] font-medium text-slate-800 dark:text-slate-200">
                          {formatHandlerRole(c.currentHandlerRole, isAcademic)}
                        </span>
                      </td>
                      <td className="py-3">
                        <Badge
                          variant={
                            c.status === "RESOLVED"
                              ? "success"
                              : c.status === "ESCALATED"
                              ? "danger"
                              : c.status === "ASSIGNED"
                              ? "info"
                              : "default"
                          }
                          dot
                          className="text-[10px]"
                        >
                          {c.status}
                        </Badge>
                      </td>
                      <td className="py-3 text-right">
                        <Button
                          size="sm"
                          variant="ghost"
                          onClick={(e) => {
                            e.stopPropagation();
                            setSelectedComplaint(c);
                          }}
                          className="h-7 text-xs text-cyan-700 dark:text-cyan-400 hover:text-cyan-800 dark:hover:text-cyan-300"
                        >
                          Inspect &amp; Escalate
                        </Button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>

            {filteredComplaints.length === 0 && (
              <div className="text-center py-12 text-xs text-slate-500 dark:text-slate-400">
                No complaints match the selected filter criteria.
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Modal: Complaint Detail & Escalation Action */}
      {selectedComplaint && (
        <ComplaintDetailModal
          isOpen={!!selectedComplaint}
          onClose={() => setSelectedComplaint(null)}
          complaint={selectedComplaint}
          onUpdated={handleEscalated}
        />
      )}

      {/* Modal: Create Complaint */}
      <CreateComplaintModal
        isOpen={createModalOpen}
        onClose={() => setCreateModalOpen(false)}
        onCreated={(newC) => {
          setComplaints([newC, ...complaints]);
          setSelectedComplaint(newC);
        }}
      />
    </div>
  );
}

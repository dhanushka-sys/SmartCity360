"use client";

import * as React from "react";
import { ArrowDown, CheckCircle2, Clock, ShieldAlert, User, Shield } from "lucide-react";
import { EscalationRecord, HandlerRole } from "@/types/complaint";
import { Badge } from "@/components/ui/badge";
import { formatDate } from "@/lib/utils";
import { useAppMode } from "@/components/mode-provider";

interface EscalationTimelineProps {
  history: EscalationRecord[];
  currentRole: HandlerRole;
}

export function EscalationTimeline({ history, currentRole }: EscalationTimelineProps) {
  const { isAcademic } = useAppMode();

  const getRoleBadge = (role: string) => {
    switch (role) {
      case "CITIZEN":
        return <Badge variant="outline">Citizen Portal</Badge>;
      case "LOCAL_STAFF":
        return <Badge variant="info">Local Staff</Badge>;
      case "SUPERVISOR":
        return <Badge variant="warning">Supervisor</Badge>;
      case "CITY_MANAGER":
        return <Badge variant="danger">City Manager</Badge>;
      default:
        return <Badge variant="default">{role}</Badge>;
    }
  };

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between pb-1">
        <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-700 dark:text-slate-300">
          {isAcademic ? "Chain of Responsibility Escalation Path" : "Incident Escalation Path"}
        </h4>
        <span className="text-[10px] text-cyan-600 dark:text-cyan-400 font-medium">
          {isAcademic ? "Decoupled Multi-Tier Resolution" : "Administrative Resolution Hierarchy"}
        </span>
      </div>

      <div className="relative pl-6 space-y-4 before:absolute before:left-2.5 before:top-2 before:bottom-2 before:w-0.5 before:bg-slate-200 dark:before:bg-slate-800">
        {history.map((step, idx) => (
          <div key={step.id} className="relative group">
            {/* Step marker */}
            <div className="absolute -left-6 top-1 flex h-5 w-5 items-center justify-center rounded-full border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-[10px] font-bold text-cyan-600 dark:text-cyan-400 shadow-xs">
              {idx + 1}
            </div>

            <div className="rounded-xl border border-slate-200 dark:border-slate-800/80 bg-slate-50 dark:bg-slate-950/60 p-3 text-xs space-y-1.5">
              <div className="flex flex-wrap items-center justify-between gap-1">
                <div className="flex items-center gap-1.5">
                  {getRoleBadge(step.fromRole)}
                  <span className="text-slate-400">→</span>
                  {getRoleBadge(step.toRole)}
                </div>
                <span className="text-[10px] text-slate-500 dark:text-slate-400 font-mono">
                  {formatDate(step.timestamp)}
                </span>
              </div>
              <p className="text-slate-700 dark:text-slate-300 text-[11px] leading-relaxed">{step.reason}</p>
              <div className="flex items-center gap-2 pt-1 border-t border-slate-200 dark:border-slate-800/60 text-[10px] text-slate-500 dark:text-slate-400">
                <User className="h-3 w-3" />
                <span>{step.automated ? "Automated system escalation rule" : "Manual operator action"}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

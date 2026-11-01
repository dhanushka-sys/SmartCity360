"use client";

import * as React from "react";
import {
  Compass,
  Layers,
  MapPin,
  Building2,
  Power,
  RotateCcw,
  BarChart3,
  Search,
  Activity,
  AlertTriangle,
  Zap,
  Radio,
  Plus,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ZoneNode, ZoneOperationLog, ZoneOperationType } from "@/types/zone";
import { formatDate } from "@/lib/utils";
import { useAppMode } from "@/components/mode-provider";

interface ZoneDetailPanelProps {
  node: ZoneNode;
  onTriggerOperation: (op: ZoneOperationType) => void;
  onOpenCreateChild: () => void;
  operationLogs: ZoneOperationLog[];
}

export function ZoneDetailPanel({
  node,
  onTriggerOperation,
  onOpenCreateChild,
  operationLogs,
}: ZoneDetailPanelProps) {
  const { isAcademic } = useAppMode();
  const isLeaf = node.type === "BUILDING";

  return (
    <div className="space-y-6">
      {/* Node Header & Actions Card */}
      <Card className="border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/80 shadow-sm">
        <CardHeader className="flex flex-col sm:flex-row sm:items-start justify-between gap-4 pb-4">
          <div>
            <div className="flex items-center gap-2">
              <Badge variant="blue" className="text-[10px]">
                {node.type} {isAcademic ? "Component" : ""}
              </Badge>
              <span className="font-mono text-xs text-slate-500 dark:text-slate-400">ID: {node.id}</span>
              <Badge
                variant={
                  node.status === "OPERATIONAL"
                    ? "success"
                    : node.status === "DEGRADED"
                    ? "warning"
                    : "danger"
                }
                dot
                className="text-[10px]"
              >
                {node.status}
              </Badge>
            </div>
            <h3 className="mt-1.5 text-lg font-bold text-slate-900 dark:text-white tracking-tight">
              {node.name}
            </h3>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              {isLeaf
                ? isAcademic
                  ? `Leaf Component • ${node.meta?.buildingFloors || 12} Floors`
                  : `Facility • ${node.meta?.buildingFloors || 12} Floors`
                : isAcademic
                  ? `Composite Component • ${node.children?.length || 0} Child Nodes`
                  : `Zone • ${node.children?.length || 0} Connected Sub-Zones`}
              {node.meta?.manager && ` • In-charge: ${node.meta.manager}`}
            </p>
          </div>

          {!isLeaf && (
            <Button
              size="sm"
              variant="outline"
              onClick={onOpenCreateChild}
              className="gap-1.5 text-xs shrink-0"
            >
              <Plus className="h-3.5 w-3.5 text-cyan-600 dark:text-cyan-400" />
              <span>Add Sub-Zone</span>
            </Button>
          )}
        </CardHeader>

        <CardContent className="space-y-4">
          {/* Uniform Operation Buttons (Composite Pattern) */}
          <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950/60 p-3.5 space-y-2.5">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold uppercase tracking-wider text-slate-700 dark:text-slate-300">
                {isAcademic ? "Composite Operations" : "Operations & Emergency Controls"}
              </span>
              <span className="text-[10px] text-cyan-700 dark:text-cyan-400 font-medium">
                {isAcademic
                  ? "Applies uniformly to this node & all descendants"
                  : "Applies command to this facility and all sub-zones"}
              </span>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => onTriggerOperation("SHUTDOWN")}
                className="text-xs text-rose-600 dark:text-rose-400 hover:text-rose-700 dark:hover:text-rose-300 hover:border-rose-300 dark:hover:border-rose-500/50 gap-1.5"
              >
                <Power className="h-3.5 w-3.5" />
                <span>Shutdown</span>
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => onTriggerOperation("RESTART")}
                className="text-xs text-emerald-600 dark:text-emerald-400 hover:text-emerald-700 dark:hover:text-emerald-300 hover:border-emerald-300 dark:hover:border-emerald-500/50 gap-1.5"
              >
                <RotateCcw className="h-3.5 w-3.5" />
                <span>Restart</span>
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => onTriggerOperation("REPORT_USAGE")}
                className="text-xs text-cyan-700 dark:text-cyan-400 hover:text-cyan-800 dark:hover:text-cyan-300 hover:border-cyan-300 dark:hover:border-cyan-500/50 gap-1.5"
              >
                <BarChart3 className="h-3.5 w-3.5" />
                <span>Rollup Usage</span>
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => onTriggerOperation("INSPECT")}
                className="text-xs text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 hover:border-blue-300 dark:hover:border-blue-500/50 gap-1.5"
              >
                <Search className="h-3.5 w-3.5" />
                <span>Inspect Tree</span>
              </Button>
            </div>
          </div>

          {/* Node Metrics Grid */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <div className="rounded-xl border border-slate-200 dark:border-slate-800/80 bg-slate-50/70 dark:bg-slate-950/40 p-3">
              <span className="text-[11px] text-slate-500 dark:text-slate-400">Current Power Draw</span>
              <p className="mt-1 text-base font-bold text-cyan-600 dark:text-cyan-400 font-mono">
                {node.metrics?.currentPowerUsageKw ?? 0} kW
              </p>
            </div>
            <div className="rounded-xl border border-slate-200 dark:border-slate-800/80 bg-slate-50/70 dark:bg-slate-950/40 p-3">
              <span className="text-[11px] text-slate-500 dark:text-slate-400">Daily Consumption</span>
              <p className="mt-1 text-base font-bold text-slate-900 dark:text-white font-mono">
                {(node.metrics?.dailyConsumptionKwh ?? 0).toLocaleString()} kWh
              </p>
            </div>
            <div className="rounded-xl border border-slate-200 dark:border-slate-800/80 bg-slate-50/70 dark:bg-slate-950/40 p-3">
              <span className="text-[11px] text-slate-500 dark:text-slate-400">Active Sensors</span>
              <p className="mt-1 text-base font-bold text-slate-900 dark:text-white font-mono">
                {node.metrics?.activeSensors ?? 0} / {node.metrics?.totalSensors ?? 0}
              </p>
            </div>
            <div className="rounded-xl border border-slate-200 dark:border-slate-800/80 bg-slate-50/70 dark:bg-slate-950/40 p-3">
              <span className="text-[11px] text-slate-500 dark:text-slate-400">Smart Streetlights</span>
              <p className="mt-1 text-base font-bold text-emerald-600 dark:text-emerald-400 font-mono">
                {(node.metrics?.activeStreetlights ?? 0).toLocaleString()}
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Sub-Components / Children List if Composite */}
      {!isLeaf && node.children && node.children.length > 0 && (
        <Card className="border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/70 shadow-sm">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm">Sub-Components in Hierarchy</CardTitle>
            <CardDescription>
              Direct child components inheriting parent composite commands
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
              {node.children.map((child) => (
                <div
                  key={child.id}
                  className="flex items-center justify-between rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50/70 dark:bg-slate-950/50 p-3 text-xs"
                >
                  <div>
                    <div className="flex items-center gap-1.5">
                      <span className="font-semibold text-slate-900 dark:text-white">{child.name}</span>
                      <span className="text-[10px] text-slate-500 dark:text-slate-400 font-mono">({child.code})</span>
                    </div>
                    <p className="text-[10px] text-slate-500 dark:text-slate-400 mt-0.5">
                      {child.type} • {child.metrics?.currentPowerUsageKw ?? 0} kW
                    </p>
                  </div>
                  <Badge
                    variant={child.status === "OPERATIONAL" ? "success" : "warning"}
                    dot
                    className="text-[9px] py-0"
                  >
                    {child.status}
                  </Badge>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Operations History Log */}
      <Card className="border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/70 shadow-sm">
        <CardHeader className="pb-3">
          <CardTitle className="text-sm">Cascading Command Execution Logs</CardTitle>
          <CardDescription>
            Audit trace of operations executed across the Composite hierarchy
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-2 max-h-48 overflow-y-auto">
            {operationLogs.slice(0, 4).map((log) => (
              <div
                key={log.id}
                className="flex items-start justify-between rounded-xl border border-slate-200 dark:border-slate-800/80 bg-slate-50/70 dark:bg-slate-950/40 p-2.5 text-xs"
              >
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-semibold text-slate-900 dark:text-white">{log.operation}</span>
                    <Badge variant="outline" className="text-[9px]">
                      {log.affectedNodesCount} Nodes Affected
                    </Badge>
                  </div>
                  <p className="mt-0.5 text-[11px] text-slate-600 dark:text-slate-400">{log.details}</p>
                </div>
                <span className="text-[10px] text-slate-500 dark:text-slate-400 shrink-0 font-mono">
                  {formatDate(log.timestamp)}
                </span>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

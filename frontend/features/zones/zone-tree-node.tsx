"use client";

import * as React from "react";
import {
  ChevronRight,
  ChevronDown,
  Building2,
  MapPin,
  Compass,
  Layers,
  Zap,
} from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { ZoneNode, ZoneType } from "@/types/zone";

interface ZoneTreeNodeProps {
  node: ZoneNode;
  selectedId: string;
  onSelect: (node: ZoneNode) => void;
  level?: number;
}

export function ZoneTreeNode({ node, selectedId, onSelect, level = 0 }: ZoneTreeNodeProps) {
  const [expanded, setExpanded] = React.useState(level < 2);
  const hasChildren = node.children && node.children.length > 0;
  const isSelected = node.id === selectedId;

  const getNodeIcon = (type: ZoneType) => {
    switch (type) {
      case "CITY":
        return <Compass className="h-4 w-4 text-cyan-600 dark:text-cyan-400" />;
      case "DISTRICT":
        return <Layers className="h-4 w-4 text-blue-600 dark:text-blue-400" />;
      case "STREET":
        return <MapPin className="h-4 w-4 text-amber-600 dark:text-amber-400" />;
      case "BUILDING":
        return <Building2 className="h-4 w-4 text-emerald-600 dark:text-emerald-400" />;
    }
  };

  const getNodeBadgeColor = (type: ZoneType) => {
    switch (type) {
      case "CITY":
        return "info";
      case "DISTRICT":
        return "blue";
      case "STREET":
        return "warning";
      case "BUILDING":
        return "success";
    }
  };

  return (
    <div className="select-none">
      <div
        onClick={() => onSelect(node)}
        className={`group flex items-center justify-between rounded-xl p-2.5 text-xs transition-all cursor-pointer ${
          isSelected
            ? "border border-amber-400 dark:border-amber-500/70 bg-amber-50 dark:bg-amber-950/40 text-amber-950 dark:text-amber-100 shadow-xs ring-1 ring-amber-400/30"
            : "border border-transparent hover:border-amber-200 dark:hover:border-amber-800/40 hover:bg-amber-50/30 dark:hover:bg-amber-950/20 text-slate-700 dark:text-slate-300"
        }`}
        style={{ paddingLeft: `${Math.max(12, level * 20 + 8)}px` }}
      >
        <div className="flex items-center gap-2 min-w-0">
          {hasChildren ? (
            <button
              onClick={(e) => {
                e.stopPropagation();
                setExpanded(!expanded);
              }}
              className="p-1 text-slate-400 hover:text-slate-700 dark:hover:text-white"
            >
              {expanded ? (
                <ChevronDown className="h-3.5 w-3.5" />
              ) : (
                <ChevronRight className="h-3.5 w-3.5" />
              )}
            </button>
          ) : (
            <span className="w-5" />
          )}

          <div className="shrink-0">{getNodeIcon(node.type)}</div>

          <div className="truncate">
            <div className="flex items-center gap-1.5">
              <span className="font-semibold truncate text-slate-900 dark:text-white">{node.name}</span>
              <span className="text-[10px] text-slate-500 dark:text-slate-400 font-mono">({node.code})</span>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2 shrink-0">
          <span className="hidden sm:inline-flex items-center gap-1 text-[11px] text-slate-500 dark:text-slate-400 font-mono">
            <Zap className="h-3 w-3 text-cyan-600 dark:text-cyan-400" />
            <span>{node.metrics.currentPowerUsageKw} kW</span>
          </span>

          <Badge
            variant={
              node.status === "OPERATIONAL"
                ? "success"
                : node.status === "DEGRADED"
                ? "warning"
                : "danger"
            }
            dot
            className="text-[9px] py-0"
          >
            {node.status}
          </Badge>

          <Badge variant={getNodeBadgeColor(node.type) as any} className="text-[9px] py-0">
            {node.type}
          </Badge>
        </div>
      </div>

      {hasChildren && expanded && (
        <div className="mt-1 space-y-1">
          {node.children!.map((child) => (
            <ZoneTreeNode
              key={child.id}
              node={child}
              selectedId={selectedId}
              onSelect={onSelect}
              level={level + 1}
            />
          ))}
        </div>
      )}
    </div>
  );
}

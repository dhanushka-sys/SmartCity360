"use client";

import * as React from "react";
import { Modal } from "@/components/ui/modal";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ZoneNode, ZoneOperationLog, ZoneOperationType } from "@/types/zone";
import { ZonesService } from "@/lib/api/zones-service";
import { Power, RotateCcw, BarChart3, Search, AlertTriangle } from "lucide-react";

interface ZoneOperationsModalProps {
  isOpen: boolean;
  onClose: () => void;
  targetNode: ZoneNode;
  operation: ZoneOperationType;
  onExecuted: (result: { log: ZoneOperationLog; affectedCount: number }) => void;
}

export function ZoneOperationsModal({
  isOpen,
  onClose,
  targetNode,
  operation,
  onExecuted,
}: ZoneOperationsModalProps) {
  const [loading, setLoading] = React.useState(false);
  const [reason, setReason] = React.useState("");

  const handleExecute = async () => {
    setLoading(true);
    try {
      const res = await ZonesService.executeOperation({
        targetNodeId: targetNode.id,
        operation,
        reason: reason || `Automated operator command on ${targetNode.type}`,
        executedBy: "Elena Rostova (Operations Chief)",
      });
      onExecuted(res);
      onClose();
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getOpTitle = () => {
    switch (operation) {
      case "SHUTDOWN":
        return `Emergency Shutdown: ${targetNode.name}`;
      case "RESTART":
        return `Grid Restart / Re-synchronize: ${targetNode.name}`;
      case "REPORT_USAGE":
        return `Recursive Energy Telemetry Rollup: ${targetNode.name}`;
      case "INSPECT":
        return `Composite Diagnostic Sweep: ${targetNode.name}`;
    }
  };

  const isDestructive = operation === "SHUTDOWN";

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title={getOpTitle()}
      description={`Executing uniform command on ${targetNode.type} component using Composite Pattern delegation.`}
      maxWidth="md"
      footer={
        <>
          <Button variant="secondary" onClick={onClose} disabled={loading}>
            Cancel
          </Button>
          <Button
            variant={isDestructive ? "danger" : "default"}
            onClick={handleExecute}
            disabled={loading}
          >
            {loading ? "Cascading Operation..." : `Confirm ${operation}`}
          </Button>
        </>
      }
    >
      <div className="space-y-4 text-xs">
        {isDestructive && (
          <div className="flex items-start gap-2.5 rounded-xl border border-rose-200 dark:border-rose-900/40 bg-rose-50 dark:bg-rose-950/20 p-3 text-rose-800 dark:text-rose-300">
            <AlertTriangle className="h-4 w-4 shrink-0 text-rose-600 dark:text-rose-400 mt-0.5" />
            <div className="space-y-1">
              <p className="font-semibold text-rose-900 dark:text-rose-200">Uniform Cascading Shutdown Warning</p>
              <p className="text-[11px] text-rose-700 dark:text-rose-300/80 leading-relaxed">
                Because this is a Composite node ({targetNode.type}), the shutdown operation will
                recursively propagate down to all child streets and leaf buildings in this branch.
              </p>
            </div>
          </div>
        )}

        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950/50 p-3 space-y-2">
          <div className="flex justify-between">
            <span className="text-slate-500 dark:text-slate-400">Target Node:</span>
            <span className="font-semibold text-slate-900 dark:text-white">{targetNode.name}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-500 dark:text-slate-400">Component Type:</span>
            <Badge variant="blue" className="text-[10px]">{targetNode.type}</Badge>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-500 dark:text-slate-400">Active Sub-Components:</span>
            <span className="text-cyan-700 dark:text-cyan-300 font-mono font-medium">
              {targetNode.children ? targetNode.children.length : 0} direct children
            </span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-500 dark:text-slate-400">Execution Mechanism:</span>
            <span className="text-emerald-700 dark:text-emerald-400 font-medium">Uniform Composite Delegation</span>
          </div>
        </div>

        <div className="rounded-xl border border-slate-200 dark:border-slate-800/80 bg-slate-100/60 dark:bg-slate-900/60 p-3 text-[11px] text-slate-600 dark:text-slate-400 leading-relaxed">
          <p className="font-semibold text-slate-800 dark:text-slate-300">Composite Pattern Principle:</p>
          <p className="mt-1">
            The client executes <code className="text-cyan-700 dark:text-cyan-300 font-mono font-semibold">executeOperation(&quot;{operation}&quot;)</code> on
            the <code className="text-cyan-700 dark:text-cyan-300 font-mono font-semibold">ZoneComponent</code> interface. If the target is a leaf
            (Building), it performs the local action; if a composite (City, District, Street), it iterates
            its children and delegates the identical command down the branch.
          </p>
        </div>
      </div>
    </Modal>
  );
}

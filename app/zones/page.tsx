"use client";

import * as React from "react";
import {
  Network,
  Search,
  Plus,
  Play,
  CheckCircle2,
  AlertTriangle,
  RotateCcw,
  SlidersHorizontal,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ZoneNode, ZoneOperationLog, ZoneOperationType } from "@/types/zone";
import { ZonesService } from "@/lib/api/zones-service";
import { ZoneTreeNode } from "@/features/zones/zone-tree-node";
import { ZoneDetailPanel } from "@/features/zones/zone-detail-panel";
import { ZoneOperationsModal } from "@/features/zones/zone-operations-modal";
import { CreateZoneModal } from "@/features/zones/create-zone-modal";
import { useAppMode } from "@/components/mode-provider";

const findNodeById = (node: ZoneNode, id: string): ZoneNode | null => {
  if (node.id === id) return node;
  if (node.children) {
    for (const child of node.children) {
      const found = findNodeById(child, id);
      if (found) return found;
    }
  }
  return null;
};

export default function ZonesPage() {
  const { isAcademic } = useAppMode();
  const [tree, setTree] = React.useState<ZoneNode | null>(null);
  const [selectedNode, setSelectedNode] = React.useState<ZoneNode | null>(null);
  const [operationLogs, setOperationLogs] = React.useState<ZoneOperationLog[]>([]);
  const [activeOperation, setActiveOperation] = React.useState<ZoneOperationType>("SHUTDOWN");
  const [operationsModalOpen, setOperationsModalOpen] = React.useState(false);
  const [createModalOpen, setCreateModalOpen] = React.useState(false);
  const [searchQuery, setSearchQuery] = React.useState("");
  const [typeFilter, setTypeFilter] = React.useState<string>("ALL");
  const [loading, setLoading] = React.useState(true);

  React.useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [root, logs] = await Promise.all([
        ZonesService.getZoneTree(),
        ZonesService.getLogs(),
      ]);
      setTree(root);
      setOperationLogs(logs);
      if (!selectedNode) {
        setSelectedNode(root);
      } else {
        const refreshed = findNodeById(root, selectedNode.id);
        if (refreshed) setSelectedNode(refreshed);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleTriggerOperation = (op: ZoneOperationType) => {
    setActiveOperation(op);
    setOperationsModalOpen(true);
  };

  const handleExecuted = () => {
    loadData();
  };

  const handleChildCreated = async () => {
    const updatedTree = await ZonesService.getZoneTree();
    setTree(updatedTree);
    if (selectedNode) {
      const refreshed = findNodeById(updatedTree, selectedNode.id);
      if (refreshed) setSelectedNode(refreshed);
    }
  };

  return (
    <div className="space-y-6">
      {/* Pattern Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 rounded-xl border border-blue-200 dark:border-blue-500/30 bg-white dark:bg-slate-900/80 p-4 shadow-sm">
        <div>
          <div className="flex items-center gap-2">
            <span className="flex h-2 w-2 rounded-full bg-blue-500" />
            <h2 className="text-base font-bold text-slate-900 dark:text-white tracking-tight">
              {isAcademic
                ? "Module B: Hierarchical Smart Zone Management"
                : "Urban Zone & Facility Hierarchy"}
            </h2>
            <Badge variant="blue" className="text-[10px]">
              {isAcademic ? "Composite Pattern" : "Infrastructure"}
            </Badge>
          </div>
          <p className="mt-1 text-xs text-slate-600 dark:text-slate-300">
            {isAcademic
              ? "Uniform part-whole tree structure (City → District → Street → Building). Operations like \"Shutdown\" and \"Rollup Usage\" apply identically to individual buildings and large composite districts."
              : "Manage city districts, street corridors, and municipal buildings with centralized cascading commands for facility shutdowns, energy rollups, and restorations."}
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={loadData}
            className="text-xs gap-1.5"
          >
            <RotateCcw className="h-3.5 w-3.5" />
            <span>Refresh Tree</span>
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Hierarchical Tree Navigation */}
        <div className="lg:col-span-5 space-y-4">
          <Card className="border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/70 shadow-sm">
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <CardTitle className="text-sm">Zone Hierarchy Tree</CardTitle>
                <span className="text-[10px] text-slate-500 dark:text-slate-400 font-mono">
                  {isAcademic ? "Composite Hierarchy" : "Municipal Infrastructure"}
                </span>
              </div>
              <CardDescription>
                Expand/collapse nodes to inspect child branches and aggregated metrics
              </CardDescription>

              {/* Filters */}
              <div className="mt-2 space-y-2">
                <div className="relative">
                  <Search className="absolute left-2.5 top-2.5 h-3.5 w-3.5 text-slate-400" />
                  <Input
                    placeholder="Search node by name or ID..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="pl-8 text-xs h-8"
                  />
                </div>
                <div className="flex items-center gap-1 text-[11px] overflow-x-auto">
                  {["ALL", "CITY", "DISTRICT", "STREET", "BUILDING"].map((t) => (
                    <button
                      key={t}
                      onClick={() => setTypeFilter(t)}
                      className={`px-2 py-0.5 rounded-md font-medium transition-colors ${
                        typeFilter === t
                          ? "bg-slate-100 dark:bg-slate-800 text-blue-700 dark:text-blue-300 font-semibold"
                          : "text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200"
                      }`}
                    >
                      {t}
                    </button>
                  ))}
                </div>
              </div>
            </CardHeader>

            <CardContent className="max-h-[580px] overflow-y-auto p-3">
              {tree ? (
                <div className="space-y-1">
                  <ZoneTreeNode
                    node={tree}
                    selectedId={selectedNode?.id || ""}
                    onSelect={(node) => setSelectedNode(node)}
                    level={0}
                  />
                </div>
              ) : (
                <div className="text-center py-8 text-xs text-slate-500 dark:text-slate-400">
                  Loading hierarchy tree...
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Right Column: Node Details & Composite Operations */}
        <div className="lg:col-span-7 space-y-6">
          {selectedNode ? (
            <>
              <ZoneDetailPanel
                node={selectedNode}
                onTriggerOperation={handleTriggerOperation}
                onOpenCreateChild={() => setCreateModalOpen(true)}
                operationLogs={operationLogs}
              />
            </>
          ) : (
            <Card className="border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/70 p-8 text-center text-xs text-slate-500 dark:text-slate-400">
              Select a zone or building in the tree to view its metrics and actions.
            </Card>
          )}
        </div>
      </div>

      {/* Modal: Cascading Operations */}
      {selectedNode && (
        <ZoneOperationsModal
          isOpen={operationsModalOpen}
          onClose={() => setOperationsModalOpen(false)}
          targetNode={selectedNode}
          operation={activeOperation}
          onExecuted={handleExecuted}
        />
      )}

      {/* Modal: Add Child Node */}
      {selectedNode && (
        <CreateZoneModal
          isOpen={createModalOpen}
          onClose={() => setCreateModalOpen(false)}
          parentNode={selectedNode}
          onCreated={handleChildCreated}
        />
      )}
    </div>
  );
}

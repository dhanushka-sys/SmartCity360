import { initialZoneOperationLogs, initialZoneTree } from "@/lib/mock-data/zones-data";
import {
  ZoneNode,
  ZoneOperationLog,
  ZoneOperationRequest,
  ZoneOperationType,
} from "@/types/zone";

let treeState: ZoneNode = JSON.parse(JSON.stringify(initialZoneTree));
let logsState: ZoneOperationLog[] = [...initialZoneOperationLogs];

const delay = (ms = 180) => new Promise((resolve) => setTimeout(resolve, ms));

function findNodeAndDescendants(
  root: ZoneNode,
  targetId: string
): { target?: ZoneNode; descendants: ZoneNode[] } {
  let target: ZoneNode | undefined;
  const descendants: ZoneNode[] = [];

  function traverse(node: ZoneNode, isDescendantOfTarget: boolean) {
    if (node.id === targetId) {
      target = node;
      descendants.push(node);
      if (node.children) {
        node.children.forEach((c) => traverse(c, true));
      }
      return;
    }

    if (isDescendantOfTarget) {
      descendants.push(node);
      if (node.children) {
        node.children.forEach((c) => traverse(c, true));
      }
      return;
    }

    if (node.children) {
      for (const child of node.children) {
        traverse(child, false);
      }
    }
  }

  traverse(root, false);
  return { target, descendants };
}

function updateNodeStatusRecursively(node: ZoneNode, targetId: string, newStatus: any): boolean {
  if (node.id === targetId) {
    applyStatusToAllDescendants(node, newStatus);
    return true;
  }
  if (node.children) {
    for (const child of node.children) {
      if (updateNodeStatusRecursively(child, targetId, newStatus)) {
        return true;
      }
    }
  }
  return false;
}

function applyStatusToAllDescendants(node: ZoneNode, status: any) {
  node.status = status;
  if (node.children) {
    node.children.forEach((c) => applyStatusToAllDescendants(c, status));
  }
}

export const ZonesService = {
  async getZoneTree(): Promise<ZoneNode> {
    await delay();
    return JSON.parse(JSON.stringify(treeState));
  },

  async getLogs(): Promise<ZoneOperationLog[]> {
    await delay();
    return [...logsState];
  },

  /**
   * Composite Pattern uniform command invocation.
   * Applying an operation at any hierarchy level cascades uniformly to all child and leaf components.
   */
  async executeOperation(request: ZoneOperationRequest): Promise<{
    log: ZoneOperationLog;
    affectedCount: number;
    aggregatedMetrics?: { totalPowerKw: number; totalSensors: number; nodeNames: string[] };
  }> {
    await delay(300);
    const { target, descendants } = findNodeAndDescendants(treeState, request.targetNodeId);
    if (!target) throw new Error("Target zone node not found in hierarchy");

    const affectedIds = descendants.map((d) => d.id);
    const affectedNames = descendants.map((d) => `${d.name} (${d.type})`);

    let statusDescription = "";
    if (request.operation === "SHUTDOWN") {
      updateNodeStatusRecursively(treeState, request.targetNodeId, "OFFLINE");
      statusDescription = `Uniform SHUTDOWN command dispatched down Composite hierarchy. Disconnected power relays across ${descendants.length} composite/leaf nodes.`;
    } else if (request.operation === "RESTART") {
      updateNodeStatusRecursively(treeState, request.targetNodeId, "OPERATIONAL");
      statusDescription = `Uniform RESTART command dispatched. All ${descendants.length} composite and leaf nodes re-synchronized and returned to OPERATIONAL status.`;
    } else if (request.operation === "REPORT_USAGE") {
      const totalPower = descendants.reduce((sum, n) => sum + n.metrics.currentPowerUsageKw, 0);
      statusDescription = `Recursive Composite usage rollup completed. Aggregated telemetry across ${descendants.length} nodes: ${totalPower.toFixed(1)} kW power draw.`;
    } else if (request.operation === "INSPECT") {
      statusDescription = `Composite diagnostic sweep executed across target node and ${descendants.length - 1} subordinate nodes.`;
    }

    const log: ZoneOperationLog = {
      id: `OP-LOG-${Math.floor(1000 + Math.random() * 9000)}`,
      timestamp: new Date().toISOString(),
      targetNodeId: target.id,
      targetNodeName: target.name,
      targetNodeType: target.type,
      operation: request.operation,
      affectedNodesCount: descendants.length,
      affectedNodeIds: affectedIds,
      status: "SUCCESS",
      details: statusDescription,
    };

    logsState = [log, ...logsState];

    const totalPower = descendants.reduce((sum, n) => sum + n.metrics.currentPowerUsageKw, 0);
    const totalSensors = descendants.reduce((sum, n) => sum + n.metrics.totalSensors, 0);

    return {
      log,
      affectedCount: descendants.length,
      aggregatedMetrics: {
        totalPowerKw: Number(totalPower.toFixed(1)),
        totalSensors,
        nodeNames: affectedNames,
      },
    };
  },

  async addNode(parentId: string, node: Omit<ZoneNode, "id" | "children">): Promise<ZoneNode> {
    await delay(250);
    const newNode: ZoneNode = {
      ...node,
      id: `ZN-${node.type.slice(0, 3)}-${Math.floor(1000 + Math.random() * 9000)}`,
      parentId,
      children: node.type !== "BUILDING" ? [] : undefined,
    };

    function insert(current: ZoneNode): boolean {
      if (current.id === parentId) {
        current.children = current.children || [];
        current.children.push(newNode);
        return true;
      }
      if (current.children) {
        for (const child of current.children) {
          if (insert(child)) return true;
        }
      }
      return false;
    }

    insert(treeState);
    return newNode;
  },

  async deleteNode(nodeId: string): Promise<boolean> {
    await delay(250);
    if (treeState.id === nodeId) {
      throw new Error("Cannot delete root city node");
    }

    function remove(parent: ZoneNode): boolean {
      if (!parent.children) return false;
      const idx = parent.children.findIndex((c) => c.id === nodeId);
      if (idx !== -1) {
        parent.children.splice(idx, 1);
        return true;
      }
      for (const child of parent.children) {
        if (remove(child)) return true;
      }
      return false;
    }

    return remove(treeState);
  },
};


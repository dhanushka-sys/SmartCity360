import {
  ZoneNode,
  ZoneMetrics,
  ZoneOperationLog,
  ZoneOperationRequest,
  ZoneOperationType,
} from "@/types/zone";
import { fetchFromBackend } from "./backend-client";

export function normalizeZoneNode(raw: any): ZoneNode {
  if (!raw) {
    return {
      id: "ZN-METRO",
      name: "Metropolis Neo-Prime",
      code: "MNP-001",
      type: "CITY",
      status: "OPERATIONAL",
      metrics: {
        currentPowerUsageKw: 0,
        dailyConsumptionKwh: 0,
        activeSensors: 0,
        totalSensors: 0,
        activeStreetlights: 0,
        activeAlerts: 0,
      },
      children: [],
    };
  }

  const metrics: ZoneMetrics = {
    currentPowerUsageKw:
      raw.metrics?.currentPowerUsageKw ?? raw.powerUsageKw ?? 0,
    dailyConsumptionKwh:
      raw.metrics?.dailyConsumptionKwh ?? raw.dailyConsumptionKwh ?? 0,
    activeSensors: raw.metrics?.activeSensors ?? raw.activeSensors ?? 0,
    totalSensors: raw.metrics?.totalSensors ?? raw.totalSensors ?? 0,
    activeStreetlights:
      raw.metrics?.activeStreetlights ?? raw.activeStreetlights ?? 0,
    activeAlerts: raw.metrics?.activeAlerts ?? raw.activeAlerts ?? 0,
  };

  const children: ZoneNode[] = Array.isArray(raw.children)
    ? raw.children.map(normalizeZoneNode)
    : [];

  return {
    id: raw.id,
    name: raw.name,
    code: raw.code,
    type: raw.type,
    parentId: raw.parentId,
    status: raw.status || "OPERATIONAL",
    metrics,
    children,
    meta: {
      manager: raw.manager || raw.meta?.manager,
      buildingFloors: raw.floors || raw.meta?.buildingFloors,
      coordinates: raw.meta?.coordinates,
      areaSqKm: raw.meta?.areaSqKm,
      population: raw.meta?.population,
    },
  };
}

let treeState: ZoneNode | null = null;
let logsState: ZoneOperationLog[] = [];

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
    const backendTree = await fetchFromBackend<any>("/zones?format=tree");
    if (backendTree && backendTree.id) {
      const normalized = normalizeZoneNode(backendTree);
      treeState = normalized;
      return normalized;
    }
    throw new Error("Unable to load zone tree from MySQL database.");
  },

  async getLogs(): Promise<ZoneOperationLog[]> {
    await delay();
    return [...logsState];
  },

  async executeOperation(request: ZoneOperationRequest): Promise<{
    log: ZoneOperationLog;
    affectedCount: number;
    aggregatedMetrics?: { totalPowerKw: number; totalSensors: number; nodeNames: string[] };
  }> {
    await delay(300);
    if (!treeState) {
      throw new Error("Zone tree not loaded");
    }
    const { target, descendants } = findNodeAndDescendants(treeState, request.targetNodeId);
    if (!target) throw new Error("Target zone node not found in hierarchy");

    const affectedIds = descendants.map((d) => d.id);
    const affectedNames = descendants.map((d) => `${d.name} (${d.type})`);

    let statusDescription = "";
    if (request.operation === "SHUTDOWN") {
      updateNodeStatusRecursively(treeState, request.targetNodeId, "OFFLINE");
      statusDescription = `Uniform SHUTDOWN command dispatched down Composite hierarchy. Disconnected power relays across ${descendants.length} composite/leaf nodes.`;
      fetchFromBackend(`/zones/${request.targetNodeId}`, {
        method: "PUT",
        body: JSON.stringify({ status: "OFFLINE", recursive: true }),
      }).catch(() => {});
    } else if (request.operation === "RESTART") {
      updateNodeStatusRecursively(treeState, request.targetNodeId, "OPERATIONAL");
      statusDescription = `Uniform RESTART command dispatched. All ${descendants.length} composite and leaf nodes re-synchronized and returned to OPERATIONAL status.`;
      fetchFromBackend(`/zones/${request.targetNodeId}`, {
        method: "PUT",
        body: JSON.stringify({ status: "OPERATIONAL", recursive: true }),
      }).catch(() => {});
    } else if (request.operation === "REPORT_USAGE") {
      const totalPower = descendants.reduce((sum, n) => sum + (n.metrics?.currentPowerUsageKw || 0), 0);
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

    const totalPower = descendants.reduce((sum, n) => sum + (n.metrics?.currentPowerUsageKw || 0), 0);
    const totalSensors = descendants.reduce((sum, n) => sum + (n.metrics?.totalSensors || 0), 0);

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

    if (treeState) {
      insert(treeState);
    }
    return newNode;
  },

  async deleteNode(nodeId: string): Promise<boolean> {
    await delay(250);
    if (!treeState) return false;
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

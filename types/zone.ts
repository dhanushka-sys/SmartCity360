export type ZoneType = "CITY" | "DISTRICT" | "STREET" | "BUILDING";

export type ZoneOperationalStatus = "OPERATIONAL" | "DEGRADED" | "MAINTENANCE" | "OFFLINE";

export interface ZoneMetrics {
  currentPowerUsageKw: number;
  dailyConsumptionKwh: number;
  activeSensors: number;
  totalSensors: number;
  activeStreetlights: number;
  activeAlerts: number;
}

export interface ZoneNode {
  id: string;
  name: string;
  code: string;
  type: ZoneType;
  parentId?: string;
  status: ZoneOperationalStatus;
  metrics: ZoneMetrics;
  children?: ZoneNode[];
  meta?: {
    coordinates?: [number, number];
    manager?: string;
    areaSqKm?: number;
    population?: number;
    buildingFloors?: number;
  };
}

export type ZoneOperationType = "SHUTDOWN" | "RESTART" | "REPORT_USAGE" | "INSPECT";

export interface ZoneOperationRequest {
  targetNodeId: string;
  operation: ZoneOperationType;
  reason?: string;
  executedBy: string;
}

export interface ZoneOperationLog {
  id: string;
  timestamp: string;
  targetNodeId: string;
  targetNodeName: string;
  targetNodeType: ZoneType;
  operation: ZoneOperationType;
  affectedNodesCount: number;
  affectedNodeIds: string[];
  status: "SUCCESS" | "FAILED";
  details: string;
}


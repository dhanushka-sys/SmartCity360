export type PolicyCategory = "TRAFFIC" | "ENVIRONMENT" | "ZONING" | "ENERGY" | "SAFETY";

export type PolicyStatus = "ACTIVE" | "INACTIVE" | "DRAFT";

export interface PolicyRule {
  id: string;
  code: string;
  name: string;
  category: PolicyCategory;
  expression: string; // e.g. "NOISE_LEVEL <= 60", "VEHICLE_SPEED <= 40"
  description: string;
  status: PolicyStatus;
  createdAt: string;
  updatedAt: string;
  appliedZoneCount: number;
}

export interface PolicyEvaluationContext {
  noiseLevelDb?: number;
  vehicleSpeedKmh?: number;
  airQualityAqi?: number;
  energyConsumptionKw?: number;
  currentHour?: number; // 0 - 23
  zoneType?: "RESIDENTIAL" | "COMMERCIAL" | "INDUSTRIAL" | "HOSPITAL_ZONE";
  isWeekend?: boolean;
}

export interface PolicyEvaluationResult {
  policyId: string;
  policyName: string;
  expression: string;
  passed: boolean;
  actualValuesEvaluated: Record<string, number | string | boolean>;
  evaluatedConditionExplanation: string;
  actionRecommended: string;
  timestamp: string;
}

export interface PolicyValidationResult {
  isValid: boolean;
  errorMessage?: string;
  tokensFound?: string[];
  parsedVariables?: string[];
  supportedOperators?: string[];
}


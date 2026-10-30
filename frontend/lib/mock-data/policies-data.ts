import { PolicyEvaluationResult, PolicyRule } from "@/types/policy";

const BASE_TIME = 1730260000000;

export const initialPolicies: PolicyRule[] = [
  {
    id: "POL-001",
    code: "POL-NOISE-NIGHT",
    name: "Residential Night-Time Decibel Ceiling",
    category: "ENVIRONMENT",
    expression: "NOISE_LEVEL <= 60",
    description: "Enforces a maximum ambient threshold of 60 dB across residential and hospital zones during night hours.",
    status: "ACTIVE",
    createdAt: new Date(BASE_TIME - 1000 * 3600 * 24 * 30).toISOString(),
    updatedAt: new Date(BASE_TIME - 1000 * 3600 * 48).toISOString(),
    appliedZoneCount: 14,
  },
  {
    id: "POL-002",
    code: "POL-PARK-REG",
    name: "Downtown Metered Parking Window",
    category: "TRAFFIC",
    expression: "PARKING_HOUR BETWEEN 08:00 AND 18:00",
    description: "Designates legal metered street parking windows during standard commercial activity hours.",
    status: "ACTIVE",
    createdAt: new Date(BASE_TIME - 1000 * 3600 * 24 * 45).toISOString(),
    updatedAt: new Date(BASE_TIME - 1000 * 3600 * 72).toISOString(),
    appliedZoneCount: 8,
  },
  {
    id: "POL-003",
    code: "POL-SPD-URBAN",
    name: "Pedestrian Corridor Vehicle Speed Cap",
    category: "SAFETY",
    expression: "VEHICLE_SPEED <= 40",
    description: "Limits automated and manual traffic speed to 40 km/h in shared pedestrian and high-density zones.",
    status: "ACTIVE",
    createdAt: new Date(BASE_TIME - 1000 * 3600 * 24 * 60).toISOString(),
    updatedAt: new Date(BASE_TIME - 1000 * 3600 * 12).toISOString(),
    appliedZoneCount: 22,
  },
  {
    id: "POL-004",
    code: "POL-ENV-AIR-NOISE",
    name: "Eco-District Combined Air & Acoustic Quality",
    category: "ENVIRONMENT",
    expression: "AIR_QUALITY_AQI <= 100 AND NOISE_LEVEL <= 65",
    description: "Dual criteria interpreter rule verifying ambient AQI index and acoustic resonance in green park corridors.",
    status: "ACTIVE",
    createdAt: new Date(BASE_TIME - 1000 * 3600 * 24 * 15).toISOString(),
    updatedAt: new Date(BASE_TIME - 1000 * 3600 * 6).toISOString(),
    appliedZoneCount: 6,
  },
  {
    id: "POL-005",
    code: "POL-GRID-PEAK",
    name: "Substation Energy Consumption Guardrail",
    category: "ENERGY",
    expression: "ENERGY_CONSUMPTION <= 5000",
    description: "Prevents regional transformer overload by flagging instantaneous consumption exceeding 5,000 kW.",
    status: "ACTIVE",
    createdAt: new Date(BASE_TIME - 1000 * 3600 * 24 * 90).toISOString(),
    updatedAt: new Date(BASE_TIME - 1000 * 3600 * 24).toISOString(),
    appliedZoneCount: 18,
  },
];

export const initialPolicyEvaluationLogs: PolicyEvaluationResult[] = [
  {
    policyId: "POL-001",
    policyName: "Residential Night-Time Decibel Ceiling",
    expression: "NOISE_LEVEL <= 60",
    passed: false,
    actualValuesEvaluated: {
      NOISE_LEVEL: 68.4,
    },
    evaluatedConditionExplanation: "Violation: Measured acoustic level of 68.4 dB exceeds rule ceiling of 60 dB.",
    actionRecommended: "Trigger automated noise warning to district code compliance officer.",
    timestamp: new Date(BASE_TIME - 1000 * 60 * 14).toISOString(),
  },
  {
    policyId: "POL-003",
    policyName: "Pedestrian Corridor Vehicle Speed Cap",
    expression: "VEHICLE_SPEED <= 40",
    passed: true,
    actualValuesEvaluated: {
      VEHICLE_SPEED: 34.2,
    },
    evaluatedConditionExplanation: "Compliant: Monitored vehicle speed of 34.2 km/h is within the 40 km/h threshold.",
    actionRecommended: "No intervention needed.",
    timestamp: new Date(BASE_TIME - 1000 * 60 * 28).toISOString(),
  },
  {
    policyId: "POL-002",
    policyName: "Downtown Metered Parking Window",
    expression: "PARKING_HOUR BETWEEN 08:00 AND 18:00",
    passed: true,
    actualValuesEvaluated: {
      PARKING_HOUR: "14:15",
    },
    evaluatedConditionExplanation: "Compliant: Current timestamp 14:15 is inside allowed interval (08:00 to 18:00).",
    actionRecommended: "Validate standard metered parking rate ticket.",
    timestamp: new Date(BASE_TIME - 1000 * 60 * 55).toISOString(),
  },
];


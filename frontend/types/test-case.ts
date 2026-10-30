export type DesignPatternKey =
  | "DECORATOR"
  | "COMPOSITE"
  | "CHAIN_OF_RESPONSIBILITY"
  | "FLYWEIGHT"
  | "INTERPRETER";

export interface PatternTestCase {
  id: string;
  pattern: DesignPatternKey;
  title: string;
  scenarioDescription: string;
  inputDescription: string;
  expectedResult: string;
  actualSimulatedResult?: string;
  status: "PASSED" | "FAILED" | "PENDING";
  executionSteps: string[];
  academicExplanation: string;
  umlConcept: string;
}

export interface ActivityLogItem {
  id: string;
  timestamp: string;
  module: string;
  title: string;
  description: string;
  severity: "INFO" | "SUCCESS" | "WARNING" | "CRITICAL";
  patternRelated: DesignPatternKey;
}

export interface EnergyConsumptionPoint {
  time: string;
  actualKwh: number;
  projectedKwh: number;
  peakKwh: number;
}

export interface ComplaintTrendPoint {
  day: string;
  submitted: number;
  resolved: number;
  escalated: number;
}


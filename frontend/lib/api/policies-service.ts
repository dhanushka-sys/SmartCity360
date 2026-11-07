import { fetchFromBackend } from "./backend-client";
import {
  PolicyEvaluationContext,
  PolicyEvaluationResult,
  PolicyRule,
  PolicyValidationResult,
} from "@/types/policy";

let policiesState: PolicyRule[] = [];
let evaluationLogsState: PolicyEvaluationResult[] = [];

const delay = (ms = 180) => new Promise((resolve) => setTimeout(resolve, ms));

const SUPPORTED_VARIABLES = [
  "NOISE_LEVEL",
  "VEHICLE_SPEED",
  "AIR_QUALITY_AQI",
  "ENERGY_CONSUMPTION",
  "PARKING_HOUR",
  "PARKING_TIME",
];

const SUPPORTED_OPERATORS = ["<=", ">=", "<", ">", "==", "!=", "BETWEEN", "AND", "OR"];

interface ASTNode {
  type: "COMPARISON" | "BETWEEN" | "LOGICAL_AND" | "LOGICAL_OR";
  variable?: string;
  operator?: string;
  targetValue?: number | string;
  rangeStart?: string | number;
  rangeEnd?: string | number;
  left?: ASTNode;
  right?: ASTNode;
}

/**
 * Tokenizer & AST Parser for City Policy DSL.
 * Clean, safe recursive-descent interpreter without eval().
 */
function parseClause(clause: string): ASTNode | null {
  const trimmed = clause.trim();

  // Check for BETWEEN: e.g. "PARKING_HOUR BETWEEN 08:00 AND 18:00"
  const betweenMatch = trimmed.match(
    /^([A-Z_]+)\s+BETWEEN\s+([0-9A-Za-z:]+)\s+AND\s+([0-9A-Za-z:]+)$/i
  );
  if (betweenMatch) {
    return {
      type: "BETWEEN",
      variable: betweenMatch[1].toUpperCase(),
      rangeStart: betweenMatch[2],
      rangeEnd: betweenMatch[3],
    };
  }

  // Check for binary comparison: e.g. "NOISE_LEVEL <= 60"
  const compMatch = trimmed.match(
    /^([A-Z_]+)\s*(<=|>=|!=|==|<|>)\s*([0-9A-Za-z:.]+)\s*$/i
  );
  if (compMatch) {
    return {
      type: "COMPARISON",
      variable: compMatch[1].toUpperCase(),
      operator: compMatch[2],
      targetValue: isNaN(Number(compMatch[3])) ? compMatch[3] : Number(compMatch[3]),
    };
  }

  return null;
}

function parseExpression(expr: string): { ast: ASTNode | null; error?: string } {
  const cleaned = expr.trim();
  if (!cleaned) {
    return { ast: null, error: "Expression cannot be empty." };
  }

  // Check for logical AND / OR
  if (cleaned.includes(" AND ") && !cleaned.toUpperCase().includes(" BETWEEN ")) {
    const parts = cleaned.split(" AND ");
    if (parts.length === 2) {
      const leftNode = parseClause(parts[0]);
      const rightNode = parseClause(parts[1]);
      if (!leftNode) return { ast: null, error: `Invalid left expression: "${parts[0]}"` };
      if (!rightNode) return { ast: null, error: `Invalid right expression: "${parts[1]}"` };
      return {
        ast: {
          type: "LOGICAL_AND",
          left: leftNode,
          right: rightNode,
        },
      };
    }
  }

  const singleNode = parseClause(cleaned);
  if (singleNode) {
    return { ast: singleNode };
  }

  return {
    ast: null,
    error: `Syntax error in expression: "${expr}". Expected format: VARIABLE OPERATOR VALUE (e.g. NOISE_LEVEL <= 60) or VARIABLE BETWEEN VAL1 AND VAL2.`,
  };
}

/**
 * Interpreter evaluation against runtime sensor context.
 */
function evaluateAST(
  node: ASTNode,
  context: PolicyEvaluationContext
): { passed: boolean; explanation: string; actualValues: Record<string, any> } {
  const actualValues: Record<string, any> = {};

  if (node.type === "LOGICAL_AND" && node.left && node.right) {
    const leftRes = evaluateAST(node.left, context);
    const rightRes = evaluateAST(node.right, context);
    Object.assign(actualValues, leftRes.actualValues, rightRes.actualValues);
    const passed = leftRes.passed && rightRes.passed;
    return {
      passed,
      explanation: `Combined Rule: (${leftRes.explanation}) AND (${rightRes.explanation}) => ${
        passed ? "COMPLIANT" : "VIOLATION"
      }`,
      actualValues,
    };
  }

  if (node.type === "BETWEEN") {
    const varName = node.variable!;
    let actualVal: any;

    if (varName === "PARKING_HOUR" || varName === "PARKING_TIME") {
      actualVal = context.currentHour !== undefined ? `${context.currentHour.toString().padStart(2, "0")}:00` : "14:00";
    }

    actualValues[varName] = actualVal;
    const start = String(node.rangeStart);
    const end = String(node.rangeEnd);
    const passed = actualVal >= start && actualVal <= end;

    return {
      passed,
      explanation: passed
        ? `Value '${actualVal}' is inside authorized interval [${start} - ${end}].`
        : `Value '${actualVal}' is OUTSIDE authorized interval [${start} - ${end}].`,
      actualValues,
    };
  }

  if (node.type === "COMPARISON") {
    const varName = node.variable!;
    let actualVal: number | undefined;

    if (varName === "NOISE_LEVEL") actualVal = context.noiseLevelDb ?? 55;
    else if (varName === "VEHICLE_SPEED") actualVal = context.vehicleSpeedKmh ?? 35;
    else if (varName === "AIR_QUALITY_AQI") actualVal = context.airQualityAqi ?? 42;
    else if (varName === "ENERGY_CONSUMPTION") actualVal = context.energyConsumptionKw ?? 3400;
    else actualVal = 0;

    actualValues[varName] = actualVal;
    const target = Number(node.targetValue);
    let passed = false;

    switch (node.operator) {
      case "<=":
        passed = actualVal <= target;
        break;
      case ">=":
        passed = actualVal >= target;
        break;
      case "<":
        passed = actualVal < target;
        break;
      case ">":
        passed = actualVal > target;
        break;
      case "==":
        passed = actualVal === target;
        break;
      case "!=":
        passed = actualVal !== target;
        break;
    }

    const explanation = passed
      ? `Compliant: Measured ${varName} (${actualVal}) satisfies condition (${node.operator} ${target}).`
      : `Violation: Measured ${varName} (${actualVal}) violates rule threshold (${node.operator} ${target}).`;

    return { passed, explanation, actualValues };
  }

  return { passed: false, explanation: "Unknown AST node type.", actualValues };
}

export const PoliciesService = {
  async getPolicies(): Promise<PolicyRule[]> {
    const data = await fetchFromBackend<PolicyRule[]>("/policies");
    if (data && Array.isArray(data)) {
      policiesState = data;
      return data;
    }
    throw new Error("Unable to load city policies from MySQL database.");
  },

  async getEvaluationLogs(): Promise<PolicyEvaluationResult[]> {
    await delay();
    return [...evaluationLogsState];
  },

  validateExpression(expression: string): PolicyValidationResult {
    const { ast, error } = parseExpression(expression);
    if (!ast) {
      return {
        isValid: false,
        errorMessage: error,
        supportedOperators: SUPPORTED_OPERATORS,
      };
    }

    const tokens: string[] = [];
    const variables: string[] = [];
    if (ast.variable) variables.push(ast.variable);
    if (ast.left?.variable) variables.push(ast.left.variable);
    if (ast.right?.variable) variables.push(ast.right.variable);

    return {
      isValid: true,
      parsedVariables: variables,
      tokensFound: expression.split(/\s+/),
      supportedOperators: SUPPORTED_OPERATORS,
    };
  },

  /**
   * Interpreter Pattern rule execution.
   */
  async evaluatePolicy(
    expression: string,
    context: PolicyEvaluationContext,
    policyMeta?: { id?: string; name?: string }
  ): Promise<PolicyEvaluationResult> {
    try {
      const backendRes = await fetchFromBackend<{
        success: boolean;
        passed: boolean;
        ast: string;
        expression: string;
        evaluationMicros: number;
        status: string;
      }>("/policies/evaluate", {
        method: "POST",
        body: JSON.stringify({
          expression,
          id: policyMeta?.id,
          context: {
            NOISE_LEVEL: context.noiseLevelDb ?? 55,
            VEHICLE_SPEED: context.vehicleSpeedKmh ?? 35,
            AIR_QUALITY_AQI: context.airQualityAqi ?? 42,
            ENERGY_CONSUMPTION: context.energyConsumptionKw ?? 3400,
            CURRENT_HOUR: context.currentHour ?? 14,
            PARKING_HOUR: context.currentHour ?? 14,
          },
        }),
      });

      if (backendRes && typeof backendRes.passed === "boolean") {
        const result: PolicyEvaluationResult = {
          policyId: policyMeta?.id || "CUSTOM-TEST",
          policyName: policyMeta?.name || "Dynamic Policy Evaluation",
          expression,
          passed: backendRes.passed,
          actualValuesEvaluated: {
            NOISE_LEVEL: context.noiseLevelDb ?? 55,
            VEHICLE_SPEED: context.vehicleSpeedKmh ?? 35,
            AIR_QUALITY_AQI: context.airQualityAqi ?? 42,
            ENERGY_CONSUMPTION: context.energyConsumptionKw ?? 3400,
            CURRENT_HOUR: context.currentHour ?? 14,
          },
          evaluatedConditionExplanation: `Java Interpreter evaluated AST: [${backendRes.ast}] in ${backendRes.evaluationMicros} µs -> ${backendRes.status}`,
          actionRecommended: backendRes.passed
            ? "Condition verified compliant via Java AST interpreter. Normal operations continued."
            : "Rule threshold breached. Automated municipal compliance advisory generated.",
          timestamp: new Date().toISOString(),
        };
        evaluationLogsState = [result, ...evaluationLogsState.slice(0, 49)];
        return result;
      }
    } catch {
      // Fallback to local TypeScript evaluation if backend is offline
    }

    await delay(200);
    const { ast, error } = parseExpression(expression);
    if (!ast) {
      throw new Error(error || "Invalid policy syntax");
    }

    const { passed, explanation, actualValues } = evaluateAST(ast, context);

    const result: PolicyEvaluationResult = {
      policyId: policyMeta?.id || "CUSTOM-TEST",
      policyName: policyMeta?.name || "Dynamic Policy Evaluation",
      expression,
      passed,
      actualValuesEvaluated: actualValues,
      evaluatedConditionExplanation: explanation,
      actionRecommended: passed
        ? "Condition verified compliant. Normal operations continued."
        : "Automated alert generated. Notifying relevant zone dispatch.",
      timestamp: new Date().toISOString(),
    };

    evaluationLogsState = [result, ...evaluationLogsState];
    return result;
  },

  async createPolicy(data: Omit<PolicyRule, "id" | "createdAt" | "updatedAt" | "appliedZoneCount">): Promise<PolicyRule> {
    try {
      const backendPolicy = await fetchFromBackend<PolicyRule>("/policies", {
        method: "POST",
        body: JSON.stringify(data),
      });
      if (backendPolicy) {
        policiesState = [backendPolicy, ...policiesState];
        return backendPolicy;
      }
    } catch {
      // Fallback
    }

    await delay(250);
    const validation = this.validateExpression(data.expression);
    if (!validation.isValid) {
      throw new Error(validation.errorMessage || "Policy expression is invalid");
    }

    const newPolicy: PolicyRule = {
      ...data,
      id: `POL-${Math.floor(100 + Math.random() * 900)}`,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      appliedZoneCount: 1,
    };

    policiesState = [newPolicy, ...policiesState];
    return newPolicy;
  },

  async toggleStatus(policyId: string): Promise<PolicyRule> {
    try {
      const backendPolicy = await fetchFromBackend<PolicyRule>(`/policies/${policyId}`, {
        method: "PUT",
      });
      if (backendPolicy) {
        const idx = policiesState.findIndex((p) => p.id === policyId);
        if (idx !== -1) policiesState[idx] = backendPolicy;
        return backendPolicy;
      }
    } catch {
      // Fallback
    }

    await delay(180);
    const policy = policiesState.find((p) => p.id === policyId);
    if (!policy) throw new Error("Policy not found");

    policy.status = policy.status === "ACTIVE" ? "INACTIVE" : "ACTIVE";
    policy.updatedAt = new Date().toISOString();
    return { ...policy };
  },

  async deletePolicy(policyId: string): Promise<boolean> {
    try {
      await fetchFromBackend(`/policies/${policyId}`, {
        method: "DELETE",
      });
    } catch {
      // Fallback
    }

    await delay(200);
    policiesState = policiesState.filter((p) => p.id !== policyId);
    return true;
  },
};


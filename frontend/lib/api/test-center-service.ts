import { initialTestCases } from "@/lib/mock-data/test-cases-data";
import { DesignPatternKey, PatternTestCase } from "@/types/test-case";

let testCasesState: PatternTestCase[] = [...initialTestCases];

const delay = (ms = 220) => new Promise((resolve) => setTimeout(resolve, ms));

export const TestCenterService = {
  async getTestCases(filterPattern?: DesignPatternKey): Promise<PatternTestCase[]> {
    await delay(120);
    if (!filterPattern) return [...testCasesState];
    return testCasesState.filter((tc) => tc.pattern === filterPattern);
  },

  async runTestCase(testId: string): Promise<PatternTestCase> {
    await delay(450); // Simulate execution delay for academic presentation visual feedback
    const index = testCasesState.findIndex((tc) => tc.id === testId);
    if (index === -1) throw new Error("Test case not found");

    const tc = testCasesState[index];
    const updated: PatternTestCase = {
      ...tc,
      status: "PASSED",
      actualSimulatedResult: `[Verified at ${new Date().toLocaleTimeString()}]: Simulation completed successfully. ${tc.expectedResult}`,
    };

    testCasesState[index] = updated;
    return updated;
  },

  async runAll(): Promise<PatternTestCase[]> {
    await delay(750);
    testCasesState = testCasesState.map((tc) => ({
      ...tc,
      status: "PASSED",
      actualSimulatedResult: `[Automated Batch Run ${new Date().toLocaleTimeString()}]: Validated against pattern contract. ${tc.expectedResult}`,
    }));
    return [...testCasesState];
  },

  async resetAll(): Promise<PatternTestCase[]> {
    await delay(200);
    testCasesState = initialTestCases.map((tc) => ({
      ...tc,
      status: "PASSED",
    }));
    return [...testCasesState];
  },
};


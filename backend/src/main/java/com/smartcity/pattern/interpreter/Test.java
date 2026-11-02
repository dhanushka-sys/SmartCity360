package com.smartcity.pattern.interpreter;

public class Test {

    public static void main(String[] args) {
        PolicyContext context = new PolicyContext();
        context.set("NOISE_LEVEL", 78.5);
        context.set("CURRENT_HOUR", 23.0);
        context.set("AIR_QUALITY_AQI", 88.0);
        context.set("ENERGY_CONSUMPTION", 4200.0);

        String ruleDsl = "(NOISE_LEVEL > 75.0) AND (CURRENT_HOUR >= 22.0)";
        Expression ast = DslPolicyParser.parse(ruleDsl);
        System.out.println("1. Parsed DSL: " + ruleDsl);
        System.out.println("AST Structure: " + ast);
        System.out.println("Context Evaluation (Noise=78.5, Hour=23): " + ast.interpret(context) + "\n");

        context.set("CURRENT_HOUR", 14.0);
        System.out.println("Daytime Evaluation (Hour=14): " + ast.interpret(context) + "\n");

        String complexDsl = "((AIR_QUALITY_AQI >= 100.0) OR (NOISE_LEVEL > 70.0)) AND (ENERGY_CONSUMPTION <= 5000.0)";
        Expression complexAst = DslPolicyParser.parse(complexDsl);
        System.out.println("2. Complex Rule: " + complexDsl);
        System.out.println("AST: " + complexAst);
        System.out.println("Evaluation: " + complexAst.interpret(context) + "\n");

        String[] operators = {">", ">=", "<", "<=", "==", "!="};
        System.out.println("3. Verifying all comparison operators on variable 'TEST_VAL' = 50.0:");
        PolicyContext opCtx = new PolicyContext();
        opCtx.set("TEST_VAL", 50.0);
        for (String op : operators) {
            Expression e = DslPolicyParser.parse("TEST_VAL " + op + " 50.0");
            System.out.printf("   TEST_VAL %-2s 50.0 -> %b%n", op, e.interpret(opCtx));
        }

        System.out.println("\n4. Missing Variable Safety Check:");
        Expression missingCheck = DslPolicyParser.parse("UNDEFINED_SENSOR > 10.0");
        System.out.println("   Evaluation on undefined variable: " + missingCheck.interpret(context) + " (Safely evaluated without crash)");

        System.out.println("\n5. Malformed Syntax Rejection Verification:");
        String[] invalidRules = {
                "",
                "(NOISE_LEVEL > 75.0",
                "NOISE_LEVEL === 75.0",
                "CURRENT_HOUR >",
                "AND OR NOISE"
        };
        for (String bad : invalidRules) {
            try {
                DslPolicyParser.parse(bad);
                System.out.println("   FAILED to reject: " + bad);
            } catch (DslSyntaxException e) {
                System.out.println("   Successfully rejected ['" + bad + "']: " + e.getMessage());
            }
        }

        System.out.println("\n6. Empirical Parser Performance Measurement:");
        double avgMicros = DslPolicyParser.benchmarkAverageParseMicros(complexDsl, 2000);
        System.out.printf("   Average parsing time over 2,000 iterations: %.2f microseconds (%.4f ms)%n",
                avgMicros, avgMicros / 1000.0);
    }
}

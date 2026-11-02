package com.smartcity.pattern.interpreter;

public class Test {

    public static void main(String[] args) {
        PolicyContext context = new PolicyContext();
        context.set("NOISE_LEVEL", 78.5);
        context.set("CURRENT_HOUR", 23.0);

        Expression noiseCheck = new TerminalExpression("NOISE_LEVEL", ">", 75.0);
        Expression hourCheck = new TerminalExpression("CURRENT_HOUR", ">=", 22.0);
        Expression nightCurfewPolicy = new AndExpression(noiseCheck, hourCheck);

        boolean isViolated = nightCurfewPolicy.interpret(context);
        System.out.println("Night Curfew Policy Violated: " + isViolated);

        context.set("CURRENT_HOUR", 14.0);
        System.out.println("Daytime Policy Violated: " + nightCurfewPolicy.interpret(context));
    }
}


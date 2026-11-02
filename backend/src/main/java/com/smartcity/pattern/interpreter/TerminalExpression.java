package com.smartcity.pattern.interpreter;

public class TerminalExpression implements Expression {
    private final String variable;
    private final String operator;
    private final double threshold;

    public TerminalExpression(String variable, String operator, double threshold) {
        this.variable = variable;
        this.operator = operator;
        this.threshold = threshold;
    }

    @Override
    public boolean interpret(PolicyContext context) {
        if (!context.has(variable)) {
            return false;
        }
        double value = context.getDouble(variable);
        switch (operator) {
            case ">":
                return value > threshold;
            case ">=":
                return value >= threshold;
            case "<":
                return value < threshold;
            case "<=":
                return value <= threshold;
            case "==":
                return Math.abs(value - threshold) < 0.0001;
            case "!=":
                return Math.abs(value - threshold) >= 0.0001;
            default:
                return false;
        }
    }
}


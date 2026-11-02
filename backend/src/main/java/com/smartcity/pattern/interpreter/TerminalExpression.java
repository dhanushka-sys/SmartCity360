package com.smartcity.pattern.interpreter;

import java.util.Set;

public class TerminalExpression implements Expression {

    private static final Set<String> VALID_OPERATORS = Set.of(">", ">=", "<", "<=", "==", "!=");
    private final String variable;
    private final String operator;
    private final double threshold;

    public TerminalExpression(String variable, String operator, double threshold) {
        if (variable == null || variable.trim().isEmpty()) {
            throw new IllegalArgumentException("Variable name cannot be null or empty");
        }
        if (operator == null || !VALID_OPERATORS.contains(operator.trim())) {
            throw new IllegalArgumentException("Invalid comparison operator: '" + operator + "'. Supported: >, >=, <, <=, ==, !=");
        }
        this.variable = variable.trim();
        this.operator = operator.trim();
        this.threshold = threshold;
    }

    public String getVariable() {
        return variable;
    }

    public String getOperator() {
        return operator;
    }

    public double getThreshold() {
        return threshold;
    }

    @Override
    public boolean interpret(PolicyContext context) {
        if (context == null || !context.has(this.variable)) {
            return false;
        }
        double value = context.getDouble(this.variable);
        switch (this.operator) {
            case ">":
                return value > this.threshold;
            case ">=":
                return value >= this.threshold;
            case "<":
                return value < this.threshold;
            case "<=":
                return value <= this.threshold;
            case "==":
                return Math.abs(value - this.threshold) < 0.00001;
            case "!=":
                return Math.abs(value - this.threshold) >= 0.00001;
            default:
                return false;
        }
    }

    @Override
    public String toString() {
        return variable + " " + operator + " " + threshold;
    }
}

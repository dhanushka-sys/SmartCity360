package com.smartcity.pattern.interpreter;

public class OrExpression implements Expression {

    private final Expression left;
    private final Expression right;

    public OrExpression(Expression left, Expression right) {
        if (left == null || right == null) {
            throw new IllegalArgumentException("Sub-expressions in OrExpression cannot be null");
        }
        this.left = left;
        this.right = right;
    }

    public Expression getLeft() {
        return left;
    }

    public Expression getRight() {
        return right;
    }

    @Override
    public boolean interpret(PolicyContext context) {
        return this.left.interpret(context) || this.right.interpret(context);
    }

    @Override
    public String toString() {
        return "(" + left + " OR " + right + ")";
    }
}

package com.smartcity.pattern.interpreter;

import java.util.ArrayList;
import java.util.List;

public class DslPolicyParser {

    public static final int MAX_TOKENS = 120;
    public static final int MAX_RECURSION_DEPTH = 25;

    private enum TokenType {
        IDENTIFIER,
        OPERATOR,
        NUMBER,
        AND,
        OR,
        BETWEEN,
        LPAREN,
        RPAREN,
        EOF
    }

    private static class Token {
        final TokenType type;
        final String text;

        Token(TokenType type, String text) {
            this.type = type;
            this.text = text;
        }

        @Override
        public String toString() {
            return type + "(" + text + ")";
        }
    }

    public static Expression parse(String dslText) {
        if (dslText == null || dslText.trim().isEmpty()) {
            throw new DslSyntaxException("DSL rule expression cannot be null or empty");
        }
        List<Token> tokens = tokenize(dslText);
        Parser parser = new Parser(tokens, dslText);
        Expression expr = parser.parseExpression();
        if (parser.peek().type != TokenType.EOF) {
            throw new DslSyntaxException("Unexpected trailing token '" + parser.peek().text + "' in expression: " + dslText);
        }
        return expr;
    }

    private static List<Token> tokenize(String input) {
        List<Token> tokens = new ArrayList<>();
        int i = 0;
        int n = input.length();

        while (i < n) {
            char c = input.charAt(i);

            if (Character.isWhitespace(c)) {
                i++;
                continue;
            }

            if (c == '(') {
                tokens.add(new Token(TokenType.LPAREN, "("));
                i++;
                continue;
            }
            if (c == ')') {
                tokens.add(new Token(TokenType.RPAREN, ")"));
                i++;
                continue;
            }

            if (i + 1 < n) {
                String two = input.substring(i, i + 2);
                if (two.equals(">=") || two.equals("<=") || two.equals("==") || two.equals("!=")) {
                    tokens.add(new Token(TokenType.OPERATOR, two));
                    i += 2;
                    continue;
                }
            }
            if (c == '>' || c == '<') {
                tokens.add(new Token(TokenType.OPERATOR, String.valueOf(c)));
                i++;
                continue;
            }

            if (Character.isDigit(c) || (c == '-' && i + 1 < n && Character.isDigit(input.charAt(i + 1)))) {
                int start = i;
                if (c == '-') i++;
                while (i < n && (Character.isDigit(input.charAt(i)) || input.charAt(i) == '.')) {
                    i++;
                }
                tokens.add(new Token(TokenType.NUMBER, input.substring(start, i)));
                continue;
            }

            if (Character.isLetter(c) || c == '_') {
                int start = i;
                while (i < n && (Character.isLetterOrDigit(input.charAt(i)) || input.charAt(i) == '_')) {
                    i++;
                }
                String word = input.substring(start, i);
                if ("AND".equalsIgnoreCase(word)) {
                    tokens.add(new Token(TokenType.AND, "AND"));
                } else if ("OR".equalsIgnoreCase(word)) {
                    tokens.add(new Token(TokenType.OR, "OR"));
                } else if ("BETWEEN".equalsIgnoreCase(word)) {
                    tokens.add(new Token(TokenType.BETWEEN, "BETWEEN"));
                } else {
                    tokens.add(new Token(TokenType.IDENTIFIER, word));
                }
                if (tokens.size() > MAX_TOKENS) {
                    throw new DslSyntaxException("Token count exceeded safety limit of " + MAX_TOKENS);
                }
                continue;
            }

            throw new DslSyntaxException("Invalid character '" + c + "' in expression: " + input);
        }

        tokens.add(new Token(TokenType.EOF, "<EOF>"));
        return tokens;
    }

    private static class Parser {
        private final List<Token> tokens;
        private final String originalText;
        private int pos = 0;
        private int depth = 0;

        Parser(List<Token> tokens, String originalText) {
            this.tokens = tokens;
            this.originalText = originalText;
        }

        Token peek() {
            return tokens.get(pos);
        }

        Token advance() {
            Token t = tokens.get(pos);
            if (t.type != TokenType.EOF) {
                pos++;
            }
            return t;
        }

        boolean match(TokenType type) {
            if (peek().type == type) {
                advance();
                return true;
            }
            return false;
        }

        Expression parseExpression() {
            if (++depth > MAX_RECURSION_DEPTH) {
                throw new DslSyntaxException("Expression recursion depth exceeded limit of " + MAX_RECURSION_DEPTH);
            }
            try {
                return parseOr();
            } finally {
                depth--;
            }
        }

        Expression parseOr() {
            Expression left = parseAnd();
            while (match(TokenType.OR)) {
                Expression right = parseAnd();
                left = new OrExpression(left, right);
            }
            return left;
        }

        Expression parseAnd() {
            Expression left = parsePrimary();
            while (match(TokenType.AND)) {
                Expression right = parsePrimary();
                left = new AndExpression(left, right);
            }
            return left;
        }

        Expression parsePrimary() {
            if (match(TokenType.LPAREN)) {
                Expression inner = parseExpression();
                if (!match(TokenType.RPAREN)) {
                    throw new DslSyntaxException("Mismatched parentheses: missing ')' in: " + originalText);
                }
                return inner;
            }

            Token varToken = advance();
            if (varToken.type != TokenType.IDENTIFIER) {
                throw new DslSyntaxException("Expected variable identifier but found '" + varToken.text + "' in: " + originalText);
            }

            if (match(TokenType.BETWEEN)) {
                Token minToken = advance();
                if (minToken.type != TokenType.NUMBER) {
                    throw new DslSyntaxException("Expected numeric start value after BETWEEN for '" + varToken.text + "' but found '" + minToken.text + "' in: " + originalText);
                }
                if (!match(TokenType.AND)) {
                    throw new DslSyntaxException("Expected AND after BETWEEN <start> for '" + varToken.text + "' in: " + originalText);
                }
                Token maxToken = advance();
                if (maxToken.type != TokenType.NUMBER) {
                    throw new DslSyntaxException("Expected numeric end value after AND for '" + varToken.text + "' but found '" + maxToken.text + "' in: " + originalText);
                }
                double minVal;
                try {
                    minVal = Double.parseDouble(minToken.text);
                } catch (NumberFormatException e) {
                    throw new DslSyntaxException("Invalid numeric literal '" + minToken.text + "' in BETWEEN clause: " + originalText, e);
                }
                double maxVal;
                try {
                    maxVal = Double.parseDouble(maxToken.text);
                } catch (NumberFormatException e) {
                    throw new DslSyntaxException("Invalid numeric literal '" + maxToken.text + "' in BETWEEN clause: " + originalText, e);
                }
                return new AndExpression(
                        new TerminalExpression(varToken.text, ">=", minVal),
                        new TerminalExpression(varToken.text, "<=", maxVal)
                );
            }

            Token opToken = advance();
            if (opToken.type != TokenType.OPERATOR) {
                throw new DslSyntaxException("Expected comparison operator (>, >=, <, <=, ==, !=) after '" + varToken.text + "' but found '" + opToken.text + "' in: " + originalText);
            }

            Token numToken = advance();
            if (numToken.type != TokenType.NUMBER) {
                throw new DslSyntaxException("Expected numeric threshold after operator '" + opToken.text + "' but found '" + numToken.text + "' in: " + originalText);
            }

            double val;
            try {
                val = Double.parseDouble(numToken.text);
            } catch (NumberFormatException e) {
                throw new DslSyntaxException("Invalid numeric literal '" + numToken.text + "' in: " + originalText, e);
            }

            return new TerminalExpression(varToken.text, opToken.text, val);
        }
    }

    public static double benchmarkAverageParseMicros(String dsl, int iterations) {
        parse(dsl);
        long t0 = System.nanoTime();
        for (int i = 0; i < iterations; i++) {
            parse(dsl);
        }
        long elapsedNanos = System.nanoTime() - t0;
        return (elapsedNanos / 1000.0) / iterations;
    }

    public static double benchmarkAverageParseAndEvalMicros(String dsl, PolicyContext context, int iterations) {
        Expression expr = parse(dsl);
        expr.interpret(context);
        long t0 = System.nanoTime();
        for (int i = 0; i < iterations; i++) {
            Expression e = parse(dsl);
            e.interpret(context);
        }
        long elapsedNanos = System.nanoTime() - t0;
        return (elapsedNanos / 1000.0) / iterations;
    }

    public static double benchmarkAveragePreParsedEvalMicros(Expression ast, PolicyContext context, int iterations) {
        if (ast == null || context == null || iterations <= 0) {
            return 0.0;
        }
        // JIT warm-up to eliminate cold execution bias
        for (int i = 0; i < Math.min(iterations, 2000); i++) {
            ast.interpret(context);
        }
        long t0 = System.nanoTime();
        for (int i = 0; i < iterations; i++) {
            ast.interpret(context);
        }
        long elapsedNanos = System.nanoTime() - t0;
        return (elapsedNanos / 1000.0) / iterations;
    }
}


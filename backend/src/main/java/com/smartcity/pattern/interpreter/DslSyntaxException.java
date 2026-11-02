package com.smartcity.pattern.interpreter;

public class DslSyntaxException extends RuntimeException {

    public DslSyntaxException(String message) {
        super(message);
    }

    public DslSyntaxException(String message, Throwable cause) {
        super(message, cause);
    }
}

package com.smartcity.controller;

import com.smartcity.test.ComprehensiveTestSuite;
import com.smartcity.util.JsonUtil;

import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

@WebServlet(name = "TestServlet", urlPatterns = {"/api/test-center", "/api/test-center/*"})
public class TestServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        runAndSendResults(resp);
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        runAndSendResults(resp);
    }

    private void runAndSendResults(HttpServletResponse resp) throws IOException {
        long t0 = System.currentTimeMillis();
        ComprehensiveTestSuite suite = new ComprehensiveTestSuite();
        suite.runAllTests();
        long elapsedMs = System.currentTimeMillis() - t0;

        int passed = 0;
        for (ComprehensiveTestSuite.TestResult r : suite.getResults()) {
            if (r.passed) passed++;
        }

        Map<String, Object> response = new HashMap<>();
        response.put("totalTests", suite.getResults().size());
        response.put("passedCount", passed);
        response.put("failedCount", suite.getResults().size() - passed);
        response.put("executionTimeMs", elapsedMs);
        response.put("successRate", Math.round(((double) passed / suite.getResults().size()) * 1000.0) / 10.0);
        response.put("results", suite.getResults());

        JsonUtil.sendJson(resp, HttpServletResponse.SC_OK, response);
    }
}

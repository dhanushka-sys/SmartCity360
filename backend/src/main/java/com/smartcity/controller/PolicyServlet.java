package com.smartcity.controller;

import com.smartcity.dao.PolicyDAO;
import com.smartcity.model.Policy;
import com.smartcity.pattern.interpreter.DslPolicyParser;
import com.smartcity.pattern.interpreter.Expression;
import com.smartcity.pattern.interpreter.PolicyContext;
import com.smartcity.util.JsonUtil;

import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.sql.SQLException;
import java.util.HashMap;
import java.util.Map;

@WebServlet(name = "PolicyServlet", urlPatterns = {"/api/policies", "/api/policies/*"})
public class PolicyServlet extends HttpServlet {

    private final PolicyDAO policyDAO = new PolicyDAO();

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        String pathInfo = req.getPathInfo();
        try {
            if (pathInfo == null || pathInfo.equals("/")) {
                JsonUtil.sendJson(resp, HttpServletResponse.SC_OK, policyDAO.getAllPolicies());
            } else {
                String id = pathInfo.substring(1);
                Policy p = policyDAO.getPolicyById(id);
                if (p != null) {
                    JsonUtil.sendJson(resp, HttpServletResponse.SC_OK, p);
                } else {
                    JsonUtil.sendJson(resp, HttpServletResponse.SC_NOT_FOUND, Map.of("error", "Policy not found"));
                }
            }
        } catch (SQLException e) {
            JsonUtil.sendJson(resp, HttpServletResponse.SC_INTERNAL_SERVER_ERROR, Map.of("error", e.getMessage()));
        }
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        String pathInfo = req.getPathInfo();
        try {
            if (pathInfo != null && pathInfo.contains("/evaluate")) {
                Map body = JsonUtil.fromRequest(req, Map.class);
                String expression = (String) body.get("expression");
                String policyId = (String) body.get("id");
                if (expression == null || expression.trim().isEmpty()) {
                    if (policyId != null && !policyId.isEmpty()) {
                        Policy p = policyDAO.getPolicyById(policyId);
                        if (p != null) {
                            expression = p.getExpression();
                        }
                    }
                }
                if (expression == null || expression.trim().isEmpty()) {
                    JsonUtil.sendJson(resp, HttpServletResponse.SC_BAD_REQUEST, Map.of("error", "DSL expression is required for evaluation"));
                    return;
                }

                Map contextMap = (Map) body.get("context");
                long t0 = System.nanoTime();
                Expression expr = DslPolicyParser.parse(expression);
                PolicyContext ctx = new PolicyContext();
                if (contextMap != null) {
                    for (Object key : contextMap.keySet()) {
                        if (key != null) {
                            ctx.set(key.toString(), contextMap.get(key));
                        }
                    }
                }

                boolean passed = expr.interpret(ctx);
                long elapsedNanos = System.nanoTime() - t0;
                double elapsedMicros = elapsedNanos / 1000.0;

                Map<String, Object> result = new HashMap<>();
                result.put("success", true);
                result.put("passed", passed);
                result.put("ast", expr.toString());
                result.put("expression", expression);
                result.put("evaluationMicros", Math.round(elapsedMicros * 100.0) / 100.0);
                result.put("status", passed ? "COMPLIANT" : "VIOLATION");
                JsonUtil.sendJson(resp, HttpServletResponse.SC_OK, result);
                return;
            }

            Policy policy = JsonUtil.fromRequest(req, Policy.class);
            if (policy.getId() == null || policy.getId().isEmpty()) {
                policy.setId("POL-" + System.currentTimeMillis());
            }
            if (policy.getStatus() == null) {
                policy.setStatus("ACTIVE");
            }
            boolean created = policyDAO.createPolicy(policy);
            if (created) {
                JsonUtil.sendJson(resp, HttpServletResponse.SC_CREATED, policy);
            } else {
                JsonUtil.sendJson(resp, HttpServletResponse.SC_BAD_REQUEST, Map.of("error", "Failed to create policy"));
            }
        } catch (Exception e) {
            JsonUtil.sendJson(resp, HttpServletResponse.SC_INTERNAL_SERVER_ERROR, Map.of("error", e.getMessage()));
        }
    }

    @Override
    protected void doPut(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        String pathInfo = req.getPathInfo();
        if (pathInfo == null || pathInfo.equals("/")) {
            JsonUtil.sendJson(resp, HttpServletResponse.SC_BAD_REQUEST, Map.of("error", "Missing policy ID"));
            return;
        }

        String id = pathInfo.substring(1);
        try {
            boolean ok = policyDAO.togglePolicyStatus(id);
            if (ok) {
                Policy updated = policyDAO.getPolicyById(id);
                JsonUtil.sendJson(resp, HttpServletResponse.SC_OK, updated);
            } else {
                JsonUtil.sendJson(resp, HttpServletResponse.SC_NOT_FOUND, Map.of("error", "Policy not found"));
            }
        } catch (Exception e) {
            JsonUtil.sendJson(resp, HttpServletResponse.SC_INTERNAL_SERVER_ERROR, Map.of("error", e.getMessage()));
        }
    }

    @Override
    protected void doDelete(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        String pathInfo = req.getPathInfo();
        if (pathInfo == null || pathInfo.equals("/")) {
            JsonUtil.sendJson(resp, HttpServletResponse.SC_BAD_REQUEST, Map.of("error", "Missing policy ID"));
            return;
        }

        String id = pathInfo.substring(1);
        try {
            boolean ok = policyDAO.deletePolicy(id);
            if (ok) {
                JsonUtil.sendJson(resp, HttpServletResponse.SC_OK, Map.of("success", true, "deletedId", id));
            } else {
                JsonUtil.sendJson(resp, HttpServletResponse.SC_NOT_FOUND, Map.of("error", "Policy not found"));
            }
        } catch (Exception e) {
            JsonUtil.sendJson(resp, HttpServletResponse.SC_INTERNAL_SERVER_ERROR, Map.of("error", e.getMessage()));
        }
    }
}


package com.smartcity.controller;

import com.smartcity.dao.PolicyDAO;
import com.smartcity.model.Policy;
import com.smartcity.util.JsonUtil;

import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.sql.SQLException;
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
        try {
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


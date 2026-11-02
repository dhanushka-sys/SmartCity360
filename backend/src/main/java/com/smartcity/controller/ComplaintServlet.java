package com.smartcity.controller;

import com.smartcity.dao.ComplaintDAO;
import com.smartcity.model.Complaint;
import com.smartcity.pattern.chain.ComplaintChainFactory;
import com.smartcity.pattern.chain.ComplaintRoutingResult;
import com.smartcity.util.JsonUtil;

import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.sql.SQLException;
import java.util.Map;

@WebServlet(name = "ComplaintServlet", urlPatterns = {"/api/complaints", "/api/complaints/*"})
public class ComplaintServlet extends HttpServlet {

    private final ComplaintDAO complaintDAO = new ComplaintDAO();

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        String pathInfo = req.getPathInfo();
        try {
            if (pathInfo == null || pathInfo.equals("/")) {
                JsonUtil.sendJson(resp, HttpServletResponse.SC_OK, complaintDAO.getAllComplaints());
            } else {
                String id = pathInfo.substring(1);
                Complaint c = complaintDAO.getComplaintById(id);
                if (c != null) {
                    JsonUtil.sendJson(resp, HttpServletResponse.SC_OK, c);
                } else {
                    JsonUtil.sendJson(resp, HttpServletResponse.SC_NOT_FOUND, Map.of("error", "Complaint not found"));
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
            if (pathInfo != null && pathInfo.contains("/route")) {
                Complaint complaint = JsonUtil.fromRequest(req, Complaint.class);
                ComplaintRoutingResult result = ComplaintChainFactory.createChain().handle(complaint);
                JsonUtil.sendJson(resp, HttpServletResponse.SC_OK, result);
                return;
            }

            if (pathInfo != null && pathInfo.contains("/notes")) {
                String complaintId = pathInfo.substring(1).replace("/notes", "");
                Map body = JsonUtil.fromRequest(req, Map.class);
                String author = (String) body.get("author");
                String role = (String) body.get("role");
                String text = (String) body.get("text");

                boolean ok = complaintDAO.addNote(complaintId, author, role, text);
                if (ok) {
                    Complaint updated = complaintDAO.getComplaintById(complaintId);
                    JsonUtil.sendJson(resp, HttpServletResponse.SC_OK, updated);
                } else {
                    JsonUtil.sendJson(resp, HttpServletResponse.SC_BAD_REQUEST, Map.of("error", "Failed to add note"));
                }
                return;
            }

            Complaint complaint = JsonUtil.fromRequest(req, Complaint.class);
            if (complaint.getId() == null || complaint.getId().isEmpty()) {
                long ts = System.currentTimeMillis();
                complaint.setId("CMP-" + (ts % 10000));
                complaint.setTrackingNumber("TRK-2026-" + (ts % 10000));
            }

            // ALWAYS execute Chain of Responsibility to guarantee strict triage & routing
            ComplaintRoutingResult result = ComplaintChainFactory.createChain().handle(complaint);
            complaint.setCurrentHandlerRole(result.getHandledByRole());
            complaint.setStatus(result.getStatus());

            boolean created = complaintDAO.createComplaint(complaint);
            if (created) {
                if (result.getAuditTrail() != null) {
                    for (com.smartcity.pattern.chain.ComplaintAuditRecord rec : result.getAuditTrail()) {
                        complaintDAO.addNote(
                                complaint.getId(),
                                rec.getFromRole() != null ? rec.getFromRole() : "Gateway",
                                rec.getToRole() != null ? rec.getToRole() : "Handler",
                                "[" + rec.getAction() + "] " + rec.getReason()
                        );
                    }
                }
                Complaint updated = complaintDAO.getComplaintById(complaint.getId());
                JsonUtil.sendJson(resp, HttpServletResponse.SC_CREATED, updated != null ? updated : complaint);
            } else {
                JsonUtil.sendJson(resp, HttpServletResponse.SC_BAD_REQUEST, Map.of("error", "Failed to create complaint"));
            }
        } catch (Exception e) {
            JsonUtil.sendJson(resp, HttpServletResponse.SC_INTERNAL_SERVER_ERROR, Map.of("error", e.getMessage()));
        }
    }

    @Override
    protected void doPut(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        String pathInfo = req.getPathInfo();
        if (pathInfo == null || pathInfo.equals("/")) {
            JsonUtil.sendJson(resp, HttpServletResponse.SC_BAD_REQUEST, Map.of("error", "Missing complaint ID"));
            return;
        }

        try {
            String path = pathInfo.substring(1);
            Map body = JsonUtil.fromRequest(req, Map.class);

            if (path.endsWith("/escalate")) {
                String id = path.replace("/escalate", "");
                String toRole = (String) body.get("toRole");
                String reason = (String) body.get("reason");
                String author = (String) body.getOrDefault("author", "Operations Officer");

                if (toRole == null || toRole.isEmpty()) {
                    Complaint existing = complaintDAO.getComplaintById(id);
                    if (existing != null) {
                        if ("LOCAL_STAFF".equalsIgnoreCase(existing.getCurrentHandlerRole())) {
                            toRole = "SUPERVISOR";
                        } else if ("SUPERVISOR".equalsIgnoreCase(existing.getCurrentHandlerRole())) {
                            toRole = "CITY_MANAGER";
                        } else {
                            toRole = "CITY_MANAGER";
                        }
                    } else {
                        toRole = "SUPERVISOR";
                    }
                }

                boolean ok = complaintDAO.escalateComplaint(id, toRole, reason, author);
                if (ok) {
                    Complaint updated = complaintDAO.getComplaintById(id);
                    JsonUtil.sendJson(resp, HttpServletResponse.SC_OK, updated);
                } else {
                    JsonUtil.sendJson(resp, HttpServletResponse.SC_NOT_FOUND, Map.of("error", "Complaint not found"));
                }
            } else if (path.endsWith("/resolve")) {
                String id = path.replace("/resolve", "");
                String summary = (String) body.get("resolutionSummary");

                boolean ok = complaintDAO.resolveComplaint(id, summary);
                if (ok) {
                    Complaint updated = complaintDAO.getComplaintById(id);
                    JsonUtil.sendJson(resp, HttpServletResponse.SC_OK, updated);
                } else {
                    JsonUtil.sendJson(resp, HttpServletResponse.SC_NOT_FOUND, Map.of("error", "Complaint not found"));
                }
            } else {
                JsonUtil.sendJson(resp, HttpServletResponse.SC_BAD_REQUEST, Map.of("error", "Unknown operation"));
            }
        } catch (Exception e) {
            JsonUtil.sendJson(resp, HttpServletResponse.SC_INTERNAL_SERVER_ERROR, Map.of("error", e.getMessage()));
        }
    }
}

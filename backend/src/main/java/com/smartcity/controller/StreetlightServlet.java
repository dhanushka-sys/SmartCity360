package com.smartcity.controller;

import com.smartcity.dao.StreetlightDAO;
import com.smartcity.model.Streetlight;
import com.smartcity.util.JsonUtil;

import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.sql.SQLException;
import java.util.List;
import java.util.Map;

@WebServlet(name = "StreetlightServlet", urlPatterns = {"/api/streetlights", "/api/streetlights/*"})
public class StreetlightServlet extends HttpServlet {

    private final StreetlightDAO streetlightDAO = new StreetlightDAO();

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        String pathInfo = req.getPathInfo();
        try {
            if (pathInfo != null && pathInfo.equals("/profiles")) {
                JsonUtil.sendJson(resp, HttpServletResponse.SC_OK, streetlightDAO.getAllProfiles());
            } else {
                JsonUtil.sendJson(resp, HttpServletResponse.SC_OK, streetlightDAO.getAllStreetlights());
            }
        } catch (SQLException e) {
            JsonUtil.sendJson(resp, HttpServletResponse.SC_INTERNAL_SERVER_ERROR, Map.of("error", e.getMessage()));
        }
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        try {
            Streetlight light = JsonUtil.fromRequest(req, Streetlight.class);
            if (light.getId() == null || light.getId().isEmpty()) {
                light.setId("SL-" + System.currentTimeMillis());
            }
            boolean ok = streetlightDAO.createStreetlight(light);
            if (ok) {
                JsonUtil.sendJson(resp, HttpServletResponse.SC_CREATED, light);
            } else {
                JsonUtil.sendJson(resp, HttpServletResponse.SC_BAD_REQUEST, Map.of("error", "Failed to create streetlight"));
            }
        } catch (Exception e) {
            JsonUtil.sendJson(resp, HttpServletResponse.SC_INTERNAL_SERVER_ERROR, Map.of("error", e.getMessage()));
        }
    }

    @Override
    protected void doPut(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        String pathInfo = req.getPathInfo();
        try {
            Map body = JsonUtil.fromRequest(req, Map.class);

            if (pathInfo != null && pathInfo.equals("/bulk")) {
                List<String> ids = (List<String>) body.get("ids");
                String status = (String) body.get("status");
                boolean ok = streetlightDAO.bulkUpdateStatus(ids, status);
                JsonUtil.sendJson(resp, HttpServletResponse.SC_OK, Map.of("success", ok, "updatedCount", ids.size()));
                return;
            }

            if (pathInfo != null && pathInfo.length() > 1) {
                String id = pathInfo.substring(1);
                boolean isStatusSubpath = false;
                boolean isBrightnessSubpath = false;
                if (id.endsWith("/status")) {
                    id = id.replace("/status", "");
                    isStatusSubpath = true;
                } else if (id.endsWith("/brightness")) {
                    id = id.replace("/brightness", "");
                    isBrightnessSubpath = true;
                }

                if (body.containsKey("brightness") || isBrightnessSubpath) {
                    int brightness = ((Number) body.getOrDefault("brightness", 80)).intValue();
                    boolean ok = streetlightDAO.updateBrightness(id, brightness);
                    JsonUtil.sendJson(resp, HttpServletResponse.SC_OK, Map.of("success", ok, "id", id, "brightness", brightness));
                } else if (body.containsKey("status") || isStatusSubpath) {
                    String status = (String) body.getOrDefault("status", "ACTIVE");
                    boolean ok = streetlightDAO.updateStatus(id, status);
                    JsonUtil.sendJson(resp, HttpServletResponse.SC_OK, Map.of("success", ok, "id", id, "status", status));
                } else {
                    JsonUtil.sendJson(resp, HttpServletResponse.SC_BAD_REQUEST, Map.of("error", "No valid field to update"));
                }
            } else {
                JsonUtil.sendJson(resp, HttpServletResponse.SC_BAD_REQUEST, Map.of("error", "Missing streetlight ID"));
            }
        } catch (Exception e) {
            JsonUtil.sendJson(resp, HttpServletResponse.SC_INTERNAL_SERVER_ERROR, Map.of("error", e.getMessage()));
        }
    }
}


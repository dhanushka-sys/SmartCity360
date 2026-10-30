package com.smartcity.controller;

import com.smartcity.dao.ZoneDAO;
import com.smartcity.model.Zone;
import com.smartcity.util.JsonUtil;

import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.sql.SQLException;
import java.util.Map;

@WebServlet(name = "ZoneServlet", urlPatterns = {"/api/zones", "/api/zones/*"})
public class ZoneServlet extends HttpServlet {

    private final ZoneDAO zoneDAO = new ZoneDAO();

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        String pathInfo = req.getPathInfo();
        try {
            if (pathInfo == null || pathInfo.equals("/")) {
                String format = req.getParameter("format");
                if ("tree".equalsIgnoreCase(format)) {
                    Zone tree = zoneDAO.getZoneTree();
                    JsonUtil.sendJson(resp, HttpServletResponse.SC_OK, tree);
                } else {
                    JsonUtil.sendJson(resp, HttpServletResponse.SC_OK, zoneDAO.getAllZones());
                }
            } else {
                String id = pathInfo.substring(1);
                Zone z = zoneDAO.getZoneById(id);
                if (z != null) {
                    JsonUtil.sendJson(resp, HttpServletResponse.SC_OK, z);
                } else {
                    JsonUtil.sendJson(resp, HttpServletResponse.SC_NOT_FOUND, Map.of("error", "Zone not found"));
                }
            }
        } catch (SQLException e) {
            JsonUtil.sendJson(resp, HttpServletResponse.SC_INTERNAL_SERVER_ERROR, Map.of("error", e.getMessage()));
        }
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        try {
            Zone zone = JsonUtil.fromRequest(req, Zone.class);
            if (zone.getId() == null || zone.getId().isEmpty()) {
                zone.setId("ZN-" + System.currentTimeMillis());
            }
            boolean created = zoneDAO.createZone(zone);
            if (created) {
                JsonUtil.sendJson(resp, HttpServletResponse.SC_CREATED, zone);
            } else {
                JsonUtil.sendJson(resp, HttpServletResponse.SC_BAD_REQUEST, Map.of("error", "Failed to create zone"));
            }
        } catch (Exception e) {
            JsonUtil.sendJson(resp, HttpServletResponse.SC_INTERNAL_SERVER_ERROR, Map.of("error", e.getMessage()));
        }
    }

    @Override
    protected void doPut(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        String pathInfo = req.getPathInfo();
        if (pathInfo == null || pathInfo.equals("/")) {
            JsonUtil.sendJson(resp, HttpServletResponse.SC_BAD_REQUEST, Map.of("error", "Missing zone ID"));
            return;
        }

        String id = pathInfo.substring(1);
        try {
            Map body = JsonUtil.fromRequest(req, Map.class);
            String status = (String) body.get("status");
            Boolean recursive = (Boolean) body.get("recursive");

            boolean ok;
            if (Boolean.TRUE.equals(recursive)) {
                ok = zoneDAO.updateZoneStatusRecursively(id, status);
            } else {
                ok = zoneDAO.updateZoneStatus(id, status);
            }

            if (ok) {
                Zone updated = zoneDAO.getZoneById(id);
                JsonUtil.sendJson(resp, HttpServletResponse.SC_OK, updated);
            } else {
                JsonUtil.sendJson(resp, HttpServletResponse.SC_NOT_FOUND, Map.of("error", "Zone not found"));
            }
        } catch (Exception e) {
            JsonUtil.sendJson(resp, HttpServletResponse.SC_INTERNAL_SERVER_ERROR, Map.of("error", e.getMessage()));
        }
    }
}


package com.smartcity.controller;

import com.smartcity.dao.UserDAO;
import com.smartcity.model.User;
import com.smartcity.util.JsonUtil;

import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.sql.SQLException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@WebServlet(name = "AuthServlet", urlPatterns = {"/api/auth", "/api/auth/*"})
public class AuthServlet extends HttpServlet {

    private final UserDAO userDAO = new UserDAO();

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        String pathInfo = req.getPathInfo();
        try {
            if ("/users".equalsIgnoreCase(pathInfo)) {
                List<User> users = userDAO.getAllUsers();
                JsonUtil.sendJson(resp, HttpServletResponse.SC_OK, users);
                return;
            }

            if ("/me".equalsIgnoreCase(pathInfo)) {
                String id = req.getParameter("id");
                if (id != null && !id.isEmpty()) {
                    User u = userDAO.getById(id);
                    if (u != null) {
                        JsonUtil.sendJson(resp, HttpServletResponse.SC_OK, u);
                        return;
                    }
                }
                JsonUtil.sendJson(resp, HttpServletResponse.SC_NOT_FOUND, Map.of("error", "User not found"));
                return;
            }

            JsonUtil.sendJson(resp, HttpServletResponse.SC_OK, Map.of("status", "Auth service online"));
        } catch (SQLException e) {
            JsonUtil.sendJson(resp, HttpServletResponse.SC_INTERNAL_SERVER_ERROR, Map.of("error", e.getMessage()));
        }
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        String pathInfo = req.getPathInfo();
        try {
            if ("/login".equalsIgnoreCase(pathInfo)) {
                Map<String, String> body = JsonUtil.fromRequest(req, Map.class);
                if (body == null) {
                    JsonUtil.sendJson(resp, HttpServletResponse.SC_BAD_REQUEST, Map.of("error", "Missing request body"));
                    return;
                }

                String identifier = body.get("identifier");
                if (identifier == null || identifier.isEmpty()) {
                    identifier = body.get("username");
                }
                if (identifier == null || identifier.isEmpty()) {
                    identifier = body.get("email");
                }

                String password = body.get("password");

                if (identifier == null || password == null) {
                    JsonUtil.sendJson(resp, HttpServletResponse.SC_BAD_REQUEST, Map.of("error", "Username/email and password required"));
                    return;
                }

                User user = userDAO.authenticate(identifier, password);
                if (user != null) {
                    Map<String, Object> result = new HashMap<>();
                    result.put("success", true);
                    result.put("token", user.getToken());
                    result.put("user", user);
                    JsonUtil.sendJson(resp, HttpServletResponse.SC_OK, result);
                } else {
                    JsonUtil.sendJson(resp, HttpServletResponse.SC_UNAUTHORIZED, Map.of("success", false, "error", "Invalid credentials"));
                }
                return;
            }

            if ("/logout".equalsIgnoreCase(pathInfo)) {
                String authHeader = req.getHeader("Authorization");
                if (authHeader != null && authHeader.startsWith("Bearer ")) {
                    String token = authHeader.substring(7).trim();
                    UserDAO.invalidateToken(token);
                }
                JsonUtil.sendJson(resp, HttpServletResponse.SC_OK, Map.of("success", true, "message", "Logged out successfully"));
                return;
            }

            JsonUtil.sendJson(resp, HttpServletResponse.SC_NOT_FOUND, Map.of("error", "Auth endpoint not found"));
        } catch (SQLException e) {
            JsonUtil.sendJson(resp, HttpServletResponse.SC_INTERNAL_SERVER_ERROR, Map.of("error", e.getMessage()));
        }
    }
}

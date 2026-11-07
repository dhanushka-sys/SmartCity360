package com.smartcity.dao;

import com.smartcity.config.DatabaseConfig;
import com.smartcity.model.User;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

public class UserDAO {

    public static class UserSession {
        public final String userId;
        public final String role;
        public final long loginTimestamp;

        public UserSession(String userId, String role) {
            this.userId = userId;
            this.role = role;
            this.loginTimestamp = System.currentTimeMillis();
        }
    }

    private static final String SALT = "SmartCity360SecureSalt2026";
    private static final Map<String, UserSession> activeTokens = new ConcurrentHashMap<>();
    private static final SecureRandom secureRandom = new SecureRandom();

    public static String hashPassword(String password) {
        if (password == null) return null;
        try {
            MessageDigest md = MessageDigest.getInstance("SHA-256");
            byte[] hashed = md.digest((SALT + password).getBytes(StandardCharsets.UTF_8));
            StringBuilder sb = new StringBuilder();
            for (byte b : hashed) {
                sb.append(String.format("%02x", b));
            }
            return sb.toString();
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException("SHA-256 algorithm not available", e);
        }
    }

    public static String generateSecureToken(String userId, String role) {
        byte[] randomBytes = new byte[32];
        secureRandom.nextBytes(randomBytes);
        StringBuilder sb = new StringBuilder("SC360_");
        for (byte b : randomBytes) {
            sb.append(String.format("%02x", b));
        }
        String token = sb.toString();
        activeTokens.put(token, new UserSession(userId, role != null ? role : "OPERATOR"));
        return token;
    }

    public static String generateSecureToken(String userId) {
        return generateSecureToken(userId, "OPERATOR");
    }

    public static boolean validateToken(String token) {
        return token != null && activeTokens.containsKey(token);
    }

    public static UserSession getSession(String token) {
        if (token == null) return null;
        return activeTokens.get(token);
    }

    public static boolean hasRole(String token, String... allowedRoles) {
        UserSession session = getSession(token);
        if (session == null || session.role == null) return false;
        for (String r : allowedRoles) {
            if (r.equalsIgnoreCase(session.role)) return true;
        }
        return false;
    }

    public static void invalidateToken(String token) {
        if (token != null) {
            activeTokens.remove(token);
        }
    }

    public User authenticate(String identifier, String password) throws SQLException {
        if (identifier == null || password == null) {
            return null;
        }

        String hashed = hashPassword(password);
        String sql = "SELECT * FROM users WHERE username = ? OR email = ?";

        try (Connection conn = DatabaseConfig.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {

            stmt.setString(1, identifier.trim());
            stmt.setString(2, identifier.trim());

            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    String storedPass = rs.getString("password");
                    boolean passwordMatches = false;

                    if (storedPass != null && storedPass.equals(hashed)) {
                        passwordMatches = true;
                    } else if (storedPass != null && storedPass.equals(password)) {
                        passwordMatches = true;
                        upgradeUserPassword(rs.getString("id"), hashed);
                    }

                    if (passwordMatches) {
                        User user = mapResultSetToUser(rs);
                        user.setPassword(null);
                        user.setToken(generateSecureToken(user.getId(), user.getRole()));
                        return user;
                    }
                }
            }
        }
        return null;
    }

    public void upgradeUserPassword(String userId, String newHashedPassword) {
        String updateSql = "UPDATE users SET password = ? WHERE id = ?";
        try (Connection conn = DatabaseConfig.getConnection();
             PreparedStatement stmt = conn.prepareStatement(updateSql)) {
            stmt.setString(1, newHashedPassword);
            stmt.setString(2, userId);
            stmt.executeUpdate();
        } catch (SQLException e) {
            System.err.println("[WARN] UserDAO: Failed to upgrade legacy password hash for user " + userId + ": " + e.getMessage());
        }
    }

    public User getById(String id) throws SQLException {
        String sql = "SELECT * FROM users WHERE id = ?";

        try (Connection conn = DatabaseConfig.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {

            stmt.setString(1, id);

            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    User user = mapResultSetToUser(rs);
                    user.setPassword(null);
                    return user;
                }
            }
        }
        return null;
    }

    public List<User> getAllUsers() throws SQLException {
        List<User> list = new ArrayList<>();
        String sql = "SELECT * FROM users ORDER BY id ASC";

        try (Connection conn = DatabaseConfig.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql);
             ResultSet rs = stmt.executeQuery()) {

            while (rs.next()) {
                User user = mapResultSetToUser(rs);
                user.setPassword(null);
                list.add(user);
            }
        }
        return list;
    }

    private User mapResultSetToUser(ResultSet rs) throws SQLException {
        User u = new User();
        u.setId(rs.getString("id"));
        u.setUsername(rs.getString("username"));
        u.setEmail(rs.getString("email"));
        u.setPassword(rs.getString("password"));
        u.setFullName(rs.getString("full_name"));
        u.setRole(rs.getString("role"));
        u.setDepartment(rs.getString("department"));
        u.setAvatarInitials(rs.getString("avatar_initials"));
        return u;
    }
}

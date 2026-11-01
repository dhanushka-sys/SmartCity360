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

    private static final String SALT = "SmartCity360SecureSalt2026";
    private static final Map<String, String> activeTokens = new ConcurrentHashMap<>();
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

    public static String generateSecureToken(String userId) {
        byte[] randomBytes = new byte[32];
        secureRandom.nextBytes(randomBytes);
        StringBuilder sb = new StringBuilder("SC360_");
        for (byte b : randomBytes) {
            sb.append(String.format("%02x", b));
        }
        String token = sb.toString();
        activeTokens.put(token, userId);
        return token;
    }

    public static boolean validateToken(String token) {
        return token != null && activeTokens.containsKey(token);
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
        String sql = "SELECT * FROM users WHERE (username = ? OR email = ?) AND (password = ? OR password = ?)";

        try (Connection conn = DatabaseConfig.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {

            stmt.setString(1, identifier.trim());
            stmt.setString(2, identifier.trim());
            stmt.setString(3, hashed);
            stmt.setString(4, password);

            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    User user = mapResultSetToUser(rs);
                    user.setPassword(null);
                    user.setToken(generateSecureToken(user.getId()));
                    return user;
                }
            }
        }
        return null;
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

package com.smartcity.dao;

import com.smartcity.config.DatabaseConfig;
import com.smartcity.model.Policy;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class PolicyDAO {

    public List<Policy> getAllPolicies() throws SQLException {
        List<Policy> list = new ArrayList<>();
        String sql = "SELECT * FROM policies ORDER BY created_at ASC";

        try (Connection conn = DatabaseConfig.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql);
             ResultSet rs = stmt.executeQuery()) {

            while (rs.next()) {
                list.add(mapResultSetToPolicy(rs));
            }
        }
        return list;
    }

    public Policy getPolicyById(String id) throws SQLException {
        String sql = "SELECT * FROM policies WHERE id = ?";
        try (Connection conn = DatabaseConfig.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {

            stmt.setString(1, id);
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    return mapResultSetToPolicy(rs);
                }
            }
        }
        return null;
    }

    public boolean createPolicy(Policy p) throws SQLException {
        String sql = "INSERT INTO policies (id, code, name, category, expression, description, status, applied_zones) VALUES (?, ?, ?, ?, ?, ?, ?, ?)";

        try (Connection conn = DatabaseConfig.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {

            stmt.setString(1, p.getId());
            stmt.setString(2, p.getCode());
            stmt.setString(3, p.getName());
            stmt.setString(4, p.getCategory());
            stmt.setString(5, p.getExpression());
            stmt.setString(6, p.getDescription());
            stmt.setString(7, p.getStatus());
            stmt.setInt(8, p.getAppliedZones());

            return stmt.executeUpdate() > 0;
        }
    }

    public boolean togglePolicyStatus(String id) throws SQLException {
        String sql = "UPDATE policies SET status = CASE WHEN status = 'ACTIVE' THEN 'INACTIVE' ELSE 'ACTIVE' END WHERE id = ?";
        try (Connection conn = DatabaseConfig.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {

            stmt.setString(1, id);
            return stmt.executeUpdate() > 0;
        }
    }

    public boolean deletePolicy(String id) throws SQLException {
        String sql = "DELETE FROM policies WHERE id = ?";
        try (Connection conn = DatabaseConfig.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {

            stmt.setString(1, id);
            return stmt.executeUpdate() > 0;
        }
    }

    private Policy mapResultSetToPolicy(ResultSet rs) throws SQLException {
        Policy p = new Policy();
        p.setId(rs.getString("id"));
        p.setCode(rs.getString("code"));
        p.setName(rs.getString("name"));
        p.setCategory(rs.getString("category"));
        p.setExpression(rs.getString("expression"));
        p.setDescription(rs.getString("description"));
        p.setStatus(rs.getString("status"));
        p.setAppliedZones(rs.getInt("applied_zones"));
        p.setCreatedAt(rs.getString("created_at"));
        return p;
    }
}


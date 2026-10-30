package com.smartcity.dao;

import com.smartcity.config.DatabaseConfig;
import com.smartcity.model.Streetlight;
import com.smartcity.model.StreetlightProfile;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class StreetlightDAO {

    public List<Streetlight> getAllStreetlights() throws SQLException {
        List<Streetlight> list = new ArrayList<>();
        String sql = "SELECT * FROM streetlights ORDER BY id ASC";

        try (Connection conn = DatabaseConfig.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql);
             ResultSet rs = stmt.executeQuery()) {

            while (rs.next()) {
                list.add(mapResultSetToStreetlight(rs));
            }
        }
        return list;
    }

    public List<StreetlightProfile> getAllProfiles() throws SQLException {
        List<StreetlightProfile> list = new ArrayList<>();
        String sql = "SELECT * FROM streetlight_profiles ORDER BY id ASC";

        try (Connection conn = DatabaseConfig.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql);
             ResultSet rs = stmt.executeQuery()) {

            while (rs.next()) {
                StreetlightProfile p = new StreetlightProfile();
                p.setId(rs.getString("id"));
                p.setModelName(rs.getString("model_name"));
                p.setManufacturer(rs.getString("manufacturer"));
                p.setWattageRating(rs.getInt("wattage_rating"));
                p.setLampType(rs.getString("lamp_type"));
                p.setDefaultBrightness(rs.getInt("default_brightness"));
                p.setOperatingSchedule(rs.getString("operating_schedule"));
                p.setColorTempKelvin(rs.getInt("color_temp_kelvin"));
                list.add(p);
            }
        }
        return list;
    }

    public boolean updateBrightness(String id, int brightness) throws SQLException {
        String sql = "UPDATE streetlights SET brightness = ? WHERE id = ?";
        try (Connection conn = DatabaseConfig.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {

            stmt.setInt(1, brightness);
            stmt.setString(2, id);
            return stmt.executeUpdate() > 0;
        }
    }

    public boolean updateStatus(String id, String status) throws SQLException {
        String sql = "UPDATE streetlights SET status = ? WHERE id = ?";
        try (Connection conn = DatabaseConfig.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {

            stmt.setString(1, status);
            stmt.setString(2, id);
            return stmt.executeUpdate() > 0;
        }
    }

    public boolean bulkUpdateStatus(List<String> ids, String status) throws SQLException {
        String sql = "UPDATE streetlights SET status = ? WHERE id = ?";
        try (Connection conn = DatabaseConfig.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {

            for (String id : ids) {
                stmt.setString(1, status);
                stmt.setString(2, id);
                stmt.addBatch();
            }
            stmt.executeBatch();
            return true;
        }
    }

    private Streetlight mapResultSetToStreetlight(ResultSet rs) throws SQLException {
        Streetlight s = new Streetlight();
        s.setId(rs.getString("id"));
        s.setSerialNumber(rs.getString("serial_number"));
        s.setProfileId(rs.getString("profile_id"));
        s.setZoneId(rs.getString("zone_id"));
        s.setZoneName(rs.getString("zone_name"));
        s.setStreetName(rs.getString("street_name"));
        s.setLatitude(rs.getDouble("latitude"));
        s.setLongitude(rs.getDouble("longitude"));
        s.setStatus(rs.getString("status"));
        s.setBrightness(rs.getInt("brightness"));
        s.setPowerUsageKw(rs.getDouble("power_usage_kw"));
        s.setLastPing(rs.getString("last_ping"));
        return s;
    }
}


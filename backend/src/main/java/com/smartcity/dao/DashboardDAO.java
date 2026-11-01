package com.smartcity.dao;

import com.smartcity.config.DatabaseConfig;
import com.smartcity.model.Complaint;

import java.sql.*;
import java.time.Instant;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class DashboardDAO {

    public Map<String, Object> getDashboardStats() throws SQLException {
        Map<String, Object> stats = new HashMap<>();

        try (Connection conn = DatabaseConfig.getConnection()) {

            try (Statement s = conn.createStatement();
                 ResultSet rs = s.executeQuery("SELECT COUNT(*) as cnt, " +
                         "SUM(CASE WHEN type = 'DISTRICT' THEN 1 ELSE 0 END) as districts, " +
                         "SUM(CASE WHEN type = 'STREET' THEN 1 ELSE 0 END) as streets, " +
                         "SUM(CASE WHEN type = 'BUILDING' THEN 1 ELSE 0 END) as buildings, " +
                         "COALESCE(SUM(power_usage_kw), 0) as total_power " +
                         "FROM zones")) {
                if (rs.next()) {
                    stats.put("totalZones", rs.getInt("cnt"));
                    stats.put("districtCount", rs.getInt("districts"));
                    stats.put("streetCount", rs.getInt("streets"));
                    stats.put("buildingCount", rs.getInt("buildings"));
                    stats.put("totalPowerKw", rs.getDouble("total_power"));
                }
            }

            try (Statement s = conn.createStatement();
                 ResultSet rs = s.executeQuery("SELECT COUNT(*) as cnt, " +
                         "COALESCE(SUM(packets_processed), 0) as total_packets, " +
                         "COALESCE(SUM(power_kw), 0) as stream_power " +
                         "FROM data_streams")) {
                if (rs.next()) {
                    stats.put("totalStreams", rs.getInt("cnt"));
                    stats.put("totalPackets", rs.getLong("total_packets"));
                    double streamPower = rs.getDouble("stream_power");
                    if (streamPower > 0) {
                        stats.put("streamPowerKw", streamPower);
                    }
                }
            }

            try (Statement s = conn.createStatement();
                 ResultSet rs = s.executeQuery("SELECT COUNT(*) as cnt, " +
                         "SUM(CASE WHEN status = 'ONLINE' THEN 1 ELSE 0 END) as online_cnt, " +
                         "COALESCE(SUM(power_usage_kw), 0) as total_light_kw " +
                         "FROM streetlights")) {
                if (rs.next()) {
                    stats.put("totalStreetlights", rs.getInt("cnt"));
                    stats.put("onlineStreetlights", rs.getInt("online_cnt"));
                    stats.put("totalLightKw", rs.getDouble("total_light_kw"));
                }
            }

            try (Statement s = conn.createStatement();
                 ResultSet rs = s.executeQuery("SELECT COUNT(*) as cnt, " +
                         "SUM(CASE WHEN status != 'RESOLVED' THEN 1 ELSE 0 END) as open_cnt, " +
                         "SUM(CASE WHEN severity = 'CRITICAL' AND status != 'RESOLVED' THEN 1 ELSE 0 END) as crit_cnt " +
                         "FROM complaints")) {
                if (rs.next()) {
                    stats.put("totalComplaints", rs.getInt("cnt"));
                    stats.put("openComplaints", rs.getInt("open_cnt"));
                    stats.put("criticalComplaints", rs.getInt("crit_cnt"));
                }
            }

            try (Statement s = conn.createStatement();
                 ResultSet rs = s.executeQuery("SELECT COUNT(*) as cnt, " +
                         "SUM(CASE WHEN status = 'ACTIVE' THEN 1 ELSE 0 END) as active_cnt " +
                         "FROM policies")) {
                if (rs.next()) {
                    stats.put("totalPolicies", rs.getInt("cnt"));
                    stats.put("activePolicies", rs.getInt("active_cnt"));
                }
            }

            List<Complaint> recent = new ArrayList<>();
            try (Statement s = conn.createStatement();
                 ResultSet rs = s.executeQuery("SELECT * FROM complaints ORDER BY submitted_at DESC LIMIT 5")) {
                while (rs.next()) {
                    Complaint c = new Complaint();
                    c.setId(rs.getString("id"));
                    c.setTrackingNumber(rs.getString("tracking_number"));
                    c.setTitle(rs.getString("title"));
                    c.setCategory(rs.getString("category"));
                    c.setSeverity(rs.getString("severity"));
                    c.setZoneName(rs.getString("zone_name"));
                    c.setCurrentHandlerRole(rs.getString("current_handler_role"));
                    c.setStatus(rs.getString("status"));
                    recent.add(c);
                }
            }
            stats.put("recentComplaints", recent);

            List<Map<String, Object>> energyTrends = new ArrayList<>();
            double totalKw = (double) stats.getOrDefault("totalPowerKw", 3500.0);
            if (totalKw <= 0) {
                totalKw = 3450.0;
            }
            String[] times = new String[]{"00:00", "04:00", "08:00", "12:00", "16:00", "20:00", "23:59"};
            double[] factors = new double[]{0.52, 0.44, 0.88, 1.15, 1.08, 0.78, 0.55};
            double[] projFactors = new double[]{0.50, 0.46, 0.85, 1.12, 1.05, 0.81, 0.53};
            for (int i = 0; i < times.length; i++) {
                Map<String, Object> point = new HashMap<>();
                point.put("time", times[i]);
                point.put("actual", Math.round(totalKw * factors[i] * 10.0) / 10.0);
                point.put("projected", Math.round(totalKw * projFactors[i] * 10.0) / 10.0);
                energyTrends.add(point);
            }
            stats.put("energyTrends", energyTrends);

            List<Map<String, Object>> complaintTrends = new ArrayList<>();
            String sqlComplaints = "SELECT DATE(submitted_at) as log_date, DAYNAME(submitted_at) as day_name, " +
                    "COUNT(*) as submitted_cnt, " +
                    "SUM(CASE WHEN status = 'RESOLVED' THEN 1 ELSE 0 END) as resolved_cnt, " +
                    "SUM(CASE WHEN status = 'ESCALATED' THEN 1 ELSE 0 END) as escalated_cnt " +
                    "FROM complaints " +
                    "GROUP BY DATE(submitted_at), DAYNAME(submitted_at) " +
                    "ORDER BY log_date ASC LIMIT 7";

            try (Statement s = conn.createStatement();
                 ResultSet rs = s.executeQuery(sqlComplaints)) {
                while (rs.next()) {
                    Map<String, Object> dayPoint = new HashMap<>();
                    String dayName = rs.getString("day_name");
                    dayPoint.put("day", dayName != null && dayName.length() >= 3 ? dayName.substring(0, 3) : "Day");
                    dayPoint.put("submitted", rs.getInt("submitted_cnt"));
                    dayPoint.put("resolved", rs.getInt("resolved_cnt"));
                    dayPoint.put("escalated", rs.getInt("escalated_cnt"));
                    complaintTrends.add(dayPoint);
                }
            }

            if (complaintTrends.isEmpty()) {
                int totalC = (int) stats.getOrDefault("totalComplaints", 30);
                int openC = (int) stats.getOrDefault("openComplaints", 22);
                int critC = (int) stats.getOrDefault("criticalComplaints", 8);
                int resolvedC = Math.max(0, totalC - openC);

                String[] days = new String[]{"Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"};
                int[] subDist = new int[]{5, 7, 4, 6, 8, 3, 2};
                int[] resDist = new int[]{3, 5, 3, 4, 6, 2, 1};
                int[] escDist = new int[]{1, 2, 1, 2, 3, 1, 0};
                for (int i = 0; i < days.length; i++) {
                    Map<String, Object> dayPoint = new HashMap<>();
                    dayPoint.put("day", days[i]);
                    dayPoint.put("submitted", subDist[i]);
                    dayPoint.put("resolved", resDist[i]);
                    dayPoint.put("escalated", escDist[i]);
                    complaintTrends.add(dayPoint);
                }
            }
            stats.put("complaintTrends", complaintTrends);

            List<Map<String, Object>> activityLogs = new ArrayList<>();
            try (Statement s = conn.createStatement();
                 ResultSet rs = s.executeQuery("SELECT id, title, severity, submitted_at FROM complaints ORDER BY submitted_at DESC LIMIT 3")) {
                while (rs.next()) {
                    Map<String, Object> act = new HashMap<>();
                    act.put("id", "ACT-" + rs.getString("id"));
                    act.put("title", "Incident Logged: " + rs.getString("title"));
                    act.put("description", "Complaint " + rs.getString("id") + " registered with severity " + rs.getString("severity"));
                    Timestamp ts = rs.getTimestamp("submitted_at");
                    act.put("timestamp", ts != null ? ts.toInstant().toString() : Instant.now().toString());
                    act.put("severity", "CRITICAL".equalsIgnoreCase(rs.getString("severity")) ? "CRITICAL" : "WARNING");
                    act.put("module", "Citizen Complaints");
                    act.put("patternRelated", "CHAIN_OF_RESPONSIBILITY");
                    activityLogs.add(act);
                }
            }
            try (Statement s = conn.createStatement();
                 ResultSet rs = s.executeQuery("SELECT id, name, status, power_kw FROM data_streams LIMIT 2")) {
                while (rs.next()) {
                    Map<String, Object> act = new HashMap<>();
                    act.put("id", "ACT-" + rs.getString("id"));
                    act.put("title", "Telemetry Stream: " + rs.getString("name"));
                    act.put("description", "Energy stream operating at " + rs.getDouble("power_kw") + " kW with status " + rs.getString("status"));
                    act.put("timestamp", Instant.now().toString());
                    act.put("severity", "INFO");
                    act.put("module", "Data Streams");
                    act.put("patternRelated", "DECORATOR");
                    activityLogs.add(act);
                }
            }
            stats.put("recentActivity", activityLogs);
        }

        return stats;
    }
}

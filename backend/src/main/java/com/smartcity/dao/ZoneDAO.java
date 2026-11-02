package com.smartcity.dao;

import com.smartcity.config.DatabaseConfig;
import com.smartcity.model.Zone;
import com.smartcity.pattern.composite.BuildingLeaf;
import com.smartcity.pattern.composite.ZoneCommand;
import com.smartcity.pattern.composite.ZoneComponent;
import com.smartcity.pattern.composite.ZoneComposite;

import java.sql.*;
import java.util.*;

public class ZoneDAO {

    public List<Zone> getAllZones() throws SQLException {
        List<Zone> zones = new ArrayList<>();
        String sql = "SELECT * FROM zones ORDER BY created_at ASC";

        try (Connection conn = DatabaseConfig.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql);
             ResultSet rs = stmt.executeQuery()) {

            while (rs.next()) {
                zones.add(mapResultSetToZone(rs));
            }
        }
        return zones;
    }

    public Zone getZoneTree() throws SQLException {
        List<Zone> all = getAllZones();
        if (all.isEmpty()) return null;

        Map<String, Zone> zoneMap = new HashMap<>();
        for (Zone z : all) {
            zoneMap.put(z.getId(), z);
        }

        Zone root = null;
        for (Zone z : all) {
            if (z.getParentId() == null || z.getParentId().isEmpty()) {
                root = z;
            } else {
                Zone parent = zoneMap.get(z.getParentId());
                if (parent != null) {
                    parent.getChildren().add(z);
                }
            }
        }
        return root != null ? root : all.get(0);
    }

    public ZoneComponent buildCompositeHierarchy(List<Zone> all, String rootId) {
        Map<String, ZoneComponent> compMap = new HashMap<>();
        for (Zone z : all) {
            if ("BUILDING".equalsIgnoreCase(z.getType())) {
                compMap.put(z.getId(), new BuildingLeaf(z.getId(), z.getName(), z.getPowerUsageKw()));
            } else {
                compMap.put(z.getId(), new ZoneComposite(z.getId(), z.getName(), z.getType()));
            }
        }
        for (Zone z : all) {
            if (z.getParentId() != null && !z.getParentId().isEmpty()) {
                ZoneComponent parent = compMap.get(z.getParentId());
                ZoneComponent child = compMap.get(z.getId());
                if (parent instanceof ZoneComposite && child != null) {
                    ((ZoneComposite) parent).add(child);
                }
            }
        }
        return compMap.get(rootId);
    }

    public Zone getZoneById(String id) throws SQLException {
        String sql = "SELECT * FROM zones WHERE id = ?";
        try (Connection conn = DatabaseConfig.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {

            stmt.setString(1, id);
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    return mapResultSetToZone(rs);
                }
            }
        }
        return null;
    }

    public boolean createZone(Zone zone) throws SQLException {
        String sql = "INSERT INTO zones (id, name, code, type, parent_id, status, power_usage_kw, daily_consumption_kwh, active_sensors, total_sensors, active_streetlights, active_alerts, manager, floors) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";

        try (Connection conn = DatabaseConfig.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {

            stmt.setString(1, zone.getId());
            stmt.setString(2, zone.getName());
            stmt.setString(3, zone.getCode());
            stmt.setString(4, zone.getType());
            stmt.setString(5, zone.getParentId());
            stmt.setString(6, zone.getStatus());
            stmt.setDouble(7, zone.getPowerUsageKw());
            stmt.setDouble(8, zone.getDailyConsumptionKwh());
            stmt.setInt(9, zone.getActiveSensors());
            stmt.setInt(10, zone.getTotalSensors());
            stmt.setInt(11, zone.getActiveStreetlights());
            stmt.setInt(12, zone.getActiveAlerts());
            stmt.setString(13, zone.getManager());
            if (zone.getFloors() != null) {
                stmt.setInt(14, zone.getFloors());
            } else {
                stmt.setNull(14, Types.INTEGER);
            }

            return stmt.executeUpdate() > 0;
        }
    }

    public boolean updateZoneStatus(String id, String status) throws SQLException {
        String sql = "UPDATE zones SET status = ? WHERE id = ?";
        try (Connection conn = DatabaseConfig.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {

            stmt.setString(1, status);
            stmt.setString(2, id);
            return stmt.executeUpdate() > 0;
        }
    }

    public boolean updateZoneStatusRecursively(String rootId, String status) throws SQLException {
        List<Zone> all = getAllZones();
        ZoneComponent rootComp = buildCompositeHierarchy(all, rootId);
        if (rootComp == null) {
            return false;
        }

        ZoneCommand cmd;
        if ("OFFLINE".equalsIgnoreCase(status) || "SHUTDOWN".equalsIgnoreCase(status)) {
            cmd = ZoneCommand.SHUTDOWN_POWER;
        } else if ("ISOLATED".equalsIgnoreCase(status)) {
            cmd = ZoneCommand.EMERGENCY_ISOLATE;
        } else {
            cmd = ZoneCommand.RESTORE_POWER;
        }

        rootComp.executeCommand(cmd);

        Map<String, ZoneComponent> stateMap = new HashMap<>();
        collectComponents(rootComp, stateMap);

        String sql = "UPDATE zones SET status = ?, power_usage_kw = ? WHERE id = ?";
        try (Connection conn = DatabaseConfig.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {

            for (Map.Entry<String, ZoneComponent> entry : stateMap.entrySet()) {
                ZoneComponent comp = entry.getValue();
                stmt.setString(1, comp.getStatus());
                stmt.setDouble(2, comp.getPowerConsumption());
                stmt.setString(3, entry.getKey());
                stmt.addBatch();
            }
            stmt.executeBatch();
            return true;
        }
    }

    private void collectComponents(ZoneComponent comp, Map<String, ZoneComponent> out) {
        if (comp == null) return;
        out.put(comp.getId(), comp);
        if (comp instanceof ZoneComposite) {
            for (ZoneComponent child : ((ZoneComposite) comp).getChildren()) {
                collectComponents(child, out);
            }
        }
    }

    private Zone mapResultSetToZone(ResultSet rs) throws SQLException {
        Zone z = new Zone();
        z.setId(rs.getString("id"));
        z.setName(rs.getString("name"));
        z.setCode(rs.getString("code"));
        z.setType(rs.getString("type"));
        z.setParentId(rs.getString("parent_id"));
        z.setStatus(rs.getString("status"));
        z.setPowerUsageKw(rs.getDouble("power_usage_kw"));
        z.setDailyConsumptionKwh(rs.getDouble("daily_consumption_kwh"));
        z.setActiveSensors(rs.getInt("active_sensors"));
        z.setTotalSensors(rs.getInt("total_sensors"));
        z.setActiveStreetlights(rs.getInt("active_streetlights"));
        z.setActiveAlerts(rs.getInt("active_alerts"));
        z.setManager(rs.getString("manager"));
        int floors = rs.getInt("floors");
        if (!rs.wasNull()) {
            z.setFloors(floors);
        }
        return z;
    }
}


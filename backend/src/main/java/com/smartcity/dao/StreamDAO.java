package com.smartcity.dao;

import com.smartcity.config.DatabaseConfig;
import com.smartcity.model.DataStream;
import com.smartcity.model.ProcessingLayer;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class StreamDAO {

    public List<DataStream> getAllStreams() throws SQLException {
        List<DataStream> streams = new ArrayList<>();
        String sql = "SELECT * FROM data_streams ORDER BY id ASC";

        try (Connection conn = DatabaseConfig.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql);
             ResultSet rs = stmt.executeQuery()) {

            while (rs.next()) {
                DataStream stream = mapResultSetToStream(rs);
                stream.setPipelineLayers(getLayersForStream(conn, stream.getId()));
                streams.add(stream);
            }
        }
        return streams;
    }

    public DataStream getStreamById(String id) throws SQLException {
        String sql = "SELECT * FROM data_streams WHERE id = ?";
        try (Connection conn = DatabaseConfig.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {

            stmt.setString(1, id);
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    DataStream stream = mapResultSetToStream(rs);
                    stream.setPipelineLayers(getLayersForStream(conn, stream.getId()));
                    return stream;
                }
            }
        }
        return null;
    }

    public boolean createStream(DataStream stream) throws SQLException {
        String sql = "INSERT INTO data_streams (id, name, source_zone_id, source_zone_name, meter_count, status, voltage, current_amps, power_kw, frequency_hz, power_factor, total_kwh, packets_processed, avg_latency_ms, error_rate_percent) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";

        try (Connection conn = DatabaseConfig.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {

            stmt.setString(1, stream.getId());
            stmt.setString(2, stream.getName());
            stmt.setString(3, stream.getSourceZoneId());
            stmt.setString(4, stream.getSourceZoneName());
            stmt.setInt(5, stream.getMeterCount());
            stmt.setString(6, stream.getStatus());
            stmt.setDouble(7, stream.getVoltage());
            stmt.setDouble(8, stream.getCurrentAmps());
            stmt.setDouble(9, stream.getPowerKw());
            stmt.setDouble(10, stream.getFrequencyHz());
            stmt.setDouble(11, stream.getPowerFactor());
            stmt.setDouble(12, stream.getTotalKwh());
            stmt.setLong(13, stream.getPacketsProcessed());
            stmt.setDouble(14, stream.getAvgLatencyMs());
            stmt.setDouble(15, stream.getErrorRatePercent());

            boolean ok = stmt.executeUpdate() > 0;
            if (ok && stream.getPipelineLayers() != null) {
                saveLayers(conn, stream.getId(), stream.getPipelineLayers());
            }
            return ok;
        }
    }

    public boolean updateLayers(String streamId, List<ProcessingLayer> layers) throws SQLException {
        try (Connection conn = DatabaseConfig.getConnection()) {
            conn.setAutoCommit(false);
            try {
                String deleteSql = "DELETE FROM stream_layers WHERE stream_id = ?";
                try (PreparedStatement delStmt = conn.prepareStatement(deleteSql)) {
                    delStmt.setString(1, streamId);
                    delStmt.executeUpdate();
                }

                saveLayers(conn, streamId, layers);
                conn.commit();
                return true;
            } catch (SQLException e) {
                conn.rollback();
                throw e;
            } finally {
                conn.setAutoCommit(true);
            }
        }
    }

    private void saveLayers(Connection conn, String streamId, List<ProcessingLayer> layers) throws SQLException {
        String insertSql = "INSERT INTO stream_layers (id, stream_id, layer_type, layer_name, enabled, layer_order, algorithm) VALUES (?, ?, ?, ?, ?, ?, ?)";
        try (PreparedStatement stmt = conn.prepareStatement(insertSql)) {
            for (int i = 0; i < layers.size(); i++) {
                ProcessingLayer l = layers.get(i);
                stmt.setString(1, l.getId() != null ? l.getId() : "LAY-" + System.currentTimeMillis() + "-" + i);
                stmt.setString(2, streamId);
                stmt.setString(3, l.getLayerType());
                stmt.setString(4, l.getLayerName());
                stmt.setBoolean(5, l.isEnabled());
                stmt.setInt(6, l.getLayerOrder() > 0 ? l.getLayerOrder() : i + 1);
                stmt.setString(7, l.getAlgorithm());
                stmt.addBatch();
            }
            stmt.executeBatch();
        }
    }

    private List<ProcessingLayer> getLayersForStream(Connection conn, String streamId) throws SQLException {
        List<ProcessingLayer> list = new ArrayList<>();
        String sql = "SELECT * FROM stream_layers WHERE stream_id = ? ORDER BY layer_order ASC";

        try (PreparedStatement stmt = conn.prepareStatement(sql)) {
            stmt.setString(1, streamId);
            try (ResultSet rs = stmt.executeQuery()) {
                while (rs.next()) {
                    ProcessingLayer l = new ProcessingLayer();
                    l.setId(rs.getString("id"));
                    l.setStreamId(rs.getString("stream_id"));
                    l.setLayerType(rs.getString("layer_type"));
                    l.setLayerName(rs.getString("layer_name"));
                    l.setEnabled(rs.getBoolean("enabled"));
                    l.setLayerOrder(rs.getInt("layer_order"));
                    l.setAlgorithm(rs.getString("algorithm"));
                    list.add(l);
                }
            }
        }
        return list;
    }

    private DataStream mapResultSetToStream(ResultSet rs) throws SQLException {
        DataStream s = new DataStream();
        s.setId(rs.getString("id"));
        s.setName(rs.getString("name"));
        s.setSourceZoneId(rs.getString("source_zone_id"));
        s.setSourceZoneName(rs.getString("source_zone_name"));
        s.setMeterCount(rs.getInt("meter_count"));
        s.setStatus(rs.getString("status"));
        s.setVoltage(rs.getDouble("voltage"));
        s.setCurrentAmps(rs.getDouble("current_amps"));
        s.setPowerKw(rs.getDouble("power_kw"));
        s.setFrequencyHz(rs.getDouble("frequency_hz"));
        s.setPowerFactor(rs.getDouble("power_factor"));
        s.setTotalKwh(rs.getDouble("total_kwh"));
        s.setPacketsProcessed(rs.getLong("packets_processed"));
        s.setAvgLatencyMs(rs.getDouble("avg_latency_ms"));
        s.setErrorRatePercent(rs.getDouble("error_rate_percent"));
        s.setLastProcessedAt(rs.getString("last_processed_at"));
        return s;
    }
}


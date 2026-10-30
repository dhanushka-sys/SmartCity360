package com.smartcity.dao;

import com.smartcity.config.DatabaseConfig;
import com.smartcity.model.Complaint;
import com.smartcity.model.ComplaintNote;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class ComplaintDAO {

    public List<Complaint> getAllComplaints() throws SQLException {
        List<Complaint> list = new ArrayList<>();
        String sql = "SELECT * FROM complaints ORDER BY submitted_at DESC";

        try (Connection conn = DatabaseConfig.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql);
             ResultSet rs = stmt.executeQuery()) {

            while (rs.next()) {
                Complaint c = mapResultSetToComplaint(rs);
                c.setNotes(getNotesForComplaint(conn, c.getId()));
                list.add(c);
            }
        }
        return list;
    }

    public Complaint getComplaintById(String id) throws SQLException {
        String sql = "SELECT * FROM complaints WHERE id = ?";
        try (Connection conn = DatabaseConfig.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {

            stmt.setString(1, id);
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    Complaint c = mapResultSetToComplaint(rs);
                    c.setNotes(getNotesForComplaint(conn, c.getId()));
                    return c;
                }
            }
        }
        return null;
    }

    public boolean createComplaint(Complaint c) throws SQLException {
        String sql = "INSERT INTO complaints (id, tracking_number, title, description, category, severity, zone_id, zone_name, citizen_name, citizen_contact, current_handler_role, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";

        try (Connection conn = DatabaseConfig.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {

            stmt.setString(1, c.getId());
            stmt.setString(2, c.getTrackingNumber());
            stmt.setString(3, c.getTitle());
            stmt.setString(4, c.getDescription());
            stmt.setString(5, c.getCategory());
            stmt.setString(6, c.getSeverity());
            stmt.setString(7, c.getZoneId());
            stmt.setString(8, c.getZoneName());
            stmt.setString(9, c.getCitizenName());
            stmt.setString(10, c.getCitizenContact());
            stmt.setString(11, c.getCurrentHandlerRole());
            stmt.setString(12, c.getStatus());

            return stmt.executeUpdate() > 0;
        }
    }

    public boolean escalateComplaint(String id, String toRole, String noteText, String author) throws SQLException {
        String updateSql = "UPDATE complaints SET current_handler_role = ?, status = 'ESCALATED' WHERE id = ?";
        try (Connection conn = DatabaseConfig.getConnection()) {
            conn.setAutoCommit(false);
            try {
                try (PreparedStatement stmt = conn.prepareStatement(updateSql)) {
                    stmt.setString(1, toRole);
                    stmt.setString(2, id);
                    stmt.executeUpdate();
                }

                if (noteText != null && !noteText.trim().isEmpty()) {
                    addNoteInternal(conn, "NOT-" + System.currentTimeMillis(), id, author, toRole, noteText);
                }
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

    public boolean resolveComplaint(String id, String resolutionSummary) throws SQLException {
        String sql = "UPDATE complaints SET status = 'RESOLVED', resolution_summary = ?, resolved_at = NOW() WHERE id = ?";
        try (Connection conn = DatabaseConfig.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {

            stmt.setString(1, resolutionSummary);
            stmt.setString(2, id);
            return stmt.executeUpdate() > 0;
        }
    }

    public boolean addNote(String complaintId, String author, String role, String text) throws SQLException {
        try (Connection conn = DatabaseConfig.getConnection()) {
            return addNoteInternal(conn, "NOT-" + System.currentTimeMillis(), complaintId, author, role, text);
        }
    }

    private boolean addNoteInternal(Connection conn, String noteId, String complaintId, String author, String role, String text) throws SQLException {
        String sql = "INSERT INTO complaint_notes (id, complaint_id, author, role, text) VALUES (?, ?, ?, ?, ?)";
        try (PreparedStatement stmt = conn.prepareStatement(sql)) {
            stmt.setString(1, noteId);
            stmt.setString(2, complaintId);
            stmt.setString(3, author);
            stmt.setString(4, role);
            stmt.setString(5, text);
            return stmt.executeUpdate() > 0;
        }
    }

    private List<ComplaintNote> getNotesForComplaint(Connection conn, String complaintId) throws SQLException {
        List<ComplaintNote> list = new ArrayList<>();
        String sql = "SELECT * FROM complaint_notes WHERE complaint_id = ? ORDER BY created_at ASC";

        try (PreparedStatement stmt = conn.prepareStatement(sql)) {
            stmt.setString(1, complaintId);
            try (ResultSet rs = stmt.executeQuery()) {
                while (rs.next()) {
                    ComplaintNote n = new ComplaintNote();
                    n.setId(rs.getString("id"));
                    n.setComplaintId(rs.getString("complaint_id"));
                    n.setAuthor(rs.getString("author"));
                    n.setRole(rs.getString("role"));
                    n.setText(rs.getString("text"));
                    n.setCreatedAt(rs.getString("created_at"));
                    list.add(n);
                }
            }
        }
        return list;
    }

    private Complaint mapResultSetToComplaint(ResultSet rs) throws SQLException {
        Complaint c = new Complaint();
        c.setId(rs.getString("id"));
        c.setTrackingNumber(rs.getString("tracking_number"));
        c.setTitle(rs.getString("title"));
        c.setDescription(rs.getString("description"));
        c.setCategory(rs.getString("category"));
        c.setSeverity(rs.getString("severity"));
        c.setZoneId(rs.getString("zone_id"));
        c.setZoneName(rs.getString("zone_name"));
        c.setCitizenName(rs.getString("citizen_name"));
        c.setCitizenContact(rs.getString("citizen_contact"));
        c.setCurrentHandlerRole(rs.getString("current_handler_role"));
        c.setStatus(rs.getString("status"));
        c.setSubmittedAt(rs.getString("submitted_at"));
        c.setResolutionSummary(rs.getString("resolution_summary"));
        c.setResolvedAt(rs.getString("resolved_at"));
        return c;
    }
}


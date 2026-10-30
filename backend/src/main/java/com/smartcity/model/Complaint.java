package com.smartcity.model;

import java.util.ArrayList;
import java.util.List;

public class Complaint {

    private String id;
    private String trackingNumber;
    private String title;
    private String description;
    private String category;
    private String severity;
    private String zoneId;
    private String zoneName;
    private String citizenName;
    private String citizenContact;
    private String currentHandlerRole;
    private String status;
    private String submittedAt;
    private String resolutionSummary;
    private String resolvedAt;
    private List<ComplaintNote> notes = new ArrayList<>();

    public Complaint() {}

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getTrackingNumber() {
        return trackingNumber;
    }

    public void setTrackingNumber(String trackingNumber) {
        this.trackingNumber = trackingNumber;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getCategory() {
        return category;
    }

    public void setCategory(String category) {
        this.category = category;
    }

    public String getSeverity() {
        return severity;
    }

    public void setSeverity(String severity) {
        this.severity = severity;
    }

    public String getZoneId() {
        return zoneId;
    }

    public void setZoneId(String zoneId) {
        this.zoneId = zoneId;
    }

    public String getZoneName() {
        return zoneName;
    }

    public void setZoneName(String zoneName) {
        this.zoneName = zoneName;
    }

    public String getCitizenName() {
        return citizenName;
    }

    public void setCitizenName(String citizenName) {
        this.citizenName = citizenName;
    }

    public String getCitizenContact() {
        return citizenContact;
    }

    public void setCitizenContact(String citizenContact) {
        this.citizenContact = citizenContact;
    }

    public String getCurrentHandlerRole() {
        return currentHandlerRole;
    }

    public void setCurrentHandlerRole(String currentHandlerRole) {
        this.currentHandlerRole = currentHandlerRole;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public String getSubmittedAt() {
        return submittedAt;
    }

    public void setSubmittedAt(String submittedAt) {
        this.submittedAt = submittedAt;
    }

    public String getResolutionSummary() {
        return resolutionSummary;
    }

    public void setResolutionSummary(String resolutionSummary) {
        this.resolutionSummary = resolutionSummary;
    }

    public String getResolvedAt() {
        return resolvedAt;
    }

    public void setResolvedAt(String resolvedAt) {
        this.resolvedAt = resolvedAt;
    }

    public List<ComplaintNote> getNotes() {
        return notes;
    }

    public void setNotes(List<ComplaintNote> notes) {
        this.notes = notes;
    }
}


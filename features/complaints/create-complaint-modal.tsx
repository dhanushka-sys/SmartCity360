"use client";

import * as React from "react";
import { Modal } from "@/components/ui/modal";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import {
  CitizenComplaint,
  ComplaintCategory,
  ComplaintSeverity,
} from "@/types/complaint";
import { ComplaintsService } from "@/lib/api/complaints-service";

interface CreateComplaintModalProps {
  isOpen: boolean;
  onClose: () => void;
  onCreated: (complaint: CitizenComplaint) => void;
}

export function CreateComplaintModal({
  isOpen,
  onClose,
  onCreated,
}: CreateComplaintModalProps) {
  const [title, setTitle] = React.useState("");
  const [description, setDescription] = React.useState("");
  const [category, setCategory] = React.useState<ComplaintCategory>("INFRASTRUCTURE");
  const [severity, setSeverity] = React.useState<ComplaintSeverity>("MEDIUM");
  const [zone, setZone] = React.useState("ZN-STR-0101");
  const [citizenName, setCitizenName] = React.useState("Marcus Sterling");
  const [citizenContact, setCitizenContact] = React.useState("m.sterling@metromail.net");
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim() || !description.trim()) {
      setError("Title and description are required");
      return;
    }
    setError("");
    setLoading(true);

    try {
      const zoneNames: Record<string, string> = {
        "ZN-STR-0101": "Grand Horizon Avenue",
        "ZN-STR-0102": "Liberty Boulevard",
        "ZN-STR-0201": "Turing Way",
        "ZN-STR-0202": "Silicon Promenade",
        "ZN-STR-0301": "Docklands Wharfway",
      };

      const created = await ComplaintsService.createComplaint({
        title,
        description,
        category,
        severity,
        zoneId: zone,
        zoneName: zoneNames[zone] || "Downtown Core",
        citizenName,
        citizenContact,
      });

      onCreated(created);
      onClose();
      setTitle("");
      setDescription("");
    } catch (err: any) {
      setError(err?.message || "Failed to submit complaint");
    } finally {
      setLoading(false);
    }
  };

  const getPredictedHandler = () => {
    if (severity === "LOW" || severity === "MEDIUM") return "Local Staff Handler";
    if (severity === "HIGH") return "Supervisor Handler (Escalated)";
    return "City Manager Executive (Critical Escalation)";
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="File Citizen Incident Complaint"
      description="Submits an issue into the automated Chain of Responsibility handler routing."
      maxWidth="md"
      footer={
        <>
          <Button variant="secondary" onClick={onClose} disabled={loading}>
            Cancel
          </Button>
          <Button onClick={handleSubmit} disabled={loading}>
            {loading ? "Routing Along Chain..." : "Submit Ticket"}
          </Button>
        </>
      }
    >
      <form onSubmit={handleSubmit} className="space-y-4">
        <Input
          label="Incident Title"
          placeholder="e.g. Broken water main flooding intersection"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          error={error}
        />

        <div className="space-y-1.5">
          <label className="block text-xs font-medium text-slate-700 dark:text-slate-300">Description</label>
          <textarea
            className="w-full rounded-lg border border-slate-300 dark:border-slate-700/80 bg-white dark:bg-slate-950/60 p-2.5 text-xs text-slate-900 dark:text-white placeholder:text-slate-400 dark:placeholder:text-slate-500 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-cyan-500/50 shadow-xs"
            rows={3}
            placeholder="Detailed description of the incident..."
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
        </div>

        <div className="grid grid-cols-2 gap-3">
          <Select
            label="Category"
            value={category}
            onChange={(e) => setCategory(e.target.value as ComplaintCategory)}
            options={[
              { label: "Infrastructure", value: "INFRASTRUCTURE" },
              { label: "Noise Pollution", value: "NOISE" },
              { label: "Traffic Flow", value: "TRAFFIC" },
              { label: "Smart Waste", value: "WASTE" },
              { label: "Public Safety", value: "PUBLIC_SAFETY" },
              { label: "Environment & Air", value: "ENVIRONMENT" },
            ]}
          />

          <Select
            label="Severity Level"
            value={severity}
            onChange={(e) => setSeverity(e.target.value as ComplaintSeverity)}
            options={[
              { label: "Low (Local Staff)", value: "LOW" },
              { label: "Medium (Local Staff)", value: "MEDIUM" },
              { label: "High (Supervisor)", value: "HIGH" },
              { label: "Critical (City Manager)", value: "CRITICAL" },
            ]}
          />
        </div>

        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950/50 p-3 text-xs">
          <span className="text-slate-500 dark:text-slate-400">Chain of Responsibility Route Target:</span>
          <p className="font-semibold text-cyan-700 dark:text-cyan-300 mt-0.5">{getPredictedHandler()}</p>
          <p className="text-[11px] text-slate-500 dark:text-slate-400 mt-1">
            Handler is determined dynamically by severity threshold rules without client coupling.
          </p>
        </div>

        <div className="grid grid-cols-2 gap-3">
          <Input
            label="Citizen Name"
            value={citizenName}
            onChange={(e) => setCitizenName(e.target.value)}
          />
          <Input
            label="Contact Email"
            value={citizenContact}
            onChange={(e) => setCitizenContact(e.target.value)}
          />
        </div>
      </form>
    </Modal>
  );
}

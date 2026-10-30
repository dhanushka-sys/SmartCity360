"use client";

import * as React from "react";
import { Modal } from "@/components/ui/modal";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import { ZoneNode, ZoneType } from "@/types/zone";
import { ZonesService } from "@/lib/api/zones-service";

interface CreateZoneModalProps {
  isOpen: boolean;
  onClose: () => void;
  parentNode: ZoneNode;
  onCreated: (node: ZoneNode) => void;
}

export function CreateZoneModal({
  isOpen,
  onClose,
  parentNode,
  onCreated,
}: CreateZoneModalProps) {
  const [name, setName] = React.useState("");
  const [code, setCode] = React.useState("");
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState("");

  const getChildType = (): ZoneType => {
    if (parentNode.type === "CITY") return "DISTRICT";
    if (parentNode.type === "DISTRICT") return "STREET";
    return "BUILDING";
  };

  const childType = getChildType();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) {
      setError("Name is required");
      return;
    }
    setError("");
    setLoading(true);

    try {
      const generatedCode = code.trim() || `${childType.slice(0, 3)}-${name.slice(0, 3).toUpperCase()}`;
      const created = await ZonesService.addNode(parentNode.id, {
        name,
        code: generatedCode,
        type: childType,
        status: "OPERATIONAL",
        metrics: {
          currentPowerUsageKw: Math.floor(100 + Math.random() * 400),
          dailyConsumptionKwh: Math.floor(2000 + Math.random() * 8000),
          activeSensors: Math.floor(50 + Math.random() * 200),
          totalSensors: Math.floor(60 + Math.random() * 210),
          activeStreetlights: Math.floor(20 + Math.random() * 100),
          activeAlerts: 0,
        },
      });

      onCreated(created);
      onClose();
      setName("");
      setCode("");
    } catch (err: any) {
      setError(err?.message || "Failed to add zone");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title={`Add Sub-Component to ${parentNode.name}`}
      description={`Attaching new ${childType} node into the Composite tree under ${parentNode.type}.`}
      maxWidth="md"
      footer={
        <>
          <Button variant="secondary" onClick={onClose} disabled={loading}>
            Cancel
          </Button>
          <Button onClick={handleSubmit} disabled={loading}>
            {loading ? "Adding..." : "Add to Tree"}
          </Button>
        </>
      }
    >
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950/60 p-3 text-xs">
          <p className="text-slate-500 dark:text-slate-400">Parent Composite Node:</p>
          <p className="font-semibold text-slate-900 dark:text-white mt-0.5">{parentNode.name} ({parentNode.type})</p>
          <p className="text-cyan-700 dark:text-cyan-400 mt-1 font-medium">New Child Type: {childType}</p>
        </div>

        <Input
          label="Component Name"
          placeholder={`e.g. ${childType === "DISTRICT" ? "Harbor Commercial Zone" : childType === "STREET" ? "Beacon Way" : "Civic Center Annex"}`}
          value={name}
          onChange={(e) => setName(e.target.value)}
          error={error}
        />

        <Input
          label="Component Code (Optional)"
          placeholder="e.g. BLD-CCA"
          value={code}
          onChange={(e) => setCode(e.target.value)}
          hint="Short identifier used in telemetry routing."
        />
      </form>
    </Modal>
  );
}

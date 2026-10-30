"use client";

import * as React from "react";
import { Modal } from "@/components/ui/modal";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import { DataStream } from "@/types/data-stream";
import { StreamsService } from "@/lib/api/streams-service";

interface CreateStreamModalProps {
  isOpen: boolean;
  onClose: () => void;
  onCreated: (stream: DataStream) => void;
}

export function CreateStreamModal({ isOpen, onClose, onCreated }: CreateStreamModalProps) {
  const [name, setName] = React.useState("");
  const [zone, setZone] = React.useState("ZN-DIST-01");
  const [meterCount, setMeterCount] = React.useState("500");
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) {
      setError("Stream name is required");
      return;
    }
    setError("");
    setLoading(true);

    try {
      const zoneNames: Record<string, string> = {
        "ZN-DIST-01": "Downtown Financial Core",
        "ZN-DIST-02": "Cyber Park Innovation Hub",
        "ZN-DIST-03": "Ocean Gateway Logistics",
      };

      const newStream = await StreamsService.createStream({
        name,
        sourceZoneId: zone,
        sourceZoneName: zoneNames[zone] || "Downtown Core",
        meterCount: Number(meterCount) || 250,
        status: "ACTIVE",
        samplePayload: {
          meterId: `EM-GEN-${Math.floor(100 + Math.random() * 900)}`,
          timestamp: new Date().toISOString(),
          voltage: 230.1,
          currentAmps: 15.4,
          powerKw: 3.54,
          frequencyHz: 50.0,
          powerFactor: 0.97,
          totalKwh: 5200.0,
        },
        pipelineLayers: [
          {
            id: `lay-${Math.random().toString(36).substring(2, 7)}`,
            type: "AUTHENTICATION",
            name: "HMAC-SHA256 Token Decorator",
            enabled: true,
            order: 1,
            params: { signatureScheme: "HMAC-SHA256", keyId: "KEY-VAULT-NEW" },
          },
          {
            id: `lay-${Math.random().toString(36).substring(2, 7)}`,
            type: "ENCRYPTION",
            name: "AES-256-GCM Envelope Decorator",
            enabled: true,
            order: 2,
            params: { algorithm: "AES-GCM-256", keyId: "VAULT-MASTER-01" },
          },
        ],
      });

      onCreated(newStream);
      onClose();
      setName("");
    } catch (err: any) {
      setError(err?.message || "Failed to create stream");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="Register New Energy Meter Stream"
      description="Initializes a new CoreDataStream component with default security decorators."
      maxWidth="md"
      footer={
        <>
          <Button variant="secondary" onClick={onClose} disabled={loading}>
            Cancel
          </Button>
          <Button onClick={handleSubmit} disabled={loading}>
            {loading ? "Registering..." : "Create Stream"}
          </Button>
        </>
      }
    >
      <form onSubmit={handleSubmit} className="space-y-4">
        <Input
          label="Stream Feed Name"
          placeholder="e.g. Industrial Harbor Microgrid Feed"
          value={name}
          onChange={(e) => setName(e.target.value)}
          error={error}
        />

        <Select
          label="Target Source Zone"
          value={zone}
          onChange={(e) => setZone(e.target.value)}
          options={[
            { label: "Downtown Financial Core (ZN-DIST-01)", value: "ZN-DIST-01" },
            { label: "Cyber Park Innovation Hub (ZN-DIST-02)", value: "ZN-DIST-02" },
            { label: "Ocean Gateway Logistics (ZN-DIST-03)", value: "ZN-DIST-03" },
          ]}
        />

        <Input
          label="Total Aggregated Sub-Meters"
          type="number"
          value={meterCount}
          onChange={(e) => setMeterCount(e.target.value)}
          hint="Number of IoT meters reporting through this primary pipeline."
        />
      </form>
    </Modal>
  );
}


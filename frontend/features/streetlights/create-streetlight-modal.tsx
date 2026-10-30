"use client";

import * as React from "react";
import { Modal } from "@/components/ui/modal";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import { Streetlight, StreetlightProfile } from "@/types/streetlight";
import { StreetlightsService } from "@/lib/api/streetlights-service";

interface CreateStreetlightModalProps {
  isOpen: boolean;
  onClose: () => void;
  profiles: StreetlightProfile[];
  onCreated: (light: Streetlight) => void;
}

export function CreateStreetlightModal({
  isOpen,
  onClose,
  profiles,
  onCreated,
}: CreateStreetlightModalProps) {
  const [profileId, setProfileId] = React.useState(profiles[0]?.id || "");
  const [streetName, setStreetName] = React.useState("");
  const [zone, setZone] = React.useState("ZN-STR-0101");
  const [poleHeight, setPoleHeight] = React.useState("8.5");
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!streetName.trim()) {
      setError("Street location is required");
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

      const created = await StreetlightsService.createStreetlight({
        profileId,
        zoneId: zone,
        zoneName: zoneNames[zone] || "Downtown Core",
        streetName,
        latitude: 40.7128 + (Math.random() - 0.5) * 0.02,
        longitude: -74.006 + (Math.random() - 0.5) * 0.02,
        poleHeightMeters: Number(poleHeight) || 8.5,
      });

      onCreated(created);
      onClose();
      setStreetName("");
    } catch (err: any) {
      setError(err?.message || "Failed to create streetlight");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="Register New Smart Streetlight"
      description="Allocates light instance with unique extrinsic coordinates referencing a shared Flyweight profile."
      maxWidth="md"
      footer={
        <>
          <Button variant="secondary" onClick={onClose} disabled={loading}>
            Cancel
          </Button>
          <Button onClick={handleSubmit} disabled={loading}>
            {loading ? "Allocating..." : "Register Light"}
          </Button>
        </>
      }
    >
      <form onSubmit={handleSubmit} className="space-y-4">
        <Select
          label="Shared Intrinsic Profile (Flyweight)"
          value={profileId}
          onChange={(e) => setProfileId(e.target.value)}
          options={profiles.map((p) => ({
            label: `${p.modelName} (${p.wattageRatingWatts}W)`,
            value: p.id,
          }))}
        />

        <Input
          label="Street Pole Location Label"
          placeholder="e.g. Grand Horizon Ave #120"
          value={streetName}
          onChange={(e) => setStreetName(e.target.value)}
          error={error}
        />

        <div className="grid grid-cols-2 gap-3">
          <Select
            label="Zone"
            value={zone}
            onChange={(e) => setZone(e.target.value)}
            options={[
              { label: "Grand Horizon Ave (ZN-STR-0101)", value: "ZN-STR-0101" },
              { label: "Liberty Boulevard (ZN-STR-0102)", value: "ZN-STR-0102" },
              { label: "Silicon Promenade (ZN-STR-0202)", value: "ZN-STR-0202" },
              { label: "Docklands Wharfway (ZN-STR-0301)", value: "ZN-STR-0301" },
            ]}
          />

          <Input
            label="Pole Height (Meters)"
            type="number"
            step="0.5"
            value={poleHeight}
            onChange={(e) => setPoleHeight(e.target.value)}
          />
        </div>
      </form>
    </Modal>
  );
}


"use client";

import * as React from "react";
import { Modal } from "@/components/ui/modal";
import { Button } from "@/components/ui/button";
import { Select } from "@/components/ui/select";
import { StreetlightProfile } from "@/types/streetlight";
import { StreetlightsService } from "@/lib/api/streetlights-service";

interface BulkAssignModalProps {
  isOpen: boolean;
  onClose: () => void;
  selectedLightIds: string[];
  profiles: StreetlightProfile[];
  onAssigned: () => void;
}

export function BulkAssignModal({
  isOpen,
  onClose,
  selectedLightIds,
  profiles,
  onAssigned,
}: BulkAssignModalProps) {
  const [profileId, setProfileId] = React.useState(profiles[0]?.id || "");
  const [loading, setLoading] = React.useState(false);

  const handleAssign = async () => {
    if (!profileId) return;
    setLoading(true);
    try {
      await StreetlightsService.bulkAssignProfile(selectedLightIds, profileId);
      onAssigned();
      onClose();
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="Bulk Assign Flyweight Profile"
      description={`Re-assign ${selectedLightIds.length} streetlights to a shared intrinsic configuration.`}
      maxWidth="md"
      footer={
        <>
          <Button variant="secondary" onClick={onClose} disabled={loading}>
            Cancel
          </Button>
          <Button onClick={handleAssign} disabled={loading}>
            {loading ? "Re-pointing..." : `Re-assign (${selectedLightIds.length}) Lights`}
          </Button>
        </>
      }
    >
      <div className="space-y-4 text-xs">
        <Select
          label="Target Shared Flyweight Profile"
          value={profileId}
          onChange={(e) => setProfileId(e.target.value)}
          options={profiles.map((p) => ({
            label: `${p.modelName} (${p.wattageRatingWatts}W - ${p.lampType})`,
            value: p.id,
          }))}
        />

        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950/60 p-3 text-[11px] text-slate-600 dark:text-slate-400 leading-relaxed">
          <p className="font-semibold text-slate-800 dark:text-slate-300">Flyweight Benefit in Bulk Operations:</p>
          <p className="mt-1">
            Updating configuration for {selectedLightIds.length} lights simply repoints their internal
            profile reference in memory, avoiding memory reallocation for schedules, optical curves, and hardware metadata.
          </p>
        </div>
      </div>
    </Modal>
  );
}

"use client";

import * as React from "react";
import { Modal } from "@/components/ui/modal";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Streetlight, StreetlightProfile } from "@/types/streetlight";
import { StreetlightsService } from "@/lib/api/streetlights-service";
import { formatDate } from "@/lib/utils";

interface StreetlightDetailModalProps {
  isOpen: boolean;
  onClose: () => void;
  streetlight: Streetlight;
  profile?: StreetlightProfile;
  onUpdated: (light: Streetlight) => void;
}

export function StreetlightDetailModal({
  isOpen,
  onClose,
  streetlight,
  profile,
  onUpdated,
}: StreetlightDetailModalProps) {
  const [loading, setLoading] = React.useState(false);

  const handleToggleStatus = async (newStatus: any) => {
    setLoading(true);
    try {
      const updated = await StreetlightsService.updateStatus(streetlight.id, newStatus);
      onUpdated(updated);
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
      title={`Streetlight ${streetlight.serialNumber}`}
      description={`Location: ${streetlight.streetName} (${streetlight.zoneName})`}
      maxWidth="md"
      footer={
        <Button variant="secondary" onClick={onClose}>
          Close
        </Button>
      }
    >
      <div className="space-y-4 text-xs">
        {/* Extrinsic vs Intrinsic State Separation Card */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {/* Extrinsic State */}
          <div className="rounded-xl border border-cyan-200 dark:border-cyan-500/30 bg-cyan-50/70 dark:bg-cyan-950/20 p-3 space-y-2">
            <span className="text-[10px] font-bold uppercase tracking-wider text-cyan-800 dark:text-cyan-300">
              Extrinsic State (Unique to Pole)
            </span>
            <div className="space-y-1 text-slate-700 dark:text-slate-300 text-[11px]">
              <div className="flex justify-between">
                <span className="text-slate-500 dark:text-slate-400">Unit ID:</span>
                <span className="font-mono text-slate-900 dark:text-white font-medium">{streetlight.id}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500 dark:text-slate-400">Coordinates:</span>
                <span className="font-mono">{streetlight.latitude.toFixed(4)}, {streetlight.longitude.toFixed(4)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500 dark:text-slate-400">Pole Height:</span>
                <span>{streetlight.poleHeightMeters}m</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500 dark:text-slate-400">Current Output:</span>
                <span className="text-cyan-700 dark:text-cyan-300 font-semibold">{streetlight.currentBrightnessPercent}%</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500 dark:text-slate-400">Status:</span>
                <Badge
                  variant={
                    streetlight.status === "ONLINE"
                      ? "success"
                      : streetlight.status === "MAINTENANCE"
                      ? "warning"
                      : "danger"
                  }
                  dot
                >
                  {streetlight.status}
                </Badge>
              </div>
            </div>
          </div>

          {/* Intrinsic State */}
          <div className="rounded-xl border border-emerald-200 dark:border-emerald-500/30 bg-emerald-50/70 dark:bg-emerald-950/20 p-3 space-y-2">
            <span className="text-[10px] font-bold uppercase tracking-wider text-emerald-800 dark:text-emerald-300">
              Intrinsic State (Shared Flyweight)
            </span>
            {profile ? (
              <div className="space-y-1 text-slate-700 dark:text-slate-300 text-[11px]">
                <div className="flex justify-between">
                  <span className="text-slate-500 dark:text-slate-400">Profile ID:</span>
                  <span className="font-mono text-slate-900 dark:text-white font-medium">{profile.id}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500 dark:text-slate-400">Hardware Model:</span>
                  <span className="truncate max-w-[110px] font-semibold text-slate-900 dark:text-white">
                    {profile.modelName}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500 dark:text-slate-400">Power Rating:</span>
                  <span className="font-mono text-emerald-700 dark:text-emerald-300 font-semibold">{profile.wattageRatingWatts}W</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500 dark:text-slate-400">Lamp Technology:</span>
                  <span>{profile.lampType}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500 dark:text-slate-400">Optical Schedule:</span>
                  <span className="truncate max-w-[100px]">{profile.operatingSchedule}</span>
                </div>
              </div>
            ) : (
              <p className="text-[11px] text-slate-500 dark:text-slate-400">No profile attached.</p>
            )}
          </div>
        </div>

        {/* Status Action Controls */}
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950/50 p-3 space-y-2">
          <span className="text-xs font-semibold text-slate-800 dark:text-slate-300">Update Extrinsic Status:</span>
          <div className="flex items-center gap-2">
            <Button
              size="sm"
              variant={streetlight.status === "ONLINE" ? "default" : "outline"}
              onClick={() => handleToggleStatus("ONLINE")}
              disabled={loading}
              className="text-xs h-7"
            >
              Set Online
            </Button>
            <Button
              size="sm"
              variant={streetlight.status === "MAINTENANCE" ? "warning" : "outline"}
              onClick={() => handleToggleStatus("MAINTENANCE")}
              disabled={loading}
              className="text-xs h-7"
            >
              Set Maintenance
            </Button>
            <Button
              size="sm"
              variant={streetlight.status === "OFFLINE" ? "danger" : "outline"}
              onClick={() => handleToggleStatus("OFFLINE")}
              disabled={loading}
              className="text-xs h-7"
            >
              Set Offline
            </Button>
          </div>
        </div>
      </div>
    </Modal>
  );
}

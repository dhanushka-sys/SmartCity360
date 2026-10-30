"use client";

import * as React from "react";
import {
  Lightbulb,
  Search,
  Plus,
  Sliders,
  CheckSquare,
  Square,
  HardDrive,
  Cpu,
  Zap,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  FlyweightMemoryAnalysis,
  Streetlight,
  StreetlightProfile,
  StreetlightStatus,
} from "@/types/streetlight";
import { StreetlightsService } from "@/lib/api/streetlights-service";
import { FlyweightSavingsCard } from "@/features/streetlights/flyweight-savings-card";
import { ProfileListCard } from "@/features/streetlights/profile-list-card";
import { StreetlightDetailModal } from "@/features/streetlights/streetlight-detail-modal";
import { BulkAssignModal } from "@/features/streetlights/bulk-assign-modal";
import { CreateStreetlightModal } from "@/features/streetlights/create-streetlight-modal";
import { formatDate } from "@/lib/utils";
import { useAppMode } from "@/components/mode-provider";

export default function StreetlightsPage() {
  const { isAcademic } = useAppMode();
  const [streetlights, setStreetlights] = React.useState<Streetlight[]>([]);
  const [profiles, setProfiles] = React.useState<StreetlightProfile[]>([]);
  const [analysis, setAnalysis] = React.useState<FlyweightMemoryAnalysis | null>(null);
  const [selectedLight, setSelectedLight] = React.useState<Streetlight | null>(null);
  const [selectedIds, setSelectedIds] = React.useState<string[]>([]);
  const [searchQuery, setSearchQuery] = React.useState("");
  const [statusFilter, setStatusFilter] = React.useState<string>("ALL");
  const [profileFilter, setProfileFilter] = React.useState<string>("ALL");
  const [createModalOpen, setCreateModalOpen] = React.useState(false);
  const [bulkModalOpen, setBulkModalOpen] = React.useState(false);
  const [loading, setLoading] = React.useState(true);

  React.useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [lights, profs, anal] = await Promise.all([
        StreetlightsService.getStreetlights(),
        StreetlightsService.getProfiles(),
        StreetlightsService.getMemoryAnalysis(),
      ]);
      setStreetlights(lights);
      setProfiles(profs);
      setAnalysis(anal);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleToggleSelect = (id: string) => {
    setSelectedIds((prev) =>
      prev.includes(id) ? prev.filter((item) => item !== id) : [...prev, id]
    );
  };

  const handleSelectAll = () => {
    if (selectedIds.length === filteredLights.length) {
      setSelectedIds([]);
    } else {
      setSelectedIds(filteredLights.map((l) => l.id));
    }
  };

  const handleBulkStatus = async (status: StreetlightStatus) => {
    if (selectedIds.length === 0) return;
    await StreetlightsService.bulkUpdateStatus(selectedIds, status);
    loadData();
    setSelectedIds([]);
  };

  const filteredLights = streetlights.filter((light) => {
    const matchesSearch =
      light.serialNumber.toLowerCase().includes(searchQuery.toLowerCase()) ||
      light.streetName.toLowerCase().includes(searchQuery.toLowerCase()) ||
      light.zoneName.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesStatus = statusFilter === "ALL" || light.status === statusFilter;
    const matchesProfile = profileFilter === "ALL" || light.profileId === profileFilter;
    return matchesSearch && matchesStatus && matchesProfile;
  });

  return (
    <div className="space-y-6">
      {/* Pattern Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 rounded-xl border border-emerald-200 dark:border-emerald-500/30 bg-white dark:bg-slate-900/80 p-4 shadow-sm">
        <div>
          <div className="flex items-center gap-2">
            <span className="flex h-2 w-2 rounded-full bg-emerald-500" />
            <h2 className="text-base font-bold text-slate-900 dark:text-white tracking-tight">
              {isAcademic
                ? "Module D: Smart Streetlight Grid Management"
                : "Smart Streetlight Fleet Infrastructure"}
            </h2>
            <Badge variant="success" className="text-[10px]">
              {isAcademic ? "Flyweight Pattern" : "Municipal Lighting"}
            </Badge>
          </div>
          <p className="mt-1 text-xs text-slate-600 dark:text-slate-300">
            {isAcademic
              ? "Separating Intrinsic state (shared hardware profiles, wattage, schedules) from Extrinsic state (location coordinates, current brightness, online status) saves ~88.8% in object memory across 24,500 city poles."
              : "Centralized lighting grid management. Reusable hardware profiles reduce server memory and network bandwidth across 24,500 streetlights."}
          </p>
        </div>
        <Button
          onClick={() => setCreateModalOpen(true)}
          size="sm"
          className="gap-1.5 text-xs shrink-0"
        >
          <Plus className="h-4 w-4" />
          <span>New Streetlight</span>
        </Button>
      </div>

      {/* Flyweight Memory Savings Card */}
      {analysis && <FlyweightSavingsCard analysis={analysis} />}

      {/* Shared Profiles Pool */}
      <ProfileListCard profiles={profiles} />

      {/* Streetlights Inventory Table */}
      <Card className="border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/70 shadow-sm">
        <CardHeader className="pb-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
              <CardTitle className="text-sm md:text-base">Streetlight Instances Registry</CardTitle>
              <CardDescription>
                {isAcademic
                  ? "Physical light poles referencing cached Flyweight configuration profiles"
                  : "Physical light poles referencing centralized configuration profiles"}
              </CardDescription>
            </div>

            {/* Bulk Action Controls */}
            {selectedIds.length > 0 && (
              <div className="flex items-center gap-2 rounded-xl border border-cyan-200 dark:border-cyan-500/30 bg-cyan-50 dark:bg-cyan-950/30 p-1.5 px-3">
                <span className="text-xs font-semibold text-cyan-800 dark:text-cyan-300">
                  {selectedIds.length} Selected
                </span>
                <Button
                  size="sm"
                  variant="outline"
                  onClick={() => setBulkModalOpen(true)}
                  className="h-7 text-xs"
                >
                  Assign Profile
                </Button>
                <Button
                  size="sm"
                  variant="outline"
                  onClick={() => handleBulkStatus("ONLINE")}
                  className="h-7 text-xs text-emerald-600 dark:text-emerald-400"
                >
                  Turn On
                </Button>
                <Button
                  size="sm"
                  variant="outline"
                  onClick={() => handleBulkStatus("OFFLINE")}
                  className="h-7 text-xs text-slate-600 dark:text-slate-400"
                >
                  Turn Off
                </Button>
                <Button
                  size="sm"
                  variant="outline"
                  onClick={() => handleBulkStatus("MAINTENANCE")}
                  className="h-7 text-xs text-amber-600 dark:text-amber-400"
                >
                  Maintenance
                </Button>
              </div>
            )}
          </div>

          {/* Filters Bar */}
          <div className="mt-3 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 pt-2">
            <div className="relative">
              <Search className="absolute left-2.5 top-2.5 h-3.5 w-3.5 text-slate-400" />
              <Input
                placeholder="Search serial number, street, or zone..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-8 text-xs h-8"
              />
            </div>

            {/* Status Filter */}
            <div className="flex items-center gap-1 text-[11px] overflow-x-auto">
              <span className="text-slate-500 dark:text-slate-400 text-xs mr-1">Status:</span>
              {["ALL", "ONLINE", "OFFLINE", "MAINTENANCE"].map((st) => (
                <button
                  key={st}
                  onClick={() => setStatusFilter(st)}
                  className={`px-2 py-0.5 rounded-md font-medium transition-colors ${
                    statusFilter === st
                      ? "bg-slate-100 dark:bg-slate-800 text-cyan-700 dark:text-cyan-300 font-semibold"
                      : "text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200"
                  }`}
                >
                  {st}
                </button>
              ))}
            </div>

            {/* Profile Filter */}
            <div className="flex items-center gap-1 text-[11px] overflow-x-auto">
              <span className="text-slate-500 dark:text-slate-400 text-xs mr-1">Profile:</span>
              <button
                onClick={() => setProfileFilter("ALL")}
                className={`px-2 py-0.5 rounded-md font-medium transition-colors ${
                  profileFilter === "ALL"
                    ? "bg-slate-100 dark:bg-slate-800 text-cyan-700 dark:text-cyan-300 font-semibold"
                    : "text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200"
                }`}
              >
                ALL
              </button>
              {profiles.map((p) => (
                <button
                  key={p.id}
                  onClick={() => setProfileFilter(p.id)}
                  className={`px-2 py-0.5 rounded-md font-medium transition-colors truncate max-w-[120px] ${
                    profileFilter === p.id
                      ? "bg-slate-100 dark:bg-slate-800 text-cyan-700 dark:text-cyan-300 font-semibold"
                      : "text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200"
                  }`}
                  title={p.modelName}
                >
                  {p.modelName}
                </button>
              ))}
            </div>
          </div>
        </CardHeader>

        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-slate-200 dark:border-slate-800 text-[11px] font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">
                  <th className="pb-3 w-8">
                    <button
                      onClick={handleSelectAll}
                      className="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200"
                    >
                      {selectedIds.length === filteredLights.length && filteredLights.length > 0 ? (
                        <CheckSquare className="h-4 w-4 text-cyan-600 dark:text-cyan-400" />
                      ) : (
                        <Square className="h-4 w-4" />
                      )}
                    </button>
                  </th>
                  <th className="pb-3">Serial / ID</th>
                  <th className="pb-3">Location &amp; Street</th>
                  <th className="pb-3">Shared Profile Model</th>
                  <th className="pb-3">Wattage</th>
                  <th className="pb-3">Brightness</th>
                  <th className="pb-3">Status</th>
                  <th className="pb-3 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200 dark:divide-slate-800/60">
                {filteredLights.map((light) => {
                  const isSelected = selectedIds.includes(light.id);
                  const prof = profiles.find((p) => p.id === light.profileId);
                  return (
                    <tr
                      key={light.id}
                      onClick={() => setSelectedLight(light)}
                      className={`hover:bg-slate-50 dark:hover:bg-slate-800/40 transition-colors cursor-pointer ${
                        isSelected ? "bg-cyan-50/50 dark:bg-cyan-950/20" : ""
                      }`}
                    >
                      <td className="py-3" onClick={(e) => e.stopPropagation()}>
                        <button
                          onClick={() => handleToggleSelect(light.id)}
                          className="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200"
                        >
                          {isSelected ? (
                            <CheckSquare className="h-4 w-4 text-cyan-600 dark:text-cyan-400" />
                          ) : (
                            <Square className="h-4 w-4" />
                          )}
                        </button>
                      </td>
                      <td className="py-3 font-mono font-medium text-slate-900 dark:text-white">
                        {light.serialNumber}
                      </td>
                      <td className="py-3">
                        <p className="font-semibold text-slate-900 dark:text-white">{light.streetName}</p>
                        <p className="text-[11px] text-slate-500 dark:text-slate-400">{light.zoneName}</p>
                      </td>
                      <td className="py-3">
                        <span className="rounded-md border border-slate-200 dark:border-slate-700 bg-slate-100 dark:bg-slate-800 px-2 py-0.5 text-[11px] font-mono text-cyan-800 dark:text-cyan-300 font-semibold">
                          {prof?.modelName || light.profileId}
                        </span>
                      </td>
                      <td className="py-3 text-slate-700 dark:text-slate-300 font-mono">
                        {prof?.wattageRatingWatts || 150}W
                      </td>
                      <td className="py-3 font-mono">
                        <div className="flex items-center gap-2">
                          <div className="h-1.5 w-12 rounded-full bg-slate-200 dark:bg-slate-800 overflow-hidden">
                            <div
                              className="h-full bg-amber-400"
                              style={{ width: `${light.currentBrightnessPercent}%` }}
                            />
                          </div>
                          <span>{light.currentBrightnessPercent}%</span>
                        </div>
                      </td>
                      <td className="py-3">
                        <Badge
                          variant={
                            light.status === "ONLINE"
                              ? "success"
                              : light.status === "MAINTENANCE"
                              ? "warning"
                              : "default"
                          }
                          dot
                          className="text-[10px]"
                        >
                          {light.status}
                        </Badge>
                      </td>
                      <td className="py-3 text-right" onClick={(e) => e.stopPropagation()}>
                        <Button
                          size="sm"
                          variant="ghost"
                          onClick={() => setSelectedLight(light)}
                          className="h-7 text-xs text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white"
                        >
                          Inspect
                        </Button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>

            {filteredLights.length === 0 && (
              <div className="text-center py-12 text-xs text-slate-500 dark:text-slate-400">
                No streetlights match the filter criteria.
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Modal: Light Details */}
      {selectedLight && (
        <StreetlightDetailModal
          isOpen={!!selectedLight}
          onClose={() => setSelectedLight(null)}
          streetlight={selectedLight}
          profile={profiles.find((p) => p.id === selectedLight.profileId)}
          onUpdated={(updated) => {
            setStreetlights((prev) => prev.map((l) => (l.id === updated.id ? updated : l)));
            setSelectedLight(updated);
          }}
        />
      )}

      {/* Modal: Bulk Assign */}
      <BulkAssignModal
        isOpen={bulkModalOpen}
        onClose={() => setBulkModalOpen(false)}
        selectedLightIds={selectedIds}
        profiles={profiles}
        onAssigned={() => {
          loadData();
          setSelectedIds([]);
        }}
      />

      {/* Modal: Create Single Streetlight */}
      <CreateStreetlightModal
        isOpen={createModalOpen}
        onClose={() => setCreateModalOpen(false)}
        profiles={profiles}
        onCreated={(newLight) => {
          setStreetlights([newLight, ...streetlights]);
          setSelectedLight(newLight);
        }}
      />
    </div>
  );
}

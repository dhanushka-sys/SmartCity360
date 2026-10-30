"use client";

import * as React from "react";
import {
  Layers,
  Search,
  Plus,
  Play,
  CheckCircle2,
  AlertTriangle,
  RotateCcw,
  Zap,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { DataStream, ProcessingLayerConfig } from "@/types/data-stream";
import { StreamsService } from "@/lib/api/streams-service";
import { PipelineVisualizer } from "@/features/data-streams/pipeline-visualizer";
import { LayerConfigurator } from "@/features/data-streams/layer-configurator";
import { CreateStreamModal } from "@/features/data-streams/create-stream-modal";
import { useAppMode } from "@/components/mode-provider";

export default function DataStreamsPage() {
  const { isAcademic } = useAppMode();
  const [streams, setStreams] = React.useState<DataStream[]>([]);
  const [selectedStreamId, setSelectedStreamId] = React.useState<string | null>(null);
  const [searchQuery, setSearchQuery] = React.useState("");
  const [statusFilter, setStatusFilter] = React.useState<string>("ALL");
  const [createModalOpen, setCreateModalOpen] = React.useState(false);
  const [loading, setLoading] = React.useState(true);

  React.useEffect(() => {
    loadStreams();
  }, []);

  const loadStreams = async () => {
    setLoading(true);
    try {
      const data = await StreamsService.getStreams();
      setStreams(data);
      if (data.length > 0 && !selectedStreamId) {
        setSelectedStreamId(data[0].id);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleLayersChange = async (updatedLayers: ProcessingLayerConfig[]) => {
    if (!selectedStreamId) return;
    try {
      const updated = await StreamsService.updateLayers(selectedStreamId, updatedLayers);
      setStreams((prev) => prev.map((s) => (s.id === updated.id ? updated : s)));
    } catch (err) {
      console.error(err);
    }
  };

  const filteredStreams = streams.filter((stream) => {
    const matchesSearch =
      stream.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      stream.sourceZoneName.toLowerCase().includes(searchQuery.toLowerCase()) ||
      stream.id.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesStatus = statusFilter === "ALL" || stream.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  const selectedStream = streams.find((s) => s.id === selectedStreamId);

  return (
    <div className="space-y-6">
      {/* Pattern Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 rounded-xl border border-cyan-200 dark:border-cyan-500/30 bg-white dark:bg-slate-900/80 p-4 shadow-sm">
        <div>
          <div className="flex items-center gap-2">
            <span className="flex h-2 w-2 rounded-full bg-cyan-500" />
            <h2 className="text-base font-bold text-slate-900 dark:text-white tracking-tight">
              {isAcademic
                ? "Module A: Secure Energy Meter Data Streams"
                : "Secure Energy Meter Data Streams"}
            </h2>
            <Badge variant="info" className="text-[10px]">
              {isAcademic ? "Decorator Pattern" : "Enterprise Security"}
            </Badge>
          </div>
          <p className="mt-1 text-xs text-slate-600 dark:text-slate-300">
            {isAcademic
              ? "Composable processing wrappers (Encryption, Authentication, Compression) attach dynamically around raw stream components without altering core meter polling."
              : "Configure real-time security pipelines, payload encryption, authentication handshakes, and compression profiles for municipal grid energy meters."}
          </p>
        </div>
        <Button
          onClick={() => setCreateModalOpen(true)}
          size="sm"
          className="gap-1.5 text-xs shrink-0"
        >
          <Plus className="h-4 w-4" />
          <span>New Stream Feed</span>
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Stream Feeds List & Filters */}
        <div className="lg:col-span-5 space-y-4">
          <Card className="border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/70 shadow-sm">
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <CardTitle className="text-sm">Energy Meter Feeds</CardTitle>
                <span className="text-xs text-slate-500 dark:text-slate-400 font-mono">
                  {filteredStreams.length} registered
                </span>
              </div>
              <CardDescription>
                {isAcademic
                  ? "Select a stream to configure its decorator pipeline"
                  : "Select a stream to configure its security & compression pipeline"}
              </CardDescription>

              {/* Search & Filter Controls */}
              <div className="mt-2 space-y-2">
                <div className="relative">
                  <Search className="absolute left-2.5 top-2.5 h-3.5 w-3.5 text-slate-400" />
                  <Input
                    placeholder="Search by feed name or zone..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="pl-8 text-xs h-8"
                  />
                </div>
                <div className="flex items-center gap-1 text-[11px]">
                  {["ALL", "ACTIVE", "IDLE"].map((status) => (
                    <button
                      key={status}
                      onClick={() => setStatusFilter(status)}
                      className={`px-2 py-0.5 rounded-md font-medium transition-colors ${
                        statusFilter === status
                          ? "bg-slate-100 dark:bg-slate-800 text-cyan-700 dark:text-cyan-300 font-semibold"
                          : "text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200"
                      }`}
                    >
                      {status}
                    </button>
                  ))}
                </div>
              </div>
            </CardHeader>

            <CardContent className="space-y-2 max-h-[520px] overflow-y-auto">
              {filteredStreams.map((stream) => {
                const isSelected = stream.id === selectedStreamId;
                const activeLayersCount = stream.pipelineLayers.filter((l) => l.enabled).length;

                return (
                  <div
                    key={stream.id}
                    onClick={() => setSelectedStreamId(stream.id)}
                    className={`cursor-pointer rounded-xl border p-3.5 transition-all text-xs ${
                      isSelected
                        ? "border-amber-400 bg-amber-50/80 dark:bg-amber-950/40 shadow-sm ring-1 ring-amber-400/30 text-amber-950 dark:text-amber-100"
                        : "border-slate-200 dark:border-slate-800/80 bg-slate-50/50 dark:bg-slate-950/40 hover:border-amber-300 dark:hover:border-amber-700/60 hover:bg-amber-50/30 dark:hover:bg-amber-950/20"
                    }`}
                  >
                    <div className="flex items-start justify-between gap-2">
                      <div>
                        <div className="flex items-center gap-2">
                          <span className="font-semibold text-slate-900 dark:text-white">{stream.name}</span>
                          <span className="font-mono text-[10px] text-slate-500 dark:text-slate-400">
                            {stream.id}
                          </span>
                        </div>
                        <p className="mt-0.5 text-[11px] text-slate-500 dark:text-slate-400">
                          {stream.sourceZoneName}
                        </p>
                      </div>
                      <Badge
                        variant={stream.status === "ACTIVE" ? "success" : "default"}
                        dot
                        className="text-[10px]"
                      >
                        {stream.status}
                      </Badge>
                    </div>

                    <div className="mt-3 flex items-center justify-between border-t border-slate-200 dark:border-slate-800/60 pt-2 text-[11px] text-slate-500 dark:text-slate-400">
                      <div className="flex items-center gap-1.5">
                        <Zap className="h-3 w-3 text-cyan-600 dark:text-cyan-400" />
                        <span>{stream.meterCount} meters</span>
                      </div>
                      <div className="flex items-center gap-1.5">
                        <span className="rounded bg-slate-100 dark:bg-slate-800 px-1.5 py-0.2 text-[10px] text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-transparent">
                          {activeLayersCount} {isAcademic ? `Decorator${activeLayersCount === 1 ? "" : "s"}` : `Security Layer${activeLayersCount === 1 ? "" : "s"}`}
                        </span>
                      </div>
                    </div>
                  </div>
                );
              })}

              {filteredStreams.length === 0 && (
                <div className="text-center py-8 text-xs text-slate-500 dark:text-slate-400">
                  No data streams match your search.
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Right Column: Pipeline Visualizer & Layer Configurator */}
        <div className="lg:col-span-7 space-y-6">
          {selectedStream ? (
            <>
              {/* Pipeline Interactive Visualizer */}
              <PipelineVisualizer stream={selectedStream} />

              {/* Dynamic Decorator Stack Configurator */}
              <Card className="border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/70 shadow-sm">
                <CardContent className="p-5">
                  <LayerConfigurator
                    layers={selectedStream.pipelineLayers}
                    onChange={handleLayersChange}
                  />
                </CardContent>
              </Card>
            </>
          ) : (
            <Card className="border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/70 p-8 text-center text-xs text-slate-500 dark:text-slate-400">
              Select a data stream from the list to view its pipeline configuration.
            </Card>
          )}
        </div>
      </div>

      {/* Modal: Create Stream */}
      <CreateStreamModal
        isOpen={createModalOpen}
        onClose={() => setCreateModalOpen(false)}
        onCreated={(newStream) => {
          setStreams([newStream, ...streams]);
          setSelectedStreamId(newStream.id);
        }}
      />
    </div>
  );
}

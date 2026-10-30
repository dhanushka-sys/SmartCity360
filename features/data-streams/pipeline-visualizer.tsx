"use client";

import * as React from "react";
import {
  Play,
  ArrowRight,
  ShieldAlert,
  CheckCircle2,
  FileJson,
  Cpu,
  Layers,
  Sparkles,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { DataStream, PipelineExecutionResult } from "@/types/data-stream";
import { StreamsService } from "@/lib/api/streams-service";
import { useAppMode } from "@/components/mode-provider";

interface PipelineVisualizerProps {
  stream: DataStream;
}

export function PipelineVisualizer({ stream }: PipelineVisualizerProps) {
  const { isAcademic } = useAppMode();
  const [loading, setLoading] = React.useState(false);
  const [result, setResult] = React.useState<PipelineExecutionResult | null>(null);
  const [activeTab, setActiveTab] = React.useState<"final" | "steps" | "raw">("final");

  React.useEffect(() => {
    runPipeline();
  }, [stream.id, stream.pipelineLayers]);

  const runPipeline = async () => {
    setLoading(true);
    try {
      const res = await StreamsService.executePipeline(stream.id);
      setResult(res);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const activeLayers = stream.pipelineLayers
    .filter((l) => l.enabled)
    .sort((a, b) => a.order - b.order);

  return (
    <Card className="border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/80 shadow-sm">
      <CardHeader className="flex flex-row items-center justify-between pb-4">
        <div>
          <div className="flex items-center gap-2">
            <CardTitle className="text-sm md:text-base">
              {isAcademic ? "Decorator Pipeline Visualizer" : "Stream Processing Pipeline"}
            </CardTitle>
            <Badge variant="info" className="text-[10px]">
              {isAcademic ? "Pattern Mechanics" : "Security Pipeline"}
            </Badge>
          </div>
          <CardDescription>
            {isAcademic
              ? "Live trace of raw energy meter readings passing through dynamic wrapper chain"
              : "Live trace of raw energy meter readings passing through configured security layers"}
          </CardDescription>
        </div>
        <Button
          size="sm"
          onClick={runPipeline}
          disabled={loading}
          className="gap-1.5 text-xs shadow-cyan-500/20"
        >
          <Play className="h-3.5 w-3.5 fill-current" />
          <span>{loading ? "Processing..." : "Process Test Packet"}</span>
        </Button>
      </CardHeader>

      <CardContent className="space-y-6">
        {/* Layer Execution Chain Flow Diagram */}
        <div className="space-y-2">
          <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400 block">
            {isAcademic ? "Runtime Wrapping Sequence (Innermost → Outermost)" : "Active Pipeline Processing Order"}
          </span>

          <div className="flex flex-wrap items-center gap-2 rounded-xl border border-slate-200 dark:border-slate-800/90 bg-slate-50 dark:bg-slate-950/60 p-4">
            {/* Core reading */}
            <div className="flex items-center gap-2 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 px-3 py-2 text-xs shadow-xs">
              <Cpu className="h-3.5 w-3.5 text-cyan-600 dark:text-cyan-400" />
              <div>
                <p className="font-semibold text-slate-900 dark:text-white">Core Meter Poller</p>
                <p className="text-[10px] text-slate-500 dark:text-slate-400 font-mono">Raw telemetry</p>
              </div>
            </div>

            {activeLayers.map((layer, idx) => (
              <React.Fragment key={layer.type}>
                <ArrowRight className="h-4 w-4 text-slate-400 shrink-0" />
                <div className="flex items-center gap-2 rounded-lg border border-cyan-200 dark:border-cyan-500/30 bg-cyan-50/70 dark:bg-cyan-950/40 px-3 py-2 text-xs shadow-xs">
                  <span className="flex h-4 w-4 items-center justify-center rounded-full bg-cyan-600 text-[10px] font-bold text-white">
                    {idx + 1}
                  </span>
                  <div>
                    <p className="font-semibold text-cyan-900 dark:text-cyan-300">{layer.name}</p>
                    <p className="text-[10px] text-cyan-700 dark:text-cyan-400/80 font-mono">
                      {isAcademic ? `${layer.type}_DECORATOR` : layer.type}
                    </p>
                  </div>
                </div>
              </React.Fragment>
            ))}

            {activeLayers.length === 0 && (
              <div className="text-xs text-amber-700 dark:text-amber-400 italic py-1">
                No active wrappers. Stream transmitting unencrypted raw plaintext.
              </div>
            )}
          </div>
        </div>

        {/* Payload Inspection Tabs */}
        {result && (
          <div className="space-y-3">
            <div className="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-2">
              <div className="flex items-center gap-2">
                <button
                  onClick={() => setActiveTab("final")}
                  className={`text-xs font-semibold px-2.5 py-1 rounded-md transition-colors ${
                    activeTab === "final"
                      ? "bg-slate-100 dark:bg-slate-800 text-cyan-700 dark:text-cyan-300 font-bold"
                      : "text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white"
                  }`}
                >
                  Final Output Envelope
                </button>
                <button
                  onClick={() => setActiveTab("steps")}
                  className={`text-xs font-semibold px-2.5 py-1 rounded-md transition-colors ${
                    activeTab === "steps"
                      ? "bg-slate-100 dark:bg-slate-800 text-cyan-700 dark:text-cyan-300 font-bold"
                      : "text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white"
                  }`}
                >
                  Transformation Steps ({result.steps.length})
                </button>
                <button
                  onClick={() => setActiveTab("raw")}
                  className={`text-xs font-semibold px-2.5 py-1 rounded-md transition-colors ${
                    activeTab === "raw"
                      ? "bg-slate-100 dark:bg-slate-800 text-cyan-700 dark:text-cyan-300 font-bold"
                      : "text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white"
                  }`}
                >
                  Original Raw Payload
                </button>
              </div>

              <div className="flex items-center gap-2 text-[11px] text-slate-500 dark:text-slate-400">
                <span>Compression: {result.overallCompressionRatio}x</span>
                <span>•</span>
                <span className={result.isEncrypted ? "text-cyan-600 dark:text-cyan-400 font-semibold" : "text-slate-400"}>
                  {result.isEncrypted ? "Encrypted" : "Plaintext"}
                </span>
                <span>•</span>
                <span className={result.isAuthenticated ? "text-emerald-600 dark:text-emerald-400 font-semibold" : "text-slate-400"}>
                  {result.isAuthenticated ? "Signed" : "Unsigned"}
                </span>
              </div>
            </div>

            {/* Tab: Final */}
            {activeTab === "final" && (
              <div className="rounded-xl border border-slate-800 bg-slate-950 p-4 font-mono text-xs text-cyan-300 overflow-x-auto max-h-72 shadow-inner">
                <pre>{result.finalPayloadString}</pre>
              </div>
            )}

            {/* Tab: Steps */}
            {activeTab === "steps" && (
              <div className="space-y-3">
                {result.steps.map((st) => (
                  <div
                    key={st.step}
                    className="rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50/70 dark:bg-slate-950/60 p-3 space-y-2"
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <span className="flex h-5 w-5 items-center justify-center rounded bg-slate-200 dark:bg-slate-800 text-[10px] font-bold text-slate-800 dark:text-white">
                          {st.step}
                        </span>
                        <span className="text-xs font-semibold text-slate-900 dark:text-white">{st.layerName}</span>
                        <Badge variant="outline" className="text-[9px]">
                          {st.processingTimeMs} ms
                        </Badge>
                      </div>
                      <span className="text-[11px] text-slate-500 dark:text-slate-400">
                        {st.byteSizeBefore} B → {st.byteSizeAfter} B
                      </span>
                    </div>
                    <p className="text-[11px] text-slate-600 dark:text-slate-300">{st.description}</p>
                    <div className="rounded-lg bg-slate-100 dark:bg-slate-900/90 p-2 font-mono text-[10px] text-slate-600 dark:text-slate-400 truncate max-w-full">
                      {st.outputPayload.slice(0, 180)}...
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* Tab: Raw */}
            {activeTab === "raw" && (
              <div className="rounded-xl border border-slate-800 bg-slate-950 p-4 font-mono text-xs text-slate-200 overflow-x-auto max-h-72 shadow-inner">
                <pre>{result.rawPayloadString}</pre>
              </div>
            )}
          </div>
        )}

        {/* Note / Theory Card */}
        {isAcademic ? (
          <div className="rounded-xl border border-cyan-200 dark:border-cyan-950/50 bg-cyan-50/70 dark:bg-cyan-950/20 p-3.5 text-xs text-cyan-900 dark:text-cyan-300/90 leading-relaxed">
            <p className="font-semibold text-cyan-800 dark:text-cyan-200">Decorator Pattern Justification:</p>
            <p className="mt-1 text-[11px] text-slate-600 dark:text-slate-400">
              By wrapping the <code className="text-cyan-700 dark:text-cyan-300 font-mono font-semibold">StreamProcessor</code> component with interchangeable
              decorator classes, encryption, authentication, and compression capabilities are composed at runtime without
              subclass explosion or modifying the underlying meter polling logic.
            </p>
          </div>
        ) : (
          <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950/50 p-3.5 text-xs text-slate-700 dark:text-slate-300 leading-relaxed">
            <p className="font-semibold text-slate-900 dark:text-white">Security &amp; Bandwidth Optimization:</p>
            <p className="mt-1 text-[11px] text-slate-600 dark:text-slate-400">
              Configured telemetry processors enforce packet encryption (AES-256-GCM), HMAC signature verification, and compression (Snappy) to protect smart grid operational telemetry across municipal transit corridors.
            </p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

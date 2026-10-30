"use client";

import * as React from "react";
import {
  ArrowUp,
  ArrowDown,
  Check,
  Lock,
  ShieldCheck,
  Minimize2,
  Trash2,
  Sliders,
  Layers,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ProcessingLayerConfig } from "@/types/data-stream";

interface LayerConfiguratorProps {
  layers: ProcessingLayerConfig[];
  onChange: (updatedLayers: ProcessingLayerConfig[]) => void;
}

export function LayerConfigurator({ layers, onChange }: LayerConfiguratorProps) {
  const toggleLayer = (id: string) => {
    const updated = layers.map((layer) =>
      layer.id === id ? { ...layer, enabled: !layer.enabled } : layer
    );
    onChange(updated);
  };

  const moveUp = (index: number) => {
    if (index === 0) return;
    const copy = [...layers];
    const temp = copy[index - 1];
    copy[index - 1] = copy[index];
    copy[index] = temp;
    copy.forEach((l, idx) => (l.order = idx + 1));
    onChange(copy);
  };

  const moveDown = (index: number) => {
    if (index === layers.length - 1) return;
    const copy = [...layers];
    const temp = copy[index + 1];
    copy[index + 1] = copy[index];
    copy[index] = temp;
    copy.forEach((l, idx) => (l.order = idx + 1));
    onChange(copy);
  };

  const getLayerIcon = (type: string) => {
    switch (type) {
      case "ENCRYPTION":
        return <Lock className="h-4 w-4 text-cyan-600 dark:text-cyan-400" />;
      case "AUTHENTICATION":
        return <ShieldCheck className="h-4 w-4 text-emerald-600 dark:text-emerald-400" />;
      case "COMPRESSION":
        return <Minimize2 className="h-4 w-4 text-purple-600 dark:text-purple-400" />;
      default:
        return <Layers className="h-4 w-4 text-slate-500 dark:text-slate-400" />;
    }
  };

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between pb-1">
        <div>
          <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-700 dark:text-slate-300">
            Active Processing Pipeline Layers (Decorator Stack)
          </h4>
          <p className="text-[11px] text-slate-500 dark:text-slate-400">
            Outer wrappers wrap inner stream components. Reorder or toggle layers to observe changes.
          </p>
        </div>
        <span className="text-xs font-semibold text-cyan-600 dark:text-cyan-400">
          {layers.filter((l) => l.enabled).length} of {layers.length} Active
        </span>
      </div>

      <div className="space-y-2">
        {layers.map((layer, index) => {
          return (
            <div
              key={layer.id}
              className={`flex items-center justify-between gap-3 rounded-xl border p-3 transition-all ${
                layer.enabled
                  ? "border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900/90 shadow-sm"
                  : "border-slate-100 dark:border-slate-800/60 bg-slate-50/60 dark:bg-slate-950/40 opacity-60"
              }`}
            >
              <div className="flex items-center gap-3">
                <span className="flex h-6 w-6 items-center justify-center rounded-lg bg-slate-100 dark:bg-slate-800 text-[11px] font-bold text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-transparent">
                  {index + 1}
                </span>

                <div className="rounded-lg border border-slate-200 dark:border-slate-700/60 bg-slate-50 dark:bg-slate-800/60 p-2">
                  {getLayerIcon(layer.type)}
                </div>

                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-semibold text-slate-900 dark:text-white">{layer.name}</span>
                    <Badge
                      variant={
                        layer.type === "ENCRYPTION"
                          ? "info"
                          : layer.type === "AUTHENTICATION"
                          ? "success"
                          : "purple"
                      }
                      className="text-[10px] py-0"
                    >
                      {layer.type}
                    </Badge>
                  </div>
                  <p className="text-[11px] text-slate-500 dark:text-slate-400">
                    {layer.type === "ENCRYPTION" &&
                      `Cipher: ${layer.params.algorithm} • Key: ${layer.params.keyId}`}
                    {layer.type === "AUTHENTICATION" &&
                      `Signature Scheme: ${layer.params.signatureScheme}`}
                    {layer.type === "COMPRESSION" &&
                      `Compression Level: ${layer.params.compressionLevel}`}
                  </p>
                </div>
              </div>

              {/* Controls */}
              <div className="flex items-center gap-1.5">
                <button
                  onClick={() => moveUp(index)}
                  disabled={index === 0}
                  className="rounded-lg p-1.5 text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 hover:text-slate-700 dark:hover:text-white disabled:opacity-30 disabled:hover:bg-transparent"
                  title="Move layer outward"
                >
                  <ArrowUp className="h-3.5 w-3.5" />
                </button>
                <button
                  onClick={() => moveDown(index)}
                  disabled={index === layers.length - 1}
                  className="rounded-lg p-1.5 text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 hover:text-slate-700 dark:hover:text-white disabled:opacity-30 disabled:hover:bg-transparent"
                  title="Move layer inward"
                >
                  <ArrowDown className="h-3.5 w-3.5" />
                </button>
                <Button
                  variant={layer.enabled ? "default" : "secondary"}
                  size="sm"
                  onClick={() => toggleLayer(layer.id)}
                  className="text-xs h-7 px-3"
                >
                  {layer.enabled ? "Enabled" : "Disabled"}
                </Button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

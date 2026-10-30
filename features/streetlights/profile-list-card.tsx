"use client";

import * as React from "react";
import { Lightbulb, Zap, Clock, ShieldCheck, Thermometer } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { StreetlightProfile } from "@/types/streetlight";

interface ProfileListCardProps {
  profiles: StreetlightProfile[];
}

export function ProfileListCard({ profiles }: ProfileListCardProps) {
  return (
    <Card className="border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/70 shadow-sm">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="text-sm md:text-base">Flyweight Profile Pool (Intrinsic State)</CardTitle>
          <Badge variant="success" className="text-[10px]">
            {profiles.length} Flyweights Cached
          </Badge>
        </div>
        <CardDescription>
          Immutable hardware definitions shared across all light pole instances
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
          {profiles.map((p) => (
            <div
              key={p.id}
              className="rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50/70 dark:bg-slate-950/50 p-3.5 text-xs space-y-2 hover:border-slate-300 dark:hover:border-slate-700 transition-colors shadow-xs"
            >
              <div className="flex items-start justify-between">
                <span className="font-mono text-[10px] text-cyan-700 dark:text-cyan-400 font-semibold">{p.id}</span>
                <Badge variant="outline" className="text-[9px]">
                  {p.lampType.replace("_", " ")}
                </Badge>
              </div>

              <div>
                <h4 className="font-semibold text-slate-900 dark:text-white truncate">{p.modelName}</h4>
                <p className="text-[11px] text-slate-500 dark:text-slate-400">{p.manufacturer}</p>
              </div>

              <div className="space-y-1 pt-1 border-t border-slate-200 dark:border-slate-800/80 text-[11px] text-slate-600 dark:text-slate-300">
                <div className="flex justify-between">
                  <span className="text-slate-500 dark:text-slate-400">Rating:</span>
                  <span className="font-mono text-cyan-700 dark:text-cyan-300 font-semibold">{p.wattageRatingWatts}W</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500 dark:text-slate-400">Default Brightness:</span>
                  <span>{p.defaultBrightnessPercent}%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500 dark:text-slate-400">Schedule:</span>
                  <span className="truncate max-w-[110px]">{p.operatingSchedule}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500 dark:text-slate-400">Color Temp:</span>
                  <span>{p.colorTemperatureKelvin}K</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

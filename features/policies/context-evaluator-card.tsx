"use client";

import * as React from "react";
import { Play, CheckCircle2, AlertTriangle, Sliders, Terminal, Sparkles } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { PolicyEvaluationContext, PolicyEvaluationResult, PolicyRule } from "@/types/policy";
import { PoliciesService } from "@/lib/api/policies-service";
import { useAppMode } from "@/components/mode-provider";

interface ContextEvaluatorCardProps {
  selectedPolicy?: PolicyRule;
}

export function ContextEvaluatorCard({ selectedPolicy }: ContextEvaluatorCardProps) {
  const { isAcademic } = useAppMode();
  const [expression, setExpression] = React.useState(
    selectedPolicy ? selectedPolicy.expression : "NOISE_LEVEL <= 60"
  );
  const [noiseLevel, setNoiseLevel] = React.useState<number>(68.4);
  const [vehicleSpeed, setVehicleSpeed] = React.useState<number>(34.0);
  const [airQuality, setAirQuality] = React.useState<number>(45);
  const [energyKw, setEnergyKw] = React.useState<number>(4200);
  const [parkingHour, setParkingHour] = React.useState<number>(14);
  const [loading, setLoading] = React.useState(false);
  const [result, setResult] = React.useState<PolicyEvaluationResult | null>(null);

  React.useEffect(() => {
    if (selectedPolicy) {
      setExpression(selectedPolicy.expression);
      setResult(null);
    }
  }, [selectedPolicy]);

  const handleEvaluate = async () => {
    setLoading(true);
    try {
      const context: PolicyEvaluationContext = {
        noiseLevelDb: Number(noiseLevel),
        vehicleSpeedKmh: Number(vehicleSpeed),
        airQualityAqi: Number(airQuality),
        energyConsumptionKw: Number(energyKw),
        currentHour: Number(parkingHour),
      };

      const res = await PoliciesService.evaluatePolicy(
        expression,
        context,
        selectedPolicy ? { id: selectedPolicy.id, name: selectedPolicy.name } : undefined
      );
      setResult(res);
    } catch (err: any) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/80 shadow-sm">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <CardTitle className="text-sm md:text-base">
              {isAcademic ? "Interpreter Evaluation Sandbox" : "Policy Rule Compliance Sandbox"}
            </CardTitle>
            <Badge variant="purple" className="text-[10px]">
              {isAcademic ? "Interpreter Pattern" : "Compliance Engine"}
            </Badge>
          </div>
          <span className="text-xs text-slate-500 dark:text-slate-400 font-mono">
            {isAcademic ? "AST Tree Walk" : "Live Telemetry"}
          </span>
        </div>
        <CardDescription>
          Adjust simulated sensor context and evaluate rule expressions dynamically
        </CardDescription>
      </CardHeader>

      <CardContent className="space-y-4">
        {/* Expression Input */}
        <div className="space-y-1.5">
          <label className="text-xs font-semibold text-slate-700 dark:text-slate-300">Target Policy Expression:</label>
          <div className="flex items-center gap-2">
            <input
              type="text"
              value={expression}
              onChange={(e) => setExpression(e.target.value)}
              className="flex-1 rounded-lg border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-950/80 px-3 py-2 font-mono text-xs text-cyan-800 dark:text-cyan-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-cyan-500 shadow-xs"
            />
            <Button
              size="sm"
              onClick={handleEvaluate}
              disabled={loading || !expression.trim()}
              className="gap-1 text-xs shrink-0"
            >
              <Play className="h-3.5 w-3.5 fill-current" />
              <span>{isAcademic ? "Evaluate AST" : "Evaluate Rule"}</span>
            </Button>
          </div>
        </div>

        {/* Sensor Context Sliders */}
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950/60 p-3.5 space-y-3">
          <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400 block">
            Simulated Runtime Sensor Context
          </span>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            {/* Noise */}
            <div className="space-y-1 rounded-lg border border-slate-200 dark:border-slate-800/80 bg-white dark:bg-slate-900/50 p-2.5 shadow-xs">
              <div className="flex justify-between text-xs">
                <span className="text-slate-500 dark:text-slate-400">NOISE_LEVEL (dB):</span>
                <span className="font-mono text-cyan-700 dark:text-cyan-400 font-bold">{noiseLevel}</span>
              </div>
              <input
                type="range"
                min="30"
                max="110"
                step="0.5"
                value={noiseLevel}
                onChange={(e) => setNoiseLevel(Number(e.target.value))}
                className="w-full accent-cyan-500"
              />
            </div>

            {/* Vehicle Speed */}
            <div className="space-y-1 rounded-lg border border-slate-200 dark:border-slate-800/80 bg-white dark:bg-slate-900/50 p-2.5 shadow-xs">
              <div className="flex justify-between text-xs">
                <span className="text-slate-500 dark:text-slate-400">VEHICLE_SPEED (km/h):</span>
                <span className="font-mono text-cyan-700 dark:text-cyan-400 font-bold">{vehicleSpeed}</span>
              </div>
              <input
                type="range"
                min="0"
                max="120"
                step="1"
                value={vehicleSpeed}
                onChange={(e) => setVehicleSpeed(Number(e.target.value))}
                className="w-full accent-cyan-500"
              />
            </div>

            {/* Air Quality */}
            <div className="space-y-1 rounded-lg border border-slate-200 dark:border-slate-800/80 bg-white dark:bg-slate-900/50 p-2.5 shadow-xs">
              <div className="flex justify-between text-xs">
                <span className="text-slate-500 dark:text-slate-400">AIR_QUALITY_AQI:</span>
                <span className="font-mono text-cyan-700 dark:text-cyan-400 font-bold">{airQuality}</span>
              </div>
              <input
                type="range"
                min="10"
                max="300"
                step="1"
                value={airQuality}
                onChange={(e) => setAirQuality(Number(e.target.value))}
                className="w-full accent-cyan-500"
              />
            </div>

            {/* Energy */}
            <div className="space-y-1 rounded-lg border border-slate-200 dark:border-slate-800/80 bg-white dark:bg-slate-900/50 p-2.5 shadow-xs">
              <div className="flex justify-between text-xs">
                <span className="text-slate-500 dark:text-slate-400">ENERGY_KW:</span>
                <span className="font-mono text-cyan-700 dark:text-cyan-400 font-bold">{energyKw}</span>
              </div>
              <input
                type="range"
                min="1000"
                max="10000"
                step="50"
                value={energyKw}
                onChange={(e) => setEnergyKw(Number(e.target.value))}
                className="w-full accent-cyan-500"
              />
            </div>

            {/* Parking Hour */}
            <div className="space-y-1 rounded-lg border border-slate-200 dark:border-slate-800/80 bg-white dark:bg-slate-900/50 p-2.5 shadow-xs">
              <div className="flex justify-between text-xs">
                <span className="text-slate-500 dark:text-slate-400">PARKING_HOUR (24h):</span>
                <span className="font-mono text-cyan-700 dark:text-cyan-400 font-bold">
                  {parkingHour}:00
                </span>
              </div>
              <input
                type="range"
                min="0"
                max="23"
                step="1"
                value={parkingHour}
                onChange={(e) => setParkingHour(Number(e.target.value))}
                className="w-full accent-purple-500"
              />
            </div>
          </div>
        </div>

        {/* Evaluation Output Result */}
        {result && (
          <div
            className={`rounded-xl border p-4 text-xs space-y-2 transition-all ${
              result.passed
                ? "border-emerald-300 dark:border-emerald-500/40 bg-emerald-50 dark:bg-emerald-950/20 text-emerald-800 dark:text-emerald-300"
                : "border-rose-300 dark:border-rose-500/40 bg-rose-50 dark:bg-rose-950/20 text-rose-800 dark:text-rose-300"
            }`}
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                {result.passed ? (
                  <CheckCircle2 className="h-5 w-5 text-emerald-600 dark:text-emerald-400" />
                ) : (
                  <AlertTriangle className="h-5 w-5 text-rose-600 dark:text-rose-400" />
                )}
                <span className="font-bold text-sm">
                  {result.passed ? "RULE VERIFIED: COMPLIANT" : "RULE TRIGGERED: VIOLATION DETECTED"}
                </span>
              </div>
              <Badge variant={result.passed ? "success" : "danger"} className="text-[10px]">
                {result.passed ? "Passed" : "Action Needed"}
              </Badge>
            </div>

            <p className="text-slate-800 dark:text-slate-200 leading-relaxed font-mono">{result.evaluatedConditionExplanation}</p>

            <div className="flex items-center justify-between pt-2 border-t border-slate-200 dark:border-slate-800/60 text-[11px] text-slate-500 dark:text-slate-400">
              <span>Automated Action: {result.actionRecommended}</span>
              <span className="font-mono">{new Date(result.timestamp).toLocaleTimeString()}</span>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

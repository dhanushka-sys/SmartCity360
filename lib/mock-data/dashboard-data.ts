import { ActivityLogItem, ComplaintTrendPoint, EnergyConsumptionPoint } from "@/types/test-case";

export const initialEnergyTrends: EnergyConsumptionPoint[] = [
  { time: "00:00", actualKwh: 2420, projectedKwh: 2600, peakKwh: 5000 },
  { time: "03:00", actualKwh: 1980, projectedKwh: 2100, peakKwh: 5000 },
  { time: "06:00", actualKwh: 3100, projectedKwh: 2950, peakKwh: 5000 },
  { time: "09:00", actualKwh: 4890, projectedKwh: 4600, peakKwh: 5000 },
  { time: "12:00", actualKwh: 4950, projectedKwh: 4800, peakKwh: 5000 },
  { time: "15:00", actualKwh: 4720, projectedKwh: 4650, peakKwh: 5000 },
  { time: "18:00", actualKwh: 4850, projectedKwh: 4700, peakKwh: 5000 },
  { time: "21:00", actualKwh: 3980, projectedKwh: 4100, peakKwh: 5000 },
];

export const initialComplaintTrends: ComplaintTrendPoint[] = [
  { day: "Mon", submitted: 24, resolved: 21, escalated: 4 },
  { day: "Tue", submitted: 31, resolved: 28, escalated: 6 },
  { day: "Wed", submitted: 19, resolved: 22, escalated: 2 },
  { day: "Thu", submitted: 27, resolved: 25, escalated: 5 },
  { day: "Fri", submitted: 35, resolved: 30, escalated: 8 },
  { day: "Sat", submitted: 18, resolved: 17, escalated: 3 },
  { day: "Sun", submitted: 15, resolved: 14, escalated: 2 },
];

export const initialActivityLogs: ActivityLogItem[] = [
  {
    id: "ACT-01",
    timestamp: "2026-10-30T04:55:00.000Z",
    module: "Citizen Complaints",
    title: "Complaint Escalate to City Manager",
    description: "Hazardous runoff ticket CMP-7701 auto-promoted through Chain of Responsibility.",
    severity: "CRITICAL",
    patternRelated: "CHAIN_OF_RESPONSIBILITY",
  },
  {
    id: "ACT-02",
    timestamp: "2026-10-30T04:42:00.000Z",
    module: "City Policies",
    title: "DSL Policy Evaluator Flagged Decibel Violation",
    description: "Evaluator evaluated 'NOISE_LEVEL <= 60' with 68.4 dB at Silicon Promenade.",
    severity: "WARNING",
    patternRelated: "INTERPRETER",
  },
  {
    id: "ACT-03",
    timestamp: "2026-10-30T04:28:00.000Z",
    module: "Data Streams",
    title: "Decorator Security Wrapper Applied",
    description: "HMAC Auth + AES-GCM-256 + Snappy pipeline processed 1,420 meter packets.",
    severity: "SUCCESS",
    patternRelated: "DECORATOR",
  },
  {
    id: "ACT-04",
    timestamp: "2026-10-30T04:15:00.000Z",
    module: "Zone Management",
    title: "Composite Hierarchical Telemetry Sweep",
    description: "Aggregated usage command cascaded down Grand Horizon Avenue to 2 building leaf nodes.",
    severity: "INFO",
    patternRelated: "COMPOSITE",
  },
  {
    id: "ACT-05",
    timestamp: "2026-10-30T03:50:00.000Z",
    module: "Streetlights",
    title: "Flyweight Profile Reused Across 8,200 Poles",
    description: "LumenPulse Apex 150W profile assigned, saving an estimated 88.8% in object memory overhead.",
    severity: "SUCCESS",
    patternRelated: "FLYWEIGHT",
  },
];

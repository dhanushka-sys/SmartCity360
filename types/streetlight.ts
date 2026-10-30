// Flyweight Intrinsic State (Shared across thousands of lights)
export interface StreetlightProfile {
  id: string;
  modelName: string;
  manufacturer: string;
  wattageRatingWatts: number;
  lampType: "LED_SMART" | "SOLAR_HYBRID" | "HIGH_EFFICIENCY_SODIUM" | "RGB_FIBER_LED";
  defaultBrightnessPercent: number;
  operatingSchedule: "DUSK_TO_DAWN" | "ADAPTIVE_TRAFFIC" | "NIGHT_DIM_50" | "ALWAYS_ON";
  maintenanceIntervalMonths: number;
  colorTemperatureKelvin: number;
  estimatedPayloadByteSize: number; // e.g. 1024 bytes per profile definition
}

export type StreetlightStatus = "ONLINE" | "OFFLINE" | "MAINTENANCE";

// Flyweight Extrinsic State (Unique to each individual light instance)
export interface Streetlight {
  id: string;
  serialNumber: string;
  profileId: string; // Reference to shared intrinsic profile
  zoneId: string;
  zoneName: string;
  streetName: string;
  latitude: number;
  longitude: number;
  status: StreetlightStatus;
  currentBrightnessPercent: number;
  powerUsageKw: number;
  lastPingAt: string;
  poleHeightMeters: number;
}

export interface FlyweightMemoryAnalysis {
  totalLightCount: number;
  uniqueProfilesCount: number;
  estimatedMemoryWithoutFlyweightKb: number;
  estimatedMemoryWithFlyweightKb: number;
  memorySavedKb: number;
  savingsPercentage: number;
  profileUsageBreakdown: {
    profileId: string;
    profileName: string;
    model: string;
    assignedLightCount: number;
  }[];
}


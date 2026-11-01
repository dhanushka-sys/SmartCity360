import { fetchFromBackend } from "./backend-client";
import {
  initialStreetlightProfiles,
  initialStreetlights,
} from "@/lib/mock-data/streetlights-data";
import {
  FlyweightMemoryAnalysis,
  Streetlight,
  StreetlightProfile,
  StreetlightStatus,
} from "@/types/streetlight";

let profilesState: StreetlightProfile[] = [...initialStreetlightProfiles];
let streetlightsState: Streetlight[] = [...initialStreetlights];

const delay = (ms = 180) => new Promise((resolve) => setTimeout(resolve, ms));

export const StreetlightsService = {
  async getStreetlights(): Promise<Streetlight[]> {
    const data = await fetchFromBackend<Streetlight[]>("/streetlights");
    if (data && Array.isArray(data)) {
      streetlightsState = data;
      return data;
    }
    throw new Error("Unable to load streetlights from MySQL database.");
  },

  async getProfiles(): Promise<StreetlightProfile[]> {
    const data = await fetchFromBackend<StreetlightProfile[]>("/streetlights/profiles");
    if (data && Array.isArray(data)) {
      profilesState = data;
      return data;
    }
    throw new Error("Unable to load streetlight profiles from MySQL database.");
  },

  /**
   * Flyweight Pattern Memory Analysis.
   * Compares memory consumption if every streetlight held its own copy of the profile (without Flyweight)
   * vs. referencing shared Flyweight profile objects (with Flyweight).
   */
  async getMemoryAnalysis(): Promise<FlyweightMemoryAnalysis> {
    await delay(120);
    // City-wide scale simulation: 24,500 physical light poles in Metropolis Neo-Prime
    const simulatedTotalLights = 24500;
    const profileCount = profilesState.length;

    // Estimated memory sizes in bytes
    const INTRINSIC_PROFILE_BYTES = 1024; // Wattage, optic curve, schedule, model name, warranty metadata
    const EXTRINSIC_INSTANCE_BYTES = 128; // Coordinates, ID, status enum, dynamic brightness, pointer

    // Without Flyweight: Each of the 24,500 lights holds full duplicate profile state
    const memoryWithoutFlyweightBytes = simulatedTotalLights * (INTRINSIC_PROFILE_BYTES + EXTRINSIC_INSTANCE_BYTES);

    // With Flyweight: Only 4 profiles allocated in Flyweight Factory pool + 24,500 light pointers
    const memoryWithFlyweightBytes =
      profileCount * INTRINSIC_PROFILE_BYTES + simulatedTotalLights * EXTRINSIC_INSTANCE_BYTES;

    const withoutKb = Math.round(memoryWithoutFlyweightBytes / 1024);
    const withKb = Math.round(memoryWithFlyweightBytes / 1024);
    const savedKb = withoutKb - withKb;
    const savingsPercent = Number(((savedKb / withoutKb) * 100).toFixed(1));

    // Calculate usage breakdown across the initial sample + scale
    const sampleTotal = streetlightsState.length;
    const profileUsage = profilesState.map((profile) => {
      const sampleAssigned = streetlightsState.filter((s) => s.profileId === profile.id).length;
      const proportion = sampleTotal > 0 ? sampleAssigned / sampleTotal : 1 / profileCount;
      const simulatedCount = Math.round(simulatedTotalLights * proportion);

      return {
        profileId: profile.id,
        profileName: profile.modelName,
        model: profile.modelName.split(" ")[0],
        assignedLightCount: simulatedCount,
      };
    });

    return {
      totalLightCount: simulatedTotalLights,
      uniqueProfilesCount: profileCount,
      estimatedMemoryWithoutFlyweightKb: withoutKb,
      estimatedMemoryWithFlyweightKb: withKb,
      memorySavedKb: savedKb,
      savingsPercentage: savingsPercent,
      profileUsageBreakdown: profileUsage,
    };
  },

  async createStreetlight(data: {
    profileId: string;
    zoneId: string;
    zoneName: string;
    streetName: string;
    latitude: number;
    longitude: number;
    poleHeightMeters: number;
  }): Promise<Streetlight> {
    try {
      const backendLight = await fetchFromBackend<Streetlight>("/streetlights", {
        method: "POST",
        body: JSON.stringify(data),
      });
      if (backendLight) {
        streetlightsState = [backendLight, ...streetlightsState];
        return backendLight;
      }
    } catch {
      // Fallback
    }

    await delay(220);
    const profile = profilesState.find((p) => p.id === data.profileId);
    if (!profile) throw new Error("Referenced Flyweight Profile not found in Factory pool.");

    const newLight: Streetlight = {
      ...data,
      id: `STL-${Math.floor(1000 + Math.random() * 9000)}`,
      serialNumber: `SN-GEN-${Math.floor(10000 + Math.random() * 90000)}`,
      status: "ONLINE",
      currentBrightnessPercent: profile.defaultBrightnessPercent,
      powerUsageKw: Number(((profile.wattageRatingWatts * (profile.defaultBrightnessPercent / 100)) / 1000).toFixed(3)),
      lastPingAt: new Date().toISOString(),
    };

    streetlightsState = [newLight, ...streetlightsState];
    return newLight;
  },

  async updateStatus(lightId: string, status: StreetlightStatus): Promise<Streetlight> {
    try {
      const backendLight = await fetchFromBackend<Streetlight>(`/streetlights/${lightId}/status`, {
        method: "PUT",
        body: JSON.stringify({ status }),
      });
      if (backendLight) {
        const idx = streetlightsState.findIndex((s) => s.id === lightId);
        if (idx !== -1) streetlightsState[idx] = backendLight;
        return backendLight;
      }
    } catch {
      // Fallback
    }

    await delay(180);
    const light = streetlightsState.find((s) => s.id === lightId);
    if (!light) throw new Error("Streetlight not found");

    light.status = status;
    if (status === "OFFLINE") {
      light.currentBrightnessPercent = 0;
      light.powerUsageKw = 0;
    } else if (status === "MAINTENANCE") {
      light.currentBrightnessPercent = 30;
    } else {
      const profile = profilesState.find((p) => p.id === light.profileId);
      light.currentBrightnessPercent = profile ? profile.defaultBrightnessPercent : 80;
    }
    light.lastPingAt = new Date().toISOString();
    return { ...light };
  },

  async bulkAssignProfile(lightIds: string[], newProfileId: string): Promise<number> {
    await delay(250);
    const profile = profilesState.find((p) => p.id === newProfileId);
    if (!profile) throw new Error("Profile not found in Flyweight pool");

    let updatedCount = 0;
    streetlightsState = streetlightsState.map((light) => {
      if (lightIds.includes(light.id)) {
        updatedCount++;
        return {
          ...light,
          profileId: newProfileId,
          currentBrightnessPercent: profile.defaultBrightnessPercent,
          powerUsageKw: Number(
            ((profile.wattageRatingWatts * (profile.defaultBrightnessPercent / 100)) / 1000).toFixed(3)
          ),
          lastPingAt: new Date().toISOString(),
        };
      }
      return light;
    });

    return updatedCount;
  },

  async bulkUpdateStatus(lightIds: string[], status: StreetlightStatus): Promise<number> {
    try {
      await fetchFromBackend("/streetlights/bulk", {
        method: "PUT",
        body: JSON.stringify({ ids: lightIds, status }),
      });
    } catch {
      // Fallback
    }

    await delay(250);
    let updatedCount = 0;
    streetlightsState = streetlightsState.map((light) => {
      if (lightIds.includes(light.id)) {
        updatedCount++;
        return {
          ...light,
          status,
          currentBrightnessPercent: status === "OFFLINE" ? 0 : light.currentBrightnessPercent,
          powerUsageKw: status === "OFFLINE" ? 0 : light.powerUsageKw,
          lastPingAt: new Date().toISOString(),
        };
      }
      return light;
    });

    return updatedCount;
  },
};


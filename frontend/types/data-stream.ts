export type LayerType = "ENCRYPTION" | "AUTHENTICATION" | "COMPRESSION";

export interface ProcessingLayerConfig {
  id: string;
  type: LayerType;
  name: string;
  enabled: boolean;
  order: number;
  params: {
    algorithm?: string;
    keyId?: string;
    signatureScheme?: string;
    compressionLevel?: string;
  };
}

export interface EnergyReading {
  meterId: string;
  timestamp: string;
  voltage: number;
  currentAmps: number;
  powerKw: number;
  frequencyHz: number;
  powerFactor: number;
  totalKwh: number;
}

export type StreamStatus = "ACTIVE" | "IDLE" | "ERROR" | "PAUSED";

export interface DataStream {
  id: string;
  name: string;
  sourceZoneId: string;
  sourceZoneName: string;
  meterCount: number;
  status: StreamStatus;
  lastProcessedAt: string;
  samplePayload: EnergyReading;
  pipelineLayers: ProcessingLayerConfig[];
  stats: {
    totalPacketsProcessed: number;
    avgLatencyMs: number;
    errorRatePercent: number;
  };
}

export interface TransformationStepResult {
  step: number;
  layerType: LayerType;
  layerName: string;
  inputPayload: string;
  outputPayload: string;
  byteSizeBefore: number;
  byteSizeAfter: number;
  processingTimeMs: number;
  description: string;
  metadata: Record<string, string>;
}

export interface PipelineExecutionResult {
  streamId: string;
  rawPayload: EnergyReading;
  rawPayloadString: string;
  steps: TransformationStepResult[];
  finalPayloadString: string;
  overallCompressionRatio: number;
  isEncrypted: boolean;
  isAuthenticated: boolean;
  isCompressed: boolean;
  executedAt: string;
}


import { initialEnergyStreams } from "@/lib/mock-data/streams-data";
import {
  DataStream,
  EnergyReading,
  PipelineExecutionResult,
  ProcessingLayerConfig,
  TransformationStepResult,
} from "@/types/data-stream";

let streamsState: DataStream[] = [...initialEnergyStreams];

const delay = (ms = 180) => new Promise((resolve) => setTimeout(resolve, ms));

export const StreamsService = {
  async getStreams(): Promise<DataStream[]> {
    await delay();
    return [...streamsState];
  },

  async getStreamById(id: string): Promise<DataStream | undefined> {
    await delay();
    return streamsState.find((s) => s.id === id);
  },

  async createStream(newStream: Omit<DataStream, "id" | "lastProcessedAt" | "stats">): Promise<DataStream> {
    await delay(250);
    const created: DataStream = {
      ...newStream,
      id: `STR-${Math.floor(1000 + Math.random() * 9000)}`,
      lastProcessedAt: new Date().toISOString(),
      stats: {
        totalPacketsProcessed: 0,
        avgLatencyMs: 2.5,
        errorRatePercent: 0,
      },
    };
    streamsState = [created, ...streamsState];
    return created;
  },

  async updateLayers(streamId: string, layers: ProcessingLayerConfig[]): Promise<DataStream> {
    await delay(200);
    const index = streamsState.findIndex((s) => s.id === streamId);
    if (index === -1) throw new Error("Stream not found");

    const updated = {
      ...streamsState[index],
      pipelineLayers: layers,
      lastProcessedAt: new Date().toISOString(),
    };
    streamsState[index] = updated;
    return updated;
  },

  /**
   * Simulates the Decorator Pattern execution.
   * Decorates the raw reading with active layers in order.
   */
  async executePipeline(
    streamId: string,
    customReading?: Partial<EnergyReading>
  ): Promise<PipelineExecutionResult> {
    await delay(220);
    const stream = streamsState.find((s) => s.id === streamId);
    if (!stream) throw new Error("Stream not found");

    const basePayload: EnergyReading = {
      ...stream.samplePayload,
      ...(customReading || {}),
      timestamp: new Date().toISOString(),
    };

    const rawPayloadString = JSON.stringify(basePayload, null, 2);
    let currentPayloadString = rawPayloadString;
    const steps: TransformationStepResult[] = [];

    // Filter enabled layers and sort by order
    const activeLayers = stream.pipelineLayers
      .filter((l) => l.enabled)
      .sort((a, b) => a.order - b.order);

    let isEncrypted = false;
    let isAuthenticated = false;
    let isCompressed = false;

    activeLayers.forEach((layer, index) => {
      const beforeSize = new Blob([currentPayloadString]).size;
      let outputPayload = "";
      let description = "";
      const metadata: Record<string, string> = {};

      if (layer.type === "AUTHENTICATION") {
        isAuthenticated = true;
        const scheme = layer.params.signatureScheme || "HMAC-SHA256";
        const keyId = layer.params.keyId || "KEY-DEFAULT";
        // Simulated HMAC digest
        const hash = Array.from({ length: 64 }, () =>
          Math.floor(Math.random() * 16).toString(16)
        ).join("");

        const envelope = {
          header: {
            authScheme: scheme,
            keyId: keyId,
            timestamp: new Date().toISOString(),
            signatureDigest: `0x${hash}`,
          },
          body: JSON.parse(currentPayloadString.startsWith("{") ? currentPayloadString : '{"data":"wrapped"}'),
        };
        outputPayload = JSON.stringify(envelope, null, 2);
        description = `Authentication Decorator attached cryptographic header (${scheme}) verifying packet integrity.`;
        metadata["Signature"] = `${scheme}: 0x${hash.slice(0, 12)}...`;
      } else if (layer.type === "ENCRYPTION") {
        isEncrypted = true;
        const algo = layer.params.algorithm || "AES-GCM-256";
        const keyId = layer.params.keyId || "VAULT-KEY";
        const iv = Array.from({ length: 24 }, () =>
          Math.floor(Math.random() * 16).toString(16)
        ).join("");
        const cipherHex = btoa(currentPayloadString)
          .split("")
          .reverse()
          .join("")
          .slice(0, 72) + "==[CIPHERTEXT_SIMULATED]==";

        const encryptedEnvelope = {
          cipherMode: algo,
          keyVaultId: keyId,
          initializationVector: `0x${iv}`,
          payloadPayloadCiphertext: cipherHex,
        };
        outputPayload = JSON.stringify(encryptedEnvelope, null, 2);
        description = `Encryption Decorator encapsulated message in ${algo} cryptographic envelope.`;
        metadata["Cipher"] = `${algo} (IV: 0x${iv.slice(0, 8)}...)`;
      } else if (layer.type === "COMPRESSION") {
        isCompressed = true;
        const level = layer.params.compressionLevel || "Standard";
        // Simulated compression
        const rawLength = currentPayloadString.length;
        const compressedBase64 = btoa(currentPayloadString).slice(0, Math.floor(rawLength * 0.42));
        const compressedEnvelope = {
          compressionFormat: "ZSTD_SIMULATED",
          compressionLevel: level,
          uncompressedBytes: beforeSize,
          compressedBytes: Math.floor(beforeSize * 0.42),
          dataBlock: `${compressedBase64}...[STREAM_COMPRESSED]`,
        };
        outputPayload = JSON.stringify(compressedEnvelope, null, 2);
        description = `Compression Decorator reduced payload volume by ~58% via streaming dictionary.`;
        metadata["Ratio"] = `${Math.round((1 - 0.42) * 100)}% reduction`;
      }

      const afterSize = new Blob([outputPayload]).size;

      steps.push({
        step: index + 1,
        layerType: layer.type,
        layerName: layer.name,
        inputPayload: currentPayloadString,
        outputPayload: outputPayload,
        byteSizeBefore: beforeSize,
        byteSizeAfter: afterSize,
        processingTimeMs: Number((Math.random() * 1.5 + 0.8).toFixed(2)),
        description,
        metadata,
      });

      currentPayloadString = outputPayload;
    });

    const initialSize = new Blob([rawPayloadString]).size;
    const finalSize = new Blob([currentPayloadString]).size;
    const ratio = initialSize > 0 ? (finalSize / initialSize) : 1;

    return {
      streamId,
      rawPayload: basePayload,
      rawPayloadString,
      steps,
      finalPayloadString: currentPayloadString,
      overallCompressionRatio: Number(ratio.toFixed(2)),
      isEncrypted,
      isAuthenticated,
      isCompressed,
      executedAt: new Date().toISOString(),
    };
  },
};


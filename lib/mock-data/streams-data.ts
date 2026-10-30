import { DataStream, EnergyReading } from "@/types/data-stream";

const BASE_TIME = 1730260000000;

export const initialEnergyStreams: DataStream[] = [
  {
    id: "STR-4091",
    name: "North Metro Grid Primary Feed",
    sourceZoneId: "ZN-DIST-01",
    sourceZoneName: "Downtown Financial Core",
    meterCount: 1420,
    status: "ACTIVE",
    lastProcessedAt: new Date(BASE_TIME - 1000 * 45).toISOString(),
    samplePayload: {
      meterId: "EM-GRID-0941A",
      timestamp: new Date(BASE_TIME).toISOString(),
      voltage: 230.4,
      currentAmps: 18.2,
      powerKw: 4.19,
      frequencyHz: 50.02,
      powerFactor: 0.98,
      totalKwh: 12480.65,
    },
    pipelineLayers: [
      {
        id: "layer-auth-1",
        type: "AUTHENTICATION",
        name: "HMAC-SHA256 Message Auth Wrapper",
        enabled: true,
        order: 1,
        params: {
          signatureScheme: "HMAC-SHA256",
          keyId: "KEY-SEC-GRID-99",
        },
      },
      {
        id: "layer-enc-1",
        type: "ENCRYPTION",
        name: "AES-256-GCM Payload Cipher Wrapper",
        enabled: true,
        order: 2,
        params: {
          algorithm: "AES-GCM-256",
          keyId: "VAULT-MASTER-01",
        },
      },
      {
        id: "layer-comp-1",
        type: "COMPRESSION",
        name: "Zstandard / Snappy Stream Compressor",
        enabled: true,
        order: 3,
        params: {
          compressionLevel: "Standard (Level 3)",
        },
      },
    ],
    stats: {
      totalPacketsProcessed: 894210,
      avgLatencyMs: 3.2,
      errorRatePercent: 0.01,
    },
  },
  {
    id: "STR-8820",
    name: "Tech District Solar Microgrid Feed",
    sourceZoneId: "ZN-DIST-02",
    sourceZoneName: "Cyber Park Innovation Hub",
    meterCount: 680,
    status: "ACTIVE",
    lastProcessedAt: new Date(BASE_TIME - 1000 * 120).toISOString(),
    samplePayload: {
      meterId: "EM-SOLAR-002",
      timestamp: new Date(BASE_TIME).toISOString(),
      voltage: 231.1,
      currentAmps: 34.5,
      powerKw: 7.97,
      frequencyHz: 49.98,
      powerFactor: 0.99,
      totalKwh: 8420.12,
    },
    pipelineLayers: [
      {
        id: "layer-enc-2",
        type: "ENCRYPTION",
        name: "ChaCha20-Poly1305 Security Wrapper",
        enabled: true,
        order: 1,
        params: {
          algorithm: "ChaCha20-Poly1305",
          keyId: "VAULT-SOLAR-KEY",
        },
      },
      {
        id: "layer-comp-2",
        type: "COMPRESSION",
        name: "Gzip Block Compressor",
        enabled: true,
        order: 2,
        params: {
          compressionLevel: "High (Level 9)",
        },
      },
      {
        id: "layer-auth-2",
        type: "AUTHENTICATION",
        name: "JWT Token Signature Verifier",
        enabled: false,
        order: 3,
        params: {
          signatureScheme: "RS256-JWT",
          keyId: "PUBKEY-AUTH-04",
        },
      },
    ],
    stats: {
      totalPacketsProcessed: 342100,
      avgLatencyMs: 4.1,
      errorRatePercent: 0.03,
    },
  },
  {
    id: "STR-3105",
    name: "Harbor Logistics Terminal Feed",
    sourceZoneId: "ZN-DIST-03",
    sourceZoneName: "Ocean Gateway Logistics",
    meterCount: 510,
    status: "IDLE",
    lastProcessedAt: new Date(BASE_TIME - 1000 * 950).toISOString(),
    samplePayload: {
      meterId: "EM-PORT-911",
      timestamp: new Date(BASE_TIME).toISOString(),
      voltage: 400.2,
      currentAmps: 112.4,
      powerKw: 44.98,
      frequencyHz: 50.01,
      powerFactor: 0.95,
      totalKwh: 98124.8,
    },
    pipelineLayers: [
      {
        id: "layer-auth-3",
        type: "AUTHENTICATION",
        name: "ECDSA Digital Signature Wrapper",
        enabled: true,
        order: 1,
        params: {
          signatureScheme: "ECDSA-secp256k1",
          keyId: "KEY-PORT-PUB",
        },
      },
      {
        id: "layer-enc-3",
        type: "ENCRYPTION",
        name: "AES-256-CBC Encrypted Envelope",
        enabled: false,
        order: 2,
        params: {
          algorithm: "AES-CBC-256",
          keyId: "VAULT-PORT-02",
        },
      },
    ],
    stats: {
      totalPacketsProcessed: 182300,
      avgLatencyMs: 2.8,
      errorRatePercent: 0.05,
    },
  },
  {
    id: "STR-1044",
    name: "Old Quarter Heritage Street Feed",
    sourceZoneId: "ZN-DIST-04",
    sourceZoneName: "Historic Cultural Quarter",
    meterCount: 390,
    status: "ACTIVE",
    lastProcessedAt: new Date(BASE_TIME - 1000 * 30).toISOString(),
    samplePayload: {
      meterId: "EM-HIST-08",
      timestamp: new Date(BASE_TIME).toISOString(),
      voltage: 229.8,
      currentAmps: 8.9,
      powerKw: 2.05,
      frequencyHz: 50.0,
      powerFactor: 0.96,
      totalKwh: 3410.5,
    },
    pipelineLayers: [
      {
        id: "layer-comp-4",
        type: "COMPRESSION",
        name: "Brotli Edge Compression Wrapper",
        enabled: true,
        order: 1,
        params: {
          compressionLevel: "Fast (Level 1)",
        },
      },
      {
        id: "layer-enc-4",
        type: "ENCRYPTION",
        name: "AES-128-GCM Lightweight Cipher",
        enabled: true,
        order: 2,
        params: {
          algorithm: "AES-GCM-128",
          keyId: "KEY-IOT-EDGE-01",
        },
      },
    ],
    stats: {
      totalPacketsProcessed: 94100,
      avgLatencyMs: 1.9,
      errorRatePercent: 0.0,
    },
  },
];


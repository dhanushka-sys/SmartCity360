package com.smartcity.controller;

import com.google.gson.reflect.TypeToken;
import com.smartcity.dao.StreamDAO;
import com.smartcity.model.DataStream;
import com.smartcity.model.ProcessingLayer;
import com.smartcity.pattern.decorator.AuthenticationDecorator;
import com.smartcity.pattern.decorator.CompressionDecorator;
import com.smartcity.pattern.decorator.EncryptionDecorator;
import com.smartcity.pattern.decorator.EnergyStreamData;
import com.smartcity.pattern.decorator.StreamData;
import com.smartcity.util.JsonUtil;

import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.lang.reflect.Type;
import java.sql.SQLException;
import java.time.Instant;
import java.util.*;

@WebServlet(name = "StreamServlet", urlPatterns = {"/api/streams", "/api/streams/*"})
public class StreamServlet extends HttpServlet {

    private final StreamDAO streamDAO = new StreamDAO();

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        String pathInfo = req.getPathInfo();
        try {
            if (pathInfo == null || pathInfo.equals("/")) {
                JsonUtil.sendJson(resp, HttpServletResponse.SC_OK, streamDAO.getAllStreams());
            } else {
                String id = pathInfo.substring(1);
                DataStream stream = streamDAO.getStreamById(id);
                if (stream != null) {
                    JsonUtil.sendJson(resp, HttpServletResponse.SC_OK, stream);
                } else {
                    JsonUtil.sendJson(resp, HttpServletResponse.SC_NOT_FOUND, Map.of("error", "Stream not found"));
                }
            }
        } catch (SQLException e) {
            JsonUtil.sendJson(resp, HttpServletResponse.SC_INTERNAL_SERVER_ERROR, Map.of("error", e.getMessage()));
        }
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        String pathInfo = req.getPathInfo();
        try {
            if (pathInfo != null && pathInfo.contains("/pipeline")) {
                String streamId = pathInfo.substring(1).replace("/pipeline", "");
                DataStream stream = streamDAO.getStreamById(streamId);
                if (stream == null) {
                    JsonUtil.sendJson(resp, HttpServletResponse.SC_NOT_FOUND, Map.of("error", "Stream not found"));
                    return;
                }

                Map customReading = JsonUtil.fromRequest(req, Map.class);
                double voltage = stream.getVoltage();
                double currentAmps = stream.getCurrentAmps();
                double powerKw = stream.getPowerKw();

                if (customReading != null) {
                    if (customReading.get("voltage") instanceof Number) {
                        voltage = ((Number) customReading.get("voltage")).doubleValue();
                    }
                    if (customReading.get("currentAmps") instanceof Number) {
                        currentAmps = ((Number) customReading.get("currentAmps")).doubleValue();
                    }
                    if (customReading.get("powerKw") instanceof Number) {
                        powerKw = ((Number) customReading.get("powerKw")).doubleValue();
                    }
                }

                StreamData current = new EnergyStreamData(streamId, voltage, currentAmps, powerKw);
                String rawPayloadString = current.getData();
                int initialSize = current.getPayloadSize();

                List<ProcessingLayer> layers = stream.getPipelineLayers();
                if (layers == null) {
                    layers = List.of();
                }
                List<ProcessingLayer> activeLayers = new ArrayList<>();
                for (ProcessingLayer l : layers) {
                    if (l.isEnabled()) {
                        activeLayers.add(l);
                    }
                }
                activeLayers.sort(Comparator.comparingInt(ProcessingLayer::getLayerOrder));

                List<Map<String, Object>> steps = new ArrayList<>();
                boolean isEncrypted = false;
                boolean isAuthenticated = false;
                boolean isCompressed = false;

                int stepNumber = 1;
                for (ProcessingLayer layer : activeLayers) {
                    String inputPayload = current.getData();
                    int beforeSize = current.getPayloadSize();
                    long t0 = System.nanoTime();
                    String layerType = layer.getLayerType() != null ? layer.getLayerType().toUpperCase() : "";

                    Map<String, String> metadata = new HashMap<>();
                    String description = "";

                    if ("COMPRESSION".equals(layerType)) {
                        isCompressed = true;
                        current = new CompressionDecorator(current);
                        description = current.getDescription();
                        metadata.put("Algorithm", "GZIP");
                        metadata.put("Ratio", String.format("%.2f", ((CompressionDecorator) current).getCompressionRatio()));
                    } else if ("ENCRYPTION".equals(layerType)) {
                        isEncrypted = true;
                        current = new EncryptionDecorator(current);
                        description = current.getDescription();
                        metadata.put("Cipher", "AES-256-GCM");
                        metadata.put("TagLength", "128-bit");
                    } else if ("AUTHENTICATION".equals(layerType)) {
                        isAuthenticated = true;
                        current = new AuthenticationDecorator(current);
                        description = current.getDescription();
                        metadata.put("Algorithm", "HMAC-SHA256");
                        metadata.put("Valid", String.valueOf(((AuthenticationDecorator) current).isValid()));
                    }

                    long elapsedNanos = System.nanoTime() - t0;
                    double elapsedMs = Math.round((elapsedNanos / 1_000_000.0) * 100.0) / 100.0;
                    int afterSize = current.getPayloadSize();

                    Map<String, Object> stepResult = new HashMap<>();
                    stepResult.put("step", stepNumber++);
                    stepResult.put("layerType", layerType);
                    stepResult.put("layerName", layer.getLayerName());
                    stepResult.put("inputPayload", inputPayload);
                    stepResult.put("outputPayload", current.getData());
                    stepResult.put("byteSizeBefore", beforeSize);
                    stepResult.put("byteSizeAfter", afterSize);
                    stepResult.put("processingTimeMs", Math.max(0.1, elapsedMs));
                    stepResult.put("description", description);
                    stepResult.put("metadata", metadata);
                    steps.add(stepResult);
                }

                int finalSize = current.getPayloadSize();
                double ratio = initialSize > 0 ? (double) finalSize / initialSize : 1.0;

                Map<String, Object> responseData = new HashMap<>();
                responseData.put("streamId", streamId);
                responseData.put("rawPayloadString", rawPayloadString);
                responseData.put("finalPayloadString", current.getData());
                responseData.put("steps", steps);
                responseData.put("overallCompressionRatio", Math.round(ratio * 100.0) / 100.0);
                responseData.put("isEncrypted", isEncrypted);
                responseData.put("isAuthenticated", isAuthenticated);
                responseData.put("isCompressed", isCompressed);
                responseData.put("executedAt", Instant.now().toString());

                JsonUtil.sendJson(resp, HttpServletResponse.SC_OK, responseData);
                return;
            }

            DataStream stream = JsonUtil.fromRequest(req, DataStream.class);
            if (stream.getId() == null || stream.getId().isEmpty()) {
                stream.setId("STR-" + System.currentTimeMillis());
            }
            boolean created = streamDAO.createStream(stream);
            if (created) {
                JsonUtil.sendJson(resp, HttpServletResponse.SC_CREATED, stream);
            } else {
                JsonUtil.sendJson(resp, HttpServletResponse.SC_BAD_REQUEST, Map.of("error", "Failed to create stream"));
            }
        } catch (Exception e) {
            JsonUtil.sendJson(resp, HttpServletResponse.SC_INTERNAL_SERVER_ERROR, Map.of("error", e.getMessage()));
        }
    }

    @Override
    protected void doPut(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        String pathInfo = req.getPathInfo();
        if (pathInfo == null || pathInfo.equals("/")) {
            JsonUtil.sendJson(resp, HttpServletResponse.SC_BAD_REQUEST, Map.of("error", "Missing stream ID"));
            return;
        }

        String streamId = pathInfo.substring(1);
        if (streamId.endsWith("/layers")) {
            streamId = streamId.replace("/layers", "");
        }

        try {
            Type listType = new TypeToken<List<ProcessingLayer>>() {}.getType();
            List<ProcessingLayer> layers = JsonUtil.getGson().fromJson(req.getReader(), listType);

            boolean ok = streamDAO.updateLayers(streamId, layers);
            if (ok) {
                DataStream updated = streamDAO.getStreamById(streamId);
                JsonUtil.sendJson(resp, HttpServletResponse.SC_OK, updated);
            } else {
                JsonUtil.sendJson(resp, HttpServletResponse.SC_NOT_FOUND, Map.of("error", "Stream not found"));
            }
        } catch (Exception e) {
            JsonUtil.sendJson(resp, HttpServletResponse.SC_INTERNAL_SERVER_ERROR, Map.of("error", e.getMessage()));
        }
    }
}

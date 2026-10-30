package com.smartcity.controller;

import com.google.gson.reflect.TypeToken;
import com.smartcity.dao.StreamDAO;
import com.smartcity.model.DataStream;
import com.smartcity.model.ProcessingLayer;
import com.smartcity.util.JsonUtil;

import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.lang.reflect.Type;
import java.sql.SQLException;
import java.util.List;
import java.util.Map;

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
                DataStream s = streamDAO.getStreamById(id);
                if (s != null) {
                    JsonUtil.sendJson(resp, HttpServletResponse.SC_OK, s);
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
        try {
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


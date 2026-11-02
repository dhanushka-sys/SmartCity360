package com.smartcity.config;

import com.smartcity.dao.UserDAO;
import com.smartcity.util.JsonUtil;

import javax.servlet.*;
import javax.servlet.annotation.WebFilter;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.Map;
import java.util.Set;

@WebFilter(filterName = "AuthFilter", urlPatterns = {"/api/*"})
public class AuthFilter implements Filter {

    private static final Set<String> PUBLIC_GET_PREFIXES = Set.of(
            "/api/dashboard",
            "/api/zones",
            "/api/streams",
            "/api/streetlights",
            "/api/policies",
            "/api/complaints",
            "/api/test-center"
    );

    @Override
    public void init(FilterConfig filterConfig) {}

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {

        HttpServletRequest req = (HttpServletRequest) request;
        HttpServletResponse res = (HttpServletResponse) response;

        String method = req.getMethod();
        String uri = req.getRequestURI();

        // 1. Allow CORS pre-flight OPTIONS
        if ("OPTIONS".equalsIgnoreCase(method)) {
            chain.doFilter(request, response);
            return;
        }

        // 2. Allow public login
        if (uri.endsWith("/api/auth/login") || uri.endsWith("/auth/login")) {
            chain.doFilter(request, response);
            return;
        }

        // 3. Allow public citizen complaint submission
        if ("POST".equalsIgnoreCase(method) && uri.contains("/api/complaints")) {
            chain.doFilter(request, response);
            return;
        }

        // 4. Allow public safe GET endpoints
        if ("GET".equalsIgnoreCase(method)) {
            boolean isPublic = false;
            for (String prefix : PUBLIC_GET_PREFIXES) {
                if (uri.contains(prefix)) {
                    isPublic = true;
                    break;
                }
            }
            if (isPublic && !uri.contains("/api/auth/users")) {
                chain.doFilter(request, response);
                return;
            }
        }

        // 5. Protected operations require Bearer token validation
        String authHeader = req.getHeader("Authorization");
        String token = null;
        if (authHeader != null && authHeader.startsWith("Bearer ")) {
            token = authHeader.substring(7).trim();
        }

        if (token == null || !UserDAO.validateToken(token)) {
            JsonUtil.sendJson(res, HttpServletResponse.SC_UNAUTHORIZED,
                    Map.of("error", "Authentication required: valid Bearer token must be supplied in Authorization header"));
            return;
        }

        // 6. Role-based Authorization check for executive operations
        if (uri.contains("/api/auth/users") || "DELETE".equalsIgnoreCase(method)) {
            if (!UserDAO.hasRole(token, "CITY_MANAGER", "SUPERVISOR")) {
                JsonUtil.sendJson(res, HttpServletResponse.SC_FORBIDDEN,
                        Map.of("error", "Forbidden: operation requires executive CITY_MANAGER or SUPERVISOR role"));
                return;
            }
        }

        chain.doFilter(request, response);
    }

    @Override
    public void destroy() {}
}

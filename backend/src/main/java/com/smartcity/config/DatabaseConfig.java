package com.smartcity.config;

import java.io.InputStream;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.Properties;

public class DatabaseConfig {

    private static String url;
    private static String user;
    private static String password;

    static {
        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
            reloadProperties();
        } catch (Exception e) {
            throw new RuntimeException("Failed to initialize database configuration", e);
        }
    }

    public static synchronized void reloadProperties() {
        Properties props = new Properties();
        try (InputStream in = DatabaseConfig.class.getClassLoader().getResourceAsStream("application.properties")) {
            if (in != null) {
                props.load(in);
            }
        } catch (Exception ignored) {}

        url = props.getProperty("db.url", "jdbc:mysql://localhost:3306/smartcity360_db?useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=UTC");
        user = props.getProperty("db.user", "root");
        String pass = props.getProperty("db.password", "dbworld");
        if (pass == null || pass.trim().isEmpty()) {
            pass = "dbworld";
        }
        password = pass;
    }

    public static Connection getConnection() throws SQLException {
        if (password == null || password.trim().isEmpty()) {
            reloadProperties();
        }
        return DriverManager.getConnection(url, user, password);
    }
}

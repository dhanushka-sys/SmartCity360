package com.smartcity.config;

import java.io.InputStream;
import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Method;
import java.lang.reflect.Proxy;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.Properties;
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;

public class DatabaseConfig {

    private static String url;
    private static String user;
    private static String password;
    private static int maxPoolSize = 10;
    private static BlockingQueue<Connection> pool;
    private static final AtomicInteger totalConnectionsCreated = new AtomicInteger(0);

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

        String envUrl = System.getenv("DB_URL");
        url = (envUrl != null && !envUrl.trim().isEmpty()) ? envUrl.trim() :
                props.getProperty("db.url", "jdbc:mysql://localhost:3306/smartcity360_db?useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=UTC");

        String envUser = System.getenv("DB_USER");
        user = (envUser != null && !envUser.trim().isEmpty()) ? envUser.trim() :
                props.getProperty("db.user", "root");

        String envPass = System.getenv("DB_PASSWORD");
        if (envPass != null && !envPass.trim().isEmpty()) {
            password = envPass.trim();
        } else {
            password = props.getProperty("db.password", "dbworld");
        }

        String poolSizeStr = props.getProperty("db.pool.max", "10");
        try {
            maxPoolSize = Integer.parseInt(poolSizeStr.trim());
        } catch (Exception ignored) {
            maxPoolSize = 10;
        }

        if (pool == null) {
            pool = new ArrayBlockingQueue<>(maxPoolSize);
        }
    }

    public static Connection getConnection() throws SQLException {
        if (url == null || user == null) {
            reloadProperties();
        }

        Connection rawConn = pool.poll();
        if (rawConn != null && !rawConn.isClosed() && rawConn.isValid(1)) {
            return wrapConnection(rawConn);
        }

        if (totalConnectionsCreated.get() < maxPoolSize) {
            totalConnectionsCreated.incrementAndGet();
            Connection newConn = DriverManager.getConnection(url, user, password);
            return wrapConnection(newConn);
        }

        try {
            rawConn = pool.poll(2, TimeUnit.SECONDS);
            if (rawConn != null && !rawConn.isClosed() && rawConn.isValid(1)) {
                return wrapConnection(rawConn);
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        Connection fallback = DriverManager.getConnection(url, user, password);
        return wrapConnection(fallback);
    }

    private static Connection wrapConnection(Connection physicalConn) {
        return (Connection) Proxy.newProxyInstance(
                DatabaseConfig.class.getClassLoader(),
                new Class<?>[]{Connection.class},
                new InvocationHandler() {
                    private boolean closed = false;

                    @Override
                    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
                        if ("close".equals(method.getName())) {
                            if (!closed) {
                                closed = true;
                                if (!physicalConn.isClosed() && pool.size() < maxPoolSize) {
                                    pool.offer(physicalConn);
                                    return null;
                                }
                            }
                            physicalConn.close();
                            return null;
                        }
                        if ("isClosed".equals(method.getName())) {
                            return closed || physicalConn.isClosed();
                        }
                        return method.invoke(physicalConn, args);
                    }
                }
        );
    }

    public static int getActivePoolSize() {
        return pool != null ? pool.size() : 0;
    }

    public static int getMaxPoolSize() {
        return maxPoolSize;
    }
}

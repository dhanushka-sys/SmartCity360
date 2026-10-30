CREATE DATABASE IF NOT EXISTS smartcity360_db;
USE smartcity360_db;

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS complaint_notes;
DROP TABLE IF EXISTS complaints;
DROP TABLE IF EXISTS streetlights;
DROP TABLE IF EXISTS streetlight_profiles;
DROP TABLE IF EXISTS stream_layers;
DROP TABLE IF EXISTS data_streams;
DROP TABLE IF EXISTS zones;
DROP TABLE IF EXISTS policies;

CREATE TABLE zones (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(50) NOT NULL,
    type VARCHAR(20) NOT NULL,
    parent_id VARCHAR(50),
    status VARCHAR(20) NOT NULL,
    power_usage_kw DOUBLE NOT NULL,
    daily_consumption_kwh DOUBLE NOT NULL,
    active_sensors INT NOT NULL,
    total_sensors INT NOT NULL,
    active_streetlights INT NOT NULL,
    active_alerts INT NOT NULL,
    manager VARCHAR(100),
    floors INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE data_streams (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    source_zone_id VARCHAR(50) NOT NULL,
    source_zone_name VARCHAR(100) NOT NULL,
    meter_count INT NOT NULL,
    status VARCHAR(20) NOT NULL,
    voltage DOUBLE NOT NULL,
    current_amps DOUBLE NOT NULL,
    power_kw DOUBLE NOT NULL,
    frequency_hz DOUBLE NOT NULL,
    power_factor DOUBLE NOT NULL,
    total_kwh DOUBLE NOT NULL,
    packets_processed BIGINT NOT NULL,
    avg_latency_ms DOUBLE NOT NULL,
    error_rate_percent DOUBLE NOT NULL,
    last_processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE stream_layers (
    id VARCHAR(50) PRIMARY KEY,
    stream_id VARCHAR(50) NOT NULL,
    layer_type VARCHAR(30) NOT NULL,
    layer_name VARCHAR(100) NOT NULL,
    enabled BOOLEAN NOT NULL,
    layer_order INT NOT NULL,
    algorithm VARCHAR(50),
    FOREIGN KEY (stream_id) REFERENCES data_streams(id) ON DELETE CASCADE
);

CREATE TABLE complaints (
    id VARCHAR(50) PRIMARY KEY,
    tracking_number VARCHAR(50) NOT NULL UNIQUE,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(30) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    zone_id VARCHAR(50) NOT NULL,
    zone_name VARCHAR(100) NOT NULL,
    citizen_name VARCHAR(100) NOT NULL,
    citizen_contact VARCHAR(100) NOT NULL,
    current_handler_role VARCHAR(30) NOT NULL,
    status VARCHAR(30) NOT NULL,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolution_summary TEXT,
    resolved_at TIMESTAMP NULL
);

CREATE TABLE complaint_notes (
    id VARCHAR(50) PRIMARY KEY,
    complaint_id VARCHAR(50) NOT NULL,
    author VARCHAR(100) NOT NULL,
    role VARCHAR(30) NOT NULL,
    text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (complaint_id) REFERENCES complaints(id) ON DELETE CASCADE
);

CREATE TABLE streetlight_profiles (
    id VARCHAR(50) PRIMARY KEY,
    model_name VARCHAR(100) NOT NULL,
    manufacturer VARCHAR(100) NOT NULL,
    wattage_rating INT NOT NULL,
    lamp_type VARCHAR(50) NOT NULL,
    default_brightness INT NOT NULL,
    operating_schedule VARCHAR(50) NOT NULL,
    color_temp_kelvin INT NOT NULL
);

CREATE TABLE streetlights (
    id VARCHAR(50) PRIMARY KEY,
    serial_number VARCHAR(50) NOT NULL UNIQUE,
    profile_id VARCHAR(50) NOT NULL,
    zone_id VARCHAR(50) NOT NULL,
    zone_name VARCHAR(100) NOT NULL,
    street_name VARCHAR(100) NOT NULL,
    latitude DOUBLE NOT NULL,
    longitude DOUBLE NOT NULL,
    status VARCHAR(20) NOT NULL,
    brightness INT NOT NULL,
    power_usage_kw DOUBLE NOT NULL,
    last_ping TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (profile_id) REFERENCES streetlight_profiles(id)
);

CREATE TABLE policies (
    id VARCHAR(50) PRIMARY KEY,
    code VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(30) NOT NULL,
    expression VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    status VARCHAR(20) NOT NULL,
    applied_zones INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
    id VARCHAR(50) PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role VARCHAR(50) NOT NULL,
    department VARCHAR(100) NOT NULL,
    avatar_initials VARCHAR(10) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO zones (id, name, code, type, parent_id, status, power_usage_kw, daily_consumption_kwh, active_sensors, total_sensors, active_streetlights, active_alerts, manager, floors) VALUES
('ZN-METRO', 'Metropolis Neo-Prime', 'MNP-001', 'CITY', NULL, 'OPERATIONAL', 18450.0, 442800.0, 1420, 1450, 24500, 3, 'Dr. Aris Thorne', NULL),
('ZN-DOWNTOWN', 'Downtown Central District', 'DCD-01', 'DISTRICT', 'ZN-METRO', 'OPERATIONAL', 7200.0, 172800.0, 580, 590, 8200, 1, 'Marcus Vance', NULL),
('ZN-STREET-INNOVATION', 'Innovation Boulevard', 'STR-INV-01', 'STREET', 'ZN-DOWNTOWN', 'OPERATIONAL', 2100.0, 50400.0, 180, 185, 2400, 0, 'Sarah Jenkins', NULL),
('ZN-BLD-TECH-A', 'NeoTech Cyber Tower A', 'BLD-NTC-A', 'BUILDING', 'ZN-STREET-INNOVATION', 'OPERATIONAL', 850.0, 20400.0, 75, 75, 0, 0, 'David Kalu', 48),
('ZN-BLD-CIVIC', 'Central Civic Center', 'BLD-CCC-01', 'BUILDING', 'ZN-STREET-INNOVATION', 'OPERATIONAL', 420.0, 10080.0, 40, 42, 0, 0, 'Hannah Brooks', 14),
('ZN-STREET-FINANCIAL', 'Financial Way Arterial', 'STR-FIN-02', 'STREET', 'ZN-DOWNTOWN', 'OPERATIONAL', 3200.0, 76800.0, 240, 245, 3100, 1, 'Julian Cross', NULL),
('ZN-BLD-EXCHANGE', 'Stock Exchange Tower', 'BLD-STX-01', 'BUILDING', 'ZN-STREET-FINANCIAL', 'DEGRADED', 1650.0, 39600.0, 110, 115, 0, 1, 'Victor Sterling', 62),
('ZN-RESIDENTIAL', 'Green Valley Eco-District', 'GVE-02', 'DISTRICT', 'ZN-METRO', 'OPERATIONAL', 4800.0, 115200.0, 410, 420, 7800, 0, 'Clara Oswald', NULL),
('ZN-STREET-SOLARIS', 'Solaris Avenue', 'STR-SOL-01', 'STREET', 'ZN-RESIDENTIAL', 'OPERATIONAL', 1500.0, 36000.0, 130, 132, 2600, 0, 'Noah Bennett', NULL),
('ZN-BLD-ECO-1', 'EcoHab Complex 1', 'BLD-ECH-01', 'BUILDING', 'ZN-STREET-SOLARIS', 'OPERATIONAL', 310.0, 7440.0, 35, 35, 0, 0, 'Rachel Adams', 8),
('ZN-INDUSTRIAL', 'Port Logistics & Energy Zone', 'PLE-03', 'DISTRICT', 'ZN-METRO', 'OPERATIONAL', 6450.0, 154800.0, 430, 440, 8500, 2, 'Captain Roger Vance', NULL);

INSERT INTO data_streams (id, name, source_zone_id, source_zone_name, meter_count, status, voltage, current_amps, power_kw, frequency_hz, power_factor, total_kwh, packets_processed, avg_latency_ms, error_rate_percent) VALUES
('STR-1001', 'Downtown Financial High-Voltage Feeder', 'ZN-DOWNTOWN', 'Downtown Central District', 124, 'ACTIVE', 230.4, 196.2, 45.2, 50.1, 0.96, 128450.0, 48210, 2.1, 0.01),
('STR-1002', 'NeoTech Cyber Tower Smart Substation', 'ZN-BLD-TECH-A', 'NeoTech Cyber Tower A', 48, 'ACTIVE', 229.8, 88.5, 20.3, 49.9, 0.98, 42100.0, 21800, 1.8, 0.0),
('STR-1003', 'Green Valley Solar Microgrid Aggregator', 'ZN-RESIDENTIAL', 'Green Valley Eco-District', 86, 'ACTIVE', 231.2, 142.0, 32.8, 50.0, 0.95, 87400.0, 35940, 2.8, 0.02),
('STR-1004', 'Port Logistics Heavy Crane Industrial Grid', 'ZN-INDUSTRIAL', 'Port Logistics & Energy Zone', 62, 'ACTIVE', 230.1, 260.4, 59.9, 50.2, 0.91, 210900.0, 61200, 3.4, 0.05);

INSERT INTO stream_layers (id, stream_id, layer_type, layer_name, enabled, layer_order, algorithm) VALUES
('LAY-101', 'STR-1001', 'COMPRESSION', 'GZIP Payload Compression', true, 1, 'GZIP-Standard'),
('LAY-102', 'STR-1001', 'AUTHENTICATION', 'HMAC-SHA256 Signature', true, 2, 'HMAC-SHA256'),
('LAY-103', 'STR-1001', 'ENCRYPTION', 'AES-256-GCM Payload Encryption', true, 3, 'AES-256-GCM'),
('LAY-104', 'STR-1002', 'AUTHENTICATION', 'HMAC-SHA256 Signature', true, 1, 'HMAC-SHA256'),
('LAY-105', 'STR-1002', 'ENCRYPTION', 'AES-256-GCM Payload Encryption', true, 2, 'AES-256-GCM'),
('LAY-106', 'STR-1003', 'COMPRESSION', 'Snappy Light Compression', true, 1, 'Snappy-v1'),
('LAY-107', 'STR-1003', 'ENCRYPTION', 'AES-128-CBC Tunnel', true, 2, 'AES-128-CBC'),
('LAY-108', 'STR-1004', 'AUTHENTICATION', 'HMAC-SHA256 Signature', true, 1, 'HMAC-SHA256'),
('LAY-109', 'STR-1004', 'ENCRYPTION', 'AES-256-GCM Payload Encryption', true, 2, 'AES-256-GCM');

INSERT INTO complaints (id, tracking_number, title, description, category, severity, zone_id, zone_name, citizen_name, citizen_contact, current_handler_role, status, resolution_summary, resolved_at) VALUES
('CMP-7701', 'TRK-2026-7701', 'Hazardous Chemical Runoff Detected Near Dock 4', 'Pungent discoloration observed entering municipal drainage line near berth 12.', 'ENVIRONMENT', 'CRITICAL', 'ZN-INDUSTRIAL', 'Port Logistics & Energy Zone', 'Tariq Mansour', 'tmansour@maritime.org', 'CITY_MANAGER', 'ESCALATED', NULL, NULL),
('CMP-7702', 'TRK-2026-7702', 'Traffic Signal Synchronization Failure on Grand Arterial', 'Four consecutive traffic lights stuck on amber cycling causing extensive gridlock.', 'TRAFFIC', 'HIGH', 'ZN-DOWNTOWN', 'Downtown Central District', 'Sarah Jenkins', 'sjenkins@urbanline.net', 'SUPERVISOR', 'UNDER_REVIEW', NULL, NULL),
('CMP-7703', 'TRK-2026-7703', 'Excessive Construction Noise After 22:00', 'Heavy jackhammer operations continuing past authorized evening quiet hours.', 'NOISE', 'MEDIUM', 'ZN-STREET-INNOVATION', 'Innovation Boulevard', 'Liam O''Connor', 'liam.oc@outlook.com', 'LOCAL_STAFF', 'ASSIGNED', NULL, NULL),
('CMP-7704', 'TRK-2026-7704', 'Overflowing Smart Waste Bin at Central Plaza', 'Compactor sensor failed; garbage overflowing onto sidewalk.', 'WASTE', 'LOW', 'ZN-DOWNTOWN', 'Downtown Central District', 'Chloe Zhao', 'chloe.zhao@citymail.com', 'LOCAL_STAFF', 'RESOLVED', 'Dispatched rapid sanitation team; replaced optical sensor.', NOW()),
('CMP-7705', 'TRK-2026-7705', 'Structural Crack on Liberty Pedestrian Overpass', 'Visible horizontal fissure expanding near column foundation 3B.', 'INFRASTRUCTURE', 'CRITICAL', 'ZN-STREET-FINANCIAL', 'Financial Way Arterial', 'Dr. Evelyn Reed', 'ereed@civileng.org', 'CITY_MANAGER', 'ESCALATED', NULL, NULL);

INSERT INTO complaint_notes (id, complaint_id, author, role, text) VALUES
('NOT-01', 'CMP-7701', 'Intake Desk Dispatcher', 'LOCAL_STAFF', 'Intake registered from citizen app. Severity flagged as Critical due to toxic runoff hazards.'),
('NOT-02', 'CMP-7701', 'Sarah Jenkins', 'SUPERVISOR', 'Forwarded to City Commissioner. Emergency environmental containment dispatched.'),
('NOT-03', 'CMP-7704', 'Liam Vance', 'LOCAL_STAFF', 'Field technician dispatched at 09:15 AM. Bin emptied and optical sensor recalibrated.');

INSERT INTO streetlight_profiles (id, model_name, manufacturer, wattage_rating, lamp_type, default_brightness, operating_schedule, color_temp_kelvin) VALUES
('PRF-LED-90W', 'LumaSmart OptiBeam 90W', 'Aether Lighting Corp', 90, 'LED_SMART', 100, 'DUSK_TO_DAWN', 4000),
('PRF-SOLAR-60W', 'Helios Solar-Hybrid 60W', 'Solaria UrbanTech', 60, 'SOLAR_HYBRID', 80, 'ADAPTIVE_TRAFFIC', 3000),
('PRF-SODIUM-150W', 'HighPressureSodium Heavy 150W', 'Industrial PowerLight', 150, 'HIGH_EFFICIENCY_SODIUM', 100, 'ALWAYS_ON', 2200),
('PRF-RGB-45W', 'AvenueArt RGB Fiber Accent 45W', 'ChromaCity Ltd', 45, 'RGB_FIBER_LED', 70, 'NIGHT_DIM_50', 5000);

INSERT INTO streetlights (id, serial_number, profile_id, zone_id, zone_name, street_name, latitude, longitude, status, brightness, power_usage_kw) VALUES
('SL-001', 'SL-MNP-01-0001', 'PRF-LED-90W', 'ZN-DOWNTOWN', 'Downtown Central District', 'Innovation Boulevard', 40.7128, -74.0060, 'ONLINE', 100, 0.090),
('SL-002', 'SL-MNP-01-0002', 'PRF-LED-90W', 'ZN-DOWNTOWN', 'Downtown Central District', 'Innovation Boulevard', 40.7132, -74.0055, 'ONLINE', 100, 0.090),
('SL-003', 'SL-MNP-01-0003', 'PRF-SOLAR-60W', 'ZN-RESIDENTIAL', 'Green Valley Eco-District', 'Solaris Avenue', 40.7180, -74.0110, 'ONLINE', 80, 0.048),
('SL-004', 'SL-MNP-01-0004', 'PRF-SOLAR-60W', 'ZN-RESIDENTIAL', 'Green Valley Eco-District', 'Solaris Avenue', 40.7184, -74.0115, 'ONLINE', 80, 0.048),
('SL-005', 'SL-MNP-01-0005', 'PRF-SODIUM-150W', 'ZN-INDUSTRIAL', 'Port Logistics & Energy Zone', 'Dockside Way', 40.7050, -74.0180, 'ONLINE', 100, 0.150),
('SL-006', 'SL-MNP-01-0006', 'PRF-SODIUM-150W', 'ZN-INDUSTRIAL', 'Port Logistics & Energy Zone', 'Dockside Way', 40.7054, -74.0185, 'MAINTENANCE', 0, 0.000),
('SL-007', 'SL-MNP-01-0007', 'PRF-RGB-45W', 'ZN-DOWNTOWN', 'Downtown Central District', 'Civic Plaza Walkway', 40.7140, -74.0040, 'ONLINE', 70, 0.0315),
('SL-008', 'SL-MNP-01-0008', 'PRF-RGB-45W', 'ZN-DOWNTOWN', 'Downtown Central District', 'Civic Plaza Walkway', 40.7145, -74.0035, 'ONLINE', 70, 0.0315);

INSERT INTO policies (id, code, name, category, expression, description, status, applied_zones) VALUES
('POL-ENV-01', 'ENV-01', 'Residential Night Silence Ordinance', 'ENVIRONMENT', 'NOISE_LEVEL <= 60 AND CURRENT_HOUR >= 22', 'Restricts excessive noise above 60 dB after 10 PM in residential zones', 'ACTIVE', 4),
('POL-TRF-01', 'TRF-01', 'School Zone Speed Enforcement', 'TRAFFIC', 'VEHICLE_SPEED <= 40', 'Restricts vehicle speed to a maximum of 40 km/h in designated school areas', 'ACTIVE', 6),
('POL-ENV-02', 'ENV-02', 'Clean Air Industrial Threshold', 'ENVIRONMENT', 'AIR_QUALITY_AQI <= 100', 'Mandates factory emissions reduction whenever air quality index exceeds 100 AQI', 'ACTIVE', 3),
('POL-NRG-01', 'NRG-01', 'Peak Grid Load Curtailment', 'ENERGY', 'ENERGY_CONSUMPTION <= 5000', 'Restricts commercial sub-district load to 5000 kW during peak heatwave hours', 'ACTIVE', 2),
('POL-TRF-02', 'TRF-02', 'Commercial Avenue Parking Hours', 'TRAFFIC', 'PARKING_HOUR BETWEEN 08:00 AND 18:00', 'Enforces metered commercial parking between 8:00 AM and 6:00 PM', 'ACTIVE', 5);

INSERT INTO users (id, username, email, password, full_name, role, department, avatar_initials) VALUES
('USR-001', 'director', 'director@smartcity360.gov', 'admin123', 'Director Elena Rostova', 'CITY_MANAGER', 'Municipal Executive Directorate', 'ER'),
('USR-002', 'supervisor', 'supervisor@smartcity360.gov', 'super123', 'Supervisor Marcus Vance', 'SUPERVISOR', 'Urban Grid & Infrastructure Oversight', 'MV'),
('USR-003', 'staff', 'staff@smartcity360.gov', 'staff123', 'Officer Sarah Jenkins', 'LOCAL_STAFF', 'Central District Response Team', 'SJ'),
('USR-004', 'citizen', 'citizen@smartcity360.gov', 'citizen123', 'Dr. Evelyn Reed', 'CITIZEN', 'Metropolis Civil Engineering Union', 'ER');



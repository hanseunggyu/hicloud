-- HiCloud Monitoring System Database Schema
-- 모니터링 시스템용 데이터베이스 스키마

-- Server monitoring table
CREATE TABLE IF NOT EXISTS server (
    id INT AUTO_INCREMENT PRIMARY KEY,
    engine_type VARCHAR(50) NOT NULL,
    agent_id VARCHAR(100) NOT NULL,
    ser_cpu_count INT NOT NULL,
    ser_cpu_percent DECIMAL(5,2) NOT NULL,
    ser_memory_total INT NOT NULL,
    ser_memory_used INT NOT NULL,
    ser_memory_percent DECIMAL(5,2) NOT NULL,
    ser_get_datetime DATETIME NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Container monitoring table  
CREATE TABLE IF NOT EXISTS container (
    id INT AUTO_INCREMENT PRIMARY KEY,
    engine_type VARCHAR(50) NOT NULL,
    agent_id VARCHAR(100) NOT NULL,
    node_name VARCHAR(100) NOT NULL,
    container_name VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL,
    con_cpu_percent DECIMAL(5,2) NOT NULL,
    con_memory_usage DECIMAL(10,2) NOT NULL,
    con_memory_percent DECIMAL(5,2) NOT NULL,
    con_get_datetime DATETIME NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for better performance
CREATE INDEX idx_server_agent_datetime ON server(agent_id, ser_get_datetime);
CREATE INDEX idx_container_agent_datetime ON container(agent_id, con_get_datetime);
CREATE INDEX idx_container_name_status ON container(container_name, status);
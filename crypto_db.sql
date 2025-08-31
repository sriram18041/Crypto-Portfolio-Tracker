CREATE DATABASE IF NOT EXISTS crypto_db;
USE crypto_db;

CREATE TABLE IF NOT EXISTS portfolio (
    id INT AUTO_INCREMENT PRIMARY KEY,
    coin_id VARCHAR(50) NOT NULL,
    amount FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sentiment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    coin_id VARCHAR(50) NOT NULL,
    positive_count INT NOT NULL,
    negative_count INT NOT NULL,
    neutral_count INT NOT NULL,
    analysis_date DATE NOT NULL
);

INSERT INTO portfolio (coin_id, amount) VALUES
('bitcoin', 0.5),
('ethereum', 2.0);

INSERT INTO sentiment (coin_id, positive_count, negative_count, neutral_count, analysis_date) VALUES
('bitcoin', 2, 1, 1, CURDATE()),
('ethereum', 1, 2, 1, CURDATE());
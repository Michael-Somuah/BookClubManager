-- -----------------------------------------------------
-- Book Club Manager Database Setup
-- Group 12 - Devops Software Development Tournament 2025
-- -----------------------------------------------------

CREATE DATABASE IF NOT EXISTS bookclubdb;
USE bookclubdb;

-- USERS TABLE
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(280) UNIQUE NOT NULL,
    password VARCHAR(300) NOT NULL,
    role VARCHAR(50) DEFAULT 'member',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Default admin
INSERT INTO users (username, password, role)
SELECT 'Group12', SHA2('Devops', 256), 'admin'
WHERE NOT EXISTS (SELECT 1 FROM users WHERE username='Group12');

-- BOOKS TABLE
CREATE TABLE IF NOT EXISTS books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    genre VARCHAR(100),
    pages_total INT,
    pages_read INT DEFAULT 0,
    status VARCHAR(50) DEFAULT 'Not Started',
    rating DECIMAL(3,1),
    meeting_date DATE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- DISCUSSIONS TABLE
CREATE TABLE IF NOT EXISTS discussions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT NOT NULL,
    comment TEXT NOT NULL,
    username VARCHAR(199),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
);

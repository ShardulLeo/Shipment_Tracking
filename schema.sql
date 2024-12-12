/* schema.sql */

-- Create Users Table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Locations Table
CREATE TABLE locations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

-- Create Statuses Table
CREATE TABLE statuses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

-- Create Shipments Table
CREATE TABLE shipments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tracking_number VARCHAR(100) NOT NULL UNIQUE,
    origin_id INT NOT NULL,
    destination_id INT NOT NULL,
    current_location_id INT NOT NULL,
    status_id INT NOT NULL,
    estimated_delivery DATE,
    user_id INT NOT NULL,
    FOREIGN KEY (origin_id) REFERENCES locations(id),
    FOREIGN KEY (destination_id) REFERENCES locations(id),
    FOREIGN KEY (current_location_id) REFERENCES locations(id),
    FOREIGN KEY (status_id) REFERENCES statuses(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

ALTER TABLE users ADD COLUMN role ENUM('admin', 'user') DEFAULT 'user';
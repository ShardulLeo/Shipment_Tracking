use shipment_tracking;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL
);

-- Locations Table (Normalized)
CREATE TABLE locations (
    id INT AUTO_INCREMENT PRIMARY KEY, -- Unique location ID
    name VARCHAR(255) NOT NULL UNIQUE -- City name (e.g., "CityA")
);

-- Statuses Table
CREATE TABLE statuses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE -- e.g., "In Transit", "Delivered"
);

-- Shipments Table (Referencing Locations)
CREATE TABLE shipments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tracking_number VARCHAR(255) NOT NULL UNIQUE,
    origin_id INT, -- Foreign Key to locations table
    destination_id INT, -- Foreign Key to locations table
    current_location_id INT, -- Foreign Key to locations table
    status_id INT, -- Foreign Key to statuses table
    estimated_delivery DATE,
    user_id INT, -- Foreign Key to users table

        -- Foreign Key Constraints
    CONSTRAINT fk_origin FOREIGN KEY (origin_id) REFERENCES locations(id),
    CONSTRAINT fk_destination FOREIGN KEY (destination_id) REFERENCES locations(id),
    CONSTRAINT fk_current_location FOREIGN KEY (current_location_id) REFERENCES locations(id),
    CONSTRAINT fk_status FOREIGN KEY (status_id) REFERENCES statuses(id),
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id)
);

select * from shipments;
select * from locations;
select * from users;




/*
ADMIN CONTROL
*/

USE shipment_tracking;

-- View all users
-- View all users
SELECT
	id, 
    username, 
    email 
FROM users
ORDER BY id;

-- Add user
INSERT INTO users (username, password, email) 
VALUES ('newadmin', 'securepassword', 'admin@example.com');

-- Update user
UPDATE users 
SET email = 'updatedemail@example.com' 
WHERE id = 1;

-- Delete user
DELETE FROM users 
WHERE id = 5;

-- Count total users
SELECT 
	COUNT(*) AS total_users 
FROM users;

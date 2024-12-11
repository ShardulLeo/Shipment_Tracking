/*
ADMIN
LOCATION MANAGMENT
*/

USE shipment_tracking;

-- All location
SELECT id, name FROM locations;

-- Add new location
INSERT INTO locations (name) 
VALUES ('NewCity');

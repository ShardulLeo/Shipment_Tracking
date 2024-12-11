/*
ADMIN
SHIPMENT TRACKING
*/

USE shipment_tracking;

-- All shipments
SELECT 
    s.id, 
    u.username,
    s.tracking_number, 
    l1.name AS origin, 
    l2.name AS destination, 
    l3.name AS current_location, 
    st.name AS status, 
    s.estimated_delivery
FROM shipments s
JOIN locations l1 ON s.origin_id = l1.id
JOIN locations l2 ON s.destination_id = l2.id
JOIN locations l3 ON s.current_location_id = l3.id
JOIN statuses st ON s.status_id = st.id
JOIN users u ON s.user_id = u.id
ORDER BY 
	s.id;

-- Add shipment
INSERT INTO shipments (tracking_number, origin_id, destination_id, current_location_id, status_id, estimated_delivery, user_id)
VALUES ('TN98765', 1, 2, 1, 1, '2024-12-15', 3);

-- Search by trackingnumber
SELECT * FROM shipments 
WHERE tracking_number = 'TN12345';

-- Count by status 
SELECT st.name AS status, COUNT(*) AS total_shipments
FROM shipments s
JOIN statuses st ON s.status_id = st.id
GROUP BY st.name;

-- Overdue Shipment
SELECT 
    s.tracking_number, 
    l1.name AS origin, 
    l2.name AS destination, 
    s.estimated_delivery
FROM shipments s
JOIN locations l1 ON s.origin_id = l1.id
JOIN locations l2 ON s.destination_id = l2.id
WHERE s.estimated_delivery < CURDATE() AND s.status_id != (SELECT id FROM statuses WHERE name = 'Delivered');




/*
ADMIN - REPORTS
*/

USE shipment_tracking;

-- Total Shipments per User
SELECT 
    u.username, 
    COUNT(s.id) AS total_shipments
FROM users u
LEFT JOIN shipments s ON u.id = s.user_id
GROUP BY u.username;

-- Total Shipments by Origin Location
SELECT 
    l.name AS origin, 
    COUNT(s.id) AS total_shipments
FROM shipments s
JOIN locations l ON s.origin_id = l.id
GROUP BY l.name;

-- Delivery Performance
SELECT 
    st.name AS status, 
    COUNT(s.id) AS total_shipments, 
    ROUND(COUNT(s.id) * 100.0 / (SELECT COUNT(*) FROM shipments), 2) AS percentage
FROM shipments s
JOIN statuses st ON s.status_id = st.id
GROUP BY st.name;

-- Average delivery time
SELECT 
    st.name AS status, 
    AVG(DATEDIFF(s.estimated_delivery, CURDATE())) AS avg_days_remaining
FROM shipments s
JOIN statuses st ON s.status_id = st.id
GROUP BY st.name;


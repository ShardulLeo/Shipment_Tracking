/*
ADMIN - CANCELED vs DELIVERY Analysis
*/

USE shipment_tracking;

-- Count of Canceled vs Delivered Shipments
SELECT 
    st.name AS status, 
    COUNT(s.id) AS total_shipments
FROM shipments s
JOIN statuses st ON s.status_id = st.id
WHERE st.name IN ('Canceled', 'Delivered')
GROUP BY st.name;

-- Percentage of Canceled vs Delivered Shipments
SELECT 
    st.name AS status, 
    COUNT(s.id) AS total_shipments, 
    ROUND(COUNT(s.id) * 100.0 / (SELECT COUNT(*) FROM shipments), 2) AS percentage
FROM shipments s
JOIN statuses st ON s.status_id = st.id
WHERE st.name IN ('Canceled', 'Delivered')
GROUP BY st.name;

-- Canceled vs Delivered by Origin Location
SELECT 
    l.name AS origin, 
    st.name AS status, 
    COUNT(s.id) AS total_shipments
FROM shipments s
JOIN statuses st ON s.status_id = st.id
JOIN locations l ON s.origin_id = l.id
WHERE st.name IN ('Canceled', 'Delivered')
GROUP BY l.name, st.name
ORDER BY l.name, st.name;

-- Monthly Trend of Canceled vs Delivered Shipments
SELECT 
    DATE_FORMAT(s.estimated_delivery, '%Y-%m') AS month, 
    st.name AS status, 
    COUNT(s.id) AS total_shipments
FROM shipments s
JOIN statuses st ON s.status_id = st.id
WHERE st.name IN ('Canceled', 'Delivered')
GROUP BY month, st.name
ORDER BY month, st.name;

-- Canceled vs Delivered by User
SELECT 
    u.username, 
    st.name AS status, 
    COUNT(s.id) AS total_shipments
FROM shipments s
JOIN statuses st ON s.status_id = st.id
JOIN users u ON s.user_id = u.id
WHERE st.name IN ('Canceled', 'Delivered')
GROUP BY u.username, st.name
ORDER BY u.username, st.name;

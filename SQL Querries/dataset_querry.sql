/*
Dataset to predict canceled orders
*/

USE shipment_tracking;
WITH raw_data as 
(SELECT 
    s.tracking_number,
    s.origin_id,
    s.destination_id,
    s.current_location_id,
    s.estimated_delivery,
    DATEDIFF(s.estimated_delivery, CURDATE()) AS days_to_delivery,
    u.id AS user_id,
    st.name AS status -- Use as the target variable
FROM shipments s
JOIN users u ON s.user_id = u.id
JOIN statuses st ON s.status_id = st.id
)
SELECT *,
    CASE 
        WHEN status = 'Canceled' THEN 1
        ELSE 0
    END AS is_canceled
FROM raw_data AS label_data;


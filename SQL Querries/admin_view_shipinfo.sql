/*
ADMIN VIEW
SHIPMENT ID, USER ID, ORIGIN, DESTINATION
*/

USE shipment_tracking;

SELECT  s.id SHIP_ID, user_id USER_ID, lo.name ORIGIN, ld.name DESTINATION
FROM shipments s 
JOIN locations lo on s.origin_id = lo.id
JOIN locations ld on s.destination_id = ld.id
ORDER BY s.id;

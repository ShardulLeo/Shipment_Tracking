from flask import Blueprint, jsonify, request
from utils.db_utils import get_db_connection
import requests

api_bp = Blueprint('api', __name__)

@api_bp.route('/shipments', methods=['GET'])
def get_shipments():
    tracking_number = request.args.get('tracking_number')
    if not tracking_number:
        return jsonify({'error': 'Tracking number is required'}), 400

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT s.tracking_number, l1.name AS origin, l2.name AS destination, l3.name AS current_location, 
               st.name AS status, s.estimated_delivery
        FROM shipments s
        JOIN locations l1 ON s.origin_id = l1.id
        JOIN locations l2 ON s.destination_id = l2.id
        JOIN locations l3 ON s.current_location_id = l3.id
        JOIN statuses st ON s.status_id = st.id
        WHERE s.tracking_number = %s
    """, (tracking_number,))
    shipment = cursor.fetchone()
    db.close()

    if not shipment:
        return jsonify({'error': 'Shipment not found'}), 404

    return jsonify(shipment)

@api_bp.route('/search_shipments', methods=['GET'])
def search_shipments():
    status = request.args.get('status')
    origin = request.args.get('origin')
    destination = request.args.get('destination')

    query = "SELECT * FROM shipments WHERE 1=1"
    params = []

    if status:
        query += " AND status_id = (SELECT id FROM statuses WHERE name = %s)"
        params.append(status)
    if origin:
        query += " AND origin_id = (SELECT id FROM locations WHERE name = %s)"
        params.append(origin)
    if destination:
        query += " AND destination_id = (SELECT id FROM locations WHERE name = %s)"
        params.append(destination)

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute(query, params)
    results = cursor.fetchall()
    db.close()
    return jsonify(results)

@api_bp.route('/predict_cancellation', methods=['POST'])
def predict_cancellation_endpoint():
    data = request.json
    prediction = predict_cancellation(data)
    return jsonify({'is_canceled': bool(prediction)})
from flask import Blueprint, jsonify, request
from utils.db_utils import get_db_connection
import requests
import os

analytics_bp = Blueprint('analytics', __name__)

# Endpoint: Get analytics data
@analytics_bp.route('/', methods=['GET'])
def analytics():
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        # Query: Total shipments
        cursor.execute("SELECT COUNT(*) AS total_shipments FROM shipments")
        total_shipments = cursor.fetchone()['total_shipments']

        # Query: Shipment status summary
        cursor.execute("""
            SELECT st.name AS status, COUNT(*) AS total
            FROM shipments s
            JOIN statuses st ON s.status_id = st.id
            GROUP BY st.name
        """)
        status_summary = cursor.fetchall()

        db.close()
        return jsonify({
            'total_shipments': total_shipments,
            'status_summary': status_summary,
        })
    except Exception as e:
        return jsonify({'error': 'Failed to fetch analytics data', 'details': str(e)}), 500


@analytics_bp.route('/optimize_route', methods=['GET'])
def optimize_route():
    origin = request.args.get('origin')
    destination = request.args.get('destination')

    if not origin or not destination:
        return jsonify({'error': 'Both origin and destination are required.'}), 400

    try:
        api_key = os.getenv('AIzaSyBs4-hYnPbLd0jwK8fFxpwfFvbqQ3LfJ6k')  # Replace with your environment variable
        url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={api_key}"
        response = requests.get(url)

        if response.status_code != 200:
            return jsonify({'error': 'Failed to fetch route details', 'details': response.text}), response.status_code

        return response.json()
    except Exception as e:
        return jsonify({'error': 'Failed to fetch route details', 'details': str(e)}), 500
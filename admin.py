from flask import Blueprint, jsonify, request, session, redirect, url_for
from utils.db_utils import get_db_connection

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/users', methods=['GET'])
def manage_users():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, username, email, role FROM users")
    users = cursor.fetchall()
    db.close()
    return jsonify(users)

@admin_bp.route('/search_shipments', methods=['GET'])
def admin_search_shipments():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('auth.login'))

    status = request.args.get('status')
    origin = request.args.get('origin')
    destination = request.args.get('destination')

    query = """
        SELECT s.tracking_number, u.username, u.email, l1.name AS origin, 
               l2.name AS destination, st.name AS status, s.estimated_delivery
        FROM shipments s
        JOIN users u ON s.user_id = u.id
        JOIN locations l1 ON s.origin_id = l1.id
        JOIN locations l2 ON s.destination_id = l2.id
        JOIN statuses st ON s.status_id = st.id
        WHERE 1=1
    """
    params = []

    if status:
        query += " AND st.name = %s"
        params.append(status)
    if origin:
        query += " AND l1.name = %s"
        params.append(origin)
    if destination:
        query += " AND l2.name = %s"
        params.append(destination)

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute(query, params)
    results = cursor.fetchall()
    db.close()

    return jsonify(results)

@admin_bp.route('/canceled_shipments', methods=['GET'])
def canceled_shipments():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT s.tracking_number, u.username, l1.name AS origin, l2.name AS destination, 
               st.name AS status, s.estimated_delivery
        FROM shipments s
        JOIN users u ON s.user_id = u.id
        JOIN locations l1 ON s.origin_id = l1.id
        JOIN locations l2 ON s.destination_id = l2.id
        JOIN statuses st ON s.status_id = st.id
        WHERE s.is_canceled = 1
    """)
    canceled_shipments = cursor.fetchall()
    db.close()
    return jsonify(canceled_shipments)

@admin_bp.route('/shipment_history', methods=['GET'])
def shipment_history():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('auth.login'))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT DATE_FORMAT(estimated_delivery, '%Y-%m') AS month, COUNT(*) AS shipment_count
            FROM shipments
            GROUP BY month
            ORDER BY month DESC
        """)
        monthly_shipments = cursor.fetchall()

        cursor.execute("""
            SELECT u.username, COUNT(*) AS shipment_count
            FROM shipments s
            JOIN users u ON s.user_id = u.id
            GROUP BY u.username
            ORDER BY shipment_count DESC
        """)
        shipments_per_user = cursor.fetchall()

        db.close()

        return jsonify({
            'monthly_shipments': monthly_shipments,
            'shipments_per_user': shipments_per_user
        })

    except Exception as e:
        db.close()
        return jsonify({'error': str(e)}), 500

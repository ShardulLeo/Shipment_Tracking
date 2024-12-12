from flask import Blueprint, jsonify, request, session, redirect, url_for, render_template
from utils.db_utils import get_db_connection

user_bp = Blueprint('user', __name__)

@user_bp.route('/user-shipment')
def user_shipment():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))  # Redirect to login if not logged in

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # Fetch shipments for the logged-in user
    cursor.execute("""
        SELECT s.tracking_number, l1.name AS origin, l2.name AS destination, 
               st.name AS status, s.estimated_delivery
        FROM shipments s
        JOIN locations l1 ON s.origin_id = l1.id
        JOIN locations l2 ON s.destination_id = l2.id
        JOIN statuses st ON s.status_id = st.id
        WHERE s.user_id = %s
    """, (session['user_id'],))
    shipments = cursor.fetchall()
    cursor.close()
    db.close()

    # Render home.html and pass shipment data
    return render_template('home.html', username=session['username'], shipments=shipments)

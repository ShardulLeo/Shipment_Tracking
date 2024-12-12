from flask import Blueprint, request, jsonify
from utils.db_utils import get_db_connection

feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route('/feedback_message', methods=['POST'])
def feedback():
    """
    Handles user feedback submission.
    """
    try:
        data = request.json
        user_id = data.get('user_id')
        message = data.get('message')

        # Validate inputs
        if not user_id or not isinstance(user_id, int):
            return jsonify({'error': 'Invalid or missing user_id'}), 400
        if not message or not isinstance(message, str) or len(message) > 500:
            return jsonify({'error': 'Invalid or missing message. Max length is 500 characters'}), 400

        # Database operations
        db = get_db_connection()
        cursor = db.cursor()
        try:
            cursor.execute("INSERT INTO feedback (user_id, message) VALUES (%s, %s)", (user_id, message))
            db.commit()
        finally:
            cursor.close()
            db.close()

        return jsonify({'message': 'Feedback submitted successfully'}), 201
    except Exception as e:
        # Log the exception (assuming a logging setup exists)
        # logger.error(f"Failed to submit feedback: {e}")
        print(f"Error: {e}")  # Replace with logger in production
        return jsonify({'error': 'Failed to submit feedback'}), 500

from auth import auth_bp
from api import api_bp
from analytics import analytics_bp
from feedback import feedback_bp
from admin import admin_bp
from user import user_bp
from models.predict_cancellation import predict_cancellation
from flask import Flask, Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from utils.db_utils import get_db_connection

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = '231b5308a683f661b7efb851945d5131'

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(analytics_bp, url_prefix='/analytics')
app.register_blueprint(feedback_bp, url_prefix='/feedback')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(user_bp, url_prefix='/user-shipment')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('auth.login'))  # Redirect to login if not logged in

if __name__ == '__main__':
    app.run(debug=True)

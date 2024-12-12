from flask import Flask, Blueprint, render_template, request, redirect, url_for, session
from utils.db_utils import get_db_connection

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form.get('email')  # Optional if email isn't used
        password = request.form['password']
        role = 'user'  # Default role if roles aren't explicitly used

        # Connect to database
        db = get_db_connection()
        cursor = db.cursor()

        # Insert user into existing `users` table
        cursor.execute(
            "INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)",
            (username, email, password, role)
        )
        db.commit()
        cursor.close()
        db.close()

        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        # Fetch user by username
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        db.close()

        # Validate password (assuming plaintext password comparison)
        if user and user['password'] == password:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user.get('role', 'user')  # Default to 'user'
            return redirect(url_for('user.user_shipment'))
        
        return render_template('login.html', error="Invalid username or password.")

    return render_template('login.html')

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

@auth_bp.route('/admin')
def admin():
    if 'user_id' not in session:
        flash('You need to log in first.')
        return redirect(url_for('auth.login'))

    if session.get('role') != 'admin':
        flash('Access denied. Admins only.')
        return redirect(url_for('index'))

    return render_template('admin_dashboard.html')

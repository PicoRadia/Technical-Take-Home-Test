from flask import Blueprint, render_template, request, redirect, url_for
import mysql.connector

auth_bp = Blueprint('auth', __name__, template_folder='../templates')

# Database configuration
db_config = {
    'host': 'picoRadia.mysql.pythonanywhere-services.com',
    'user': 'picoRadia',
    'password': 'radia@betterearth',
    'database': 'picoRadia$better_earth_db'
}

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login form submission
        username = request.form.get('username')
        password = request.form.get('password')

        # Connect to the database
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()

        # Perform authentication logic
        query = "SELECT * FROM logins WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()

        if result:
            # Successful login
            return redirect(url_for('auth.dashboard'))
        else:
            # Invalid credentials
            error_message = 'Invalid username or password'
            return render_template('login.html', error_message=error_message)

    return render_template('login.html')


@auth_bp.route('/dashboard' , methods=['GET', 'POST'])
def dashboard():
    # Protected route for logged-in users
    return render_template('dashboard.html')

@auth_bp.route('/documentation' )
def documentation():
    return render_template('documentation.html')

@auth_bp.route('/logout')
def logout():
    # Handle logout functionality
    return redirect(url_for('auth.login'))

@auth_bp.route('/search')
def search():
    return render_template('dashboard.html')

@auth_bp.route('/feedback')
def feedback():
    return render_template('feedback.html')

@auth_bp.route('/about')
def about():
    return render_template('about.html')

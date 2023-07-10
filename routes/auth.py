from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import mysql.connector
import requests
from utils.utility_rate_finder import UtilityRateFinder
from requests.exceptions import ProxyError, ConnectionError
import json

auth_bp = Blueprint('auth', __name__, template_folder='../templates')

proxies = {
    "http": None,  # Bypass HTTP proxy
    "https": None,  # Bypass HTTPS proxy
}


# Google Places API key
google_api_key = 'AIzaSyCnz6CYBwoue5J559-_sgRLHD6WIaQKb3w'

# NREL API key
nrel_api_key = "bnHKPIbk3cLZrMdwsac1odH9LsAFEp5FYjzrlAzi"



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

@auth_bp.route('/address-suggestions')
def address_suggestions():
    query = request.args.get('query')

    url = f'https://maps.googleapis.com/maps/api/place/autocomplete/json?input={query}&key={google_api_key}'

    response = requests.get(url)
    data = response.json()

    suggestions = []
    if data['status'] == 'OK':
        predictions = data['predictions']
        suggestions = [prediction['description'] for prediction in predictions]

    return jsonify({'suggestions': suggestions})



@auth_bp.route('/utility-rate', methods=['POST'])
def utility_rate():
    data = request.get_json()
    address = data.get('address')
    print(address)
    # Create an instance of UtilityRateFinder
    rate_finder = UtilityRateFinder(api_key='bnHKPIbk3cLZrMdwsac1odH9LsAFEp5FYjzrlAzi')

    # Get the utility rate using the address
    utility_rate = rate_finder.get_utility_rate(address)

    if utility_rate is not None:
        output = {
            "address": address,
            "residential_utility_rate": utility_rate
        }
        json_output = json.dumps(output, indent=4)
        print(json_output)
    else:
        print("Failed to retrieve utility rate.")


    return jsonify({'utility_rate': utility_rate})


@auth_bp.route('/search', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        address = request.form.get('address')

        # Create an instance of UtilityRateFinder
        rate_finder = UtilityRateFinder(api_key='bnHKPIbk3cLZrMdwsac1odH9LsAFEp5FYjzrlAzi')

        # Get the utility rate using the address
        utility_rate = rate_finder.get_utility_rate(address)

        if utility_rate is not None:
            # Successful utility rate retrieval
            return render_template('dashboard.html', utility_rate=utility_rate)
        else:
            # Utility rate not found
            error_message = 'Utility rate not found'
            return render_template('dashboard.html', error_message=error_message)

    # Render the initial dashboard template
    return render_template('dashboard.html', utility_rate=None, error_message=None)



@auth_bp.route('/documentation')
def documentation():
    return render_template('documentation.html')


@auth_bp.route('/logout')
def logout():
    # Handle logout functionality
    return redirect(url_for('auth.login'))




@auth_bp.route('/feedback')
def feedback():
    return render_template('feedback.html')


@auth_bp.route('/about')
def about():
    return render_template('about.html')

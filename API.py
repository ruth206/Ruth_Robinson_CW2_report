from flask import Flask, request, jsonify
import requests
from create_connection import make_connection  # Import to make a connection to the server

app = Flask(__name__)

# URL for the authenticator API
auth_api_url = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"

# Authenticate the user by checking their email and password
def authenticate_user(email, password):
    auth_credentials = {
        "email": email,
        "password": password
    }
    
    response = requests.post(auth_api_url, json=auth_credentials)
    
    # Check if the response is successful and the user is verified
    if response.status_code == 200:
        response_data = response.json()
        if isinstance(response_data, list) and 'Verified' in response_data and 'True' in response_data:
            return True  # User is authenticated
        else:
            return False  # User verification failed
    else:
        return False  # Authentication failed

# Create a trail
@app.route('/trails', methods=['POST'])
def add_trail():
    # Get user credentials (email and password) from the request headers or body
    email = request.json.get('email')
    password = request.json.get('password')
    
    # Authenticate the user before proceeding
    if not authenticate_user(email, password):
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.json
    conn = make_connection()
    cursor = conn.cursor()
    cursor.execute('''
        EXEC CW2.AddTrail @TrailName=?, @TrailSummary=?, @TrailDescription=?, @Difficulty=?, 
                          @Location=?, @Length=?, @ElevationGain=?, @RouteType=?, @OwnerID=?
    ''', (data['trail_name'], data['trail_summary'], data['trail_description'], 
          data['difficulty'], data['location'], data['length'], 
          data['elevation_gain'], data['route_type'], data['owner_id']))

    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Trail added successfully'}), 201

# View a trail
@app.route('/trails/<int:trail_id>', methods=['GET'])
def get_trail(trail_id):
    # Get user credentials (email and password) from the request headers or body
    email = request.args.get('email')
    password = request.args.get('password')
    
    # Authenticate the user before proceeding
    if not authenticate_user(email, password):
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = make_connection()
    cursor = conn.cursor()
    cursor.execute('EXEC CW2.GetTrailById @TrailId=?', (trail_id,))
    trail = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if trail:
        return jsonify({'trail': trail}), 200
    else:
        return jsonify({'error': 'Trail not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

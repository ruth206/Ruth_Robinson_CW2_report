from flask import Flask, request, jsonify
import requests
from create_connection import make_connection  # Import to make a connection to the server

app = Flask(__name__)

# URL for the authenticator API
auth_api_url = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"

# Define a function to authenticate user credentials
def authenticate_user(email, password):
    auth_credentials = {
        "email": email,
        "password": password
    }
    
    response = requests.post(auth_api_url, json=auth_credentials)
    
    # Checking if the login was successful
    if response.status_code == 200:
        response_data = response.json()
        print("Debug: Auth Response Data:", response_data)  # Debugging statement
        if isinstance(response_data, list) and 'Verified' in response_data and 'True' in response_data:
            return True  # User is authenticated and verified
        else:
            return False  # User verification failed
    else:
        return False  # Authentication failed

# Define a function to check if the user is an admin
def is_admin_user(email, password):
    auth_credentials = {
        "email": email,
        "password": password
    }
    
    response = requests.post(auth_api_url, json=auth_credentials)
    
    if response.status_code == 200:
        try:
            response_data = response.json()
            print("Debug: Response Data Type:", type(response_data))  # Log the type of response data
            print("Debug: Raw Response Data:", response_data)  # Log the raw response data
            
            # Define a list of admin users based on the provided accounts
            admin_users = ["ada@plymouth.ac.uk", "tim@plymouth.ac.uk"]
            
            # Check if response_data is a list and contains 'True'
            if isinstance(response_data, list) and 'True' in response_data:
                print("Debug: Response is a list containing 'True'")
                # Check if the email is in the admin users list
                return email in admin_users
            
            else:
                print("Debug: Unexpected response format or 'True' not in response_data:", response_data)
                return False
        
        except ValueError:
            print("Failed to parse JSON response")
            return False
    else:
        print(f"Failed to authenticate. Status code: {response.status_code}, Response: {response.text}")
        return False

# Create a trail (admin only)
@app.route('/trails', methods=['POST'])
def add_trail():
    # Get user credentials
    email = request.json.get('email')
    password = request.json.get('password')
    
    # Check if the user is an admin
    if not is_admin_user(email, password):
        return jsonify({'error': 'Unauthorized - Admin access required'}), 401

    data = request.json

    # Check if OwnerID exists
    owner_id = data.get('owner_id')
    conn = make_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM CW2.Users WHERE UserID = ?', (owner_id,))
    owner = cursor.fetchone()
    if not owner:
        return jsonify({'error': 'Invalid OwnerID'}), 400

    cursor.execute('''
        EXEC CW2.AddTrail @TrailName=?, @TrailSummary=?, @TrailDescription=?, @Difficulty=?, 
                          @Location=?, @Length=?, @ElevationGain=?, @RouteType=?, @OwnerID=?
    ''', (data['trail_name'], data['trail_summary'], data['trail_description'], 
          data['difficulty'], data['location'], data['length'], 
          data['elevation_gain'], data['route_type'], owner_id))

    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Trail added successfully'}), 201

# View a trail (anyone can view)
@app.route('/trails/<int:trail_id>', methods=['GET'])
def get_trail(trail_id):
    try:
        conn = make_connection()
        cursor = conn.cursor()
        cursor.execute('EXEC CW2.GetTrailById @TrailID=?', (trail_id,))
        trail = cursor.fetchone()
        print("Debug: Trail fetched:", trail)
        cursor.close()
        conn.close()
        
        if trail:
            columns = ["TrailID", "TrailName", "TrailSummary", "TrailDescription", "Difficulty",
                       "Location", "Length", "ElevationGain", "RouteType", "OwnerID"]
            trail_dict = dict(zip(columns, trail))
            return jsonify({'trail': trail_dict}), 200
        else:
            return jsonify({'error': 'Trail not found'}), 404
    
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'Internal server error'}), 500

# Update a trail (admin only)
@app.route('/trails/<int:trail_id>', methods=['PUT'])
def update_trail(trail_id):
    # Get user credentials
    email = request.json.get('email')
    password = request.json.get('password')
    
    # Check if the user is an admin
    if not is_admin_user(email, password):
        return jsonify({'error': 'Unauthorized - Admin access required'}), 401
    
    data = request.json

    # Check if all keys are present in the request body
    required_keys = ['trail_name', 'trail_summary', 'trail_description', 'difficulty', 'location', 
                     'length', 'elevation_gain', 'route_type', 'owner_id']
    for key in required_keys:
        if key not in data:
            return jsonify({'error': f'Missing key: {key}'}), 400

    # Check if OwnerID exists
    owner_id = data.get('owner_id')
    conn = make_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM CW2.Users WHERE UserID = ?', (owner_id,))
    owner = cursor.fetchone()
    if not owner:
        return jsonify({'error': 'Invalid OwnerID'}), 400

    cursor.execute('''
        EXEC CW2.UpdateTrail @TrailID=?, @TrailName=?, @TrailSummary=?, @TrailDescription=?, @Difficulty=?, 
                             @Location=?, @Length=?, @ElevationGain=?, @RouteType=?, @OwnerID=?
    ''', (trail_id, data['trail_name'], data['trail_summary'], data['trail_description'], 
          data['difficulty'], data['location'], data['length'], 
          data['elevation_gain'], data['route_type'], owner_id))

    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Trail updated successfully'}), 200

# Delete a trail (admin only)
@app.route('/trails/<int:trail_id>', methods=['DELETE'])
def delete_trail(trail_id):
    # Get user credentials
    email = request.json.get('email')
    password = request.json.get('password')
    
    # Check if the user is an admin
    if not is_admin_user(email, password):
        return jsonify({'error': 'Unauthorized - Admin access required'}), 401
    
    conn = make_connection()
    cursor = conn.cursor()
    cursor.execute('EXEC CW2.DeleteTrail @TrailID=?', (trail_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Trail deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

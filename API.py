from flask import Flask, request, jsonify
import requests
from create_connection import make_connection  #Import to make a connection to the server
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yaml'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'trails' : "Trail API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


auth_api_url = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"

#function to verify users credentials
def authenticate_user(email, password):
    auth_credentials = {
        "email": email,
        "password": password
    }
    
    response = requests.post(auth_api_url, json=auth_credentials)
    
    #checking to see if login was successful
    if response.status_code == 200:
        response_data = response.json()
        print("Debug: Auth Response Data:", response_data)
        if isinstance(response_data, list) and 'Verified' in response_data and 'True' in response_data:
            return True 
        else:
            return False 
    else:
        return False 

#function to see if the user is admin
def is_admin_user(email, password):
    auth_credentials = {
        "email": email,
        "password": password
    }
    
    response = requests.post(auth_api_url, json=auth_credentials)
    
    if response.status_code == 200:
        try:
            response_data = response.json()
            print("Debug: Response Data Type:", type(response_data))
            print("debug: Response Data:", response_data)
            
            #list of admin users
            admin_users = ["ada@plymouth.ac.uk", "tim@plymouth.ac.uk"]
            
            
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

# Create a trail 
@app.route('/trails', methods=['POST'])
def add_trail():
    # Get user credentials
    email = request.json.get('email')
    password = request.json.get('password')
    
    #checking the user is admin
    if not is_admin_user(email, password):
        return jsonify({'error': 'Unauthorized - Admin access required'}), 401

    data = request.json

    #Checking to see if OwnerID exists
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

#Viewing a trail
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

#Updating a trail
@app.route('/trails/<int:trail_id>', methods=['PUT'])
def update_trail(trail_id):
    
    email = request.json.get('email')
    password = request.json.get('password')
    
    
    if not is_admin_user(email, password):
        return jsonify({'error': 'Unauthorized - Admin access required'}), 401
    
    data = request.json

    
    required_keys = ['trail_name', 'trail_summary', 'trail_description', 'difficulty', 'location', 
                     'length', 'elevation_gain', 'route_type', 'owner_id']
    for key in required_keys:
        if key not in data:
            return jsonify({'error': f'Missing key: {key}'}), 400

    
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

#Deleting a trail
@app.route('/trails/<int:trail_id>', methods=['DELETE'])
def delete_trail(trail_id):
    # Get user credentials
    email = request.json.get('email')
    password = request.json.get('password')
    
    
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



from create_connection import make_connection

# Function to get the most recent TrailID
def get_most_recent_trail_id():
    conn = make_connection()
    cursor = conn.cursor()
    
    # Execute the query to get the most recent TrailID
    cursor.execute('''
        SELECT TOP 1 TrailID FROM CW2.Trails ORDER BY TrailID DESC
    ''')
    
    # Fetch the result
    result = cursor.fetchone()
    
    # Close the connection
    cursor.close()
    conn.close()
    
    # Return the most recent TrailID
    if result:
        return result.TrailID
    else:
        return None

# Example usage after adding a new trail
most_recent_trail_id = get_most_recent_trail_id()
if most_recent_trail_id:
    print(f"The most recent TrailID is {most_recent_trail_id}")
else:
    print("No trails found.")

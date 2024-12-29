from create_connection import make_connection


def get_most_recent_trail_id():
    conn = make_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT TOP 1 TrailID FROM CW2.Trails ORDER BY TrailID DESC
    ''')
    
    
    result = cursor.fetchone()
    
    
    cursor.close()
    conn.close()
    
    
    if result:
        return result.TrailID
    else:
        return None

most_recent_trail_id = get_most_recent_trail_id()
if most_recent_trail_id:
    print(f"The most recent TrailID is {most_recent_trail_id}")
else:
    print("No trails found.")
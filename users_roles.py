
import bcrypt
from create_connection import make_connection  #Import to make a connection to the server

conn = make_connection()
cursor = conn.cursor()

#users and their roles
users = [
    {"email": "tim@plymouth.ac.uk", "username": "Tim Berners-Lee", "password": "COMP2001!", "role": "Admin"},
    {"email": "grace@plymouth.ac.uk", "username": "Grace Hopper", "password": "ISAD123!", "role": "User"}
]

#add or update the user in the database 
for user in users:
    # Hash the password
    hashed_password = bcrypt.hashpw(user["password"].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    #checking to see if the user exsists
    cursor.execute('''
        SELECT * FROM CW2.Users
        WHERE EmailAddress = ?;
    ''', (user["email"],))
    existing_user = cursor.fetchone()
    
    if existing_user:
        #updating user
        cursor.execute('''
            EXEC CW2.UpdateUser
                @UserId = ?,
                @EmailAddress = ?,
                @Username = ?,
                @PasswordHash = ?,
                @Role = ?
        ''', (existing_user[0], user["email"], user["username"], hashed_password, user["role"]))
        print(f"Updated User: {user['email']}")
    else:
        #adding user
        cursor.execute('''
            EXEC CW2.AddUser
                @EmailAddress = ?,
                @Username = ?,
                @PasswordHash = ?,
                @Role = ?
        ''', (user["email"], user["username"], hashed_password, user["role"]))
        print(f"Added User: {user['email']}")

conn.commit()

# Verify insertion or update
for user in users:
    cursor.execute('''
        SELECT * FROM CW2.Users
        WHERE EmailAddress = ?;
    ''', (user["email"],))
    inserted_user = cursor.fetchone()
    print(f"Verified User: {inserted_user}")

cursor.close()
conn.close()
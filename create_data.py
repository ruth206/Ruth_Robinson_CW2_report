import bcrypt
from create_connection import make_connection  # Import to make a connection to the server



conn = make_connection()  
cursor = conn.cursor()

password = 'insecurePassword'
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()) #hashing password with salt to store in server

#adding the admin user into user table with hashed password for security
cursor.execute('''
    INSERT INTO CW2.Users(UserID, EmailAddress, Username, Password, Role)
    VALUES(?, ?, ?, ?, ?)
               
''',(1, 'ada@plymouth.ac.uk', 'Ada Lovelace', hashed, 'Admin' ))


#inserting test data into trails table
cursor.execute('''
    INSERT INTO CW2.Trails(TrailID, TrailName, TrailSummary, TrailDescription, Difficulty, Location, Length, ElevationGain, RouteType, OwnerID)
    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', (
    288, 
    'Bude Coast and Canal Circular', 
    'Takes an average of 2h 33m, popular area for birds, hiking and mountain biking',  
    'This trail is an incredible and stunning route winding at the very pretty coastline and the canal with amazing views. It is an easy route to follow, but when it\'s raining, the fields can get very muddy, making it necessary to wear proper boots. This place offers incredible opportunities to snap lots of unique and breathtaking photos.',
    'Moderate',  
    'Bude, Cornwall, England', 
    10.6,  
    193,  
    'Loop',  
    1  
))
print('trail test data inserted')


conn.commit()
conn.close()

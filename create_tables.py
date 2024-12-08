from create_connection import make_connection  #import to make a connection to the server

conn = make_connection()  
cursor = conn.cursor()

#User table
cursor.execute (''' 
    CREATE TABLE CW2.Users (
        UserID INT PRIMARY KEY,
        EmailAddress VARCHAR(255) NOT NULL,
        Username VARCHAR(255) UNIQUE NOT NULL,
        Password VARCHAR(255) NOT NULL,  
        Role VARCHAR(50) NOT NULL
    )
''')
print("users created")

#trails table
cursor.execute (''' 
    CREATE TABLE CW2.Trails (
        TrailID INT PRIMARY KEY,
        TrailName VARCHAR(255) NOT NULL,
        TrailSummary TEXT,
        TrailDescription TEXT,
        Difficulty VARCHAR(255),
        Location VARCHAR(255),
        Length DECIMAL(10,2),  
        ElevationGain DECIMAL(10,2),  
        RouteType VARCHAR(255),
        OwnerID INT,
        FOREIGN KEY (OwnerID) REFERENCES CW2.Users(UserID)
    )
''')
print("trails table created")

#trail location point table
cursor.execute (''' 
    CREATE TABLE CW2.Trail_locationPt (
        TrailID INT,
        LocationPointID INT,  
        OrderNo INT,
        FOREIGN KEY(TrailID) REFERENCES CW2.TRAILS(TrailID)
    )
''')
print("trails locationpt created")

#location point table
cursor.execute (''' 
    CREATE TABLE CW2.Location_point (
        LocationPointID INT PRIMARY KEY, 
        Latitude FLOAT,
        Longitude FLOAT,
        Description TEXT
    )
''')
print("location point created")

#trail feature table
cursor.execute (''' 
    CREATE TABLE CW2.TrailFeature (
        TrailID INT,
        FeatureID INT,  
        FOREIGN KEY (TrailID) REFERENCES CW2.Trails(TrailID)
    )
''')
print("trail features created")

#feature table
cursor.execute (''' 
    CREATE TABLE CW2.Feature (
        FeatureID INT PRIMARY KEY,  
        TrailFeature VARCHAR(255)
    )
''')
print("features created")

conn.commit()
conn.close()
#closing database connection 


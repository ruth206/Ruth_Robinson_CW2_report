from create_connection import make_connection

conn = make_connection()
cursor = conn.cursor()



cursor.execute('''
    CREATE TABLE CW2.New_Trails (
        TrailID INT IDENTITY(1,1) PRIMARY KEY,
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
print("New_Trails table created")

cursor.execute('''
    INSERT INTO CW2.New_Trails (TrailName, TrailSummary, TrailDescription, Difficulty, Location, Length, ElevationGain, RouteType, OwnerID)
    SELECT TrailName, TrailSummary, TrailDescription, Difficulty, Location, Length, ElevationGain, RouteType, OwnerID FROM CW2.Trails
''')
print("Data copied to New_Trails table")


cursor.execute('''
    SELECT Old.TrailID AS OldTrailID, New.TrailID AS NewTrailID
    FROM CW2.Trails Old
    JOIN CW2.New_Trails New
    ON Old.TrailName = New.TrailName
''')
trail_id_mapping = cursor.fetchall()


conn.autocommit = False

try:
    
    cursor.execute('''
        ALTER TABLE CW2.TrailFeature NOCHECK CONSTRAINT FK__TrailFeat__Trail__01142BA1
    ''')
    print("Foreign key constraint on TrailFeature disabled")
    cursor.execute('''
        ALTER TABLE CW2.Trail_locationPt NOCHECK CONSTRAINT FK__Trail_loc__Trail__7D439ABD
    ''')
    print("Foreign key constraint on Trail_locationPt disabled")

    
    for mapping in trail_id_mapping:
        cursor.execute(f'''
            UPDATE CW2.TrailFeature
            SET TrailID = {mapping.NewTrailID}
            WHERE TrailID = {mapping.OldTrailID}
        ''')
        cursor.execute(f'''
            UPDATE CW2.Trail_locationPt
            SET TrailID = {mapping.NewTrailID}
            WHERE TrailID = {mapping.OldTrailID}
        ''')
    print("TrailID updated in related tables")

    
    cursor.execute('''
        EXEC sp_rename 'CW2.Trails', 'Old_Trails'
    ''')
    print("Original Trails table renamed to Old_Trails")

    
    cursor.execute('''
        EXEC sp_rename 'CW2.New_Trails', 'Trails'
    ''')
    print("New_Trails table renamed to Trails")

 
    cursor.execute('''
        ALTER TABLE CW2.TrailFeature CHECK CONSTRAINT FK__TrailFeat__Trail__01142BA1
    ''')
    print("Foreign key constraint on TrailFeature re-enabled")
    cursor.execute('''
        ALTER TABLE CW2.Trail_locationPt CHECK CONSTRAINT FK__Trail_loc__Trail__7D439ABD
    ''')
    print("Foreign key constraint on Trail_locationPt re-enabled")

   
    conn.commit()
    print("Transaction committed successfully")

except Exception as e:
    
    conn.rollback()
    print("Transaction rolled back due to error:", e)

finally:
    
    conn.close()
    print("Connection closed")

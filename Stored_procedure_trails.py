from create_connection import make_connection  # Import to make a connection to the server

conn = make_connection()
cursor = conn.cursor()

#AddTrail stored procedure
cursor.execute('''
    CREATE PROCEDURE CW2.AddTrail (
               @TrailName VARCHAR(255),
               @TrailSummary TEXT,
               @TrailDescription TEXT,
               @Difficulty VARCHAR(255),  
               @Location VARCHAR(255),
               @Length DECIMAL(10,2),
               @ElevationGain DECIMAL(10,2),
               @RouteType VARCHAR(255),
               @OwnerID INT
    )
    AS
    BEGIN
        INSERT INTO CW2.Trails (TrailName, TrailSummary, TrailDescription, Difficulty, Location, Length, ElevationGain, RouteType, OwnerID)
        VALUES (@TrailName, @TrailSummary, @TrailDescription, @Difficulty, @Location, @Length, @ElevationGain, @RouteType, @OwnerID)
    END
''')
print("AddTrail stored procedure created")

#GetTrailById stored procedure
cursor.execute('''
    CREATE PROCEDURE CW2.GetTrailById (
               @TrailID INT
    )
    AS
    BEGIN
        SELECT * FROM CW2.Trails
        WHERE TrailID = @TrailID
    END
''')
print("gettrailbyId stored procedure created")

#updateTrail stored procedure
cursor.execute('''
    CREATE PROCEDURE CW2.UpdateTrail (
               @TrailID INT,  -- Added the missing @TrailID parameter
               @TrailName VARCHAR(255),
               @TrailSummary TEXT,
               @TrailDescription TEXT,
               @Difficulty VARCHAR(255),  -- Fixed typo here
               @Location VARCHAR(255),
               @Length DECIMAL(10,2),
               @ElevationGain DECIMAL(10,2),
               @RouteType VARCHAR(255),
               @OwnerID INT
    )
    AS
    BEGIN
        UPDATE CW2.Trails
        SET TrailName = @TrailName,
            TrailSummary = @TrailSummary,
            TrailDescription = @TrailDescription,
            Difficulty = @Difficulty,
            Location = @Location,
            Length = @Length,
            ElevationGain = @ElevationGain,
            RouteType = @RouteType,
            OwnerID = @OwnerID
        WHERE TrailID = @TrailID
    END
''')
print("updatetrail stored procedure created")

#DeleteTrail stored procedure
cursor.execute('''
    CREATE PROCEDURE CW2.DeleteTrail (
               @TrailID INT
    )
    AS
    BEGIN
        DELETE FROM CW2.Trails
        WHERE TrailID = @TrailID
    END
''')
print("deletetrail stored procedure created")


conn.commit()
conn.close()

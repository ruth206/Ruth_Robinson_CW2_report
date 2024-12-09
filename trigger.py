from create_connection import make_connection  # Import to make a connection to the server

conn = make_connection()  
cursor = conn.cursor()

#triggers to automatically delete related data when a record is deleted from a table


cursor.execute('''
    CREATE TRIGGER triggerDeleteTrailLocationpt
    ON CW2.Trails
    AFTER DELETE
    AS
    BEGIN
        DELETE FROM CW2.Trail_locationPt
        WHERE TrailID IN (SELECT TrailID FROM deleted)
    END
''')
print("trigger Delete Trail LocationPt created")


cursor.execute('''
    CREATE TRIGGER triggerDeleteTrailFeature
    ON CW2.Trails
    AFTER DELETE
    AS
    BEGIN
        DELETE FROM CW2.TrailFeature
        WHERE TrailID IN (SELECT TrailID FROM deleted)
    END
''')
print("trigger Delete trail feature created")


cursor.execute('''
    CREATE TRIGGER triggerDeleteLocationPoint
    ON CW2.Trail_locationPt
    AFTER DELETE
    AS
    BEGIN
        DELETE FROM CW2.Location_point
        WHERE LocationPointID IN (SELECT LocationPointID FROM deleted)
    END
''')
print("Trigger delete location point created")


cursor.execute('''
    CREATE TRIGGER triggerDeleteFeature
    ON CW2.TrailFeature
    AFTER DELETE
    AS
    BEGIN
        DELETE FROM CW2.Feature
        WHERE FeatureID IN (SELECT FeatureID FROM deleted)
    END
''')
print("Trigger delete feature created")


conn.commit()
conn.close()

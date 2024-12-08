from create_connection import make_connection  # Import to make a connection to the server

conn = make_connection()
cursor = conn.cursor()


cursor.execute('''
    INSERT INTO CW2.Feature (FeatureID, TrailFeature)
    VALUES (?, ?)
''', (1, 'Bird Watching'))
cursor.execute('''
    INSERT INTO CW2.Feature (FeatureID, TrailFeature)
    VALUES (?, ?)
''', (2, 'Hiking'))
cursor.execute('''
    INSERT INTO CW2.Feature (FeatureID, TrailFeature)
    VALUES (?, ?)
''', (3, 'Mountain Biking'))
cursor.execute('''
    INSERT INTO CW2.Feature (FeatureID, TrailFeature)
    VALUES (?, ?)
''', (4, 'Running'))
cursor.execute('''
    INSERT INTO CW2.Feature (FeatureID, TrailFeature)
    VALUES (?, ?)
''', (5, 'Walking'))
cursor.execute('''
    INSERT INTO CW2.Feature (FeatureID, TrailFeature)
    VALUES (?, ?)
''', (6, 'Dogs on Leash'))
cursor.execute('''
    INSERT INTO CW2.Feature (FeatureID, TrailFeature)
    VALUES (?, ?)
''', (7, 'Kid-friendly'))
cursor.execute('''
    INSERT INTO CW2.Feature (FeatureID, TrailFeature)
    VALUES (?, ?)
''', (8, 'Partially Paved'))
cursor.execute('''
    INSERT INTO CW2.Feature (FeatureID, TrailFeature)
    VALUES (?, ?)
''', (9, 'Beach'))
cursor.execute('''
    INSERT INTO CW2.Feature (FeatureID, TrailFeature)
    VALUES (?, ?)
''', (10, 'Views'))
cursor.execute('''
    INSERT INTO CW2.Feature (FeatureID, TrailFeature)
    VALUES (?, ?)
''', (11, 'Wildlife'))

print("Inserted into Feature table")

cursor.execute('''
    INSERT INTO CW2.TrailFeature (TrailID, FeatureID)
    VALUES (?, ?)
''', (288, 1))
cursor.execute('''
    INSERT INTO CW2.TrailFeature (TrailID, FeatureID)
    VALUES (?, ?)
''', (288, 2))
cursor.execute('''
    INSERT INTO CW2.TrailFeature (TrailID, FeatureID)
    VALUES (?, ?)
''', (288, 3))
cursor.execute('''
    INSERT INTO CW2.TrailFeature (TrailID, FeatureID)
    VALUES (?, ?)
''', (288, 4))
cursor.execute('''
    INSERT INTO CW2.TrailFeature (TrailID, FeatureID)
    VALUES (?, ?)
''', (288, 5))
cursor.execute('''
    INSERT INTO CW2.TrailFeature (TrailID, FeatureID)
    VALUES (?, ?)
''', (288, 6))
cursor.execute('''
    INSERT INTO CW2.TrailFeature (TrailID, FeatureID)
    VALUES (?, ?)
''', (288, 7))
cursor.execute('''
    INSERT INTO CW2.TrailFeature (TrailID, FeatureID)
    VALUES (?, ?)
''', (288, 8))
cursor.execute('''
    INSERT INTO CW2.TrailFeature (TrailID, FeatureID)
    VALUES (?, ?)
''', (288, 9))
cursor.execute('''
    INSERT INTO CW2.TrailFeature (TrailID, FeatureID)
    VALUES (?, ?)
''', (288, 10))
cursor.execute('''
    INSERT INTO CW2.TrailFeature (TrailID, FeatureID)
    VALUES (?, ?)
''', (288, 11))

print("Trail features linked to TrailID 288")


cursor.execute('''
    INSERT INTO CW2.Location_point (LocationPointID, Latitude, Longitude, Description)
    VALUES (?, ?, ?, ?)
''', (1, 50.8321, -4.5390, 'Start of trail'))
cursor.execute('''
    INSERT INTO CW2.Location_point (LocationPointID, Latitude, Longitude, Description)
    VALUES (?, ?, ?, ?)
''', (2, 50.8535, -4.5050, 'Middle of the trail at 6km'))
cursor.execute('''
    INSERT INTO CW2.Location_point (LocationPointID, Latitude, Longitude, Description)
    VALUES (?, ?, ?, ?)
''', (3, 50.8705, -4.5312, 'End of trail at 10.6km'))

print("Location point test data created")


cursor.execute('''
    INSERT INTO CW2.Trail_locationPt (TrailID, LocationPointID, OrderNo)
    VALUES (?, ?, ?)
''', (288, 1, 1))
cursor.execute('''
    INSERT INTO CW2.Trail_locationPt (TrailID, LocationPointID, OrderNo)
    VALUES (?, ?, ?)
''', (288, 2, 2))
cursor.execute('''
    INSERT INTO CW2.Trail_locationPt (TrailID, LocationPointID, OrderNo)
    VALUES (?, ?, ?)
''', (288, 3, 3))

print("Location point trail test data created")


conn.commit()
conn.close()

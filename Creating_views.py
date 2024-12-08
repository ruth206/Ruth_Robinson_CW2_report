from create_connection import make_connection  # Import to make a connection to the server

conn = make_connection()  
cursor = conn.cursor()

#dropping views to recreate them
cursor.execute('DROP VIEW IF EXISTS Feature_View')
cursor.execute('DROP VIEW IF EXISTS TrailFeature_View')
cursor.execute('DROP VIEW IF EXISTS LocationPoint_View')
cursor.execute('DROP VIEW IF EXISTS TrailLocationPoint_View')
cursor.execute('DROP VIEW IF EXISTS Trail_View')


#creating views

cursor.execute('''CREATE VIEW Feature_View AS
    SELECT * FROM CW2.Feature
''')
print("Feature view created")

cursor.execute('''CREATE VIEW TrailFeature_View AS
    SELECT * FROM CW2.TrailFeature
''')
print("TrailFeature view created")

cursor.execute('''CREATE VIEW LocationPoint_View AS
    SELECT * FROM CW2.Location_point
''')
print("LocationPoint view created")

cursor.execute('''CREATE VIEW TrailLocationPoint_View AS
    SELECT * FROM CW2.Trail_locationPt
''')
print("TrailLocationPoint view created")

cursor.execute('''CREATE VIEW Trail_View AS
    SELECT * FROM CW2.Trails
''')
print("Trail view created")


#querying all the views to check they have all been poulated properly

cursor.execute('SELECT * FROM Feature_View')
print("Feature View Data:", cursor.fetchall())

cursor.execute('SELECT * FROM TrailFeature_View')
print("TrailFeature View Data:", cursor.fetchall())

cursor.execute('SELECT * FROM LocationPoint_View')
print("LocationPoint View Data:", cursor.fetchall())

cursor.execute('SELECT * FROM TrailLocationPoint_View')
print("TrailLocationPoint View Data:", cursor.fetchall())

cursor.execute('SELECT * FROM Trail_View')
print("Trail View Data:", cursor.fetchall())

conn.close()






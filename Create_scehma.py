from create_connection import make_connection

conn = make_connection()
cursor = conn.cursor()

cursor.execute("CREATE SCHEMA CW2")
conn.commit()
print("CW2 was created successfully")

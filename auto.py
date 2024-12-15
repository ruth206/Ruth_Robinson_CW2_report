from create_connection import make_connection  #Import to make a connection to the server

def recreate_users_table():
    conn = make_connection()
    cursor = conn.cursor()
    
    
    cursor.execute('''
        CREATE TABLE CW2.New_Users (
            UserID INT IDENTITY(1,1) PRIMARY KEY,
            EmailAddress VARCHAR(255) NOT NULL,
            Username VARCHAR(255) UNIQUE NOT NULL,
            Password VARCHAR(255) NOT NULL,
            Role VARCHAR(50) NOT NULL
        );
    ''')
    print("New_Users table created")

   
    cursor.execute('''
        INSERT INTO CW2.New_Users (EmailAddress, Username, Password, Role)
        SELECT EmailAddress, Username, Password, Role FROM CW2.Users
    ''')
    print("Data copied to New_Users table")

   
    cursor.execute('''
        SELECT Old.UserID AS OldUserID, New.UserID AS NewUserID
        FROM CW2.Users Old
        JOIN CW2.New_Users New
        ON Old.EmailAddress = New.EmailAddress
    ''')
    user_id_mapping = cursor.fetchall()

    conn.autocommit = False

    try:
        
        cursor.execute('''
            ALTER TABLE CW2.Trails NOCHECK CONSTRAINT ALL
        ''')
        cursor.execute('''
            ALTER TABLE CW2.Trail_locationPt NOCHECK CONSTRAINT ALL
        ''')
        cursor.execute('''
            ALTER TABLE CW2.TrailFeature NOCHECK CONSTRAINT ALL
        ''')
        print("Foreign key constraints on related tables disabled")
        
        
        for mapping in user_id_mapping:
            cursor.execute(f'''
                UPDATE CW2.Trails
                SET OwnerID = {mapping.NewUserID}
                WHERE OwnerID = {mapping.OldUserID}
            ''')
        print("OwnerID updated in Trails table")

        
        cursor.execute('''
            EXEC sp_rename 'CW2.Users', 'Old_Users'
        ''')
        print("Original Users table renamed to Old_Users")

        
        cursor.execute('''
            EXEC sp_rename 'CW2.New_Users', 'Users'
        ''')
        print("New_Users table renamed to Users")

       
        cursor.execute('''
            ALTER TABLE CW2.Trails CHECK CONSTRAINT ALL
        ''')
        cursor.execute('''
            ALTER TABLE CW2.Trail_locationPt CHECK CONSTRAINT ALL
        ''')
        cursor.execute('''
            ALTER TABLE CW2.TrailFeature CHECK CONSTRAINT ALL
        ''')
        print("Foreign key constraints on related tables re-enabled")

        conn.commit()
        print("Transaction committed successfully")

    except Exception as e:
        conn.rollback()
        print("Transaction rolled back due to error:", e)

    finally:
        conn.close()
        print("Connection closed")


recreate_users_table()

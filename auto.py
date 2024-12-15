from create_connection import make_connection  # Import to make a connection to the server

def recreate_users_table():
    conn = make_connection()
    cursor = conn.cursor()
    
    # Step 1: Create New_Users table with UserID as an auto-incrementing primary key
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

    # Step 2: Copy data from Users to New_Users
    cursor.execute('''
        INSERT INTO CW2.New_Users (EmailAddress, Username, Password, Role)
        SELECT EmailAddress, Username, Password, Role FROM CW2.Users
    ''')
    print("Data copied to New_Users table")

    # Step 3: Fetch UserID mappings
    cursor.execute('''
        SELECT Old.UserID AS OldUserID, New.UserID AS NewUserID
        FROM CW2.Users Old
        JOIN CW2.New_Users New
        ON Old.EmailAddress = New.EmailAddress
    ''')
    user_id_mapping = cursor.fetchall()

    conn.autocommit = False

    try:
        # Step 4: Disable foreign key constraints on related tables
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
        
        # Step 5: Update references in related tables
        for mapping in user_id_mapping:
            cursor.execute(f'''
                UPDATE CW2.Trails
                SET OwnerID = {mapping.NewUserID}
                WHERE OwnerID = {mapping.OldUserID}
            ''')
        print("OwnerID updated in Trails table")

        # Step 6: Rename original Users table
        cursor.execute('''
            EXEC sp_rename 'CW2.Users', 'Old_Users'
        ''')
        print("Original Users table renamed to Old_Users")

        # Step 7: Rename New_Users table to Users
        cursor.execute('''
            EXEC sp_rename 'CW2.New_Users', 'Users'
        ''')
        print("New_Users table renamed to Users")

        # Step 8: Re-enable foreign key constraints on related tables
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

# Run the drop and recreate function
recreate_users_table()

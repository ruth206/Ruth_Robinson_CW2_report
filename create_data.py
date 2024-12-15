from create_connection import make_connection  # Import to make a connection to the server

def drop_foreign_keys_and_users_table():
    conn = make_connection()
    cursor = conn.cursor()
    
    # Find and drop foreign key constraints referencing the Users table
    cursor.execute('''
        DECLARE @sql NVARCHAR(MAX) = N'';
        SELECT @sql += 'ALTER TABLE ' + QUOTENAME(rc.TABLE_SCHEMA) + '.' + QUOTENAME(rc.TABLE_NAME) 
                     + ' DROP CONSTRAINT ' + QUOTENAME(rc.CONSTRAINT_NAME) + ';'
        FROM INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS rc
        JOIN INFORMATION_SCHEMA.TABLE_CONSTRAINTS tc 
        ON rc.CONSTRAINT_NAME = tc.CONSTRAINT_NAME
        WHERE tc.TABLE_NAME = 'Users';
        EXEC sp_executesql @sql;
    ''')
    
    # Drop the Users table
    cursor.execute('''
        IF OBJECT_ID('CW2.Users', 'U') IS NOT NULL
        DROP TABLE CW2.Users;
    ''')
    
    # Create the Users table with UserID as an auto-incrementing primary key
    cursor.execute('''
        CREATE TABLE CW2.Users (
            UserID INT IDENTITY(1,1) PRIMARY KEY,
            EmailAddress VARCHAR(255) NOT NULL,
            Username VARCHAR(255) NOT NULL,
            Password VARCHAR(255) NOT NULL,
            Role VARCHAR(50) NOT NULL
        );
    ''')
    print("Users table created successfully")
    
    # Recreate the stored procedures
    cursor.execute('''
        CREATE PROCEDURE CW2.AddUser (
            @EmailAddress VARCHAR(255),
            @Username VARCHAR(255),
            @PasswordHash VARCHAR(255),
            @Role VARCHAR(50)
        )
        AS
        BEGIN
            INSERT INTO CW2.Users (EmailAddress, Username, Password, Role)
            VALUES (@EmailAddress, @Username, @PasswordHash, @Role);
        END;
    ''')
    print("AddUser procedure created successfully")
    
    cursor.execute('''
        CREATE PROCEDURE CW2.GetUserById (
            @UserId INT
        )
        AS
        BEGIN
            SELECT * FROM CW2.Users
            WHERE UserId = @UserId;
        END;
    ''')
    print("GetUserById procedure created successfully")
    
    cursor.execute('''
        CREATE PROCEDURE CW2.UpdateUser (
            @UserId INT,
            @EmailAddress VARCHAR(255),
            @Username VARCHAR(255),
            @PasswordHash VARCHAR(255),
            @Role VARCHAR(50)
        )
        AS
        BEGIN
            UPDATE CW2.Users
            SET EmailAddress = @EmailAddress,
                Username = @Username,
                Password = @PasswordHash,
                Role = @Role
            WHERE UserId = @UserId;
        END;
    ''')
    print("UpdateUser procedure created successfully")
    
    cursor.execute('''
        CREATE PROCEDURE CW2.DeleteUser (
            @UserId INT
        )
        AS
        BEGIN
            DELETE FROM CW2.Users
            WHERE UserId = @UserId;
        END;
    ''')
    print("DeleteUser procedure created successfully")
    
    conn.commit()
    cursor.close()
    conn.close()

# Run the drop and recreate function
drop_foreign_keys_and_users_table()

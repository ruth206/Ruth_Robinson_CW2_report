import bcrypt
from create_connection import make_connection  # Import to make a connection to the server

conn = make_connection()
cursor = conn.cursor()

#AddUser stored procedure
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
print("adduser created successfully")

#GetUserById stored procedure
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
print("getuserbyidcreated successfully")

#UpdateUser stored procedure
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
print("updateuser created successfully")

#deleteUser stored procedure
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
print("deleteuser created successfully")

conn.commit()


password = 'insecurePassword'
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')  # Hash the password with a generated salt and decode it to a string 

cursor.execute('''
    EXEC CW2.AddUser
        @EmailAddress = ?,
        @Username = ?,
        @PasswordHash = ?,
        @Role = ?
''', ('ada@plymouth.ac.uk', 'Ada Lovelace', hashed, 'Admin'))

conn.commit()

cursor.execute('''
    SELECT * FROM CW2.Users
    WHERE EmailAddress = 'ada@plymouth.ac.uk';
''')
user = cursor.fetchone()  #testing to see if user has been added 
print("Inserted User:", user)  

cursor.close()
conn.close()




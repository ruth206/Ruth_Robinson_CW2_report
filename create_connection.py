import pyodbc

def make_connection():
    server = 'dist-6-505.uopnet.plymouth.ac.uk'
    database = 'COMP2001_RRobinson'
    username = 'RRobinson'
    password = 'GjyI491+'
    driver = '{ODBC Driver 17 for SQL Server}'

    conn_str = (
        f'DRIVER={driver};'
        f'SERVER={server};'
        f'DATABASE={database};'
        f'UID={username};'
        f'PWD={password};'
        'Encrypt=Yes;'
        'TrustServerCertificate=Yes;'
        'Connection Timeout=30;'
        'Trusted_Connection=No'
    )

    conn = pyodbc.connect(conn_str)
    return conn

import sqlite3

def create_database():
    # Connect to the SQLite database (it will be created if it doesn't exist)
    conn = sqlite3.connect('iphwr_analysis.db')
    cursor = conn.cursor()

    # Drop the properties table if it exists
    cursor.execute('''DROP TABLE IF EXISTS properties;''')

    # Create the properties table with additional fields
    cursor.execute(''' 
    CREATE TABLE properties (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        channel_id TEXT,
        property_name TEXT,
        database_type TEXT,
        reactor_type TEXT,
        reactor_name TEXT,
        Year TEXT,
        HOY TEXT,
        Length TEXT,
        Entry_by TEXT,
        Entry_Date TEXT,
        Remark TEXT,
        Cell1 TEXT,
        Cell2 TEXT,
        Cell3 TEXT,
        Cell4 TEXT,
        Cell5 TEXT,
        Cell6 TEXT,
        Cell7 TEXT,
        Cell8 TEXT,
        Cell9 TEXT,
        Cell10 TEXT,
        Cell11 TEXT,
        Cell12 TEXT,
        Cell13 TEXT,
        Cell14 TEXT,
        Cell15 TEXT,
        Cell16 TEXT,
        Cell17 TEXT,
        Cell18 TEXT,
        Cell19 TEXT,
        Cell20 TEXT,
        Cell21 TEXT,
        Cell22 TEXT,
        Cell23 TEXT,
        Cell24 TEXT
    );
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    print("Database and table created successfully!")

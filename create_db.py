import sqlite3

def create_database():
    """Create the SQLite database and properties table."""
    conn = sqlite3.connect('iphwr_analysis.db')
    cursor = conn.cursor()

    # Drop the properties table if it exists
    #cursor.execute('''DROP TABLE IF EXISTS properties;''')

    # Create the properties table with the necessary fields
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
        {fields}
    );
    '''.format(fields=', '.join(f'Cell{i} TEXT, Position{i} TEXT' for i in range(1, 101))))
    
    # Commit changes and close the connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    print("Database and table created successfully!")

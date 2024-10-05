import sqlite3

def display_table(database_type, channel):
    """Fetch and display table content from the SQLite database."""
    # Connect to the database
    conn = sqlite3.connect('iphwr_analysis.db')
    cursor = conn.cursor()

    # Define the columns for the table (you can modify or include all required columns)
    headers = [
        'Channel ID', 'Property Name', 'Year', 'HOY', 'Length', 'Entry By', 'Entry Date', 'Remark',
        'Cell1', 'Cell2', 'Cell3', 'Cell4', 'Cell5', 'Cell6', 'Cell7', 'Cell8', 'Cell9', 'Cell10',
        'Cell11', 'Cell12', 'Cell13', 'Cell14', 'Cell15', 'Cell16', 'Cell17', 'Cell18', 'Cell19',
        'Cell20', 'Cell21', 'Cell22', 'Cell23', 'Cell24'
    ]

    # Fetch the data for the specified channel and database type
    cursor.execute("SELECT channel_id, property_name, Year, HOY, Length, Entry_by, Entry_Date, Remark, Cell1, Cell2, Cell3, Cell4, Cell5, Cell6, Cell7, Cell8, Cell9, Cell10,Cell11, Cell12, Cell13, Cell14, Cell15, Cell16, Cell17, Cell18, Cell19, Cell20, Cell21, Cell22, Cell23, Cell24 FROM properties where channel_id='"+channel+"'")
    
    rows = cursor.fetchall()

    if not rows:
        print(f"No data found for Channel: {channel} and Database Type: {database_type}")
        return

    # Display the headers
    print(f"\nData for Channel: {channel} and Database Type: {database_type}\n")
    print("{:<12} {:<15} {:<5} {:<5} {:<7} {:<10} {:<12} {:<15} ".format(*headers[:8]), end="")
    for i in range(1, 25):
        print(f"Cell{i:<5}", end=" ")
    print("\n" + "-" * 200)

    # Display each row of data
    for row in rows:
        # Print the first few columns
        print("{:<12} {:<15} {:<5} {:<5} {:<7} {:<10} {:<12} {:<15} ".format(*row[:8]), end="")
        # Print the cell data
        for cell in row[8:]:
            print(f"{str(cell):<7}", end=" ")
        print()

    # Close the database connection
    conn.close()


if __name__ == "__main__":
    # Example usage
    database_type = "Type A"  # Set your database type
    channel = "Example_Channel"             # Set your channel

    display_table(database_type, channel)

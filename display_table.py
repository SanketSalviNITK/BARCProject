import sqlite3

def display_table(database_type, channel):
    """Fetch and display table content from the SQLite database."""
    # Connect to the database
    conn = sqlite3.connect('iphwr_analysis.db')
    cursor = conn.cursor()

    # Define the headers for the table including position columns
    headers = [
        'Channel ID', 'Property Name', 'Year', 'HOY', 'Length', 'Entry By', 'Entry Date', 'Remark',
        'Cell1', 'Cell1 Position', 'Cell2', 'Cell2 Position', 'Cell3', 'Cell3 Position', 
        'Cell4', 'Cell4 Position', 'Cell5', 'Cell5 Position', 'Cell6', 'Cell6 Position', 
        'Cell7', 'Cell7 Position', 'Cell8', 'Cell8 Position', 'Cell9', 'Cell9 Position', 
        'Cell10', 'Cell10 Position', 'Cell11', 'Cell11 Position', 'Cell12', 'Cell12 Position', 
        'Cell13', 'Cell13 Position', 'Cell14', 'Cell14 Position', 'Cell15', 'Cell15 Position', 
        'Cell16', 'Cell16 Position', 'Cell17', 'Cell17 Position', 'Cell18', 'Cell18 Position', 
        'Cell19', 'Cell19 Position', 'Cell20', 'Cell20 Position', 'Cell21', 'Cell21 Position', 
        'Cell22', 'Cell22 Position', 'Cell23', 'Cell23 Position', 'Cell24', 'Cell24 Position'
    ]

    # Fetch the data for the specified channel and database type
    cursor.execute("""
        SELECT 
            channel_id, property_name, Year, HOY, Length, Entry_by, Entry_Date, Remark, 
            Cell1, Cell1_position, Cell2, Cell2_position, Cell3, Cell3_position, 
            Cell4, Cell4_position, Cell5, Cell5_position, Cell6, Cell6_position, 
            Cell7, Cell7_position, Cell8, Cell8_position, Cell9, Cell9_position, 
            Cell10, Cell10_position, Cell11, Cell11_position, Cell12, Cell12_position, 
            Cell13, Cell13_position, Cell14, Cell14_position, Cell15, Cell15_position, 
            Cell16, Cell16_position, Cell17, Cell17_position, Cell18, Cell18_position, 
            Cell19, Cell19_position, Cell20, Cell20_position, Cell21, Cell21_position, 
            Cell22, Cell22_position, Cell23, Cell23_position, Cell24, Cell24_position 
        FROM properties 
        WHERE channel_id = ? AND database_type = ?
    """, (channel, database_type))
    
    rows = cursor.fetchall()

    if not rows:
        print(f"No data found for Channel: {channel} and Database Type: {database_type}")
        return

    # Display the headers
    print(f"\nData for Channel: {channel} and Database Type: {database_type}\n")
    header_format = "{:<12} {:<15} {:<5} {:<5} {:<7} {:<10} {:<12} {:<15} "
    print(header_format.format(*headers[:8]), end="")
    for i in range(1, 25):
        print(f"Cell{i:<15} {'Position':<15}", end=" ")
    print("\n" + "-" * 280)

    # Display each row of data
    for row in rows:
        # Print the first few columns
        print(header_format.format(*row[:8]), end="")
        # Print the cell data and their corresponding positions
        for i in range(8, len(row), 2):  # Start from 8th column (Cell1)
            print(f"{str(row[i]):<15} {str(row[i + 1]):<15}", end=" ")  # Cell and Position
        print()

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    # Example usage
    database_type = "Type A"  # Set your database type
    channel = "A08"            # Set your channel

    display_table(database_type, channel)

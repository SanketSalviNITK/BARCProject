import sqlite3
import random
from datetime import datetime

def insert_random_data(table_name, thickness_column_suffix):
    connection = sqlite3.connect('reactor_data.db')
    cursor = connection.cursor()

    # Define the number of cells (e.g., 100 cells for Position and min_thickness)
    num_cells = 100

    # Generate random values for other fields
    random_channel_id = "A08"
    random_property_name = "Tube Dimensions"
    random_database_type = "Mechanical"
    random_reactor_type = "220_IPHWR"
    random_reactor_name = "RAPS"
    random_year = "2024"
    random_hoy = "HOY Value"
    random_length = "100m"
    random_entry_by = "XYZ"
    random_entry_date = datetime.now().strftime('%Y-%m-%d')
    random_remark = "Sample Remark"

    # Generate random values for each cell's position and min thickness
    random_cell_positions = [random.uniform(0, 5000) for _ in range(num_cells)]
    random_cell_thicknesses = [random.uniform(1, 10) for _ in range(num_cells)]

    # Combine all values into a single data tuple
    data = (
        random_channel_id, random_property_name, random_database_type, random_reactor_type,
        random_reactor_name, random_year, random_hoy, random_length, random_entry_by,
        random_entry_date, random_remark,
        *random_cell_positions,
        *random_cell_thicknesses
    )

    # Prepare the SQL insert statement with 211 placeholders
    placeholders = ', '.join(['?'] * 211)
    insert_sql = f"INSERT INTO {table_name} VALUES (NULL, {placeholders})"  # NULL for auto-increment ID

    cursor.execute(insert_sql, data)
    connection.commit()
    connection.close()

# Insert data into each table
insert_random_data("reactor_data_min_thickness", "min_thickness")
insert_random_data("reactor_data_max_thickness", "max_thickness")
insert_random_data("reactor_data_min_inner_diameter", "min_inner_diameter")
insert_random_data("reactor_data_max_inner_diameter", "max_inner_diameter")
insert_random_data("reactor_data_avg_outside_diameter", "avg_outside_diameter")

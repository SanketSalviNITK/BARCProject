import sqlite3

# Connect to the SQLite database (creates one if not exists)
conn = sqlite3.connect('reactor_data.db')
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS reactor_data_min_thickness")
cursor.execute("DROP TABLE IF EXISTS reactor_data_max_thickness")
cursor.execute("DROP TABLE IF EXISTS reactor_data_min_inner_diameter")
cursor.execute("DROP TABLE IF EXISTS reactor_data_max_inner_diameter")
cursor.execute("DROP TABLE IF EXISTS reactor_data_avg_outside_diameter")
cursor.execute("DROP TABLE IF EXISTS Tube_Mechanical_Properties")
cursor.execute("DROP TABLE IF EXISTS Tube_Chemical_Composition")
cursor.execute("DROP TABLE IF EXISTS Tube_Ingot_Details")
cursor.execute("DROP TABLE IF EXISTS Tube_Installation")

# Function to create tables with specific columns for each measurement type
def create_tube_dimensions_table(table_name, thickness_type):
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
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
    """
    
    # Add columns for each cell up to Cell 100 with Position and specified thickness/diameter type
    for i in range(1, 101):
        create_table_sql += f"    Cell{i}_Position_mm REAL,\n"
        create_table_sql += f"    Cell{i}_{thickness_type}_mm REAL,\n"

    # Remove the last comma and close the SQL statement
    create_table_sql = create_table_sql.rstrip(",\n") + "\n);"
    
    # Execute the create table command
    cursor.execute(create_table_sql)
    print(f"Table '{table_name}' created successfully.")

# Create tables with the specified thickness/diameter type
create_tube_dimensions_table("reactor_data_min_thickness", "Min_Thickness")
create_tube_dimensions_table("reactor_data_max_thickness", "Max_Thickness")
create_tube_dimensions_table("reactor_data_min_inner_diameter", "Min_Inner_Diameter")
create_tube_dimensions_table("reactor_data_max_inner_diameter", "Max_Inner_Diameter")
create_tube_dimensions_table("reactor_data_avg_outside_diameter", "Avg_Outside_Diameter")

# Commit the transaction and close the connection
#conn.commit()
#conn.close()

print("All tube dimension tables created successfully.")

def create_tube_mechanical_properties_table():
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS Tube_Mechanical_Properties (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        channel_id TEXT,
        property_name TEXT,
        database_type TEXT,
        reactor_type TEXT,
        reactor_name TEXT,
        entered_by TEXT,
        remark TEXT,
        uts_rt_ksi REAL,
        ys_rt_ksi REAL,
        elong_rt_percent REAL,
        ht_test_temp_deg_c REAL,
        uts_300_ht_ksi REAL,
        ys_300_ht_ksi REAL,
        elong_300_ht_percent REAL,
        hardness_ne_hrc REAL,
        hardness_oe_hrc REAL,
        corrosion_limits_mg_dm2 REAL,
        cold_work_percent REAL,
    """
    
    # Adding columns for each cell up to Cell100
    for i in range(1, 101):
        create_table_sql += f"    Cell{i} REAL,\n"

    # Remove the last comma and close the SQL statement
    create_table_sql = create_table_sql.rstrip(",\n") + "\n);"
    
    # Execute the create table command
    cursor.execute(create_table_sql)
    print("Table 'Tube_Mechanical_Properties' created successfully.")

# Create the table
create_tube_mechanical_properties_table()

# Commit the transaction and close the connection
#conn.commit()
#conn.close()


def create_chemical_composition_table():
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS Tube_Chemical_Composition (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        channel_id TEXT,
        property_name TEXT,
        database_type TEXT,
        reactor_type TEXT,
        reactor_name TEXT,
        entered_by TEXT,
        remark TEXT,
        niobium_nb_ppm REAL,
        oxygen_o_ppm REAL,
        iron_fe_ppm REAL,
        carbon_c_ppm REAL,
        nitrogen_n_ppm REAL,
        hydrogen_h_ppm REAL
    );
    """
    
    # Execute the create table command
    cursor.execute(create_table_sql)
    print("Table 'Tube_Chemical_Composition' created successfully.")

# Create the Tube_Chemical_Composition table
create_chemical_composition_table()

# Commit the transaction and close the connection
#conn.commit()
#conn.close()

# Function to create a table for Tube Ingot Details with for loop for repetitive columns
def create_ingot_details_table():
    # Start the SQL command for creating the table
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS Tube_Ingot_Details (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        channel_id TEXT,
        property_name TEXT,
        database_type TEXT,
        reactor_type TEXT,
        reactor_name TEXT,
        entered_by TEXT,
        remark TEXT,
        manuf_route TEXT,
        origin TEXT,
        ingot_no TEXT,
        entry_type TEXT,
    """
    
    # List of elements with repetitive ppm measurements
    elements = ["niobium_nb", "oxygen_o", "iron_fe", "carbon_c", "hydrogen_h", "nitrogen_n", "phosphorus_p", "tin_sn", "aluminium_al", "chlorine_cl"]
    
    # Generate columns for each element with -1 to -4 suffix
    for element in elements:
        for i in range(1, 5):
            create_table_sql += f"{element}_ppm_{i} REAL,\n"
    
    # Generate columns for Cell41 to Cell100
    for i in range(41, 101):
        create_table_sql += f"cell_{i} REAL,\n"
    
    # Remove the last comma and newline, then close the table creation statement
    create_table_sql = create_table_sql.rstrip(",\n") + "\n);"
    
    # Execute the create table command
    cursor.execute(create_table_sql)
    print("Table 'Tube_Ingot_Details' created successfully.")

# Create the Tube_Ingot_Details table
create_ingot_details_table()

# Commit the transaction and close the connection
#conn.commit()
#conn.close()

# Function to create the Tube_Installation table with repetitive column names
def create_installation_table():
    # Start the SQL command for creating the table
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS Tube_Installation (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        channel_id TEXT,
        property_name TEXT,
        database_type TEXT,
        reactor_type TEXT,
        reactor_name TEXT,
        entered_by TEXT,
        remark TEXT,
        coolant_tube_no TEXT,
        hq_ncr_no TEXT,
        imp_hq_ncr_comments TEXT,
        trimming_length_south REAL,
        trimming_length_north REAL,
        two_t_south REAL,
        od_coolant_tube_rolling_area_s REAL,
        ef_no_s TEXT,
        ef_dcr_s TEXT,
        b1_dia_s REAL,
        inter_clear_south REAL,
        gray_lock_orientation_s TEXT,
        roller_reach_s REAL,
        lt_pt_gap_br_s REAL,
        lt_pt_gap_ar_s REAL,
        exp_set_dia_required_s REAL,
        exp_set_dia_actual_s REAL,
        spring_back_s REAL,
        rolled_id_s REAL,
        percent_wall_red_s REAL,
        helium_leak_rate_s REAL,
        two_t_north REAL,
        od_coolant_tube_rolling_area_n REAL,
        ef_no_n TEXT,
        ef_dcr_n TEXT,
        b1_dia_n REAL,
        inter_clear_north REAL,
        gray_lock_orientation_n TEXT,
        expander_reach_n REAL,
        lt_pt_gap_br_n REAL,
        lt_pt_gap_ar_n REAL,
        exp_set_dia_required_n REAL,
        exp_set_dia_actual_n REAL,
        spring_back_n REAL,
        rolled_id_n REAL,
        percent_wall_red_n REAL,
        helium_leak_rate_n REAL,
    """

    # Adding GS position and coil diameter columns dynamically
    for i in range(1, 5):
        create_table_sql += f"gs_{i}_position REAL,\n"
        create_table_sql += f"gs_{i}_coil_diameter REAL,\n"

    # Add PT trimmed length and other observation columns
    create_table_sql += """
        pt_trimmed_length_south REAL,
        pt_trimmed_length_north REAL,
        visual_observation_od_nfc_report TEXT,
        boroscopic_inspection_observation TEXT,
        observations_duration_videography_rolled_area_s TEXT,
        observations_duration_videography_rolled_area_n TEXT,
        site_installation_ncr_dcr TEXT,
    """

    # Adding Cell50 to Cell100 dynamically
    for i in range(50, 101):
        create_table_sql += f"cell_{i} REAL,\n"

    # Remove the last comma and newline, then close the table creation statement
    create_table_sql = create_table_sql.rstrip(",\n") + "\n);"
    
    # Execute the create table command
    cursor.execute(create_table_sql)
    print("Table 'Tube_Installation' created successfully.")

# Create the Tube_Installation table
create_installation_table()

# Start of the SQL command to create the table
create_table_sql = """
CREATE TABLE IF NOT EXISTS ISI_PSI_Avg_Diameter (
    channel_id TEXT,
    property_name TEXT,
    database_type TEXT,
    reactor_type TEXT,
    reactor_name TEXT,
    HOY INTEGER,
    FPY INTEGER,
    Entered_By TEXT,
    Year INTEGER,
    Remark TEXT,
"""

# Add cell columns (Position and Diameter for each cell)
for i in range(1, 101):
    create_table_sql += f"    Cell{i}_Position_mm REAL,\n"
    create_table_sql += f"    Cell{i}_Diameter_mm REAL,\n"

# Remove the last comma and newline, then close the SQL command
create_table_sql = create_table_sql.rstrip(",\n") + "\n);"

# Execute the SQL command to create the table
cursor.execute(create_table_sql)

print("ISI_PSI_Avg_Diameter table created successfully.")

# Start of the SQL command to create the table
create_table_sql = """
CREATE TABLE IF NOT EXISTS ISI_PT_Centerline_SAG (
    channel_id TEXT,
    property_name TEXT,
    database_type TEXT,
    reactor_type TEXT,
    reactor_name TEXT,
    HOY INTEGER,
    FPY INTEGER,
    Entered_By TEXT,
    Year INTEGER,
    Remark TEXT,
"""

# Add cell columns (Position and Sag for each cell)
for i in range(1, 101):
    create_table_sql += f"    Cell{i}_Position_mm REAL,\n"
    create_table_sql += f"    Cell{i}_Sag_mm REAL,\n"

# Remove the last comma and newline, then close the SQL command
create_table_sql = create_table_sql.rstrip(",\n") + "\n);"

# Execute the SQL command to create the table
cursor.execute(create_table_sql)
print("ISI_PT_Centerline_SAG table created successfully.")


create_table_sql = """
CREATE TABLE IF NOT EXISTS ISI_Thickness (
    channel_id TEXT,
    property_name TEXT,
    database_type TEXT,
    reactor_type TEXT,
    reactor_name TEXT,
    HOY INTEGER,
    FPY INTEGER,
    Entered_By TEXT,
    Year INTEGER,
    Remark TEXT,
"""

# Add cell columns (Position and Sag for each cell)
for i in range(1, 101):
    create_table_sql += f"    Cell{i}_Position_mm REAL,\n"
    create_table_sql += f"    Cell{i}_Thickness_mm REAL,\n"

# Remove the last comma and newline, then close the SQL command
create_table_sql = create_table_sql.rstrip(",\n") + "\n);"

# Execute the SQL command to create the table
cursor.execute(create_table_sql)

print("ISI_Thickness table created successfully.")

create_table_sql = """
CREATE TABLE IF NOT EXISTS ISI_Channel_Length (
    channel_id TEXT,
    property_name TEXT,
    database_type TEXT,
    reactor_type TEXT,
    reactor_name TEXT,
    HOY INTEGER,
    FPY INTEGER,
    Entered_By TEXT,
    Year INTEGER,
    Remark TEXT,
"""

# Add cell columns (Position and Sag for each cell)
for i in range(1, 101):
    create_table_sql += f"    Cell{i}_Length_mm REAL,\n"

# Remove the last comma and newline, then close the SQL command
create_table_sql = create_table_sql.rstrip(",\n") + "\n);"

# Execute the SQL command to create the table
cursor.execute(create_table_sql)

print("ISI_Channel_Length table created successfully.")


create_table_sql = """
CREATE TABLE IF NOT EXISTS ISI_Inspection_Log (
    channel_id TEXT,
    property_name TEXT,
    database_type TEXT,
    reactor_type TEXT,
    reactor_name TEXT,
    HOY INTEGER,
    FPY INTEGER,
    Entered_By TEXT,
    Year INTEGER,
    Remark TEXT,
    UT_inspection_report BLOB,
    Sliver_status TEXT,
    Sliver_location TEXT,
    

"""

for i in range(1, 101):
    create_table_sql += f"    Cell{i} REAL,\n"

# Remove the last comma and newline, then close the SQL command
create_table_sql = create_table_sql.rstrip(",\n") + "\n);"

# Execute the SQL command to create the table
cursor.execute(create_table_sql)

print("ISI_Inspection_Log table created successfully.")




create_table_sql = """
CREATE TABLE IF NOT EXISTS ISI_GS_Position (
    channel_id TEXT,
    property_name TEXT,
    database_type TEXT,
    reactor_type TEXT,
    reactor_name TEXT,
    HOY INTEGER,
    FPY INTEGER,
    Entered_By TEXT,
    Year INTEGER,
    Remark TEXT,
"""

for i in range(1, 101):
    create_table_sql += f"    Cell{i} REAL,\n"

# Remove the last comma and newline, then close the SQL command
create_table_sql = create_table_sql.rstrip(",\n") + "\n);"

# Execute the SQL command to create the table
cursor.execute(create_table_sql)

conn.commit()
conn.close()
print("ISI_GS_Position table created successfully.")

print("All table created successfully in the reactor_data.db database.")
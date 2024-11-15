import sqlite3
import random
from datetime import datetime

# Connect to the SQLite database
conn = sqlite3.connect('reactor_data.db')
cursor = conn.cursor()

# Fixed values for insertion
random_channel_id = "A08"
random_property_name = "Tube Dimensions"
random_database_type = "Mechanical"
random_reactor_type = "220_IPHWR"
random_reactor_name = "RAPS"
random_year = "2024"
random_hoy = "3.2"
random_fpy ="4.5"
random_length = "100m"
random_entry_by = "XYZ"
random_entry_date = datetime.now().strftime('%Y-%m-%d')
random_remark = "Sample Remark"
props=['min_thickness', 'max_thickness', 'min_inner_diameter', 'max_inner_diameter', 'avg_outside_diameter']
# Function to insert random values into reactor data tables (min, max thickness, etc.)
def insert_random_values_into_reactor_data_tables():
    for i in range(5):  # We have 5 tables for reactor data (Min_Thickness, Max_Thickness, etc.)
        table_name = f"reactor_data_"+props[i]
        
        for j in range(1, 101):  # For 100 cells
            # Generate random position and random value for thickness/diameter
            random_position = random.uniform(1, 1000)  # Random position in mm
            random_value = random.uniform(10, 50)  # Random value for thickness/diameter in mm
            
            # Construct the SQL insert query dynamically based on table structure
            cell_column_name = f"Cell{j}_"+props[i]+"_mm"  # Cell{j}_min_mm, Cell{j}_max_mm, etc.
            insert_sql = f"""
            INSERT INTO {table_name} (
                channel_id, property_name, database_type, reactor_type, reactor_name,
                Year, HOY, Length, Entry_by, Entry_Date, Remark, 
                {cell_column_name}
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            );
            """
            cursor.execute(insert_sql, (
                random_channel_id, random_property_name, random_database_type,
                random_reactor_type, random_reactor_name, random_year, random_hoy,
                random_length, random_entry_by, random_entry_date, random_remark,
                random_value
            ))
        print(f"Random data inserted into {table_name}.")

# Insert data into Tube_Mechanical_Properties table
def insert_into_mechanical_properties():
    for i in range(1, 101):  # For 100 cells
        random_uts_rt_ksi = random.uniform(10, 100)
        random_ys_rt_ksi = random.uniform(10, 100)
        random_elong_rt_percent = random.uniform(1, 10)
        random_ht_test_temp_deg_c = random.uniform(20, 200)
        random_uts_300_ht_ksi = random.uniform(10, 100)
        random_ys_300_ht_ksi = random.uniform(10, 100)
        random_elong_300_ht_percent = random.uniform(1, 10)
        random_hardness_ne_hrc = random.uniform(10, 50)
        random_hardness_oe_hrc = random.uniform(10, 50)
        random_corrosion_limits_mg_dm2 = random.uniform(1, 20)
        random_cold_work_percent = random.uniform(1, 10)
        
        # Insert into the table
        insert_sql = f"""
        INSERT INTO Tube_Mechanical_Properties (
            channel_id, property_name, database_type, reactor_type, reactor_name, 
            entered_by, remark, uts_rt_ksi, ys_rt_ksi, elong_rt_percent, 
            ht_test_temp_deg_c, uts_300_ht_ksi, ys_300_ht_ksi, elong_300_ht_percent, 
            hardness_ne_hrc, hardness_oe_hrc, corrosion_limits_mg_dm2, cold_work_percent, 
            Cell{i}
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?
        );
        """
        cursor.execute(insert_sql, (
            random_channel_id, random_property_name, random_database_type,
            random_reactor_type, random_reactor_name, random_entry_by, random_remark,
            random_uts_rt_ksi, random_ys_rt_ksi, random_elong_rt_percent,
            random_ht_test_temp_deg_c, random_uts_300_ht_ksi, random_ys_300_ht_ksi,
            random_elong_300_ht_percent, random_hardness_ne_hrc, random_hardness_oe_hrc,
            random_corrosion_limits_mg_dm2, random_cold_work_percent, random.uniform(1, 100)
        ))

    print("Random data inserted into Tube_Mechanical_Properties table.")

# Insert into Tube_Chemical_Composition table
def insert_into_chemical_composition():
    for i in range(1, 6):  # Random data for the first few rows
        niobium_nb_ppm = random.uniform(1, 100)
        oxygen_o_ppm = random.uniform(1, 100)
        iron_fe_ppm = random.uniform(1, 100)
        carbon_c_ppm = random.uniform(1, 100)
        nitrogen_n_ppm = random.uniform(1, 100)
        hydrogen_h_ppm = random.uniform(1, 100)
        
        insert_sql = """
        INSERT INTO Tube_Chemical_Composition (
            channel_id, property_name, database_type, reactor_type, reactor_name,
            entered_by, remark, niobium_nb_ppm, oxygen_o_ppm, iron_fe_ppm,
            carbon_c_ppm, nitrogen_n_ppm, hydrogen_h_ppm
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        );
        """
        cursor.execute(insert_sql, (
            random_channel_id, random_property_name, random_database_type,
            random_reactor_type, random_reactor_name, random_entry_by, random_remark,
            niobium_nb_ppm, oxygen_o_ppm, iron_fe_ppm, carbon_c_ppm,
            nitrogen_n_ppm, hydrogen_h_ppm
        ))

    print("Random data inserted into Tube_Chemical_Composition table.")

# Insert into Tube_Ingot_Details table
def insert_into_ingot_details():
    elements = ["niobium_nb", "oxygen_o", "iron_fe", "carbon_c", "hydrogen_h", "nitrogen_n", "phosphorus_p", "tin_sn", "aluminium_al", "chlorine_cl"]
    
    for i in range(1, 6):  # Insert 5 random entries
        for element in elements:
            for j in range(1, 5):
                ppm_value = random.uniform(1, 100)  # Random ppm value
                insert_sql = f"""
                INSERT INTO Tube_Ingot_Details (
                    channel_id, property_name, database_type, reactor_type, reactor_name, 
                    entered_by, remark, {element}_ppm_{j}
                ) VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?
                );
                """
                cursor.execute(insert_sql, (
                    random_channel_id, random_property_name, random_database_type,
                    random_reactor_type, random_reactor_name, random_entry_by, random_remark,
                    ppm_value
                ))

    print("Random data inserted into Tube_Ingot_Details table.")

def insert_into_installation():
    for i in range(1, 6):  # For 5 rows of data
        insert_sql = f"""
INSERT INTO Tube_Installation (
    channel_id, property_name, database_type, reactor_type, reactor_name, 
    entered_by, remark, coolant_tube_no, hq_ncr_no, imp_hq_ncr_comments,
    trimming_length_south, trimming_length_north, two_t_south, od_coolant_tube_rolling_area_s,
    ef_no_s, ef_dcr_s, b1_dia_s, inter_clear_south, gray_lock_orientation_s, roller_reach_s,
    lt_pt_gap_br_s, lt_pt_gap_ar_s, exp_set_dia_required_s, exp_set_dia_actual_s, 
    spring_back_s, rolled_id_s, percent_wall_red_s, helium_leak_rate_s, two_t_north, 
    od_coolant_tube_rolling_area_n, ef_no_n, ef_dcr_n, b1_dia_n, inter_clear_north, 
    gray_lock_orientation_n, expander_reach_n, lt_pt_gap_br_n, lt_pt_gap_ar_n,
    exp_set_dia_required_n, exp_set_dia_actual_n, spring_back_n, rolled_id_n,
    percent_wall_red_n, helium_leak_rate_n, gs_1_position, gs_1_coil_diameter, gs_2_position, 
    gs_2_coil_diameter, gs_3_position, gs_3_coil_diameter, gs_4_position, gs_4_coil_diameter,
    pt_trimmed_length_south, pt_trimmed_length_north, visual_observation_od_nfc_report, 
    boroscopic_inspection_observation, observations_duration_videography_rolled_area_s,
    observations_duration_videography_rolled_area_n, site_installation_ncr_dcr,
    cell_50, cell_51, cell_52, cell_53, cell_54, cell_55, cell_56, cell_57, cell_58, 
    cell_59, cell_60, cell_61, cell_62, cell_63, cell_64, cell_65, cell_66, cell_67, 
    cell_68, cell_69, cell_70, cell_71, cell_72, cell_73, cell_74, cell_75, cell_76, 
    cell_77, cell_78, cell_79, cell_80, cell_81, cell_82, cell_83, cell_84, cell_85, 
    cell_86, cell_87, cell_88, cell_89, cell_90, cell_91, cell_92, cell_93, cell_94, 
    cell_95, cell_96, cell_97, cell_98, cell_99, cell_100
) VALUES (
    ?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
);
"""

        # Make sure this data list has 110 values
        data = (
            random_channel_id, random_property_name, random_database_type,
            random_reactor_type, random_reactor_name, random_entry_by, random_remark,
            random.randint(1000, 9999), random.randint(1000, 9999), "Sample Comment",
            random.uniform(1, 100), random.uniform(1, 100), random.uniform(1, 100), random.uniform(1, 100),
            random.uniform(1, 100), random.uniform(1, 100), random.uniform(1, 100), random.uniform(1, 100),
            random.uniform(1, 100), random.uniform(1, 100), random.uniform(1, 100), random.uniform(1, 100),
            random.uniform(1, 100), random.uniform(1, 100), random.uniform(1, 100), random.uniform(1, 100),
            random.uniform(1, 100), random.uniform(1, 100), random.uniform(1, 100), random.uniform(1, 100),
            random.uniform(1, 100), random.uniform(1, 100), random.uniform(1, 100), random.uniform(1, 100),
            random.uniform(1, 100), random.uniform(1, 100), random.uniform(1, 100), random.uniform(1, 100),
            random.uniform(1, 100), random.uniform(1, 100), random.uniform(1, 100),
            random.uniform(1, 100), random.uniform(1, 100), random.uniform(1, 100), random.uniform(1, 100),
            random.uniform(1, 100), random.uniform(1, 100), random.uniform(1, 100),
            random.uniform(1, 100), random.uniform(1, 100), random.uniform(1, 100), random.uniform(1, 100),
            random.uniform(1, 100), random.uniform(1, 100), random.uniform(1, 100),
            random.uniform(1, 100), random.uniform(1, 100), random.uniform(1, 100), random.uniform(1, 100),
            random.uniform(1, 100), random.uniform(1, 100), random.uniform(1, 100),
            random.uniform(1, 100), random.uniform(1, 100), random.uniform(1, 100), random.uniform(1, 100),
            random.uniform(1, 100), random.uniform(1, 100), random.uniform(1, 100),
            random.uniform(1, 100), random.uniform(1, 100), random.uniform(1, 100), random.uniform(1, 100),
            random.uniform(1, 100), random.uniform(1, 100), random.uniform(1, 100),
            random.uniform(1, 100), random.uniform(1, 100), random.uniform(1, 100), random.uniform(1, 100),
            random.uniform(1, 100), random.uniform(1, 100), random.uniform(1, 100),
            random.uniform(1, 100), random.uniform(1, 100), random.uniform(1, 100), random.uniform(1, 100),
            random.uniform(1, 100), random.uniform(1, 100), random.uniform(1, 100), random.uniform(1, 100), random.uniform(1, 100),
            random.uniform(1, 100), random.uniform(1, 100), random.uniform(1, 100), random.uniform(1, 100),
            random.uniform(1, 100), random.uniform(1, 100),random.uniform(1, 100), random.uniform(1, 100), random.uniform(1, 100),
            random.uniform(1, 100), random.uniform(1, 100), random.uniform(1, 100), random.uniform(1, 100),
            random.uniform(1, 100), random.uniform(1, 100), random.uniform(1, 100),
            random.uniform(1, 100), random.uniform(1, 100)
        )

        cursor.execute(insert_sql, data)

    print("Random data inserted into Tube_Installation table.")
# Execute all insertion functions
insert_random_values_into_reactor_data_tables()
insert_into_mechanical_properties()
insert_into_chemical_composition()
insert_into_ingot_details()
insert_into_installation()

# Function to insert random values into the specified table
def insert_random_values(table_name, cell_value_type):
    # Start of the SQL command to insert data
    insert_sql = f"""
    INSERT INTO {table_name} (
        Channel_ID, Property_Name, Database_Type, Reactor_Type, Reactor_Name, HOY, FPY,
        Entered_By, Year, Remark,
    """
    
    # Add columns for each cell up to Cell100
    for i in range(1, 101):
        if(table_name!="ISI_Channel_Length" and table_name!="ISI_Inspection_Log" and table_name!="ISI_GS_Position"):
            insert_sql += f"Cell{i}_Position_mm, "
        if(table_name=="ISI_Inspection_Log"):
            if(i==100):
                continue
            insert_sql += f"Cell{i+1}, "
        elif(table_name=="ISI_GS_Position"):
            insert_sql += f"Cell{i}, "
        else:
            insert_sql += f"Cell{i}_{cell_value_type}, "
    
    # Remove last comma and add closing parenthesis for the column names
    insert_sql = insert_sql.rstrip(", ") + ") VALUES ("
    
    # Add fixed values for the initial columns
    insert_sql += f"'{random_channel_id}', '{random_property_name}', '{random_database_type}', "
    insert_sql += f"'{random_reactor_type}', '{random_reactor_name}', '{random_hoy}', {random_fpy}, "
    insert_sql += f"'{random_entry_by}', {random_year}, '{random_remark}', "

    # Add random values for each cell column
    for i in range(1, 101):
        if(table_name!="ISI_Channel_Length" and table_name!="ISI_Inspection_Log" and table_name!="ISI_GS_Position"):
            insert_sql += f"{random.uniform(0, 100):.2f}, "  # Position_mm
        if(table_name=="ISI_Inspection_Log"):
            if(i==100):
                continue
            insert_sql += f"{random.uniform(0, 50):.2f}, " 
        else:
            insert_sql += f"{random.uniform(0, 50):.2f}, "   # Value for Diameter, Sag, Thickness, Length, or general cell
     
    # Remove last comma and add closing parenthesis for values
    insert_sql = insert_sql.rstrip(", ") + ");"

    # Execute the SQL command to insert data
    cursor.execute(insert_sql)

# Insert random data for each table
insert_random_values("ISI_PSI_Avg_Diameter", "Diameter_mm")
insert_random_values("ISI_PT_Centerline_SAG", "Sag_mm")
insert_random_values("ISI_Thickness", "Thickness_mm")
insert_random_values("ISI_Channel_Length", "Length_mm")
def print_table_columns(table_name):
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    print(f"Columns in {table_name}:")
    for column in columns:
        print(column[1])  # Print column name

# Check the columns in each table to verify their structure
print_table_columns("ISI_GS_Position")
insert_random_values("ISI_Inspection_Log", "Inspec")  # For this table, cells do not have Position_mm
insert_random_values("ISI_GS_Position", "GSPos")     # For this table, cells do not have Position_mm

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Random values inserted into all tables successfully.")







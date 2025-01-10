import pandas as pd
import mysql.connector

# Database connection details
db_config = {
    'host': 'localhost',
    'user': 'root',  
    'password': 'akash', 
    'database': 'iot_database'  
}

# Step 1: Established the connection
try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    print("Database connection successful.")
except mysql.connector.Error as err:
    print(f"Error: {err}")
    exit(1)

# Step 2: Created Tables
try:
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sites (
            site_id INT AUTO_INCREMENT PRIMARY KEY,
            site_name VARCHAR(255) NOT NULL UNIQUE
        );
    ''')
    print("Table 'sites' created successfully.")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS meters (
            meter_id INT AUTO_INCREMENT PRIMARY KEY,
            meter_name VARCHAR(255) NOT NULL UNIQUE,
            site_id INT,
            FOREIGN KEY (site_id) REFERENCES sites(site_id)
        );
    ''')
    print("Table 'meters' created successfully.")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS readings (
            reading_id INT AUTO_INCREMENT PRIMARY KEY,
            meter_id INT,
            timestamp DATETIME NOT NULL,
            sensor_name VARCHAR(255) NOT NULL,
            sensor_value FLOAT NOT NULL,
            status VARCHAR(50),
            FOREIGN KEY (meter_id) REFERENCES meters(meter_id)
        );
    ''')
    print("Table 'readings' created successfully.")

except mysql.connector.Error as err:
    print(f"Error: {err}")
    cursor.close()
    conn.close()
    exit(1)

# Step 3: Loading the dataset
file_path = "Clean_IoT_Sensor_Data.csv"  
df = pd.read_csv(file_path)


# Step 4: Inserting data into database
try:
    # unique site_ids from the dataset
    unique_sites = df['site_id'].unique()
    # Inserting unique site_ids into the 'sites' table
    for site_name in unique_sites:
        cursor.execute('''
            INSERT IGNORE INTO sites (site_name) VALUES (%s)
        ''', (site_name,))
        conn.commit()

    # Inserting data into 'meters' and 'readings' tables
    for index, row in df.iterrows():
        # Retrieving the site_id for the current row
        cursor.execute('''
            SELECT site_id FROM sites WHERE site_name = %s
        ''', (row['site_id'],))
        site_id = cursor.fetchone()[0]

        # Inserting into meters table
        cursor.execute('''
            INSERT IGNORE INTO meters (meter_name, site_id) VALUES (%s, %s)
        ''', (row['meter_id'], site_id))
        conn.commit()

        # Retrieving the meter_id for the current row
        cursor.execute('''
            SELECT meter_id FROM meters WHERE meter_name = %s
        ''', (row['meter_id'],))
        meter_id = cursor.fetchone()[0]

        # Inserting into readings table
        cursor.execute('''
            INSERT INTO readings (meter_id, timestamp, sensor_name, sensor_value,status) VALUES (%s, %s, %s, %s,%s)
        ''', (meter_id, row['timestamp'], row['sensor_name'], row['sensor_value'], row['status']))
        conn.commit()

    print("Data successfully imported into the database.")

except mysql.connector.Error as err:
    print(f"Error while inserting data: {err}")
finally:
    cursor.close()
    conn.close()
    print("Database connection closed.")

import mysql.connector
from datetime import datetime, timedelta

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
    cursor = conn.cursor(dictionary=True) 
    print("Database connection successful.")
except mysql.connector.Error as err:
    print(f"Error: {err}")
    exit(1)

# Step 2: Defined and executed SQL queries
try:
    # Query 1: Total power consumption for each site over the two-week period
    print("\n--- Total Power Consumption for Each Site ---")
    cursor.execute('''
        SELECT 
            s.site_name, 
            SUM(r.sensor_value) AS total_power_consumption
        FROM readings r
        INNER JOIN meters m ON r.meter_id = m.meter_id
        INNER JOIN sites s ON m.site_id = s.site_id
        WHERE r.sensor_name = 'power_consumption'
        GROUP BY s.site_name;
    ''')
    total_power_results = cursor.fetchall()
    for row in total_power_results:
        print(f"Site: {row['site_name']}, Total Power Consumption: {row['total_power_consumption']}")

    # Query 2: Identifying meters contributing the highest power usage at each site
    print("\n--- Meters with Highest Power Usage at Each Site ---")
    cursor.execute('''
        SELECT 
            s.site_name, 
            m.meter_name,
            SUM(r.sensor_value) AS total_power_consumption
        FROM readings r
        INNER JOIN meters m ON r.meter_id = m.meter_id
        INNER JOIN sites s ON m.site_id = s.site_id
        WHERE r.sensor_name = 'power_consumption'
        GROUP BY s.site_name, m.meter_name
        ORDER BY s.site_name, total_power_consumption DESC;
    ''')
    highest_power_results = cursor.fetchall()

    current_site = None
    for row in highest_power_results:
        if row['site_name'] != current_site:
            print(f"\nSite: {row['site_name']}")
            current_site = row['site_name']
        print(f"  Meter: {row['meter_name']}, Power Usage: {row['total_power_consumption']}")

    # Query 3: Identifying missing timestamps in the data for each meter
    print("\n--- Missing Timestamps for Each Meter ---")
    cursor.execute('''
        SELECT DISTINCT meter_id FROM readings;
    ''')
    meter_ids = [row['meter_id'] for row in cursor.fetchall()]

    for meter_id in meter_ids:
        cursor.execute('''
            SELECT MIN(timestamp) AS start_time, MAX(timestamp) AS end_time 
            FROM readings
            WHERE meter_id = %s;
        ''', (meter_id,))
        time_range = cursor.fetchone()
        
        start_time = time_range['start_time']
        end_time = time_range['end_time']

        cursor.execute('''
            SELECT timestamp FROM readings WHERE meter_id = %s ORDER BY timestamp;
        ''', (meter_id,))
        timestamps = [row['timestamp'] for row in cursor.fetchall()]

        # Check for missing timestamps
        missing_timestamps = []
        current_time = start_time
        while current_time <= end_time:
            if current_time not in timestamps:
                missing_timestamps.append(current_time)
            current_time += timedelta(minutes=5)  # 5-minute interval

        if missing_timestamps:
            print(f"Meter ID: {meter_id}, Missing Timestamps: {len(missing_timestamps)}")
        else:
            print(f"Meter ID: {meter_id}, No missing timestamps.")

except mysql.connector.Error as err:
    print(f"Error while executing queries: {err}")
finally:
    cursor.close()
    conn.close()
    print("\nDatabase connection closed.")

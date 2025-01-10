import pandas as pd
import mysql.connector
from sklearn.preprocessing import MinMaxScaler
from datetime import timedelta

# Database connection details
db_config = {
    'host': 'localhost',
    'user': 'root', 
    'password': 'akash', 
    'database': 'iot_database' 
}

class DataPreProcessor:
    def __init__(self, db_config):
        self.db_config = db_config
        self.conn = None

    def fetch_data(self):
        """Fetched sensor data from the database."""
        try:
            self.conn = mysql.connector.connect(**self.db_config)
            query = '''
                SELECT meter_id, timestamp, sensor_name, sensor_value
                FROM readings
                WHERE sensor_name = 'power_consumption'; 
            '''
            df = pd.read_sql(query, con=self.conn)
            print("Data fetched successfully.")
            return df
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
        finally:
            if self.conn:
                self.conn.close()

    def normalize_sensor_values(self, df):
        """Normalized sensor values between 0 and 1."""
        scaler = MinMaxScaler()
        df['normalized_value'] = scaler.fit_transform(df[['sensor_value']])
        print("Sensor values normalized.")
        return df

    def create_time_series(self, df):
        """Created a time-series DataFrame with missing timestamps handled."""
        df['timestamp'] = pd.to_datetime(df['timestamp'])  
        df.set_index('timestamp', inplace=True) 

        df = df.infer_objects()  # Converted object dtype to specific dtypes

        # Resample to 5-minute intervals and interpolate missing values
        df = df.groupby('meter_id', group_keys=False).apply(
            lambda group: group.resample('5min').interpolate(method='time')
        )
        
        print("Time-series DataFrame created with missing timestamps interpolated.")
        return df

# Instantiate and run the DataPreProcessor
if __name__ == "__main__":
    processor = DataPreProcessor(db_config)

    # Step 1: Fetched data
    data = processor.fetch_data()
    if data is not None:
        # Step 2: Normalized sensor values
        normalized_data = processor.normalize_sensor_values(data)

        # Step 3: Created a time-series DataFrame
        time_series_data = processor.create_time_series(normalized_data)

        # Displayed the processed data
        print(time_series_data.head())

        # Saved the processed data to a CSV file (optional)
        time_series_data.to_csv("processed_iot_data.csv")

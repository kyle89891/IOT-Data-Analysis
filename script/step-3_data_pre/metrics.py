import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns
import os

class MetricsCalculator:
    def __init__(self, db_config):
        self.db_config = db_config
        self.connection = mysql.connector.connect(**db_config)
        self.cursor = self.connection.cursor()
    
    def fetch_data(self):
        
        query = ''' 
        SELECT s.site_id AS site_id, r.timestamp AS timestamp, r.sensor_value AS sensor_value
        FROM readings r
        INNER JOIN meters m ON r.meter_id = m.meter_id
        INNER JOIN sites s ON m.site_id = s.site_id
        '''
        # Fetched data and load into DataFrame
        df = pd.read_sql(query, con=self.connection)
        df['timestamp'] = pd.to_datetime(df['timestamp']) 
        return df

    def calculate_metrics(self, df):
        """
        Calculated daily and weekly metrics using Pandas.
        """
        df.set_index('timestamp', inplace=True)

        # Daily Metrics
        daily_metrics = df.resample('D').agg({
            'sensor_value': ['mean', 'max', 'sum']
        }).rename(columns={
            'mean': 'daily_average',
            'max': 'daily_max',
            'sum': 'daily_total'
        })

        # Weekly Metrics
        weekly_metrics = df.resample('W').agg({
            'sensor_value': ['mean', 'max', 'sum']
        }).rename(columns={
            'mean': 'weekly_average',
            'max': 'weekly_max',
            'sum': 'weekly_total'
        })

        # Reset index for easier processing
        daily_metrics.columns = daily_metrics.columns.droplevel(0)
        daily_metrics.reset_index(inplace=True)

        weekly_metrics.columns = weekly_metrics.columns.droplevel(0)
        weekly_metrics.reset_index(inplace=True)

        return daily_metrics, weekly_metrics

    def calculate_site_metrics(self, df):
        """
        Calculate daily metrics per site.
        """
        site_metrics = df.groupby(['site_id']).resample('D').agg({
            'sensor_value': ['mean', 'max', 'sum']
        }).rename(columns={
            'mean': 'daily_average',
            'max': 'daily_max',
            'sum': 'daily_total'
        })

        # Flatten columns
        site_metrics.columns = site_metrics.columns.droplevel(0)
        site_metrics.reset_index(inplace=True)

        return site_metrics
    
    def create_table(self, table_name, metrics_df):
        """
        Created a table in the database based on the columns of the metrics DataFrame.
        """
        columns_with_types = ", ".join([f"{col} FLOAT" if col != 'timestamp' else f"{col} DATETIME" for col in metrics_df.columns])
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} (id INT AUTO_INCREMENT PRIMARY KEY, {columns_with_types})"
        self.cursor.execute(create_table_query)
        print(f"Table '{table_name}' created or already exists.")

    def store_metrics(self, table_name, metrics_df):
        """
        Stored the calculated metrics into a database table using mysql-connector.
        """
        # Created the table if it doesn't exist
        self.create_table(table_name, metrics_df)
        
        # Inserted data into the table
        for _, row in metrics_df.iterrows():
            # Prepared the INSERT query based on the table's columns
            columns = ', '.join(metrics_df.columns)
            values = []

            # Ensured timestamp values are wrapped in quotes
            for val, col in zip(row.tolist(), metrics_df.columns):
                if isinstance(val, pd.Timestamp):  
                    values.append(f'"{val.strftime("%Y-%m-%d %H:%M:%S")}"')
                else:
                    values.append(str(val))

            values_str = ', '.join(values)
            insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({values_str})"
            print(insert_query)

            # Executed the query and commit
            self.cursor.execute(insert_query)
            
            # Commit all changes
            self.connection.commit()
        print(f"Metrics stored in table '{table_name}'.")

    def save_metrics_to_csv(self, daily_metrics, weekly_metrics, site_metrics, file_name="metrics_report.csv"):
        """
        Combine all metrics (daily, weekly, site) and save them to a CSV file.
        """
        # Merged all metrics into a single DataFrame
        combined_metrics = pd.merge(daily_metrics, weekly_metrics, on='timestamp', how='outer')
        combined_metrics = pd.merge(combined_metrics, site_metrics, on='timestamp', how='outer')

        # Saved the combined metrics to CSV
        combined_metrics.to_csv(file_name, index=False)
        print(f"Metrics report saved to '{file_name}'.")

class GraphGenerator:
    def __init__(self, output_folder='visualizations'):
        """
        Initialized the class with the folder to store visualizations.
        """
        self.output_folder = output_folder
        # Created the output folder if it doesn't exist
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def plot_time_series(self, df, title, file_name):
        """
        Ploted a time-series graph for the sensor data.
        """
        plt.figure(figsize=(10, 6))
        sns.lineplot(x='timestamp', y='sensor_value', data=df)
        plt.title(title)
        plt.xlabel('Timestamp')
        plt.ylabel('Sensor Value')
        plt.xticks(rotation=45)
        plt.tight_layout()

        plot_path = os.path.join(self.output_folder, file_name)
        plt.savefig(plot_path)
        plt.close()
        print(f"Time-series plot saved to {plot_path}")

    def plot_daily_metrics(self, daily_metrics_df, title, file_name):
        """
        Ploted daily metrics (e.g., daily averages, max, and totals).
        """
        plt.figure(figsize=(10, 6))
        sns.lineplot(x='timestamp', y='daily_average', data=daily_metrics_df, label='Average')
        sns.lineplot(x='timestamp', y='daily_max', data=daily_metrics_df, label='Max')
        sns.lineplot(x='timestamp', y='daily_total', data=daily_metrics_df, label='Total')
        plt.title(title)
        plt.xlabel('Date')
        plt.ylabel('Sensor Value')
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()

        plot_path = os.path.join(self.output_folder, file_name)
        plt.savefig(plot_path)
        plt.close()
        print(f"Daily metrics plot saved to {plot_path}")

    def plot_weekly_metrics(self, weekly_metrics_df, title, file_name):
        """
        Ploted weekly metrics (e.g., weekly averages, max, and totals).
        """
        plt.figure(figsize=(10, 6))
        sns.lineplot(x='timestamp', y='weekly_average', data=weekly_metrics_df, label='Average')
        sns.lineplot(x='timestamp', y='weekly_max', data=weekly_metrics_df, label='Max')
        sns.lineplot(x='timestamp', y='weekly_total', data=weekly_metrics_df, label='Total')
        plt.title(title)
        plt.xlabel('Date')
        plt.ylabel('Sensor Value')
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()

        plot_path = os.path.join(self.output_folder, file_name)
        plt.savefig(plot_path)
        plt.close()
        print(f"Weekly metrics plot saved to {plot_path}")

    def plot_site_metrics(self, site_metrics_df, title, file_name):
        """
        Ploted site-specific metrics (e.g., daily averages, max, and totals per site).
        """
        plt.figure(figsize=(10, 6))
        sns.barplot(x='site_id', y='daily_average', data=site_metrics_df)
        plt.title(title)
        plt.xlabel('Site ID')
        plt.ylabel('Daily Average Sensor Value')
        plt.tight_layout()

        plot_path = os.path.join(self.output_folder, file_name)
        plt.savefig(plot_path)
        plt.close()
        print(f"Site metrics plot saved to {plot_path}")


# Usage Example
if __name__ == "__main__":
    # Database connection details
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'akash',
        'database': 'iot_database'
    }

    # Initialize MetricsCalculator
    metrics_calculator = MetricsCalculator(db_config)
    graph_generator = GraphGenerator()

    # Fetch data from the database
    sensor_data = metrics_calculator.fetch_data()

    # Calculate metrics
    daily_metrics, weekly_metrics = metrics_calculator.calculate_metrics(sensor_data)
    site_metrics = metrics_calculator.calculate_site_metrics(sensor_data)


    # Store metrics in the database
    metrics_calculator.store_metrics('daily_metrics', daily_metrics)
    metrics_calculator.store_metrics('weekly_metrics', weekly_metrics)
    metrics_calculator.store_metrics('site_metrics', site_metrics)

     # Generate and store visualizations
    graph_generator.plot_time_series(sensor_data, "Sensor Time-Series Data", "time_series_plot.png")
    graph_generator.plot_daily_metrics(daily_metrics, "Daily Metrics", "daily_metrics_plot.png")
    graph_generator.plot_weekly_metrics(weekly_metrics, "Weekly Metrics", "weekly_metrics_plot.png")
    graph_generator.plot_site_metrics(site_metrics, "Site Metrics", "site_metrics_plot.png")

     # Generate the CSV report
    metrics_calculator.save_metrics_to_csv(daily_metrics, weekly_metrics, site_metrics, "metrics_report.csv")

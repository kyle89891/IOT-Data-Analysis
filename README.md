# IoT Data Pipeline and Analysis

This repository demonstrates an end-to-end data pipeline for IoT sensor data, including data exploration, cleaning, database operations, analysis, preprocessing, and visualization. The project is modularly organized into folders based on the workflow steps.

## Repository Structure

```
script/
├── step-1_Explore/
│   ├── IoT_Sensor_Data/               # Contains raw CSV data files
│   └── Explore_data.py    # Performs data cleaning and exports cleaned data
├── step-2_Load/
│   └── load.py              # Database configurations and data loading
    └── analysis.py         # Queries and fetches insights from the database
├── step-3_data_pre/
    ├── visualizations    #contains graphs pic in png                      #  
│   ├── test.py          # Data preprocessing operations
│   └── metrices.py      # Calculates metrics, generates graphs, and stores results
├── Dockerfile              # Docker setup for containerization
└── requirements.txt       # Python dependencies
```

---

## Workflow Details

### Step 1: Explore and Clean Data
- **File**: `Explore_data.py`
- **Description**: This script performs:
  - Data cleaning (e.g., handling missing or negative values).
  - Exporting a cleaned dataset as a new CSV file.
- **Output**: Cleaned CSV file.

### Step 2: Load Data into Database
- **File**: `load.py`
- **Description**:
  - Configures the database connection.
  - Loads the cleaned CSV data into a database.
  - Creates necessary database tables or schemas for the data.

  ### Analysis Queries
  - **File**: `analysis.py`
  - **Description**: Runs SQL queries to extract insights, such as:
    - Total power consumption for each site over a two-week period.
    - Meters contributing the highest power usage at each site.
    - Identifying missing timestamps in the data.

### Step 3: Data Preprocessing and Analysis
#### **Preprocessing**
- **File**: `test.py`
- **Description**:
  - Normalizes sensor values.
  - Creates a time-series DataFrame.
  - Saves the processed data to `processed_iot_data.csv`.

#### **Metrics Calculation and Visualization**
- **File**: `metrices.py`
- **Description**:
  - Calculates daily and weekly metrics and stores them in a new database table.
  - Generates visualizations using Seaborn and Matplotlib.
  - Saves graphs in the `visualization/` folder.
  - Exports a report summarizing the metrics and analysis.

---

## Additional Files
- **`Dockerfile`**:
  - Configures the environment for running the pipeline in a Docker container.
- **`requirements.txt`**:
  - Lists the Python dependencies required to run the scripts.

---

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd script
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the pipeline:
   - **Step 1**: Data Cleaning:
     ```bash
     python step-1_Explore/Explore_data.py
     ```
   - **Step 2**: Load Data:
     ```bash
     python step-2_Load/load.py
     ```
   - **Run Analysis Queries**:
     ```bash
     python analysis.py
     ```
   - **Step 3**: Preprocess Data:
     ```bash
     python step-3_data_pre/test.py
     ```
   - **Calculate Metrics and Generate Reports**:
     ```bash
     python step-3_data_pre/metrices.py
     ```
   

4. (Optional) Run in Docker:
   ```bash
   docker build -t iot-data-pipeline .
   docker run iot-data-pipeline
   ```

---

## Outputs
- **Cleaned Data**: Saved as a CSV in Step 1.
- **Processed Data**: Time-series data saved as `processed_iot_data.csv`.
- **Metrics and Visualizations**:
  - Metrics stored in the database.
  - Graphs saved in the `visualization/` folder.
  - Summary report generated in Step 3.

---

## Technologies Used
- **Python Libraries**: Pandas, NumPy, Matplotlib, Seaborn.
- **Database**: SQL-based database (configured in `load.py`).
- **Containerization**: Docker.

---

Feel free to raise issues or contribute to the repository!


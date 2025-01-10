import pandas as pd

# Step 1: Loading the dataset
file_path = "IoT_Sensor_Data.csv" 
df = pd.read_csv(file_path)

# Step 2: Inspecting the dataset
print("\n--- First Few Rows of the Dataset ---")
print(df.head())

print("\n--- Dataset Information ---")
df.info()

print("\n--- Summary Statistics ---")
print(df.describe())

# Step 3: Identifying Issues

# Checking for missing values
print("\n--- Missing Values ---")
missing_values = df.isnull().sum()
print(missing_values)

# Checking for duplicate rows
print("\n--- Duplicate Rows ---")
num_duplicates = df.duplicated().sum()
print(f"Number of duplicate rows: {num_duplicates}")

# Checking for inconsistent data (e.g., negative values in specific columns)

if 'temperature' in df.columns:
    negative_temp = df[df['temperature'] < 0]
    print(f"\n--- Negative Temperature Values ---\n{negative_temp}")

if 'power_consumption' in df.columns:
    negative_power = df[df['power_consumption'] < 0]
    print(f"\n--- Negative Power Consumption Values ---\n{negative_power}")

# Step 4: Report Summary
print("\n--- Data Quality Summary ---")
if missing_values.any():
    print("The dataset has missing values.")
else:
    print("No missing values detected.")

if num_duplicates > 0:
    print(f"The dataset contains {num_duplicates} duplicate rows.")
else:
    print("No duplicate rows detected.")

if 'temperature' in df.columns and not negative_temp.empty:
    print(f"There are {len(negative_temp)} rows with negative temperature values.")
else:
    print("No negative temperature values detected.")

if 'power_consumption' in df.columns and not negative_power.empty:
    print(f"There are {len(negative_power)} rows with negative power consumption values.")
else:
    print("No negative power consumption values detected.")


# Saving the cleaned DataFrame to a new file
clean_file_path = "Clean_IoT_Sensor_Data.csv"
df.to_csv(clean_file_path, index=False)
print(f"\nCleaned data has been saved to {clean_file_path}")
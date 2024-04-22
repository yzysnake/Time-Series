import os
import pandas as pd
from datetime import datetime

# Set the directory
directory = "Traffic Flow Data"

# Function to parse date from filename
def parse_date(filename):
    parts = filename.split('-')
    year = int(parts[2])
    month = parts[3]
    day = int(parts[4].split('.')[0])  # Remove the file extension
    month_number = datetime.strptime(month, '%B').month
    return datetime(year, month_number, day)

# List to hold data from each file
data_frames = []

# Get all Excel files and sort them by date in descending order
files = [f for f in os.listdir(directory) if f.endswith(".xls") or f.endswith(".xlsx")]
files.sort(key=parse_date, reverse=False)  # Sort ascending to maintain the file order by date

# Iterate through every file in the sorted list
for filename in files:
    file_path = os.path.join(directory, filename)
    # Determine the appropriate engine based on file extension
    engine = 'xlrd' if filename.endswith('.xls') else 'openpyxl'
    try:
        data = pd.read_excel(file_path, sheet_name='Sheet0', usecols="E", skiprows=4, nrows=24, engine=engine)
        data_frames.append(data)
    except Exception as e:
        print(f"Failed to process {filename}: {e}")

# Only attempt to concatenate if data_frames is not empty
if data_frames:
    combined_data = pd.concat(data_frames, axis=0)  # Concatenate vertically
    combined_data.columns = ['traffic_flow']  # Rename the single column to 'traffic_flow'
    combined_data.reset_index(drop=True, inplace=True)  # Reset index to ensure continuous index
    output_path = os.path.join(directory, 'Combined_Traffic_Flow_Data.xlsx')
    combined_data.to_excel(output_path, index=False, engine='openpyxl')
    print(f"Data combined and saved to {output_path}")
else:
    print("No valid Excel data to process.")

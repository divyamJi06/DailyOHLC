import json
import os
import csv
from datetime import datetime

def convert_to_unix_timestamp(date_str):
    """
    Converts a date string in 'YYYY-MM-DD' format to a Unix timestamp.
    """
    dt = datetime.strptime(date_str, "%Y%m%d")
    return int(dt.timestamp())

def get_data_from_csv(base_path, year, month, day):
    """
    Reads data from a CSV file at the specified path and processes it.
    
    Args:
        base_path (str): The base directory where the CSV files are stored.
        year (str): The year as a string.
        month (str): The month as a string.
        day (str): The day as a string.

    Returns:
        dict: Processed data grouped by symbol.
    """
    # Construct the path to the CSV file
    day_path = os.path.join(base_path, year, month, f"{day}.csv")

    symbol_data = {}

    try:
        # Read and process the CSV file
        with open(day_path, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                symbol = row["SYMBOL"]
                timestamp = convert_to_unix_timestamp(row["TIMESTAMP"])
                entry = {
                    "open": float(row["OPEN"]),
                    "high": float(row["HIGH"]),
                    "low": float(row["LOW"]),
                    "close": float(row["CLOSE"]),
                    "date": timestamp,
                    "volume": int(row["VOLUME"])
                }
                if symbol not in symbol_data:
                    symbol_data[symbol] = []
                symbol_data[symbol].append(entry)
        
        print(f"DONE {year}/{month}/{day}.csv")
    except FileNotFoundError:
        print(f"ERROR: File not found at {day_path}")
    except Exception as e:
        print(f"ERROR: An error occurred while processing {day_path}: {e}")

    return symbol_data

def save_to_json(symbol_data, output_folder):
    """
    Save symbol data to individual JSON files, appending to existing data if the file already exists.
    
    Args:
        symbol_data (dict): The processed symbol data to save.
        output_folder (str): Directory where the JSON files will be saved.
    """
    os.makedirs(output_folder, exist_ok=True)
    
    for symbol, data in symbol_data.items():
        output_path = os.path.join(output_folder, f"{symbol}.json")
        
        # Load existing data if the file exists
        if os.path.exists(output_path):
            with open(output_path, 'r') as json_file:
                try:
                    existing_data = json.load(json_file)
                except json.JSONDecodeError:
                    print(f"WARNING: Corrupt JSON file at {output_path}. Overwriting it.")
                    existing_data = []
        else:
            existing_data = []

        # Append new data
        updated_data = existing_data + data
        
        # Save updated data back to the file
        with open(output_path, 'w') as json_file:
            json.dump(updated_data, json_file, indent=4)
    
    print(f"Appended and saved JSON files to {output_folder}")


def sortDataForToday(data_path, date_str, output_folder):
    """
    Process CSV data for a given date and save results as JSON files.
    
    Args:
        data_path (str): The base directory where CSV files are stored.
        date_str (str): The date in 'YYYYMMDD' format.
        output_folder (str): The directory where JSON files will be saved.
    """
    year = date_str[:4]      # Extract year as a string
    month = date_str[4:6]    # Extract month as a string
    day = date_str[6:]       # Extract day as a string

    # Process files and save JSON
    symbol_data = get_data_from_csv(data_path, year, month, day)
    save_to_json(symbol_data, output_folder)
    print(f"Processed and saved JSON files to {output_folder}")

# Example usage
# if __name__ == "__main__":
#     BASE_FOLDER = "data"
#     OUTPUT_FOLDER = "testFolder"
#     DATE_STRING = "20241127"
#     # print("Current working directory:", os.getcwd())
#     sortDataForToday(BASE_FOLDER, DATE_STRING, OUTPUT_FOLDER)

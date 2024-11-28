import os
import csv
import json
from datetime import datetime

# Base folder containing year folders
BASE_FOLDER = "data"

def convert_to_unix_timestamp(date_str):
    """Convert YYYYMMDD to Unix timestamp."""
    dt = datetime.strptime(date_str, "%Y%m%d")
    return int(dt.timestamp())

def process_csv_files(base_folder):
    """Process all CSV files in the folder structure."""
    symbol_data = {}

    # Traverse the folder structure
    for year in os.listdir(base_folder):
        year_path = os.path.join(base_folder, year)
        if os.path.isdir(year_path):
            for month in os.listdir(year_path):
                month_path = os.path.join(year_path, month)
                if os.path.isdir(month_path):
                    for day_file in os.listdir(month_path):
                        if day_file.endswith(".csv"):
                            day_path = os.path.join(month_path, day_file)
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
                        print(f"DONE {year}/{month}/{day_file}")
    
    return symbol_data

def save_to_json(symbol_data, output_folder):
    """Save symbol data to individual JSON files."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for symbol, data in symbol_data.items():
        output_path = os.path.join(output_folder, f"{symbol}.json")
        with open(output_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

def main():
    # Specify the output folder for JSON files
    OUTPUT_FOLDER = "individual_stock_ohlc_data"

    # Process files and save JSON
    symbol_data = process_csv_files(BASE_FOLDER)
    save_to_json(symbol_data, OUTPUT_FOLDER)
    print(f"Processed and saved JSON files to {OUTPUT_FOLDER}")

if __name__ == "__main__":
    main()

from datetime import datetime, timedelta
from after07072024 import download_and_process_equity_bhavcopy
from get_individual_by_date import sortDataForToday  # Replace with actual script name
import os
import json
import pytz
import shutil
import psycopg2
from dotenv import dotenv_values

# Load environment variables
# secret = dotenv_values()
# DATABASE_URL = secret["DATABASE_URL"]

# Get the DATABASE_URL from the environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set.")
def force_remove_folder(folder_path):
    try:
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
            print(f"Folder '{folder_path}' has been removed.")
        else:
            print(f"Folder '{folder_path}' does not exist.")
    except Exception as e:
        print(f"Error: {e}")

def get_today_date():
    return datetime.today().strftime('%Y%m%d')

def format_date(timestamp):
    utc_time = datetime.utcfromtimestamp(timestamp)  # Convert timestamp to UTC
    ist_timezone = pytz.timezone("Asia/Kolkata")
    utc_time = pytz.utc.localize(utc_time)  # Localize as UTC
    ist_time = utc_time.astimezone(ist_timezone)  # Convert to IST
    ist_time = ist_time.replace(hour=15, minute=30)  # Set the time to 15:30 IST
    return ist_time

def push_to_db(folder_path):
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(DATABASE_URL, sslmode="require")
        cursor = conn.cursor()

        batch_size = 1000
        batch_buffer = []  # Buffer to store rows for batch insertion

        for filename in os.listdir(folder_path):
            if filename.endswith(".json"):
                nse_code = filename.replace(".json", "")  # Extract NSE code from filename

                # Check if the company exists
                cursor.execute("SELECT id FROM company WHERE nse_code = %s", (nse_code,))
                company = cursor.fetchone()
                if not company:
                    print(f"Company with NSE code {nse_code} not found.")
                    continue

                company_id = company[0]

                # Load the JSON file
                with open(os.path.join(folder_path, filename), "r") as file:
                    data = json.load(file)

                    for record in data:
                        date = format_date(record["date"])

                        # Check if this date already exists
                        cursor.execute(
                            "SELECT id FROM ohlc WHERE company_id = %s AND date = %s",
                            (company_id, date),
                        )
                        if cursor.fetchone():
                            print(f"Data for {nse_code} on {date} already exists. Skipping...")
                            continue

                        # Add record to the batch buffer
                        batch_buffer.append(
                            (
                                company_id,
                                date,
                                record["open"],
                                record["high"],
                                record["low"],
                                record["close"],
                                record["volume"],
                            )
                        )

                        # If buffer reaches batch size, execute batch insert
                        if len(batch_buffer) >= batch_size:
                            cursor.executemany(
                                """
                                INSERT INTO ohlc (company_id, date, open, high, low, close, volume)
                                VALUES (%s, %s, %s, %s, %s, %s, %s)
                                """,
                                batch_buffer,
                            )
                            print(f"Inserted {len(batch_buffer)} records into the database.")
                            batch_buffer.clear()  # Clear the buffer after insertion

                print(f"Data for {nse_code} processed successfully.")

        # Insert remaining records in the buffer
        if batch_buffer:
            cursor.executemany(
                """
                INSERT INTO ohlc (company_id, date, open, high, low, close, volume)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                batch_buffer,
            )
            print(f"Inserted remaining {len(batch_buffer)} records into the database.")
            batch_buffer.clear()

        # Commit the changes
        conn.commit()

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()


if __name__ == "__main__":
    # today_date = get_today_date()
    today_date = "20241206"
    output_path = "data"
    try:
        # Download and process the bhavcopy
        download_and_process_equity_bhavcopy(today_date, output_path)
        
        print("Sorting data into files")

        # Sort the stock data for today
        individual_stock_ohlc_data = "individual_stock_ohlc_data2"
        sortDataForToday(output_path, today_date, individual_stock_ohlc_data)

        print("Pushing into DB")
        # Push data to PostgreSQL
        push_to_db(individual_stock_ohlc_data)

        print("Cleaning up")
        # Clean up the folder after processing
        force_remove_folder(individual_stock_ohlc_data)
        
        print("All DONE !!")
        
    except Exception as e:
        print("Failed to get and load data")
        print(e)
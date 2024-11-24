import os
from datetime import datetime, timedelta
from before07072024 import download_and_process_equity_bhavcopy  # Import the function from your original file

def get_date_range(start_date, end_date):
    """
    Generate a list of dates from start_date to end_date.
    
    Args:
        start_date (datetime): The start date of the range.
        end_date (datetime): The end date of the range.
        
    Returns:
        list: A list of datetime objects between the start and end dates (inclusive).
    """
    delta = timedelta(days=1)
    current_date = start_date
    date_range = []
    
    while current_date <= end_date:
        date_range.append(current_date)
        current_date += delta
    
    return date_range

def process_dates(start_date, end_date, destination_folder):
    """
    Process the NSE bhavcopy for each date in the range from start_date to end_date.
    
    Args:
        start_date (datetime): The start date for processing.
        end_date (datetime): The end date for processing.
        destination_folder (str): The destination folder where processed files will be saved.
    
    Returns:
        None
    """
    # Get the range of dates to process
    date_range = get_date_range(start_date, end_date)

    # Loop through each date in the range and process the bhavcopy
    for date in date_range:
        print(f"Processing data for: {date.strftime('%Y-%m-%d')}")
        processed_df = download_and_process_equity_bhavcopy(date, destination_folder)
        if processed_df is not None:
            print(f"Processed data for {date.strftime('%Y-%m-%d')}")
        else:
            print(f"Failed to process data for {date.strftime('%Y-%m-%d')}")

if __name__ == "__main__":
    # Define your start and end dates
    start_date_str = "2014-01-01"
    # start_date_str = "2024-01-01"
    end_date_str = "2023-12-31"
    # end_date_str = "2024-07-06"

    # Convert strings to datetime objects
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    # Destination folder where the processed data will be saved
    destination_folder = "data"

    # Process the date range
    process_dates(start_date, end_date, destination_folder)

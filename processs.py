from datetime import datetime, timedelta
from after07072024 import download_and_process_equity_bhavcopy  # Replace with actual script name

def generate_date_range(start_date, end_date):
    """
    Generates a list of dates from start_date to end_date (inclusive).
    The dates are in the format 'YYYYMMDD'.
    """
    start = datetime.strptime(start_date, "%Y%m%d")
    end = datetime.strptime(end_date, "%Y%m%d")
    delta = timedelta(days=1)

    current_date = start
    while current_date <= end:
        yield current_date.strftime("%Y%m%d")
        current_date += delta

if __name__ == "__main__":
    # Define the start and end dates
    start_date = "20240813"  # Start date in YYYYMMDD format
    end_date = "20241122"    # End date in YYYYMMDD format
    output_path = "data/"  # Specify your output path here

    # Process each date in the range
    for date in generate_date_range(start_date, end_date):
        print(f"Processing data for {date}...")
        download_and_process_equity_bhavcopy(date, output_path)

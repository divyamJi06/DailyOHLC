from datetime import datetime, timedelta
from after07072024 import download_and_process_equity_bhavcopy  # Replace with actual script name


def get_today_date():
    # Get today's date in YYYYMMDD format
    return datetime.today().strftime('%Y%m%d')


if __name__ == "__main__":

    # Example usage
    today_date = get_today_date()
    output_path = "data"
    download_and_process_equity_bhavcopy(today_date,output_path)

from datetime import datetime, timedelta
from after07072024 import download_and_process_equity_bhavcopy
from get_individual_by_date import sortDataForToday  # Replace with actual script name


def get_today_date():
    # Get today's date in YYYYMMDD format
    return datetime.today().strftime('%Y%m%d')


if __name__ == "__main__":

    # Example usage
    # today_date = "20241127"
    today_date = get_today_date()
    output_path = "data"
    download_and_process_equity_bhavcopy(today_date,output_path)
    sortDataForToday(output_path, today_date, "individual_stock_ohlc_data")

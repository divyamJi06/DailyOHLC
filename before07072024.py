import os
import urllib.request
import zipfile
import pandas as pd
from io import BytesIO
from datetime import datetime


def download_bhavcopy(url, date):
    """
    Download the NSE equity bhavcopy ZIP file into memory.
    
    Args:
        date (datetime): The date for which to download the bhavcopy.
    
    Returns:
        BytesIO: The downloaded ZIP file in memory.
    """
    try:
        # Attempt to download the ZIP file into memory
        response = urllib.request.urlopen(url)
        if response.getcode() == 404:
            print(f"Error: File not available for date: {date.strftime('%Y-%m-%d')}")
            return None
        print(f"File downloaded into memory for: {date.strftime('%Y-%m-%d')}")
        return BytesIO(response.read())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"Error: File not available for date: {date.strftime('%Y-%m-%d')}")
        else:
            print(f"HTTP error occurred: {e.code} for {date.strftime('%Y-%m-%d')}")
        return None
    except Exception as e:
        print(f"Error downloading file for {date.strftime('%Y-%m-%d')}: {str(e)}")
        return None


def extract_csv_from_zip(zip_buffer):
    """
    Extract the CSV file from the given ZIP file buffer in memory.
    
    Args:
        zip_buffer (BytesIO): The ZIP file in memory.
    
    Returns:
        pd.DataFrame: The extracted CSV loaded into a DataFrame.
    """
    try:
        with zipfile.ZipFile(zip_buffer, 'r') as zip_ref:
            # Find the first file ending with "bhav.csv"
            csv_filename = [name for name in zip_ref.namelist() if name.endswith("bhav.csv")][0]
            print(f"Extracting file: {csv_filename}")
            
            # Read the file into a DataFrame
            with zip_ref.open(csv_filename) as csv_file:
                df = pd.read_csv(csv_file)
        return df
    except zipfile.BadZipFile:
        print("Error: Bad zip file.")
        return None
    except Exception as e:
        print("Error extracting CSV from ZIP file:", str(e))
        return None


def process_bhavcopy_dataframe(df):
    """
    Process the NSE equity bhavcopy DataFrame.
    
    Args:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: The processed DataFrame.
    """
    try:
        # Filter for rows where SERIES is 'EQ' (or 'BE' or 'BZ' as needed)
        df = df[df['SERIES'].isin(['EQ', 'BE', 'BZ'])]
        
        # Retain only required columns and rename 'TOTTRDQTY' to 'VOLUME'
        required_columns = {
            "SYMBOL": "SYMBOL",
            "TIMESTAMP": "TIMESTAMP",
            "OPEN": "OPEN",
            "HIGH": "HIGH",
            "LOW": "LOW",
            "CLOSE": "CLOSE",
            "TOTTRDQTY": "VOLUME"
        }
        df = df[list(required_columns.keys())].rename(columns=required_columns)
        
        # Convert the TIMESTAMP column to the desired format
        df = convert_timestamp_column(df, 'TIMESTAMP')
        return df
    except KeyError as e:
        print(f"Error: Missing required column: {str(e)}")
        return None
    except Exception as e:
        print(f"Error processing DataFrame: {str(e)}")
        return None


def convert_timestamp_column(df, column_name, output_format='%Y%m%d'):
    """
    Converts a timestamp column to a specified format, handling multiple input formats.
    
    Args:
        df (pd.DataFrame): The input DataFrame.
        column_name (str): The name of the column to convert.
        output_format (str): The desired output format (default is '%Y%m%d').
    
    Returns:
        pd.DataFrame: The DataFrame with the converted timestamp column.
    """
    try:
        input_formats = ['%d-%b-%Y', '%d-%b-%y']

        def parse_date(date_str):
            for fmt in input_formats:
                try:
                    return pd.to_datetime(date_str, format=fmt)
                except ValueError:
                    continue
            raise ValueError(f"Date format for {date_str} not recognized.")

        df[column_name] = df[column_name].apply(parse_date).dt.strftime(output_format)
        return df
    except Exception as e:
        print(f"Error converting timestamp column: {str(e)}")
        return df


def append_to_equity_bhavcopy(processed_df, source_date, destination_folder):
    """
    Append the processed data to the destination bhavcopy file if it exists, or save it if not.

    Args:
        processed_df (pd.DataFrame): The processed bhavcopy DataFrame.
        source_date (str): The date of the source file in 'YYYY-MM-DD' format.
        destination_folder (str): The destination folder path where the file should be saved.

    Returns:
        None
    """
    try:
        # Extract year, month, and day from the source date
        year = source_date[:4]
        month = source_date[5:7]
        day = source_date[8:10]

        # Construct the directory path
        directory = os.path.join(destination_folder, year, month)
        
        # Ensure the directory exists
        os.makedirs(directory, exist_ok=True)

        # Create the destination file name
        destination_file_name = f"{day}.csv"
        destination_file_path = os.path.join(directory, destination_file_name)

        # Save or append the processed DataFrame to the destination file
        if os.path.exists(destination_file_path):
            processed_df.to_csv(destination_file_path, mode='a', header=False, index=False)
            print(f"Data appended to {destination_file_path}")
        else:
            processed_df.to_csv(destination_file_path, index=False, header=True)
            print(f"Processed file saved to: {destination_file_path}")
    except Exception as e:
        print(f"Error appending to or saving the file: {str(e)}")


def download_and_process_equity_bhavcopy(date, destination_folder):
    """
    Download, extract, process, and save the NSE equity bhavcopy for the given date.
    
    Args:
        date (datetime): The date for which to download and process the bhavcopy.
        destination_folder (str): The folder where the processed file should be saved.
    
    Returns:
        pd.DataFrame: The processed DataFrame.
    """
    # Construct the URL for downloading the file
    url = "https://archives.nseindia.com/content/historical/EQUITIES/{}/{}/cm{}bhav.csv.zip".format(
        date.strftime("%Y"),
        date.strftime("%b").upper(),
        date.strftime("%d%b%Y").upper()
    )
    
    # Download the ZIP file
    zip_buffer = download_bhavcopy(url, date)
    if zip_buffer is None:
        return None

    # Extract the CSV from the ZIP
    df = extract_csv_from_zip(zip_buffer)
    if df is None:
        return None

    # Process the DataFrame
    processed_df = process_bhavcopy_dataframe(df)
    if processed_df is None:
        return None
    
    # Extract date in 'YYYY-MM-DD' format
    source_date = date.strftime('%Y-%m-%d')
    
    # Save the processed data to the destination file
    append_to_equity_bhavcopy(processed_df, source_date, destination_folder)

    # Return the processed DataFrame
    return processed_df


# # Example Usage
# if __name__ == "__main__":
#     destination_folder = "data"
#     sample_date = datetime.strptime("2022-09-12", "%Y-%m-%d")
#     processed_df = download_and_process_equity_bhavcopy(sample_date, destination_folder)
#     if processed_df is not None:
#         print(processed_df.head())

import os
import io
import urllib.request
import zipfile
import pandas as pd
from datetime import datetime

def Download_And_Extract_NSE_Bhavcopy_File(NSE_Bhavcopy_URL, output_path= "data"):
    """
    Downloads a ZIP file from the given URL, extracts it in memory, and returns the extracted file data.
    """
    try:
        # Download the ZIP file into a buffer
        response = urllib.request.urlopen(NSE_Bhavcopy_URL)
        zip_buffer = io.BytesIO(response.read())
        print("Zip file downloaded to memory.")

        # Extract the file from the ZIP buffer
        with zipfile.ZipFile(zip_buffer, 'r') as zip_ref:
            file_names = zip_ref.namelist()
            if len(file_names) == 0:
                raise Exception("The ZIP file is empty.")

            # Extract and save the first file
            extracted_file_name = file_names[0]
            extracted_data = zip_ref.read(extracted_file_name)
            print(f"File extracted from ZIP: {extracted_file_name}")

            # Save the extracted file to the output directory
            extracted_file_path = os.path.join(output_path, extracted_file_name)
            with open(extracted_file_path, "wb") as f:
                f.write(extracted_data)

        return extracted_file_path
    except Exception as e:
        print(f"Error downloading and extracting the file: {e}")
        return None

import os
from datetime import datetime

import os
from datetime import datetime

import os
from datetime import datetime

def Rename_NSE_Bhavcopy_File(file_path, date_obj, output_path="data"):
    """
    Renames a single extracted NSE Bhavcopy file and organizes it by year/month.
    Saves the file as 'DD.csv' in the year/month directory.
    """
    try:
        # Get the directory and file name from the file path
        directory, file = os.path.split(file_path)

        # Check if the file ends with the expected format
        if file.endswith("0000.csv"):
            # Generate the new file name as 'DD.csv' based on the date
            new_name = date_obj.strftime("%d") + ".csv"

            # Create a folder structure for year/month (i.e., /YYYY/MM/)
            date_folder = date_obj.strftime("%Y/%m")
            output_dir = os.path.join(output_path, date_folder)
            os.makedirs(output_dir, exist_ok=True)

            # Set the new file path with the dynamic name in the year/month directory
            new_file_path = os.path.join(output_dir, new_name)

            # Rename and move the file to the new path
            os.rename(file_path, new_file_path)
            print(f"File '{file}' renamed to: '{new_name}' and saved in {output_dir}")
            return new_file_path
        else:
            # If the file doesn't match the expected format, raise an error
            raise ValueError(f"The file '{file}' does not match the expected format.")
    except Exception as e:
        print(f"Error renaming the file: {e}")
        return None


def Modify_NSE_Bhavcopy_File(file_path):
    """
    Modifies the renamed NSE Bhavcopy file based on the specified conditions.
    """
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)

        # Remove the specified columns
        columns_to_remove = ['BizDt', 'Sgmt', 'Src', 'FinInstrmTp', 'FinInstrmId', 'ISIN', 'XpryDt',
                             'FininstrmActlXpryDt', 'StrkPric', 'OptnTp', 'FinInstrmNm', 'LastPric',
                             'PrvsClsgPric', 'UndrlygPric', 'SttlmPric', 'OpnIntrst', 'ChngInOpnIntrst',
                             'TtlTrfVal', 'TtlNbOfTxsExctd', 'SsnId', 'NewBrdLotQty', 'Rmks', 'Rsvd1',
                             'Rsvd2', 'Rsvd3', 'Rsvd4']
        df = df.drop(columns=columns_to_remove, errors='ignore')

        # Filter rows based on SERIES column
        df = df[df['SctySrs'].isin(['EQ', 'BE', 'BZ'])]

        # Convert the 'TradDt' column to datetime by inferring the format
        df['TradDt'] = pd.to_datetime(df['TradDt'], errors='coerce')

        # Format 'TradDt' as YYYYMMDD
        df['TradDt'] = df['TradDt'].dt.strftime('%Y%m%d')

        # Reorder columns, placing 'TradDt' before 'OpnPric'
        cols = df.columns.tolist()
        cols.remove('TradDt')
        cols.insert(cols.index('OpnPric'), 'TradDt')
        df = df[cols]

        # Remove the SctySrs column
        df = df.drop(columns=['SctySrs'], errors='ignore')

        # Sort by 'TckrSymb'
        df = df.sort_values(by='TckrSymb')
        
        required_columns = {
            "TckrSymb": "SYMBOL",
            "TradDt": "TIMESTAMP",
            "OpnPric": "OPEN",
            "HghPric": "HIGH",
            "LwPric": "LOW",
            "ClsPric": "CLOSE",
            "TtlTradgVol": "VOLUME"
        }
        
        df = df[list(required_columns.keys())].rename(columns=required_columns)

        # Save the modified DataFrame back to the same file
        df.to_csv(file_path, index=False, header=True)

        print(f"{os.path.basename(file_path)}: Eq_Bhavcopy Data Structure converted.")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error processing the file: {e}")

def download_and_process_equity_bhavcopy(date_str, output_path = "data"):
    """
    Main function to download, rename, and process an NSE Bhavcopy file for a given date.
    """
    try:
        # Construct the URL for downloading the file
        NSE_Bhavcopy_URL = f"https://archives.nseindia.com/content/cm/BhavCopy_NSE_CM_0_0_0_{date_str}_F_0000.csv.zip"
        print(f"Downloading from: {NSE_Bhavcopy_URL}")

        # Download and extract the Bhavcopy file
        extracted_file_path = Download_And_Extract_NSE_Bhavcopy_File(NSE_Bhavcopy_URL,output_path)
        if not extracted_file_path:
            raise Exception(f"Failed to extract file for {date_str}")

        # Parse the date_str into a datetime object
        date_obj = datetime.strptime(date_str, "%Y%m%d")

        # Rename the extracted file
        renamed_file_path = Rename_NSE_Bhavcopy_File(extracted_file_path, date_obj, output_path)
        if not renamed_file_path:
            raise Exception(f"Failed to rename file for {date_str}")

        # Modify the renamed file
        Modify_NSE_Bhavcopy_File(renamed_file_path)

        print(f"Processed file saved at: {renamed_file_path}")
    except Exception as e:
        print(f"Error processing the file for {date_str}: {e}")

# if __name__ == "__main__":
#     # Example usage: specify a date to process
#     process_date = "20240822"  # Date format: YYYYMMDD
#     # Directory to save the final output file
#     output_path = "output_test2/"
#     download_and_process_equity_bhavcopy(process_date,output_path)

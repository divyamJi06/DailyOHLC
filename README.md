# Historical OHLC Data for NSE Listed Stocks

This repository contains historical OHLC (Open, High, Low, Close) data for stocks listed on the National Stock Exchange (NSE) of India. The data spans from January 1, 2016, and is continuously updated daily with new entries.

## Repository Structure

The data is organized into two formats: CSV and JSON. 

1. **CSV Files**: Historical OHLC data was initially stored in CSV files, organized by year, month, and day. Each CSV file contains OHLC data for multiple stocks on a specific date.
2. **JSON Files**: Data for each individual stock is now stored in JSON format. Each stock symbol has a dedicated JSON file containing daily OHLC data for that stock.

### Folder Structure Explained:

- **data Folder**: Contains the historical OHLC data for multiple stocks. Inside the `data` folder:
  - **CSV Files**: The data for each day is stored in CSV files under year/month/day folders. For example, `data/2024/11/26/01.csv` would represent the CSV file for 1st November 26, 2024.
  
- **individual_stock_ohlc_data Folder**: Contains JSON files for each individual stock symbol (NSE code).
  - Each stock has a dedicated JSON file named after its NSE code (e.g., `TCS.json` for Tata Consultancy Services), containing daily OHLC data for that stock.

---

### Folder Structure Example:

```
data/                       # Folder containing historical OHLC data in CSV format
├── 2024/
│   └── 11/
│       └── 26/
│           └── 01.csv    # CSV file for 1st November 26, 2024
│           └── 02.csv    # CSV file for 2nd November 26, 2024
individual_stock_ohlc_data/  # Folder containing individual stock JSON files
├── TCS.json               # JSON file for Tata Consultancy Services (TCS)
├── INFY.json              # JSON file for Infosys (INFY)
└── RELIANCE.json          # JSON file for Reliance Industries (RELIANCE)
```

---

## Data Format

### 1. **CSV Format (Historical Data Before JSON Conversion)**

Each CSV file contains data with the following columns:

- **Symbol**: The ticker symbol of the stock.
- **Timestamp**: The date of the data entry (in YYYYMMDD format).
- **Open**: The opening price of the stock on that day.
- **High**: The highest price of the stock on that day.
- **Low**: The lowest price of the stock on that day.
- **Close**: The closing price of the stock on that day.
- **Volume**: The trading volume of the stock on that day.

Example of a CSV file:

```csv
Symbol,Timestamp,Open,High,Low,Close,Volume
TCS,20160101,2300,2345,2295,2320,50000
INFY,20160101,1150,1180,1145,1165,30000
```

### 2. **JSON Format (Current Data)**

Each stock has its own JSON file that stores the OHLC data. The file contains an array of objects, each representing a day's data for the stock. Each object has the following fields:

- **open**: The opening price of the stock on that day.
- **high**: The highest price of the stock on that day.
- **low**: The lowest price of the stock on that day.
- **close**: The closing price of the stock on that day.
- **date**: The date of the data entry, represented as a Unix timestamp.
- **volume**: The trading volume of the stock on that day.

Example of a JSON file for `TCS`:

```json
[
    {
        "open": 29.55,
        "high": 31.0,
        "low": 29.55,
        "close": 31.0,
        "date": 1634841000,
        "volume": 96393
    },
    {
        "open": 32.55,
        "high": 32.55,
        "low": 32.55,
        "close": 32.55,
        "date": 1635100200,
        "volume": 94036
    }
]
```

### Example File Name:
- **TCS.json**: This file contains the OHLC data for the stock symbol `TCS` (Tata Consultancy Services).

### Data Timeline:
- The data starts from January 1, 2016, and includes daily updates for each stock symbol. The CSV files represent earlier data, and the JSON files represent the current, individual stock data from the year 2016 onward.

---

## How to Use the Data

1. **Accessing OHLC Data for a Stock:**
   - To retrieve OHLC data for a specific stock, navigate to the corresponding JSON file using the stock's NSE symbol. For example, `TCS.json` for Tata Consultancy Services.

2. **Working with JSON Data:**
   - Each stock’s JSON file can be read using standard JSON libraries in most programming languages. You can load the data and process it as needed for analysis or visualization.

---

## Example: Accessing Data with Python

To access and manipulate the OHLC data for a stock (e.g., `TCS`), you can use the following Python code:

```python
import json

# Load the data from the JSON file
with open('individual_stock_ohlc_data/TCS.json', 'r') as file:
    data = json.load(file)

# Example: Print the closing price of the first entry
print("First entry closing price:", data[0]["close"])
```

---

## Updating the Data

The data is updated daily. Each new day’s data is appended to the respective stock's JSON file. You can automate this process using scripts to download and append the latest data.

---

## Contributing

If you would like to contribute to this dataset by adding more stock symbols or updating the data, feel free to submit a pull request.

---
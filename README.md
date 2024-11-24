# Historical OHLC Data for NSE Listed Stocks

This repository contains historical OHLC (Open, High, Low, Close) data for stocks listed on the National Stock Exchange (NSE) of India. The data spans from the year 2016 and is continuously updated every day with new entries.

## Repository Structure

The data is organized into folders by year, and within each year, the data is further divided by month and day. The folder structure is as follows:


### Folder Structure Explained:
- **Year Folder**: Represents the data for a specific year (e.g., `2016`, `2017`).
- **Month Folder**: Each year is divided into 12 month folders (`01` for January, `02` for February, etc.).
- **Day CSV**: Each day of the month is represented by a CSV file named by the day number (e.g., `01.csv` for the first day of the month, `02.csv` for the second day, etc.).

## Data Format

Each CSV file contains the following columns:
- **Symbol**: The ticker symbol of the stock.
- **Timestamp**: The date of the data entry.
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

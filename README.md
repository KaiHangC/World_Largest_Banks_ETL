# World_Largest_Banks_ETL
This project is part of Python Project for Data Engineering Lecture from IBM Data Engineer Certification

# Project Scenario:
I have been hired as a data engineer by research organization.The boss has asked you to a code that can be used to compile the list of the top 10 largest banks in the world ranked by market capitalization in billion USD. Further, the data needs to be transformed and stored in GBP, EUR and INR as well, in accordance with the exchange rate information that has been made available to you as a CSV file. The processed information table is to be saved locally in a CSV format and as a database table.

My job is to create an automated system to generate this information so that the same can be executed in every financial quarter to prepare the report.

# Features
- Web scraping of bank data from Wikipedia
- Currency conversion using exchange rates from a CSV file
- Data logging throughout the ETL process
- Output to CSV file
- Storage in SQLite database
- Example SQL queries to demonstrate data access

# Requirements
- Python 3.x
- Required Python packages:
  - BeautifulSoup4
  - requests
  - pandas
  - numpy
  - sqlite3
 
# Installation
1. Clone this repository
2. Install the required packages:
```
pip install beautifulsoup4 requests pandas numpy
```

# Usage
1. Ensure you have the exchange_rate.csv file in your working directory
2. Run the Python script:
```
python bank_project.py
```

# Output Files
The SQLite database contains one table:
- Largest_banks with columns:
  - Name: Bank name
  - MC_USD_Billion: Market capitalization in USD (billions)
  - MC_GBP_Billion: Market capitalization in GBP (billions)
  - MC_EUR_Billion: Market capitalization in EUR (billions)
  - MC_INR_Billion: Market capitalization in INR (billions)

# Example Queries
The script includes three example queries:
1. Select all data from the table
2. Calculate the average market cap in GBP
3. Select names of the top 5 banks

# Code for ETL operations on Country-GDP data
# Importing the required libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime 

def log_progress(message):
    ''' This function logs the mentioned message of a given stage of the
    code execution to a log file. Function returns nothing'''
    timestamp_format = '%Y-%h-%d-%H:%M:%S' # Year-Monthname-Day-Hour-Minute-Second 
    now = datetime.now() # get current timestamp 
    timestamp = now.strftime(timestamp_format) 
    with open("./code_log.txt","a") as f: 
        f.write(timestamp + ' : ' + message + '\n') 

def extract(url,table_attribs):
    ''' This function aims to extract the required
    information from the website and save it to a data frame. The
    function returns the data frame for further processing. '''
    page = requests.get(url).text
    data = BeautifulSoup(page,'html.parser')
    df = pd.DataFrame(columns=table_attribs)

    tables = data.find_all('tbody')
    rows = tables[0].find_all('tr')

    for row in rows:
        col = row.find_all('td')
        if len(col) != 0:
            Name = col[-2].get_text(strip=True)
            MC_USD_Billion = float(col[-1].get_text(strip=True))
            
            data = pd.DataFrame({
                "Name": [Name],
                "MC_USD_Billion": [MC_USD_Billion]
            })

            df = pd.concat([df, data], ignore_index=True)

    return df

def transform(df, csv_path):
    ''' This function accesses the CSV file for exchange rate
    information, and adds three columns to the data frame, each
    containing the transformed version of Market Cap column to
    respective currencies'''
    exchange_rate = pd.read_csv(csv_path)

    # Create dictionary of exchange rates
    exchange_dict = exchange_rate.set_index('Currency').to_dict()['Rate']

    # Add new columns with converted values
    df['MC_GBP_Billion'] = [np.round(x * exchange_dict['GBP'], 2) for x in df['MC_USD_Billion']]
    df['MC_EUR_Billion'] = [np.round(x * exchange_dict['EUR'], 2) for x in df['MC_USD_Billion']]
    df['MC_INR_Billion'] = [np.round(x * exchange_dict['INR'], 2) for x in df['MC_USD_Billion']]
    
    return df

def load_to_csv(df, output_path):
    ''' This function saves the final data frame as a CSV file in
    the provided path. Function returns nothing.'''
    df.to_csv(output_path)

def load_to_db(df, sql_connection, table_name):
    ''' This function saves the final data frame to a database
    table with the provided name. Function returns nothing.'''
    df.to_sql(table_name, sql_connection, if_exists='replace', index=False)

def run_query(query_statement, sql_connection):
    ''' This function runs the query on the database table and
    prints the output on the terminal. Function returns nothing. '''
    ''' Here, you define the required entities and call the relevant
    functions in the correct order to complete the project. Note that this
    portion is not inside any function.'''
    print(query_statement)
    query_output = pd.read_sql(query_statement, sql_connection)
    print(query_output)

url = 'https://web.archive.org/web/20230908091635 /https://en.wikipedia.org/wiki/List_of_largest_banks'
table_attribs = ['Name', 'MC_USD_Billion']
db_name = 'Banks.db'
table_name = 'Largest_banks'
csv_path = 'exchange_rate.csv'
output_path = '././Largest_banks_data.csv'

log_progress('Preliminaries complete. Initiating ETL process')

df = extract(url,table_attribs)
log_progress('Data extraction complete. Initiating Transformation process')

df = transform(df,csv_path)
log_progress('Data transformation complete. Initiating loading process')

load_to_csv(df, output_path)
log_progress('Data saved to CSV file')

sql_connection = sqlite3.connect(db_name)
log_progress('SQL Connection initiated.')

load_to_db(df, sql_connection, table_name)
log_progress('Data loaded to Database as table. Running the query')

query_statement = "SELECT * FROM Largest_banks"
run_query(query_statement, sql_connection)

query_statement = "SELECT AVG(MC_GBP_Billion) FROM Largest_banks"
run_query(query_statement, sql_connection)

query_statement = "SELECT Name from Largest_banks LIMIT 5"
run_query(query_statement, sql_connection)

log_progress('Process Complete.')
sql_connection.close()
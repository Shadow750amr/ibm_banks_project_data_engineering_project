from datetime import datetime
from bs4 import BeautifulSoup
import requests
from typing import Optional
import pandas as pd

# Code for ETL operations on Country-GDP data

# Importing the required libraries

def log_progress(message):
    ''' This function logs the mentioned message of a given stage of the
    code execution to a log file. Function returns nothing'''
    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
    print(f'{formatted_date,message}')
    return None

def extract(url,table_attribs):  
    ''' This function aims to extract the required
    information from the website and save it to a data frame. The
    function returns the data frame for further processing. '''
    
    log_progress("Preliminaries complete. Initiating ETL process")
    response = requests.get(url)
    soup = BeautifulSoup(response.content,'html.parser')
    lista = []
    for table in soup.find_all('table'):
        headers = [th.text.strip() for th in table.find_all('th')]
        if table_attribs in headers:
            headers = headers
            for row in table.find_all('tr'):
                data = [td.text.strip() for td in row.find_all('td')]
                lista.append(data)
    df = pd.DataFrame(lista,columns=headers)
    df.rename(columns={"Number":"MC_USD_Billion"},inplace=True)
    df.to_csv('final.csv')

    return df

    log_progress('Data extraction complete. Initiating Transformation process')
    
    

def transform(df, csv_path):
    ''' This function accesses the CSV file for exchange rate
	information, and adds three columns to the data frame, each
	containing the transformed version of Market Cap column to
	respective currencies'''




    log_progress('Data transformation complete. Initiating Loading process')
    return df

def load_to_csv(df, output_path):
    ''' This function saves the final data frame as a CSV file in
	the provided path. Function returns nothing.'''


    log_progress('Data saved to CSV file')

def load_to_db(df, sql_connection, table_name):
    ''' This function saves the final data frame to a database
	table with the provided name. Function returns nothing.'''

    log_progress('SQL Connection initiated')
    log_progress('Data loaded to Database as a table, Executing queries')
    log_progress('Data loaded to Database as a table, Executing queries')
    
    


def run_query(query_statement, sql_connection):
    ''' This function runs the query on the database table and
    prints the output on the terminal. Function returns nothing. '''


log_progress('Process Complete')
log_progress('Server Connection closed')


''' Here, you define the required entities and call the relevant
functions in the correct order to complete the project. Note that this
portion is not inside any function.'''



if __name__ =="__main__":
    url = 'https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks'
    extract(url,'Market cap(US$ billion)')

    
from datetime import datetime
from bs4 import BeautifulSoup
import requests
from typing import Optional
import pandas as pd
import sqlite3
import numpy as np

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
        if "Market cap(US$ billion)" in headers:
            for row in table.find_all('tr'):
                data = [td.text.strip() for td in row.find_all('td')]
                lista.append(data)
    df = pd.DataFrame(lista,columns=headers)
    df.rename(columns=table_attribs,inplace=True)
    df.to_csv('final.csv')

    return df

    log_progress('Data extraction complete. Initiating Transformation process')
    
    

def transform(df, csv_path):
    ''' This function accesses the CSV file for exchange rate
	information, and adds three columns to the data frame, each
	containing the transformed version of Market Cap column to
	respective currencies'''

    df_path = pd.read_csv(df)
    exchange_rate_csv = pd.read_csv(csv_path)
    exchange_rate = exchange_rate_csv.set_index('Currency').to_dict()['Rate']
    
    gbp_rate = float(exchange_rate['GBP'])
    df_path['MC_GBP_Billion'] = [np.round(x * gbp_rate, 2) for x in df_path['MC_USD_Billion']]
    eur_rate = float(exchange_rate['EUR'])
    df_path['MC_EUR_Billion'] = [np.round(x * eur_rate, 2) for x in df_path['MC_USD_Billion']]
    inr_rate = float(exchange_rate['INR'])
    df_path['MC_INR_Billion'] = [np.round(x * inr_rate, 2) for x in df_path['MC_USD_Billion']]

    log_progress('Data transformation complete. Initiating Loading process')
    return df_path

def load_to_csv(df, output_path):
    ''' This function saves the final data frame as a CSV file in
	the provided path. Function returns nothing.'''
    df_path = pd.read_csv(df)
    df_path.to_csv(output_path)

    log_progress('Data saved to CSV file')

def load_to_db(df, sql_connection, table_name):
    ''' This function saves the final data frame to a database
	table with the provided name. Function returns nothing.'''
    df_to_upload = pd.read_csv(df)
    conn = sqlite3.connect(sql_connection)
    log_progress('SQL Connection initiated')
    df_to_upload.to_sql(table_name,conn)
    log_progress('Data loaded to Database as a table, Executing queries')
    conn.close()

def run_query(query_statement, sql_connection):
    ''' This function runs the query on the database table and
    prints the output on the terminal. Function returns nothing. '''
    conn = sqlite3.connect(sql_connection)
    cursor = conn.cursor()
    cursor.execute(query_statement)
    cursor.close()

    conn.close()


    log_progress('Process Complete')

    log_progress('Server Connection closed')


    ''' Here, you define the required entities and call the relevant
    functions in the correct order to complete the project. Note that this
    portion is not inside any function.'''



if __name__ =="__main__":
    url = 'https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks'
    table_attribs = {"Country":"Name","Number":"MC_USD_Billion"}
    extract(url,table_attribs)
    transform('final.csv','exchange_rate.csv')
    load_to_csv('final.csv','final_final.csv')
    load_to_db('final_final.csv','Banks.db','Largest_banks')
    run_query('SELECT AVG(MC_GBP_Billion) FROM Largest_banks','Banks.db')


    #cursor.execute('SELECT AVG(MC_GBP_Billion) FROM Largest_banks')
    #cursor.execute('SELECT Bank name from Largest_banks LIMIT 5')
    #cursor.execute('SELECT * FROM Largest_banks')
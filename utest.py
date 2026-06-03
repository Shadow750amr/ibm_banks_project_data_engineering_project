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

def extract(url):  #table_attribs
    ''' This function aims to extract the required
    information from the website and save it to a data frame. The
    function returns the data frame for further processing. '''
    
    log_progress("Preliminaries complete. Initiating ETL process")
    response = requests.get(url)
    soup = BeautifulSoup(response.content,'html.parser')
    lista = []
    table_attribs = ["Market cap(US$ billion)"]

    for table in soup.find_all('table'):
        headers = [th.text.split() for th in table.find_all('th')]
        print(headers)


    log_progress('Data extraction complete. Initiating Transformation process')
    
    

if __name__ =="__main__":
    url = 'https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks'
    
    extract(url,)

    
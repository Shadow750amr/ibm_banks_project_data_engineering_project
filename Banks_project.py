from datetime import datetime
from bs4 import BeautifulSoup
import requests
import pandas as pd
import sqlite3
import numpy as np

url = 'https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks'
csv_url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-PY0221EN-Coursera/labs/v2/exchange_rate.csv'
table_attribs = ["Name", "MC_USD_Billion"]
output_csv_path = './Largest_banks_data.csv'
db_name = 'Banks.db'
table_name = 'Largest_banks'
log_file = 'code_log.txt'

def log_progress(message):
    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f'[{formatted_date}] : {message}\n'
    print(log_entry.strip())
    with open(log_file, "a") as f:
        f.write(log_entry)

def extract(url, table_attribs):  
    log_progress("Preliminaries complete. Initiating ETL process")
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    lista = []
    
    for table in soup.find_all('table'):
        rows = table.find_all('tr')
        if len(rows) > 0:
            first_row = rows[0].text.strip()
            if "Market cap" in first_row or "Bank name" in first_row:
                for row in rows[1:]:
                    tds = row.find_all('td')
                    if len(tds) >= 3:
                        bank_name = tds[1].text.strip()
                        market_cap = tds[2].text.strip()
                        lista.append([bank_name, market_cap])
                break

    df = pd.DataFrame(lista, columns=table_attribs)
    df['MC_USD_Billion'] = df['MC_USD_Billion'].str.replace('\n', '').str.replace(',', '').astype(float)
    df = df.head(10)

    log_progress('Data extraction complete. Initiating Transformation process')
    return df

def transform(df, csv_path):
    exchange_rate_csv = pd.read_csv(csv_path)
    exchange_rate = exchange_rate_csv.set_index('Currency').to_dict()['Rate']
    
    gbp_rate = float(exchange_rate['GBP'])
    eur_rate = float(exchange_rate['EUR'])
    inr_rate = float(exchange_rate['INR'])
    
    df['MC_GBP_Billion'] = np.round(df['MC_USD_Billion'] * gbp_rate, 2)
    df['MC_EUR_Billion'] = np.round(df['MC_USD_Billion'] * eur_rate, 2)
    df['MC_INR_Billion'] = np.round(df['MC_USD_Billion'] * inr_rate, 2)

    log_progress('Data transformation complete. Initiating Loading process')
    return df

def load_to_csv(df, output_path):
    df.to_csv(output_path, index=False)
    log_progress(f'Data saved to CSV file')

def load_to_db(df, sql_connection, table_name):
    conn = sqlite3.connect(sql_connection)
    log_progress('SQL Connection initiated')
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    log_progress('Data loaded to Database as a table, Executing queries')
    conn.close()

def run_query(query_statement, sql_connection):
    conn = sqlite3.connect(sql_connection)
    cursor = conn.cursor()
    cursor.execute(query_statement)
    results = cursor.fetchall()
    print(f"\n--- Ejecutando Query: {query_statement} ---")
    for row in results:
        print(row)
    print("------------------------------------------------\n")
    cursor.close()
    conn.close()
    log_progress('Process Complete')

if __name__ == "__main__":
    df_extracted = extract(url, table_attribs)
    df_transformed = transform(df_extracted, csv_url)
    
    load_to_csv(df_transformed, output_csv_path)
    load_to_db(df_transformed, db_name, table_name)
    
    run_query("SELECT * FROM Largest_banks", db_name)
    run_query("SELECT AVG(MC_GBP_Billion) FROM Largest_banks", db_name)
    run_query("SELECT Name FROM Largest_banks LIMIT 5", db_name)
    
    log_progress('Server Connection closed')
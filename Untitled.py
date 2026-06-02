import requests 
from bs4 import BeautifulSoup


url = 'https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks'

response = requests.get(url)

soup = BeautifulSoup(response.text,'html.parser')

lista = []

for table in soup.find_all('table'):
    headers = [th.text.strip() for th in table.find_all('th')]
    if 'Market cap(US$ billion)' in headers:
        for row in soup.find_all('tr'):
            data = [td.text.strip() for td in soup.find_all('td')]
            final_list = lista.append(data)
            

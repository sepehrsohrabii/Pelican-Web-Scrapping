# web scrapping for vitalmedicalsupplies.com.au products to list Pelican products
import pandas as pd
import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import json

df = pd.read_excel('data.xlsx', index_col=0)
SKU_list = df['SKU'].tolist()

# https://www.vitalmedicalsupplies.com.au/api/product/search?page=1&pageSize=16&searchPhrase=516&brands=1073745934
soup_json_list = []

for SKU in SKU_list:
    process_percentage = ((SKU_list.index(SKU))/len(SKU_list)) * 100
    print(process_percentage)
    if SKU != '':
        url = f'https://www.vitalmedicalsupplies.com.au/api/product/search?page=1&pageSize=16&searchPhrase={SKU}&brands=1073745934'
        response = requests.get(url, headers=Headers(headers=True).generate())

        soup = BeautifulSoup(response.text, 'html.parser')
        soup_json = json.loads(soup.text)
        if len(soup_json['products']) != 0:
            for item in soup_json['products']:
                soup_json_list.append(item)

with open('data.json', 'w') as f:
    for item in soup_json_list:
        json.dump(item, f)
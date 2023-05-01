# web scrapping for thinkmobility.com.au products to list Pelican products
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from fake_headers import Headers
import json

URL = "https://thinkmobility.com.au/search?q=&type=product&_=pf&pf_t_brand=brand%3APelican"
browser = webdriver.Chrome('/home/sepehr/Desktop/Moin/Pelican/chromedriver')
browser.get(URL)
html = browser.page_source
soup = BeautifulSoup(html, "html.parser")
products = soup.findAll('a', attrs={"class": "gschecked"})

print(len(products))

product_tags = []
for item in products:
    product_href = item['href']
    product_tag = product_href.split('/').pop()
    product_tags.append(product_tag)

product_tags = list(dict.fromkeys(product_tags))

# https://thinkmobility.com.au/products/bed-rail-protector-heat-sealed-n-pair-214hs.json
soup_json_list = []
for item in product_tags:
    link = f'https://thinkmobility.com.au/products/{item}.json'
    response = requests.get(link)
    print(link)
    try:
        print(response.text)
        soup_json = json.loads(response.text)
        soup_json_list.append(soup_json)
    except:
        pass
with open('thinkmobility-data.json', 'w') as f:
    for item in soup_json_list:
       json.dump(item, f)
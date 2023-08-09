import os
from time import sleep
import csv
from bs4 import BeautifulSoup
import requests

tab_lv01_brands = os.getcwd() + '\FICHACOMPLETA_TAB_LV01_BRANDS.csv'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
}

url = 'https://www.fichacompleta.com.br/carros/marcas/'
r = requests.get(url=url)
sleep(2)

print(f'Status: {r.status_code}')


soup = BeautifulSoup(r.content, 'html.parser')
info01 = soup.find_all('div', {'class': 'col-md-2 col-md-offset-1'})

brands = []
links = []

for el in info01:
    brands.append(el.a.get_text().strip())
    links.append(f'https://www.fichacompleta.com.br{el.a["href"]}')
    #print(f'{el.a.get_text().strip()} {el.a["href"]}')

for i, b in enumerate(brands):
    with open(tab_lv01_brands, 'a', newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([b, links[i], 'False'])
        csvfile.close()

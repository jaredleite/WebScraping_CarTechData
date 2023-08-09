import os
from time import sleep
import random
import csv
from bs4 import BeautifulSoup
import requests
import pandas as pd

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
}

tab_lv01_brands = os.getcwd() + '\FICHACOMPLETA_TAB_LV01_BRANDS.csv'
tab_lv02_familys = os.getcwd() + '\FICHACOMPLETA_TAB_LV02_FAMILYS.csv'

df1 = pd.read_csv(tab_lv01_brands, encoding='utf-8')
df2 = pd.read_csv(tab_lv02_familys, encoding='utf-8')

df = df1

# only false flag_download rows
df_temp = df[[not elem for elem in df['download_flag']]]

list_search = [i for i in df_temp.index]
random.shuffle(list_search)

while list_search != []:
    index = list_search.pop()
    brand = df.loc[index, 'Brands']
    link = df.loc[index, 'Link']
    print(brand)
    r = requests.get(url=link)
    sleep(2)
    print(f'Status: {r.status_code}')

    soup = BeautifulSoup(r.content, 'html.parser')
    info01 = soup.find_all(
        'div', {'class': 'col-xs-5 col-xs-offset-1 col-sm-3'})

    for el in info01:
        with open(tab_lv02_familys, 'a', newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            family = el.a.get_text().strip()
            family_link = f'https://www.fichacompleta.com.br{el.a["href"]}'
            writer.writerow([brand, family, family_link, 'False'])
            csvfile.close()

        #print(f'{el.a.get_text().strip()} {el.a["href"]}')

    df.loc[index, 'download_flag'] = True
    df.to_csv(tab_lv01_brands, index=False, encoding='utf-8')
    sleep(30)

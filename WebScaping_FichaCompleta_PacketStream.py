import os
from time import sleep
import random
import csv
from bs4 import BeautifulSoup
import requests
import pandas as pd
from MyKeys import My_Keys  # My own keys

# My own keys
my_keys = My_Keys()


# use youur keys here
http_proxy = my_keys.PacketStream_2
https_proxy = my_keys.PacketStream_2

proxyDict = {
    "http": http_proxy,
    "https": https_proxy,
}


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
}

tab_lv01_brands = os.getcwd() + '\FICHACOMPLETA_TAB_LV01_BRANDS.csv'
tab_lv02_familys = os.getcwd() + '\FICHACOMPLETA_TAB_LV02_FAMILYS.csv'
tab_lv03_04_years_models = os.getcwd() + '\FICHACOMPLETA_TAB_LV03_04_YEARS_MODELS.csv'
tab_lv05_infos = os.getcwd() + '\FICHACOMPLETA_TAB_INFOS.csv'


df1 = pd.read_csv(tab_lv01_brands, encoding='utf-8')
df2 = pd.read_csv(tab_lv02_familys, encoding='utf-8')
df3 = pd.read_csv(tab_lv03_04_years_models, encoding='utf-8')
df5 = pd.read_csv(tab_lv05_infos, encoding='utf-8')

df = df3

# only false flag_download rows
df_temp = df[[not elem for elem in df['download_flag']]]

list_search = [i for i in df_temp.index]
random.shuffle(list_search)
info01 = []
tech_info = []
equipment_info = []

while list_search != []:

    try:
        info01 = []
        info02 = []
        tech_info = []
        equipment_info = []
        remaining_links = len(list_search)
        print(f'Remaining links: {remaining_links}')

        index = list_search.pop()
        brand = df.loc[index, 'Brands']
        link = df.loc[index, 'Link']
        family = df.loc[index, 'Familys']
        year = df.loc[index, 'Years']
        model = df.loc[index, 'Models']
        print(brand, family, year, model)

        r = requests.get(url=link, proxies=proxyDict)
        sleep(2)
        print(f'Status: {r.status_code}')
        soup = BeautifulSoup(r.content, 'html.parser')

        info01 = soup.find_all('div', {'class': 'colEsq'})
        info02 = soup.find_all('div', {'class': 'colDir'})

        for i, el in enumerate(info01):
            line = f'{el.get_text().strip()}{info02[i].get_text().strip()}'
            tech_info.append(line)
            # print(line)
            # sleep(10)
        # /html/body/div[1]/div[1]/div/div[2]/div[1]

        info3 = soup.find_all('span')

        for el in info3:
            try:
                if el.i != None:
                    equipment = el.get_text().strip()
                    equipment_info.append(equipment)
                    # print(equipment)
            except:
                pass
        '''
        soup = BeautifulSoup(r.content, 'html.parser')
        info01 = soup.find_all(
            'div', {'class': 'col-xs-12 col-xs-offset-1 col-sm-offset-0 col-sm-4'})

        # print(f'info: {info01}')
        for el in info01:
            text = el.a.get_text().strip()
            len_text = len(text)
            # print('Teste')
            # print(el)
            # print(f'Texto:{text}, tamanho:{len_text}')
        '''
        if info01 != []:
            with open(tab_lv05_infos, 'a', newline='', encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(
                    [brand, family, year, model, ';'.join(tech_info), ';'.join(equipment_info)])
                csvfile.close()

        if info01 != []:
            df.loc[index, 'download_flag'] = True
            df.to_csv(tab_lv03_04_years_models, index=False, encoding='utf-8')

    except:
        pass
    sleep(3)

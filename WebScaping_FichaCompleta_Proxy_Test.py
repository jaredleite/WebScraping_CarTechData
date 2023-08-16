import os
from time import sleep
import random
#import csv
from bs4 import BeautifulSoup
import requests
import pandas as pd

proxyDict = {
    "http": 1,
    "https": 1,
}


def WebScraping(proxy):
    global proxyDict
    proxyDict["http"] = proxy
    proxyDict["https"] = proxy

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

    if list_search != []:

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

            if proxy == '':
                print('sem proxy')
                r = requests.get(url=link, headers=headers, timeout=3)
            else:
                print(f'com proxy {proxy}')
                r = requests.get(url=link, proxies=proxyDict, headers=headers, timeout=3)
            sleep(2)

            result = r.status_code
            print(f'IP: {proxy}, Status: {result}')
            soup = BeautifulSoup(r.content, 'html.parser')

            info01 = soup.find_all('div', {'class': 'colEsq'})
            info02 = soup.find_all('div', {'class': 'colDir'})

            for i, el in enumerate(info01):
                line = f'{el.get_text().strip()}{info02[i].get_text().strip()}'
                tech_info.append(line)

            info3 = soup.find_all('span')

            for el in info3:
                try:
                    if el.i != None:
                        equipment = el.get_text().strip()
                        equipment_info.append(equipment)
                        # print(equipment)
                except:
                    pass

            if info01 == []:
                list_search.append(index)
                result = -1

            '''
            if info01 != []:
                with open(tab_lv05_infos, 'a', newline='', encoding="utf-8") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(
                        [brand, family, year, model, ';'.join(tech_info), ';'.join(equipment_info)])
                    csvfile.close()
            else:
                list_search.append(index)
                r = -1

            if info01 != []:
                df.loc[index, 'download_flag'] = True
                df.to_csv(tab_lv03_04_years_models,
                          index=False, encoding='utf-8')
        '''
        except:
            r = -1
            print('caiu no except')
        # sleep(3)

    else:
        print('Finished')

    return result

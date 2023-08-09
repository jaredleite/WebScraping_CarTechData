import os
import pandas as pd
import random
import csv
from time import sleep

from bs4 import BeautifulSoup
import requests
from MyKeys import My_Keys  # My own keys

# My own keys
my_keys = My_Keys()


# use youur keys here
http_proxy = my_keys.PacketStream
https_proxy = my_keys.PacketStream

proxyDict = {
    "http": http_proxy,
    "https": https_proxy,
}

# update frequently
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}

# test link lists length
tab_lv01_brands = os.getcwd() + '\CARROSWEB_TAB_LV01_BRANDS.csv'
tab_lv02_familys = os.getcwd() + '\CARROSWEB_TAB_LV02_FAMILY.csv'
tab_lv03_years = os.getcwd() + '\CARROSWEB_TAB_LV03_YEARS.csv'
tab_lv04_models = os.getcwd() + '\CARROSWEB_TAB_LV04_MODELS.csv'

df1 = pd.read_csv(tab_lv01_brands, encoding='utf-8')
df2 = pd.read_csv(tab_lv02_familys, encoding='utf-8')
df3 = pd.read_csv(tab_lv03_years, encoding='utf-8')
df3 = df3.loc[df3['Familys'] != 'Todos']
df3 = df3.loc[df3['Years'] != 'Todos']

df2_temp = df2.groupby(['Brands', 'Familys'])['Familys'].count()
df3_temp = df3.groupby(['Brands', 'Familys'])['Familys'].count()

len_tb_LV02 = len(df2_temp)
qtd_familys_tb_LV03 = len(df3_temp)

print('Validação:')
if len_tb_LV02 == qtd_familys_tb_LV03:
    print('Ok')
else:
    print('Fail')
    print(f'Qtd Famílias Tabela LV02: {len_tb_LV02}')
    print(f'Qtd Famílias Tabela LV03: {qtd_familys_tb_LV03}')
    print('\n')


def Get_Texto_Link(table):
    """
    Get_Texto_Link
    """

    elements = table_Model.find_all('a')
    textos = []
    links = []

    global brand

    for element in elements:
        aux = f'{element.get("title")}'

        if aux.find(brand) != -1:
            aux = aux[(len(brand)+1):]

        textos.append(aux)
        links.append('https://www.carrosnaweb.com.br/' + element.get('href'))

    textos_final = []
    links_final = []

    for i, t in enumerate(textos):
        if t != '' and t != None and t != 'None':
            textos_final.append(t)
            links_final.append(links[i])

    return textos_final, links_final


df = df3

# only false flag_download rows
df_temp = df[[not elem for elem in df['download_flag']]]

list_search = [i for i in df_temp.index]
random.shuffle(list_search)


while list_search != []:
    index = list_search.pop()
    print(f'Faltam {len(list_search)} links\n')
    year = df.loc[index, 'Years']
    family = df.loc[index, 'Familys']
    brand = df.loc[index, 'Brands']
    link = df.loc[index, 'Link_Years']
    print(f'{brand} {family} {year}')

    flag_try = True

    while flag_try:
        try:
            r = requests.get(url=link, proxies=proxyDict, headers=headers)
            flag_try = False
        except:
            print("erro")
            flag_try = True

        sleep(2)

    sleep(2)
    soup = BeautifulSoup(r.content, 'html.parser')

    table_Model = soup.html.body.find_all('table')[2].find_all('tr')[
        2].find_all('td')[2]
    models, models_Link = Get_Texto_Link(table_Model)

    for i, m in enumerate(models):

        with open(tab_lv04_models, 'a', newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([brand, family, year, m, models_Link[i], 'False'])
            csvfile.close()

    df.loc[index, 'download_flag'] = True
    df.to_csv(tab_lv03_years, index=False, encoding='utf-8')
    sleep(2)

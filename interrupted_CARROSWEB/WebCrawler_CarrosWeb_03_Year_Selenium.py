import os
import pandas as pd
import random
import csv
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from Timer import Timer

tab_lv01_brands = os.getcwd() + '\CARROSWEB_TAB_LV01_BRANDS.csv'
tab_lv02_familys = os.getcwd() + '\CARROSWEB_TAB_LV02_FAMILY.csv'

df1 = pd.read_csv(tab_lv01_brands, encoding='utf-8')
df2 = pd.read_csv(tab_lv02_familys, encoding='utf-8')
df2 = df2.loc[df2['Familys'] != 'Todos']

len_tb_LV01 = len(df1["Brands"])
qtd_brands_tb_LV02 = len(df2["Brands"].unique())

print('Validação:')
if len_tb_LV01 == qtd_brands_tb_LV02:
    print('Ok')
else:
    print('Fail')
print(f'Tamanho Tabela LV01: {len_tb_LV01}')
print(f'Qtd Marcas Tabela LV02: {qtd_brands_tb_LV02}')
print('\n')

timer = Timer()

options = Options()
options.add_argument('window-size=400,800')
# options.add_argument('--headless')
navegador = webdriver.Chrome(options=options)

tab_lv03_years = os.getcwd() + '\CARROSWEB_TAB_LV03_YEARS.csv'


def Get_Texto_Link(table):
    """
    Get_Texto_Link
    """

    tables = table.find_elements(By.TAG_NAME, "table")
    textos = []
    links = []

    for tab in tables:
        for element in tab.find_elements(By.TAG_NAME, "a"):
            textos.append(element.text)
            links.append(element.get_attribute('href'))

    return textos, links


df = df2  # pd.read_csv(tab_lv02_familys, encoding='utf-8')

# only false flag_download rows
df_temp = df[[not elem for elem in df['download_flag']]]

list_search = [i for i in df_temp.index]
random.shuffle(list_search)

while list_search != []:
    index = list_search.pop()
    family = df.loc[index, 'Familys']
    brand = df.loc[index, 'Brands']
    link = df.loc[index, 'Link_Familys']
    print(family)

    navegador.get(link)
    sleep(5)
    table_Year = navegador.find_element(
        By.XPATH, '/html/body/table[3]/tbody/tr/td[1]/font/font/font/font/font/font/table')
    years, years_Link = Get_Texto_Link(table_Year)
    for i, y in enumerate(years):
        with open(tab_lv03_years, 'a', newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([brand, family, y, years_Link[i], 'False'])
            csvfile.close()

    df.loc[index, 'download_flag'] = True
    df.to_csv(tab_lv02_familys, index=False, encoding='utf-8')
    timer.take_a_break()

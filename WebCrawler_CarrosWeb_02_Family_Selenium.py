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

timer = Timer()

options = Options()
options.add_argument('window-size=400,800')
# options.add_argument('--headless')
navegador = webdriver.Chrome(options=options)

tab_lv01_brands = os.getcwd() + '\CARROSWEB_TAB_LV01_BRANDS.csv'
tab_lv02_familys = os.getcwd() + '\CARROSWEB_TAB_LV02_FAMILY.csv'


def Get_Texto_Link_Family(table):
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


df = pd.read_csv(tab_lv01_brands, encoding='utf-8')

# only false flag_download rows
df_temp = df[[not elem for elem in df['download_flag']]]

list_search = [i for i in df_temp.index]
random.shuffle(list_search)

while list_search != []:
    index = list_search.pop()
    brand = df.loc[index, 'Brands']
    link = df.loc[index, 'Link_Brands']
    print(brand)

    navegador.get(link)
    sleep(20)
    table_Family = navegador.find_element(
        By.XPATH, '/html/body/table[3]/tbody/tr/td[1]/font/font/font/font/font/table')
    familys, familys_Link = Get_Texto_Link_Family(table_Family)
    for i, fam in enumerate(familys):
        with open(tab_lv02_familys, 'a', newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([brand, fam, familys_Link[i], 'False'])
            csvfile.close()

    df.loc[index, 'download_flag'] = True
    df.to_csv(tab_lv01_brands, index=False, encoding='utf-8')
    timer.take_a_break()

import os
import pandas as pd
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
#from bs4 import BeautifulSoupq

tab_lv01_brands = os.getcwd() + '\CARROSWEB_TAB_LV01_BRANDS.csv'


options = Options()
options.add_argument('window-size=400,800')
options.add_argument('--headless')

navegador = webdriver.Chrome(options=options)
navegador.get('https://www.carrosnaweb.com.br/avancada.asp')
sleep(2)

table_Brand = navegador.find_element(
    By.XPATH, '//*[@id="form1"]/table[2]/tbody/tr[3]/td/table/tbody/tr[2]')


def Get_Texto_Link(table):
    """
    Get_Texto_Link
    """

    rows = table.find_elements(By.TAG_NAME, "tr")
    textos = []
    links = []

    for row in rows:
        for col in row.find_elements(By.TAG_NAME, "td"):
            for element in col.find_elements(By.TAG_NAME, "a"):
                textos.append(element.text)
                links.append(element.get_attribute('href'))

    return textos, links


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


brands, brands_Links = Get_Texto_Link_Family(table_Brand)

print(brands)
print(brands_Links)

df = pd.DataFrame(list(zip(brands, brands_Links)),
                  columns =['Brands', 'Link_Brands'])
df.to_csv(tab_lv01_brands, index=False, encoding='utf-8')

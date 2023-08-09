import os
from time import sleep
import random
import csv
from bs4 import BeautifulSoup
import requests
import pandas as pd
import string

""""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
"""

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
}

urls = [
    'https://www.carrosnaweb.com.br/fichadetalhe.asp?codigo=12397',
    'https://www.carrosnaweb.com.br/fichadetalhe.asp?codigo=7080',
    'https://www.carrosnaweb.com.br/fichadetalhe.asp?codigo=18535',
    'https://www.carrosnaweb.com.br/fichadetalhe.asp?codigo=4054',
    'https://www.carrosnaweb.com.br/fichadetalhe.asp?codigo=705',
    'https://www.carrosnaweb.com.br/fichadetalhe.asp?codigo=2967',
    'https://www.carrosnaweb.com.br/fichadetalhe.asp?codigo=13503',
    'https://www.carrosnaweb.com.br/fichadetalhe.asp?codigo=18514'
]
url = 'https://www.fichacompleta.com.br/carros/ford/focus-sedan-glx-1-6-16v-2010'
#url='https://www.fichacompleta.com.br/carros/ford/focus-sedan-glx-2-0-2009'
r = requests.get(url=url)
sleep(2)

print(f'Status: {r.status_code}')


soup = BeautifulSoup(r.content, 'html.parser')
# table_Infos = soup.html.body.find_all('div')[0].find_all('div')[0].find_all('div')[
#    0].find_all('div')[1]
info01 = soup.find_all('div', {'class': 'colEsq'})
info02 = soup.find_all('div', {'class': 'colDir'})

for i, el in enumerate(info01):
    print(f'{el.get_text().strip()}{info02[i].get_text().strip()}')
# /html/body/div[1]/div[1]/div/div[2]/div[1]

info3 = soup.find_all('span')

for el in info3:
    try:
        if el.i != None:
            print(el.get_text().strip())
    except:
        pass
'''for el in info3:
    try:
        if el.i['class'] == 'fa-li fa fa-check':
            print(el.get_text().strip())
    except:
        pass
'''

#    'table')[2]  # .find_all('tr')[0].table
#table_Infos = table_Model = soup.html.body

# print(table_Infos)


"""table_Infos = navegador.find_element(
    By.XPATH, '/html/body/table[3]/tbody/tr/td[1]/table/tbody')

table = table_Infos

rows = table.find_elements(By.TAG_NAME, "tr")

selector = 1

tipo_info_list = []
info_list = []
desc_list = []

tipo_info = ''
info = ''

tipo_equipamento_list = []
equipamento_list = []
status_equipamento_list = []

tipo_equipamento = ''
equipamento = ''
status_equipamento = ''


def get_geral_info(row):
    global tipo_info_list
    global info_list
    global desc_list

    global tipo_info
    global info

    global selector

    for col in row.find_elements(By.TAG_NAME, "td"):
        try:
            font = col.find_element(By.TAG_NAME, "font")
            size = font.get_attribute('size')
            text = col.text
            bgcolor = col.get_attribute("bgcolor")
        except:
            font = ''
            size = ''
            text = ''
            bgcolor = ''

        if size == '5' and text != '':
            if text.strip() == 'Equipamentos':
                selector = 2
                print(f'Selector: {selector}')
            if text.strip() == 'Fotos':
                selector = 3
                print(f'Selector: {selector}')

        if selector == 1:
            if size == '4' and text != '':
                tipo_info = text

            if size == '3' and text != '':
                if text == 'Ano':
                    tipo_info = 'GERAL'

                if bgcolor == '#ffffff':
                    info = text

                if bgcolor == '#efefef':
                    tipo_info_list.append(tipo_info)
                    info_list.append(info)
                    desc_list.append(text)
    return


def get_equipamentos(row):
    global tipo_equipamento_list
    global equipamento_list
    global status_equipamento_list

    global tipo_equipamento
    global equipamento
    global status_equipamento

    global selector

    for col in row.find_elements(By.TAG_NAME, "td"):
        try:
            font = col.find_element(By.TAG_NAME, "font")
            size = font.get_attribute('size')
            text = col.text
            bgcolor = col.get_attribute("bgcolor")
        except:
            font = ''
            size = ''
            text = ''
            bgcolor = ''

        if size == '5' and text != '':
            if text.strip() == 'Equipamentos':
                selector = 2
                print(f'Selector: {selector}')
            if text.strip() == 'Fotos':
                selector = 3
                print(f'Selector: {selector}')

        if selector == 1:
            if size == '4' and text != '':
                tipo_info = text

            if size == '3' and text != '':
                if text == 'Ano':
                    tipo_info = 'GERAL'

                if bgcolor == '#ffffff':
                    info = text

                if bgcolor == '#efefef':
                    tipo_info_list.append(tipo_info)
                    info_list.append(info)
                    desc_list.append(text)
    return
"""

"""for row in rows:
    if selector == 1:
        get_geral_info(row)

    if selector == 2:
        pass
"""
"""
        table2 = row.find_element(By.TAG_NAME, 'td').find_element(By.TAG_NAME, 'td').find_element(
            By.TAG_NAME, 'table').find_element(By.TAG_NAME, 'tbody')
        for row2 in table2:
            for col in row2.find_elements(By.TAG_NAME, 'tr'):
                try:
                    font = col.find_element(By.TAG_NAME, "font")
                    size = font.get_attribute('size')
                    text = col.text
                    #bgcolor = col.get_attribute("bgcolor")
                except:
                    font = ''
                    size = ''
                    text = ''
                    #bgcolor = ''

                if size == '5' and text != '':
                    if text.strip() == 'Equipamentos':
                        selector = 2
                        print(f'Selector: {selector}')
                    if text.strip() == 'Fotos':
                        selector = 3
                        print(f'Selector: {selector}')

                if selector == 1:
                    if size == '4' and text != '':
                        tipo_info = text

                    if size == '3' and text != '':
                        if text == 'Ano':
                            tipo_info = 'GERAL'

                        if bgcolor == '#ffffff':
                            info = text

                        if bgcolor == '#efefef':
                            tipo_info_list.append(tipo_info)
                            info_list.append(info)
                            desc_list.append(text)
"""
"""
for i, el in enumerate(desc_list):
    print(f'{tipo_info_list[i]} {info_list[i]} {desc_list[i]}')
# Tratar consumo e autonomia para carros flex
"""

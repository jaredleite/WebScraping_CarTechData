import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
from time import sleep
import random
import csv
import WebScraping_Timer
# import target function
import WebScaping_FichaCompleta_Proxy_Target as wc
# import WebCrawler_CarrosWeb_04_Model_BeautifulSoup as wc

start = time.time()
end = time.time()

Timer = WebScraping_Timer.Timer()

treated_proxies_file = os.getcwd() + '\\treated_proxies.csv'
current_proxies_file = os.getcwd() + '\\current_proxies.csv'

df_treated_proxies = pd.read_csv(treated_proxies_file, encoding='utf-8')
df_current_proxies = pd.read_csv(current_proxies_file, encoding='utf-8')

proxyDict = {
    "http": '1',
            "https": '2'
}


def test(p):
    global proxyDict

    if(p != ''):
        proxyDict['http'] = p
        proxyDict['https'] = p
        r = requests.get("http://ipinfo.io/json", timeout=3, proxies=proxyDict)
    else:
        r = requests.get("http://ipinfo.io/json", timeout=3)
    print(r.content)
    return r.status_code


def refresh_proxy_list():
    global df_treated_proxies
    global df_current_proxies

    df_treated_proxies = pd.read_csv(treated_proxies_file, encoding='utf-8')
    for p in df_treated_proxies['proxy']:
        # print(p)
        if df_current_proxies[(df_current_proxies['proxy'] == p)].shape[0] == 0:
            df_current_proxies.loc[len(df_current_proxies)] = [p, 0, 'on']
            # print(df_current_proxies)
    df_current_proxies.to_csv(current_proxies_file,
                              index=False, encoding='utf-8')
    print('Atualizou current proxy')


def set_timer():
    global start
    global df_current_proxies
    n_proxies = len(df_current_proxies[(df_current_proxies['status'] == 'on')])

    if n_proxies != 0:
        start = time.time()

    if n_proxies <= 3:
        print('timer situação <=3')
        Timer.take_long_time_min = 10
        Timer.take_long_time_max = 15
        Timer.short_break_min = 120
        Timer.short_break_max = 180
        Timer.long_break_min = 60
        Timer.long_break_max = 120

    else:
        if n_proxies <= 10:
            print('timer situação <=10')
            Timer.take_long_time_min = 20
            Timer.take_long_time_max = 30
            Timer.short_break_min = 30
            Timer.short_break_max = 60
            Timer.long_break_min = 30
            Timer.long_break_max = 60

        else:
            print('timer situação >10')
            Timer.take_long_time_min = 40
            Timer.take_long_time_max = 50
            Timer.short_break_min = 5
            Timer.short_break_max = 30
            Timer.long_break_min = 10
            Timer.long_break_max = 30


while(end - start <= 60*60):
    refresh_proxy_list()
    set_timer()
    try:
        p = random.choice(
            list(df_current_proxies[(df_current_proxies['status'] == 'on')]['proxy']))
    except:
        p = ''
    try:
        # target function
        #r = test(p)
        r = wc.WebScraping(p)
    except:
        print('Target function fail')
        r = -1

    index = df_current_proxies[(
        df_current_proxies['proxy'] == p)].index.item()

    if r == 200:
        df_current_proxies.at[index, 'err_count'] = 0
        Timer.take_a_break()

    else:
        err_count = df_current_proxies.at[index, 'err_count']
        err_count = err_count + 1
        df_current_proxies.at[index, 'err_count'] = err_count

        if err_count >= 100:
            df_current_proxies.at[index, 'status'] = 'off'

    df_current_proxies.to_csv(current_proxies_file,
                              index=False, encoding='utf-8')
    end = time.time()

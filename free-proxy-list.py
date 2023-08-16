import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
from time import sleep
import csv

# import target function
import WebScaping_FichaCompleta_Proxy_Test as wc
#import WebCrawler_CarrosWeb_04_Model_BeautifulSoup as wc


treated_proxies_file = os.getcwd() + '\\treated_proxies.csv'
#link_test_list_file = ''


proxyDict = {
    "http": '1',
            "https": '2'
}

url = 'https://free-proxy-list.net/'
# free proxy list site

fail_count = 0


def test():
    global proxyDict
    r = requests.get("http://ipinfo.io/json", timeout=3, proxies=proxyDict)
    print(r.content)
    return r.status_code


def Raw_Proxies():
    global fail_count
    r = requests.get(url, timeout=4)
    sleep(5)
    soup = BeautifulSoup(r.content, 'html.parser')

    rows = soup.find_all('tr')

    ip = []
    country = []
    https = []

    for rw in rows:
        try:
            cols = rw.find_all('td')
            ip_adrress = cols[0].get_text()
            port = cols[1].get_text()
            country_name = cols[3].get_text()
            https_YorN = cols[6].get_text()
            if ip_adrress.count('.') == 3:
                ip.append(f'{ip_adrress}:{port}')
                country.append(country_name)
                https.append(https_YorN)
        except:
            fail_count = fail_count + 1
            print(f'Fail: Get list proxies - Count:{fail_count}')
            pass

    df = pd.DataFrame(list(zip(ip, country, https)),
                      columns=['ip', 'country', 'https'])

    return df


def Main():
    global fail_count
    global proxyDict
    n_list = 0
    while fail_count <= 100:
        n_list = n_list + 1
        print(f'Raw list #{n_list}')
        inicio = time.time()
        df_raw_proxies = Raw_Proxies()

        for p in df_raw_proxies['ip']:
            try:
                #proxyDict['http'] = p
                #proxyDict['https'] = p

                # r = target function
                #r = wc.WedCrawler(p)
                #r = test()
                r = wc.WebScraping(p)

                if r == 200:
                    with open(treated_proxies_file, 'a', newline='', encoding="utf-8") as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow([p])
                        csvfile.close()

                    print(f'sucess/{p}')
                else:
                    print(f'fail/{p}')
            except:
                print(f'fail/{p}')

        fim = time.time()
        print(f'Tempo de durção: {(fim - inicio)/60} min')


Main()

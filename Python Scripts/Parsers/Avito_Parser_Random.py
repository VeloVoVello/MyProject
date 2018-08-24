# Avito multiple pages parser
#!/usr/bin/env python3

import re
import csv
import sys
import requests
from bs4 import BeautifulSoup

url = 'https://www.avito.ru/moskva/mototsikly_i_mototehnika/mototsikly/kross_i_enduro?s_trg=7'
baseurl = 'https://www.avito.ru/moskva/mototsikly_i_mototehnika/mototsikly/kross_i_enduro?p='
http = 'https://www.avito.ru'

url_list = []
title_list = []
price_list = []
city_list = []
time_list = []
date_list = []
href_list = []


# Download full HTML page (with OS version determination)

def fullsoup(url):
    r = requests.get(url)
    if 'win' in sys.platform.lower():
        fullsoup = BeautifulSoup(r.text, 'html.parser')
    else:
        fullsoup = BeautifulSoup(r.text, 'lxml')
        
    return fullsoup

# Count URL summary

def totalpages(fullsoup):
    pages = fullsoup.find('div', class_='pagination-pages')
    pages = pages.find_all('a', class_='pagination-page')
    pages = pages[-1].get('href')
    totalpages = pages.split('=')[-1]

    return int(totalpages)

# URL list generator

def genurl(totalpages):
    for i in range(1, totalpages + 1):
        genurl = baseurl + str(i)
        url_list.append(genurl)

# Fill out lists with data

def fillout():

    for url in url_list:
        r = requests.get(url)
        pagesoup = BeautifulSoup(r.text, 'html.parser')

        for tag in pagesoup.find_all(re.compile("^a"), class_="item-description-title-link"):
            title_list.append(tag.text.strip().replace(',', ''))

        for tag in pagesoup.find_all(re.compile("^span"), class_='price'):
            price_list.append(tag.text.strip().replace('  ₽', ''))

        for tag in pagesoup.select('p')[2:-3]:
            string = tag.text.replace('\xa0', ' ')
            city_list.append(string)

        for tag in pagesoup.find_all(re.compile("^div"), class_="js-item-date c-2"):
            time_list.append(tag.text.strip())

        for tag in pagesoup.select('.js-item-date'):
            date_list.append(tag.get('data-absolute-date'))

        for tag in pagesoup.select('.item-description-title-link'):
            href = http + tag.get('href')
            href_list.append(href)

# Write out CSV file

def writedata():
    with open('items.csv', 'w', newline='') as f:
        fieldnames = ['Наименование', 'Цена', 'Район', 'Время размещения', 'Точное время', 'Ссылка']
        writer = csv.writer(f)
        writer.writerow(fieldnames)
        writer.writerows(zip(title_list, price_list, city_list, time_list, date_list, href_list))
		
def main():
    genurl(totalpages(fullsoup(url)))
    fillout()
    writedata()

if __name__ == "__main__":
    main()
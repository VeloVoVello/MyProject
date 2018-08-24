# Для поиска из фильтра по категориям (много полей)

import re
import csv
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


# Загружаем всю HTML страницу

def fullsoup(url):
    r = requests.get(url)
    fullsoup = BeautifulSoup(r.text, 'html.parser')

    return fullsoup


# Считаем количество всех URL

def totalpages(fullsoup):
    pages = fullsoup.find('div', class_='pagination-pages')
    pages = pages.find_all('a', class_='pagination-page')
    pages = pages[-1].get('href')
    totalpages = pages.split('=')[-1]

    return int(totalpages)


# Создаем список всех URL

def genurl(totalpages):
    for i in range(1, totalpages + 1):
        genurl = baseurl + str(i)
        url_list.append(genurl)


# Наполняем списки данными

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

# Записываем данные в CSV файл

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
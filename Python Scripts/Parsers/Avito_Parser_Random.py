# Для поиска из фильтра по категориям (много полей)

import re
import csv
import requests
from bs4 import BeautifulSoup

url = 'https://www.avito.ru/moskva/mototsikly_i_mototehnika/mototsikly/kross_i_enduro?s_trg=7'
baseurl = 'https://www.avito.ru/moskva/mototsikly_i_mototehnika/mototsikly/kross_i_enduro?p='

url_list = []
title_list = []
price_list = []
city_list = []
time_list = []


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
            string = tag.replace(u'\xa0', u' ')
            string.append(tag.replace(u'\xa0', u' '))

        for tag in pagesoup.find_all(re.compile("^div"), class_="js-item-date c-2"):
            time_list.append(tag.text.strip())

# Записываем данные в CSV файл

def writedata():
    with open('items.csv', 'a', newline='') as f:
        fieldnames = ['Наименование', 'Цена', 'Район', 'Время размещения']
        writer = csv.writer(f)
        writer.writerow(fieldnames)
        writer.writerows(zip(title_list, price_list, city_list, time_list))
		
def main():
    genurl(totalpages(fullsoup(url)))
    fillout()
    writedata()


if __name__ == "__main__":
    main()

"""
def pagesoup(genurl):

	r = requests.get(genurl)
	pagesoup = BeautifulSoup(r.text, 'html.parser')
	
	return pagesoup
	
def fillout(pagesoup):

    for url in soup.find_all(re.compile("^a"), class_="item-description-title-link"):
        title_list.append(url.text.strip().replace(',', ''))

    for url in soup.find_all(re.compile("^span"), class_='price'):
        price_list.append(url.text.strip().replace('  ₽', ''))

    for url in soup.find_all(re.compile("^p")):
        city_list.append(url.text.replace(',',''))

    for url in soup.find_all(re.compile("^div"), class_="js-item-date c-2"):
        time_list.append(url.text.strip())
"""

""" 
    titles_set = soup.find_all(class_="item-description-title-link") # Создание сета с наименованиями
    prices_set = soup.find_all(class_="price") # Создание сета с ценами
    
    for i in titles_set:
        title_obj_list = i['title'].replace(',', '').split() # Создание раздельного списка объектов из сета наименований
        titles_list.append(title_obj_list)  # Наполнение списка titles_list
        #title_list.append(str(title_obj_list[0]) + ' ' + str(title_obj_list[1]))  # Наполнение списка title_list
        title_list.append(i.text.strip().replace(',', ''))
        #year_list.append(title_obj_list[-3])  # Наполнение списка year_list
        city_list.append(title_obj_list[-1])  # Наполнение списка city_list (ОК)

Разобраться с циклом

for url in set:
    aurls = url.find_all("a", {"class": "item-description-title-link"})
    for url in aurls:
        print(url.text)
		
		


Отлично работает:

for url in soup.find_all(re.compile("^a"), class_="item-description-title-link"):
    print(url.text.strip())

Suzuki TL1000R
Yamaha XVS 650 V-Star
XF650 Freewind 2000гв
Yamaha BT 1100
Honda CB750 2006
Honda vfr 800
Honda XL 650

for url in soup.find_all(re.compile("^span"), class_='price'):
    print(url.text)

160 000  ₽
210 000  ₽
250 000  ₽
250 000  ₽
250 000  ₽
150 000  ₽
180 000  ₽
210 000  ₽

for url in soup.find_all(re.compile("^p")):
    print(url.text)

м. Тушинская
м. Южная
м. Медведково
м. Медведково
м. Марьино
м. Бабушкинская
м. Кунцевская

for url in soup.find_all(re.compile("^div"), class_="js-item-date c-2"):
    print(url.text.strip())
    
Вчера 23:34
Вчера 22:18
Вчера 22:06
Вчера 20:57
Вчера 20:49

    for i in prices_set:
        price_obj_raw_string = i.text.strip().replace('  ₽', '')
        price_obj_int = int(price_obj_raw_string.replace(' ', ''))
        price_list.append(price_obj_int)  # Наполнение списка price_list (ОК)
"""

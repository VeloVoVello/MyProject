# Для поиска из фильтра по категориям (много полей)

import os
import csv
import time
import requests
from bs4 import BeautifulSoup

url = 'https://www.avito.ru/moskva/mototsikly_i_mototehnika/mototsikly?pmax=250000&pmin=150000&s_trg=3'

items_dict = {}

titles_list = []
title_list = []
price_list = []
year_list = []
city_list = []

cwd = os.getcwd()

def get_soup_data(url):

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    titles_set = soup.find_all(class_="item-description-title-link") # Создание сета с наименованиями
    prices_set = soup.find_all(class_="price") # Создание сета с ценами

    for i in titles_set:
        title_obj_list = i['title'].replace(',', '').split() # Создание раздельного списка объектов из сета наименований
        titles_list.append(title_obj_list)  # Наполнение списка titles_list
        #title_list.append(str(title_obj_list[0]) + ' ' + str(title_obj_list[1]))  # Наполнение списка title_list
        title_list.append(i.text.strip().replace(',', ''))
        #year_list.append(title_obj_list[-3])  # Наполнение списка year_list
        city_list.append(title_obj_list[-1])  # Наполнение списка city_list (ОК)



""" 

Разобраться с циклом

for tag in set:
    aTags = tag.find_all("a", {"class": "item-description-title-link"})
    for tag in aTags:
        print(tag.text)

Отлично работает:

for tag in soup.find_all(re.compile("^p")):
    print(tag.text)

м. Тушинская
м. Южная
м. Медведково
м. Медведково
м. Марьино
м. Бабушкинская
м. Кунцевская

for tag in soup.find_all(re.compile("^span"), class_='price'):
    print(tag.text)

160 000  ₽
210 000  ₽
250 000  ₽
250 000  ₽
250 000  ₽
150 000  ₽
180 000  ₽
210 000  ₽


for tag in soup.find_all(re.compile("^a"), class_="item-description-title-link"):
    print(tag.text.strip())

Suzuki TL1000R
Yamaha XVS 650 V-Star
XF650 Freewind 2000гв
Yamaha BT 1100
Honda CB750 2006
Honda vfr 800
Honda XL 650

for tag in soup.find_all(re.compile("^div"), class_="js-item-date c-2"):
    print(tag.text.strip())
    
Вчера 23:34
Вчера 22:18
Вчера 22:06
Вчера 20:57
Вчера 20:49

"""

    for i in prices_set:
        price_obj_raw_string = i.text.strip().replace('  ₽', '')
        price_obj_int = int(price_obj_raw_string.replace(' ', ''))
        price_list.append(price_obj_int)  # Наполнение списка price_list (ОК)

def write_data_lists():

    with open('items_lists_1.csv', 'w', newline='') as f:  # write CSV from lists
        #fieldnames = ['Марка', 'Цена', 'Год', 'Город']
        writer = csv.writer(f)
        #writer.writerow(fieldnames)
        #writer.writerows(zip(title_list, price_list, year_list, city_list))
        writer.writerows(zip(title_list, price_list))
        print('\nCSV file "items_lists_1.csv" is written in:\n{}'.format(cwd))

def main():

    get_soup_data(url)
    write_data_lists()

if __name__ == "__main__":
    main()

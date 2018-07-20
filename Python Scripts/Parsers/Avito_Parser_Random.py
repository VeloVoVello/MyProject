import csv
import time
import requests
from bs4 import BeautifulSoup

url = 'https://www.avito.ru/moskva/avtomobili/audi/a4/universal?radius=300&s_trg=3&f=188_898b902&i=1'

items_dict = {}

titles_list = []
title_list = []
price_list = []
year_list = []
city_list = []

def get_soup_data(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    titles_set = soup.find_all(class_="item-description-title-link") # Создание сета с наименованиями
    prices_set = soup.find_all(class_="price") # Создание сета с ценами

    for i in titles_set:
        title_obj_list = i['title'].replace(',', '').split() # Создание раздельного списка объектов из сета наименований
        titles_list.append(title_obj_list)  # Наполнение списка titles_list
        title_list.append(str(title_obj_list[0]) + ' ' + str(title_obj_list[1]))  # Наполнение списка title_list
        year_list.append(title_obj_list[-3])  # Наполнение списка year_list
        city_list.append(title_obj_list[-1])  # Наполнение списка city_list

    for i in prices_set:
        price_obj_raw_string = i.text.strip().replace('  ₽', '')
        price_obj_int = int(price_obj_raw_string.replace(' ', ''))
        price_list.append(price_obj_int)  # Наполнение списка price_list
"""
    for x, y in zip(titles_list, price_list):
        items_dict[x] = y # Наполнение словаря

    print('Data lists and item dictionary were filled out...')
    time.sleep(1)
"""
"""
def write_data_dict():
    with open('items_dict.csv', 'w') as f:  # write CSV from dictionary
        writer = csv.writer(f)
        for key, value in items_dict.items():
            writer.writerow([key, value])
    print('CSV file is written from dictionary')
"""
def write_data_lists():
    with open('items_lists.csv', 'w', newline='') as f:  # write CSV from lists
        fieldnames = ['Марка', 'Цена', 'Год', 'Город']
        writer = csv.writer(f)
        writer.writerow(fieldnames)
        writer.writerows(zip(title_list, price_list, year_list, city_list))
        print('CSV file is written from lists')

def main():
    get_soup_data(url)
#    write_data_dict()
    write_data_lists()

if __name__ == "__main__":
    main()

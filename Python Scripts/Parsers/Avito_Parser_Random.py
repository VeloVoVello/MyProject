# Avito multiple pages parser
#!/usr/bin/env python3

import re
import csv
import sys
import requests
import mysql.connector
from bs4 import BeautifulSoup

password = input('Password: ')

url = 'https://www.avito.ru/moskva/mototsikly_i_mototehnika/mototsikly/kross_i_enduro?s_trg=7'
baseurl = 'https://www.avito.ru/moskva/mototsikly_i_mototehnika/mototsikly/kross_i_enduro?p='
http = 'https://www.avito.ru'

url_list = []
id_list = []
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

def fillists():

    for url in url_list:
        r = requests.get(url)
        pagesoup = BeautifulSoup(r.text, 'html.parser')

        for tag in pagesoup.find_all("div", attrs={'class':'item_table'}):
            id_list.append(tag.get('id'))
		
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

def writecsv():
    with open('items.csv', 'w', newline='') as f:
        fieldnames = ['ID', 'Наименование', 'Цена', 'Район', 'Время размещения', 'Точное время', 'Ссылка']
        writer = csv.writer(f)
        writer.writerow(fieldnames)
        writer.writerows(zip(id_list, title_list, price_list, city_list, time_list, date_list, href_list))

def writesql():

    serv = mysql.connector.connect(
        host="10.80.132.132",
        user="root",
        passwd=password
    )

    servcursor = serv.cursor()

    servcursor.execute("DROP DATABASE IF EXISTS moto;")
    servcursor.execute("CREATE DATABASE moto")
    servcursor.close()
    serv.close()

    motodb = mysql.connector.connect(
        host="10.80.132.132",
        user="root",
        passwd=password,
        database="moto"
    )

    motodbcursor = motodb.cursor()

    motodbcursor.execute(
        "CREATE TABLE items (idgen MEDIUMINT NOT NULL AUTO_INCREMENT, id VARCHAR(15), title VARCHAR(80)," 
        "price VARCHAR(20), city VARCHAR(20), time VARCHAR(20),"
        "date VARCHAR(20), url VARCHAR(120), PRIMARY KEY (idgen));")

    add_data = "INSERT INTO items (id,title,price,city,time,date,url) VALUES (%s, %s, %s, %s, %s, %s, %s);"

    for id, title, price, city, time, date, url in zip(id_list, title_list, price_list, city_list, time_list, date_list,
                                                       href_list):
        data = (id, title, price, 'NULL', time, 'NULL', url)
        motodbcursor.execute(add_data, data)

    motodb.commit()

def main():
    genurl(totalpages(fullsoup(url)))
    fillists()
  #  writecsv()
    writesql()

if __name__ == "__main__":
    main()
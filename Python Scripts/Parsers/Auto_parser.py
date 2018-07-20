import csv
import requests
from bs4 import BeautifulSoup

url = 'https://www.avito.ru/moskva/avtomobili/s_probegom/honda/odyssey?radius=300&s_trg=3'

r = requests.get(url)

soup = BeautifulSoup(r.text, 'html.parser')

filename = 'auto.csv'
f = open(filename, 'a')

headers = 'brand, price\n'

f.write(headers)


# grab ID
# soup.find_all(id="i1581458031")
# grab Titles
titles = soup.find_all(class_="item-description-title-link")
title[0]['title'].replace(',', '')
title[0]['title'].split(',')[0]
# grab Price
prices = soup.find_all(class_="price")
price[0].text.strip()

for i in titles:
    title = i['title'].replace(',', '')
    title_list.append(title)
    print(title)

<<<<<<< HEAD
for i in prices:
    pri_1 = i.text.strip().replace('  ₽', '')
    price = int(pri_1.replace(' ', ''))
    print(price)

f.close()
=======
for i in titles:
    tit = i['title']
    print(tit)


for i in price:
    one = i.text.strip().split(' ')
    sum = int(one[0] + one[1])
    print(sum)


data = {'title': tit,
        'price': sum}
>>>>>>> MyProject_GitHub/HQ1057

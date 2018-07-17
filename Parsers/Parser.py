import requests
from bs4 import BeautifulSoup

url = 'https://www.avito.ru/moskva/avtomobili/s_probegom/honda/odyssey?radius=0&s_trg=3&i=1'
r = requests.get(url)
html = r.text()
soup = BeautifulSoup(html, 'html.parser')

print(soup.prettify())

# ищем все элементы
soup.find_all('div', class_='item_table')

cars = soup.find_all('div', class_='item_table')

for i in soup.find_all('div', class_='item_table'):
    print(i.get('href'))

import requests
from bs4 import BeautifulSoup

url = https://www.avito.ru/moskva/avtomobili/s_probegom/honda/odyssey?radius=300&s_trg=3

r = requests.get(url)

soup = BeautifulSoup(r.text, 'html.parser')

# grab ID
soup.find_all(id="i1581458031")
# grab Titles
titles = soup.find_all(class_="item-description-title-link")
# grab Price
price = soup.find_all(class_="price")



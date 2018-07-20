import csv
import time
import requests
from bs4 import BeautifulSoup

url = 'https://www.avito.ru/moskva/avtomobili/s_probegom/honda/odyssey?radius=300&s_trg=3'

titles_list = []
prices_list = []

items_dict = {}

def get_soup_data(url):

	r = requests.get(url)
	soup = BeautifulSoup(r.text, 'html.parser')
	titles_set = soup.find_all(class_="item-description-title-link")
	prices_set = soup.find_all(class_="price")	

	for i in titles_set:
		title_obj_string = i['title'].replace(',', '')
		titles_list.append(title_obj_string) # Наполнение списка titles_list

	for i in prices_set:
		price_obj_raw_string = i.text.strip().replace('  ₽', '')
		price_obj_int = int(price_obj_raw_string.replace(' ', ''))
		prices_list.append(price_obj_int) # Наполнение списка prices_list

	for x,y in zip(titles_list, prices_list):
    	items_dict[x] = y

	print('Data lists and item dictionary were filled out...')
	time.sleep(1)

def write_data(s):

	with open('items_dict.csv', 'w') as csv_file: # write from dictionary
    	writer = csv.writer(csv_file)
    	for key, value in items_dict.items():
    		writer.writerow([key, value])

    """
    with open('items_dict.csv', 'r') as csv_file:
    	reader = csv.reader(csv_file)
    	items_dict = dict(reader)
   	
   	"""

   	with open('new.csv', 'w') as new_file:

   		fieldnames = ['title', 'price']

    	writer = csv.DictWriter(new_file, fieldnames=fieldnames, delimiter='\t')
    	writer.writerow(prices_list)

def main():
	get_soup()

if __name__ == "__main__":
	main() 


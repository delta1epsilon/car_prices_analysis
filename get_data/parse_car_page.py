from bs4 import BeautifulSoup
import urllib.request as ur
import pandas as pd
import numpy as np
import re, time

def remove_shit(s):
	return re.sub('[ \n$€]', '', s)

def get_prices(parsed_page):
	main_price = parsed_page.find_all(name = 'div', attrs = {'class':'price-seller'})[0].text
	price_dollar = remove_shit(main_price)
	price_euro, price_grn = ['NA']*2
	try:
		prices = list(parsed_page.find_all(name = 'div', attrs = {'class':'price-at-rate'}))[0].text.rsplit('/', 1)
		if '$' in main_price:
			if '€' in prices[0]:
				price_euro =  remove_shit(prices[0])
				price_grn =  remove_shit(prices[1])
				price_grn = ''.join(re.findall('[\d]', price_grn))
			else:
				price_euro =  remove_shit(prices[1])
				price_grn =  remove_shit(prices[0])
				price_grn = ''.join(re.findall('[\d]', price_grn))
		elif '€' in main_price:
			price_euro = remove_shit(main_price)
			if '$' in prices[0]:
				price_dollar =  remove_shit(prices[0])
				price_grn =  remove_shit(prices[1])
				price_grn = ''.join(re.findall('[\d]', price_grn))
			else:
				price_dollar =  remove_shit(prices[1])
				price_grn =  remove_shit(prices[0])
				price_grn = ''.join(re.findall('[\d]', price_grn))
		elif 'грн' in main_price:
			price_grn = remove_shit(main_price)
			price_grn = ''.join(re.findall('[\d]', price_grn))
			if '€' in prices[0]:
				price_euro =  remove_shit(prices[0])
				price_dollar =  remove_shit(prices[1])
			else:
				price_euro =  remove_shit(prices[1])
				price_dollar =  remove_shit(prices[0])
	except:
		pass

	return price_dollar, price_euro, price_grn

def get_technical_characteristics(parsed_page):
	transmission, drive_type, doors, color, seats, fuel, engine_v = 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA'
	characteristics = list(parsed_page.find(name = 'dl', attrs = {'class':'unordered-list', 'style':'margin-top: 10px;'}))
	for char in characteristics[1:]:
		char = char.text.rsplit(None, 1)
		if 'Коробка передач:' in char[0]:
			transmission = char[1]
		elif char[0] == 'Привід:':
			drive_type = char[1]
		elif char[0] == 'Кількість дверей:':
			doors = char[1]
		elif char[0] == 'Кількість місць:':
			seats = char[1]
		elif char[0] == 'Колір:':
			color = char[1]
		elif char[0] == 'Паливо:':
			fuel = char[1]
		elif 'Об\'єм двигуна:' in char[0]:
			engine_v = ''.join(re.findall('[\d.]', char[0]))

	return transmission, drive_type, doors, color, seats, fuel, engine_v

def check_if_uncustomed(parsed_page):
	uncustomed = 0
	try:
		customs = list(parsed_page.find_all(name = 'dl', attrs = {'class':'uncustomed'}))[0].text
		if 'Авто не розмитнено' in customs:
			uncustomed = 1
	except:
		pass
	return uncustomed 

def get_user_id(parsed_page):
	user_id = 'NA'
	try:
		user_id = list(parsed_page.find_all(name = 'dl', attrs = {'class':'info-user'}))[0].find_all('a')[0].get('href')
		user_id = ''.join(re.findall('[\d]', user_id))
	except:
		pass
	return user_id

def get_description(parsed_page):
	description = 'NA'
	try:
		description = list(parsed_page.find_all(name = 'p', attrs = {'class':'description-order'}))[0].text
		description = re.sub('[\n\r]', '', description)
	except:
		pass
	return description 

def get_city(parsed_page):
	city = list(parsed_page.find(name = 'dd', attrs = {'class':'item'}))[1].text
	city = remove_shit(city)
	return city

def get_milage(parsed_page):
	milage = list(parsed_page.find_all(name = 'p', attrs = {'class':'item-param'}))[2].text
	milage = remove_shit(milage)
	milage = re.findall('\d+', milage)
	if milage == []: milage = 0
	else: milage = milage[0]
	return milage 

def get_body(parsed_page):
	body = parsed_page.find_all(name = 'strong', attrs = {'id':'final_page__characteristic_body_name'})[0].string
	body = remove_shit(body)
	return body

def get_car_type(parsed_page):
	car_type = list(parsed_page.find(name = 'p', attrs = {'class':'item-param'}))[3].string
	car_type = remove_shit(car_type)
	return car_type

def get_year(parsed_page):
	return int(parsed_page.find_all(name = 'span', attrs = {'class':'year'})[0].string)

def get_additional_data(parsed_page):
	additional_data = 'NA'
	try:
		additional_data = list(parsed_page.find_all(name = 'p', attrs = {'class':'additional-data'}))[0].text    
	except: 
		pass
	return re.sub('[\n\r]', '', additional_data)

def get_page_add_date(parsed_page):
	return list(parsed_page.find_all(name = 'strong', attrs = {'id':'final_page__add_date'}))[0].text.rsplit(' ', 1)[0]

def get_extraction_date():
	return time.strftime('%m/%d/%Y')

def parse_car_page(url):
	car_page = ur.urlopen(url).read()
	car_page_parsed = BeautifulSoup(car_page, 'html.parser')

	year = get_year(car_page_parsed)
	price_dollar, price_euro, price_grn = get_prices(car_page_parsed)
	uncustomed = check_if_uncustomed(car_page_parsed)
	car_type = get_car_type(car_page_parsed)
	body = get_body(car_page_parsed)
	milage = get_milage(car_page_parsed)
	city = get_city(car_page_parsed)
	transmission, drive_type, doors, color, seats, fuel, engine_v = get_technical_characteristics(car_page_parsed)
	user_id = get_user_id(car_page_parsed)    
	description = get_description(car_page_parsed)
	additional_data = get_additional_data(car_page_parsed)
	page_add_date = get_page_add_date(car_page_parsed)
	extraction_date = get_extraction_date()
	
	df = pd.DataFrame([[year, price_dollar, price_euro, price_grn, uncustomed, car_type, body, 
						milage, city, transmission, drive_type, doors, seats, color, 
						fuel, engine_v, user_id, additional_data, description, page_add_date, extraction_date]],
					columns = ['year', 'price_dollar', 'price_euro', 'price_grn', 'uncustomed', 'car_type', 'body', 
						'milage', 'city', 'transmission', 'drive_type', 'doors', 'seats', 'color', 
						'fuel', 'engine_v', 'user_id', 'additional_data', 'description', 'page_add_date', 'extraction_date'])

	return df


if __name__ == "__main__":
	import logging
	
	logging.basicConfig(level=logging.INFO,
						format='%(asctime)s %(levelname)-4s %(message)s',
						datefmt='%H:%M:%S')
	logger = logging.getLogger(__name__)
	
	logger.info('Reading csv with links on cars ...')
	cars_links = pd.read_csv('german_cars_links.csv', nrows = 2000)#"ISO-8859-1"
	logger.info('Got {0} links on cars'.format(cars_links.shape[0]))

	logger.info('Parsing cars pages ...')
	cars = pd.DataFrame(columns = ['year', 'price_dollar', 'price_euro', 'price_grn', 'uncustomed', 'car_type', 'body', 
									'milage', 'city', 'transmission', 'drive_type', 'doors', 'seats', 'color', 
									'fuel', 'engine_v', 'user_id', 'additional_data', 'description', 'page_add_date', 
									'extraction_date', 'brand', 'model', 'link'])
	for i in range(cars_links.shape[0]):
		# print('Parsing car page: ', i)
		df = pd.DataFrame([['NA']*21], columns = ['year', 'price_dollar', 'price_euro', 'price_grn', 'uncustomed', 'car_type', 'body', 
						'milage', 'city', 'transmission', 'drive_type', 'doors', 'seats', 'color', 
						'fuel', 'engine_v', 'user_id', 'additional_data', 'description', 'page_add_date', 'extraction_date'])
		try:
			df = parse_car_page(cars_links.link[i])
		except:
			 pass
		df['brand'] = cars_links.brand[i]
		df['model'] = cars_links.model[i]
		df['link'] = cars_links.link[i]
		cars = cars.append(df, ignore_index = True)

	file_name = 'autoria_german_cars_data.csv'
	cars.to_csv(file_name)
	logger.info('The data was saved into {0}'.format(file_name))
from bs4 import BeautifulSoup
import urllib.request as ur
import pandas as pd
import numpy as np
import re, time

def remove_shit(s):
	return re.sub('[ \n$€]', '', s)

def get_prices(parsed_page):
	main_price = [parsed_page.find_all(name = 'div', attrs = {'class':'price-seller'})[0].text]
	price_at_rate = []
	try:
		price_at_rate = list(parsed_page.find_all(name = 'div', attrs = {'class':'price-at-rate'}))[0].text.rsplit('/')
	except:
		pass
	prices = main_price + price_at_rate
	df = pd.DataFrame([['price_dollar', '$', ''], 
					   ['price_euro', '€', ''], 
					   ['price_grn', 'грн.', '']],
					columns = ['currency', 'sign', 'value'])
	try:
		for i in range(3):
			for j in range(len(prices)):
				if df.iloc[i, 1] in prices[j]:
					df.ix[i, 'value'] = ''.join(re.findall('[\d]', remove_shit(prices[j])))
	except:
		pass
	return df.value[0], df.value[1], df.value[2]

def get_technical_characteristics(parsed_page):
	transmission, drive_type, doors, color, seats, fuel, engine_v = ['']*7
	characteristics = list(parsed_page.find(name = 'dl', attrs = {'class':'unordered-list', 'style':'margin-top: 10px;'}))
	for char in characteristics[1:]:
		char = char.text.rsplit(None, 1)
		if 'Коробка передач:' in char[0]:
			transmission = char[1]
		elif char[0] == 'Привід:':
			drive_type = char[1]
		elif char[0] == 'Кількість дверей:':
			doors = int(char[1])
		elif char[0] == 'Кількість місць:':
			seats = int(char[1])
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

def check_if_after_accident(parsed_page):
	accident = 0
	try:
		if 'ДТП' in parsed_page.find(name = 'p', attrs = {'class':'item-param'}).text:
			accident = 1
	except:
		pass
	return accident

def get_user_id(parsed_page):
	user_id = ''
	try:
		user_id = list(parsed_page.find_all(name = 'dl', attrs = {'class':'info-user'}))[0].find_all('a')[0].get('href')
		user_id = ''.join(re.findall('[\d]', user_id))
	except:
		pass
	return user_id

def get_description(parsed_page):
	description = ''
	try:
		description = list(parsed_page.find_all(name = 'p', attrs = {'class':'description-order'}))[0].text
		description = re.sub('[\n\r]', '', description)
	except:
		pass
	return description 

def get_location(parsed_page):
	region = parsed_page.find_all(name = 'span', attrs = {'id':'final_page__breadcrumbs_state'})[0].text
	city = parsed_page.find_all(name = 'span', attrs = {'id':'final_page__breadcrumbs_city'})[0].text
	return region, city

def get_milage(parsed_page):
	data = list(parsed_page.find(name = 'div', attrs = {'class':'characteristic delimeter'}))
	milage = ''
	for l in data:
		try:
			if 'Пробіг' in l.text:
				milage = ''.join(re.findall('[\d]', l.text))
				milage = int(milage)
		except:
			pass
	return milage

def get_body(parsed_page):
	body = parsed_page.find_all(name = 'strong', attrs = {'id':'final_page__characteristic_body_name'})[0].string
	return remove_shit(body)

def get_car_type(parsed_page):
	data_list = list(parsed_page.find_all(name = 'p', attrs = {'class':'item-param'}))
	for item in data_list:
		if 'Тип транспорту' in item.text:
			car_type = item
	return remove_shit(list(car_type)[3].string)

def get_year(parsed_page):
	return int(parsed_page.find_all(name = 'span', attrs = {'class':'year'})[0].string)

def get_additional_data(parsed_page):
	additional_data = ''
	try:
		data = list(parsed_page.find_all(name = 'p', attrs = {'class':'additional-data'}))
		for i in range(len(data)):
			additional_data = additional_data + ' ' + re.sub('[\n\r]', '', data[i].text)
	except: 
		pass
	if additional_data == '':
		return ''
	else: 
		return ' '.join(additional_data.split())

def get_status(parsed_page):
    status = ''
    try:
        error = parsed_page.find_all(name = 'div', attrs = {'class':'error'})[0].text
        if 'Авто видалено' in error:
            status = 'removed'
        elif 'продано' in error:
            status = 'sold'
    except:
        pass
    return status

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
	region, city = get_location(car_page_parsed)
	transmission, drive_type, doors, color, seats, fuel, engine_v = get_technical_characteristics(car_page_parsed)
	user_id = get_user_id(car_page_parsed)    
	description = get_description(car_page_parsed)
	additional_data = get_additional_data(car_page_parsed)
	status = get_status(car_page_parsed)
	page_add_date = get_page_add_date(car_page_parsed)
	after_accident = check_if_after_accident(car_page_parsed)
	extraction_date = get_extraction_date()
	
	df = pd.DataFrame([[year, price_dollar, price_euro, price_grn, uncustomed, after_accident, car_type, body, 
						milage, region, city, transmission, drive_type, doors, seats, color, 
						fuel, engine_v, user_id, additional_data, description, status, page_add_date, extraction_date]],
					columns = ['year', 'price_dollar', 'price_euro', 'price_grn', 'uncustomed', 'after_accident', 'car_type', 'body', 
						'milage', 'region', 'city', 'transmission', 'drive_type', 'doors', 'seats', 'color', 
						'fuel', 'engine_v', 'user_id', 'additional_data', 'description', 'status', 'page_add_date', 'extraction_date'])

	return df


if __name__ == "__main__":
	import logging, argparse, os

	current_dir = os.path.abspath(os.path.dirname(__file__))
	directory = os.path.join(current_dir, 'raw_data')

	parser = argparse.ArgumentParser()
	parser.add_argument("--links_in", type=str, dest = 'cars_links_filename',
						default = "collected_cars_links.csv", help="name of csv file with cars links")
	parser.add_argument("--output_to", type=str, dest = 'output_filename',
						default = "autoria_cars_data.csv", help="name of csv file to write data in")
	args = parser.parse_args()

	logging.basicConfig(level=logging.INFO,
						format='%(asctime)s %(levelname)-4s %(message)s',
						datefmt='%H:%M:%S')
	logger = logging.getLogger(__name__)
	

	logger.info('Reading csv with links on cars ...')
	cars_links = pd.read_csv(os.path.join(directory, args.cars_links_filename), encoding="ISO-8859-1")#"ISO-8859-1"
	logger.info('Got {0} links on cars'.format(cars_links.shape[0]))

	features = ['year', 'price_dollar', 'price_euro', 'price_grn', 'uncustomed', 'after_accident', 'car_type', 'body', 
				'milage', 'region', 'city', 'transmission', 'drive_type', 'doors', 'seats', 'color', 
				'fuel', 'engine_v', 'user_id', 'additional_data', 'description', 'status', 'page_add_date', 'extraction_date']

	logger.info('Parsing cars pages ...')
	cars = pd.DataFrame(columns = features + ['brand', 'model', 'link'])
	m = round(cars_links.shape[0] / 20)
	for i in range(cars_links.shape[0]):
		# print('Parsing car page: ', i)
		df = pd.DataFrame([['']*24], columns = features)
		try:
			df = parse_car_page(cars_links.link[i])
		except:
			pass
		df['brand'] = cars_links.brand[i]
		df['model'] = cars_links.model[i]
		df['link'] = cars_links.link[i]
		cars = cars.append(df, ignore_index = True)
		if i!=0 and i%m == 0:
			logger.info('	Parsed {0}% of car pages'.format(round((100*i)/cars_links.shape[0])))

	cars.to_csv(os.path.join(directory, args.output_filename), index=False)
	logger.info('The data was saved into {0}'.format('raw_data/'+args.output_filename))
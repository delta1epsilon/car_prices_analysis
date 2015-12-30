import unittest
from bs4 import BeautifulSoup
import urllib.request as ur

import os

from get_data.parse_car_page import (get_technical_characteristics, check_if_uncustomed, get_user_id, 
									 get_location, get_milage, get_body, get_car_type, get_year)

def read_case(filename):
	current_dir = os.path.abspath(os.path.dirname(__file__))
	testcase = open(os.path.join(current_dir, 'testcases', filename +'.txt'))
	data = testcase.read()
	testcase.close()
	return BeautifulSoup(data, 'html.parser')

data = read_case('testcase')

class TestGettingDescriptions(unittest.TestCase):

	def test_getting_technical_characteristics(self):
		expected = ('Типтронік', 'Повний', 5, 'Сірий', 5, 'Дизель', '2')
		self.assertEqual(get_technical_characteristics(data), expected)

	def test_checking_if_uncustomed(self):
		expected = 0
		self.assertEqual(check_if_uncustomed(data), expected)

	def test_getting_user_id(self):
		expected = ''
		self.assertEqual(get_user_id(data), expected)

	def test_getting_location(self):
		expected = ('Одеська область', 'Одеса')
		self.assertEqual(get_location(data), expected)

	def test_getting_milage(self):
		expected = ''
		self.assertEqual(get_milage(data), expected)

	def test_getting_body(self):
		expected = 'Позашляховик/Кроссовер'
		self.assertEqual(get_body(data), expected)

	def test_getting_car_type(self):
		expected = 'Легкові'
		self.assertEqual(get_car_type(data), expected)

	def test_getting_year(self):
		expected = 2015
		self.assertEqual(get_year(data), expected)



	






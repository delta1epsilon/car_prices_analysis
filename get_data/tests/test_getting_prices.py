import unittest
from bs4 import BeautifulSoup
import urllib.request as ur

import os

from get_data.parse_car_page import get_prices

def read_case(filename):
	current_dir = os.path.abspath(os.path.dirname(__file__))
	testcase = open(os.path.join(current_dir, 'testcases', filename +'.txt'))
	data = testcase.read()
	testcase.close()
	return BeautifulSoup(data, 'html.parser')

class TestGettingPrices(unittest.TestCase):

	def test_getting_prices1(self):
		data = read_case('price_testcase1')
		expected = ('32000', '28255', '775040')
		self.assertEqual(get_prices(data), expected)

	def test_getting_prices2(self):
		data = read_case('price_testcase2')
		expected = ('32000', '28255', '775040')
		self.assertEqual(get_prices(data), expected)		

	def test_getting_prices3(self):
		data = read_case('price_testcase3')
		expected = ('32000', 'NA', 'NA')
		self.assertEqual(get_prices(data), expected)		

	def test_getting_prices4(self):
		data = read_case('price_testcase4')
		expected = ('NA', 'NA', '775040')
		self.assertEqual(get_prices(data), expected)
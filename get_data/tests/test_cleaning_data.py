import unittest
import pandas as pd
import numpy as np
from pandas.util.testing import assert_frame_equal

from get_data.clean_data import (remove_empty_rows, remove_test_pages, fix_milage)

class TestCleaningData(unittest.TestCase):
	def test_remove_empty_rows(self):
		data = pd.DataFrame([[1, 2, 3, 'a', 'b', 'b'],
							 [None, None, None, 'c', 'd', 'd'],
							 [None, 4, None, 'e', 'f', 'f']], 
							columns=['a', 'b', 'c', 'brand', 'model', 'link'])
		expected = pd.DataFrame([[1, 2, 3, 'a', 'b', 'b'],
								 [None, 4, None, 'e', 'f', 'f']], 
								columns=['a', 'b', 'c', 'brand', 'model', 'link'])
		data = remove_empty_rows(data)
		self.assertEqual(data.shape, expected.shape)
		# self.assertTrue(np.all(remove_empty_rows(data).values == expected.values))

	def test_remove_test_pages(self):
		data = pd.DataFrame([[1, 'scsvs тест-драйв'],
							 [None, 'тест не видаляти'],
							 ['df', 'fаіві тест драйв'],
							 ['fsfs', 'fаіві тест '],
							 ['dffsdfsd', 'fаіві dasdsa']], 
							columns=['a', 'description'])
		expected = pd.DataFrame([[1, 'scsvs тест-драйв'],
								['df', 'fаіві тест драйв'],
								['dffsdfsd', 'fаіві dasdsa']], 
								columns=['a', 'description'])
		cleaned = remove_test_pages(data)
		self.assertTrue(np.all(cleaned.values == expected.values))

	def test_fix_milage(self):
		data = pd.DataFrame([[150000, 'scsvs тест-драйв'],
							 [None, 'тест не видаляти'],
							 [40, 'fаіві тест драйв'],
							 [123456, 'fаіві тест '],
							 [5, 'fаіві dasdsa'],
							 [200, 'fаіві dasdsa']], 
							columns=['milage', 'description'])
		expected = pd.DataFrame([[150, 'scsvs тест-драйв'],
								 [0, 'тест не видаляти'],
								 [40, 'fаіві тест драйв'],
								 [123, 'fаіві тест '],
								 [5, 'fаіві dasdsa'],
								 [200, 'fаіві dasdsa']], 
								columns=['milage', 'description'])
		self.assertTrue(np.all(fix_milage(data).values == expected.values))
import pandas as pd
import numpy as np
import re, time

def remove_empty_rows(table):
	table = table[list(table.columns[:-3])]
	return table.iloc[~np.array(table.apply(lambda x: all(x.isnull()), axis=1))]

def leave_only_cars(table):
	return table[table.car_type == 'Легкові']

def remove_crashed_cars(table):
	return table[table.after_accident != 1]

def remove_test_pages(table):
	description = list(table.description)
	not_test = [re.search('(?!тест-драйв|тест драйв|драйв)(тест)', str(x).lower()) for x in description]
	return table.iloc[[x == None for x in not_test]]

def fix_milage(table):
	milage = table.milage.fillna(0).tolist()
	milage = [str(int(x))[:3].replace('.', '') for x in milage]
	table.milage = [int(x) for x in milage]
	return table

pipe = [('Remove Empty rows', remove_empty_rows), 
		('Leave only cars', leave_only_cars), 
		('Remove cars after accidents', remove_crashed_cars), 
		('Remove test pages', remove_test_pages), 
		('Fix broken milage', fix_milage)]

if __name__ == "__main__":
	import logging, argparse, os

	logging.basicConfig(level=logging.INFO,
						format='%(asctime)s %(levelname)-4s %(message)s',
						datefmt='%H:%M:%S')
	logger = logging.getLogger(__name__)

	parser = argparse.ArgumentParser()
	parser.add_argument('--raw_data_file', type=str, dest='raw_data_file', required=True,
						help="""name of csv file in raw_data directory to be cleaned
								(will be saved to tidy_data directory)""")
	args = parser.parse_args()

	if args.raw_data_file is None:
		raise ValueError("Write path to csv file to be cleaned!")

	current_dir = os.path.abspath(os.path.dirname(__file__))
	directory = os.path.join(current_dir, 'raw_data')

	logger.info('Reading csv with raw cars data')
	data = pd.read_csv(os.path.join(directory, args.raw_data_file), encoding="utf-8")
	logger.info('Got {0} observations'.format(data.shape[0]))



	for procedure_name, func in pipe:
		logger.info("	{}".format(procedure_name))

		nrows = len(data)
		data = func(data)
		n_cleaned_rows = len(data)

		if func != fix_milage:
			logger.info("		Nrows after cleaning procedure: {} ({})".format(
						n_cleaned_rows, n_cleaned_rows - nrows
						))

	logger.info('Dimension of the tidy data is {} x {}'.format(*data.shape))

	directory = os.path.join(current_dir, 'tidy_data')
	data.to_csv(os.path.join(directory, args.raw_data_file), index=False, encoding='utf-8')
	logger.info('The tidy data was saved into {0}'.format('tidy_data/'+args.raw_data_file))
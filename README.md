# Car Prices Analysis

Analysis of ukrainian car prices taken from auto.ria.com.

## Quick start

1. [Get data](#get-data)

## Get data

1. Collect car links for specific brands.

	```
	$ python get_data/collect_cars_links.py -h
	usage: collect_cars_links.py [-h] [--brand CAR_BRANDS [CAR_BRANDS ...]]
	                             [--output_to OUTPUT_FILENAME]

	optional arguments:
	  -h, --help            show this help message and exit
	  --brand CAR_BRANDS [CAR_BRANDS ...]
	                        list of car brands for getting links; Available
	                        brands: Audi, BMW, Mercedes-Benz, Volkswagen, Opel,
	                        Acura, Honda, Lexus, Mazda, Mitsubishi, Nissan,
	                        Subaru, Suzuki, Toyota, Kia, Hyundai, Daewoo,
	                        Chevrolet, Cadillac, Ford, Chrysler, Dodge, Jeep
	  --output_to OUTPUT_FILENAME
	                        name of csv file to write links in
	```

2. Parse car pages.

	```
	$ python get_data/parse_car_page.py -h
	usage: parse_car_page.py [-h] [--links_in CARS_LINKS_FILENAME]
	                         [--output_to OUTPUT_FILENAME]

	optional arguments:
	  -h, --help            show this help message and exit
	  --links_in CARS_LINKS_FILENAME
	                        name of csv file with cars links
	  --output_to OUTPUT_FILENAME
	                        name of csv file to write data in
	```
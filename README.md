# Car Prices Analysis

Analysis of ukrainian car prices taken from auto.ria.com.

## Quick start

1. [Get data](#get-data)
2. [Data cleaning](#data-cleaning)

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
	                        name of csv file to write links in raw_data directory
	                        (raw_data directory will be created if it doesn't
	                        exist)	
    ```

2. Parse car pages.

	```
	$ python get_data/parse_car_page.py -h
	usage: parse_car_page.py [-h] [--links_in CARS_LINKS_FILENAME]
	                         [--output_to OUTPUT_FILENAME]

	optional arguments:
	  -h, --help            show this help message and exit
	  --links_in CARS_LINKS_FILENAME
	                        name of csv file with cars links in raw_data directory
	  --output_to OUTPUT_FILENAME
	                        name of csv file to write data in raw_data directory
	```

The data will contain next self-explaining variables:

1. year
2. price_dollar
3. price_euro
4. price_grn
5. uncustomed
6. after_accident
7. car_type
8. body
9. milage
10. region
11. city
12. transmission
13. drive_type
14. doors
15. seats
16. color 
17. fuel
18. engine_v
19. user_id
20. additional_data
21. description
22. status
23. page_add_date
24. extraction_date
25. brand
26. model
27. link

## Data cleaning

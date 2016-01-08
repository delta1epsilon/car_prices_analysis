from bs4 import BeautifulSoup
import urllib.request as ur
import pandas as pd
import numpy as np
import re

def get_links(url, site_url = 'https://auto.ria.com'):
    def get_cars_links(url, site_url = 'https://auto.ria.com'):
        page = ur.urlopen(url).read()
        parsed_page = BeautifulSoup(page, 'html.parser')

        links = parsed_page.body.find(name = 'div', attrs={'class':'content'}).find_all(name = 'a')
        df = pd.DataFrame(columns = ['brand', 'model', 'link'])
        for i in range(len([x for x in links if not x.string.isdigit()])):
                df.loc[i] = [links[i].string.split(' ', 1)[0],
                             links[i].string.split(' ', 1)[1],
                             site_url + links[i].attrs.get('href', 'CHECK')
                            ]
        return df

    page = ur.urlopen(url).read()
    parsed_page = BeautifulSoup(page, 'html.parser')

    links = parsed_page.body.find(name = 'div', attrs={'class':'content'}).find_all(name = 'a')
    page_numbers_links = [site_url + x.attrs.get('href', 'CHECK') for x in links if x.string.isdigit()]
    if len(page_numbers_links) == 0:
        return get_cars_links(url)
    else:
        df = pd.DataFrame(columns = ['brand', 'model', 'link'])
        for link in page_numbers_links:
            df = df.append(get_cars_links(link), ignore_index = True)
        return df

def get_brands_links(parsed_page):
    map_bu_links = parsed_page.body.find(name = 'div', attrs={'class':'content'}).find_all(name = 'a')
    brand_indexes = {}
    for i in range(len(map_bu_links)):
        if map_bu_links[i].string in target_cars:
            brand_indexes[map_bu_links[i].string] = i

    brand_links = pd.DataFrame(list(brand_indexes.items()), columns = ['brand', 'ind'])
    brand_links['link1'] = ''

    for i in range(brand_links.shape[0]):
        brand_links.loc[i, 'link1'] = site_url + map_bu_links[brand_links.ind[i]].attrs.get('href', 'CHECK')
    return brand_links

def get_models_links(brand_links):
    brand_model = pd.DataFrame(columns = ['brand', 'model', 'link'])
    for j in range(brand_links.shape[0]):    
        brand_model_url = brand_links.link1[j]
        df = get_links(brand_model_url)
        brand_model = brand_model.append(df, ignore_index = True)
    return brand_model

def clean_links(link):
    pattern = re.compile("(все|груз.|пасс.|пас.)", re.I)
    return [pattern.sub('', l) for l in link]

def clean_models(model):
    model = [re.sub('пасс.', 'pass', l) for l in model]
    model = [re.sub('пас.', 'pass', l) for l in model]
    model = [re.sub(' \(все\)', '', l) for l in model]
    return [re.sub('груз.', 'gruz', l) for l in model]

if __name__ == "__main__":
    import logging, argparse, os

    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-4s %(message)s',
                    datefmt='%H:%M:%S')
    logger = logging.getLogger(__name__)

    current_dir = os.path.abspath(os.path.dirname(__file__))
    directory = os.path.join(current_dir, 'raw_data')
    if not os.path.exists(directory):
        os.makedirs(directory)

    target_cars = ['Acura'#'Audi', 'BMW', 'Mercedes-Benz', 'Volkswagen', 'Opel'#, # German - 5 ~72000
                    # 'Acura', 'Honda', 'Lexus', 'Mazda', 'Mitsubishi', 'Nissan', 'Subaru', 'Suzuki', 'Toyota', # Japanese - 9
                    # 'Kia', 'Hyundai'#, 'Daewoo', # Korean - 3
                    # 'Chevrolet', 'Cadillac', 'Ford', 'Chrysler', 'Dodge', 'Jeep' # American - 6
                    ]

    parser = argparse.ArgumentParser()
    parser.add_argument("--brand", type=str, nargs='+', dest = 'car_brands',
                        default = target_cars, 
                        help="""list of car brands for getting links; 
                                Available brands: 
                                    Audi, BMW, Mercedes-Benz, Volkswagen, Opel, 
                                    Acura, Honda, Lexus, Mazda, Mitsubishi, 
                                    Nissan, Subaru, Suzuki, Toyota,
                                    Kia, Hyundai, Daewoo,
                                    Chevrolet, Cadillac, Ford, Chrysler, Dodge, Jeep"""
                        )
    parser.add_argument("--output_to", type=str, dest = 'output_filename',
                        default = "collected_cars_links.csv", 
                        help="""name of csv file to write links in raw_data directory
                                (raw_data directory will be created if it doesn't exist)""")
    args = parser.parse_args()

    target_cars = args.car_brands

    site_url = 'https://auto.ria.com'
    map_bu_url = 'https://auto.ria.com/uk/map/bu/'
    map_bu_page = ur.urlopen(map_bu_url).read()
    map_bu_parsed = BeautifulSoup(map_bu_page, 'html.parser')

    logger.info('Collecting links on brands ...')
    brand_links = get_brands_links(map_bu_parsed)

    logger.info('Collecting links on models ...')
    brand_model = get_models_links(brand_links)

    #====== get cars links
    logger.info('Collecting links on cars ...')
    brand_model_link = pd.DataFrame(columns = ['brand', 'model', 'link'])
    for i in range(brand_model.shape[0]):    
        df = None
        while df is None:
            try:
                df = get_links(brand_model.link[i])
            except:
                pass
        brand_model_link = brand_model_link.append(df, ignore_index = True)

    # remove/replace 'все', 'груз.', 'пасс.' from links and models
    brand_model_link.link = clean_links(brand_model_link.link)
    brand_model_link.model = clean_models(brand_model_link.model)

    brand_model_link.to_csv(os.path.join(directory, args.output_filename))
    logger.info('{0} car links were collected and saved into {1}'.format(brand_model_link.shape[0], 'raw_data/'+args.output_filename))

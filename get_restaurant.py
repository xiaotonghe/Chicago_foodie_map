import pandas as pd
import requests
import json
from bs4 import BeautifulSoup
import geopandas as gpd
import numpy as np
from itertools import product

def get_data(test=1):

    # parameters
    api_key = 'yelpapikey'
    headers = {'Authorization': 'Bearer %s' % api_key}
    url = 'https://api.yelp.com/v3/businesses/search'
    ca = gpd.read_file('Boundaries - Community Areas (current).geojson')
    ca_name = ca['community']
    # categories = [
    #     'burgers', 'thai', 'chinese', 'mexican', 'indian', 'spanish', 'japanese', 'french',
    #     'mediterranean', 'malaysian', 'halal', 'seafood', 'korean',
    #     'bars', 'pubs', 'american(new)', 'fast food', 'salad', 'pizza', 'breakfast & brunch',
    #     'ice cream & frozen yogurt', 'american(traditional)', 'coffee & tea', 'vietnamese'
    # ]
    cols = ['id', 'name', 'image_url', 'url', 'category', 'rating', 'review_count'
            'latitude', 'longtitude', 'price','city', 'state', 'zipcode', 'address', 'phone']
    # get data
    # testing
    listings=[]

    if test == 1:
        print('testing')
        cm_test = ['Lincoln Park', 'Roger Park']
        offset = np.arange(1, 40, 20)
    elif test == 0:
        print('testing')
        cm_test = ['Lincoln Park', 'Roger Park']
        offset = np.arange(1, 40, 20)

    tuples = list(product(cm_test, offset))
        
    for cm, offset in tuples:
        params = {
            'term': 'restaurants',
            'location': cm + ', Chicago, IL',
            'offset':offset
        }
        # make a get request to the API
        req = requests.get(url, params=params, headers=headers)
        req_code = req.status_code
        print(offset)
        print("the status code is {}".format(req_code))

        raw_data = req.json()
        if req_code == 200:
            for business in raw_data['businesses']:
                id = business['id']
                name = business['name']
                image_url = business['image_url']
                url = business['url']
                category = business['categories'][0]['title']
                rating = business['rating']
                review_count = business['review_count']
                latitude = business['coordinates']['latitude']
                longtitude = business['coordinates']['longitude']
                if 'price' in business:
                    price = business['price']
                else:
                    price = 'unknown'
                city = business['location']['city']
                state = business['location']['state']
                zipcode = business['location']['zip_code']
                address = business['location']['address1']
                phone = business['display_phone']
                if id not in listings:
                    listings.append([id, name, image_url, url, category, rating, review_count, latitude, longtitude, price, city, state, zipcode, address, phone])
        else:
            print("Break at the status code {}".format(req_code))
            break
    df = pd.DataFrame.from_records(listings, columns=cols)
    return raw_data

df = get_data(test=1)
print(df)
# df.to_csv('data_test.csv')


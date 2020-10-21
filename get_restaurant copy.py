import pandas as pd
import requests
import json
from bs4 import BeautifulSoup
import geopandas as gpd

def get_data(test=1):

    # parameters
    api_key = '5mmP45AiQV5p20S0a5uyV5gMayS_udYfyFxdEWCky7kfN1Lh3g5kfIHkIWFxmj4rliwZumJWUh4ibiGabWAmqXGEw3tSV6jbYSFOvsmgsV5mpiOIJtDIwuXgSXZFX3Yx'
    headers = {'Authorization': 'Bearer %s' % api_key}
    url = 'https://api.yelp.com/v3/businesses/search'
    ca = gpd.read_file('Boundaries - Community Areas (current).geojson')
    ca_name = ca['community']
    categories = [
        'burgers', 'thai', 'chinese', 'mexican', 'indian', 'spanish', 'japanese', 'french',
        'mediterranean', 'malaysian', 'halal', 'seafood', 'korean',
        'bars', 'pubs', 'american(new)', 'fast food', 'salad', 'pizza', 'breakfast & brunch',
        'ice cream & frozen yogurt', 'american(traditional)', 'coffee & tea', 'vietnamese'
    ]

    # get data
    # testing
    jsonData = []
    raw_data = pd.DataFrame([])

    if test == 1:
        print('testing')
        cm_test = ['Lincoln Park', 'Roger Park']
        for cm in cm_test:
            for offset in range(0,40,20):
                params = {
                    'term': 'restaurants', 'location': cm+', Chicago, IL','offset':offset
                }
                # make a get request to the API
                req = requests.get(url, params=params, headers=headers)
                print(offset)
                req_code = req.status_code
                print("the status code is {}".format(req_code))
                if req_code == 200:
                    j = req.json()['businesses'][0]  # get a list of dict
                    raw_data=j
                    # df_temp = pd.DataFrame.from_dict(j)
                    # raw_data = raw_data.append(df_temp,ignore_index=True,sort=False)
                else:
                    print("Break at the status code {}".format(req_code))
                    break
                    
    # processing    
    elif test == 0:
        for cm in ca_name:
            for offset in range(0, 1000, 20):
                params = {
                    'term': 'restaurants', 'location': cm+', Chicago, IL','offset':offset
                }
                # make a get request to the API
                req = requests.get(url, params=params, headers=headers)
                # proceed only if the  status  code is  200
                print(cm, ': ', offset)
                req_code = req.status_code
                print("the status code is {}".format(req_code))
                if req_code == 200:
                    j = req.json()['businesses']  # get a list of dict
                    df_temp = pd.DataFrame.from_dict(j)
                    raw_data = raw_data.append(df_temp,ignore_index=True,sort=False)
                else:
                    print("Break at the status code {}".format(req_code))
                    break

    # converting json to pd.dataframe
    # print(jsonData)
    # df = pd.DataFrame.from_dict(jsonData)
    
    return raw_data

df = get_data(test=1)
print(df)
# df.to_csv('data_test.csv')


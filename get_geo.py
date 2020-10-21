import pandas as pd
import requests
import json
from bs4 import BeautifulSoup

address = 'lincoln park'
geo_api_key = "googlekey"
geocoding_url = 'https://maps.googleapis.com/maps/api/geocode/json?address={},Chicago,IL&key={}'.format(address, geo_api_key)
request = requests.get(geocoding_url).json()

# print(request['results'][0]['geometry']['location'])
print(request)

